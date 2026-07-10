# Harness Improvement Log

Use this when a team turns a repeated agent failure into a durable harness
change. The point is to leave the workshop with reusable operating knowledge,
not just one-off prompts.

## Entry Template

```text
Team:
Date/time:
Ticket or run:
Trace or PR:

Failure or friction observed:

Evidence:

Chosen mechanism:
brief line | agent spec | agent-session/platform policy | execution scope | skill | reviewer config | hook | governed MCP/UC policy | test/check | sub-agent | other

Compatibility mechanism set:
brief line | skill | reviewer config | hook | governed MCP/UC policy | test/check | sub-agent

Why this mechanism:

Validation:
smoke use | syntax/format check | reviewed application against one PR | platform denial | trace comparison

Expected effect:

Owner for pilot:

When to revisit or remove:
```

## Mechanism Guide

| Symptom | Prefer | Why |
|---|---|---|
| One ticket was ambiguous | Brief line | Cheap and local to the dispatch. |
| The same role/model/tool setup is needed again | Agent spec | Makes harness, model, tool, policy, and sub-agent choices explicit and reviewable. |
| Same reviewer comment repeats | Reviewer config or skill | Makes the critique reusable. |
| Same unsafe pattern appears in generated code | Hook or lightweight check | Fires only when the pattern appears. |
| Same code shape keeps appearing in PRs | Semgrep rule | Turns the review comment into local, repeatable feedback. |
| The agent should pause or stop on a risky action | Agent-session/platform policy | Produces ALLOW, ASK, or DENY evidence close to the tool call. |
| The agent needs too much filesystem, network, or env access | Execution scope | Keeps execution contained without relying on advice in the prompt. |
| A policy breach would be dangerous if overridden | Governed MCP, Unity Catalog, or platform policy | Containment needs a hard block, not advice. |
| Noisy research pollutes the main run | Sub-agent | Summary returns; noisy context stays out of the main loop. |
| Tests miss the real acceptance criteria | Test/check | Makes correctness verifiable before review. |

Hooks and reviewer configs are quality controls. Agent specs make the harness
repeatable. Agent-session/platform policies and execution scope are containment
controls. They do not replace the
operating envelope for secrets, ungranted data, raw egress, merge, deploy, or
identity switching.

## End-Of-Day Summary

```text
Most useful harness change:

Most expensive failure we prevented:

Change we would carry into the 60-day pilot:

Change we would not carry forward yet:

Evidence link:
```
