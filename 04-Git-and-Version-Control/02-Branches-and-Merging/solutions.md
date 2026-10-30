# Branches and Merging: Suggested Solutions

These are reference workflows. Substitute your repository's actual base branch name and commit hashes.

## Exercise 1 — Branch basics

```bash
git status
git branch
git switch -c practice/branch-basics
git branch
```

The asterisk in `git branch` indicates the current branch.

## Exercise 2 — Commit on a topic branch

```bash
echo "Branch practice" > practice-note.txt
git add practice-note.txt
git commit -m "Add branch practice note"
git log --oneline -5
```

## Exercise 3 — Merge a branch

```bash
git switch main
git merge practice/branch-basics
git log --oneline --graph --decorate --all
```

A fast-forward is possible when the target branch has not diverged and can advance to the topic branch tip. If both branches have independent commits, Git generally needs a three-way merge.

## Exercise 4 — Merge strategies

- `git merge --ff-only <branch>` permits only a fast-forward and fails if the branches have diverged.
- `git merge --no-ff <branch>` requests a merge commit even if a fast-forward is possible.
- `git merge <branch>` allows Git to fast-forward when possible and otherwise use a three-way merge when appropriate.

The actual result depends on the repository's commit graph.

## Exercise 5 — Non-overlapping changes

Make two branches from a common base and change separate lines. Merge each into the base branch. Git can usually combine edits that do not overlap, though file structure and context can affect the result.

## Exercise 6 — Conflict resolution

```bash
git status
# Edit the conflicted file and remove all conflict markers.
git diff
git add path/to/conflicted-file
git merge --continue
git status
```

Review both versions before editing. Run relevant tests after the conflict is resolved.

## Exercise 7 — Abort a merge

```bash
git merge --abort
git status
```

This attempts to return the repository to the state before the in-progress merge. Protect unrelated uncommitted work first, because complicated pre-existing changes can make recovery less straightforward.

## Exercise 8 — Branch cleanup

```bash
git branch --merged
git branch --no-merged
git branch -d practice/branch-basics
```

Confirm that the branch is merged and no longer needed before deleting it.

## Exercise 9 — Branch from an older commit

```bash
git log --oneline
git switch -c practice/older <commit-id>
```

Replace `<commit-id>` with a real commit hash. The new branch points to that historical commit rather than the current tip.

## Exercise 10 — Example team policy

- Names: `feature/`, `fix/`, `docs/`, followed by a short description.
- Commits: use concise imperative messages describing one logical change.
- Reviews: run tests and request review before integrating into protected branches.
- Conflicts: inspect both sides, remove markers, and test the resolved result.
- Cleanup: delete topic branches after confirming they are merged and no longer needed.
- Shared history: avoid force-pushing shared branches unless the team explicitly agrees.

## Troubleshooting

### “Your local changes would be overwritten”

Check `git status`, then commit or stash your work before switching branches.

### “Already up to date”

The current branch may already contain the commits being merged. Inspect `git log --oneline --graph --all` to confirm.

### Conflict markers remain

Search the file for `<<<<<<<`, `=======`, and `>>>>>>>`, remove the markers, inspect the final content, and run tests before staging the file.
