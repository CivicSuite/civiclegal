# CivicLegal

CivicLegal is the CivicSuite internal legal-record research support module. Version 0.1.1 ships deterministic foundations for privilege-aware corpus filtering, citation-first search across city records, prior-action lookup, attorney-reviewed memo scaffolds, ordinance comparison checklists, litigation-hold candidate flags, optional database-backed legal workpapers, authority citation tracking, FastAPI runtime, docs, tests, browser QA, and release gates.

It is intentionally not legal advice, not Westlaw or Lexis, not a court-filing system, not an autonomous legal conclusion engine, and not an external legal-system connector. City attorneys control the corpus, approve outputs, and make all legal judgments.

## Shipping in v0.1.1

- Privilege-tier helpers for public, staff, attorney, and privileged records.
- Citation-first cross-corpus search over supplied city legal records.
- Prior-action lookup with citation output and attorney-review boundary.
- Legal memo draft scaffolds that require attorney review.
- Optional SQLAlchemy-backed memo draft and litigation-hold workpaper records through `CIVICLEGAL_WORKPAPER_DB_URL`.
- Ordinance draft comparison checklists.
- Litigation-hold candidate flagging.
- Attorney-maintained statute/case citation tracking.
- FastAPI runtime with health, public landing page, and deterministic API endpoints.

## Not shipped yet

- Legal advice, Westlaw/Lexis replacement, autonomous legal conclusions, court filing, e-discovery management, live LLM calls, live privileged corpus ingestion, or external legal-system connector runtime.
- Live CivicCode, CivicClerk, or CivicContracts imports. v0.1.1 models the handoff shapes and keeps them deterministic.

## Install

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civiclegal.main:app --host 127.0.0.1 --port 8140
```

CivicLegal v0.1.1 is pinned to `civiccore==0.3.0`.

Set `CIVICLEGAL_WORKPAPER_DB_URL` to persist attorney-review memo drafts and litigation-hold preflight records. Without it, CivicLegal remains deterministic and stateless.

## Documentation

- [User Manual](USER-MANUAL.md)
- [Architecture](docs/architecture.md)
- [Landing Page](docs/index.html)
- [Release Notes](CHANGELOG.md)

Apache 2.0 code. CC BY 4.0 docs.
