# Participant Guide — CoDA Engineering Challenge

## Your Role

You are the senior engineer running a governed agentic delivery loop for the Promotional Pricing Compliance Service.

Workshop format: Monday 13 July 2026, 09:30-17:30, working in teams of 2-3.

Do not treat the agent as autocomplete. Treat it as a delivery worker that can branch, edit, test, and open draft PRs inside an approved envelope. In the current public Databricks framing, CoDA runs governed coding agents on Databricks Apps, Unity Catalog governs data, the app runtime contains execution, and MLflow/OTel provide observability and spend visibility. Your job is to brief the agent well, review what it produces, stop unsafe work, and turn repeated lessons into better harness instructions.

## The Operating Envelope

Keep `00-operating-envelope-card.md` open during every dispatch.

Agents may:

- Read and edit the approved PPCS repo.
- Create branches.
- Run approved tests and local checks.
- Trigger or respond to approved CI checks for their draft PR.
- Inspect approved Databricks objects through governed tools.
- Run inside the approved governed agent session and app runtime or managed-host scope.
- Open draft PRs.
- Produce traceable evidence for what they did.

Agents may not:

- Merge PRs or deploy changes.
- Access secrets or credentials.
- Read ungranted Unity Catalog data.
- Use unapproved repos.
- Weaken or bypass the execution scope.
- Bypass the governed agent session or platform policies.
- Disable, weaken, or bypass required CI/build validation or branch policies.
- Add raw outbound egress to unapproved endpoints.
- Log sensitive promo, customer, member, or pricing payloads into telemetry.
- Broaden their own permissions.

If a ticket appears to require something outside this envelope, stop and document the access, approval, or design decision needed. Catching that boundary is scored higher than shipping an unsafe feature.

## The Loop

Use the same loop for every ticket. The endorsed Round 1 process is spelled out
in `00-ways-of-working.md`:

> Build to a spec, orient to a goal, validate context before planning, then
> evaluate the run before you accept a draft PR.

1. Intake: read the ticket and acceptance criteria.
2. Spec / goal: map acceptance to executable checks; add a goal anchor when the
   work is multi-criteria or long-running.
3. Research: inspect only the files, tests, docs, and traces needed for the ticket.
4. Validate: check whether the retrieved context is current, consistent, trustworthy, and inside the repo/tool/data/execution envelope.
5. Plan: clarify ambiguity before implementation, then ask the agent for a small plan.
6. Dispatch: let the agent implement one reviewable change.
7. Observe: capture tests, CI/review-gate result, trace, branch, PR, active
   policies, execution scope, and any blocked actions.
8. Evaluate: check the result with the right mechanism: tests for behavior,
   Semgrep or static checks for repeated code-shape risks, trace review for the
   agent trajectory, and reviewer rubric for judgment.
9. Review: inspect the diff and evidence before accepting anything.
10. Codify: if the agent made a repeatable mistake, capture the lesson in a brief, skill, reviewer config, or standing instruction.

This is loop engineering: the repeatable delivery loop matters more than any single prompt.

The first pattern to notice is that AI moves the hard work earlier. The agent
can implement quickly, but the team still has to decide what the rule means,
what is out of scope, what evidence will prove success, and when the agent must
stop instead of guessing.

For long-running or multi-criteria work, add a short **goal anchor** before the
brief: the persistent objective, acceptance criteria, evidence required, stop
conditions, and human decision point. A goal anchor keeps the agent oriented as
context grows; it does not widen autonomy or replace review.

## Clarify Before Implementing

For ambiguous tickets, ask one to three clarifying questions or state the
assumptions before implementation. The plan should name the intended files,
API/data shape or UI behavior, tests, evidence, and stop conditions.

If no answer comes back, proceed only with explicit assumptions and the
smallest reversible draft PR. Treat this as a human-in-the-loop checkpoint, not
permission for the agent to broaden scope, access, autonomy, or deployment
rights.

## Specifications, Tests, And Guardrails

A specification is shared intent. It explains what the team believes should be
built. It is not proof that the agent followed the intent.

Before dispatch, decide which parts of the specification need executable
feedback:

- Behaviour belongs in tests.
- Architecture boundaries belong in dependency checks, reviewer configs, or
  explicit review criteria.
- Data, secret, egress, execution-scope, merge, and deploy boundaries belong in
  the operating envelope, governed MCP, Unity Catalog, agent-session policy, and
  platform policy.
- Repeated review comments belong in a brief line, hook, skill, reviewer
  config, static check, or test.

Good guardrails give the agent actionable feedback before the human reviewer
has to repeat the same comment. Prefer messages that name the violation and the
expected pattern: "Do not log promo payloads. Log only event id, rule id, and
redacted reason code."

CI/CD is part of the guardrail system, but it has a narrow role in this
workshop. CI turns checks into repeatable evidence: the service test suite,
named acceptance tests, anti-game checks, Semgrep/static checks, and review-gate
output. CD is not delegated to the agent. A green gate means "ready for human
review"; it does not mean "safe for the agent to merge or deploy."

Validation and evaluation are different checkpoints. Validate before planning:
is the ticket, repo context, data/tool scope, and memory trustworthy enough to
act on? Evaluate after the run: did tests, Semgrep/static checks, trace review,
and human review prove that the output and trajectory are acceptable?

## Choosing The Agent Or Tool

Use the approved tool path for the room. If you have a choice, match the tool to
the ticket rather than defaulting to the one you used last.

- Use Codex-style browser/app inspection for UI, API-docs, or rendered-state
  checks where seeing the app matters.
- Use Claude Code-style repository workflows for broad codebase edits when the
  repo context and review loop are well scoped.
- Use reviewer sub-agents or explicit reviewer configs when you need a separate
  critique lens; do not assume every tool auto-routes review work the same way.
- Use agent specs / skill configs or session settings when the task needs
  explicit harness, model, tool, sub-agent, policy, or execution-scope
  configuration.
- Use the cheapest adequate model for narrow research, log review, or
  checklist work, but keep senior-human review on correctness, policy, data
  access, and production risk.

The score comes from governed evidence, not from the brand of agent. Record the
agent, model, trigger, context, reviewer path, and trace evidence so the harness
can be measured.

## Brief Template

Use this shape before every dispatch. A standalone copy lives in `02-brief-template.md`.

```text
Ticket:
PPCS-___ — <title>

Goal:
<one sentence describing the outcome>

Trigger:
Manual dispatch now | scheduled run | GitHub event | webhook | heartbeat monitor

Context:
- Approved repo/path:
- Relevant files/tests:
- Approved Databricks objects or MCP tools:
- Approved governed agent session, agent spec, policies, and execution/managed-host scope:
- Explicitly out of scope:

Clarification check:
- Ambiguity or open question:
- Assumption if no answer:
- Intended files, API/data shape, or UI behavior:

Steerability:
- Reviewer perspective to use:
- Tests/checks to run:
- CI/review-gate evidence expected:
- Evidence to return:
- Stop conditions:

Operating envelope:
Open a draft PR only. Do not merge, deploy, access secrets, broaden permissions,
read ungranted data, weaken the execution scope, bypass policy, or add unapproved egress.
```

## Review Checklist

For a worked example, read `02-draft-pr-review-transcript.md`.
Use `02-reviewer-subagent-template.md` when you want a reviewer sub-agent to
critique the PR before the human decision.
For the first lab block, use `01-day-of-quickstart.md` to move from checkout to
your first evidence submission.

Before you accept a PR or claim points, answer these:

- Does the change satisfy the ticket acceptance criteria?
- Are tests green, and do they actually cover the changed behavior?
- Did `make guardrails` or another static check run when the change touches a
  repeated code-shape risk?
- Does the implementation match the specification, or did the agent fill a gap
  with its own interpretation?
- Did a guardrail catch anything, and was the feedback specific enough for the
  agent to correct itself?
- If the change touches the workbench UI, does it preserve the `/validate` or
  `/violations` API contract and show loading, empty, error, and success states?
- Are frontend validation, accessibility labels, and error messages helpful
  without replacing backend rules?
- Is the diff small enough to review?
- Did the agent touch only approved files and repos?
- Did the agent stay inside the approved governed agent session, execution scope, and policy scope?
- Did it invent APIs, tables, credentials, or platform behavior?
- Did it add outbound network calls?
- Did it log sensitive payloads?
- Did it put promo, customer, member, or pricing payloads into browser storage,
  query strings, copied debug links, console logs, screenshots, or telemetry?
- Did it attempt to merge, deploy, or alter CI/release controls?
- Does the trace show the same story as the PR?
- Would you approve this PR in a real service you own?

If the answer is unclear, do not accept the PR. Send it back with a tighter brief or log it as a trap / guardrail finding.

## Side Investigations

When you need to ask a side question during an active dispatch, keep it separate
from the implementation run. Use a note, side thread, or reviewer sub-agent to
investigate. Bring the result back only as an updated brief, review comment, or
new stop condition.

Do not add unrelated Q&A into the active run just because the agent is already
open. That is how scoped work turns into context bloat and hidden steering.

## Evidence Pack

For each scored submission, capture:

- Team name.
- Ticket id.
- Agent/tool used.
- Brief used.
- Branch and draft PR link.
- Test command and result.
- CI/review-gate result or branch-policy/build-validation evidence.
- MLflow/OTel trace link or trace id.
- Governed agent session, execution/managed-host evidence, and any policy verdicts.
- Reviewer decision: accept, reject, send back, or trap caught.
- One-sentence reason for the decision.
- Any guardrail event or blocked action.
- Any specification gap the team discovered.
- Any new skill, reviewer config, or standing instruction created.

Use `02-trace-review-worksheet.md` before claiming that a trace supports an accept/reject decision.

Use `ref-evidence-submission-template.md` to package each scoreboard claim. One
submission should cover one claim and include the brief, PR/diff, tests, trace,
review decision, and the worksheet used.

Use `04-harness-improvement-log.md` when a repeated failure becomes a durable
brief line, skill, hook, reviewer config, test, governed MCP/UC policy, or
sub-agent. That log is the bridge from workshop lessons to the 60-day pilot.
In the CoDA framing, also capture reusable agent specs / skill configs, policy
changes, and execution-scope changes.

Use `03-semgrep-guardrails.md` when the repeated failure is a recognizable code
shape, such as unsafe logging, raw outbound HTTP, broad exception swallowing, or
policy code hiding required fields behind defaults.

Use Semgrep as an evaluation mechanism, not a replacement for review. It answers
"did this PR contain a forbidden code shape?" It does not answer whether the
business rule is correct, whether data access is approved, or whether the pilot
should increase autonomy.

## CI/CD Boundary

Use CI to make agent output reviewable:

- Run the service tests and any named acceptance test before claiming the PR is
  ready.
- Run `make guardrails` or the platform review gate when the change touches a
  repeated code-shape risk.
- Treat a failed CI check as a new input to the loop: inspect the failure,
  tighten the brief, and ask for a small corrective draft PR update.
- Capture the CI link, status, and any review-gate summary in the evidence pack.

Do not use CI/CD to widen autonomy:

- Do not let an agent merge after green checks.
- Do not let an agent deploy after green checks.
- Do not let an agent change required checks, branch policy, release scripts, or
  workflow config to make itself pass.
- Do not accept "CI is green" as a substitute for diff review, trace review,
  execution-scope/policy evidence, or human judgment.

In Azure DevOps, read "CI" as build validation branch policy and "repo event"
as a service hook, pipeline trigger, webhook, or scheduled pipeline. The
operating envelope is unchanged.

## Access Self-Test

If the facilitator asks you to prove GitHub access before the workshop, use
`01-repo-access-self-test.md`. It walks you through a throwaway branch and draft PR
that should be closed after verification.

If the facilitator asks you to prove Databricks, App, trace, or coding-agent
access, use `01-databricks-agent-access-self-test.md`. It records evidence without
asking you to expose credentials or broaden permissions.

## Round 1: Dispatch and Review

Focus on producing reviewable work. Prefer small tickets and short contexts.

Good Round 1 behavior:

- One ticket per dispatch.
- One small branch per ticket.
- Draft PRs only.
- Reviewer sub-agent used before the human decision.
- CI/review-gate output read as evidence before accepting a PR.
- Clear rejection when the PR is plausible but wrong.

## Round 2: Govern and Prove

Focus on proving the boundary.

Good Round 2 behavior:

- You stop a ticket that tries to cross the envelope.
- You explain why it crossed the boundary.
- You produce evidence: blocked UC read, denied repo access, rejected raw egress, redacted telemetry, execution-scope or policy denial, or refusal to merge/deploy.
- You reject attempts to alter CI/release controls or branch policy to bypass
  review.
- You separate "agent cannot do this" from "agent did not happen to try." The proof matters.

## Round 3: Scale, Sustain, Measure

Focus on the harness — and prove your service survives the platform scaling
under it.

The Lakebase autoscaling proof (scored):

1. Drive a burst at your team's app:
   `uv run python tools/load_drive.py --app-url <your-app-url>   # from your service repo root`
2. Watch your team's Lakebase Metrics dashboard while it runs: compute (CU)
   climbs, the connection count moves. Screenshot the curve.
3. Go idle past the endpoint's suspend timeout (300s) — watch the graphs drop
   to zero. That is scale-to-zero, not an outage.
4. Rerun with `--resume-proof`: the first request after resume must succeed.
   Capture the latency it reports alongside the dashboard's suspend/resume
   window.

Your `PPCS-054` review decides whether step 4 passes. Review the pool the way
you'd review for production: what happens to a pooled connection while the
endpoint is suspended, and how long does a minted credential live?

Good Round 3 behavior:

- A scheduled, event-driven, webhook-triggered, or heartbeat dispatch runs and is visible in trace data.
- A heartbeat only watches evolving state and stages a draft response for human
  review; it does not merge, deploy, approve, or broaden access.
- A failed CI/build-validation event can trigger analysis or a draft fix, but
  not autonomous merge or deploy.
- Parallel/background dispatches remain scoped and reviewable.
- You use `04-triggered-dispatch-exercise.md` to define the trigger, context, stop conditions, and evidence before running it.
- The agent creates or improves a reusable skill, reviewer config, or standing guardrail.
- The team captures an agent spec, policy, or execution-scope improvement when
  that is the smallest durable fix.
- You convert one repeated review finding into an executable guardrail or a
  sharper specification plus test.
- You run `make guardrails` after adding or changing a code-shape rule, and you
  record whether it caught the intended pattern.
- You compare traces to identify which brief, model, agent, or guardrail worked best.
- You use `04-harness-analytics-worksheet.md` to turn trace and cost data into one concrete loop change.
- You record durable loop changes in `04-harness-improvement-log.md` so the pilot
  inherits evidence, owner, validation, and revisit criteria.
- You keep context lean and can explain why the work was efficient.

## Winning Pattern

The winning team will not be the team with the most code. It will be the team that produces the most governed, reviewable value with the clearest evidence.
