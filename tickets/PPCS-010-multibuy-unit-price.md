id: PPCS-010
title: Add multi-buy effective unit price calculation
type: feature
difficulty: 2

## Brief
Promo Ops need PPCS to calculate the effective unit price for multi-buy offers
like "3 for $10". Add a helper that returns the unit price and include it in the
validation response when a multi-buy offer is supplied.

## Acceptance
- Multi-buy input supports quantity and bundle price.
- `3 for 10.00` returns an effective unit price of `3.33` using normal currency
  rounding.
- Invalid quantity or bundle price is rejected.
- Existing Was/Now checks keep working for non-multi-buy promos.
- Tests cover normal and invalid multi-buy inputs.

## Notes for the dispatcher
Keep this to calculation + response shape. Do not add margin rules unless a
separate ticket asks for them.
