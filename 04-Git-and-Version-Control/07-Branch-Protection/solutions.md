# Solutions — Branch Protection

Use these as sample answers; adapt them to your repository and team's policy.

## Exercise 1 — Draft a policy for `main`

Example policy:
- All changes must arrive through pull requests.
- At least one eligible reviewer must approve.
- New commits that change the reviewed diff dismiss stale approvals.
- Unit tests, linting, and relevant security checks must pass.
- Review conversations must be resolved.
- Force pushes and deletion are disabled.
- Administrator and bypass behavior is explicitly reviewed.

## Exercise 2 — Why block force pushes?

A force push can rewrite branch history and remove commits from the branch's visible history. Blocking it on shared, important branches reduces accidental loss and makes collaboration and auditing more predictable.

## Exercise 3 — Which checks should be required?

Require checks that are important and reliable for the repository, such as tests, linting, build validation, and dependency or security scanning. Avoid requiring a check that never runs for the relevant pull request; that can leave merges blocked.

## Exercise 4 — Responding to a blocked pull request

1. Read the exact merge-blocking message.
2. Check approvals, review conversations, branch freshness, and CI status.
3. Fix the code or configuration causing the failure.
4. Push the update to the pull-request branch.
5. Wait for required checks to complete and obtain any re-review required by policy.
6. Ask a repository administrator for help if the rule appears misconfigured; do not bypass it without authorization.

## Exercise 5 — Branch protection rule versus ruleset

Branch protection rules configure protection for matching branches, with one applicable branch protection rule taking precedence when multiple rules target a branch. Rulesets can layer multiple applicable rules, have enforcement statuses, and may target branches across repositories depending on plan and scope. Check current GitHub documentation for exact capabilities and availability.

## Troubleshooting guide

| Symptom | Likely cause | Next step |
|---|---|---|
| Required check is missing | Workflow did not run or check name differs | Run the workflow and confirm the exact reported name |
| Required check fails | CI found an issue | Inspect logs, fix the issue, push a correction |
| Approval is no longer valid | New commits changed the reviewed diff | Request review again |
| Branch must be up to date | Base branch has advanced | Update feature branch according to team policy |
| Direct push rejected | PR requirement or push restriction | Push a feature branch and open a pull request |
| Protection appears inconsistent | Pattern, overlapping rules, permissions, or bypass settings | Review settings and applicable rules |

## Suggested review rubric

- 2 points: identifies the target branch and protection purpose.
- 2 points: configures pull request and review requirements.
- 2 points: configures real CI status checks correctly.
- 2 points: protects against force pushes and deletion.
- 2 points: demonstrates and documents blocked-merge troubleshooting.

Total: 10 points.
