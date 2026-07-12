# Ways Of Working — Loop Development

Keep this card open for the first lab block. The day follows one teaching
shape: **theory → demo → challenge**. This card is the theory you practice in
Round 1.

## Core thesis

> We do not vibe features into the backlog.
> We **build to a spec**, **orient to a goal**, then **validate and evaluate**
> before we accept a draft PR.

The SDLC phases did not disappear. Implementation got faster; judgment did not.
The hard work moved earlier — into specification quality, goal clarity, context
validation, and post-run evaluation.

```text
build to spec  →  build to a goal  →  validate (before)  →  evaluate (after)
```

## Theory: same SDLC, new control points

| SDLC phase | Agentic bottleneck | What you do in this lab |
|---|---|---|
| Requirements | Spec precise enough to test | Turn ticket acceptance into executable feedback |
| Design | Fast implementation amplifies bad boundaries | Name goal, envelope, and stop conditions |
| Implementation | Scoped dispatch | One reviewable change; draft PR only |
| Testing | Behavior plus run quality | Tests, Semgrep/static checks, CI |
| Review | Summary is not evidence | Diff + trace + human decision |
| Release | Green gate is not approval | Human-owned merge and deploy |
| Maintenance | Repeated failures return | Codify into skills, hooks, tests, policies |

### Build to spec

A specification is shared intent. It is not enough on its own — if it leaves
room for interpretation, the agent will fill the gap.

Before dispatch, decide which parts of the ticket need **executable feedback**:

- business behaviour → tests
- unsafe patterns → Semgrep / hooks / reviewer config
- data and tool boundaries → UC, governed MCP, operating envelope
- repeated review comments → durable harness changes

Test: if you would reject a PR for violating the rule, decide where that rule
lives **before** the next dispatch.

### Build to a goal

For anything beyond a one-line fix, write a short **goal anchor** in the brief:

- persistent objective
- acceptance criteria
- evidence required
- stop conditions
- human decision point

The goal keeps the agent oriented as context grows. It does **not** widen
autonomy. The agent still opens a draft PR only.

### Validate versus evaluate

Do not conflate these.

| | When | Question | Examples |
|---|---|---|---|
| **Validate** | Before the plan | Is the context safe to reason from? | Current files? Stale memory? Inside envelope? Assumptions explicit? |
| **Evaluate** | After the run | Did the output and trajectory meet the bar? | Tests pass? Trace clean? Reviewer would approve? |

Use **R.V.P.I.** inside every loop:

| Step | Question | Artifact |
|---|---|---|
| Research | What context is relevant? | Candidate files, docs, traces |
| Validate | Is it current, consistent, and in scope? | Validated assumptions / conflicts |
| Plan | What small path should we take? | Files, tests, evidence, stops |
| Implement | Did the agent execute and verify one step? | Branch, tests, trace, draft PR |

Let the platform absorb mechanical validation (UC denials, bundle validate,
minted credentials). Spend human V-budget on semantic intent: is the rule
right, is the test expressing acceptance, is the PR maintainable?

## Demo: what the facilitator shows once

On `PPCS-001`, you will see the ladder live:

1. **Spec** — ticket acceptance: 4.6% must fail; ≥5% must pass; `pytest` green.
2. **Goal** — one scoped fix in `discount_pct`; draft PR only; no merge/deploy.
3. **Validate** — approved repo `dgokeeffe/ppcs-challenge`, right files, envelope.
4. **Implement** — agent branches, edits, tests, opens draft PR.
5. **Evaluate** — diff, tests, CI, trace, human accept/reject.
6. **Govern** — one boundary stop under named identity (optional in the demo).

The unit of value is a **reviewable governed change**, not a green chat.

## Challenge: Round 1 practice

Repeat the same ladder on your first ticket:

```text
ticket → spec + goal briefly → R.V.P.I. → draft PR → evidence packet → decision
```

| Step | You do | Agent does | Proof |
|---|---|---|---|
| Spec | Name acceptance + executable checks | — | Brief lists tests / stop rules |
| Goal | Write goal anchor if multi-criteria | — | Objective + evidence + human decision |
| Research / Validate | Approve context and envelope | Inspect only approved files/tools | Conflicts surfaced before plan |
| Plan | Clarify or state assumptions | Propose a small plan | Files, tests, stops named |
| Implement | Dispatch one scoped change | Branch, edit, test | Diff + pytest |
| Evaluate / Review | Accept, send back, or reject | Open draft PR + return trace | PR URL, CI, trace, reasons |
| Codify | Log the harness lesson | — | Skill / brief / reviewer note |

### Brief shape

Use `02-brief-template.md`. Every Round 1 brief answers:

- **Trigger** — usually "manual dispatch now"
- **Context** — approved repo, files, tests, out of scope
- **Steerability** — draft PR only; return diff, pytest, trace id; stop on
  secrets / ungranted data / merge-deploy

Add a goal anchor when the ticket is multi-criteria or likely to run long.

### Evidence packet (what "done" means)

1. Spec / acceptance mapped to checks
2. Goal (or explicit one-liner objective)
3. Scoped brief
4. Diff limited to the ticket
5. Targeted test output
6. Draft PR (not merged)
7. Trace or equivalent run evidence
8. Human review decision with reasons

## Where durable truth lives (supporting)

Placement is not the thesis — it is part of Context when the ticket needs it.

| If the ticket needs… | Put it here |
|---|---|
| Rule math, API, UI, tests | Application code in `service/` |
| Thresholds, price history, verdicts, identity proof | Team Lakebase schema |
| Events / denied production-like reads | Unity Catalog under grant |
| What the agent did / cost / tools | MLflow / OTel trace |

```text
memory  →  reason
trace   →  evidence
Lakebase → truth now
```

A trace is not an operational database. Prompt memory is not durable state.
See `LAKEBASE.md` when a ticket actually touches state (e.g. PPCS-055 / 056).

## What not to endorse

- Vibing a feature from an underspecified prompt
- Skipping Validate because the research "looked fine"
- Treating Evaluate as "tests passed, ship it"
- Confusing a long chat for a goal
- Merging or deploying because the demo deadline is near

Theory on this card. Demo on `PPCS-001`. Challenge is your first scored loop.
