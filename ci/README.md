# CI (pending activation)

This directory holds the PPCS test workflow. It lives here — not under
`.github/workflows/` — only because the account that seeded this repo pushed
with a token missing the GitHub `workflow` OAuth scope, which is required to
create files under `.github/workflows/`.

## Activate it (one step)

Copy `ci.yml` to `.github/workflows/ci.yml` on `main`. Either:

- **Web UI:** GitHub → Add file → Create new file → path
  `.github/workflows/ci.yml` → paste the contents of `ci/ci.yml` → commit to
  `main`. (Web commits don't need the `workflow` CLI scope.)
- **CLI:** `gh auth refresh -h github.com -s workflow`, then
  `git mv ci/ci.yml .github/workflows/ci.yml && git commit -m "Activate CI" && git push`.

Once `.github/workflows/ci.yml` exists, delete this `ci/` directory.

## What it does

Runs the PPCS service test suite on `team-*` branches (push + PR). The
challenge ships one intentional failing seed test (PPCS-001,
`tests/test_rules.py::test_marginal_discount_below_threshold_fails`), so the
documented baseline is **6 passed, 1 failed**. The workflow treats that exact
baseline as success and fails CI only on a *different* failure (a real
regression) or if the suite can't run. It does not reward silently "fixing"
the PPCS-001 seed.
