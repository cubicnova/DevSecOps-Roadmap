# Secure Git Workflows — Suggested Solutions

Use these examples as starting points. Test workflow syntax and behavior in a non-production repository before adopting changes.

## Exercise 1 — Staged diff review

```bash
git status
git diff
git diff --cached
```

The staged diff shows what the next commit will contain. Review it to catch unintended files, credentials, generated artifacts, or unrelated edits before committing.

## Exercise 2 — `.gitignore` and example configuration

Example:

```gitignore
.env
.env.*
!.env.example
*.pem
*.key
secrets/
```

Example `.env.example` should use fake placeholders. If a sensitive file is already tracked, `.gitignore` alone will not untrack it. After verifying the path, use `git rm --cached <path>` and commit the change. If a real credential was exposed, rotate it regardless of whether it is later removed from Git.

## Exercise 3 — Least-privilege workflow

For a test workflow that only needs to read repository content:

```yaml
permissions:
  contents: read
```

Add permissions only for specific jobs that require them. A release-publishing job may need write permissions, but those permissions should be scoped to the job and protected by trusted triggers and appropriate approvals.

## Exercise 4 — Script injection

Use an environment variable and quote it:

```yaml
- name: Print PR title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    printf '%s\n' "$PR_TITLE"
```

Do not pass untrusted text into `eval`, construct shell commands from it, or interpolate it directly into a script body.

## Exercise 5 — Untrusted pull requests

Fork code can be attacker-controlled. A privileged workflow may have secrets, write-capable tokens, or access to trusted caches. Use an unprivileged `pull_request` workflow for testing. Separate privileged release or deployment work so it runs only after trusted review and from a trusted ref. Treat artifacts from untrusted workflows as untrusted input.

## Exercise 6 — Third-party Action review

A good record identifies the upstream repository, purpose, full verified commit SHA, permissions required, secret access, advisory review, and maintenance owner. Pinning reduces the risk of a tag being moved, but does not prove that the pinned code is safe; review the source and update process too.

## Exercise 7 — Secret incident response

1. Revoke or rotate the token immediately.
2. Identify permissions, systems, and data the token could access.
3. Notify the responsible owner or security team.
4. Review audit logs and activity for misuse.
5. Remove the secret from current files and replace it with a safe reference.
6. Decide whether history cleanup is required; coordinate any rewrite.
7. Check forks, caches, artifacts, logs, and other copies where relevant.
8. Add preventive controls such as secret scanning and push protection.

## Exercise 8 — Secure repository guardrails

- **Branch protection/rulesets:** prevent direct changes to important branches and require checks.
- **Required reviews:** ensure changes are reviewed before integration.
- **CODEOWNERS:** route sensitive file changes to responsible reviewers when enforced by rules.
- **Secret scanning/push protection:** help detect and prevent credential leaks.
- **Dependency alerts:** identify vulnerable dependencies and Actions where supported.
- **Signed commits:** provide cryptographic evidence about commit signatures.
- **Actions restrictions and minimal token permissions:** reduce risk from compromised or untrusted workflow code.

No single control is sufficient; combine controls according to the threat model.

## Mini-project — Example pipeline requirements

A reasonable design includes read-only permissions by default, a non-privileged test workflow for pull requests, no secrets in test jobs, pinned and reviewed Actions, code-owner review for `.github/workflows/`, and a separately protected release workflow. Validate the workflow with a parser and test it in a practice repository before enabling it for production.
