# CivicLegal Architecture

CivicLegal v0.1.0 accepts city-controlled legal records, applies access-tier filtering, returns citation-first search/precedent outputs, and creates attorney-reviewed drafting aids.

![CivicLegal architecture](architecture-civiclegal.svg)

## Current Components

- FastAPI runtime.
- Access-tier filtering.
- Citation-first search and precedent lookup.
- Attorney-reviewed memo and ordinance comparison scaffolds.
- Litigation-hold candidate flagging.
- Citation tracker for attorney-maintained authorities.

## Boundaries

No legal advice, Westlaw/Lexis replacement, autonomous legal conclusions, court filing, e-discovery management, live LLM calls, or external legal-system connector runtime ships in v0.1.0.
