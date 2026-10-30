# Remote Repositories - Troubleshooting Guide

Use this guide to diagnose common Git remote problems. Inspect the repository and remote destination before changing configuration or history.

## 1. `fatal: remote origin already exists`

Inspect existing remotes:

```bash
git remote -v
```

If the existing remote is correct, keep it. If its URL is wrong, update it:

```bash
git remote set-url origin <CORRECT_URL>
```

Do not add a duplicate remote with the same name.

## 2. `fatal: 'origin' does not appear to be a git repository`

Check whether a remote is configured:

```bash
git remote -v
```

If none exists, add the intended repository URL:

```bash
git remote add origin <REPOSITORY_URL>
```

Confirm the URL is correct and that the repository exists.

## 3. `Permission denied (publickey)`

This usually indicates an SSH authentication or authorization problem.

```bash
git remote -v
ssh -T git@github.com
```

Check that the public key is added to the correct GitHub account, the private key is available to your SSH agent, and the remote uses the intended SSH URL. Never share your private key.

## 4. HTTPS authentication failed

GitHub does not accept account passwords for Git operations over HTTPS. Use an approved credential manager or a personal access token when prompted. Check that the token has the required access and has not expired or been revoked. Never put a token in source code or a remote URL.

## 5. `src refspec main does not match any`

Possible causes include:

- There is no local branch named `main`.
- No commit has been created yet.

Inspect:

```bash
git branch --show-current
git status
git log --oneline -n 3
```

Commit the intended files first and use the actual branch name.

## 6. `non-fast-forward` push rejection

The remote branch contains commits that are not included in your local branch.

```bash
git status
git fetch origin
git log --oneline --graph --decorate --all
```

Inspect the graph and integrate the remote work using the repository's merge or rebase policy. Resolve conflicts and test before pushing again. Do not use `--force` as a shortcut.

## 7. `unrelated histories`

This may happen when a local repository and remote repository were initialized independently.

Before integrating them, inspect both histories and confirm that you selected the intended remote. Back up important local work. Only use `--allow-unrelated-histories` when the two independent histories genuinely need to be combined and you understand the resulting merge.

## 8. Wrong remote URL

Inspect:

```bash
git remote -v
git remote get-url origin
```

Update only after confirming the destination:

```bash
git remote set-url origin <CORRECT_URL>
```

## 9. Pull reports local changes would be overwritten

Inspect the working tree:

```bash
git status
git diff
```

Commit the work or safely stash it before pulling. Do not discard changes unless you are certain they are no longer needed.

## 10. Quick diagnostic checklist

- [ ] Am I in the correct local repository?
- [ ] Is the remote URL correct?
- [ ] Does the remote repository exist?
- [ ] Do I have access to it?
- [ ] Is the URL HTTPS or SSH, and is the matching authentication configured?
- [ ] Does the local branch track the intended remote branch?
- [ ] Have I fetched and inspected remote commits before integrating?
- [ ] Is the working tree clean or safely backed up?
- [ ] Have I avoided exposing credentials in logs, screenshots, and command output?

## Official references

- https://docs.github.com/en/get-started/git-basics/managing-remote-repositories
- https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository
- https://git-scm.com/docs/git-remote
