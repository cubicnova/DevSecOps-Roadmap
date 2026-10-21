# 01 - Git Fundamentals

This module introduces the Git workflow used to track changes, collaborate, and maintain project history.

## Learning objectives

By completing this module, you will be able to:

- Explain repositories, commits, branches, remotes, and the staging area.
- Configure Git and initialize a local repository.
- Stage, inspect, commit, and review changes.
- Create branches and merge changes.
- Connect a local repository to GitHub using HTTPS or SSH.
- Resolve a basic merge conflict.
- Use `.gitignore` and handle secrets safely.

## Prerequisites

- A terminal or command prompt.
- Git installed (`git --version`).
- A GitHub account for the optional remote exercise.

## Files in this module

```text
01-Git-Fundamentals/
├── README.md
├── examples.md
├── practical.md
├── solutions.md
└── .gitignore.example
```

## Topics

1. Git concepts and repository lifecycle
2. Git identity and configuration
3. Initializing and cloning repositories
4. Staging, commits, and commit messages
5. `git status`, `git diff`, and `git log`
6. Branches and merges
7. Remotes, push, pull, and fetch
8. `.gitignore`
9. Merge-conflict resolution
10. Mini-project: version-control a small DevSecOps utility

## Quick start

Use a disposable practice directory:

```bash
mkdir git-practice
cd git-practice
git init
git status
```

Set your identity if it has not been configured:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use your own name and email. Git identity is recorded in commits; it is not a login credential.

## Safety checklist

- Inspect `git status` and `git diff` before staging or committing.
- Never commit passwords, private keys, access tokens, or production `.env` files.
- `.gitignore` does not untrack a file that is already committed.
- A commit is local history; `git push` sends commits to a remote.
- Avoid force-pushing shared branches unless you understand the impact and have coordinated with collaborators.
- Check your current repository and branch before running commands that discard or rewrite history.

## Recommended sequence

1. Read `examples.md`.
2. Complete `practical.md` in a disposable repository.
3. Use `solutions.md` to check your work after attempting each exercise.
4. Copy or adapt `.gitignore.example` when starting a suitable project.

## Completion checklist

- [ ] Initialize a repository and create a first commit.
- [ ] Inspect staged and unstaged changes.
- [ ] Create and merge a branch.
- [ ] Configure and inspect a remote.
- [ ] Resolve a simple merge conflict.
- [ ] Explain the limitations of `.gitignore`.
