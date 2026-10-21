# Conflict Resolution - Reference Solutions

Use these solutions to check your work after completing the exercises.

## Lab 1: Marker meanings

- `<<<<<<<` begins one version of the content.
- `=======` separates the competing versions.
- `>>>>>>>` ends the other version.

Git cannot automatically determine which content reflects the intended result.

## Lab 2: Reproduce a conflict

```bash
mkdir conflict-lab
cd conflict-lab
git init
git switch -c main
echo "Status: draft" > status.txt
git add status.txt
git commit -m "Add initial status"

git switch -c feature-a
echo "Status: reviewed by feature A" > status.txt
git add status.txt
git commit -m "Update status in feature A"

git switch main
echo "Status: reviewed by main" > status.txt
git add status.txt
git commit -m "Update status on main"

git merge feature-a
```

Git should report a conflict in `status.txt`.

## Lab 3: Resolve manually

Edit `status.txt` to the intended final content, for example:

```text
Status: reviewed by main and feature A
```

Then:

```bash
git diff
git diff --check
git status
git add status.txt
git commit -m "Resolve status conflict"
git log --oneline --graph --all
```

## Lab 4: Multiple files

Run `git status` and resolve every path marked as unmerged. Stage each resolved file. Before committing, verify that `git status` no longer lists unmerged paths.

## Lab 5: Add/delete conflict

The correct result depends on intended behavior. Decide whether the deletion or modification should win, or whether the content should be preserved in a new location. Apply that decision manually, then stage the result and complete the merge.

## Lab 6: Abort a merge

During an active merge:

```bash
git merge --abort
git status
```

This attempts to restore the pre-merge state. Always commit or safely back up unrelated work before beginning the exercise.

## Lab 7: Rebase conflict

After editing the conflicted file:

```bash
git add path/to/resolved-file
git rebase --continue
```

Repeat if more conflicts appear. To abandon the rebase:

```bash
git rebase --abort
```

A rebase reapplies commits onto a new base and rewrites the rebased commits, so the resulting history differs from a merge.

## Lab 8: Validation commands

```bash
git status
git diff --check
git diff
git diff --staged
```

Run project-specific tests before completing the operation. A conflict-marker search can help, but review matches because examples and documentation may intentionally contain markers.

## Reflection answers

1. A conflict occurs when Git cannot automatically reconcile competing changes.
2. Markers delimit the competing versions so a person can select or combine the intended content.
3. The diff reveals accidental deletions, duplicated logic, whitespace issues, or incomplete resolution.
4. `git merge --abort` cancels an active merge; `git rebase --abort` cancels an active rebase and returns to its starting state.
5. During a rebase, Git replays commits onto another base, so the labels can describe the replay context rather than the intuitive “my branch versus their branch.” Inspect the actual content.

## Further reading

- https://git-scm.com/docs/git-merge
- https://git-scm.com/docs/git-rebase
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts
