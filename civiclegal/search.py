"""Citation-first cross-corpus legal search helpers."""
from dataclasses import dataclass

from civiclegal.corpus_access import LegalRecord, filter_accessible_records


@dataclass(frozen=True)
class SearchHit:
    record_id: str
    title: str
    corpus: str
    citation: str
    excerpt: str
    access_tier: str


def search_legal_corpus(
    query: str,
    records: list[LegalRecord],
    role: str,
    *,
    limit: int = 5,
) -> list[SearchHit]:
    terms = [term.lower() for term in query.split() if term.strip()]
    accessible = filter_accessible_records(records, role)
    hits: list[SearchHit] = []
    for record in accessible:
        haystack = f"{record.title} {record.text} {record.citation}".lower()
        if not terms or any(term in haystack for term in terms):
            hits.append(
                SearchHit(
                    record.record_id,
                    record.title,
                    record.corpus,
                    record.citation,
                    record.text[:220],
                    record.access_tier.value,
                )
            )
    return hits[:limit]
