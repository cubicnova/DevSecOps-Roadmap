# Git Hooks Troubleshooting

## Hook does not run

1. Confirm the hook is named exactly for its event, for example `pre-commit`.
2. Find the configured hooks directory:

   ```bash
   git rev-parse --git-path hooks
   git config --show-origin --get core.hooksPath
   ```

3. Confirm the script has execute permission on Unix-like systems:

   ```bash
   chmod +x .git/hooks/pre-commit
   ```

4. Confirm the first line has a valid interpreter, such as `#!/bin/sh`.
5. Check line endings and ensure required tools are installed.

## Hook rejects an operation

Read the error message and determine which staged file, message, test, or policy caused the failure. Correct the issue and retry. Avoid using bypass options to evade team policy.

## Hook runs locally but not for teammates

Hooks in `.git/hooks` are local and normally are not committed. Use a tracked directory such as `.githooks/`, document `git config core.hooksPath .githooks`, and consider a controlled setup script or hook manager.

## Local and server-side enforcement

Local hooks improve developer feedback, but they are not a security boundary. Use CI and hosting-platform protections for mandatory checks. Server-side hooks such as `pre-receive` and `update` are configured by the Git server administrator or hosting provider and are not generally installed by an ordinary clone.

## Safety checklist

- [ ] Review hook scripts like any other executable code.
- [ ] Avoid embedding credentials or tokens.
- [ ] Avoid destructive actions and unexplained network access.
- [ ] Keep error messages actionable.
- [ ] Keep commit-time checks quick.
- [ ] Run comprehensive tests in CI.
