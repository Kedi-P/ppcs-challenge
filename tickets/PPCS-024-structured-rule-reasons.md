id: PPCS-024
title: Return structured rule failure reasons
type: feature
difficulty: 1

## Brief
The current response tells us whether Was/Now passed, but support needs a reason
they can show in a ticket. Add structured failure reasons to the validation
response.

## Acceptance
- Failed rules return stable reason codes.
- Reasons are machine-readable, not only prose.
- Passing rules do not emit failure reasons.
- Tests cover at least one passing promo and one failing promo.

## Notes for the dispatcher
Good small ticket. Keep reason codes stable and boring.
