import pytest
from fastapi import HTTPException

from app.main import PromoIn, validate


def test_validate_returns_existing_verdict_shape():
    response = validate(PromoIn(sku="SKU-OK", was_price=10.00, now_price=9.00))

    assert response == {
        "sku": "SKU-OK",
        "discount_pct": 10,
        "was_now_compliant": True,
    }


def test_validate_marginal_discount_is_noncompliant_after_ppcs_001():
    # PPCS-001: a 4.6% markdown must be reported non-compliant. The display
    # value still rounds to a whole 5% (contract: discount_pct is display-only),
    # but the compliance gate uses the exact, unrounded markdown.
    response = validate(PromoIn(sku="SKU-1", was_price=10.00, now_price=9.54))

    assert response == {
        "sku": "SKU-1",
        "discount_pct": 5,
        "was_now_compliant": False,
    }


# --- PPCS-006: minimum promotion duration rule -----------------------------


def test_validate_omits_duration_field_when_dates_absent():
    # The stable 3-key shape must be preserved when no dates are supplied.
    response = validate(PromoIn(sku="SKU-OK", was_price=10.00, now_price=9.00))

    assert "duration_compliant" not in response


def test_validate_seven_day_promo_is_duration_compliant():
    response = validate(
        PromoIn(
            sku="SKU-OK",
            was_price=10.00,
            now_price=9.00,
            start_date="2026-07-13",
            end_date="2026-07-19",
        )
    )

    assert response["duration_compliant"] is True
    # Was/Now rule stays independent and unaffected.
    assert response["was_now_compliant"] is True


def test_validate_six_day_promo_is_not_duration_compliant():
    # PPCS-006: 6-day promo -> duration_compliant present and False.
    response = validate(
        PromoIn(
            sku="SKU-SHORT",
            was_price=10.00,
            now_price=9.00,
            start_date="2026-07-13",
            end_date="2026-07-18",
        )
    )

    assert response["duration_compliant"] is False
    # Discount is a genuine 10% — only the duration rule fails.
    assert response["was_now_compliant"] is True


def test_validate_combined_was_now_and_duration_failure():
    # Both rules fail independently: shallow discount AND too-short window.
    response = validate(
        PromoIn(
            sku="SKU-BAD",
            was_price=10.00,
            now_price=9.80,  # 2% markdown — below the 5% bar
            start_date="2026-07-13",
            end_date="2026-07-18",  # 6 inclusive days — below the 7-day bar
        )
    )

    assert response["was_now_compliant"] is False
    assert response["duration_compliant"] is False


def test_validate_reversed_dates_rejected_with_400():
    with pytest.raises(HTTPException) as exc_info:
        validate(
            PromoIn(
                sku="SKU-REV",
                was_price=10.00,
                now_price=9.00,
                start_date="2026-07-19",
                end_date="2026-07-13",
            )
        )

    assert exc_info.value.status_code == 400
