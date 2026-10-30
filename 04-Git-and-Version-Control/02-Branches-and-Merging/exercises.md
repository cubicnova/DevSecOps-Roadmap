# Branches and Merging: Exercises

Use a disposable local repository. Do not practice conflict experiments in an important working tree.

## Exercise 1 — Branch basics

1. Display the current state with `git status`.
2. List local branches.
3. Create and switch to `practice/branch-basics`.
4. Record which branch is checked out.

**Expected outcome:** the new branch exists and is the current branch.

## Exercise 2 — Commit on a topic branch

1. Create `practice-note.txt`.
2. Add a short line and commit it.
3. Inspect the commit with `git log --oneline`.

**Expected outcome:** the commit is on the topic branch and the working tree is clean.

## Exercise 3 — Merge a branch

1. Switch to the base branch (`main` or `master`).
2. Merge the practice branch.
3. Inspect the history graph.

**Questions:** Did Git fast-forward, or did it create a merge commit? Why?

## Exercise 4 — Compare merge strategies

In separate experiments, compare:

```bash
git merge --ff-only <branch>
git merge --no-ff <branch>
git merge <branch>
```

Record when each succeeds and whether a merge commit is created.

## Exercise 5 — Merge non-overlapping changes

Create two branches from the same base. Edit different lines in the same text file and commit each edit. Merge both branches into the base branch.

**Expected outcome:** Git should normally combine non-overlapping changes automatically.

## Exercise 6 — Resolve a conflict

1. Create two branches from the same commit.
2. Edit the same line differently on both branches.
3. Commit each edit.
4. Merge one branch into the other.
5. Resolve the conflict and complete the merge.

**Validation:** the final file contains the intended content and no `<<<<<<<`, `=======`, or `>>>>>>>` markers.

## Exercise 7 — Abort a merge

Repeat the conflict setup, start the merge, and run:

```bash
git merge --abort
git status
```

Explain what was cancelled and why existing uncommitted work should be protected before starting.

## Exercise 8 — Branch cleanup

Run:

```bash
git branch --merged
git branch --no-merged
```

Identify branches that are safe to remove and delete a confirmed merged branch with `git branch -d`.

## Exercise 9 — Start from an earlier commit

Find a commit hash with `git log --oneline`, then create a practice branch from that commit:

```bash
git switch -c practice/older <commit-id>
```

Explain how this branch differs from one created at the current branch tip.

## Exercise 10 — Team workflow

Write a short branch policy that defines:

- branch naming;
- commit-message conventions;
- review and test requirements;
- conflict-resolution expectations;
- when branches should be deleted.

## Mini-project — Simulated team merge

In a temporary repository, create a documentation branch and a bug-fix branch. Make separate commits, merge both into the base branch, and provide a short report containing:

- the commands used;
- a history graph;
- any conflicts and how they were resolved;
- checks performed before integration.
