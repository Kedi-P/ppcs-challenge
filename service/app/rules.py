"""Promotional pricing compliance rules.

Deliberately small and a little flawed — this is the surface the challenge
backlog acts on. PPCS-001 lives in `discount_pct` below.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

#: A markdown must be at least this deep to count as a genuine discount.
MIN_DISCOUNT_PCT = 5.0

#: A promotion must run for at least this many calendar days (inclusive) to be
#: a genuine, sustained offer rather than a fleeting one (PPCS-006).
MIN_DURATION_DAYS = 7


@dataclass
class Promo:
    sku: str
    was_price: float
    now_price: float


def _markdown_pct(promo: Promo) -> float:
    """Exact percentage markdown from was→now, unrounded.

    This is the value compliance decisions gate on — see `is_was_now_compliant`.
    """
    return (promo.was_price - promo.now_price) / promo.was_price * 100


def discount_pct(promo: Promo) -> int:
    """Whole-percent markdown for display only.

    Per the API contract, this is the rounded display value. It must NOT be used
    as the threshold gate — rounding a 4.6% markdown up to 5% would wrongly clear
    the genuine-discount bar (PPCS-001). Gate on `_markdown_pct` instead.
    """
    return round(_markdown_pct(promo))


def is_was_now_compliant(promo: Promo) -> bool:
    """A was/now promo is compliant only if the markdown clears MIN_DISCOUNT_PCT.

    Uses the exact, unrounded markdown so a marginal discount below the threshold
    is not rounded up past the bar.
    """
    return _markdown_pct(promo) >= MIN_DISCOUNT_PCT


def duration_days(start: date, end: date) -> int:
    """Calendar length of a promo window, counted **inclusively**.

    Both endpoints count, so a promo running 2026-07-13..2026-07-19 spans 7
    days, and a single-day promo (start == end) spans 1. This matches the
    "at least 7 calendar days (inclusive)" wording in the API contract.
    """
    return (end - start).days + 1


def is_duration_compliant(start: date, end: date) -> bool:
    """A promo is duration-compliant when its inclusive window is long enough.

    Independent of the was/now rule: a promo can clear one bar and fail the
    other. Callers are responsible for rejecting reversed windows (end < start)
    before asking for a verdict.
    """
    return duration_days(start, end) >= MIN_DURATION_DAYS
