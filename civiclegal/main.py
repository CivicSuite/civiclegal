"""FastAPI runtime foundation for CivicLegal."""
from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civiclegal import __version__
from civiclegal.corpus_access import AccessTier, LegalRecord, filter_accessible_records
from civiclegal.litigation_hold import flag_litigation_hold_candidates
from civiclegal.memo import draft_legal_memo
from civiclegal.ordinance import compare_ordinance_draft
from civiclegal.precedent import lookup_precedent
from civiclegal.public_ui import render_public_lookup_page
from civiclegal.search import search_legal_corpus
from civiclegal.statutes import track_authority_citations

app = FastAPI(
    title="CivicLegal",
    version=__version__,
    description="Internal legal-corpus lookup, privilege-aware search, and attorney-reviewed drafting support for CivicSuite.",
)

SAMPLE_RECORDS = [
    LegalRecord("code-1", "Noise ordinance", "code", "Quiet hours and variance standards.", "Code 8.12", AccessTier.PUBLIC),
    LegalRecord("min-1", "Prior council discussion", "minutes", "Council discussed downtown noise in 2024.", "Minutes 2024-06-11", AccessTier.STAFF),
    LegalRecord("memo-1", "Attorney memo", "legal_opinion", "Privileged work product on litigation strategy.", "Attorney Memo 2025-02", AccessTier.PRIVILEGED),
]


class SearchRequest(BaseModel):
    query: str
    role: str = "staff"


class PrecedentRequest(BaseModel):
    question: str
    role: str = "staff"


class MemoRequest(BaseModel):
    topic: str
    cited_sources: list[str]


class OrdinanceRequest(BaseModel):
    proposed_title: str
    prior_citations: list[str]


class HoldRequest(BaseModel):
    matter: str


class CitationRequest(BaseModel):
    topic: str
    citations: list[str]


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "CivicLegal",
        "version": __version__,
        "status": "internal legal-corpus foundation",
        "message": (
            "CivicLegal package, API foundation, privilege-aware record filtering, citation-first "
            "search, precedent lookup, memo draft scaffolds, ordinance comparison, litigation-hold "
            "candidate flags, citation tracking, and public UI foundation are online; legal advice, "
            "Westlaw/Lexis replacement, autonomous legal conclusions, live LLM calls, court filing, "
            "and external legal-system connector runtime are not implemented yet."
        ),
        "next_step": "Post-v0.1.1 roadmap: attorney-managed corpus imports, legal review queues, and cross-module handoffs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "civiclegal",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civiclegal", response_class=HTMLResponse)
def public_civiclegal_page() -> str:
    return render_public_lookup_page()


@app.post("/api/v1/civiclegal/search")
def search(request: SearchRequest) -> dict[str, object]:
    return {"hits": [hit.__dict__ for hit in search_legal_corpus(request.query, SAMPLE_RECORDS, request.role)]}


@app.post("/api/v1/civiclegal/precedent")
def precedent(request: PrecedentRequest) -> dict[str, object]:
    return lookup_precedent(request.question, SAMPLE_RECORDS, request.role).__dict__


@app.post("/api/v1/civiclegal/memo")
def memo(request: MemoRequest) -> dict[str, object]:
    return draft_legal_memo(request.topic, request.cited_sources).__dict__


@app.post("/api/v1/civiclegal/ordinance-comparison")
def ordinance_comparison(request: OrdinanceRequest) -> dict[str, object]:
    return compare_ordinance_draft(request.proposed_title, request.prior_citations).__dict__


@app.post("/api/v1/civiclegal/litigation-hold")
def litigation_hold(request: HoldRequest) -> dict[str, object]:
    return flag_litigation_hold_candidates(request.matter, SAMPLE_RECORDS).__dict__


@app.post("/api/v1/civiclegal/citation-tracker")
def citation_tracker(request: CitationRequest) -> dict[str, object]:
    return track_authority_citations(request.topic, request.citations).__dict__


@app.get("/api/v1/civiclegal/accessible-records/{role}")
def accessible_records(role: str) -> dict[str, object]:
    return {"records": [record.__dict__ for record in filter_accessible_records(SAMPLE_RECORDS, role)]}

@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Return an empty favicon response so browser QA has a clean console."""

    return Response(status_code=204)
