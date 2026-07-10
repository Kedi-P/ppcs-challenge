# Databricks And Agent Access Self-Test

Run this before the workshop if the facilitator asks you to confirm Databricks
workspace, App, trace, and coding-agent access.

Use the links and profile names supplied by the facilitator. Do not paste tokens,
secrets, connection strings, or screenshots containing credentials into the
evidence note.

## Prerequisites

- You can sign in to the nominated Databricks workspace.
- You have the Databricks CLI installed if the facilitator asks for CLI proof.
- You have access to the nominated coding-agent tool.
- You have the workshop repo or participant bundle.

## 1. Workspace Access

Browser proof:

```text
Workspace URL:
Signed-in identity:
Screenshot or note:
```

Optional CLI proof:

```bash
databricks current-user me -p <profile> -o json
```

Pass criteria:

- The identity is your workshop identity.
- You can reach the workspace without requesting extra permission on the day.

## 2. App Access

Open the PPCS App URL supplied by the facilitator.

If CLI proof is requested:

```bash
TOKEN=$(databricks auth token <profile> -o json | jq -r .access_token)
curl -sS <ppcs-app-url>/validate \
  -H "authorization: Bearer $TOKEN" \
  -H "content-type: application/json" \
  -d '{"sku":"SKU-1","was_price":10.0,"now_price":9.54}'
```

Pass criteria:

- The App responds.
- Before `PPCS-001` is fixed, the response should show the seeded Was/Now bug:

```json
{"sku":"SKU-1","discount_pct":5,"was_now_compliant":true}
```

## 3. Lakebase State

If the facilitator asks for App-mediated Lakebase proof, open or call the
Lakebase proof endpoint supplied by the facilitator.

Default live route, if enabled:

```text
<ppcs-app-url>/platform/lakebase-check
```

Record:

```text
Access mode:
Proof endpoint or query:
Identity model:
Result summary:
```

Pass criteria:

- The result proves state read/write, not only App reachability.
- The proof uses the approved App-mediated path or an explicitly approved
  direct Lakebase path.
- No credentials, connection strings, or tokens are included in the evidence.

## 4. Trace Access

Open the MLflow or trace view supplied by the facilitator.

Record:

```text
Trace or run id:
Ticket id visible:
Draft PR URL visible:
Tool calls visible:
Test output visible:
Cost or token signal visible:
```

Pass criteria:

- You can find at least one dispatch trace or run.
- The trace links ticket, brief, PR or diff, tests, and cost/usage evidence.

If participants will not have direct trace access, the facilitator must confirm
that trace review will be projected or mediated during the workshop.

## 5. Unity Catalog Boundary

If the facilitator asks for live governance proof, run or observe the
allowed/denied Unity Catalog check under your workshop identity.

Record:

```text
UC identity:
Allowed object:
Allowed result:
Denied object:
Denied error class:
```

Pass criteria:

- The allowed object succeeds under your identity.
- The denied object fails with an authorization denial such as
  `INSUFFICIENT_PERMISSIONS`.
- The denied result is not object-not-found.
- You do not broaden grants, switch identity, or copy restricted data to make
  the check pass.

## 6. Coding-Agent Access

Run a harmless read-only command in the nominated agent tool.

Suggested prompt:

```text
Read the participant guide and summarize the operating envelope in five bullets.
Do not edit files. Do not run tests. Do not access Databricks.
```

Pass criteria:

- The agent starts successfully.
- It can read the approved participant materials.
- It does not request broader repo, data, or secret access for this read-only task.

## 7. Governed Tool Access

If the workshop uses governed MCP or equivalent tools, ask the agent to run the
approved read-only tool named by the facilitator.

Record:

```text
Tool name:
Identity:
Approved action result:
Denied/refused action result, if tested:
Trace/log link:
```

Pass criteria:

- Approved read-only tool call succeeds.
- Any denied/refused action is denied by tool policy, permission, or review path,
  not merely because of a typo or missing object.

## Evidence To Send Back

Fill one complete `attendee-access-evidence-template.json` file that includes:

- the `repo` section from `01-repo-access-self-test.md`;
- the `databricks` section from this self-test, including `lakebase_state` and
  `uc_boundary`; and
- the `agent` section from this self-test.

The evidence file must use an ISO-8601 timestamp, `https` URLs for the
workspace and App, and one of these `trace_access_mode` values:

- `direct`
- `facilitated`
- `facilitator identity`
- `projected`
- `screen share`

Leave `blockers` empty only when every required check has passed. If any blocker
remains, send the file as a diagnostic note, not as pass evidence.

Send that single completed JSON file to the facilitator. It must pass:

```text
Facilitator evidence checker: attendee access evidence is structurally complete.
```

If you cannot use the JSON template, send:

```text
Participant:
Workspace identity:
Repo self-test PR:
App response:
Lakebase state result:
Trace/run id:
UC allowed/denied result:
Agent tool:
Governed tool result:
Any blocker:
```

If any item fails, send the exact error and stop. Do not try to work around
workspace, data, secret, or tool permissions.
