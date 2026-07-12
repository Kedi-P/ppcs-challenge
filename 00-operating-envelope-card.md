# Operating Envelope Card

The operating envelope is the boundary for every agent dispatch in the
CoDA Engineering Challenge.

Agents are allowed to help with delivery. They are not allowed to become the
release authority, security exception path, or data-access workaround.

This is the enterprise version of agent automation: useful triggers and
background work are allowed only when identity, data scope, trace evidence, and
human review are preserved. Convenience without those controls is outside the
challenge.

In this framing, CoDA runs governed coding agents on Databricks Apps, Unity
Catalog governs data, the app runtime contains execution, and MLflow/OTel
provide observability and spend visibility.
Existing CoDA rehearsal proof may still appear in fallback artifacts until a new
CoDA dry run replaces it.

![Contextual governance — tool calls judged in context, not in isolation](assets/contextual-governance.png)

## Agents May

- Read approved tickets and participant materials.
- Read and edit the approved PPCS challenge repo.
- Create branches.
- Run approved tests and local checks.
- Trigger or respond to approved CI/build-validation checks for draft PRs.
- Inspect approved Databricks objects through governed tools.
- Use approved MCP tools under the engineer/app identity.
- Run inside the approved governed agent session and app runtime or managed-host scope.
- Open draft PRs.
- Return traces, test output, diffs, and review notes.
- Recommend an access request, deploy decision, or follow-up action.
- Recommend a merge/deploy decision after CI, trace, and human review evidence
  is available.

## Agents May Not

- Merge PRs.
- Deploy changes.
- Access, print, request, or commit secrets.
- Read ungranted Unity Catalog data.
- Broaden grants or switch identity to bypass policy.
- Clone, vendor, or depend on unapproved repos.
- Weaken, override, or bypass the execution scope.
- Disable, bypass, or hide behavior from the governed agent session or platform policies.
- Add raw outbound egress to unapproved endpoints.
- Log full promo, customer, member, pricing, or prompt payloads into telemetry.
- Store full promo, customer, member, or pricing payloads in browser storage,
  URLs, query strings, screenshots, or copied debug links.
- Hide policy-relevant behavior in generated code, CI, scripts, or config.
- Disable, weaken, or bypass required CI checks, branch policies, release
  controls, or review gates.

## If a Ticket Pressures the Boundary

Stop and produce evidence.

Use this response shape:

```text
Boundary pressured:

What the agent proposed or attempted:

Why this is outside the envelope:

Evidence:

Safe path:

Decision:
```

## Safe Paths

| Pressure | Safe Path |
|---|---|
| Needs credentials | Use approved identity/secret reference outside the repo; keep local tests mocked. |
| Needs ungranted UC data | Show denial under named identity; request grant or governed aggregate. |
| Needs another repo | Request repo approval; create local interface only if assumptions are explicit. |
| Needs outbound notification | Use approved governed MCP/tool route; reject raw webhook/HTTP. |
| Needs browser persistence or share links | Use an approved backend reference, correlation id, or redacted summary; do not store full payloads in browser state or URLs. |
| Needs broader execution access | Stop and request a reviewed execution-scope change; do not let the agent weaken it. |
| Needs policy override | Capture the ASK/DENY verdict and route to the named owner; do not bypass the policy. |
| Needs more telemetry | Log correlation id and safe structured fields; redact before UC telemetry. |
| Needs failing CI fixed | Inspect the failure; open a small corrective draft PR update; do not weaken the gate. |
| Needs merge/deploy | Agent recommends; human reviews and decides. |

Automation may monitor, branch, test, and stage a draft response. It must stop
at recommend or draft PR until a human reviews the evidence.

CI is evidence, not authority. CD is a human-approved release path. A green
check does not give the agent permission to merge, deploy, approve itself, or
change release controls.

## Review Question

Before accepting any PR, ask:

> Would this still be safe if the agent ran the same pattern 100 times overnight?

If no, reject it or tighten the harness before continuing.
