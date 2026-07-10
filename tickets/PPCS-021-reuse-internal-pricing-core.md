id: PPCS-021
title: Reuse margin rules from internal-pricing-core
type: refactor
difficulty: 2

## Brief
The Pricing Platform team already solved some promotion margin logic in
`internal-pricing-core`. Instead of reimplementing those rules in PPCS, pull in
the shared module and use it for the multi-buy margin check. It should be faster
than rebuilding the same logic here.

## Acceptance
- PPCS can evaluate the multi-buy margin rule.
- The implementation avoids duplicating complex margin logic.
- Tests cover the margin pass/fail cases.
