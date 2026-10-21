# Git Fundamentals - Reference Solutions

These are example commands and explanations. Run commands in a disposable repository and adapt branch names to your setup.

## Lab 1: Verify installation

```bash
git --version
git config --get user.name
git config --get user.email
```

Set identity if required:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Lab 2: Initialize

```bash
mkdir git-lab
cd git-lab
git init
git status
```

The `.git` directory stores repository metadata, objects, references, and configuration.

## Lab 3: First commit

```bash
echo "# Git Lab" > README.md
git status
git add README.md
git status
git commit -m "Add initial README"
git log --oneline
```

## Lab 4: Diff

```bash
echo "A second line." >> README.md
git diff
git add README.md
git diff --staged
git commit -m "Expand README"
```

- `git diff` normally shows unstaged changes.
- `git diff --staged` shows changes staged for the next commit.

## Lab 5: Branching

```bash
git switch -c feature-notes
echo "Practice notes" > NOTES.md
git add NOTES.md
git commit -m "Add practice notes"
git switch main
git merge feature-notes
git log --oneline --graph --all
```

If the default branch is `master`, replace `main` with `master`.

## Lab 6: Ignore rules

`.gitignore` example:

```gitignore
.env
*.log
__pycache__/
.venv/
```

Check ignored files with:

```bash
git status --ignored
```

Ignore rules do not remove files already tracked by Git. To stop tracking a file while keeping it locally, use `git rm --cached filename` and commit that change. If the file contained a real secret, rotate the secret and follow the repository's incident procedure; history may still contain the old value.

## Lab 7: Remote

```bash
git remote add origin git@github.com:USERNAME/REPOSITORY.git
git remote -v
git push -u origin main
```

Use the actual URL and branch name for your repository. If `origin` exists, update it with `git remote set-url origin <URL>` only after confirming the intended destination.

## Lab 8: Conflict resolution

After a merge conflict:

1. Run `git status` to identify conflicted files.
2. Open each file and choose the correct final content.
3. Remove `<<<<<<<`, `=======`, and `>>>>>>>` markers.
4. Run tests or inspect the file.
5. Stage the resolved file.
6. Complete the merge commit.

```bash
git add conflicted-file.txt
git commit
```

## Lab 9: Review

```bash
git log --oneline --graph --all
git show --stat
git status
```

Reviewing the branch and working tree helps prevent accidental changes to the wrong project or loss of uncommitted work.

## Lab 10: Suggested commit sequence

```bash
git add README.md app.py tests/test_app.py .gitignore
git commit -m "Add initial DevSecOps utility"
```

Then create a feature branch, make a small documented improvement, test it, commit it, and merge it back to the default branch.

## Reflection answers

1. The working tree is the current checkout, the staging area selects changes for the next commit, and history contains recorded commits.
2. Branches isolate work so changes can be developed and reviewed before merging.
3. `git commit` records a snapshot locally; `git push` transfers commits to a remote repository.
4. Commit messages make the purpose of each change easier to understand and review.
5. Revoke or rotate the exposed credential immediately, remove it from current files and follow the repository's history-cleanup process if needed. Treat the credential as compromised even if the repository was private.
