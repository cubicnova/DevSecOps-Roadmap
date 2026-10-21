# 09 — Git Hooks

Git hooks are scripts that Git runs at specific points in its workflow. They can automate checks, enforce local conventions, and trigger helpful actions before or after operations such as commits, checkouts, and pushes.

## Learning objectives

- Explain how Git hooks work and where they are stored.
- Distinguish common client-side and server-side hooks.
- Create and test a `pre-commit` or `commit-msg` hook.
- Use `core.hooksPath` to configure a shared hooks directory.
- Understand limitations of local hooks and why CI/server-side enforcement still matters.

## How hooks work

By default, Git looks for hooks in `$GIT_DIR/hooks` (usually `.git/hooks`). Sample hooks often end in `.sample` and do not run until configured as executable hook files without that suffix. The hooks directory can be changed with `git config core.hooksPath`.

A hook generally signals success by exiting with status `0`. A non-zero exit status can stop the operation for hooks designed to validate or reject it. Behavior depends on the hook event. <Cite refs={["turn499779search0"]}/>

## Common hooks

| Hook | When it runs | Common use |
|---|---|---|
| `pre-commit` | Before a commit is created | Run linting, tests, whitespace checks |
| `prepare-commit-msg` | Before the commit message editor | Prepare or modify a default message |
| `commit-msg` | After the message is prepared | Validate commit-message format |
| `post-commit` | After a commit is created | Local notifications or reporting |
| `pre-push` | Before a push is sent | Run quick tests or checks |
| `post-checkout` | After checkout/switch updates the worktree | Refresh local development setup |
| `post-merge` | After a successful merge | Update local generated state |
| `pre-receive` | On a receiving server before refs are updated | Server-side push policy |
| `update` | On a receiving server for each ref update | Validate an individual ref update |
| `post-receive` | On a receiving server after refs update | Notifications and deployment triggers |

The exact hook contract and arguments vary. Check the official Git hooks documentation before relying on a hook's inputs or behavior. <Cite refs={["turn499779search0"]}/>

## Create a simple pre-commit hook

From the root of a repository on Linux, macOS, or Git Bash:

```bash
mkdir -p .git/hooks
cat > .git/hooks/pre-commit <<'EOF'
#!/bin/sh
set -eu

if git diff --cached --check; then
  echo "Pre-commit checks passed."
else
  echo "Pre-commit checks failed: fix whitespace errors before committing." >&2
  exit 1
fi
EOF

chmod +x .git/hooks/pre-commit
```

Test it by staging a change and committing. `git diff --cached --check` checks the staged diff for whitespace errors. If the hook rejects the commit, fix the issue, stage the correction, and retry.

> This example assumes a Unix-like shell. Windows users can use Git Bash or adapt the script to their environment.

## Create a commit-message hook

This example requires a commit message to start with a conventional type such as `feat:`, `fix:`, `docs:`, `test:`, or `chore:`.

Create `.git/hooks/commit-msg`:

```sh
#!/bin/sh
set -eu

message_file="$1"
first_line=$(sed -n '1p' "$message_file")

case "$first_line" in
  feat:*|fix:*|docs:*|test:*|chore:*)
    exit 0
    ;;
  *)
    echo "Commit message must start with feat:, fix:, docs:, test:, or chore:." >&2
    exit 1
    ;;
esac
```

Make it executable:

```bash
chmod +x .git/hooks/commit-msg
```

Example valid message: `docs: add git hooks guide`

## Share hooks with a project

Files inside `.git/hooks` are local repository metadata and normally are not committed. To share hooks, store them in a tracked directory, for example `.githooks/`, and configure each clone:

```bash
git config core.hooksPath .githooks
```

Make sure scripts in `.githooks/` are executable on platforms that support executable bits. Document the setup step in the repository README or onboarding guide.

Do not silently replace an existing team-wide `core.hooksPath` configuration. Check the current value first:

```bash
git config --show-origin --get core.hooksPath
```

## Security and reliability guidance

- Treat hooks as executable code: review changes before running them.
- Keep checks fast enough for the event where they run.
- Do not put credentials or secret values inside hook scripts.
- Avoid destructive commands and unexpected network calls.
- Hooks can be bypassed in some situations, and local hooks are not automatically installed for every clone.
- Enforce critical policies in CI and on the server as appropriate; do not rely only on a contributor's local hook.
- Provide clear failure messages and a documented remediation path.

## Troubleshooting

- **Hook does not run:** Check filename, location, executable permission, line endings, and `core.hooksPath`.
- **Permission denied:** On Unix-like systems, run `chmod +x .git/hooks/pre-commit`.
- **Hook runs from the wrong directory:** Git normally changes to the working-tree root for hooks in a non-bare repository; push-related server hooks run in the Git directory.
- **A hook blocks a commit:** Read the message, fix the staged changes or message, and retry.
- **Hook works on one machine only:** Confirm the hook is installed and dependencies are available on each machine.
- **Need enforcement across contributors:** Add required CI checks and suitable server-side controls.

## Exercises

1. Create a `pre-commit` hook that checks the staged diff.
2. Create a `commit-msg` hook for a message convention.
3. Explain why a local hook is not sufficient for organization-wide policy.
4. Configure a tracked `.githooks/` directory.
5. Describe the difference between `pre-push` and server-side `pre-receive`.

## References

- [Git Hooks — Git documentation](https://git-scm.com/docs/githooks)
- [git hook command — Git documentation](https://git-scm.com/docs/git-hook)
- [pre-commit-hooks project](https://github.com/pre-commit/pre-commit-hooks)
