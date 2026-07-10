id: PPCS-009
title: Flag member-only prices advertised as general prices
type: feature
difficulty: 2

## Brief
Member-only promotions must not be presented as general public prices. Add a
rule that flags a promo when `member_only=true` but the promo channel or display
copy marks it as a general public offer.

## Acceptance
- Promo input supports enough fields to distinguish member-only and public
  display treatment.
- Member-only offer advertised as public is non-compliant.
- Member-only offer clearly labelled as member-only is compliant for this rule.
- Public offer is not affected by this rule.
- Tests cover all three cases.

## Notes for the dispatcher
Good ticket for asking the agent to propose a small data shape first, then
implement after review.
