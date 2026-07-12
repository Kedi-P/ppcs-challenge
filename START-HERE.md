# Start Here — CoDA Engineering Challenge

You are on a team of 2-3, running a governed coding-agent delivery loop for the
**Promotional Pricing Compliance Service (PPCS)**. This page orients you in two
minutes; open the linked files as you need them.

## What you are doing

You inherit PPCS — a pricing-compliance service (FastAPI backend + browser
workbench) running on Databricks Apps, Lakebase, and Unity Catalog. You do not
type most of the code. You **write briefs, dispatch a coding agent, review its
draft PRs and traces, prove the guardrails hold, and measure the harness.**

You and your agents work in **one repo: `dgokeeffe/ppcs-challenge`** — it holds
the PPCS service (`service/`), the ticket backlog (`tickets/`), and your team
branch (`team-01`…`team-10`). That is the only "approved repo"; reaching for any
other repo is outside the envelope.

The day is three scored rounds:

1. **Dispatch & Review** — clear backlog tickets by dispatching agents and
   reviewing the queue.
2. **Govern & Prove** — prove the operating envelope holds; catch the tickets
   engineered to bait an agent past it.
3. **Scale, Sustain & Measure** — drive load at your app, watch your Lakebase
   compute autoscale and survive scale-to-zero, and improve the harness.

Catching an unsafe path is worth more than shipping a feature. The score is
**governed, reviewable value with evidence** — not code volume.

## Visual map

![Governed developer workflow — agent, evidence packet, draft PR, human release](assets/ppcs-developer-workflow-release.png)

The agent works inside the harness; **you** own merge, deploy, and acceptance.
Diagrams for each round live in `assets/` and in the linked guides below.

## The files you open, in order

| When | Open |
|---|---|
| PPCS system you are changing | `01-base-app-architecture.md` + `assets/ppcs-solution-architecture.png` |
| First, to understand your role and the loop | `00-participant-guide.md` |
| Before Round 1, the endorsed ticket process | `00-ways-of-working.md` (build to spec → goal → validate/evaluate) |
| Before every dispatch, kept open | `00-operating-envelope-card.md` (what agents may / may not do) |
| To pick work | `tickets/` (the PPCS backlog) and `ref-scoreboard.md` |
| To shape a dispatch | `02-brief-template.md` |
| To review what came back | `02-reviewer-subagent-template.md`, `02-trace-review-worksheet.md` |
| To run against the service | `service/` (the PPCS app + tests) |
| When a ticket touches state | `LAKEBASE.md`, `01-base-app-architecture.md` |
| When setup misbehaves | `01-day-of-quickstart.md`, `01-repo-access-self-test.md` |
| To submit evidence | `ref-evidence-submission-template.md` |

If you read nothing else first, read `00-participant-guide.md` and
`00-ways-of-working.md`.

## Ground rules

- Agents branch, edit, test, and open **draft** PRs — they never merge or
  deploy. A human stays on the loop.
- If a ticket seems to need something outside the envelope (a secret, an
  ungranted table, an unapproved repo), **stop and say why.** That is the win.
- Keep briefs lean and reset context between unrelated tickets — efficiency
  breaks ties on the scoreboard.
