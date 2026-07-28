from fastapi.testclient import TestClient

from app.main import RiskRequest, calculate_score, app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "UP"}


def test_low_risk_request_is_approved() -> None:
    response = client.post("/api/risk", json={"customer_id": "C-1", "amount": 100})
    assert response.status_code == 200
    assert response.json()["level"] == "LOW"
    assert response.json()["approved"] is True


def test_high_risk_request_is_rejected() -> None:
    response = client.post(
        "/api/risk",
        json={"customer_id": "C-2", "amount": 2000, "international": True, "prior_chargebacks": 2},
    )
    assert response.status_code == 200
    assert response.json()["level"] == "HIGH"
    assert response.json()["approved"] is False


def test_score_is_capped_at_100() -> None:
    request = RiskRequest(customer_id="C-3", amount=5000, international=True, prior_chargebacks=20)
    assert calculate_score(request) == 95
