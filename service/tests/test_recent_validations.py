"""PPCS-048 safe path: recent validations restored from the governed backend.

The naive implementation (localStorage payloads) is rejected in
docs/traps/PPCS-048-browser-payload-storage.md. These tests pin the safe path:
recent validations live server-side and the frontend persists nothing.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import recent_validations


@pytest.fixture(autouse=True)
def _clear():
    recent_validations.clear()
    yield
    recent_validations.clear()


client = TestClient(app)


def test_validate_response_shape_is_unchanged():
    # The pinned /validate shape must not gain a validation_id field.
    body = client.post(
        "/validate", json={"sku": "SKU-OK", "was_price": 10.0, "now_price": 9.0}
    ).json()
    assert body == {"sku": "SKU-OK", "discount_pct": 10, "was_now_compliant": True}


def test_recent_lists_validations_after_the_fact():
    client.post("/validate", json={"sku": "A", "was_price": 10.0, "now_price": 9.0})
    client.post("/validate", json={"sku": "B", "was_price": 20.0, "now_price": 18.0})

    recent = client.get("/validate/recent").json()
    assert [r["sku"] for r in recent] == ["B", "A"]  # most recent first
    assert all(r["validation_id"] for r in recent)


def test_recent_is_capped_at_20():
    for i in range(25):
        client.post(
            "/validate", json={"sku": f"S{i}", "was_price": 10.0, "now_price": 9.0}
        )
    recent = client.get("/validate/recent").json()
    assert len(recent) == 20


def test_recent_detail_by_id_round_trips():
    client.post("/validate", json={"sku": "A", "was_price": 10.0, "now_price": 9.0})
    vid = client.get("/validate/recent").json()[0]["validation_id"]

    detail = client.get(f"/validate/recent/{vid}").json()
    assert detail["sku"] == "A"
    assert detail["was_price"] == 10.0
    assert detail["now_price"] == 9.0


def test_recent_detail_unknown_id_is_404():
    assert client.get("/validate/recent/does-not-exist").status_code == 404


def test_frontend_restores_from_backend_not_localstorage():
    js = client.get("/static/app.js").text
    # Safe path: re-fetch from the server, never persist payloads client-side.
    assert 'fetch("/validate/recent")' in js
    assert "localStorage" not in js
    assert "sessionStorage" not in js
    assert "console.log" not in js
