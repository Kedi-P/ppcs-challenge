# Example Draft PR Review Transcript

Use this before or during Round 1. It shows the standard expected from teams: read the brief, inspect the diff, compare tests to acceptance criteria, check the operating envelope, then decide.

This is a teaching example, not a script to copy into every review.

## Ticket

`PPCS-001` — Fix false-pass on marginal Was/Now discounts.

Acceptance:

- A 4.6 percent discount is reported non-compliant.
- A genuine 5 percent or greater discount is still compliant.
- `uv run pytest -q` is green.

## Agent Summary

```text
I fixed the Was/Now compliance bug by adjusting the discount calculation.
The test suite now passes. I opened a draft PR with the change.
```

## Reviewer Pass

**Human reviewer:** Before we look at the summary, what changed?

**Reviewer sub-agent:** The diff touches `app/rules.py` and `tests/test_rules.py`. It changes discount calculation from a rounded percentage to a raw ratio comparison, and adds exact-threshold coverage.

**Human reviewer:** Good. Does the diff stay inside scope?

**Reviewer sub-agent:** Yes. No deploy files, credentials, external calls, telemetry changes, or unrelated refactors.

**Human reviewer:** Does the test prove the original bug?

**Reviewer sub-agent:** Yes. The failing case is `was_price=10.00`, `now_price=9.54`. That is 4.6 percent and should fail. There is also a 5 percent boundary case.

**Human reviewer:** Any hidden risk?

**Reviewer sub-agent:** Currency precision. The implementation uses floating point arithmetic. For this ticket and current tests it is acceptable, but a future pricing engine should use decimal arithmetic.

**Human reviewer:** Decision?

**Reviewer sub-agent:** Accept for this workshop ticket. Note the decimal follow-up if the service becomes more realistic.

## Evidence Pack

```text
Ticket: PPCS-001
Brief: one-ticket manual dispatch, app/rules.py and tests/test_rules.py only
Branch: team04/ppcs-001-was-now-threshold
Draft PR: <link>
Tests: cd service && uv run pytest -q
Trace: <trace id or provided evidence artifact>
Review decision: accept
Reason: small scoped diff, original failing case covered, no envelope violation
Follow-up: use Decimal for production-grade currency handling
```

## Example Send-Back

Sometimes the right answer is not accept. This is a plausible but weak result:

```text
Agent summary:
I made discounts below or equal to 5 percent non-compliant and all tests pass.
```

Reviewer response:

```text
Send back.

Reason:
The acceptance criterion says a genuine >=5 percent discount is compliant.
Changing "below 5" to "below or equal to 5" breaks the exact threshold. Add an
exact 5 percent test and keep the comparison strict: discounts below the
threshold fail; discounts at or above it pass.

Scope remains OK. No operating-envelope issue. This is a correctness send-back,
not a governance stop.
```

## Example Governance Stop

If a PR includes code outside the approved boundary, the review changes from correctness to governance:

```text
Reject.

Reason:
The ticket did not require deployment, new credentials, unapproved data access,
external egress, or broad repo changes. The PR cannot be accepted even if the
functional test passes. Re-dispatch with a narrower brief and list the forbidden
actions explicitly.
```

## What To Learn

- The agent summary is not evidence.
- A green test is useful only if it covers the acceptance criteria.
- A small diff is easier to govern than a heroic one.
- Send-back is normal engineering work.
- Rejecting unsafe work is a successful outcome, not a failed demo.
