# Conflict Resolution - Practical Exercises

Use a disposable repository. These labs intentionally create conflicts so you can practice resolving them without risking project work.

## Lab 1: Recognize conflict markers

1. Read the sample conflict in `examples.md`.
2. Identify the start marker, separator, and end marker.
3. Explain why Git cannot choose the correct line automatically.

## Lab 2: Reproduce a conflict

1. Create a repository and commit a text file.
2. Create a feature branch and change one line.
3. Return to the base branch and change the same line differently.
4. Commit both changes.
5. Merge the feature branch and inspect `git status`.

## Lab 3: Resolve manually

1. Edit the conflicted file.
2. Choose or combine the intended content.
3. Remove all conflict markers.
4. Run `git diff` and `git diff --check`.
5. Stage the resolved file and complete the merge.
6. Inspect the commit graph.

## Lab 4: Multiple conflicted files

1. Create two files and commit them.
2. Edit both files differently on two branches.
3. Merge the branches.
4. Resolve both files.
5. Confirm `git status` no longer reports unmerged paths before completing the merge.

## Lab 5: Add/delete conflict

In a disposable repository:

1. Commit a file.
2. On one branch, delete the file.
3. On another branch, modify and commit the file.
4. Merge the branches.
5. Decide whether the final result should keep, modify, or delete the file based on the intended project behavior.

Document your reasoning before resolving.

## Lab 6: Abort a merge

1. Reproduce a merge conflict.
2. Run `git status` and record the state.
3. Run `git merge --abort`.
4. Confirm the repository returned to its pre-merge state.
5. Explain why you should protect unrelated work before starting a merge.

## Lab 7: Resolve a rebase conflict

1. Create a base commit.
2. Create a feature branch with a change.
3. Add a conflicting commit to the base branch.
4. Rebase the feature branch onto the base branch.
5. Resolve the conflict, stage the file, and run `git rebase --continue`.
6. Inspect the resulting history.

Use `git rebase --abort` if you need to abandon the exercise.

## Lab 8: Validate the resolution

Before completing a merge, perform these checks:

- [ ] No unresolved paths remain in `git status`.
- [ ] No unintended conflict markers remain.
- [ ] `git diff --check` reports no whitespace errors.
- [ ] The final file content matches the intended behavior.
- [ ] Relevant tests pass.
- [ ] The staged diff contains only the intended changes.

## Lab 9: Conflict prevention plan

Write a short team plan that explains how to keep branches current, assign ownership of shared files, communicate overlapping changes, and review conflict resolutions.

## Lab 10: Mini-project

Create a small text-based configuration or Python project. Simulate two branches making overlapping changes, resolve the conflict, run the project's checks, and record the merge in Git history.

## Reflection questions

1. Why does a conflict occur?
2. What do the conflict markers represent?
3. Why should you inspect the final diff before committing?
4. What is the difference between `git merge --abort` and `git rebase --abort`?
5. Why can “ours” and “theirs” be confusing during a rebase?
