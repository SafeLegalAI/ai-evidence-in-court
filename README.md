---
license: cc-by-4.0
pretty_name: "AI-generated evidence and deepfakes in court — decisions and rule status (SafeLegalAI)"
language:
  - en
size_categories:
  - n<1K
tags:
  - courts
  - evidence
  - deepfakes
  - authentication
  - fre-707
  - generative-ai
  - legal
  - law
  - ai-regulation
  - ai-safety
  - ai-governance
  - safelegalai
configs:
  - config_name: decisions
    default: true
    data_files:
      - split: train
        path: data/decisions.parquet
  - config_name: instruments
    data_files:
      - split: train
        path: data/instruments.parquet
---

# AI-generated evidence and deepfakes in court

**60 court decisions worldwide on AI-generated, AI-altered or AI-"enhanced" evidence, deepfake defences and AI outputs tendered as evidence, coded by evidence type, challenge and ruling, plus 10 rules, proposals and guidance instruments with dated status (including proposed Federal Rule of Evidence 707).**

Built 2026-09-08 by [SafeLegalAI](https://safelegalai.com) (Cognesio LLP). Canonical pages: [safelegalai.com/courts/evidence](https://safelegalai.com/courts/evidence) · repository, pipeline and issues: [https://github.com/SafeLegalAI/ai-evidence-in-court](https://github.com/SafeLegalAI/ai-evidence-in-court) · this mirror: [https://huggingface.co/datasets/safelegalaidata/ai-evidence-in-court](https://huggingface.co/datasets/safelegalaidata/ai-evidence-in-court).

| table | rows | one row is |
|---|---|---|
| `decisions` | 60 | one ruling on AI-generated/altered evidence or a deepfake challenge |
| `instruments` | 10 | one rule, proposal, statute or guidance on AI-generated evidence |

Every row carries `source_url`, `fetched_at` and, where the Wayback Machine accepted the page, `archive_url`; `url` links the canonical page on safelegalai.com; `notice` carries the terms below. Full schemas: `schema/`.

A `decisions` row is one ruling: `evidence_type`, `ai_role` (alleged-deepfake · ai-enhanced · ai-generated-submitted · acknowledged-ai-output · deepfake-defence · voice-clone), `offered_by`, `challenge`, `ruling` (admitted · excluded · authentication-ordered · expert-required · no-weight · sanction · not-adjudicated), `rules_cited[]`, the court's finding quoted (`court_finding_quote`), a 40–60-word summary and `sensitive`/`publication_ban_checked` flags. An `instruments` row is one rule, proposed rule, statute, bench card or guidance with `status`, `status_date`, `status_quote`, `next_event` and the `operative_text`.

### `decisions` by `country`

| value | rows |
|---|---|
| US | 23 |
| CA | 14 |
| AU | 5 |
| NL | 3 |
| IN | 3 |
| FR | 2 |
| IT | 2 |
| IL | 2 |
| GB | 2 |
| ES | 1 |
| NZ | 1 |
| BE | 1 |
| CO | 1 |

### `decisions` by `ai_role`

| value | rows |
|---|---|
| acknowledged-ai-output | 32 |
| alleged-deepfake | 15 |
| ai-generated-submitted | 5 |
| voice-clone | 3 |
| deepfake-defence | 3 |
| ai-enhanced | 1 |
| other | 1 |

### `decisions` by `ruling`

| value | rows |
|---|---|
| no-weight | 22 |
| admitted | 16 |
| other | 8 |
| excluded | 6 |
| not-adjudicated | 5 |
| sanction | 2 |
| authentication-ordered | 1 |

### `instruments` by `status`

| value | rows |
|---|---|
| in-force | 4 |
| published | 4 |
| under-study | 1 |
| not-advanced | 1 |

### `instruments` by `type`

| value | rows |
|---|---|
| rule | 2 |
| proposed-rule | 2 |
| bench-card | 2 |
| guidance | 2 |
| survey | 1 |
| statute | 1 |

### `instruments` by `country`

| value | rows |
|---|---|
| US | 7 |
| CA | 1 |
| GB | 1 |
| IN | 1 |

## Method

Leads: Damien Charlotin's CC0 deepfakes and AI-evidence databases, the Federal Judicial Center survey in the May 2026 Evidence Rules agenda book, CourtListener discovery searches, news. Every US decision was read from the court's own site or the public RECAP archive; Canadian, Australian and UK decisions were read by a human one at a time on CanLII/AustLII/Find Case Law and are linked, not reproduced. Rule status is taken from uscourts.gov committee materials and legislatures and re-checked after each committee meeting. No media is hosted or linked.

SafeLegalAI records what courts, regulators, legislatures and vendors' own public pages state; it does not infer, rank or advise. Coding columns are SafeLegalAI's good-faith reading for comparison, not findings about any person or body. Corrections and right of reply: [safelegalai.com/report](https://safelegalai.com/report).

## Licence and notices

US opinions and federal committee materials are public domain; state statutes are edicts. Non-US judgments are quoted at ≤25 words and linked. The compilation and coding are **CC BY 4.0** — attribute *SafeLegalAI (safelegalai.com), published by Cognesio LLP*. Code is Apache-2.0.

Provided as is, without warranty. Not legal advice. SafeLegalAI (Cognesio LLP) records what courts, regulators, legislatures and vendors' own public pages state; the linked official documents are the record. Names and marks belong to their owners. Anyone named may reply: https://safelegalai.com/report. Full terms: https://safelegalai.com/disclaimer See `DISCLAIMER.md` and `NOTICE` in this repository.

## Uses

**Suited to:** counting and comparing what the record shows (by court, jurisdiction, date, actor, outcome, status); building watch-lists and alerts from `source_url`/`fetched_at`; grounding retrieval or summarisation on cited primary documents; teaching and library guides that need a dated, sourced list.

**Not suited to:** ranking products, people or courts; inferring prevalence beyond what a court or regulator has itself stated; any use that treats a coding column as a finding of fact or law. Where a row names a person or organisation it does so as they appear in a public document; anyone named may request a correction or right of reply at https://safelegalai.com/report.

## Cite

> SafeLegalAI (Cognesio LLP), "AI-generated evidence and deepfakes in court", v0.1.1, 2026-09-08. https://huggingface.co/datasets/safelegalaidata/ai-evidence-in-court — CC BY 4.0. Canonical: https://safelegalai.com/courts/evidence

```bibtex
@dataset{safelegalai_ai_evidence_in_court_0_1_1,
  title        = {AI-generated evidence and deepfakes in court},
  author       = {{SafeLegalAI (Cognesio LLP)}},
  year         = {2026},
  version      = {0.1.1},
  url          = {https://safelegalai.com/courts/evidence},
  note         = {Mirror: https://huggingface.co/datasets/safelegalaidata/ai-evidence-in-court. Data CC BY 4.0. Built 2026-09-08.}
}
```
