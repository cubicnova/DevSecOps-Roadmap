# Git Fundamentals - Practical Exercises

Use a new, disposable directory for these labs. Do not experiment with history-rewriting or destructive commands in an important repository.

## Lab 1: Verify Git

1. Run `git --version`.
2. Check your configured name and email.
3. Configure your own identity if needed.

## Lab 2: Create a repository

1. Create a directory named `git-lab`.
2. Run `git init`.
3. Run `git status`.
4. Explain what the `.git` directory stores.

## Lab 3: Make your first commit

1. Create `README.md`.
2. Inspect `git status`.
3. Stage the file with `git add`.
4. Inspect status again.
5. Commit with a clear message.
6. Review the commit with `git log --oneline`.

## Lab 4: Compare staged and unstaged changes

1. Modify `README.md`.
2. Run `git diff`.
3. Stage the change.
4. Run `git diff --staged`.
5. Commit the change.

Explain the difference between the two diff commands.

## Lab 5: Branch and merge

1. Create a branch named `feature-notes`.
2. Add `NOTES.md` and commit it.
3. Switch back to your default branch.
4. Merge `feature-notes`.
5. Inspect history using `git log --oneline --graph --all`.

## Lab 6: Configure ignore rules

1. Copy relevant patterns from `.gitignore.example` into a `.gitignore` file in your practice project.
2. Create a harmless `.env` placeholder such as `EXAMPLE_KEY=not-a-real-secret`.
3. Confirm that Git ignores the file.
4. Explain why ignore rules do not erase files already committed.

Never use a real secret in this lab.

## Lab 7: Connect to GitHub

1. Create an empty practice repository on GitHub.
2. Add it as `origin`.
3. Verify it with `git remote -v`.
4. Push your default branch.
5. Confirm the files appear on GitHub.

You may use HTTPS or SSH. Do not paste access tokens into source files or command history.

## Lab 8: Resolve a merge conflict

1. Commit a file containing a single line on the default branch.
2. Create a feature branch and change that same line.
3. Switch back to the default branch and change the line differently.
4. Commit both edits on their respective branches.
5. Merge the feature branch and inspect the conflict.
6. Edit the file to the desired final content, remove conflict markers, stage it, and complete the merge.

## Lab 9: Review history and status

1. Run `git status`.
2. Run `git log --oneline --graph --all`.
3. Run `git show --stat`.
4. Explain why checking the branch and working tree matters before running commands that discard changes.

## Lab 10: Mini-project - Version-control a DevSecOps utility

Create this structure:

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
- Add a useful README.
- Add a simple Python function and a unit test.
- Ignore `.env`, `.venv/`, `__pycache__/`, and `*.log`.
- Make at least three meaningful commits.
- Create a feature branch, make a change, and merge it.
- Review the final history.
- Do not commit credentials, private keys, or production data.

## Reflection questions

1. What are the working tree, staging area, and repository history?
2. Why are branches useful?
3. What is the difference between `git commit` and `git push`?
4. What makes a commit message useful?
5. What should you do if a secret is accidentally committed?
