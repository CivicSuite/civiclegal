from fastapi.testclient import TestClient

from civiclegal import __version__
from civiclegal.main import app

client = TestClient(app)


def test_root_reports_honest_current_state():
    payload = client.get("/").json()

    assert payload["name"] == "CivicLegal"
    assert payload["version"] == __version__
    assert "legal advice" in payload["message"]
    assert "not implemented yet" in payload["message"]


def test_health_reports_civiccore_pin():
    assert client.get("/health").json() == {
        "status": "ok",
        "service": "civiclegal",
        "version": "0.1.1",
        "civiccore_version": "0.3.0",
    }


def test_public_ui_contains_version_boundaries_and_dependency():
    text = client.get("/civiclegal").text

    assert "CivicLegal v0.1.1" in text
    assert "No legal advice" in text
    assert "civiccore==0.3.0" in text


def test_api_endpoints_return_deterministic_payloads():
    assert client.post("/api/v1/civiclegal/search", json={"query": "noise", "role": "staff"}).status_code == 200
    assert client.post("/api/v1/civiclegal/precedent", json={"question": "noise", "role": "staff"}).status_code == 200
    assert client.post("/api/v1/civiclegal/memo", json={"topic": "noise", "cited_sources": ["Code 8.12"]}).json()["not_legal_advice"] is True
    assert client.post("/api/v1/civiclegal/ordinance-comparison", json={"proposed_title": "Noise", "prior_citations": ["Ord. 1"]}).status_code == 200
    assert client.post("/api/v1/civiclegal/litigation-hold", json={"matter": "noise"}).status_code == 200
    assert client.post("/api/v1/civiclegal/citation-tracker", json={"topic": "noise", "citations": ["Case 1"]}).status_code == 200


def test_api_blocks_privileged_sample_records_from_staff():
    payload = client.post("/api/v1/civiclegal/search", json={"query": "strategy", "role": "staff"}).json()

    assert payload["hits"] == []
