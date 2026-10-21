# Git Fundamentals - Practical Exercises

Use a new, disposable directory for these exercises. Do not experiment with destructive commands in a work repository.

## Lab 1: Verify installation

1. Run `git --version`.
2. Check `git config --get user.name`.
3. Check `git config --get user.email`.

If identity is missing, configure your own name and email.

## Lab 2: Initialize a repository

1. Create a directory named `git-lab`.
2. Run `git init`.
3. Run `git status`.
4. Explain what the `.git` directory stores at a high level.

## Lab 3: First commit

1. Create `README.md`.
2. Inspect `git status`.
3. Stage the file.
4. Inspect status again.
5. Commit with a clear message.
6. Review the commit with `git log --oneline`.

## Lab 4: Understand diff

1. Add another line to `README.md`.
2. Run `git diff`.
3. Stage the change.
4. Run `git diff --staged`.
5. Commit the change.

Explain the difference between unstaged and staged changes.

## Lab 5: Branching

1. Create a branch named `feature-notes`.
2. Add a `NOTES.md` file and commit it.
3. Switch back to your default branch.
4. Merge `feature-notes`.
5. Inspect the history graph.

## Lab 6: `.gitignore`

1. Create a `.env` file with a harmless placeholder such as `EXAMPLE_KEY=not-a-real-secret`.
2. Add `.env` to `.gitignore`.
3. Run `git status` and confirm the file is ignored.
4. Explain why ignore rules do not erase files already committed.

Do not place real secrets in the exercise file.

## Lab 7: Remote repository

1. Create an empty practice repository on GitHub.
2. Add it as `origin`.
3. Verify with `git remote -v`.
4. Push the branch.
5. Confirm the files appear on GitHub.

If using SSH, ensure the remote URL uses the SSH form and your key is configured.

## Lab 8: Simulate a merge conflict

1. Create and commit a file on the default branch.
2. Create a branch and edit the same line.
3. Switch back to the default branch and edit that same line differently.
4. Commit both branch changes separately.
5. Merge the feature branch and inspect the conflict.
6. Resolve the markers, stage the result, and complete the merge.

## Lab 9: Review and recovery

1. Use `git log --oneline --graph --all`.
2. Use `git show --stat`.
3. Run `git status`.
4. Explain why checking the current branch and working tree matters before running a destructive command.

## Lab 10: Mini-project - Version-control a DevSecOps utility

Create a small folder with:

```text
sample-tool/
├── README.md
├── app.py
├── tests/
│   └── test_app.py
└── .gitignore
```

Requirements:

- Initialize Git.
- Add an informative README.
- Add a simple Python function and a unit test.
- Ignore `__pycache__/`, `.venv/`, `.env`, and `*.log`.
- Make at least three meaningful commits.
- Create a feature branch, make a change, and merge it.
- Review the final commit history.
- Do not commit real credentials or private keys.

## Reflection questions

1. What is the difference between the working tree, staging area, and repository history?
2. Why use branches?
3. What does `git push` do compared with `git commit`?
4. Why is a good commit message useful?
5. What steps should you take if a secret is accidentally committed?
