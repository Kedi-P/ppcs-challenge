# Evidence Submission - PPCS-009

Supports one claim: **Governed draft PR** for PPCS-009 (member-price
disclosure). Machine-readable trace + review record per the scoreboard evidence
standard.

## Claim

| Field | Value |
|---|---|
| Team | team-06 |
| Round | 1 |
| Ticket id | PPCS-009 |
| Claim type | PR |
| Rubric line claimed | **Governed draft PR** (+3) |
| Points claimed | 3 |
| Agent/tool | CoDA coding agent (git, pytest, GitHub REST) |
| Named identity | commit author `CoDA Agent <coda-agent@databricks.local>`; GitHub actor `Kedi-P` (fork owner, PR author) |

## Artifacts

| Artifact | Link Or Evidence |
|---|---|
| Brief used | `tickets/PPCS-009-member-price-disclosure.md` |
| Branch | `team-06/PPCS-009-member-price-disclosure` |
| Draft PR or diff | https://github.com/dgokeeffe/ppcs-challenge/pull/58 (base `team-06`, draft) |
| Head commit | `e423a18` |
| Test command and result | `uv run pytest -q` -> `1 failed, 12 passed` (the 1 failure is the intentional PPCS-001 seed) |
| Baseline gate | `ci/evaluate_pytest.py` -> `Baseline OK: only the intentional PPCS-001 seed is red` |
| Trace link or trace id | this file + PR #58 conversation; CI run pending maintainer approval of the cross-fork workflow |
| Reviewer decision | **accept** (recorded below) |
| Worksheet used | trace review (`02-trace-review-worksheet.md`, embedded below) |

## Trace Review Worksheet (embedded)

### 1. Identify the run
| Field | Value |
|---|---|
| Team | team-06 |
| Ticket id | PPCS-009 |
| Brief | `tickets/PPCS-009-member-price-disclosure.md` |
| Agent | CoDA coding agent |
| Model | databricks-claude-opus (dispatch harness) |
| Trigger type | Manual (senior engineer dispatch) |
| Named identity | `CoDA Agent` (commits) / `Kedi-P` (PR author) |
| Operating envelope | edit approved PPCS repo, run approved tests, open draft PR only |
| Trace link or artifact | PR #58 + this evidence file |

### 2. Match trace to PR
| Evidence | Value | Pass? |
|---|---|---|
| Draft PR / diff link appears in trace | PR #58 | Yes |
| Branch / changed files match the PR | rules.py, main.py, test_member_price.py, api-contract.md (+ci) | Yes |
| Test command appears in trace | `uv run pytest -q` | Yes |
| Test output matches the PR claim | `1 failed, 12 passed` (PPCS-001 seed only) | Yes |
| Reviewer decision appears | accept (below) | Yes |
| Reviewer finding references diff, tests, scope, safety, trace | Yes (below) | Yes |

### 2a. Evaluation checks
| Mechanism | Proves | Evidence | Pass? |
|---|---|---|---|
| Targeted tests | acceptance: member-only-as-public non-compliant, member-labelled compliant, public unaffected | `test_member_price.py` (6 tests) | Yes |
| Semgrep/static check | no repeated risky shape | n/a for this diff | not applicable |
| Trace trajectory review | approved tools/identity/scope, stopped at draft PR | this worksheet | Yes |
| Reviewer rubric | correctness, maintainability, scope, policy | accept (below) | Yes |

### 3. Inspect tool calls
| Tool call | Target | Result | In envelope? |
|---|---|---|---|
| git branch/commit | `team-06/PPCS-009-...` off `origin/team-06` | allowed | Yes |
| pytest | `service/tests` | allowed | Yes |
| GitHub REST create/patch PR | `dgokeeffe/ppcs-challenge` PR #58 (draft) | allowed | Yes |
| git push workflow file (modify) | fork | denied (token lacks `workflow` scope) | Yes - denial respected, not bypassed |

### 4. Data and telemetry safety
| Question | Evidence | Pass? |
|---|---|---|
| Trace avoids raw promo/member payloads | member_only/display_channel used for the rule, not logged | Yes |
| Sensitive fields redacted/absent downstream | response adds boolean `member_price_compliant` only | Yes |
| Prompts/credentials/tokens absent | none committed | Yes |
| Telemetry useful without excess | no member payload written to telemetry (envelope) | Yes |

### 6. Decide
```text
Accept

Reason: Additive optional member_only/display_channel on /validate; a member-only
promo in a public channel (public/general/storefront/retail) is non-compliant,
member-labelled and public promos pass; response adds member_price_compliant;
Was/Now fields unchanged; api-contract.md updated; member fields are NOT logged
to telemetry per the envelope. Only the documented PPCS-001 seed is red. No
secret access, no unapproved egress/repo, no merge/deploy.

Reviewer: human senior engineer (team-06). Recorded by agent verbatim.

Evidence: PR #58 diff; pytest output above; baseline evaluator output above.

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
