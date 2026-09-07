"""Best-effort Wayback Machine snapshots for rows whose archive_url is null.

Walks work/agents/*.jsonl, calls Save Page Now once per distinct source_url (≤ 1 request / 6 s,
identified UA), writes the resulting https://web.archive.org/web/<ts>/<url> back into every row
that shares the URL. Failures are left null; nothing is retried in the same run.

    .venv/bin/python pipeline/archive.py [--max N] [--delay 6]
"""
from __future__ import annotations

import argparse, json, re, time, urllib.request, urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UA = "SafeLegalAI-Bot/1.0 (+https://safelegalai.com/datasets; hello@safelegalai.com)"


def save(url: str) -> str | None:
    req = urllib.request.Request(f"https://web.archive.org/save/{url}", method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            loc = r.headers.get("Content-Location") or r.headers.get("Location") or ""
            if loc.startswith("/web/"):
                return "https://web.archive.org" + loc
            final = r.geturl()
            return final if "/web/" in final else None
    except urllib.error.HTTPError as e:
        loc = e.headers.get("Content-Location") or e.headers.get("Location") or ""
        return "https://web.archive.org" + loc if loc.startswith("/web/") else None
    except Exception:
        return None


def available(url: str) -> str | None:
    """Fall back to the newest existing capture."""
    try:
        with urllib.request.urlopen(urllib.request.Request(f"https://archive.org/wayback/available?url={urllib.parse.quote(url, safe='')}", headers={"User-Agent": UA}), timeout=30) as r:
            d = json.load(r)
            return (d.get("archived_snapshots") or {}).get("closest", {}).get("url")
    except Exception:
        return None


def main():
    import urllib.parse  # noqa: F401 (used in available)
    ap = argparse.ArgumentParser(); ap.add_argument("--max", type=int, default=400); ap.add_argument("--delay", type=float, default=6.0)
    a = ap.parse_args()
    files = sorted((ROOT / "work" / "agents").glob("*.jsonl"))
    rows_by_file = {f: [json.loads(l) for l in f.open(encoding="utf-8") if l.strip()] for f in files}
    todo = {}
    for rows in rows_by_file.values():
        for r in rows:
            if r.get("source_url") and not r.get("archive_url"):
                todo.setdefault(r["source_url"], None)
    print(f"{len(todo)} distinct URLs without archive_url")
    done = 0
    for url in list(todo)[: a.max]:
        snap = save(url) or available(url)
        todo[url] = snap
        done += 1
        if done % 25 == 0:
            print(f"  {done} tried, {sum(1 for v in todo.values() if v)} archived")
        time.sleep(a.delay)
    changed = 0
    for f, rows in rows_by_file.items():
        n = 0
        for r in rows:
            if not r.get("archive_url") and todo.get(r.get("source_url")):
                r["archive_url"] = todo[r["source_url"]]
                n += 1
        if n:
            f.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
            changed += n
    print(f"archive: {sum(1 for v in todo.values() if v)}/{done} URLs archived; {changed} rows updated")


if __name__ == "__main__":
    main()
