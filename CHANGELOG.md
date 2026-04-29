# Changelog

## [0.1.2] - 2026-04-29

### Changed

- Privilege-tier filtering now reuses the shared `civiccore.search` access helpers instead of local-only access comparisons.
- Dependency alignment moved CivicLegal to the published `civiccore` v0.11.0 release wheel.
- Updated verification scripts, runtime tests, package metadata, and current-facing docs for the v0.1.2 release.

## [0.1.1] - 2026-04-28

### Added

- Optional SQLAlchemy-backed memo draft and litigation-hold workpaper records via `CIVICLEGAL_WORKPAPER_DB_URL`.
- Legal memo and litigation-hold retrieval endpoints for persisted records.

### Changed

- Dependency-alignment release: moved CivicLegal to `civiccore==0.3.0` while preserving the existing v0.1.0 runtime foundation behavior.
- Updated CI, verification gates, package metadata, docs, runtime tests, landing page, and public UI labels for the v0.1.1 release.

## [0.1.0] - 2026-04-27

### Added

- CivicLegal package, FastAPI runtime, privilege-aware corpus filtering, citation-first search, precedent lookup, memo scaffolds, ordinance comparison, litigation-hold candidate flags, citation tracking, docs, tests, browser QA, and release gates.

### Not Shipped

- Legal advice, Westlaw/Lexis replacement, autonomous legal conclusions, court filing, e-discovery management, live LLM calls, live privileged corpus ingestion, or external legal-system connector runtime.
