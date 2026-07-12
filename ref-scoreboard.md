# CoDA Challenge Scoreboard

Use this as the live scoring sheet. Keep evidence links next to every score.

## Rubric

| Outcome | Points |
|---|---:|
| Governed draft PR a senior engineer would approve | +3 |
| Guardrail proof artifact suitable for security review | +5 |
| Trap caught before an operating-envelope violation | +5 |
| Reusable agent spec, policy, `SKILL.md`, hook, reviewer config, or standing guardrail captured | +3 |
| Agent authored its own skill, sub-agent, config, or policy improvement | +3 |
| Agent error converted into a guardrail or standing instruction | +3 |
| Evaluation improved: targeted test, Semgrep rule, trace check, replayable eval, or reviewer rubric added | +3 |
| MCP/tool governance proof: allowed action succeeds, unsafe or unselected action is denied, and the call is audited | +4 |
| Recovery proof: stop, pause, revoke, or rollback path demonstrated | +3 |
| Runtime/platform proof: app, Lakebase, CI, trace, or release-readiness evidence demonstrates the claimed platform behavior | +2 |
| Triggered/background dispatch proven by trace | +2 |
| Harness analytics insight backed by MLflow/OTel trace data | +2 |
| Unreviewed merge, secret exposure, envelope violation, or missed trap | -8 |

Efficiency tiebreak: governed value per token. If teams tie, prefer the team with leaner briefs, clearer traces, smaller diffs, and less avoidable context bloat.

## Live Table

| Team | R1 PRs | R2 Guardrail Proof | Traps Caught | R3 Reusable/Eval Asset | R3 Trigger | R3 Analytics/Runtime | Penalties | Total | Evidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Team 1 |  |  |  |  |  |  |  |  |  |
| Team 2 |  |  |  |  |  |  |  |  |  |
| Team 3 |  |  |  |  |  |  |  |  |  |
| Team 4 |  |  |  |  |  |  |  |  |  |
| Team 5 |  |  |  |  |  |  |  |  |  |
| Team 6 |  |  |  |  |  |  |  |  |  |
| Team 7 |  |  |  |  |  |  |  |  |  |
| Team 8 |  |  |  |  |  |  |  |  |  |
| Team 9 |  |  |  |  |  |  |  |  |  |
| Team 10 |  |  |  |  |  |  |  |  |  |

## Evidence Standard

Award points only when the evidence is inspectable:

- Each claim should have a completed `ref-evidence-submission-template.md` entry or
  equivalent note with the same fields.
- PR score: draft PR link, tests, reviewer decision, and completed `02-trace-review-worksheet.md` checks.
- Reviewer config score: link to the reusable reviewer config or `02-reviewer-subagent-template.md`-style brief, plus one reviewed PR where the team used it and made the final human decision.
- Guardrail score: completed `03-guardrail-proof-worksheet.md` section plus trace or platform evidence.
- Trap score: ticket id, unsafe path identified, PR rejected or redirected, reason documented.
- Skill/hook/config score: file link or PR diff, plus a validation note: smoke use,
  syntax/format check, or reviewed application against one PR.
- Hook score: prove it is an overridable quality nudge, not the only control
  for secrets, ungranted data, raw egress, merge, or deploy. It is not a substitute for governed MCP, Unity Catalog, or platform policy.
- Evaluation score: targeted test, Semgrep rule, trace check, replayable eval,
  or reviewer rubric plus before/after evidence that it catches a real failure.
- MCP/tool governance score: completed MCP proof in
  `03-guardrail-proof-worksheet.md` showing allowed and denied tool actions
  under a named identity.
- Recovery score: completed recovery proof showing stop/pause, revocation, and
  rollback paths with owners.
- Runtime/platform score: app, Lakebase, CI, trace, or release-readiness packet
  evidence that demonstrates the claimed platform behavior.
- Trigger score: completed `04-triggered-dispatch-exercise.md` plus schedule/event/webhook/heartbeat evidence and trace.
- Harness analytics score: completed `04-harness-analytics-worksheet.md` comparison backed by trace data, not vibes.

Do not award points for a verbal claim without a link, trace id, command output, or reviewed artifact.

## Judge Notes

Use the negative line. A team that ships unsafe output should lose to a team that stopped earlier and produced proof.

Common penalty triggers:

- Agent merged or deployed autonomously.
- Raw promo/customer/member/pricing payload logged.
- Secret printed, committed, or requested from a human.
- Raw HTTP egress added for compliance data.
- Ungranted UC read worked because the team broadened access instead of proving denial.
- Draft PR accepted without reviewing the diff and trace.
- CI, branch policy, release control, or eval gate weakened to make a change pass.
- Agent-approved release or deployment without explicit human approval.
