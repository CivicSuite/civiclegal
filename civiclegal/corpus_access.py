"""Privilege-tier helpers for CivicLegal."""
from dataclasses import dataclass
from enum import StrEnum


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
    normalized = value.strip().lower().replace("-", "_")
    try:
        return AccessTier(normalized)
    except ValueError as exc:
        raise ValueError(f"unknown access tier: {value}") from exc


def tier_for_role(role: str) -> AccessTier:
    normalized = role.strip().lower().replace("-", "_")
    if normalized not in ROLE_TIERS:
        raise ValueError(f"unknown legal role: {role}")
    return ROLE_TIERS[normalized]


def can_access(user_tier: str | AccessTier, record_tier: str | AccessTier) -> bool:
    return _TIER_RANK[normalize_tier(user_tier)] >= _TIER_RANK[normalize_tier(record_tier)]


def filter_accessible_records(
    records: list[LegalRecord],
    role: str,
) -> list[LegalRecord]:
    user_tier = tier_for_role(role)
    return [record for record in records if can_access(user_tier, record.access_tier)]
