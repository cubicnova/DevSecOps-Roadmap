# Git Hooks — Examples

## 1. Inspect the default hooks directory

```bash
git rev-parse --git-path hooks
ls -la "$(git rev-parse --git-path hooks)"
git config --show-origin --get core.hooksPath
```

The final command may print nothing if no custom hooks path is configured.

## 2. Pre-commit whitespace check

Save as `.git/hooks/pre-commit`:

```sh
#!/bin/sh
set -eu
git diff --cached --check
```

Enable it on Linux/macOS/Git Bash:

```bash
chmod +x .git/hooks/pre-commit
```

## 3. Commit-message convention

Save as `.git/hooks/commit-msg`:

```sh
#!/bin/sh
set -eu
message_file="$1"
first_line=$(sed -n '1p' "$message_file")

case "$first_line" in
  feat:*|fix:*|docs:*|test:*|chore:*) exit 0 ;;
  *) echo "Use feat:, fix:, docs:, test:, or chore:." >&2; exit 1 ;;
esac
```

Try:
- `docs: explain git hooks` — expected to pass.
- `updated the docs` — expected to be rejected.

## 4. Shared hooks directory

```bash
mkdir -p .githooks
# Add reviewed hook scripts to .githooks/
git config core.hooksPath .githooks
git config --show-origin --get core.hooksPath
```

The scripts should be committed with the repository. Team members must configure the path when cloning unless the team uses a documented bootstrap process. Be careful: a local `core.hooksPath` setting may already exist.

## 5. Pre-push smoke test

Save as `.git/hooks/pre-push`:

```sh
#!/bin/sh
set -eu
echo "Running quick checks before push..."
# Replace this with your project's actual test command.
# Example: npm test
exit 0
```

A real project should replace the placeholder with a reliable, appropriately scoped test command. Do not leave a false-success stub in a production repository.

## 6. Server-side validation concept

A `pre-receive` hook runs on the receiving Git server before refs are updated. It can reject the receive operation by exiting non-zero. This differs from `pre-push`, which runs on the contributor's client before the push is sent. Server-side hook installation depends on the hosting platform and its permissions model. <Cite refs={["turn499779search0"]}/>
