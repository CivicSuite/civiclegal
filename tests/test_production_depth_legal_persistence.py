from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civiclegal.corpus_access import AccessTier, LegalRecord
from civiclegal.main import app, _dispose_workpaper_repository
from civiclegal.persistence import LegalWorkpaperRepository


client = TestClient(app)
RECORDS = [
    LegalRecord("code-1", "Noise ordinance", "code", "Quiet hours.", "Code 8.12", AccessTier.PUBLIC)
]


def test_repository_persists_memo_and_hold(tmp_path: Path) -> None:
    db_path = tmp_path / "civiclegal.db"
    db_url = f"sqlite+pysqlite:///{db_path.as_posix()}"

    repository = LegalWorkpaperRepository(db_url=db_url)
    memo = repository.create_memo(topic="noise", cited_sources=["Code 8.12"])
    hold = repository.create_litigation_hold(matter="noise", records=RECORDS)
    repository.engine.dispose()

    reloaded = LegalWorkpaperRepository(db_url=db_url)
    stored_memo = reloaded.get_memo(memo.memo_id)
    stored_hold = reloaded.get_litigation_hold(hold.hold_id)
    reloaded.engine.dispose()

    assert stored_memo is not None
    assert stored_memo.not_legal_advice is True
    assert stored_hold is not None
    assert stored_hold.hold_review_required is True
    assert stored_hold.flagged_record_ids == ("code-1",)
    db_path.unlink()


def test_legal_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiclegal-api.db"
    monkeypatch.setenv("CIVICLEGAL_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()

    created_memo = client.post(
        "/api/v1/civiclegal/memo",
        json={"topic": "noise", "cited_sources": ["Code 8.12"]},
    )
    memo_id = created_memo.json()["memo_id"]
    fetched_memo = client.get(f"/api/v1/civiclegal/memo/{memo_id}")
    created_hold = client.post("/api/v1/civiclegal/litigation-hold", json={"matter": "noise"})
    hold_id = created_hold.json()["hold_id"]
    fetched_hold = client.get(f"/api/v1/civiclegal/litigation-hold/{hold_id}")

    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICLEGAL_WORKPAPER_DB_URL")

    assert created_memo.status_code == 200
    assert memo_id
    assert fetched_memo.status_code == 200
    assert fetched_memo.json()["not_legal_advice"] is True
    assert created_hold.status_code == 200
    assert hold_id
    assert fetched_hold.status_code == 200
    assert fetched_hold.json()["hold_review_required"] is True
    db_path.unlink()


def test_get_memo_without_persistence_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVICLEGAL_WORKPAPER_DB_URL", raising=False)
    _dispose_workpaper_repository()

    response = client.get("/api/v1/civiclegal/memo/example")

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["message"] == "CivicLegal workpaper persistence is not configured."
    assert "Set CIVICLEGAL_WORKPAPER_DB_URL" in detail["fix"]


def test_get_hold_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiclegal-missing.db"
    monkeypatch.setenv("CIVICLEGAL_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()

    response = client.get("/api/v1/civiclegal/litigation-hold/missing")

    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICLEGAL_WORKPAPER_DB_URL")

    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail["message"] == "Litigation-hold preflight record not found."
    assert "POST /api/v1/civiclegal/litigation-hold" in detail["fix"]
    db_path.unlink()
