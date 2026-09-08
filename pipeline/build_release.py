"""Generic release builder for SafeLegalAI datasets (config in dataset.json).

Merges work/agents/<table>-*.jsonl, validates each row against schema/<table>.schema.json,
dedupes, writes data/<table>.{jsonl,csv,parquet}, data/manifest.json and README.md (the
Hugging Face dataset card); --push uploads to huggingface.co/datasets/<org>/<repo>.

    .venv/bin/python pipeline/build_release.py [--push] [--version 0.1.0]
"""
from __future__ import annotations

import argparse, csv, hashlib, json, os, re
from collections import Counter
from datetime import date
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / "dataset.json").read_text())
WORK, DATA = ROOT / "work" / "agents", ROOT / "data"
SITE = "https://safelegalai.com"
HF_ORG = os.environ.get("HF_ORG", "safelegalaidata")
NOTICE = ("Provided as is, without warranty. Not legal advice. SafeLegalAI (Cognesio LLP) records what courts, regulators, "
          "legislatures and vendors' own public pages state; the linked official documents are the record. Names and marks "
          "belong to their owners. Anyone named may reply: https://safelegalai.com/report. Full terms: https://safelegalai.com/disclaimer")


def read_jsonl(p: Path):
    out = []
    for i, l in enumerate(p.open(encoding="utf-8"), 1):
        if l.strip():
            try:
                out.append(json.loads(l))
            except json.JSONDecodeError as e:
                print(f"  ! {p.name}:{i} bad JSON ({e}) — skipped")
    return out


def is_banned(url, banned) -> bool:
    """Exact host or subdomain match only (so bloomberglaw.com is not caught by law.com)."""
    if not url:
        return False
    from urllib.parse import urlparse
    host = (urlparse(url).hostname or "").lower()
    return any(host == b or host.endswith("." + b) for b in banned)


def flatten(r: dict) -> dict:
    """Parquet/CSV-friendly: nested objects and arrays become JSON strings."""
    return {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v) for k, v in r.items()}


def build_table(tname: str, tcfg: dict, version: str):
    schema = json.loads((ROOT / "schema" / f"{tname}.schema.json").read_text())
    validator = jsonschema.Draft202012Validator(schema)
    idf, banned = tcfg["id_field"], tuple(CFG.get("banned_hosts", []))
    rows, rejected, seen = [], [], {}
    files = sorted(WORK.glob(f"{tname}-*.jsonl")) + ([WORK / f"{tname}.jsonl"] if (WORK / f"{tname}.jsonl").exists() else [])
    for f in files:
        for r in read_jsonl(f):
            errs = [e.message for e in validator.iter_errors(r)]
            for uf in tcfg.get("url_fields", ["source_url"]):
                if is_banned(r.get(uf), banned):
                    errs.append(f"{uf} is a banned host")
            if errs:
                rejected.append({"file": f.name, "id": r.get(idf), "errors": errs[:6]})
                continue
            key = r[idf]
            dk = tuple((r.get(k) or "").strip().lower() if isinstance(r.get(k), str) else r.get(k) for k in tcfg.get("dedupe_fields", []))
            if key in seen or (dk and any(dk == d for d in seen.values())):
                # keep the row with the richer verification / more fields
                prev = next(i for i, x in enumerate(rows) if x[idf] == key or (dk and tuple((x.get(k) or "").strip().lower() if isinstance(x.get(k), str) else x.get(k) for k in tcfg.get("dedupe_fields", [])) == dk))
                if len(json.dumps(r)) > len(json.dumps(rows[prev])):
                    rows[prev] = r
                    seen[key] = dk
                continue
            seen[key] = dk
            rows.append(r)
    rows.sort(key=lambda r: (str(r.get(tcfg.get("sort_field", idf)) or ""), r[idf]), reverse=tcfg.get("sort_desc", False))
    for r in rows:
        r.setdefault("url", f"{SITE}{tcfg['site_path'].format(**{idf: r[idf]})}" if tcfg.get("site_path") else None)
        r["notice"] = NOTICE
    DATA.mkdir(exist_ok=True)
    (DATA / f"{tname}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    flat = [flatten(r) for r in rows]
    cols = sorted({k for r in flat for k in r}, key=lambda c: (c != idf, c))
    with (DATA / f"{tname}.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(flat)
    import pyarrow as pa, pyarrow.parquet as pq
    strflat = [{c: (None if r.get(c) is None else (r[c] if isinstance(r[c], (int, float, bool)) else str(r[c]))) for c in cols} for r in flat]
    # unify mixed-type columns as strings
    for c in cols:
        types = {type(r[c]) for r in strflat if r[c] is not None}
        if len(types) > 1:
            for r in strflat:
                if r[c] is not None:
                    r[c] = str(r[c])
    pq.write_table(pa.Table.from_pylist(strflat), DATA / f"{tname}.parquet", compression="zstd")
    if rejected:
        (ROOT / "work" / f"rejected-{tname}.json").write_text(json.dumps(rejected, indent=1, ensure_ascii=False))
    stats = {"rows": len(rows), "rejected": len(rejected)}
    for f in tcfg.get("count_fields", []):
        vals = []
        for r in rows:
            v = r.get(f)
            vals.extend(v if isinstance(v, list) else [v])
        stats[f"by_{f}"] = dict(Counter(str(v) for v in vals if v is not None).most_common(40))
    print(f"{tname}: {len(rows)} rows, {len(rejected)} rejected")
    return rows, stats


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--push", action="store_true"); ap.add_argument("--version", default=CFG.get("version", "0.1.0"))
    a = ap.parse_args()
    manifest = {"dataset": CFG["pretty_name"], "version": a.version, "built": date.today().isoformat(), "canonical": SITE + CFG["canonical_path"],
                "repository": f"https://github.com/SafeLegalAI/{CFG['repo']}", "huggingface": f"https://huggingface.co/datasets/{HF_ORG}/{CFG['repo']}",
                "license_data": "CC BY 4.0 (SafeLegalAI, Cognesio LLP); underlying official documents keep their own status (see NOTICE)",
                "notice": NOTICE, "tables": {}}
    tables = {}
    for tname, tcfg in CFG["tables"].items():
        rows, stats = build_table(tname, tcfg, a.version)
        tables[tname] = rows
        manifest["tables"][tname] = {"file": f"data/{tname}.jsonl", "schema": f"schema/{tname}.schema.json", "stats": stats}
    (DATA / "manifest.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    (ROOT / "README.md").write_text(card(tables, manifest), encoding="utf-8")
    if a.push:
        from huggingface_hub import HfApi
        api = HfApi(token=os.environ.get("HF_TOKEN"))
        rid = f"{HF_ORG}/{CFG['repo']}"
        api.create_repo(rid, repo_type="dataset", exist_ok=True)
        api.upload_folder(repo_id=rid, repo_type="dataset", folder_path=str(DATA), path_in_repo="data", commit_message=f"v{a.version}")
        api.upload_folder(repo_id=rid, repo_type="dataset", folder_path=str(ROOT / "schema"), path_in_repo="schema", commit_message=f"schema v{a.version}")
        for fn in ("README.md", "DISCLAIMER.md", "NOTICE"):
            api.upload_file(path_or_fileobj=str(ROOT / fn), path_in_repo=fn, repo_id=rid, repo_type="dataset", commit_message=f"{fn} v{a.version}")
        print("pushed", f"https://huggingface.co/datasets/{rid}")


def card(tables: dict, manifest: dict) -> str:
    cfgs = "\n".join(
        f"  - config_name: {t}\n{'    default: true' + chr(10) if i == 0 else ''}    data_files:\n      - split: train\n        path: data/{t}.parquet"
        for i, t in enumerate(CFG["tables"]))
    total = sum(len(v) for v in tables.values())
    size = "n<1K" if total < 1000 else "1K<n<10K"
    counts = "\n".join(f"| `{t}` | {len(rows)} | {CFG['tables'][t]['row_is']} |" for t, rows in tables.items())
    statblocks = []
    for t, tcfg in CFG["tables"].items():
        st = manifest["tables"][t]["stats"]
        for f in tcfg.get("count_fields", [])[:3]:
            lines = "\n".join(f"| {k} | {v} |" for k, v in list(st.get(f"by_{f}", {}).items())[:15])
            statblocks.append(f"### `{t}` by `{f}`\n\n| value | rows |\n|---|---|\n{lines}\n")
    gh = manifest["repository"]; hf = manifest["huggingface"]; can = manifest["canonical"]
    ATTRIBUTION = ("\n**Attribution for leads.** " + CFG["attribution"] + "\n") if CFG.get("attribution") else ""
    return f"""---
license: cc-by-4.0
pretty_name: "{CFG['pretty_name']} (SafeLegalAI)"
language:
  - en
size_categories:
  - {size}
tags:
{chr(10).join('  - ' + t for t in dict.fromkeys(CFG['tags'] + ['legal', 'law', 'courts', 'ai-regulation', 'ai-safety', 'ai-governance', 'safelegalai']))}
configs:
{cfgs}
---

# {CFG['title']}

**{CFG['headline'].format(**{f'n_{t}': len(rows) for t, rows in tables.items()})}**

Built {manifest['built']} by [SafeLegalAI]({SITE}) (Cognesio LLP). Canonical pages: [{can.removeprefix('https://')}]({can}) · repository, pipeline and issues: [{gh}]({gh}) · this mirror: [{hf}]({hf}).

| table | rows | one row is |
|---|---|---|
{counts}

Every row carries `source_url`, `fetched_at` and, where the Wayback Machine accepted the page, `archive_url`; `url` links the canonical page on safelegalai.com; `notice` carries the terms below. Full schemas: `schema/`.

{CFG['what_a_row_is']}

{chr(10).join(statblocks)}
## Method

{CFG['method']}
{ATTRIBUTION}
SafeLegalAI records what courts, regulators, legislatures and vendors' own public pages state; it does not infer, rank or advise. Coding columns are SafeLegalAI's good-faith reading for comparison, not findings about any person or body. Corrections and right of reply: [{SITE.removeprefix('https://')}/report]({SITE}/report).

## Licence and notices

{CFG['licence_note']} The compilation and coding are **CC BY 4.0** — attribute *SafeLegalAI ({SITE.removeprefix('https://')}), published by Cognesio LLP*. Code is Apache-2.0.

{NOTICE} See `DISCLAIMER.md` and `NOTICE` in this repository.

## Uses

**Suited to:** counting and comparing what the record shows (by court, jurisdiction, date, actor, outcome, status); building watch-lists and alerts from `source_url`/`fetched_at`; grounding retrieval or summarisation on cited primary documents; teaching and library guides that need a dated, sourced list.

**Not suited to:** ranking products, people or courts; inferring prevalence beyond what a court or regulator has itself stated; any use that treats a coding column as a finding of fact or law. Where a row names a person or organisation it does so as they appear in a public document; anyone named may request a correction or right of reply at {SITE}/report.

## Cite

> SafeLegalAI (Cognesio LLP), "{CFG['title']}", v{manifest['version']}, {manifest['built']}. {hf} — CC BY 4.0. Canonical: {can}

```bibtex
@dataset{{safelegalai_{CFG['repo'].replace('-', '_')}_{manifest['version'].replace('.', '_')},
  title        = {{{CFG['title']}}},
  author       = {{{{SafeLegalAI (Cognesio LLP)}}}},
  year         = {{{manifest['built'][:4]}}},
  version      = {{{manifest['version']}}},
  url          = {{{can}}},
  note         = {{Mirror: {hf}. Data CC BY 4.0. Built {manifest['built']}.}}
}}
```
"""


if __name__ == "__main__":
    main()
