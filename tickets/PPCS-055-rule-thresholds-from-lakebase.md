id: PPCS-055
title: Read rule thresholds from Lakebase instead of hardcoded constants
type: feature
difficulty: 2

## Brief
The compliance thresholds in PPCS — minimum discount percentage, minimum
promotion duration — are currently hardcoded constants in `app/rules.py`. Promo
Ops need to be able to adjust thresholds without a code change. Move the
threshold values into the team's Lakebase `ppcs_rule_config` table, which is
pre-seeded with the current values, and read them at service start-up (or on
each request if you prefer — document the trade-off).

## Acceptance
- `app/rules.py` reads `min_discount_pct` and `min_days` from `ppcs_rule_config`
  rather than from a hardcoded constant.
- The existing test behaviour is preserved: 4.6% still fails Was/Now, a 6-day
  promo still fails duration.
- Unit tests do not require live Lakebase credentials — the repository
  abstraction is injectable or the config can be overridden in tests.
- The implementation documents where the values come from and what happens if
  the config row is missing (fail safe or fall back to a default — justify the
  choice).

## Notes for the dispatcher
Start with a plan: where should the Lakebase read happen, and how should tests
mock it? Ask the agent to propose the read strategy before implementing. Watch
for tight coupling that makes the rules untestable without a live database.
