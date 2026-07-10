# Enterprise x Databricks CoDA Engineering Challenge Pre-Read

Read this before the workshop. It is intentionally short: the workshop is hands-on, and most of the learning comes from dispatching agents, reviewing their work, and proving where the operating envelope holds.

Workshop format: Monday 13 July 2026, 09:30-17:30, working in teams of 2-3.

## What You Are Walking Into

You will work in a small team as the senior engineer responsible for a seeded backlog on a **Promotional Pricing Compliance Service**.

The service validates promotions before they go live. The domain is realistic for pricing and ticketing compliance, but the repo is a workshop stand-in. You are not working on production customer code.

The point of the day is not "can an agent write code?" The point is:

- Can you write a brief that produces reviewable work?
- Can you catch plausible but unsafe agent output?
- Can you use platform controls to prove what an agent did and did not do?
- Can you turn repeated review lessons into a better loop?

## What To Bring

Bring a laptop and be ready to use:

- Git and branch-based review.
- A coding agent such as Codex, Claude Code, GitHub Copilot, OpenCode, or the provided workshop path.
- A browser for Databricks App, traces, PRs, and score evidence.

You do not need deep Databricks platform expertise. The Databricks concepts are taught through the engineering workflow.

## The Mental Model

The workshop uses **loop engineering**: design the repeatable loop around the agent, not just the prompt.

Every dispatch has three control points:

| Control | Question |
|---|---|
| Trigger | What starts the agent run: you, a schedule, a repo event, an approved webhook, or a heartbeat monitor? |
| Context | What repo, files, data, tools, and policy can the agent see? |
| Steerability | How is the work reviewed, measured, retried, or stopped? |

Good teams will not simply send bigger prompts. They will tighten the loop:
smaller tickets, clearer context, reviewer sub-agents, evidence-backed review,
explicit reject criteria, and durable harness changes.

## Operating Envelope

Agents may:

- Work only in approved workshop repos.
- Create branches and draft PRs.
- Run approved tests and inspect approved data.
- Use governed tools under a named identity.
- Produce evidence for review.

Agents may not:

- Merge or deploy autonomously.
- Read secrets or ungranted data.
- Pull in unapproved repos.
- Exfiltrate data to external endpoints.
- Log sensitive payloads into telemetry.
- Treat "the tests pass" as sufficient proof.

Some backlog items are intentionally shaped to test this boundary. Catching unsafe work is a successful engineering outcome.

## How To Prepare

Before the day:

1. Confirm you can access the workshop repo or participant bundle.
2. If asked, run `01-repo-access-self-test.md`.
3. If asked, run `01-databricks-agent-access-self-test.md`.
4. Confirm you can run the local service tests if instructed.
5. Skim `00-participant-guide.md`.
6. Skim `00-operating-envelope-card.md`.
7. Skim `ref-evidence-submission-template.md` so you know what a scoreboard claim needs.
8. Bring one example from your own work where an agent was useful, risky, or both.

## How You Will Be Assessed

Teams score through evidence, not volume:

- Reviewable draft PRs.
- Correct rejects with reasons.
- Guardrail proof.
- Clean traces.
- Cost-aware context choices.
- Useful loop improvements such as skills, hooks, reviewer configs, tests, or
  standing guardrails.

The strongest team is not the one with the most agent output. It is the one that can show which work is safe to accept, which work must be rejected, and how the platform proves the difference.
