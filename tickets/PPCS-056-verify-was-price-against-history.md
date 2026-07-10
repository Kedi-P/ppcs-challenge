id: PPCS-056
title: Verify caller-supplied was_price against recorded price history
type: feature
difficulty: 3

## Brief
The `/validate` endpoint currently trusts the caller's `was_price` field
completely. A retailer could claim any was-price and the rule would pass as long
as the arithmetic works out. Add a verification step: look up the SKU in the
team's Lakebase `ppcs_price_history` table and check whether the supplied
`was_price` matches a recorded price within an acceptable tolerance. Return a
`was_price_verified` field in the response indicating whether the history
lookup confirmed the claim.

If no price history exists for the SKU, set `was_price_verified` to `false`
but do **not** fail the compliance check on that basis alone — an unverifiable
claim is not the same as a false one. Document the decision.

## Acceptance
- `/validate` response includes a `was_price_verified` boolean.
- A SKU with a matching price history entry returns `was_price_verified: true`.
- A SKU with a recorded price that does not match the supplied was_price
  returns `was_price_verified: false`.
- A SKU with no price history returns `was_price_verified: false`.
- Compliance verdict (`was_now_compliant`) is not changed by this field alone.
- Unit tests do not require live Lakebase credentials.
- The implementation explains the tolerance used for price matching and why.

## Notes for the dispatcher
This is a trust-boundary ticket. Before implementing, ask the agent: what does
it mean that the caller supplies the was_price? Who could lie, and what is the
governance consequence? The design decision — strict reject, flag-only, or
silent pass — should be in the PR description, not just in code comments. The
`ppcs_price_history` table is pre-seeded with SKU-1, SKU-2, and SKU-3.
