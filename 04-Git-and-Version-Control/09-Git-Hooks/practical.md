# Practical Lab — Build and Test Git Hooks

## Goal

Create local hooks that validate staged changes and commit-message formatting.

## Prerequisites

- A Git repository you own or can safely modify.
- Git installed and available from the terminal.
- Linux, macOS, or Git Bash for the shell examples below.

## Lab A — Inspect the repository

Run:

```bash
git status
git rev-parse --git-path hooks
git config --show-origin --get core.hooksPath
```

Record the hooks directory and whether a custom hooks path is configured.

## Lab B — Install a pre-commit check

Create `.git/hooks/pre-commit`:

```sh
#!/bin/sh
set -eu
git diff --cached --check
```

Then:

```bash
chmod +x .git/hooks/pre-commit
```

Make and stage a small edit. Commit it. Verify that a clean staged diff passes. In a throwaway file or test repository, introduce trailing whitespace and verify the hook rejects the commit.

## Lab C — Validate commit messages

Create `.git/hooks/commit-msg` using the example in `examples.md`. Make a valid commit and then try an invalid message in a safe test branch. Confirm the invalid message is rejected and that the error explains how to fix it.

## Lab D — Share hooks

1. Create a tracked `.githooks/` directory.
2. Move or copy your reviewed hook scripts into it.
3. Configure the repository:

   ```bash
   git config core.hooksPath .githooks
   ```

4. Confirm the setting and commit the tracked hook files.
5. Document how another contributor should enable the hooks after cloning.

Do not overwrite an existing hooks path without understanding its purpose.

## Lab E — Reflect on enforcement

Write a short response explaining:
- Why a local hook may not run on every contributor's machine.
- Which checks belong in CI.
- Which policies need server-side enforcement.
- How hook failures should be communicated to contributors.

## Submission checklist

- [ ] Hook directory inspected.
- [ ] Pre-commit hook installed and executable.
- [ ] Clean staged diff passes.
- [ ] Invalid staged diff is rejected.
- [ ] Commit-message hook tested.
- [ ] Shared hooks directory documented.
- [ ] CI/server-side limitations explained.
