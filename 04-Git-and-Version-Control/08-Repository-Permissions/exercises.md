# Repository Permissions — Exercises

Use hypothetical users or a test repository. Do not change production permissions without authorization.

## Exercise 1 — Map roles to responsibilities

Assign the lowest suitable role for each person:

1. A reader who only needs to inspect documentation.
2. A community manager who labels issues and organizes pull requests.
3. A developer who pushes feature branches.
4. A project maintainer who manages routine repository tasks.
5. A repository owner who controls access and security settings.

Explain each choice and note any assumptions.

## Exercise 2 — Build an access inventory

Create a Markdown table with columns for person/team, direct or inherited access, current role, required task, proposed role, owner, and review date.

Use fictional identities. Identify any role that appears excessive.

## Exercise 3 — Repository role comparison

Explain the difference between Read, Triage, Write, Maintain, and Admin. Include one example task for each role and one task that should not be granted at that level.

## Exercise 4 — Direct versus team access

A developer has Write access through a parent team and Read access directly. Explain why removing the direct collaborator entry may not remove the developer's effective access.

## Exercise 5 — Access removal

Draft an offboarding checklist for a contractor whose project work has ended. Include repository access, team membership, tokens, deploy keys, secrets, and ownership of open work.

## Exercise 6 — Branch protection

A contributor has Write access and can push feature branches. Explain how branch protection or repository rules can still require pull requests, reviews, and status checks before changes reach a protected branch.

## Exercise 7 — GitHub Actions permissions

Review this workflow permission block:

```yaml
permissions: write-all
```

Explain why broad permissions increase risk and propose a narrower permission block for a workflow that only checks out source and runs tests.

## Exercise 8 — Access audit

Create a quarterly review checklist that covers:
- inactive collaborators;
- direct and inherited team access;
- administrator count;
- organization base permissions;
- deploy keys and tokens;
- Actions workflow permissions;
- documented owners and review dates.

## Mini-project — Least-privilege repository plan

Design an access model for a fictional software project with maintainers, developers, issue triagers, external reviewers, and CI automation. Deliver:
- a role matrix;
- an access-review process;
- an offboarding checklist;
- branch protection recommendations;
- a short risk assessment.
