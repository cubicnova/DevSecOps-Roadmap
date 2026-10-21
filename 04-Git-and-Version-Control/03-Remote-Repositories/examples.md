# Remote Repositories - Examples

Use a practice repository or a repository you are authorized to access. Replace placeholders such as `OWNER` and `REPOSITORY` with real values.

## 1. Clone a repository

HTTPS:

```bash
git clone https://github.com/OWNER/REPOSITORY.git
```

SSH:

```bash
git clone git@github.com:OWNER/REPOSITORY.git
```

Cloning creates a local repository and normally configures the cloned remote as `origin`.

## 2. List remotes

```bash
git remote
git remote -v
git remote show origin
```

`-v` displays fetch and push URLs.

## 3. Add a remote

```bash
git remote add origin https://github.com/OWNER/REPOSITORY.git
git remote -v
```

If `origin` already exists, do not add it again. Inspect it first.

## 4. Change a remote URL

```bash
git remote set-url origin git@github.com:OWNER/REPOSITORY.git
git remote -v
```

Use the intended HTTPS or SSH URL and verify the result.

## 5. Rename or remove a remote

```bash
git remote rename origin primary
git remote -v
git remote rename primary origin
```

To unlink a remote from the local repository:

```bash
git remote remove origin
```

Removing a remote does not delete the hosted repository; it removes the local remote configuration.

## 6. Fetch without integrating

```bash
git fetch origin
git branch -r
git log --oneline --graph --decorate --all
```

Fetching updates remote-tracking references but does not automatically merge the changes into your current branch.

## 7. Pull changes

```bash
git status
git pull --ff-only origin main
```

`--ff-only` makes the pull stop if it cannot be completed as a fast-forward. Use the branch name and integration strategy required by your project.

## 8. Push a local branch

```bash
git switch -c feature-docs
# Make and commit a change.
git push -u origin feature-docs
```

The `-u` option sets the upstream tracking branch for convenient future pushes and pulls.

## 9. Inspect upstream tracking

```bash
git branch -vv
git status -sb
```

Set an upstream for a branch that already exists on the remote:

```bash
git branch --set-upstream-to=origin/main main
```

Only run the last command if `origin/main` exists and `main` is the local branch you intend to track.

## 10. Work with a fork

For a fork-based workflow, `origin` often points to your fork and `upstream` points to the original repository:

```bash
git remote add upstream https://github.com/ORIGINAL-OWNER/REPOSITORY.git
git remote -v
git fetch upstream
```

To integrate upstream changes, review the project workflow before merging or rebasing.

## 11. Diagnose a rejected push

```bash
git status
git fetch origin
git log --oneline --graph --decorate --all
```

Review why the histories differ. If the remote contains commits you do not have, integrate them using the agreed merge or rebase workflow, test, then push again.

Avoid using `git push --force` as a generic fix. If rewriting a branch is explicitly approved, prefer `--force-with-lease` and understand its consequences first.

## 12. Check SSH authentication

```bash
ssh -T git@github.com
```

A successful response confirms GitHub recognized the SSH key. It does not provide general shell access.

## 13. Check the configured URL

```bash
git remote get-url origin
git config --get remote.origin.url
```

Do not share output publicly if your remote URL accidentally contains sensitive information. A normal GitHub URL should not embed credentials.

## References

- https://docs.github.com/en/get-started/git-basics/about-remote-repositories
- https://docs.github.com/en/get-started/git-basics/managing-remote-repositories
- https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository
