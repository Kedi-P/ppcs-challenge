id: PPCS-038
title: Improve the workbench result card
type: feature
difficulty: 1

## Brief
Support teams want the PPCS workbench to make validation outcomes obvious at a
glance. Improve the result card so a user can see the SKU, discount percentage,
Was/Now verdict, and whether the promo is safe to advertise without opening the
API response.

## Acceptance
- The workbench calls `POST /validate` and renders the returned verdict.
- The pass/fail state is visually clear and accessible to screen readers.
- Client-side validation catches missing SKU, non-numeric prices, zero/negative
  prices, and `now_price > was_price` before calling the API.
- Tests or static checks prove the UI entry point and script are still served.

## Notes for the dispatcher
This is the first full-stack ticket. Keep it small: do not introduce a build
toolchain, framework, or separate frontend service.
