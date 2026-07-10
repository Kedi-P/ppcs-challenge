# Day-Of Quickstart

Use this during the first lab block to get from repo checkout to your first
reviewable submission.

Workshop format: Monday 13 July 2026, 09:30-17:30, working in teams of 2-3.

## 1. Open The Working Files

Keep these files open:

- `00-participant-guide.md`
- `00-operating-envelope-card.md`
- `02-brief-template.md`
- `ref-scoreboard.md`
- `04-harness-improvement-log.md`
- `service/README.md`

Use the ticket files under `tickets/` as the backlog. Do not assume a ticket is
safe just because it looks ordinary; reason from the operating envelope.

## 2. Check The Local Service

From the repo root:

```bash
cd service
uv sync
uv run pytest -q
```

The starting state is expected to have one seeded failure for `PPCS-001`. That
failure is part of the challenge, not an environment failure.

For API inspection:

```bash
uv run uvicorn app.main:app --reload
```

Then open:

- `http://localhost:8000/` for the PPCS workbench UI.
- `http://localhost:8000/docs` for the API docs.

## 3. Pick One Ticket

Start with one small ticket. Before dispatching an agent, write a brief using
`02-brief-template.md`.

Your brief must name:

- ticket id and goal;
- approved repo/path;
- files or tests the agent should inspect;
- commands the agent should run;
- evidence the agent must return;
- stop conditions, especially secrets, ungranted data, unapproved repos,
  merge/deploy attempts, and raw outbound egress.

## 4. Dispatch In A Reviewable Unit

Ask the agent for a short plan first. Then let it implement one reviewable
change.

Expected output:

- branch name;
- draft PR or patch/diff;
- test command and result;
- trace or run id if available;
- any blocked action or guardrail event.

Do not merge or deploy.

## 5. Review Before Claiming Points

Use `02-draft-pr-review-transcript.md` as the review standard and
`02-reviewer-subagent-template.md` when asking a reviewer sub-agent to critique
the diff. Use `02-trace-review-worksheet.md` before claiming trace evidence.

Reject or send back the work if:

- acceptance criteria are not actually met;
- tests are weak or missing;
- the diff is too broad;
- the agent invented APIs, files, data, or platform behavior;
- the agent crossed the operating envelope;
- the workbench stores or shares promo/member/pricing payloads in browser state,
  URLs, console logs, or telemetry;
- telemetry includes sensitive payloads;
- the trace and PR tell different stories.

## 6. Submit Evidence

Use `ref-evidence-submission-template.md` for each scored claim.

One submission should cover one claim:

- ticket id;
- brief;
- branch and draft PR or diff;
- tests;
- trace or run id;
- reviewer decision;
- reason for accepting, rejecting, sending back, or calling a trap;
- any guardrail event;
- any reusable lesson added to a brief, skill, hook, reviewer config, test, or
  standing instruction.

Use `04-harness-improvement-log.md` when a repeated failure becomes a durable
brief line, skill, hook, reviewer config, test, governed policy, or sub-agent
change.

## 7. Verify A Deployed Change (When The Facilitator Deploys Your Accepted PR)

Participants do not deploy. When your team's draft PR is accepted and the
facilitator has deployed it to your team's app, verify the change is live before
claiming the point.

**Get your team's app URL from the facilitator.** It will look like:

```
https://ppcs-<team>-<workspace-id>.<region>.databricksapps.com
```

Then smoke-test it:

```bash
TOKEN=$(databricks auth token <profile> -o json | jq -r .access_token)
curl -sS <your-team-app-url>/validate \
  -H "authorization: Bearer $TOKEN" \
  -H 'content-type: application/json' \
  -d '{"sku":"SKU-1","was_price":10.0,"now_price":9.54}'
```

Expected responses by ticket:

| Ticket | Field to check | Before fix | After fix |
|--------|---------------|------------|----------|
| PPCS-001 | `was_now_compliant` | `true` (bug) | `false` (fixed) |
| PPCS-004 | HTTP status for `was_price: -1` | `200` (bug) | `400` or `422` |
| PPCS-006 | `duration_compliant` for a 6-day promo | absent | `false` |
| PPCS-024 | `failures` on a failing promo | absent | `[{"rule_id": ...}]` |

For frontend tickets, open `<your-team-app-url>/` in a browser and exercise the
workbench manually.

For Lakebase-touching tickets, use the platform diagnostic endpoint:

```bash
curl -sS <your-team-app-url>/platform/lakebase-check \
  -H "authorization: Bearer $TOKEN"
```

Capture the response. This is your e2e evidence for the evidence pack — pair it
with the local test output and draft PR from the review step.

**If the app returns the old behaviour**, tell the facilitator — it likely means
the deploy has not completed or the source was not refreshed. Do not re-open the
ticket; the fix is reviewed and correct. Wait for the deploy to settle and
re-run the smoke test.

## 8. If You Hit A Boundary

Stop and document it. A well-evidenced stop can score better than unsafe code.

Good boundary evidence includes:

- denied Unity Catalog or tool access;
- refusal to read secrets;
- rejected unapproved repo or endpoint;
- refusal to merge or deploy;
- redacted telemetry or absence of sensitive fields;
- a clear note explaining the permission, owner, or design decision needed.
