CivicLegal v0.1.1 is the CivicSuite internal legal-record research support module.

Shipping: privilege-aware corpus filtering, citation-first city-record search, prior-action lookup, attorney-reviewed memo scaffolds, ordinance comparison checklists, litigation-hold candidate flags, optional database-backed memo/hold workpapers, authority citation tracking, FastAPI runtime, docs, tests, and browser QA evidence.

Boundaries: CivicLegal is not legal advice, not Westlaw or Lexis, not a court-filing system, not an autonomous legal conclusion engine, not an e-discovery platform, not a live LLM runtime, and not an external legal-system connector.

Install:
python -m pip install -e ".[dev]"
python -m uvicorn civiclegal.main:app --host 127.0.0.1 --port 8140

Dependency: civiccore==0.3.0.

Set CIVICLEGAL_WORKPAPER_DB_URL to persist attorney-review memo drafts and litigation-hold preflight records. Without it, CivicLegal remains deterministic and stateless.
