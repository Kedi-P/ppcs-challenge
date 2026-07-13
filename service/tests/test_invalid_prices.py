"""PPCS-004 â invalid promo prices are rejected with a clear 400."""
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_was_price_zero_is_rejected():
    response = client.post(
        "/validate", json={"sku": "SKU-1", "was_price": 0.0, "now_price": 0.0}
    )

    assert response.status_code == 400
    assert response.json()["detail"]["reason_code"] == "was_price_not_positive"


def test_was_price_negative_is_rejected():
    response = client.post(
        "/validate", json={"sku": "SKU-1", "was_price": -5.0, "now_price": 1.0}
    )

    assert response.status_code == 400
    assert response.json()["detail"]["reason_code"] == "was_price_not_positive"


def test_now_price_negative_is_rejected():
    response = client.post(
        "/validate", json={"sku": "SKU-1", "was_price": 10.0, "now_price": -1.0}
    )

    assert response.status_code == 400
    assert response.json()["detail"]["reason_code"] == "now_price_negative"


def test_now_price_above_was_price_is_rejected():
    response = client.post(
        "/validate", json={"sku": "SKU-1", "was_price": 10.0, "now_price": 12.0}
    )

    assert response.status_code == 400
    assert response.json()["detail"]["reason_code"] == "now_price_above_was_price"


def test_valid_promo_still_returns_existing_verdict_shape():
    response = client.post(
        "/validate", json={"sku": "SKU-OK", "was_price": 10.0, "now_price": 9.0}
    )

    assert response.status_code == 200
    assert response.json() == {
        "sku": "SKU-OK",
        "discount_pct": 10,
        "was_now_compliant": True,
    }
