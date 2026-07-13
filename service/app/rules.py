"""Promotional pricing compliance rules.

Deliberately small and a little flawed — this is the surface the challenge
backlog acts on. PPCS-001 lives in `discount_pct` below.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal

#: A markdown must be at least this deep to count as a genuine discount.
MIN_DISCOUNT_PCT = 5.0


@dataclass
class Promo:
    sku: str
    was_price: float
    now_price: float


def discount_pct(promo: Promo) -> float:
    """Percentage markdown from was→now.

    BUG (PPCS-001): rounds to a whole percent *before* the threshold check, so a
    4.6% discount becomes 5% and wrongly clears the genuine-discount bar.
    """
    return round((promo.was_price - promo.now_price) / promo.was_price * 100)


def is_was_now_compliant(promo: Promo) -> bool:
    """A was/now promo is compliant only if the markdown clears MIN_DISCOUNT_PCT."""
    return discount_pct(promo) >= MIN_DISCOUNT_PCT


def multibuy_unit_price(quantity: int, bundle_price: float) -> float:
    """Effective per-unit price for a multi-buy offer like "3 for $10".

    Returns the bundle price divided by the quantity, rounded to two decimal
    places using normal currency rounding (half-up). ``3 for 10.00`` -> 3.33.

    Raises ``ValueError`` for a non-positive quantity or a non-positive bundle
    price -- those are not valid multi-buy inputs.
    """
    if quantity <= 0:
        raise ValueError("multibuy quantity must be a positive integer")
    if bundle_price <= 0:
        raise ValueError("multibuy bundle price must be greater than 0")
    unit = Decimal(str(bundle_price)) / Decimal(quantity)
    return float(unit.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
