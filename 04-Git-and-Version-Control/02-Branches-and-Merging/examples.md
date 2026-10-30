# Branches and Merging: Command Examples

Use a practice repository for experiments.

## 1. Create and switch to a branch

```bash
git switch -c feature/log-parser
git branch
git status
```

The new branch starts from the currently checked-out commit.

## 2. Compare a topic branch with the base branch

```bash
git diff main...feature/log-parser
git log --oneline --graph --decorate --all
```

The three-dot diff compares the topic branch's changes since its merge base with `main`.

## 3. Merge a branch into the current branch

```bash
git switch main
git merge feature/log-parser
```

Git merges the named branch into the branch currently checked out.

## 4. Require a fast-forward merge

```bash
git merge --ff-only feature/docs
```

Git refuses if the current branch cannot advance directly to the branch tip.

## 5. Keep an explicit merge commit

```bash
git merge --no-ff feature/docs
```

This requests a merge commit even when a fast-forward would have been possible.

## 6. Recognize a conflict

A conflicted file may contain:

```text
<<<<<<< HEAD
Status: reviewed
=======
Status: feature complete
>>>>>>> feature/status
```

These markers separate the current branch's content from the incoming branch's content. They are not valid final content and must be removed.

## 7. Complete a conflict resolution

Edit the file to the intended final content, for example:

```text
Status: reviewed and feature complete
```

Then run:

```bash
git diff
git add status.txt
git merge --continue
git status
```

If you decide to cancel while the merge is still in progress:

```bash
git merge --abort
```

## 8. Review branch cleanup candidates

```bash
git branch --merged
git branch --no-merged
git branch -d feature/log-parser
```

Use `-d` for ordinary deletion because Git protects against deleting branches it considers unmerged. Avoid `-D` unless you understand the consequences.

## 9. Inspect a merge

```bash
git show --stat --oneline HEAD
git log --oneline --graph --decorate --all
git diff HEAD^ HEAD
```

Review the output and run relevant tests before pushing.

## 10. Handle local changes before switching

```bash
git status
git stash push -m "work before branch switch"
git switch main
# Later, return to the branch and restore the work:
git stash pop
```

Inspect the result of `stash pop` carefully because it can itself produce conflicts.
