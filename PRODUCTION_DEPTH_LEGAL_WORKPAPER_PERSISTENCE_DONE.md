# Production Depth: Legal Workpaper Persistence

## Summary

CivicLegal now supports optional SQLAlchemy-backed attorney-review memo draft and litigation-hold preflight records through `CIVICLEGAL_WORKPAPER_DB_URL`.

## Shipped

- `LegalWorkpaperRepository` with schema-aware SQLAlchemy tables.
- Persisted legal memo draft records with `memo_id`.
- Persisted litigation-hold preflight records with `hold_id`.
- Retrieval endpoints:
  - `GET /api/v1/civiclegal/memo/{memo_id}`
  - `GET /api/v1/civiclegal/litigation-hold/{hold_id}`
- Actionable `503` guidance when persistence is not configured.
- Regression tests for repository reload, API round trip, missing-record `404`, no-config `503`, and stateless fallback behavior.

## Still Not Shipped

- Legal advice.
- Westlaw/Lexis replacement.
- Autonomous legal conclusions.
- Court filing.
- E-discovery management.
- Live LLM calls.
- Legal-system connectors.
