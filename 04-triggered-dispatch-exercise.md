# Triggered And Parallel Dispatch Exercise

Use this in Round 3. The goal is to practise moving from one-off manual prompting to a governed dispatch loop without letting the agent merge, deploy, or broaden access.

## Outcome

By the end of the exercise, your team should have evidence for one of:

- A scheduled dispatch design.
- A repo-event dispatch design.
- A webhook dispatch design.
- A heartbeat monitor design that watches evolving state and stages a draft
  response for review.
- A CI/build-validation follow-up design that turns failed checks into a scoped
  draft fix without granting merge or deploy authority.
- A parallel/background dispatch plan for two low-blast-radius tickets.

You do not need to automate the whole system during the workshop. You do need to prove that the trigger, context, review step, and stop conditions are explicit.

## Choose A Trigger

Pick one.

| Trigger | Good For | Minimum Proof |
|---|---|---|
| Manual dispatch | First run, high uncertainty, new ticket type | Brief, trace, draft PR, review decision |
| Scheduled dispatch | Routine checks, dependency updates, report generation | Schedule config or design, trace field, owner |
| Repo event | New issue, label, PR update, failed CI | Event source, issue/PR link, scoped action |
| Webhook | External intake from approved system | Approved source, payload contract, auth boundary |
| Heartbeat | Watching evolving state such as PR comments or failed checks inside the same governed thread | Poll interval, watched state, staged draft response, human review point |

Do not choose a trigger that requires secrets, unapproved egress, autonomous deploy, autonomous merge, or broad production data access. A heartbeat may stage a draft response; it may not push, merge, deploy, or approve itself.

A failed CI or build-validation event may trigger analysis, a review comment, or
a draft PR update. It must not trigger autonomous merge, deploy, approval,
branch-policy changes, or release-control changes.

## Candidate Tickets

Good Round 3 candidates:

- `PPCS-020` — nightly violations trend report.
- `PPCS-033` — reviewer config or skill.
- `PPCS-034` — trace metadata for dispatches.
- `PPCS-036` — context budget checklist.

Avoid using higher-risk tickets for parallel dispatch unless a facilitator approves the boundary.

## Trigger Brief

```text
Trigger:
<manual | scheduled | repo event | webhook | heartbeat>

Trigger source:
<who/what starts the dispatch>

Ticket:
PPCS-___

Context:
- Approved repo/path:
- Relevant files:
- Approved data/tool scope:
- Explicitly out of scope:

Steerability:
- Reviewer sub-agent:
- Tests/checks:
- Trace fields required:
- Stop conditions:

Delivery boundary:
Draft PR only. No merge, deploy, secrets, ungranted data, unapproved repos, or unapproved egress.
```

## Parallel Dispatch Plan

Use this only for low-blast-radius work. Parallelism is not a bravery contest.

| Dispatch | Ticket | Isolated Checkout / Worktree | Files Allowed | Reviewer | Stop Condition | Evidence |
|---|---|---|---|---|---|---|
| A |  |  |  |  |  |  |
| B |  |  |  |  |  |  |

Rules:

- Use a separate branch plus an isolated checkout, worktree, or agent workspace
  for each parallel dispatch. Do not run two agents against the same dirty
  working tree.
- Dispatches must not edit the same file unless the facilitator approves it.
- Each dispatch needs its own branch or PR-equivalent artifact.
- Each dispatch needs its own trace or trace marker.
- A human decides whether either output is accepted.
- If the two branches conflict, stop and review. Do not ask an agent to
  auto-resolve a broad conflict or silently combine changes from two worktrees.

## Trace Fields To Capture

Ask the agent or harness to expose:

- `ticket_id`
- `brief_id`
- `trigger_type`
- `trigger_source`
- `agent`
- `model`
- `approved_repo`
- `reviewer_subagent`
- `draft_pr`
- `tests_run`
- `guardrail_events`
- `estimated_cost`

These fields feed `04-harness-analytics-worksheet.md`.

## Review Questions

Before claiming points:

- Did the trigger fire from an approved source?
- Did the agent stay inside the intended files, repo, tools, and data?
- Did the run stop at draft PR?
- If the trigger was failed CI/build validation, did the agent fix the PR rather
  than weaken the gate?
- Is the trace good enough for another engineer to understand the run?
- Were parallel dispatches isolated by branch and checkout/worktree/workspace?
- Did parallelism reduce elapsed time without increasing review risk?
- What would have to be true before this moved from in-loop review to on-loop sampling?

## Submission

Paste links or notes into the scoreboard:

```text
Team:
Trigger type:
Ticket(s):
Branch / draft PR:
Trace:
Review decision:
Harness change:
Why this is safe to repeat:
```
