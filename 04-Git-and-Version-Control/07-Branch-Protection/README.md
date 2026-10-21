# 07 — Branch Protection

Learn how to protect important GitHub branches and enforce safer collaboration practices.

## Learning objectives

By the end of this module, you should be able to:

- Explain why default and release branches need protection.
- Configure a branch protection rule in GitHub.
- Require pull requests, approvals, and passing CI checks.
- Prevent accidental branch deletion and force pushes.
- Understand branch protection rules versus repository rulesets.
- Troubleshoot blocked merges without bypassing safeguards.

## Why branch protection matters

A branch such as `main` often represents reviewed, working, or releasable code. Branch protection adds server-side rules so contributors cannot merge changes unless required conditions are met. It helps prevent accidental history rewrites, unreviewed changes, and merges that fail automated checks.

## Core concepts

| Setting | Purpose |
|---|---|
| Require a pull request before merging | Prevents direct changes from bypassing the PR workflow |
| Required approvals | Requires review from one or more eligible reviewers |
| Dismiss stale approvals | Requires re-review when later commits change the pull request |
| Require status checks | Blocks merging until selected CI checks succeed |
| Require conversation resolution | Ensures review discussions are resolved before merge |
| Require signed commits | Requires commits to be signed and verified |
| Require linear history | Prevents merge commits where the setting applies |
| Restrict who can push | Limits who can update matching branches |
| Block force pushes / prevent deletion | Protects history and keeps important branches available |
| Include administrators / restrict bypass | Makes safeguards apply more consistently, depending on configuration |

Exact options and availability depend on repository type, plan, and permissions.

## Configure a branch protection rule

1. Open the repository on GitHub.
2. Go to **Settings → Branches** (the exact navigation may vary as GitHub evolves).
3. Add a branch protection rule.
4. Set the branch name pattern to `main` for the default branch, or use a pattern such as `release/*` for matching release branches.
5. Enable **Require a pull request before merging**.
6. Require at least one approval for a team project; consider more for high-risk changes.
7. Enable **Require status checks to pass before merging** and select the real CI checks your repository runs.
8. Keep force pushes and deletions disabled for important branches.
9. Consider requiring conversation resolution and applying rules to administrators.
10. Save the rule and test the expected workflow with a pull request.

Do not select a required status check until the corresponding check has run and appears in GitHub. Keep CI job names unique across workflows to avoid ambiguous check results.

## Recommended baseline for `main`

- Require pull requests before merging.
- Require at least one approving review.
- Dismiss stale approvals when new commits change the reviewable diff.
- Require relevant automated tests, linting, and security checks.
- Require review conversations to be resolved.
- Prevent force pushes and deletion.
- Review administrator and bypass permissions.
- Document an emergency process rather than routinely bypassing controls.

Adapt the policy to your team's risk, repository plan, and delivery workflow.

## Example workflow

```bash
git switch -c feature/update-readme
# Make changes, then:
git add README.md
git commit -m "docs: update README"
git push -u origin feature/update-readme
```

Open a pull request from `feature/update-readme` into `main`. Wait for required checks, request review, address feedback, and merge only when all branch rules are satisfied.

## Branch protection versus rulesets

Branch protection rules are a branch-specific mechanism. GitHub rulesets provide another way to apply and layer repository or organization rules; multiple applicable rulesets can be enforced together. Check the official documentation and your repository's available settings before choosing a model.

## Troubleshooting

- **Merge button is blocked:** Review the pull request's checks, review requirements, unresolved conversations, and branch-up-to-date requirement.
- **Required check is missing:** Confirm the workflow ran and the expected check name is correct.
- **Branch is behind the base branch:** Update your feature branch using your team's merge or rebase policy, then rerun checks.
- **Direct push is rejected:** This may be expected when pull requests are required. Push to a feature branch and open a pull request.
- **A rule seems not to apply:** Check the target branch pattern, overlapping rules, permissions, and bypass settings.

## Exercises

1. Draft a protection policy for `main`.
2. Explain why force-push protection matters.
3. List the CI checks that should be required before merging an application change.
4. Describe how a contributor should respond to a blocked pull request.
5. Compare a branch protection rule with a ruleset.

## References

- [About protected branches — GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- [Managing a branch protection rule — GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)
- [About rulesets — GitHub Docs](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
