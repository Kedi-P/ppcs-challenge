"""PPCS-024: structured rule failure reasons on the /validate response."""
from app.main import PromoIn, validate
from app.rules import (
    REASON_DISCOUNT_BELOW_THRESHOLD,
    RULE_WAS_NOW,
    Promo,
    rule_failures,
)


def test_passing_promo_emits_no_failure_reasons():
    # 10% markdown clears the bar; no failures should be present.
    assert rule_failures(Promo("A", was_price=10.00, now_price=9.00)) == []


def test_failing_promo_emits_structured_reason():
    # 2% markdown is below the 5% genuine-discount bar.
    failures = rule_failures(Promo("B", was_price=10.00, now_price=9.80))
    assert [f.as_dict() for f in failures] == [
        {"rule_id": RULE_WAS_NOW, "reason_code": REASON_DISCOUNT_BELOW_THRESHOLD}
    ]


def test_validate_omits_failures_for_passing_promo():
    response = validate(PromoIn(sku="SKU-OK", was_price=10.00, now_price=9.00))
    assert "failures" not in response
    assert response["was_now_compliant"] is True


def test_validate_returns_structured_failures_for_failing_promo():
    response = validate(PromoIn(sku="SKU-FAIL", was_price=10.00, now_price=9.80))
    assert response["was_now_compliant"] is False
    assert response["failures"] == [
        {"rule_id": RULE_WAS_NOW, "reason_code": REASON_DISCOUNT_BELOW_THRESHOLD}
    ]
