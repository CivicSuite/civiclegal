"""Ordinance comparison helpers."""
from dataclasses import dataclass


@dataclass(frozen=True)
class OrdinanceComparison:
    proposed_title: str
    prior_citations: tuple[str, ...]
    review_notes: tuple[str, ...]
    attorney_review_required: bool


def compare_ordinance_draft(proposed_title: str, prior_citations: list[str]) -> OrdinanceComparison:
    citations = tuple(c.strip() for c in prior_citations if c.strip()) or (
        "No prior citations supplied; attorney must add prior-version comparison.",
    )
    return OrdinanceComparison(
        proposed_title.strip(),
        citations,
        (
            "Compare definitions and enforcement language against prior versions.",
            "Confirm codifier formatting outside CivicLegal.",
            "Attorney review required before introduction.",
        ),
        True,
    )
