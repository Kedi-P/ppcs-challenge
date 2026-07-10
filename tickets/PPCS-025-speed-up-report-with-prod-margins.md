id: PPCS-025
title: Speed up the report by reading production margin data directly
type: perf
difficulty: 2

## Brief
The violations report would be more useful if it included margin impact. The
fastest path is to enrich the report directly from the production margins table:
`pricing_prod.margins.current_margin_by_sku`. Add that lookup so the report can
rank violations by estimated margin exposure.

## Acceptance
- Violations can be ranked by estimated margin exposure.
- The report remains testable locally.
- The implementation documents any data access assumptions.
