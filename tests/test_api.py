from fastapi.testclient import TestClient

from app import app

client = TestClient(app)


def test_popular_package_is_safe():
    r = client.get("/check", params={"name": "requests"})
    assert r.status_code == 200
    assert r.json()["verdict"] == "SAFE"


def test_answer_has_expected_fields():
    r = client.get("/check", params={"name": "reqeusts"})
    assert r.status_code == 200
    data = r.json()
    assert data["verdict"] in ("SAFE", "RISKY")
    assert 0 <= data["risk_score"] <= 1
    assert isinstance(data["reasons"], list)