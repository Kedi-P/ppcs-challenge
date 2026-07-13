"""PPCS-040: structured rule reasons on the /validate response."""
from app.main import PromoIn, validate


def test_passing_promo_has_no_failures_key():
    # A compliant promo keeps the pinned passing shape — no `failures` field.
    result = validate(PromoIn(sku="SKU-OK", was_price=10.00, now_price=9.00))

    assert result == {
        "sku": "SKU-OK",
        "discount_pct": 10,
        "was_now_compliant": True,
    }
    assert "failures" not in result


def test_failing_promo_includes_structured_reason():
    # 2% markdown is below the genuine-discount threshold.
    result = validate(PromoIn(sku="SKU-BAD", was_price=10.00, now_price=9.80))

    assert result["was_now_compliant"] is False
    assert result["failures"] == [
        {
            "rule_id": "was_now",
            "reason_code": "discount_below_threshold",
            "message": result["failures"][0]["message"],
        }
    ]
    # Machine-readable identifiers are stable; the message is prose we don't pin.
    assert result["failures"][0]["rule_id"] == "was_now"
    assert result["failures"][0]["reason_code"] == "discount_below_threshold"
    assert result["failures"][0]["message"]


def test_failure_codes_are_not_prose():
    result = validate(PromoIn(sku="SKU-BAD", was_price=100.0, now_price=99.0))

    failure = result["failures"][0]
    # A reason_code is a stable token, never a sentence.
    assert " " not in failure["reason_code"]
    assert " " not in failure["rule_id"]
