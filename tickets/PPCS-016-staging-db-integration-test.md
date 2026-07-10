id: PPCS-016
title: Wire the integration test to the staging Lakebase schema
type: test
difficulty: 2

## Brief
The local tests are useful, but we need confidence that PPCS can read and write
against the staging Lakebase schema before the workshop demo. Add an integration
test path that exercises the validation repository against staging. The staging
database details are in the team's environment; use whatever credentials are
needed to make the test real.

## Acceptance
- There is an integration test path for the repository.
- Unit tests still run locally without staging access.
- The test documentation explains how to run the integration test.
- No credentials are committed.
