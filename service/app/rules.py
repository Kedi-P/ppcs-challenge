"""Promotional pricing compliance rules.

Deliberately small and a little flawed — this is the surface the challenge
backlog acts on. PPCS-001 lives in `discount_pct` below.
"""
from __future__ import annotations

from dataclasses import dataclass

#: A markdown must be at least this deep to count as a genuine discount.
MIN_DISCOUNT_PCT = 5.0


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
