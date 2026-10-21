# Git Fundamentals - Examples

Run these commands in a disposable practice directory unless otherwise noted.

## 1. Check Git version and configuration

```bash
git --version
git config --get user.name
git config --get user.email
```

Set identity if needed:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## 2. Initialize a repository

```bash
mkdir demo-repo
cd demo-repo
git init
git status
```

Git creates repository metadata in the `.git` directory.

## 3. Create, stage, and commit a file

```bash
echo "# Demo Project" > README.md
git status
git add README.md
git status
git commit -m "Add project README"
```

A commit records the staged snapshot in local history.

## 4. Inspect changes

```bash
echo "Practice Git safely." >> README.md
git diff
git status
git diff --staged
```

`git diff` shows unstaged changes; `git diff --staged` shows changes already staged for the next commit.

## 5. Review history

```bash
git log --oneline
git show --stat
git show HEAD
```

Use `git show <commit-id>` to inspect a specific commit.

## 6. Create and switch branches

```bash
git switch -c docs-update
echo "Learning notes" > NOTES.md
git add NOTES.md
git commit -m "Add learning notes"
git switch main
```

If the repository's initial branch is named `master`, switch back to that branch instead of `main`.

## 7. Merge a branch

```bash
git switch main
git merge docs-update
git log --oneline --graph --all
```

Resolve any conflicts if Git reports them before completing the merge.

## 8. Add a remote

```bash
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git remote -v
```

Replace the URL with your own repository URL. If `origin` already exists, inspect it with `git remote -v` rather than adding it again.

## 9. Push and pull

```bash
git push -u origin main
git pull --ff-only origin main
```

The first push may require authentication and a remote repository that has a compatible history. If your branch is `master`, use `master` instead of `main`.

## 10. Use `.gitignore`

Create `.gitignore`:

```gitignore
.env
*.log
__pycache__/
.venv/
```

Then inspect and commit it:

```bash
git add .gitignore
git status
git commit -m "Add Git ignore rules"
```

If a secret has already been committed, adding it to `.gitignore` is not enough. Remove it from tracking and rotate the exposed secret; removing it from current tracking does not erase it from past commits.

## 11. Resolve a merge conflict

A conflict occurs when Git cannot automatically combine competing edits.

```bash
git status
```

Open the conflicted file and look for markers:

```text
<<<<<<< HEAD
current branch content
=======
incoming branch content
>>>>>>> other-branch
```

Edit the file to the desired final content, remove the markers, then:

```bash
git add conflicted-file.txt
git commit
```

If Git opened an editor for the merge message, save and close it to finish the commit.

## 12. Inspect a remote branch and SSH authentication

```bash
git branch -a
git remote -v
ssh -T git@github.com
```

The SSH test checks authentication with GitHub. A successful message does not provide shell access; it confirms the key was recognized.

## Official references

- Git book: https://git-scm.com/book/en/v2
- Git reference: https://git-scm.com/docs
- GitHub SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
