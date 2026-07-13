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


@dataclass(frozen=True)
class RuleFailure:
    """A structured, machine-readable reason a promo failed a rule.

    `rule_id` and `reason_code` are stable identifiers (PPCS-040); `message` is
    optional human-readable prose that the UI may show but must not parse.
    """

    rule_id: str
    reason_code: str
    message: str


def discount_pct(promo: Promo) -> float:
    """Percentage markdown from was→now.

    BUG (PPCS-001): rounds to a whole percent *before* the threshold check, so a
    4.6% discount becomes 5% and wrongly clears the genuine-discount bar.
    """
    return round((promo.was_price - promo.now_price) / promo.was_price * 100)


def is_was_now_compliant(promo: Promo) -> bool:
    """A was/now promo is compliant only if the markdown clears MIN_DISCOUNT_PCT."""
    return discount_pct(promo) >= MIN_DISCOUNT_PCT


def evaluate_failures(promo: Promo) -> list[RuleFailure]:
    """Return the structured rule failures for a promo.

    Empty list means the promo is compliant. Keeping this separate from the
    boolean verdict lets the API expose stable reason codes (PPCS-040) without
    changing the existing `was_now_compliant` field.
    """
    failures: list[RuleFailure] = []
    if not is_was_now_compliant(promo):
        failures.append(
            RuleFailure(
                rule_id="was_now",
                reason_code="discount_below_threshold",
                message=(
                    f"Markdown does not reach the minimum "
                    f"{MIN_DISCOUNT_PCT:g}% genuine-discount threshold."
                ),
            )
        )
    return failures
