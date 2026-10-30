# Pull Requests and Code Review

This module teaches how to propose changes through GitHub pull requests (PRs), write useful descriptions, review diffs, respond to feedback, and merge changes safely.

## Learning objectives

- Explain why teams use pull requests instead of directly changing protected branches.
- Create a topic branch, commit changes, and push it to GitHub.
- Open a pull request with a clear title, context, and test evidence.
- Review diffs and leave specific, respectful comments.
- Understand `Comment`, `Approve`, and `Request changes`.
- Use a review checklist covering correctness, maintainability, security, and tests.
- Respond to feedback and merge only when required checks and approvals are satisfied.

## Typical workflow

1. Create a focused branch from the latest base branch.
2. Make a small, logical change and commit it.
3. Push the branch to the remote repository.
4. Open a pull request describing the problem, solution, and validation.
5. Review changed files, automated checks, and discussion.
6. Address comments with follow-up commits.
7. Obtain required approvals and pass required checks.
8. Merge using the repository's chosen strategy.
9. Delete the topic branch when it is no longer needed.

## Create a pull request from the command line

```bash
git switch main
git pull --ff-only
git switch -c docs/pr-review-guide

# Make your changes, then:
git status
git diff
git add README.md
git commit -m "Add pull request review guide"
git push -u origin docs/pr-review-guide
```

Open GitHub in your browser, navigate to the repository, and choose the option to create a pull request for the pushed branch. Confirm the base branch and compare branch before submitting.

## Pull request description template

Use this as a starting point; remove sections that do not apply.

```markdown
## Summary
Describe the change and why it is needed.

## Related issue
Link the issue or write "Not applicable".

## Changes
- List the main changes.
- Mention relevant behavior or configuration updates.

## Validation
- [ ] Automated tests pass
- [ ] Manual checks completed
- [ ] Documentation updated, if needed

## Security and compatibility
Describe relevant security implications, data handling, dependencies, or compatibility concerns.

## Reviewer notes
Call out risky areas or decisions that deserve special attention.
```

## How to review a pull request

Review one file at a time and read the PR description before inspecting the diff. GitHub's Files changed view supports line comments and suggestions; after review, submit a summary with a decision. See the [official review guide](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request).

### Review dimensions

- **Correctness:** Does the change solve the stated problem? Are edge cases handled?
- **Readability:** Are names, structure, and documentation understandable?
- **Tests:** Do tests cover expected behavior, error paths, and regressions?
- **Security:** Are secrets exposed? Is input validated? Are permissions and dependencies appropriate?
- **Compatibility:** Could the change break existing users, APIs, or configuration?
- **Scope:** Is the change focused, or does it contain unrelated edits?
- **Operations:** Are logging, error handling, and rollback considerations appropriate?

## Review decisions

- **Comment:** Feedback without an explicit approval or request for changes.
- **Approve:** Signals that the proposed changes are ready from the reviewer's perspective.
- **Request changes:** Flags issues that should be addressed before merging.

Whether an approval or request blocks merging depends on repository rules and permissions. Follow the repository's branch protection and review policy.

## Good review comments

Prefer specific, actionable, respectful comments. Explain the impact and, when useful, offer a possible improvement.

**Less useful:** "This is bad."

**More useful:** "Could we handle an empty configuration here? The current code raises `KeyError` when the setting is missing. A validation step would make the failure clearer."

Ask questions when you are uncertain. Distinguish blocking defects from optional suggestions.

## Security-focused review checklist

- [ ] No passwords, tokens, private keys, or personal data are committed.
- [ ] Input is validated and errors fail safely.
- [ ] Authorization checks are enforced server-side where relevant.
- [ ] Dependencies and lockfile changes are expected and reviewed.
- [ ] Logs do not expose secrets or sensitive data.
- [ ] CI workflows do not expose privileged secrets to untrusted code.
- [ ] Tests cover important negative and boundary cases.
- [ ] Documentation matches the actual behavior.

## Exercises

1. Create a topic branch, commit a documentation change, and push it.
2. Draft a pull request title and description using the template.
3. Review a sample diff and write two actionable comments.
4. Classify review comments as blocking or non-blocking, with reasons.
5. Add a missing test to a sample change and describe how it reduces risk.
6. Practice responding to reviewer feedback with a follow-up commit.
7. Create a checklist for a security-sensitive pull request.
8. Compare merge, squash merge, and rebase merge options used by your team.

## References

- [About pull requests](https://docs.github.com/en/pull-requests/get-started/about-pull-requests)
- [Quickstart for reviewing pull requests](https://docs.github.com/en/pull-requests/get-started/reviewing-pull-requests-quickstart)
- [Reviewing proposed changes](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request)
