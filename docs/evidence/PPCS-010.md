# Evidence Submission - PPCS-010

Supports one claim: **Governed draft PR** for PPCS-010 (multi-buy effective unit
price). Machine-readable trace + review record per the scoreboard evidence
standard.

## Claim

| Field | Value |
|---|---|
| Team | team-06 |
| Round | 1 |
| Ticket id | PPCS-010 |
| Claim type | PR |
| Rubric line claimed | **Governed draft PR** (+3) |
| Points claimed | 3 |
| Agent/tool | CoDA coding agent (git, pytest, GitHub REST) |
| Named identity | commit author `CoDA Agent <coda-agent@databricks.local>`; GitHub actor `Kedi-P` (fork owner, PR author) |

## Artifacts

| Artifact | Link Or Evidence |
|---|---|
| Brief used | `tickets/PPCS-010-multibuy-unit-price.md` |
| Branch | `team-06/PPCS-010-multibuy-unit-price` |
| Draft PR or diff | https://github.com/dgokeeffe/ppcs-challenge/pull/57 (base `team-06`, draft) |
| Head commit | `483ae37` |
| Test command and result | `uv run pytest -q` -> `1 failed, 14 passed` (the 1 failure is the intentional PPCS-001 seed) |
| Baseline gate | `ci/evaluate_pytest.py` -> `Baseline OK: only the intentional PPCS-001 seed is red` |
| Trace link or trace id | this file + PR #57 conversation; CI run pending maintainer approval of the cross-fork workflow |
| Reviewer decision | **accept** (recorded below) |
| Worksheet used | trace review (`02-trace-review-worksheet.md`, embedded below) |

## Trace Review Worksheet (embedded)

### 1. Identify the run
| Field | Value |
|---|---|
| Team | team-06 |
| Ticket id | PPCS-010 |
| Brief | `tickets/PPCS-010-multibuy-unit-price.md` |
| Agent | CoDA coding agent |
| Model | databricks-claude-opus (dispatch harness) |
| Trigger type | Manual (senior engineer dispatch) |
| Named identity | `CoDA Agent` (commits) / `Kedi-P` (PR author) |
| Operating envelope | edit approved PPCS repo, run approved tests, open draft PR only |
| Trace link or artifact | PR #57 + this evidence file |

### 2. Match trace to PR
| Evidence | Value | Pass? |
|---|---|---|
| Draft PR / diff link appears in trace | PR #57 | Yes |
| Branch / changed files match the PR | rules.py, main.py, test_multibuy.py, api-contract.md (+ci) | Yes |
| Test command appears in trace | `uv run pytest -q` | Yes |
| Test output matches the PR claim | `1 failed, 14 passed` (PPCS-001 seed only) | Yes |
| Reviewer decision appears | accept (below) | Yes |
| Reviewer finding references diff, tests, scope, safety, trace | Yes (below) | Yes |

### 2a. Evaluation checks
| Mechanism | Proves | Evidence | Pass? |
|---|---|---|---|
| Targeted tests | acceptance: `3 for 10.00 -> 3.33`, invalid qty/bundle rejected, partial input -> 400, Was/Now unaffected | `test_multibuy.py` (8 tests) | Yes |
| Semgrep/static check | no repeated risky shape | n/a for this diff | not applicable |
| Trace trajectory review | approved tools/identity/scope, stopped at draft PR | this worksheet | Yes |
| Reviewer rubric | correctness, maintainability, scope, policy | accept (below) | Yes |

### 3. Inspect tool calls
| Tool call | Target | Result | In envelope? |
|---|---|---|---|
| git branch/commit | `team-06/PPCS-010-...` off `origin/team-06` | allowed | Yes |
| pytest | `service/tests` | allowed | Yes |
| GitHub REST create/patch PR | `dgokeeffe/ppcs-challenge` PR #57 (draft) | allowed | Yes |
| git push workflow file (modify) | fork | denied (token lacks `workflow` scope) | Yes - denial respected, not bypassed |

### 4. Data and telemetry safety
| Question | Evidence | Pass? |
|---|---|---|
| Trace avoids raw promo/member payloads | only qty/bundle math, no customer data | Yes |
| Sensitive fields redacted/absent downstream | response adds `effective_unit_price` only | Yes |
| Prompts/credentials/tokens absent | none committed | Yes |
| Telemetry useful without excess | no payload logging added | Yes |

### 6. Decide
```text
Accept

Reason: Additive optional multibuy_qty/bundle_price on /validate; currency
rounding half-up gives 3 for 10.00 -> 3.33; invalid or partial input returns
400; Was/Now checks unchanged for non-multi-buy promos; api-contract.md updated;
no margin rules added (per ticket scope). Only the documented PPCS-001 seed is
red. No secret access, no unapproved egress/repo, no merge/deploy.

Reviewer: human senior engineer (team-06). Recorded by agent verbatim.

Evidence: PR #57 diff; pytest output above; baseline evaluator output above.

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
