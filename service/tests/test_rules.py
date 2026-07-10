from app.rules import Promo, is_was_now_compliant


def test_genuine_discount_passes():
    # 10% markdown — clearly compliant.
    assert is_was_now_compliant(Promo("A", was_price=10.00, now_price=9.00)) is True


def test_deep_discount_passes():
    assert is_was_now_compliant(Promo("C", was_price=20.00, now_price=15.00)) is True


def test_marginal_discount_below_threshold_fails():
    # 4.6% markdown must FAIL the 5% genuine-discount bar.
    # Currently rounds up to 5% and wrongly passes — this is PPCS-001.
    assert is_was_now_compliant(Promo("B", was_price=10.00, now_price=9.54)) is False
