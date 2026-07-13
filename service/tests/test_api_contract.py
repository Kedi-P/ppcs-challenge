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
