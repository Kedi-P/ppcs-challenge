# Harness Analytics Worksheet

Use this in Round 3 to compare agent loops. The point is not to crown a model. The point is to find which **harness** produced reviewable, governed work with the least rework.

## 1. Pick Two Runs

Choose two dispatches to compare. They can be:

- Two teams on similar tickets.
- One team's first attempt and second attempt.
- A manual dispatch versus a scheduled, event-triggered, webhook, or heartbeat
  dispatch.
- A run with a reviewer sub-agent versus one without.
- A cheap research/log-review model versus a stronger implementation or review
  model.
- A persistent reviewer or QA/explorer config versus an ad hoc reviewer prompt.
- A repeated failure codified as a brief line, skill, hook, governed MCP/UC
  policy, or sub-agent.
- A repeated code-shape finding evaluated with Semgrep versus only human review.
- A release-readiness packet versus a PR with only local test output.
- A rewritten context pack versus the original broad prompt.
- A golden regression eval set versus ad hoc review.
- A supply-chain-reviewed customization versus an unreviewed plugin, skill,
  hook, MCP server, or reviewer config.

| Field | Run A | Run B |
|---|---|---|
| Ticket id |  |  |
| Trigger | Manual / scheduled / repo event / webhook / heartbeat | Manual / scheduled / repo event / webhook / heartbeat |
| Agent and model |  |  |
| Reasoning depth / effort setting | Low / medium / high / default | Low / medium / high / default |
| Reviewer sub-agent used? | Yes / no | Yes / no |
| Explicit reviewer config or critique lens? |  |  |
| Persistent sub-agent/model config? |  |  |
| Codified lesson mechanism | Brief / skill / hook / MCP-UC policy / sub-agent / none | Brief / skill / hook / MCP-UC policy / sub-agent / none |
| Evaluation mechanism | Tests / Semgrep / trace review / reviewer rubric | Tests / Semgrep / trace review / reviewer rubric |
| Eval dataset or golden cases |  |  |
| Customization reviewed? | Yes / no / not applicable | Yes / no / not applicable |
| Brief link or summary |  |  |
| Draft PR or diff link |  |  |
| Trace link or artifact |  |  |

## 2. Score The Outcome

Use evidence, not the agent summary.

| Metric | Run A | Run B | Evidence |
|---|---:|---:|---|
| Draft PR opened? |  |  | PR/diff link |
| Tests passed? |  |  | Test output |
| Semgrep/static check passed? |  |  | `make guardrails` output or equivalent |
| Accepted by human reviewer? |  |  | Review decision |
| Sent back for rework? |  |  | Review comments |
| Rejected as unsafe or out of scope? |  |  | Review comments / guardrail proof |
| Post-review defect found? |  |  | Reviewer note / failing test |
| Guardrail event observed? |  |  | Trace / platform denial |

## 3. Read The Trace

Fill only what you can prove from a trace, log, or provided evidence artifact.

| Trace Signal | Run A | Run B | Why It Matters |
|---|---:|---:|---|
| Tool calls |  |  | More tool calls may mean useful research or aimless wandering. |
| Files touched |  |  | Large blast radius increases review cost. |
| Tests run |  |  | Tests show what the agent tried to prove. |
| Static checks run |  |  | Semgrep or similar checks show repeated code-shape risks were evaluated. |
| Blocked actions |  |  | Guardrails are working only if they are visible. |
| Input tokens |  |  | Large context raises cost and failure surface. |
| Output tokens |  |  | Long output is not automatically useful output. |
| Cache-read tokens |  |  | Caching helps repeated context, but still signals context size. |
| Estimated cost |  |  | Compare cost against accepted value, not in isolation. |
| Human review time |  |  | The harness is expensive if humans must untangle messy output. |

## 4. Calculate Harness Ratios

Approximate is fine. Make assumptions visible.

| Ratio | Formula | Run A | Run B |
|---|---|---:|---:|
| Accepted PR rate | accepted PRs / dispatches |  |  |
| Defect-free accepted PR rate | accepted PRs with no post-review defect / dispatches |  |  |
| Escaped defect rate | post-review defects / accepted PRs |  |  |
| Rework rate | send-backs / dispatches |  |  |
| Guardrail hit rate | guardrail events / dispatches |  |  |
| Review cost | human review minutes / accepted PR |  |  |
| Token cost per accepted PR | estimated cost / accepted PRs |  |  |
| Cost per defect-free accepted PR | estimated cost / defect-free accepted PRs |  |  |
| Human minutes saved after rework | baseline minutes - current minutes, after send-backs |  |  |
| Context bloat signal | input + cache-read tokens |  |  |

If a run has zero accepted PRs, do not hide it behind a divide-by-zero problem. Write "no accepted value yet" and explain what the team learned.

## 5. Diagnose The Loop

Pick the most likely cause of waste or risk.

| Symptom | Likely Loop Problem | Next Change |
|---|---|---|
| Large diff with unrelated edits | Brief too broad or context too loose | Narrow files, acceptance criteria, and out-of-scope list |
| Tests pass but reviewer rejects | Tests do not cover the real acceptance criteria | Add targeted failing test before dispatch |
| Same unsafe code shape repeats | Evaluation missing a local static check | Add or tighten a Semgrep rule with an agent-readable message |
| Agent asks for secrets or broad data | Operating envelope not explicit enough | Add denied actions and approved data scope to brief |
| Many turns, little progress | Context bloat or unclear stop condition | Start fresh with smaller ticket and done criteria |
| Same review comment repeats | Lesson not codified | Create or update reviewer config / skill / standing instruction |
| Quality warning needs to fire only on a pattern | Wrong mechanism chosen for a repeatable nudge | Add a post-tool-use hook or lightweight check that fires only when the pattern appears |
| Policy violation would be dangerous if overridden | Nudge used where a hard block is needed | Move the boundary to governed MCP, Unity Catalog, or platform policy |
| Trace lacks useful evidence | Observability fields missing | Add ticket id, brief id, PR URL, test output, and guardrail fields |
| Strong model used for narrow log review | Tool/model choice not matched to task | Route narrow research to a cheaper adequate model and reserve stronger models for implementation or review |
| High reasoning used for deterministic lookup | Reasoning depth not matched to step | Use lower reasoning for simple reads/tool calls and reserve higher reasoning for planning, risk, or architecture review |
| Reviewer sub-agent gives generic praise | Reviewer config too vague | Give the reviewer explicit acceptance criteria, trap risks, and operating-envelope checks |
| New eval passes but old failure returns | No golden regression case | Add the old failure to a small replayable eval set |
| Custom skill, hook, plugin, or MCP server behaves surprisingly | Customization provenance and scope unclear | Review source, owner, version, allowed actions, and deny behavior before reuse |

Example harness change:

```text
Pin a cheap adequate model to a QA/explorer reviewer config for log review and
browser checks. Keep the stronger model for implementation or final critique.
Measure whether accepted PR rate, review time, and token cost improve without
increasing missed defects or guardrail events.
```

## 6. Decide The Next Harness Change

Choose one change before the next dispatch.

| Change Type | What Will Change | Owner | How We Will Know It Worked |
|---|---|---|---|
| Brief |  |  |  |
| Context scope |  |  |  |
| Reviewer sub-agent |  |  |  |
| Test or check |  |  |  |
| Semgrep/static evaluation |  |  |  |
| Golden regression eval |  |  |  |
| Guardrail |  |  |  |
| Skill / hook / config / instruction |  |  |  |
| Customization supply-chain review |  |  |  |
| Trigger |  |  |  |

## 7. Eval Flywheel

Use this when a run exposes a failure that should not recur.

| Step | Evidence |
|---|---|
| Failure or missed risk found |  |
| Root cause in brief, context, tool scope, tests, or review |  |
| Harness change made |  |
| Golden regression case added |  |
| Before replay result |  |
| After replay result |  |
| Monitoring signal for the pilot |  |

Score the eval improvement only when the new check is replayable and catches
the old failure.

## 8. Customization Supply-Chain Review

Use this before reusing a custom skill, hook, plugin, MCP server, reviewer
config, policy, or agent spec.

| Mechanism | Owner | Source / Provenance | Scope | Benign Case Allowed? | Bad Case Blocked? | Eval Result | Pilot Reuse? |
|---|---|---|---|---|---|---|---|
|  |  |  |  | Yes / no | Yes / no |  | Yes / no |

## 9. Two-Minute Report

Use this structure for the final demo:

```text
We compared [Run A] and [Run B].

The better harness was [A/B] because [evidence].

The most important trace signal was [signal], which showed [finding].

The next change to the loop is [change].

We would not increase autonomy yet because [remaining risk], or we would move from in-loop to on-loop review for [narrow case] because [evidence].
```

Good Round 3 answers sound like engineering judgment, not agent enthusiasm.
