from datetime import date

from app.rules import (
    MIN_DURATION_DAYS,
    Promo,
    duration_days,
    is_duration_compliant,
    is_was_now_compliant,
)


def test_genuine_discount_passes():
    # 10% markdown — clearly compliant.
    assert is_was_now_compliant(Promo("A", was_price=10.00, now_price=9.00)) is True


def test_deep_discount_passes():
    assert is_was_now_compliant(Promo("C", was_price=20.00, now_price=15.00)) is True


def test_marginal_discount_below_threshold_fails():
    # 4.6% markdown must FAIL the 5% genuine-discount bar.
    # Currently rounds up to 5% and wrongly passes — this is PPCS-001.
    assert is_was_now_compliant(Promo("B", was_price=10.00, now_price=9.54)) is False


# --- PPCS-006: minimum promotion duration rule -----------------------------
# Duration is counted inclusively: a promo running start..end spans
# (end - start).days + 1 calendar days. The bar is MIN_DURATION_DAYS (7).


def test_duration_days_counts_inclusively():
    # 2026-07-13 .. 2026-07-19 is a 7-day promo (both endpoints count).
    assert duration_days(date(2026, 7, 13), date(2026, 7, 19)) == 7
    # Single-day promo spans 1 day, not 0.
    assert duration_days(date(2026, 7, 13), date(2026, 7, 13)) == 1


def test_seven_day_promo_is_duration_compliant():
    # Exactly at the MIN_DURATION_DAYS bar — compliant.
    assert (
        is_duration_compliant(date(2026, 7, 13), date(2026, 7, 19)) is True
    )


def test_six_day_promo_is_not_duration_compliant():
    # 2026-07-13 .. 2026-07-18 is 6 inclusive days — below the 7-day bar.
    assert (
        is_duration_compliant(date(2026, 7, 13), date(2026, 7, 18)) is False
    )


def test_min_duration_days_is_seven():
    assert MIN_DURATION_DAYS == 7
