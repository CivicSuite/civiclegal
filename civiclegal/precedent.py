"""Prior-action lookup support."""
from dataclasses import dataclass

from civiclegal.corpus_access import LegalRecord
from civiclegal.search import search_legal_corpus


@dataclass(frozen=True)
class PrecedentLookup:
    question: str
    citations: tuple[str, ...]
    attorney_review_required: bool
    boundary: str


def lookup_precedent(question: str, records: list[LegalRecord], role: str) -> PrecedentLookup:
    hits = search_legal_corpus(question, records, role)
    return PrecedentLookup(
        question.strip(),
        tuple(hit.citation for hit in hits),
        True,
        "CivicLegal surfaces prior city records with citations; it does not make legal conclusions.",
    )
