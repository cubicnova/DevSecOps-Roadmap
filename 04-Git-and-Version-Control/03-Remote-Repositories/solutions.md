# Remote Repositories - Reference Solutions

These examples assume you are working in a repository you own or are authorized to access. Replace placeholders and branch names as appropriate.

## Lab 1: Clone and inspect

```bash
git clone https://github.com/OWNER/REPOSITORY.git
cd REPOSITORY
git remote -v
git branch -vv
```

`origin` is a conventional remote name; it is not a special keyword.

## Lab 2: Add a remote

```bash
git init
echo "# Remote practice" > README.md
git add README.md
git commit -m "Add practice README"
git remote add origin https://github.com/OWNER/REPOSITORY.git
git remote -v
```

Use a remote repository that exists and that you can access.

## Lab 3: Change URL

```bash
git remote -v
git remote set-url origin git@github.com:OWNER/REPOSITORY.git
git remote -v
```

SSH requires an SSH key registered with GitHub. HTTPS uses an approved credential flow, such as Git Credential Manager or a personal access token when requested. Never put the token directly in the URL.

## Lab 4: Fetch vs pull

```bash
git fetch origin
git log --oneline --graph --decorate --all
git pull --ff-only origin main
```

Fetch downloads remote information without integrating it into the current branch. Pull fetches and then integrates the selected remote branch, according to the configured strategy.

## Lab 5: Push a feature branch

```bash
git switch -c feature-remote-practice
# Make a change.
git add README.md
git commit -m "Add remote workflow notes"
git push -u origin feature-remote-practice
git branch -vv
```

## Lab 6: Manage remotes

```bash
git remote add backup https://github.com/OWNER/OTHER-REPOSITORY.git
git remote -v
git remote rename backup secondary
git remote remove secondary
git remote -v
```

These commands change local remote configuration. They do not delete the hosted repository.

## Lab 7: Fork workflow

```bash
git clone git@github.com:YOUR-USERNAME/REPOSITORY.git
cd REPOSITORY
git remote add upstream https://github.com/ORIGINAL-OWNER/REPOSITORY.git
git remote -v
git fetch upstream
git branch -r
```

Usually, push your work to your fork (`origin`) and submit a pull request to the original repository.

## Lab 8: Non-fast-forward rejection

A safe high-level recovery sequence is:

```bash
git status
git fetch origin
git log --oneline --graph --decorate --all
git pull --ff-only origin main
```

If fast-forward integration is not possible, stop and inspect the graph. Follow the repository's merge or rebase policy, resolve conflicts, run tests, and then push. Do not overwrite remote work blindly.

## Lab 9: Authentication troubleshooting

For SSH:

```bash
git remote -v
ssh -T git@github.com
```

For HTTPS, inspect the URL and use your approved credential manager. Never share access tokens, passwords, or private-key contents.

## Reflection answers

1. A remote is a named URL configuration; a remote-tracking branch is a local reference to a branch state observed on that remote.
2. Fetch downloads updates, pull fetches and integrates updates, and push publishes local commits.
3. `origin` is simply the conventional default name used by many clone workflows; remotes can have other names.
4. `upstream` usually points to the original repository so a fork can fetch changes from it.
5. Force-push can rewrite remote branch history and remove commits from the visible branch tip. Coordinate first; if explicitly approved, `--force-with-lease` is safer than unconditional `--force` but still requires care.

## Official documentation

- https://docs.github.com/en/get-started/git-basics/about-remote-repositories
- https://docs.github.com/en/get-started/git-basics/managing-remote-repositories
- https://docs.github.com/en/get-started/using-git/getting-changes-from-a-remote-repository
