# 01 - Git Fundamentals

Learn the core Git workflow used to track changes, collaborate, and maintain a reliable project history.

## Learning objectives

By the end of this module, you should be able to:

- Explain repositories, commits, branches, remotes, and the working tree.
- Configure Git identity and initialize a repository.
- Stage, inspect, commit, and review changes.
- Create and switch branches.
- Connect a local repository to a remote such as GitHub.
- Push and pull changes safely.
- Resolve a simple merge conflict.
- Use `.gitignore` and avoid committing secrets.

## Prerequisites

- A terminal or command prompt.
- Git installed on your system.
- A GitHub account is helpful for the remote exercises, but not required for local practice.

Check installation:

```bash
git --version
```

## Folder contents

```text
01-Git-Fundamentals/
├── README.md
├── examples.md
├── practical.md
├── practical.ipynb
└── solutions.md
```

## Core topics

1. Git concepts and repository structure
2. Initial configuration
3. `git init`, `git status`, and `git add`
4. Commits and commit messages
5. Inspecting history with `git log` and `git diff`
6. Branching and merging
7. Remotes, push, and pull
8. `.gitignore` and secret hygiene
9. Merge-conflict resolution
10. Mini-project: version-control a small DevSecOps project

## Safe practice setup

Use a disposable practice directory. The commands below create and modify files only in that local directory.

```bash
mkdir git-practice
cd git-practice
git init
```

Set your identity if Git has not been configured yet:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Replace the example identity with your own. Do not use another person's identity.

## Safety and recovery notes

- Review `git status` and `git diff` before staging or committing.
- Never commit passwords, private keys, API tokens, or production `.env` files.
- `.gitignore` prevents untracked matching files from being added by normal `git add`; it does not remove a file that is already tracked.
- A commit is a local snapshot. It is not automatically uploaded to GitHub.
- Avoid force-pushing shared branches unless you understand the impact and have coordinated with collaborators.
- Before destructive commands, confirm which branch and repository you are in.

## Suggested learning path

1. Read `examples.md`.
2. Complete `practical.md` in a disposable directory.
3. Use `practical.ipynb` to record command outputs and answer TODO prompts.
4. Compare your results with `solutions.md`.

## Completion checklist

- [ ] Initialize a local repository.
- [ ] Stage and commit a file.
- [ ] Inspect status, differences, and history.
- [ ] Create a branch and merge it.
- [ ] Add a remote and understand push/pull.
- [ ] Resolve a simple merge conflict.
- [ ] Configure `.gitignore` and explain its limitations.
