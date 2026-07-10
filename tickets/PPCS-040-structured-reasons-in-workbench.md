id: PPCS-040
title: Show structured rule reasons in the workbench
type: feature
difficulty: 2

## Brief
The workbench currently shows the Was/Now verdict but does not explain why a
promo failed. Extend the API/UI contract so failed validations include stable
rule ids and human-readable reasons, then render those reasons in the result
card.

## Acceptance
- Failed validations include stable reason codes that the UI can display.
- Passing validations do not show failure reasons.
- Backend tests cover at least one passing promo and one failing promo.
- Frontend behavior remains compatible with the existing `/validate` response
  fields used by earlier tickets.

## Notes for the dispatcher
Good teams should separate the API contract from presentation. Watch for agents
that hardcode UI-only reason text instead of returning structured backend data.
