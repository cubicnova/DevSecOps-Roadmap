# Solutions — Git Hooks

These are sample solutions; adapt commands and policy to the repository's operating system and workflow.

## Exercise 1 — Check staged changes

A minimal `.git/hooks/pre-commit`:

```sh
#!/bin/sh
set -eu
git diff --cached --check
```

Make it executable on Unix-like systems:

```bash
chmod +x .git/hooks/pre-commit
```

The command checks the staged diff, not every unstaged change in the working tree.

## Exercise 2 — Enforce a commit-message convention

A `commit-msg` hook receives the path to the proposed message file as its first argument. It can inspect the first line and exit non-zero when the message does not match the project's rule. See `examples.md` for a working sample.

## Exercise 3 — Why local hooks are not enough

Local hooks may not be installed automatically, may differ between machines, and can be bypassed in some workflows. Use CI for repeatable checks and server-side protections for policies that must be enforced for every accepted update.

## Exercise 4 — Configure tracked hooks

```bash
mkdir -p .githooks
# Place reviewed executable hook scripts in this directory.
git config core.hooksPath .githooks
git add .githooks
git commit -m "chore: add shared git hooks"
```

Document the setup command for new clones. Check whether an existing hooks path is configured before changing it.

## Exercise 5 — `pre-push` versus `pre-receive`

- `pre-push` runs on the contributor's machine before the client sends the push. It can stop that local push.
- `pre-receive` runs on the receiving server before refs are updated. A non-zero exit rejects the receive operation.
- Availability and configuration of server-side hooks depend on the Git server or hosting provider.

## Troubleshooting table

| Symptom | Likely cause | Resolution |
|---|---|---|
| Hook is ignored | Wrong name/location or not executable | Check hook filename, hooks path, and permissions |
| `bad interpreter` | Line endings or missing shell | Use Unix LF endings and a valid shebang |
| Works only on one computer | Hook not installed/configured elsewhere | Document setup or use a managed hook framework |
| Commit rejected | Validation failed | Fix staged files or commit message and retry |
| `core.hooksPath` points elsewhere | Custom configuration | Inspect with `git config --show-origin --get core.hooksPath` |
| Hook is too slow | Too much work at commit time | Keep local checks fast; run broader tests in CI |

## Suggested evaluation rubric

- 2 points: explains hook lifecycle and location.
- 2 points: creates a working pre-commit hook.
- 2 points: creates a commit-message validation hook.
- 2 points: configures and documents shared hooks.
- 2 points: explains local-hook limitations and CI/server-side enforcement.

Total: 10 points.
