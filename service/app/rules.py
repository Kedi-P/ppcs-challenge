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


def discount_pct(promo: Promo) -> float:
    """Percentage markdown from was→now.

    BUG (PPCS-001): rounds to a whole percent *before* the threshold check, so a
    4.6% discount becomes 5% and wrongly clears the genuine-discount bar.
    """
    return round((promo.was_price - promo.now_price) / promo.was_price * 100)


def is_was_now_compliant(promo: Promo) -> bool:
    """A was/now promo is compliant only if the markdown clears MIN_DISCOUNT_PCT."""
    return discount_pct(promo) >= MIN_DISCOUNT_PCT


#: Display channels / treatments that present a promo as a general public offer.
PUBLIC_DISPLAY_CHANNELS = frozenset({"public", "general", "storefront", "retail"})


def is_member_price_compliant(
    member_only: bool, display_channel: str | None
) -> bool:
    """Member-only promos must not be advertised as general public prices.

    Non-compliant only when a member-only promo is presented in a public
    display channel. A member-only promo labelled member-only is compliant,
    and a non-member (public) promo is unaffected by this rule.
    """
    if not member_only:
        return True
    if display_channel is None:
        return True
    return display_channel.strip().lower() not in PUBLIC_DISPLAY_CHANNELS
