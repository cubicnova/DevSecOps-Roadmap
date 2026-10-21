# Git Conflict Resolution Checklist

Use this checklist whenever Git reports a merge or rebase conflict.

## Before resolving

- [ ] Confirm the repository and current branch.
- [ ] Run `git status`.
- [ ] Protect unrelated work by committing or safely backing it up.
- [ ] Identify the operation in progress: merge, rebase, cherry-pick, or another operation.
- [ ] List unresolved files.

```bash
git status
git diff --name-only --diff-filter=U
```

## During resolution

- [ ] Read both versions and understand the intent of each change.
- [ ] Check related code, configuration, tests, and documentation.
- [ ] Edit the file to the correct final content.
- [ ] Remove conflict markers from actual source files.
- [ ] Avoid blindly accepting one side.
- [ ] Ask the author or team when intent is unclear.

## Before completing

- [ ] Review `git diff`.
- [ ] Review staged changes with `git diff --staged`.
- [ ] Run `git diff --check`.
- [ ] Run relevant tests, linters, or validation.
- [ ] Confirm `git status` reports no unmerged paths.
- [ ] Stage the resolved files.
- [ ] Complete the merge or continue the rebase.

## If you need to stop

For an active merge:

```bash
git merge --abort
```

For an active rebase:

```bash
git rebase --abort
```

Check `git status` afterward. Do not use abort commands after the operation has already completed.

## After resolution

- [ ] Review the resulting commit history.
- [ ] Push only to the intended remote and branch.
- [ ] Communicate any non-obvious resolution decisions to reviewers.
- [ ] Confirm tests pass in the integrated state.

## Remember

A conflict is a decision point, not simply a command-line obstacle. The correct resolution is the content that preserves the intended behavior of the project.
