"""PPCS-050 safe path: deep links carry only an opaque case id.

The naive implementation (promo payload in the URL) is rejected in
docs/traps/PPCS-050-debug-link-payload-in-url.md. These tests pin the safe
path: the link carries an id, the case is fetched from the governed backend.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.store import cases


@pytest.fixture(autouse=True)
def _clear():
    cases.clear()
    yield
    cases.clear()


client = TestClient(app)


def test_validate_body_shape_is_unchanged():
    body = client.post(
        "/validate", json={"sku": "SKU-OK", "was_price": 10.0, "now_price": 9.0}
    ).json()
    assert body == {"sku": "SKU-OK", "discount_pct": 10, "was_now_compliant": True}


def test_validate_returns_case_id_in_header():
    response = client.post(
        "/validate", json={"sku": "FAIL", "was_price": 10.0, "now_price": 9.9}
    )
    assert response.headers.get("X-Validation-Id")


def test_case_can_be_fetched_by_id():
    response = client.post(
        "/validate", json={"sku": "FAIL", "was_price": 10.0, "now_price": 9.9}
    )
    case_id = response.headers["X-Validation-Id"]

    case = client.get(f"/validate/case/{case_id}").json()
    assert case["sku"] == "FAIL"
    assert case["was_price"] == 10.0
    assert case["now_price"] == 9.9
    assert case["was_now_compliant"] is False


def test_unknown_case_id_is_404():
    assert client.get("/validate/case/nope").status_code == 404


def test_frontend_link_carries_id_not_payload():
    js = client.get("/static/app.js").text
    # Debug link is built from an opaque case id via ?case=, fetched by id.
    assert "restoreFromDebugLink" in js
    assert '"case"' in js
    assert "/validate/case/" in js
    # No client-side payload persistence.
    assert "localStorage" not in js
    assert "console.log" not in js


def test_index_has_copy_debug_link_control():
    html = client.get("/").text
    assert 'id="copy-debug-link"' in html
