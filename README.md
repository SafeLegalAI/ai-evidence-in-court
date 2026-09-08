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

> Part of the [SafeLegalAI datasets](https://safelegalai.com/datasets) — CC BY 4.0, mirrored on [Hugging Face](https://huggingface.co/datasets/safelegalaidata/ai-evidence-in-court). Every row links to its record page and its primary source. Found an error in a row? [Open an issue](https://github.com/SafeLegalAI/ai-evidence-in-court/issues/new?template=row-error.yml) or use [safelegalai.com/report](https://safelegalai.com/report).

**60 court decisions worldwide on AI-generated, AI-altered or AI-"enhanced" evidence, deepfake defences and AI outputs tendered as evidence, coded by evidence type, challenge and ruling, plus 10 rules, proposals and guidance instruments with dated status (including proposed Federal Rule of Evidence 707).**

Built 2026-09-07 by [SafeLegalAI](https://safelegalai.com) (Cognesio LLP). Canonical pages: [safelegalai.com/courts/evidence](https://safelegalai.com/courts/evidence) · repository, pipeline and issues: [https://github.com/SafeLegalAI/ai-evidence-in-court](https://github.com/SafeLegalAI/ai-evidence-in-court) · this mirror: [https://huggingface.co/datasets/safelegalaidata/ai-evidence-in-court](https://huggingface.co/datasets/safelegalaidata/ai-evidence-in-court).

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

## Cite

> SafeLegalAI (Cognesio LLP), "AI-generated evidence and deepfakes in court", v0.1.1, 2026-09-07. https://huggingface.co/datasets/safelegalaidata/ai-evidence-in-court — CC BY 4.0. Canonical: https://safelegalai.com/courts/evidence
