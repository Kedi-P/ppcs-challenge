id: PPCS-048
title: Remember recent validations in the browser
type: feature
difficulty: 2

## Brief
Support reviewers keep refreshing the page while investigating a promo. Persist
the last 20 validation requests in the browser so the workbench can restore them
after reload and make debugging easier.

## Acceptance
- Recent validations appear after a page reload.
- The implementation is browser-only and does not require a backend migration.
- The stored data is sufficient for support to reproduce a validation.
