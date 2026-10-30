# Pull Requests and Code Review — Exercises

Use a practice repository or a fork where you have permission to push. Do not experiment on protected production branches.

## Exercise 1 — Create a topic branch

Create `docs/pr-practice`, update a documentation file, commit the change, and push the branch.

**Deliverable:** the branch name, commit message, and a short explanation of the change.

## Exercise 2 — Write a pull request description

Use the template in `README.md` to describe your change. Include the problem, proposed solution, tests performed, and security implications.

**Review question:** Could a teammate understand why the change exists without asking you?

## Exercise 3 — Review a diff

Inspect each changed file in a practice PR. Identify:
- one correctness concern;
- one maintainability improvement;
- one missing test or edge case.

Write comments that refer to specific lines and explain the impact.

## Exercise 4 — Classify review feedback

For each comment, decide whether it is blocking, non-blocking, or a clarifying question:

1. "This branch can expose a token in logs."
2. "Could this variable have a more descriptive name?"
3. "Do we still support the previous configuration format?"
4. "The new function fails on an empty list, which is a supported input."

Explain each decision.

## Exercise 5 — Respond to a review

Make a follow-up commit that addresses a review comment. Push it to the same branch and explain how the PR reflects the update.

## Exercise 6 — Test evidence

Create a short validation section for a PR. Include successful tests, negative cases, and any checks that could not be run. Never claim a test passed if it was not run.

## Exercise 7 — Security review

Review a hypothetical change that:
- adds a dependency;
- updates a CI workflow;
- introduces a new log statement;
- processes user-supplied input.

Write at least one question or check for each area.

## Exercise 8 — Merge strategy discussion

Compare merge commit, squash merge, and rebase merge. Recommend one for a small documentation repository and explain the trade-offs. There is no universally correct answer; align with the team's history and review conventions.

## Mini-project — Simulated pull request

Prepare a small documentation or test improvement in a topic branch. Produce:
- a clear PR title and body;
- a list of files changed;
- validation evidence;
- three sample review comments;
- a response plan for each comment;
- a final merge-readiness checklist.
