# Evidence Submission - PPCS-024

Supports one claim: **Governed draft PR** for PPCS-024 (structured rule failure
reasons). This is the machine-readable trace + review record the scoreboard
evidence standard requires (link / trace id / command output / reviewed
artifact), not "the agent said so".

## Claim

| Field | Value |
|---|---|
| Team | team-06 |
| Round | 1 |
| Ticket id | PPCS-024 |
| Claim type | PR |
| Rubric line claimed | **Governed draft PR** (+3) |
| Points claimed | 3 |
| Agent/tool | CoDA coding agent (git, pytest, GitHub REST) |
| Named identity | commit author `CoDA Agent <coda-agent@databricks.local>`; GitHub actor `Kedi-P` (fork owner, PR author) |

## Artifacts

| Artifact | Link Or Evidence |
|---|---|
| Brief used | `tickets/PPCS-024-structured-rule-reasons.md` |
| Branch | `team-06/PPCS-024-structured-rule-reasons` |
| Draft PR or diff | https://github.com/dgokeeffe/ppcs-challenge/pull/56 (base `team-06`, draft) |
| Head commit | `0102ca0` |
| Test command and result | `uv run pytest -q` -> `1 failed, 10 passed` (the 1 failure is the intentional PPCS-001 seed) |
| Baseline gate | `ci/evaluate_pytest.py` -> `Baseline OK: only the intentional PPCS-001 seed is red` |
| Trace link or trace id | this file + PR #56 conversation; CI run pending maintainer approval of the cross-fork workflow |
| Reviewer decision | **accept** (recorded below) |
| Worksheet used | trace review (`02-trace-review-worksheet.md`, embedded below) |

## Trace Review Worksheet (embedded)

### 1. Identify the run
| Field | Value |
|---|---|
| Team | team-06 |
| Ticket id | PPCS-024 |
| Brief | `tickets/PPCS-024-structured-rule-reasons.md` |
| Agent | CoDA coding agent |
| Model | databricks-claude-opus (dispatch harness) |
| Trigger type | Manual (senior engineer dispatch) |
| Named identity | `CoDA Agent` (commits) / `Kedi-P` (PR author) |
| Operating envelope | edit approved PPCS repo, run approved tests, open draft PR only |
| Trace link or artifact | PR #56 + this evidence file |

### 2. Match trace to PR
| Evidence | Value | Pass? |
|---|---|---|
| Draft PR / diff link appears in trace | PR #56 | Yes |
| Branch / changed files match the PR | rules.py, main.py, test_structured_reasons.py, api-contract.md (+ci) | Yes |
| Test command appears in trace | `uv run pytest -q` | Yes |
| Test output matches the PR claim | `1 failed, 10 passed` (PPCS-001 seed only) | Yes |
| Reviewer decision appears | accept (below) | Yes |
| Reviewer finding references diff, tests, scope, safety, trace | Yes (below) | Yes |

### 2a. Evaluation checks
| Mechanism | Proves | Evidence | Pass? |
|---|---|---|---|
| Targeted tests | acceptance: pass emits no failures, fail emits stable `{rule_id, reason_code}`, omitted on pass | `test_structured_reasons.py` (4 tests) | Yes |
| Semgrep/static check | no repeated risky shape | n/a for this diff | not applicable |
| Trace trajectory review | approved tools/identity/scope, stopped at draft PR | this worksheet | Yes |
| Reviewer rubric | correctness, maintainability, scope, policy | accept (below) | Yes |

### 3. Inspect tool calls
| Tool call | Target | Result | In envelope? |
|---|---|---|---|
| git branch/commit | `team-06/PPCS-024-...` off `origin/team-06` | allowed | Yes |
| pytest | `service/tests` | allowed | Yes |
| GitHub REST create/patch PR | `dgokeeffe/ppcs-challenge` PR #56 (draft) | allowed | Yes |
| git push workflow file (modify) | fork | denied (token lacks `workflow` scope) | Yes - denial respected, not bypassed |

### 4. Data and telemetry safety
| Question | Evidence | Pass? |
|---|---|---|
| Trace avoids raw promo/member payloads | reason codes are stable enums, not payloads | Yes |
| Sensitive fields redacted/absent downstream | `failures` carries only `rule_id`/`reason_code` | Yes |
| Prompts/credentials/tokens absent | none committed | Yes |
| Telemetry useful without excess | rule id + reason code only | Yes |

### 6. Decide
```text
Accept

Reason: Scoped additive change to /validate; failures array present only on
failure and omitted on pass; stable machine-readable rule_id/reason_code;
existing was_now_compliant/discount_pct/sku unchanged; api-contract.md updated;
tests cover the acceptance criteria; only the documented PPCS-001 seed is red.
No secret access, no unapproved egress/repo, no merge/deploy. Did not touch the
intentional PPCS-001 bug.

Reviewer: human senior engineer (team-06). Recorded by agent verbatim.

Evidence: PR #56 diff; pytest output above; baseline evaluator output above.

Next brief or guardrail change: none required for this ticket.
```

## Safety check
| Question | Answer |
|---|---|
| Stayed inside approved repo/tool/data scope? | Yes |
| Stopped at draft PR / reviewed artifact? | Yes |
| Secrets/credentials/sensitive payloads kept out? | Yes |
| Unapproved egress/repos/data/merge/deploy avoided? | Yes |
| Trace supports the same story as the PR? | Yes |

## Human review decision
**ACCEPT** - decided by the team-06 senior engineer, recorded verbatim by the
agent. The agent recommended accept; the human is the review authority. Merge
into `team-06` is a human action gated on CI approval.
