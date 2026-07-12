# Repo Access Self-Test

Run this before the workshop if you are asked to confirm GitHub access. It proves
you can read the challenge repo, create a branch, push it, and open a draft PR.

Use a throwaway branch and PR. Do not use a real ticket branch for this test.

## Prerequisites

- GitHub CLI installed.
- GitHub CLI authenticated with the account you will use during the workshop.
- Access to the nominated challenge repository.

## 1. Confirm GitHub Auth

```bash
gh auth status
```

If you have multiple GitHub accounts, switch to the workshop one before
continuing — CoDA sync writeback to the Databricks Git folder uses this identity:

```bash
gh auth switch
gh auth status
```

Pass criteria:

- The account shown is the account you will use during the workshop.
- The account has access to the challenge repository.

## 2. Confirm Repo Visibility

Replace `<owner>/<repo>` with the nominated workshop repository.

```bash
gh repo view <owner>/<repo> --json nameWithOwner,url,viewerPermission
```

Pass criteria:

- The command returns repository metadata.
- `viewerPermission` is enough to create a branch and draft PR.

## 3. Clone and Create a Scratch Branch

```bash
git clone https://github.com/<owner>/<repo>.git coda-access-check
cd coda-access-check
git checkout -b access-check/<your-github-login>
mkdir -p .access-checks
printf "access check for <your-github-login>\n" > .access-checks/<your-github-login>.md
git add .access-checks/<your-github-login>.md
git commit -m "chore: access check for <your-github-login>"
git push -u origin access-check/<your-github-login>
```

Pass criteria:

- Branch push succeeds.
- No secret-scanning or permission failure blocks the push.

## 4. Open a Draft PR

```bash
gh pr create \
  --draft \
  --title "chore: access check for <your-github-login>" \
  --body "Pre-workshop access check. Close after verification." \
  --base main \
  --head access-check/<your-github-login>
```

Pass criteria:

- GitHub returns a draft PR URL.
- The PR is clearly labelled as an access check.

## 5. Record Evidence

Fill the `repo` section in `attendee-access-evidence-template.json`.

This repo self-test alone is not a complete attendee access proof. The final
attendee evidence JSON must also include the Databricks/App/trace and agent
sections from `01-databricks-agent-access-self-test.md` before the facilitator can
validate it with the workshop evidence checker.

Use the exact GitHub `owner/repo` value, a GitHub draft PR URL ending in
`/pull/<number>`, and a `viewer_permission` value of `WRITE`, `MAINTAIN`, or
`ADMIN`. `READ` is not enough evidence because participants must be able to
push a branch and open a draft PR.

If you cannot use the JSON template for this repo-only step, send:

```text
GitHub account:
Repo:
Branch:
Draft PR:
Any error:
```

## 6. Cleanup

After the facilitator confirms the evidence:

```bash
gh pr close <pr-number> --delete-branch
cd ..
```

The facilitator may choose to leave one access-check PR open as evidence for the
dry run. Do not merge access-check PRs.
