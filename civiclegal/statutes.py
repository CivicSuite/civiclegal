"""Attorney-maintained statute and case citation tracking."""
from dataclasses import dataclass


@dataclass(frozen=True)
class CitationTracker:
    topic: str
    citations: tuple[str, ...]
    attorney_maintained: bool
    boundary: str


def track_authority_citations(topic: str, citations: list[str]) -> CitationTracker:
    normalized = tuple(citation.strip() for citation in citations if citation.strip())
    return CitationTracker(
        topic.strip(),
        normalized,
        True,
        "Attorney-maintained citation list only; CivicLegal does not replace Westlaw or Lexis.",
    )
