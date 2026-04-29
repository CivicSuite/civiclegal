from civiclegal import __version__
from civiclegal.corpus_access import AccessTier, LegalRecord, can_access, filter_accessible_records
from civiclegal.litigation_hold import flag_litigation_hold_candidates
from civiclegal.memo import draft_legal_memo
from civiclegal.ordinance import compare_ordinance_draft
from civiclegal.precedent import lookup_precedent
from civiclegal.search import search_legal_corpus
from civiclegal.statutes import track_authority_citations


def test_version_is_release_version():
    assert __version__ == "0.1.2"


def test_privilege_tiers_are_strictly_ordered():
    assert can_access("privileged", "privileged") is True
    assert can_access("staff", "privileged") is False
    assert can_access("public", "staff") is False


def test_access_filter_blocks_privileged_records_for_staff():
    records = [
        LegalRecord("public", "Published ordinance", "code", "Noise", "Code 8.12", AccessTier.PUBLIC),
        LegalRecord("privileged", "Attorney memo", "memo", "Strategy", "Memo A", AccessTier.PRIVILEGED),
    ]

    visible = filter_accessible_records(records, "staff")

    assert [record.record_id for record in visible] == ["public"]


def test_search_returns_citations_only_for_accessible_records():
    records = [
        LegalRecord("staff", "Prior action", "minutes", "Noise discussion", "Minutes 1", AccessTier.STAFF),
        LegalRecord("priv", "Privileged action", "memo", "Noise strategy", "Memo 1", AccessTier.PRIVILEGED),
    ]

    hits = search_legal_corpus("noise", records, "staff")

    assert [hit.citation for hit in hits] == ["Minutes 1"]


def test_precedent_lookup_requires_attorney_review():
    result = lookup_precedent("noise", [], "staff")

    assert result.attorney_review_required is True
    assert "does not make legal conclusions" in result.boundary


def test_memo_draft_is_not_legal_advice():
    draft = draft_legal_memo("noise enforcement", ["Code 8.12"])

    assert draft.attorney_review_required is True
    assert draft.not_legal_advice is True


def test_ordinance_comparison_requires_attorney_review():
    comparison = compare_ordinance_draft("Noise update", ["Ord. 2024-01"])

    assert comparison.attorney_review_required is True
    assert "Attorney review" in " ".join(comparison.review_notes)


def test_litigation_hold_flags_candidate_records():
    records = [LegalRecord("r1", "Downtown claim", "memo", "Claim filed", "Memo 1", AccessTier.STAFF)]

    flag = flag_litigation_hold_candidates("claim", records)

    assert flag.flagged_record_ids == ("r1",)
    assert flag.hold_review_required is True


def test_statute_tracker_is_attorney_maintained_not_westlaw():
    tracker = track_authority_citations("noise", ["Colo. Rev. Stat. 1"])

    assert tracker.attorney_maintained is True
    assert "Westlaw" in tracker.boundary
