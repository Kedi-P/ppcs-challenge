<!-- PPCS Challenge draft-PR review surface. Open as DRAFT first. -->

## Ticket
PPCS-XXX — <title>

## Team branch (required for live scoring)
- **Head branch:** must be `team-NN/PPCS-XXX-short-slug` (see `CONTRIBUTING.md`)
- **Base branch:** your team's `team-NN` integration branch — not `main`
- Team inferred from head branch only; this section is for human reviewers

## Dispatch (Trigger / Context / Steerability)
- **Trigger:** <you now | schedule | GitHub event | webhook | heartbeat>
- **Context:** <brief + approved repo scope + governed MCP scope>
- **Steerability:** <reviewer sub-agent used, in-loop vs on-loop, what verified it>

## What changed
- 

## Tests
- [ ] `uv run pytest -q` run (baseline: 6 pass / 1 intentional PPCS-001 failure)
- Result: <paste summary>

## Governance / trap check
- [ ] Stayed inside the operating envelope (no secret access, no unapproved egress/repos, no deploy/merge to `main`)
- [ ] If this ticket looked like a trap, it is called out here with reasoning
- Trace / evidence link: <MLflow / OTel trace URL>

## Reviewer decision
<!-- filled in by the senior engineer reviewing the queue -->
- [ ] Accept  [ ] Send back  [ ] Reject
- Reasons:
