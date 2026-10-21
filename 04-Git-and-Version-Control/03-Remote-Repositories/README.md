# 03 - Remote Repositories

Learn how local Git repositories communicate with remote repositories such as GitHub, how to synchronize branches, and how to troubleshoot common remote-workflow issues.

## Learning objectives

By completing this module, you should be able to:

- Explain local repositories, remotes, remote-tracking branches, and upstream branches.
- Clone a remote repository.
- Add, inspect, rename, and update remote URLs.
- Distinguish `fetch`, `pull`, and `push`.
- Work with `origin` and `upstream` remotes.
- Configure HTTPS or SSH authentication safely.
- Handle non-fast-forward rejections and synchronization conflicts.
- Diagnose common remote connection and permission errors.

## Module files

```text
03-Remote-Repositories/
├── README.md
├── examples.md
├── practical.md
├── solutions.md
└── troubleshooting.md
```

## Prerequisites

- Git installed (`git --version`).
- Basic knowledge of commits and branches.
- A GitHub account for the optional remote exercises.

## Key concepts

- **Remote:** a named URL for another Git repository.
- **`origin`:** the conventional name for the repository cloned from or first configured.
- **`upstream`:** often used for the original repository when working from a fork.
- **Remote-tracking branch:** a local reference to the last fetched state of a remote branch, such as `origin/main`.
- **Fetch:** downloads remote updates without merging them into the current branch.
- **Pull:** fetches and then integrates changes, commonly by merge or rebase depending on configuration.
- **Push:** publishes local commits to a remote repository.

## Quick start

```bash
git clone https://github.com/OWNER/REPOSITORY.git
cd REPOSITORY
git remote -v
git fetch origin
git branch -vv
```

Replace the example URL with the repository you are authorized to access.

## Recommended workflow

1. Check `git status` and commit or safely set aside local work.
2. Fetch remote updates.
3. Inspect incoming changes.
4. Integrate them with merge or rebase according to the project's workflow.
5. Run tests or review the result.
6. Push your branch to the intended remote.

## Security and safety

- Never put access tokens, passwords, or private keys in remote URLs, source files, or shell scripts.
- Use SSH keys or an approved credential manager for authentication.
- Confirm the destination with `git remote -v` before pushing.
- Do not force-push shared branches without authorization and coordination.
- Treat a rejected push as a signal to inspect history, not as a reason to overwrite remote work.
- Only access repositories you own or are authorized to use.

## Official references

- GitHub: About remote repositories — https://docs.github.com/en/get-started/git-basics/about-remote-repositories
- GitHub: Managing remote repositories — https://docs.github.com/en/get-started/git-basics/managing-remote-repositories
- GitHub: Getting changes from a remote repository — https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository
- Git remote reference — https://git-scm.com/docs/git-remote
