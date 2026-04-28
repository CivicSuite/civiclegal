"""Litigation-hold preflight helpers."""
from dataclasses import dataclass

from civiclegal.corpus_access import LegalRecord


@dataclass(frozen=True)
class LitigationHoldFlag:
    matter: str
    flagged_record_ids: tuple[str, ...]
    hold_review_required: bool


def flag_litigation_hold_candidates(matter: str, records: list[LegalRecord]) -> LitigationHoldFlag:
    terms = [term.lower() for term in matter.split() if term.strip()]
    ids = tuple(
        record.record_id
        for record in records
        if any(term in f"{record.title} {record.text}".lower() for term in terms)
    )
    return LitigationHoldFlag(matter.strip(), ids, True)
