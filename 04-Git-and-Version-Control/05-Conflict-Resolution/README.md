# 05 - Conflict Resolution

Learn to recognize, understand, and safely resolve Git merge conflicts during branch integration and collaboration.

## Learning objectives

By completing this module, you should be able to:

- Explain why Git reports conflicts.
- Identify conflicted files and inspect conflict markers.
- Resolve conflicts manually and validate the result.
- Continue or abort a merge safely.
- Resolve conflicts during a rebase.
- Use `git diff`, `git status`, and `git log` to understand repository state.
- Reduce avoidable conflicts through collaboration practices.
- Protect uncommitted work before attempting conflict resolution.

## Module files

```text
05-Conflict-Resolution/
├── README.md
├── examples.md
├── practical.md
├── solutions.md
└── conflict-checklist.md
```

## Prerequisites

- Git installed and basic knowledge of commits and branches.
- Familiarity with `git status`, `git diff`, `git switch`, `git merge`, and `git log`.

## What is a merge conflict?

Git can automatically combine many changes. A conflict occurs when Git cannot determine the intended final result—for example, when two branches change the same lines differently or when one branch deletes a file another branch modifies.

A conflict is not data loss by itself. It is a request for a person to choose or construct the correct final content.

## Standard merge-conflict workflow

1. Check the repository state with `git status`.
2. Identify conflicted files.
3. Open each file and review the conflict markers.
4. Edit the file to the intended final content.
5. Remove all conflict markers.
6. Run tests or inspect the diff.
7. Stage resolved files.
8. Complete the merge commit.

```bash
git status
git diff
# Edit conflicted files in your editor.
git diff --check
git add path/to/resolved-file
git status
git commit
```

## Abort safely

If you need to return to the pre-merge state and Git supports aborting the current operation:

```bash
git merge --abort
```

For a conflicted rebase:

```bash
git rebase --abort
```

Before starting, commit or safely back up unrelated work. Abort commands are intended to restore the operation's starting state, but should not replace understanding the current repository state.

## Safety notes

- Use a disposable repository for practice.
- Read `git status` before running commands.
- Do not blindly accept “ours” or “theirs”; those labels depend on the operation and may be confusing during a rebase.
- Never resolve a conflict by deleting important code or tests without understanding the impact.
- Review the final diff and run relevant tests before committing.
- Avoid force-pushing shared branches as a conflict-resolution shortcut.

## Completion checklist

- [ ] Create and reproduce a merge conflict.
- [ ] Resolve conflict markers manually.
- [ ] Validate the final diff.
- [ ] Complete a merge and inspect history.
- [ ] Practice aborting a merge in a disposable repository.
- [ ] Explain how merge conflicts differ from rebase conflicts.
