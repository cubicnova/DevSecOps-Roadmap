# Remote Repositories - Practical Exercises

Use a practice repository you own or are authorized to access. Avoid destructive commands on important branches.

## Lab 1: Clone and inspect

1. Clone a public practice repository or your own repository.
2. Run `git remote -v`.
3. Run `git branch -vv`.
4. Explain what `origin` means in this repository.

## Lab 2: Add and verify a remote

1. Initialize a local practice repository and create a commit.
2. Create an empty remote repository on GitHub.
3. Add the remote using `git remote add origin <URL>`.
4. Verify the URL with `git remote -v`.

## Lab 3: Switch remote URL formats

1. Inspect the current remote URL.
2. Change from HTTPS to SSH or SSH to HTTPS using `git remote set-url`.
3. Verify the result.
4. Explain what authentication configuration the selected URL requires.

## Lab 4: Fetch vs pull

1. Make a small change on the remote repository using the GitHub interface.
2. Run `git fetch origin`.
3. Inspect the graph and remote-tracking branch.
4. Integrate the update using the workflow chosen for the practice repository.
5. Explain the difference between fetch and pull.

## Lab 5: Push a feature branch

1. Create a branch named `feature-remote-practice`.
2. Make a small documentation change and commit it.
3. Push it with `git push -u origin feature-remote-practice`.
4. Confirm the branch exists on GitHub.
5. Inspect `git branch -vv`.

## Lab 6: Manage remotes

1. Add a second remote with a distinct name to a repository you control.
2. List remotes.
3. Rename the second remote.
4. Remove that remote configuration.
5. Confirm that removing the local remote does not delete the hosted repository.

## Lab 7: Fork workflow

1. Fork a repository you are permitted to use.
2. Clone your fork.
3. Confirm `origin` points to your fork.
4. Add the original repository as `upstream`.
5. Fetch from upstream and inspect its branches.

Do not push to the original repository unless you have permission.

## Lab 8: Recover from a non-fast-forward rejection

In a disposable repository, create a situation where the remote has a commit that the local branch does not have. Attempt a push and observe the rejection.

Then:

1. Inspect `git status`.
2. Fetch the remote.
3. Inspect the commit graph.
4. Integrate the remote changes using the agreed workflow.
5. Resolve conflicts if necessary.
6. Test and push again.

Do not use force-push to bypass the exercise.

## Lab 9: Authentication troubleshooting

1. Check whether your remote uses HTTPS or SSH.
2. For SSH, run `ssh -T git@github.com`.
3. For HTTPS, check your approved credential manager or token configuration.
4. Write down the error category without recording or sharing credentials.

## Lab 10: Mini-project - Remote collaboration simulation

Using a repository you control:

- Configure `origin`.
- Create and push a feature branch.
- Make a separate commit on the remote default branch.
- Fetch and inspect the new commit.
- Integrate the changes into your local branch.
- Resolve a conflict if one occurs.
- Push the completed feature branch.
- Document the final remotes, branches, and commit graph.

## Reflection questions

1. What is the difference between a remote and a remote-tracking branch?
2. How are `fetch`, `pull`, and `push` different?
3. Why is `origin` not a special Git keyword?
4. What is the purpose of an `upstream` remote in a fork workflow?
5. Why is force-push risky on a shared branch?
