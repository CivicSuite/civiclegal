"""Attorney-reviewed legal memo drafting support."""
from dataclasses import dataclass


@dataclass(frozen=True)
class LegalMemoDraft:
    topic: str
    sections: tuple[str, ...]
    attorney_review_required: bool
    not_legal_advice: bool


def draft_legal_memo(topic: str, cited_sources: list[str]) -> LegalMemoDraft:
    sources = tuple(source.strip() for source in cited_sources if source.strip()) or (
        "Attorney must add controlling authority and city-record citations.",
    )
    return LegalMemoDraft(
        topic.strip(),
        (
            "Issue presented",
            "City record background",
            *sources,
            "Open questions for attorney review",
            "Attorney signature required before use",
        ),
        True,
        True,
    )
