# Git Fundamentals - Examples

Run these commands in a disposable practice directory unless a step explicitly says otherwise.

## 1. Check Git and configuration

```bash
git --version
git config --get user.name
git config --get user.email
```

Configure your identity if required:

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

## 3. Stage and commit a file

```bash
echo "# Demo Project" > README.md
git status
git add README.md
git status
git commit -m "Add project README"
```

## 4. Inspect changes

```bash
echo "Practice Git safely." >> README.md
git diff
git add README.md
git diff --staged
git commit -m "Expand project README"
```

`git diff` normally shows unstaged changes. `git diff --staged` shows staged changes prepared for the next commit.

## 5. Review commit history

```bash
git log --oneline
git log --oneline --graph --all
git show --stat
```

## 6. Create a branch and merge it

```bash
git switch -c docs-update
echo "Learning notes" > NOTES.md
git add NOTES.md
git commit -m "Add learning notes"
git switch main
git merge docs-update
```

If your default branch is named `master` or something else, switch back to that branch instead of `main`.

## 7. Inspect remotes

```bash
git remote -v
git remote add origin git@github.com:USERNAME/REPOSITORY.git
git remote -v
```

Replace the example URL with your own repository URL. If `origin` already exists, inspect it before changing anything.

## 8. Push and pull

```bash
git push -u origin main
git pull --ff-only origin main
```

Use the correct branch name for your repository. Authentication must be configured, and the local and remote histories must be compatible.

## 9. Use ignore rules

The file `.gitignore.example` in this module provides common patterns for virtual environments, logs, local environment files, and generated Python files. Copy suitable rules into a project's `.gitignore`; do not blindly ignore files your project needs.

Important: adding a tracked secret to `.gitignore` does not remove it from Git history. Revoke or rotate the secret immediately and follow the repository's cleanup procedure.

## 10. Resolve a merge conflict

After Git reports a conflict:

```bash
git status
```

Open the conflicted file. It may contain markers like:

```text
<<<<<<< HEAD
content from the current branch
=======
content from the incoming branch
>>>>>>> feature-branch
```

Edit the file to the intended final content, remove the markers, then run:

```bash
git add conflicted-file.txt
git commit
```

Run tests or inspect the file before completing the merge.

## 11. Rename a branch

```bash
git branch --show-current
git branch -m new-branch-name
```

If the branch has already been published, coordinate with collaborators before changing the remote branch.

## 12. Inspect SSH authentication

```bash
ssh -T git@github.com
```

A successful GitHub SSH authentication message confirms that GitHub recognized the key; it does not provide general shell access.

## References

- Pro Git book: https://git-scm.com/book/en/v2
- Git command reference: https://git-scm.com/docs
- GitHub remote repositories: https://docs.github.com/en/get-started/git-basics/managing-remote-repositories
