"""PPCS-010: multi-buy effective unit price calculation."""
import pytest
from fastapi import HTTPException

from app.main import PromoIn, validate
from app.rules import multibuy_unit_price


def test_three_for_ten_rounds_to_unit_price():
    assert multibuy_unit_price(3, 10.00) == 3.33


def test_two_for_five_is_exact():
    assert multibuy_unit_price(2, 5.00) == 2.50


def test_invalid_quantity_rejected():
    with pytest.raises(ValueError):
        multibuy_unit_price(0, 10.00)


def test_invalid_bundle_price_rejected():
    with pytest.raises(ValueError):
        multibuy_unit_price(3, 0.0)


def test_validate_includes_effective_unit_price():
    response = validate(
        PromoIn(sku="SKU-MB", was_price=10.00, now_price=9.00, multibuy_qty=3, bundle_price=10.00)
    )
    assert response["effective_unit_price"] == 3.33
    # Was/Now checks keep working alongside multi-buy.
    assert response["was_now_compliant"] is True


def test_validate_without_multibuy_omits_unit_price():
    response = validate(PromoIn(sku="SKU-OK", was_price=10.00, now_price=9.00))
    assert "effective_unit_price" not in response


def test_validate_rejects_invalid_multibuy_qty():
    with pytest.raises(HTTPException) as exc:
        validate(
            PromoIn(sku="SKU-BAD", was_price=10.00, now_price=9.00, multibuy_qty=0, bundle_price=10.00)
        )
    assert exc.value.status_code == 400


def test_validate_rejects_partial_multibuy_input():
    with pytest.raises(HTTPException) as exc:
        validate(
            PromoIn(sku="SKU-BAD", was_price=10.00, now_price=9.00, multibuy_qty=3)
        )
    assert exc.value.status_code == 400
