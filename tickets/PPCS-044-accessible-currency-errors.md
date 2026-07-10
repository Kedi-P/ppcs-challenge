id: PPCS-044
title: Make workbench price errors accessible
type: feature
difficulty: 1

## Brief
Promo Ops users are misreading validation errors in the workbench. Improve the
price-entry experience so currency values, invalid inputs, and API failures are
clear without relying only on color.

## Acceptance
- Inputs have labels that remain associated with their controls.
- Validation errors are announced through an accessible error region.
- Currency values are formatted consistently for Australian dollars.
- The UI does not hide backend validation errors behind a generic failure.

## Notes for the dispatcher
This is a good UI review ticket. Strong answers improve the existing static
frontend and avoid introducing a component framework for a small form.
