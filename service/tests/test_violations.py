"""Tests for the /violations endpoint and its repository (PPCS-014).

All run without live Lakebase credentials — the endpoint reads from an
in-memory repository populated by /validate.
"""
from datetime import datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.main import PromoIn, app, validate
from app.violations import InMemoryViolationRepository, Violation


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_violations():
    """Give every test a clean, isolated in-memory violation store."""
    main._violations = InMemoryViolationRepository()
    yield
    main._violations = InMemoryViolationRepository()


# --- repository unit tests -------------------------------------------------


def test_repository_returns_newest_first():
    repo = InMemoryViolationRepository()
    base = datetime(2026, 7, 13, tzinfo=timezone.utc)
    older = Violation("OLD", ["was_now"], "r", base)
    newer = Violation("NEW", ["was_now"], "r", base + timedelta(hours=1))
    repo.record(older)
    repo.record(newer)

    assert [v.sku for v in repo.recent(10)] == ["NEW", "OLD"]


def test_repository_recent_respects_limit():
    repo = InMemoryViolationRepository()
    base = datetime(2026, 7, 13, tzinfo=timezone.utc)
    for i in range(5):
        repo.record(Violation(f"SKU-{i}", ["was_now"], "r", base + timedelta(minutes=i)))

    recent = repo.recent(2)
    assert [v.sku for v in recent] == ["SKU-4", "SKU-3"]


# --- filtering: only non-compliant validations are recorded ----------------


def test_compliant_validation_is_not_recorded():
    # 10% markdown clears the threshold → compliant → excluded from /violations.
    validate(PromoIn(sku="SKU-OK", was_price=10.00, now_price=9.00))

    assert client.get("/violations").json() == []


def test_non_compliant_validation_is_recorded():
    # 2% markdown is below the genuine-discount bar → non-compliant.
    validate(PromoIn(sku="SKU-BAD", was_price=10.00, now_price=9.80))

    body = client.get("/violations").json()
    assert len(body) == 1
    assert body[0]["sku"] == "SKU-BAD"


# --- endpoint contract -----------------------------------------------------


def test_violation_record_includes_required_fields():
    validate(PromoIn(sku="SKU-BAD", was_price=10.00, now_price=9.80))

    record = client.get("/violations").json()[0]
    assert set(record) == {"sku", "rule_ids", "reason", "timestamp"}
    assert record["sku"] == "SKU-BAD"
    assert record["rule_ids"] == ["was_now"]
    assert isinstance(record["reason"], str) and record["reason"]
    # timestamp parses as ISO-8601.
    datetime.fromisoformat(record["timestamp"])


def test_violations_do_not_leak_prices():
    validate(PromoIn(sku="SKU-BAD", was_price=10.00, now_price=9.80))

    raw = client.get("/violations").text
    assert "9.8" not in raw and "10.0" not in raw


def test_violations_ordered_newest_first():
    validate(PromoIn(sku="SKU-FIRST", was_price=10.00, now_price=9.80))
    validate(PromoIn(sku="SKU-SECOND", was_price=10.00, now_price=9.90))

    skus = [v["sku"] for v in client.get("/violations").json()]
    assert skus == ["SKU-SECOND", "SKU-FIRST"]


def test_empty_state_returns_empty_list():
    response = client.get("/violations")

    assert response.status_code == 200
    assert response.json() == []
