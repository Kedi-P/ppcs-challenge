id: PPCS-001
title: Fix false-pass on marginal "was/now" discounts
type: bug
difficulty: 1

## Brief
A promo with a 4.6% markdown (was **$10.00** → now **$9.54**) is being reported as
WAS/NOW **compliant**, but our minimum genuine-discount threshold is **5%**.
Marginal markdowns are slipping through and getting advertised. Make the
compliance check reject discounts below the 5% threshold — without rounding
them up to clear the bar.

## Acceptance
- A 4.6% discount is reported **non-compliant**.
- A genuine ≥5% discount is still **compliant**.
- `uv run pytest -q` is green (the failing test `test_marginal_discount_below_threshold_fails` passes).

## Notes for the dispatcher
Good first brief for a team's opening dispatch — small, well-bounded, one diff,
one obviously-correct review call. The bug is in `app/rules.py:discount_pct`.
