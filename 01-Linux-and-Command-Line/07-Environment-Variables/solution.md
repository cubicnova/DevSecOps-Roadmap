# Linux Environment Variables — Solutions

These are reference solutions for the exercises in `practical.md`. Examples assume Bash.

## Solution 1: Inspect Your Environment

```bash
printf 'HOME=%s\n' "$HOME"
printf 'USER=%s\n' "$USER"
printf 'SHELL=%s\n' "$SHELL"
printf 'PWD=%s\n' "$PWD"
printf 'PATH=%s\n' "$PATH"

printenv
export -p
```

- `printenv` displays exported environment variables.
- `env` displays the environment or runs a command with a modified environment.
- `set` displays shell variables, functions, and shell options in Bash, so it may show more sensitive information than expected.

Review output before sharing it.

## Solution 2: Shell Variable vs. Environment Variable

```bash
LAB_MESSAGE="Hello from the lab"
printf '%s\n' "$LAB_MESSAGE"
printenv LAB_MESSAGE
```

Before export, the shell can read the variable but a child process normally cannot.

```bash
export LAB_MESSAGE
printenv LAB_MESSAGE
bash -c 'printf "%s\n" "$LAB_MESSAGE"'
```

Exporting the variable makes it part of the environment inherited by subsequently started child processes.

## Solution 3: Temporary Command Variables

```bash
LAB_MODE=testing printenv LAB_MODE
printenv LAB_MODE
```

The first command receives `LAB_MODE=testing`. The assignment does not set `LAB_MODE` in the current shell, so the second command normally produces no value and returns a non-zero status if the variable was otherwise unset.

For a script:

```bash
LAB_MODE=development bash ./app_config.sh
```

This is useful for tests and one-off configuration.

## Solution 4: Unset vs. Empty

```bash
unset LAB_VALUE

if [[ -v LAB_VALUE ]]; then
  echo "LAB_VALUE is set"
else
  echo "LAB_VALUE is unset"
fi

LAB_VALUE=""

if [[ -v LAB_VALUE ]]; then
  echo "LAB_VALUE is set, possibly empty"
fi
```

An unset variable and a variable set to an empty string can both expand to an empty value. Use a variable-existence test when that distinction matters.

## Solution 5: Defaults and Configuration Validation

Create `validate_config.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

APP_ENV="${APP_ENV:-development}"
LOG_LEVEL="${LOG_LEVEL:-info}"

case "$APP_ENV" in
  development|testing|production)
    ;;
  *)
    printf 'Error: invalid APP_ENV: %s\n' "$APP_ENV" >&2
    exit 1
    ;;
esac

printf 'APP_ENV=%s\n' "$APP_ENV"
printf 'LOG_LEVEL=%s\n' "$LOG_LEVEL"
```

Test:

```bash
bash validate_config.sh
APP_ENV=testing bash validate_config.sh
APP_ENV=unknown bash validate_config.sh
APP_ENV='' bash validate_config.sh
```

The empty value falls back to `development` because the expression uses `:-`.

## Solution 6: Modify PATH Safely

```bash
printf '%s\n' "$PATH" | tr ':' '\n'
command -v bash
command -v python3

mkdir -p "$HOME/bin"
export PATH="$HOME/bin:$PATH"

printf '%s\n' "$PATH" | tr ':' '\n'
```

Prepending `$HOME/bin` makes commands in that directory take precedence over commands with the same name in later directories. Only put trusted executables there and ensure the directory is controlled by the intended user.

## Solution 7: Persist a Non-Sensitive Variable

Back up the file if it exists:

```bash
if [[ -f ~/.bashrc ]]; then
  cp ~/.bashrc ~/.bashrc.backup
fi
```

Edit `~/.bashrc` and add:

```bash
export EDITOR="nano"
```

Reload and test:

```bash
source ~/.bashrc
printf '%s\n' "$EDITOR"
```

`~/.bashrc` is commonly read by interactive non-login Bash shells. Login-shell behavior depends on startup-file configuration. Other applications and services may not read it.

## Solution 8: Application Configuration Script

Create `app_config.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

APP_ENV="${APP_ENV:-development}"
LOG_LEVEL="${LOG_LEVEL:-info}"
APP_PORT="${APP_PORT:-8080}"

case "$APP_ENV" in
  development|testing|production) ;;
  *)
    printf 'Error: APP_ENV must be development, testing, or production\n' >&2
    exit 1
    ;;
esac

case "$LOG_LEVEL" in
  debug|info|warning|error) ;;
  *)
    printf 'Error: invalid LOG_LEVEL\n' >&2
    exit 1
    ;;
esac

if [[ ! "$APP_PORT" =~ ^[0-9]+$ ]]; then
  printf 'Error: APP_PORT must be an integer\n' >&2
  exit 1
fi

if (( APP_PORT < 1 || APP_PORT > 65535 )); then
  printf 'Error: APP_PORT must be between 1 and 65535\n' >&2
  exit 1
fi

printf 'APP_ENV=%s\n' "$APP_ENV"
printf 'LOG_LEVEL=%s\n' "$LOG_LEVEL"
printf 'APP_PORT=%s\n' "$APP_PORT"
```

Test:

```bash
bash app_config.sh
APP_ENV=testing APP_PORT=9000 bash app_config.sh
APP_PORT=invalid bash app_config.sh
APP_PORT=70000 bash app_config.sh
```

The script prints only non-sensitive configuration. In production, do not print secret values.

## Solution 9: Inspect a Clean Environment

```bash
env -i PATH=/usr/bin:/bin HOME="$HOME" \
  bash --noprofile --norc -c 'printf "HOME=%s\nPATH=%s\n" "$HOME" "$PATH"'
```

`env -i` clears the inherited environment before adding the specified variables. This can make tests more reproducible, but programs may fail if they depend on variables such as `LANG`, `TERM`, proxy settings, or application-specific configuration.

## Solution 10: Environment Variables and Secret Handling

Proposed practice:

```bash
echo "DATABASE_PASSWORD=real-password" >> ~/.bashrc
git add .env
```

Risks include:

1. Secrets may be committed to source control or retained in Git history.
2. Shell startup files may expose credentials to every process launched by that shell.
3. Debugging commands and logs may accidentally print sensitive values.
4. Shared backups or home-directory access may expose the credentials.
5. Credentials can be reused across development and production environments.

Safer approach:

- Never commit secret-bearing `.env` files; add them to `.gitignore`.
- Commit a `.env.example` containing placeholders only.
- Restrict access to local configuration files.
- Use a secrets manager or CI/CD platform's secret store for production credentials.
- Inject only the secrets required by a given process.
- Rotate credentials if they were exposed.

Environment variables are convenient, but they are not a dedicated secret vault.

## Solution 11: Troubleshooting a Missing Variable

Check whether the variable is exported:

```bash
printf 'Shell value: %s\n' "${APP_ENV-<unset>}"
printenv APP_ENV
```

If it is only a shell variable, export it:

```bash
export APP_ENV=testing
```

Or pass it explicitly to one command:

```bash
APP_ENV=testing bash ./app_config.sh
```

A child process receives an environment snapshot when it starts. Changing a variable in the parent shell does not update the environment of processes that are already running.

## Solution 12: DevSecOps Configuration Design

A sensible configuration design separates ordinary settings from secrets.

### Non-sensitive settings

Examples include:

- `APP_ENV`
- `LOG_LEVEL`
- `APP_PORT`

Use validated defaults for local development when appropriate.

### Required or sensitive configuration

Examples include database credentials, API tokens, and private keys.

- Supply required values from a secret manager or protected CI/CD variables.
- Validate required variables before the application starts.
- Keep production and testing credentials separate.
- Avoid printing secret values in logs.
- Restrict access to build logs, deployment configuration, and secret stores.
- Rotate exposed credentials promptly.

### Example validation

```bash
: "${DATABASE_URL:?DATABASE_URL must be supplied securely}"
: "${APP_ENV:?APP_ENV must be set}"
```

This checks that the values are present and non-empty; it does not validate the full URL format or prove that a secret is authentic. Add application-specific validation where needed.

## Final Review

You should now understand:

- How shell and environment variables differ.
- How child processes inherit exported variables.
- How to set, unset, and persist configuration.
- How to validate configuration in Bash scripts.
- How to update `PATH` safely.
- Why secrets need careful handling in local development and CI/CD.

## References

- [GNU Bash Manual — Environment](https://www.gnu.org/software/bash/manual/html_node/Environment.html)
- [Linux `environ(7)` Manual](https://man7.org/linux/man-pages/man7/environ.7.html)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
