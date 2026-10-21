# Branch Protection Examples

## 1. A safe feature-branch workflow

```bash
git switch main
git pull --ff-only
git switch -c feature/add-health-check
# edit files
git add .
git commit -m "feat: add health check"
git push -u origin feature/add-health-check
```

Then open a pull request to `main`. Git commands create and publish the branch; GitHub enforces configured protection rules during updates and merges.

## 2. Suggested policy by branch type

| Branch | Suggested protections |
|---|---|
| `main` | PR required, approvals, CI checks, no force push/deletion |
| `release/*` | PR required, release tests, limited push access, no force push/deletion |
| `develop` | PR required, CI checks, review policy suited to team |
| `feature/*` | Usually lighter controls; team policy may still require checks |

These are starting points, not universal requirements.

## 3. Sample CI checks to require

Possible checks for an application repository:

- `tests`
- `lint`
- `dependency-audit`

Use the actual names reported by your repository's CI workflows. A name in this example is not automatically created by GitHub.

## 4. What a blocked merge might look like

```text
Required status check "tests" is expected.
```

Response:
1. Open the pull request's **Checks** tab.
2. Inspect failed, pending, or missing checks.
3. Fix the underlying issue or correct the configured check name.
4. Push the fix to the feature branch.
5. Wait for checks to complete and request any required re-review.

## 5. Branch protection and Git commands

Protection is configured on the hosting service; there is no general local Git command that turns on GitHub branch protection. Local commands such as these help contributors follow the workflow:

```bash
git status
git fetch origin
git diff origin/main...HEAD
git push
```

If a direct push to `main` is rejected, do not try to bypass the rule. Create or use a feature branch and open a pull request.
