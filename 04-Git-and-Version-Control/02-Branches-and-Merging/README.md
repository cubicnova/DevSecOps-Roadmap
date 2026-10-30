# Git and Version Control: Branches and Merging

This module explains how Git branches support isolated development and how to integrate changes with merges.

## Learning objectives

- Create, list, switch, rename, and delete branches.
- Compare changes between branches.
- Understand fast-forward and three-way merges.
- Resolve merge conflicts and verify the final result.
- Follow a safe branch workflow for team repositories.

## Essential commands

| Task | Command |
|---|---|
| Show current state | `git status` |
| List local branches | `git branch` |
| List local and remote branches | `git branch -a` |
| Create a branch | `git branch feature/docs` |
| Create and switch | `git switch -c feature/docs` |
| Switch branches | `git switch main` |
| Rename current branch | `git branch -m feature/documentation` |
| Compare changes | `git diff main...feature/docs` |
| View commit graph | `git log --oneline --graph --decorate --all` |
| Merge into current branch | `git merge feature/docs` |
| Allow fast-forward only | `git merge --ff-only feature/docs` |
| Force a merge commit when possible | `git merge --no-ff feature/docs` |
| List merged branches | `git branch --merged` |
| Delete a merged branch | `git branch -d feature/docs` |
| Abort an in-progress merge | `git merge --abort` |

## Recommended feature-branch workflow

Start with a clean working tree and use the branch name that matches your repository policy.

```bash
git status
git switch main
git pull --ff-only
git switch -c docs/branching-guide

# Edit documentation, then stage and commit the change.
git add README.md
git commit -m "Improve branching guide"

# Integrate the work into the target branch.
git switch main
git merge --no-ff docs/branching-guide

# Inspect the result before sharing it.
git log --oneline --graph --decorate -10
git status
```

If your team uses pull requests or protects `main`, push the feature branch and open a pull request instead of merging directly to `main`.

## Merge types

- **Fast-forward merge:** The target branch has not diverged. Git can move the target branch pointer forward without creating a merge commit.
- **Three-way merge:** Both branches have commits after their common ancestor. Git combines the changes and may create a merge commit.
- **Squash merge:** The changes are combined into one new commit. This is commonly selected in a hosting platform or performed with `git merge --squash`.

## Resolving merge conflicts

1. Run `git status` to identify conflicted files.
2. Open each file and locate conflict markers: `<<<<<<<`, `=======`, and `>>>>>>>`.
3. Review both versions and edit the file into the intended final form.
4. Remove all conflict markers.
5. Run tests or inspect the changes.
6. Stage resolved files and complete the merge.

```bash
git add path/to/resolved-file
git merge --continue
```

To cancel an in-progress merge instead:

```bash
git merge --abort
```

Do not choose “ours” or “theirs” without reviewing the content. Commit or stash pre-existing work before merging; aborting a merge is not a substitute for protecting unrelated uncommitted changes.

## Practical exercises

1. Create `practice/branch-basics` and confirm the current branch.
2. Add and commit a small change on a feature branch.
3. Merge the branch into the base branch.
4. Inspect the history using `git log --oneline --graph --all`.
5. Compare `--ff-only`, `--no-ff`, and default merge behavior in a disposable repository.
6. Make different edits to separate lines in two branches and merge them.
7. Make conflicting edits to the same line, resolve the conflict, and complete the merge.
8. Start another conflict and practice `git merge --abort`.
9. Use `git branch --merged` and `git branch --no-merged` to review branch status.
10. Write a short team policy for branch names, commits, reviews, and branch cleanup.

## Safe conflict lab

Run this in a temporary directory, not in an important project:

```bash
mkdir git-merge-lab
cd git-merge-lab
git init
git config user.name "Practice User"
git config user.email "practice@example.invalid"

echo "Status: draft" > status.txt
git add status.txt
git commit -m "Add initial status"

git switch -c feature/status
echo "Status: feature complete" > status.txt
git commit -am "Update status on feature branch"

git switch main
echo "Status: reviewed" > status.txt
git commit -am "Update status on main"

git merge feature/status
```

If your initial branch is named `master`, use that name instead of `main`. The merge should conflict because both branches changed the same line. Edit `status.txt`, remove the markers, then stage and finish the merge.

## Best practices

- Keep branches focused and reasonably short-lived.
- Use descriptive names such as `feature/`, `fix/`, and `docs/`.
- Review diffs and run tests before merging.
- Commit or stash work before switching or merging.
- Follow the repository's pull-request and branch-protection rules.
- Delete branches only after confirming they are no longer needed.
- Avoid force-pushing shared branches unless your team explicitly agrees.

## References

- [Pro Git: Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [Official `git-branch` documentation](https://git-scm.com/docs/git-branch)
- [Official `git-merge` documentation](https://git-scm.com/docs/git-merge)
