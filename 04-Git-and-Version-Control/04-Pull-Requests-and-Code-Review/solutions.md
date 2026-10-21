# Pull Requests and Code Review — Suggested Answers

These are examples of good practice rather than the only acceptable answers.

## Exercise 1 — Create a topic branch

```bash
git switch main
git pull --ff-only
git switch -c docs/pr-practice
# Edit the intended documentation file.
git status
git diff
git add README.md
git commit -m "Add pull request practice notes"
git push -u origin docs/pr-practice
```

Confirm the correct file is staged before committing. If the repository uses `master`, substitute the actual base branch.

## Exercise 2 — Pull request description

A good description states the problem, summarizes the change, lists validation evidence, and notes security or compatibility concerns. Keep it concise but specific. Link a related issue when one exists.

## Exercise 3 — Review a diff

Review the PR description first, then inspect every changed file. Focus on correctness, readability, test coverage, security, compatibility, and scope. Write comments on the lines that demonstrate the concern.

## Exercise 4 — Classify feedback

1. **Blocking:** exposing a token in logs is a security issue that should be fixed before merge.
2. **Usually non-blocking:** a naming improvement may be optional unless the name causes real confusion.
3. **Clarifying question:** compatibility requirements should be confirmed before deciding whether the change is safe.
4. **Blocking:** if empty lists are supported, the regression should be fixed and tested.

Context can change these classifications; explain the impact and follow the team's review policy.

## Exercise 5 — Respond to a review

Edit the relevant file, run the applicable tests, commit the fix, and push to the same source branch. Reply to the comment with what changed and the validation performed. If you disagree, explain the reasoning respectfully and provide evidence.

## Exercise 6 — Test evidence

Example:

```markdown
## Validation
- [x] Unit tests pass locally
- [x] Empty and malformed input cases tested
- [ ] Integration tests not run: test service unavailable
```

Only mark checks as complete if they were actually performed.

## Exercise 7 — Security review

- **Dependency:** check the package source, version rationale, license, maintenance, and known vulnerabilities.
- **CI workflow:** review permissions, token scopes, event triggers, and whether untrusted code can access secrets.
- **Logging:** ensure credentials, tokens, and personal data are not written to logs.
- **User input:** validate type, size, format, and authorization; test invalid and boundary inputs.

## Exercise 8 — Merge strategy

- **Merge commit:** retains branch context but adds a merge commit.
- **Squash merge:** produces a tidy single commit, but does not retain individual topic commits as base-branch history.
- **Rebase merge:** produces linear history, but changes commit identities when commits are replayed.

Choose according to repository settings, traceability needs, and team conventions.

## Mini-project — Example readiness checklist

- [ ] PR title and description explain the goal.
- [ ] Changes are focused and reviewable.
- [ ] Tests and checks are accurately reported.
- [ ] Security-sensitive changes were inspected.
- [ ] Blocking comments are resolved.
- [ ] Required approvals and status checks are satisfied.
- [ ] Merge strategy matches repository policy.
