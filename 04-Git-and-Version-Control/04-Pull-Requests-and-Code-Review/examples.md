# Pull Requests and Code Review — Examples

## 1. Publish a topic branch

```bash
git switch main
git pull --ff-only
git switch -c feature/input-validation
# Make changes and run tests.
git diff
git add .
git commit -m "Validate user input"
git push -u origin feature/input-validation
```

Push only changes you intend to share. Avoid `git add .` if unrelated or sensitive files may be present; inspect `git status` first.

## 2. Example pull request title

```text
Add validation for uploaded configuration files
```

A useful title describes the outcome rather than saying only "updates" or "fixes".

## 3. Example pull request body

```markdown
## Summary
Validate configuration input before processing it.

## Changes
- Reject missing required fields.
- Return a clear validation error.
- Add tests for malformed input.

## Validation
- [x] Unit tests pass
- [x] Invalid input cases tested

## Security considerations
No credentials or production data are included.
```

## 4. Example review comments

**Blocking:** "This path accepts an empty value and passes it to the authorization check. Please reject empty input and add a regression test."

**Non-blocking:** "Consider extracting this repeated formatting logic into a helper to make the function easier to read."

**Clarifying question:** "Is this dependency version required for a compatibility fix? Could you add a note explaining the reason for the upgrade?"

## 5. Respond to feedback

Make the requested change on the same topic branch, test it, and push another commit:

```bash
git status
# Edit the relevant files.
git diff
git add path/to/file
git commit -m "Handle empty configuration input"
git push
```

The open pull request updates automatically when new commits are pushed to its source branch.

## 6. Review checklist template

```markdown
- [ ] I understand the problem and intended behavior.
- [ ] The diff contains only relevant changes.
- [ ] Error handling and edge cases are covered.
- [ ] Tests pass and cover regression risks.
- [ ] No secrets or sensitive data are exposed.
- [ ] Dependency and workflow changes are justified.
- [ ] Documentation is updated where necessary.
```

## 7. Merge strategy overview

- **Merge commit:** Preserves the branch structure and creates a merge commit.
- **Squash and merge:** Combines the topic branch's changes into one commit on the base branch.
- **Rebase and merge:** Replays commits onto the base branch to create a linear history.

The repository's settings determine which options are available. Follow team policy and avoid rewriting shared history unexpectedly.
