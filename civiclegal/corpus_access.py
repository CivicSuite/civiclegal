"""Privilege-tier helpers for CivicLegal."""
from dataclasses import dataclass
from enum import StrEnum

from civiccore.search import (
    access_level_allows,
    filter_records_by_access_level,
    normalize_access_value,
)


class AccessTier(StrEnum):
    PUBLIC = "public"
    STAFF = "staff"
    ATTORNEY = "attorney"
    PRIVILEGED = "privileged"


@dataclass(frozen=True)
class LegalRecord:
    record_id: str
    title: str
    corpus: str
    text: str
    citation: str
    access_tier: AccessTier = AccessTier.STAFF


ROLE_TIERS: dict[str, AccessTier] = {
    "resident": AccessTier.PUBLIC,
    "staff": AccessTier.STAFF,
    "clerk": AccessTier.STAFF,
    "paralegal": AccessTier.ATTORNEY,
    "attorney": AccessTier.PRIVILEGED,
    "city_attorney": AccessTier.PRIVILEGED,
}

_TIER_RANK = {
    AccessTier.PUBLIC: 0,
    AccessTier.STAFF: 1,
    AccessTier.ATTORNEY: 2,
    AccessTier.PRIVILEGED: 3,
}


def normalize_tier(value: str | AccessTier) -> AccessTier:
    if isinstance(value, AccessTier):
        return value
    normalized = normalize_access_value(value)
    try:
        return AccessTier(normalized)
    except ValueError as exc:
        raise ValueError(f"unknown access tier: {value}") from exc


def tier_for_role(role: str) -> AccessTier:
    normalized = normalize_access_value(role)
    if normalized not in ROLE_TIERS:
        raise ValueError(f"unknown legal role: {role}")
    return ROLE_TIERS[normalized]


def can_access(user_tier: str | AccessTier, record_tier: str | AccessTier) -> bool:
    return access_level_allows(
        normalize_tier(user_tier).value,
        normalize_tier(record_tier).value,
        level_ranks={tier.value: rank for tier, rank in _TIER_RANK.items()},
    )


def filter_accessible_records(
    records: list[LegalRecord],
    role: str,
) -> list[LegalRecord]:
    user_tier = tier_for_role(role)
    return filter_records_by_access_level(
        records,
        user_level=user_tier.value,
        level_ranks={tier.value: rank for tier, rank in _TIER_RANK.items()},
        access_level_for=lambda record: record.access_tier.value,
    )
