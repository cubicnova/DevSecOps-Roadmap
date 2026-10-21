# Secure Git Workflows — Exercises

Use fake credentials and a repository where you have permission to experiment. Do not test secret handling by committing real tokens.

## Exercise 1 — Staged diff review

Create a harmless file, stage it, and inspect `git diff --cached`. Explain why reviewing staged content is an important step before committing.

## Exercise 2 — `.gitignore` and example configuration

Create a `.gitignore` that excludes local `.env` files, private key files, and a `secrets/` directory while allowing `.env.example`. Write a sample `.env.example` containing placeholders only.

Check whether any ignored file is already tracked and explain how to stop tracking it without deleting the local copy.

## Exercise 3 — Least-privilege workflow

Review a sample workflow that has broad token permissions. Rewrite it so a test-only job has only the permissions it needs. Explain when extra write permissions would be justified.

## Exercise 4 — Script injection

Review this workflow step:

```yaml
- name: Print PR title
  run: echo "${{ github.event.pull_request.title }}"
```

Explain the risk and rewrite it to pass the title as data rather than injecting it into shell script source.

## Exercise 5 — Untrusted pull requests

Explain why a privileged workflow should not check out and execute code from an untrusted fork pull request while holding secrets or a write-capable token. Propose a safer separation of testing and privileged release tasks.

## Exercise 6 — Third-party Action review

Choose a fictional third-party Action and create a review record with its source, pinned commit SHA, required permissions, secret access, known advisories, and update owner. Do not invent a SHA; use a real, verified value only if you perform the research.

## Exercise 7 — Secret incident response

Write an incident checklist for an API token accidentally committed and pushed. Include revocation, scope analysis, log review, code/history cleanup, collaborator coordination, and prevention.

## Exercise 8 — Secure repository guardrails

Recommend a combination of branch protection, required reviews, CODEOWNERS, secret scanning, dependency alerts, signed commits, and Actions restrictions for a small team. Explain which risks each control addresses.

## Mini-project — Secure pull request pipeline

Create a proposed workflow design that:
- runs tests with read-only repository permissions;
- treats fork PR code as untrusted;
- avoids inline shell interpolation of event fields;
- pins third-party Actions to verified full commit SHAs;
- requires review for workflow changes;
- documents how secrets are stored and rotated.

Deliver a workflow draft, a threat checklist, and a short explanation of remaining risks.
