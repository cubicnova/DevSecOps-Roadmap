# Practical Lab — Configure Branch Protection

## Goal

Configure a protected `main` branch in a GitHub repository you own or are authorized to administer.

## Prerequisites

- A GitHub repository where you have permission to change settings.
- A feature branch with a small test change.
- If you want to require CI, a workflow that runs and reports status checks.

## Lab A — Configure the rule

1. Open **Settings → Branches** in your repository.
2. Create a branch protection rule targeting `main`.
3. Require pull requests before merging.
4. Set the required number of approvals to at least one if suitable for your team.
5. Enable required status checks only for checks that actually exist in the repository.
6. Keep force pushes and branch deletion disabled.
7. Consider requiring conversation resolution and including administrators.
8. Save the rule.

Record the options you enabled and why.

## Lab B — Test the workflow

1. Create a branch:

   ```bash
   git switch -c lab/branch-protection
   ```

2. Make a small documentation change, then commit and push:

   ```bash
   git add README.md
   git commit -m "docs: test branch protection workflow"
   git push -u origin lab/branch-protection
   ```

3. Open a pull request targeting `main`.
4. Observe which requirements GitHub displays.
5. If CI checks are configured, inspect their status.
6. Complete the review requirements and merge only when all required conditions are met.
7. Delete the temporary branch after merging if your repository policy permits it.

## Lab C — Test failure handling

Using a non-production test repository, create a pull request with a deliberately failing test or lint check. Confirm the merge is blocked. Fix the issue, push a new commit, and verify the required check passes.

Do not deliberately break production workflows or modify protection settings on repositories you do not control.

## Submission checklist

- [ ] Target branch and rule name recorded.
- [ ] Pull requests required.
- [ ] Approval policy documented.
- [ ] Actual CI checks selected, if available.
- [ ] Force pushes and deletion blocked.
- [ ] Pull request tested.
- [ ] Blocked-merge scenario documented.
- [ ] Any exception or bypass process documented.
