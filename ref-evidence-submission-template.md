# Evidence Submission Template

Use this for every scoreboard claim. One submission should support one claim:
a governed PR, guardrail proof, trap caught, trigger proof, harness insight, or
reusable skill/config.

## Claim

| Field | Value |
|---|---|
| Team |  |
| Round | 1 / 2 / 3 |
| Ticket id |  |
| Claim type | PR / guardrail / trap / trigger / harness / skill-config |
| Points claimed |  |
| Agent/tool |  |
| Named identity |  |

## Artifacts

| Artifact | Link Or Evidence |
|---|---|
| Brief used |  |
| Branch |  |
| Draft PR or diff |  |
| Test command and result |  |
| Trace link or trace id |  |
| Reviewer decision | accept / send back / reject / escalate |
| Worksheet used | trace review / guardrail proof / trigger exercise / harness analytics |

## Worksheet Mapping

Attach or reference the worksheet that matches the claim:

| Claim type | Required Evidence |
|---|---|
| PR | `02-trace-review-worksheet.md`, draft PR or diff, tests, reviewer decision |
| guardrail | `03-guardrail-proof-worksheet.md`, denied/refused action or redaction proof |
| trap | ticket id, unsafe path identified, rejection or redirect reason |
| trigger | `04-triggered-dispatch-exercise.md`, schedule/event/webhook/heartbeat proof, trace id |
| harness | `04-harness-analytics-worksheet.md`, trace comparison, cost/context signal |
| skill-config | `02-reviewer-subagent-template.md` adaptation, file link, or diff plus the repeated failure it addresses and a validation note: smoke use, syntax/format check, or reviewed application against one PR |

## Safety Check

Answer before asking for points.

| Question | Answer |
|---|---|
| Did the agent stay inside approved repo/tool/data scope? | Yes / no |
| Did the run stop at draft PR or reviewed artifact? | Yes / no |
| Were secrets, credentials, and sensitive payloads kept out? | Yes / no |
| Were unapproved egress, repos, data, merge, and deploy avoided? | Yes / no |
| Does the trace support the same story as the PR or decision? | Yes / no |

## Decision

```text
What we want scored:

Why this is safe to count:

What we rejected, sent back, or changed:

One loop improvement we will keep:
```

Do not submit a claim if the evidence is only "the agent said so." Use the
scoreboard evidence standard: link, trace id, command output, or reviewed
artifact.
