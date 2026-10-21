# Secure Git Workflows

Secure Git workflows combine safe source-control practices with review, automation, and access controls to reduce the risk of leaked secrets, unauthorized changes, and software supply-chain compromise.

This module focuses on practical safeguards for everyday Git and GitHub workflows.

## Learning objectives

- Keep credentials and sensitive files out of commits.
- Use focused branches, pull requests, and protected branches.
- Apply least privilege to GitHub Actions token permissions.
- Recognize risks from untrusted pull request code and workflow injection.
- Pin third-party Actions to immutable commit SHAs where practical.
- Use secret scanning, dependency checks, and signed commits as defense-in-depth.
- Respond safely when a secret or key is accidentally committed.

## Secure workflow principles

1. **Least privilege:** users, tokens, workflows, and deploy credentials should receive only the access they need.
2. **Review before integration:** protect important branches with pull requests, required reviews, and status checks.
3. **No secrets in Git:** store credentials in an approved secret manager or GitHub Secrets, not in source files or example configs.
4. **Treat external contributions as untrusted:** pull request titles, branch names, issue text, artifacts, and code may contain attacker-controlled input.
5. **Pin and review automation dependencies:** use trusted Actions and pin them to full commit SHAs when possible.
6. **Verify changes:** run tests, linters, secret scanning, and relevant security checks before merging.
7. **Prepare for incidents:** rotate exposed credentials and remove sensitive material from current and historical Git data when required.

## Example secure development workflow

```bash
git status
git switch main
git pull --ff-only
git switch -c feature/secure-config

# Make a focused change.
git diff
git status
git add path/to/intended-file
git diff --cached
git commit -m "Validate secure configuration"

git push -u origin feature/secure-config
```

Open a pull request, review the diff, wait for required checks and approvals, then merge according to repository policy. Avoid broad staging commands when unreviewed or sensitive files might be present.

## Protect secrets

Before committing, inspect staged changes:

```bash
git status
git diff --cached
```

Use `.gitignore` for local secret files and generated output, but remember that `.gitignore` does not remove files already tracked by Git.

Example `.gitignore` entries:

```gitignore
.env
.env.*
!.env.example
*.pem
*.key
secrets/
```

Adapt these patterns to your project. Some projects legitimately track test certificates or fixtures; review every ignored or included file rather than relying on patterns blindly. `.env.example` should contain placeholders, never real credentials.

If a secret is committed or pushed, treat it as exposed:
1. Revoke or rotate it immediately.
2. Identify systems and permissions that the credential could access.
3. Review logs and activity for misuse.
4. Remove the secret from the current tree and, if needed, rewrite history using a documented process.
5. Coordinate history rewriting with collaborators; changing history alone does not invalidate the credential.

## Secure GitHub Actions workflows

Set the smallest practical `GITHUB_TOKEN` permissions. For a workflow that only reads repository content and runs tests:

```yaml
permissions:
  contents: read
```

Grant additional permissions only to jobs that need them. For example, publishing a release may require write access, which should be scoped and protected.

### Avoid script injection

Do not interpolate untrusted event fields directly into shell script source. Prefer passing values through environment variables and quote them carefully:

```yaml
- name: Check pull request title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    printf 'Checking title: %s\n' "$PR_TITLE"
```

Treat the value as data. Avoid constructs that evaluate it as shell code.

### Protect privileged workflow triggers

Be cautious with `pull_request_target` and `workflow_run`, especially when handling fork pull requests or artifacts produced by untrusted code. Do not check out and execute untrusted pull request code in a privileged workflow that can access secrets or write tokens. Use unprivileged workflows for testing untrusted contributions and separate privileged tasks.

### Pin third-party Actions

A tag such as `@v3` can potentially move. Pinning an Action to a verified full-length commit SHA makes the reference immutable. Confirm the SHA belongs to the intended upstream repository and periodically review dependencies for updates and security advisories.

## Repository guardrails

Consider enabling, where available and appropriate:

- Protected branches or rulesets.
- Required pull request reviews and status checks.
- CODEOWNERS review for workflow and security-sensitive files.
- Secret scanning and push protection.
- Dependency graph, Dependabot alerts, and dependency updates.
- Code scanning and workflow security analysis.
- Signed commits or tags where required by policy.
- Restricted Actions sources and minimal workflow permissions.

Feature availability can vary by repository visibility, organization policy, and GitHub plan.

## Incident response: accidental secret commit

```text
1. Revoke or rotate the exposed credential first.
2. Determine scope, permissions, and possible misuse.
3. Notify the responsible owner or security team.
4. Remove the secret from the current code and replace it with a safe reference.
5. Decide whether history cleanup is required.
6. Coordinate force-push/history rewrite if approved.
7. Verify scanning, logs, and downstream copies.
8. Document the cause and preventive action.
```

Deleting a secret from the latest commit is not sufficient if the credential remains valid or the secret exists in Git history, forks, caches, logs, or clones.

## Exercises

1. Review a staged diff and identify accidentally included secrets.
2. Create a safe `.env.example` and an appropriate `.gitignore`.
3. Harden a basic GitHub Actions workflow with minimal permissions.
4. Rewrite an unsafe workflow snippet to avoid shell injection.
5. Explain the risk of executing fork pull request code in a privileged workflow.
6. Create a checklist for pinning and reviewing third-party Actions.
7. Draft a response plan for an exposed API token.
8. Design a secure pull-request workflow for a small DevSecOps project.

## References

- [GitHub Actions: Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [GitHub: Secure repository quickstart](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository)
- [GitHub: About commit signature verification](https://docs.github.com/en/authentication/managing-commit-signature-verification/about-commit-signature-verification)
- [Git documentation](https://git-scm.com/docs)
