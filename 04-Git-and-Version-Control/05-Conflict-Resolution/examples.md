# Conflict Resolution - Examples

Run these commands only in a disposable practice repository or a project where you are authorized to make changes.

## 1. Create a practice repository

```bash
mkdir conflict-lab
cd conflict-lab
git init
git switch -c main
echo "Status: draft" > status.txt
git add status.txt
git commit -m "Add initial status"
```

If your Git version or configuration creates a different default branch, use your current branch name consistently.

## 2. Create two branches that change the same line

Create the first branch and change the file:

```bash
git switch -c feature-a
echo "Status: reviewed by feature A" > status.txt
git add status.txt
git commit -m "Update status in feature A"
```

Return to the base branch and make a different edit to the same line:

```bash
git switch main
echo "Status: reviewed by main" > status.txt
git add status.txt
git commit -m "Update status on main"
```

Attempt the merge:

```bash
git merge feature-a
```

Git should report a conflict because both branches changed the same line differently.

## 3. Understand conflict markers

A conflicted file may contain:

```text
<<<<<<< HEAD
Status: reviewed by main
=======
Status: reviewed by feature A
>>>>>>> feature-a
```

- `<<<<<<<` starts the current-side section.
- `=======` separates the competing versions.
- `>>>>>>>` ends the incoming-side section.

The marker labels and exact form can vary by operation. Do not keep the markers in the final file.

## 4. Resolve manually

Edit `status.txt` so it contains the desired final result, for example:

```text
Status: reviewed by main and feature A
```

Then inspect and complete the merge:

```bash
git diff
git diff --check
git status
git add status.txt
git commit -m "Resolve status conflict"
git log --oneline --graph --all
```

## 5. List conflicted files

```bash
git status
git diff --name-only --diff-filter=U
```

The second command lists paths with unresolved merge conflicts.

## 6. Inspect conflict stages

For an unmerged file, Git may store up to three index stages:

```bash
git show :1:status.txt
git show :2:status.txt
git show :3:status.txt
```

These represent the merge base, current side, and other side for a typical merge conflict. A stage may be absent for add/delete cases. Use this only when the file and operation match the example.

## 7. Abort a merge

If you decide not to continue the merge:

```bash
git merge --abort
git status
```

Run this during an active merge, not after the merge has already completed. Make sure unrelated work was committed or safely backed up before beginning.

## 8. Resolve during a rebase

```bash
git status
# Edit each conflicted file and remove conflict markers.
git add path/to/resolved-file
git rebase --continue
```

To abandon the rebase and return to its starting state:

```bash
git rebase --abort
```

During a rebase, the meanings of “ours” and “theirs” can be counterintuitive. Inspect the content rather than choosing a side automatically.

## 9. Check for leftover markers

Search tracked files for conflict markers:

```bash
git grep -n -E '^(<<<<<<<|=======|>>>>>>>)'
```

This can also match intentional examples in documentation. Review each result; do not assume every match is an unresolved conflict.

## 10. Useful prevention habits

- Keep branches small and short-lived.
- Pull or fetch regularly according to the team's workflow.
- Avoid having multiple contributors edit the same large file at once.
- Communicate ownership of files likely to conflict.
- Add tests and review the diff after resolution.

## Official references

- https://git-scm.com/docs/git-merge
- https://git-scm.com/docs/git-rebase
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts
