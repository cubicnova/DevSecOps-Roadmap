# Git Fundamentals - Reference Solutions

Try each lab before checking these example commands. Adjust branch names and remote URLs to match your setup.

## Lab 1: Verify Git

```bash
git --version
git config --get user.name
git config --get user.email
```

If needed:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Lab 2: Initialize a repository

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

- `git diff` shows changes not yet staged.
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

Use your actual default branch name if it is not `main`.

## Lab 6: Ignore rules

Example `.gitignore` patterns:

```gitignore
.env
*.log
__pycache__/
.venv/
```

To inspect ignored files:

```bash
git status --ignored
```

If a file is already tracked, ignore rules do not stop tracking it. `git rm --cached filename` removes it from the index while leaving the local file in place, but does not erase the file from earlier commits. If a real secret was exposed, rotate or revoke it immediately.

## Lab 7: Remote

```bash
git remote add origin git@github.com:USERNAME/REPOSITORY.git
git remote -v
git push -u origin main
```

Use the real repository URL. If `origin` already exists, inspect it before changing it.

## Lab 8: Conflict resolution

1. Run `git status` to find conflicted files.
2. Open each file and choose the correct final content.
3. Remove the `<<<<<<<`, `=======`, and `>>>>>>>` marker lines.
4. Review the file and run tests if applicable.
5. Stage the resolved file.
6. Complete the merge commit.

```bash
git add conflicted-file.txt
git commit
```

## Lab 9: Review

```bash
git status
git log --oneline --graph --all
git show --stat
```

These commands help verify the current branch, uncommitted work, and recent history.

## Lab 10: Suggested workflow

```bash
git init
git add README.md app.py tests/test_app.py .gitignore
git commit -m "Add initial DevSecOps utility"
git switch -c feature-update
# Make a small change and test it.
git add .
git commit -m "Improve utility behavior"
git switch main
git merge feature-update
git log --oneline --graph --all
```

Inspect `git status` before using `git add .` so you do not stage unwanted files.

## Reflection answers

1. The working tree is the current checkout; the staging area selects content for the next commit; history contains recorded commits.
2. Branches isolate work for development and review before changes are merged.
3. `git commit` records a snapshot locally; `git push` sends commits to a remote repository.
4. A good commit message concisely explains the purpose of the change.
5. Revoke or rotate the secret immediately, remove it from current files, and follow the repository's history-cleanup procedure. Treat it as compromised even if the repository was private.

## Further reading

- https://git-scm.com/book/en/v2
- https://git-scm.com/docs
- https://docs.github.com/en/get-started/git-basics/managing-remote-repositories
