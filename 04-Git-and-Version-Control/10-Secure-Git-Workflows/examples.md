# Secure Git Workflows — Examples

Use a practice repository and fake credentials only. Never paste real secrets into examples, terminal output, or commits.

## 1. Inspect what will be committed

```bash
git status
git diff
git diff --cached
```

Review staged changes before committing. If an unintended file is staged:

```bash
git restore --staged path/to/file
```

This removes it from the index but keeps the working copy.

## 2. Ignore local secret files

Example `.gitignore`:

```gitignore
.env
.env.*
!.env.example
*.pem
*.key
secrets/
```

Check whether a file is already tracked:

```bash
git ls-files .env
```

If it is already tracked, adding it to `.gitignore` does not untrack it. After confirming the file should no longer be tracked:

```bash
git rm --cached .env
git commit -m "Stop tracking local environment file"
```

This does not remove prior versions from history and does not revoke exposed credentials.

## 3. Safe example configuration

`.env.example`:

```dotenv
APP_ENV=development
API_BASE_URL=https://api.example.invalid
API_TOKEN=replace-with-a-local-test-token
```

Use clearly fake placeholders and document how developers obtain real credentials through approved channels.

## 4. Minimal GitHub Actions permissions

For a workflow that only reads code and runs tests:

```yaml
name: Test

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<VERIFIED_FULL_COMMIT_SHA>
      - name: Run tests
        run: echo "Replace with your test command"
```

Replace `<VERIFIED_FULL_COMMIT_SHA>` with a verified full-length commit SHA for the intended `actions/checkout` release. The placeholder is not valid workflow syntax as-is. Validate the final YAML before use.

## 5. Avoid shell interpolation of untrusted input

**Risky pattern:**

```yaml
- name: Check title
  run: echo "${{ github.event.pull_request.title }}"
```

The title is untrusted input and is inserted into shell script text.

**Safer pattern:**

```yaml
- name: Check title
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    printf '%s\n' "$PR_TITLE"
```

Treat the value as data. Quoting helps prevent word splitting, but commands that evaluate data as code must still be avoided.

## 6. Use CODEOWNERS for sensitive files

Example `.github/CODEOWNERS`:

```text
/.github/workflows/ @your-org/security-reviewers
/CODEOWNERS          @your-org/repository-maintainers
```

Replace the example team handles with real teams in your organization. Combine CODEOWNERS with branch rules requiring code-owner review; the file alone does not enforce approval.

## 7. Secret exposure response

If a fake test token was committed, rehearse the process:

1. Revoke or rotate the credential.
2. Search for uses and assess access.
3. Remove the value from the current code.
4. Check secret-scanning alerts and logs.
5. Determine whether history cleanup is required.
6. Coordinate any history rewrite with collaborators.

Do not rely on history rewriting as a substitute for credential rotation.

## 8. Review third-party Actions

For each Action, record:
- source repository and maintainer;
- purpose and permissions required;
- full commit SHA or other approved immutable reference;
- security advisories and update process;
- whether it can access secrets or modify the repository.
