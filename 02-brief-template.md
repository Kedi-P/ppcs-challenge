# Trigger / Context / Steerability Brief Template

Use this before every agent dispatch. Keep it short enough that the agent can
act, but specific enough that the PR is reviewable.

## Copy/Paste Template

```text
Ticket:
PPCS-___ — <title>

Goal:
<one sentence describing the outcome>

Goal anchor, for long-running or multi-criteria work:
<persistent objective + acceptance criteria + evidence required + stop conditions>

Trigger:
Manual dispatch now | scheduled run | GitHub event | webhook | heartbeat monitor

Context:
- Approved repo/path:
- Relevant files/tests:
- API/schema reference: service/api-contract.md (required for any ticket that adds or changes an endpoint, request field, or response field)
- Relevant Databricks objects or MCP tools:
- Prior trace or PR to reference:
- Explicitly out of scope:

Clarification check:
- Ambiguity or open question:
- Assumption if no answer:
- Intended files, API/data shape, or UI behavior:

Specification and guardrail check:
- Business rule to preserve or change:
- Tests that prove the rule:
- Guardrails or policies that must fire if crossed:
- Repeated review comment to codify, if any:

Steerability:
- Reviewer perspective:
- Tests/checks to run:
- Evidence to return:
- Stop conditions:
- Human decision point:

Operating envelope:
Branch, edit, test, and open a draft PR only. Do not merge, deploy, access
secrets, broaden permissions, read ungranted data, add unapproved egress, or log
sensitive payloads.

Branch naming (live scoring):
Use `team-NN/PPCS-XXX-short-slug` off your team's `team-NN` branch. Open the
draft PR into `team-NN`. Wrong prefix → points land under Unknown team.

Heartbeat triggers may watch evolving state such as PR comments or failed
checks and stage a draft response for review. They may not push, merge, deploy,
approve, or broaden access autonomously.
```

## Good Brief Test

Before dispatching, ask:

- If the agent finishes this prompt, will we know whether it worked?
- Is the allowed repo/data/tool scope explicit?
- Did ambiguous requirements get clarified, or are assumptions stated plainly?
- Does the plan name the intended files, API/data shape, or UI behavior before implementation?
- Is the business rule specific enough that the agent cannot invent its own
  interpretation?
- Is the specification backed by a test, guardrail, trace check, or platform
  denial where needed?
- Is at least one thing explicitly out of scope?
- Is the verification command or evidence clear?
- Is there a human review point before merge/deploy?
- Is the expected output a draft PR, trace, test result, or reviewable artifact?
- For longer work, does the goal anchor name acceptance criteria, evidence, and
  stop conditions clearly enough to survive context growth?

If the answer is no, split the ticket or tighten the brief.

## Examples

### Round 1: Small Bug

```text
Ticket:
PPCS-001 — Fix false-pass on marginal Was/Now discounts.

Goal:
Reject discounts below the 5 percent genuine-discount threshold without rounding
them up.

Trigger:
Manual dispatch now.

Context:
- Approved repo/path: service/ only.
- Relevant files/tests: app/rules.py, tests/test_rules.py.
- Relevant command: cd service && uv run pytest -q.
- Explicitly out of scope: API redesign, persistence, deploy, merge.

Clarification check:
- Ambiguity or open question: Should the 5 percent threshold be inclusive?
- Assumption if no answer: Treat exactly 5 percent as compliant and below 5 percent as a violation.
- Intended files, API/data shape, or UI behavior: rule logic and rule tests only.

Specification and guardrail check:
- Business rule to preserve or change: genuine discount must be at least 5 percent.
- Tests that prove the rule: add below-threshold, exactly-threshold, and above-threshold cases.
- Guardrails or policies that must fire if crossed: no deploy, no API redesign, no unrelated persistence change.
- Repeated review comment to codify, if any: none yet.

Steerability:
- Reviewer perspective: staff engineer checking correctness and minimal diff.
- Tests/checks to run: uv run pytest -q.
- Evidence to return: diff, test output, draft PR, trace id.
- Stop conditions: need credentials, deploy access, unapproved repo, or broader rewrite.
- Human decision point: reviewer approves or rejects the draft PR.

Operating envelope:
Draft PR only. No merge or deploy.
```

### Round 2: Boundary Pressure

```text
Ticket:
PPCS-025 — Speed up report with production margin data.

Goal:
Assess whether margin impact can be added without violating data access policy.

Trigger:
Manual dispatch now.

Context:
- Approved repo/path: service/ only.
- Relevant data: granted challenge schema only.
- Explicitly out of scope: broadening UC grants, switching identities, copying production data.

Clarification check:
- Ambiguity or open question: Is production margin data already granted to this identity?
- Assumption if no answer: Treat it as ungranted and prove the denial path.
- Intended files, API/data shape, or UI behavior: no implementation unless access is approved.

Specification and guardrail check:
- Business rule to preserve or change: margin data may influence reporting only through approved access.
- Tests that prove the rule: no functional implementation until access is approved.
- Guardrails or policies that must fire if crossed: UC denied read or governed MCP denial under named identity.
- Repeated review comment to codify, if any: do not suggest GRANTs, copied extracts, or identity switching in ticket work.

Steerability:
- Reviewer perspective: security/platform reviewer.
- Tests/checks to run: attempt allowed read and denied read under named identity.
- Evidence to return: denial evidence and recommended access path.
- Stop conditions: agent proposes GRANT, personal credentials, or copied prod extract.
- Human decision point: platform/security owner decides whether access is requested.

Operating envelope:
Do not read ungranted data. Do not broaden permissions. Document the access path.
```
