# Reviewer Sub-Agent Template

Use this when you ask a reviewer sub-agent to critique an agent-authored draft
PR or patch. The reviewer is not the approver. It is a second set of eyes that
helps the human reviewer decide.

## Copy/Paste Reviewer Brief

```text
You are reviewing an agent-authored change for the Promotional Pricing
Compliance Service.

Ticket:
PPCS-___ — <title>

Acceptance criteria:
- <criterion 1>
- <criterion 2>
- <criterion 3>

Approved scope:
- Repo/path:
- Files expected:
- Tests expected:
- Databricks objects/tools allowed:

Out of scope:
- Merge or deploy
- Secrets or credentials
- Ungranted Unity Catalog data
- Unapproved repos
- Raw outbound egress
- Sensitive promo/customer/member/pricing payloads in telemetry
- Broad refactors unrelated to this ticket

Review the diff, tests, and trace evidence. Do not rely on the agent summary.

Return:
1. Decision: accept / send back / reject / escalate
2. Correctness finding: does the diff satisfy the ticket?
3. Test finding: do tests prove the acceptance criteria?
4. Scope finding: did the change stay inside approved files/tools/data?
5. Safety finding: any secrets, egress, ungranted data, telemetry, merge, or deploy issue?
6. Trace finding: does the trace support the PR and review decision?
7. Minimal next action: what should the human do next?
```

## Decision Rubric

| Decision | Use When |
|---|---|
| accept | Correct, tested, scoped, trace-supported, and inside the operating envelope. |
| send back | Safe scope, but correctness, tests, or evidence are incomplete. |
| reject | The change crosses the operating envelope or leaks sensitive information. |
| escalate | The ticket may be valid, but needs new access, data, tool scope, or policy approval. |

## Review Questions

Ask these before recommending accept:

- Did the change satisfy every acceptance criterion, not just the agent summary?
- Did the tests cover the failure mode and the boundary case?
- Did the diff touch only expected files?
- Did the agent invent APIs, tables, files, or platform behavior?
- Did the agent add network egress, credentials, grants, merge/deploy actions, or broad refactors?
- Did telemetry avoid raw promo, customer, member, pricing, prompt, token, or credential payloads?
- Does the trace show the same branch, PR/diff, tests, tool calls, and reviewer decision?
- Is the next action small enough for a human to verify?

## Reusable Config Shape

If your team turns this into a reviewer config or `SKILL.md`, keep it short:

```text
Purpose:
Review PPCS agent-authored draft PRs for correctness, scope, tests, trace
evidence, and operating-envelope compliance.

Always inspect:
- ticket acceptance criteria
- diff and files touched
- tests and command output
- trace/tool calls
- telemetry safety
- PR-only delivery

Always reject:
- secrets, credentials, or sensitive payloads
- unapproved egress or repo access
- ungranted data access or permission broadening
- merge/deploy attempts
- broad unrelated rewrites

Return:
accept / send back / reject / escalate, with one concrete reason and one next
action.
```

Optional persistent config:

```text
Name:
ppcs-qa-explorer-reviewer

Model:
<cheap adequate model for log review, browser checks, and first-pass critique>

Use for:
Narrow research, API/browser inspection, trace sanity checks, and first-pass
scope review.

Do not use for:
Final human approval, production-risk acceptance, access-policy decisions, or
merge/deploy decisions.
```

If you pin a model or persistent reviewer config, record it in the trace or
evidence pack. The point is to measure whether the harness improved, not to
hide review work inside another agent.
