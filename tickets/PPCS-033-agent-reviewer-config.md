id: PPCS-033
title: Create a reusable reviewer config for PPCS PRs
type: docs
difficulty: 1

## Brief
Teams keep asking reviewer agents to check the same things manually. Create a
small reusable reviewer config or `SKILL.md` that tells a reviewer sub-agent how
to assess PPCS PRs for correctness, scope control, tests, data access, telemetry,
and PR-only delivery.

## Acceptance
- The reviewer config names the PPCS operating envelope.
- It includes checks for secrets, egress, UC data access, telemetry payloads, and
  merge/deploy attempts.
- It tells the reviewer to inspect tests and trace evidence, not only the agent
  summary.
- A later PR review can reuse it.

## Notes for the dispatcher
Round 3 harness-improvement ticket. The output is valuable only if it is short
enough to reuse.
