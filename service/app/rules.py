"""Promotional pricing compliance rules.

Deliberately small and a little flawed — this is the surface the challenge
backlog acts on. PPCS-001 lives in `discount_pct` below.
"""
from __future__ import annotations

from dataclasses import dataclass

#: A markdown must be at least this deep to count as a genuine discount.
MIN_DISCOUNT_PCT = 5.0

#: Stable, machine-readable identifier for the Was/Now markdown rule.
RULE_WAS_NOW = "was_now"
#: Stable, machine-readable reason code emitted when the markdown is too shallow.
REASON_DISCOUNT_BELOW_THRESHOLD = "discount_below_threshold"


@dataclass(frozen=True)
class RuleFailure:
    """A structured, machine-readable reason a rule failed.

    ``rule_id`` and ``reason_code`` are stable identifiers (never prose) so
    support tooling can key off them. Human-readable text, if any, lives
    elsewhere.
    """

    rule_id: str
    reason_code: str

    def as_dict(self) -> dict[str, str]:
        return {"rule_id": self.rule_id, "reason_code": self.reason_code}


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


def rule_failures(promo: Promo) -> list[RuleFailure]:
    """Structured failure reasons for every rule this promo fails.

    Returns an empty list for a fully compliant promo. Passing rules never
    emit a failure â a reason is present only when the corresponding rule
    actually fails.
    """
    failures: list[RuleFailure] = []
    if not is_was_now_compliant(promo):
        failures.append(
            RuleFailure(RULE_WAS_NOW, REASON_DISCOUNT_BELOW_THRESHOLD)
        )
    return failures
