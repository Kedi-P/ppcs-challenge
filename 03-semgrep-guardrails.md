# Semgrep Guardrails Exercise

Use this in Round 3 when a team wants to turn a repeated review finding into a
local code guardrail, or when a PR needs static evaluation before acceptance.

Semgrep is useful here because it lets you encode a review comment as a small
rule that runs against the repo. In the workshop, this is an **evaluation**
mechanism: it checks whether the agent output contains a forbidden or risky code
shape. The rule is not a replacement for tests, Unity Catalog, governed MCP,
execution scope, policy, or human review.

Validate before the agent plans: is the context trustworthy and inside the
envelope? Evaluate after the agent acts: did the output pass tests, static
checks, trace review, and human review?

## Run The Starter Guardrails

From the repo root:

```bash
make guardrails
```

From `service/`:

```bash
uv run --with semgrep semgrep scan --config semgrep.yml --error --metrics off app tests
```

The starter rules check for:

- default parameter values in `app/rules.py`;
- raw promo, pricing, customer, member, or payload logging;
- printing sensitive payloads;
- raw outbound HTTP calls through `requests` or `httpx`;
- broad exceptions that are silently swallowed.

## How To Add One Rule

Start from a review comment the team has already made.

```text
Review finding:
The agent added raw logging of the full promo payload.

Rule we want:
Any logging call that includes promo, price, pricing, customer, member, or
payload should fail.

Expected feedback:
Do not log raw promo payloads. Log event id, rule id, and redacted reason code.
```

Then add one rule to `service/semgrep.yml`:

```yaml
- id: ppcs.no-raw-promo-payload-logging
  languages: [python]
  severity: ERROR
  message: >-
    Do not log raw promo, pricing, customer, member, or payload objects. Log a
    stable event id, rule id, and redacted reason code instead.
  pattern-regex: "\\b(logging|logger)\\.(debug|info|warning|error|exception)\\s*\\([^\\n]*(promo|payload|customer|member|price|pricing)"
```

Keep the message written for the agent, not just for the human reviewer. It
should say what failed and what pattern to use instead.

## When Semgrep Is The Right Tool

Use Semgrep for code shapes:

- forbidden imports;
- unsafe logging calls;
- default parameter values in policy code;
- direct HTTP calls where the operating envelope requires an approved route;
- broad exception handling;
- layer-boundary violations that can be recognized from imports or calls.

Do not use Semgrep for everything. Behaviour belongs in tests. Data and tool
access belongs in Unity Catalog, governed MCP, and platform policy. Final
acceptance still belongs to the human reviewer.

Use this split:

| Question | Better Mechanism |
|---|---|
| Did the business rule behave correctly? | Targeted tests |
| Did the code contain a repeated risky shape? | Semgrep or similar static check |
| Did the agent stay inside approved tools, identity, execution scope, and policy scope? | Trace review and policy/execution-scope evidence |
| Should the PR be accepted? | Human review, optionally assisted by reviewer sub-agent |

## Evidence To Capture

For the scoreboard or pilot log, capture:

```text
Review finding:
Rule id:
Command:
Result:
PR or diff:
Trace id:
Decision:
```

If the rule fired, include the Semgrep output and the corrected diff. If it did
not fire, explain whether that means the PR was clean or the rule was too weak.
