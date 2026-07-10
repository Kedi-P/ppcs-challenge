# Contributing & Team Coordination — PPCS Challenge

This repo is the shared coordination space for all teams building against the
**Promotional Pricing Compliance Service (PPCS)** backlog during the CoDA
Engineering Challenge (Monday 13 July 2026). You dispatch CoDA agents against
this repo, review their draft PRs, and govern what is safe to accept.

Read `README.md` first for the challenge framing, then `START-HERE.md` and
`00-participant-guide.md` for how a team actually works a ticket.

## Teams

- ~10 teams of 2–3 engineers (`team-01` … `team-10`).
- Each team owns a long-lived branch named after it: `team-01`, `team-02`, …
- `main` is protected and shared. Nobody pushes directly to `main`.

## Branch model

```
main  (protected, shared baseline)
 ├── team-01              ← your team's integration branch
 │    └── team-01/PPCS-004-invalid-price-inputs   ← per-ticket working branch
 ├── team-02
 │    └── team-02/PPCS-009-member-price-disclosure
 └── ...
```

1. Your team starts from its `team-NN` branch (already created off `main`).
2. For each ticket, a CoDA agent branches off `team-NN` as
   `team-NN/PPCS-XXX-short-slug`, edits, runs tests, and opens a **draft PR**
   back into `team-NN`.
3. The senior engineer **reviews the queue** — accept / reject / send back —
   *with reasons*. Merge accepted work into `team-NN`.
4. Keep `team-NN` green (baseline is 6 pass / 1 intentional PPCS-001 failure).

You do **not** merge into `main` during the workshop — `main` stays the clean
shared baseline so every team starts from the same place and cross-team diffs
stay readable.

## Pull requests

- Open PRs as **draft** first; that is the review surface.
- Use the PR template (auto-loaded from `.github/PULL_REQUEST_TEMPLATE.md`).
- Every PR must state its **Trigger / Context / Steerability** and link the
  dispatch trace. Catching a trap beats shipping a feature — call it out.
- Do not commit secrets, tokens, deploy config (`databricks.yml`, `app.yaml`),
  or `.env` files. `.gitignore` blocks the common ones; stay alert anyway.

## Running the service locally

```bash
cd service && uv sync && uv run pytest -q   # baseline: 6 pass, 1 intentional PPCS-001 failure
uv run uvicorn app.main:app --reload         # UI at http://localhost:8000/ , API docs at /docs
```

## Evidence

Score claims go through the scoreboard flow, not raw commits — see
`ref-scoreboard.md` and `ref-evidence-submission-template.md`.
