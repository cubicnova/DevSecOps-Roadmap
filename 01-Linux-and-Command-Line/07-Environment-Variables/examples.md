# Linux Environment Variables — Examples

Examples below assume Bash on Linux. Outputs vary by user, distribution, and session.

## 1. Inspect Common Variables

```bash
printf 'HOME=%s\n' "$HOME"
printf 'USER=%s\n' "$USER"
printf 'SHELL=%s\n' "$SHELL"
printf 'PWD=%s\n' "$PWD"
printf 'PATH=%s\n' "$PATH"
```

`printf` is useful for predictable formatting. Some variables may be unset or may not describe the current process exactly as expected.

## 2. List Exported Variables

```bash
printenv
env
export -p
```

- `printenv` and `env` display environment variables.
- `export -p` displays variables marked for export in Bash.
- `set` shows more than environment variables, including shell variables and functions. It may expose sensitive shell state, so avoid sharing its full output publicly.

Inspect one variable:

```bash
printenv HOME
printenv PATH
```

## 3. Shell Variable vs. Environment Variable

```bash
DEMO_MESSAGE="Hello from Bash"
printf '%s\n' "$DEMO_MESSAGE"
printenv DEMO_MESSAGE
```

The shell can read `DEMO_MESSAGE`, but `printenv` normally will not display it until it is exported.

Export it:

```bash
export DEMO_MESSAGE
printenv DEMO_MESSAGE
bash -c 'printf "%s\n" "$DEMO_MESSAGE"'
```

The child Bash process inherits the exported value.

## 4. Set and Export in One Step

```bash
export APP_ENV="development"
printf 'App environment: %s\n' "$APP_ENV"
printenv APP_ENV
```

Environment variable names are case-sensitive. By convention, names are commonly uppercase, and there must be no spaces around `=` in an assignment.

## 5. Set a Variable for One Command

```bash
APP_ENV=testing printenv APP_ENV
printenv APP_ENV
```

The first command prints `testing`. The second normally prints nothing and returns a non-zero status if `APP_ENV` was not already exported in the shell.

This technique is useful for running an application with a temporary configuration value:

```bash
APP_ENV=testing ./app.sh
```

## 6. Unset a Variable

```bash
export DEMO_TEMP="temporary"
printenv DEMO_TEMP

unset DEMO_TEMP
printenv DEMO_TEMP
```

To distinguish an unset variable from an empty value in Bash:

```bash
unset SAMPLE
if [[ -v SAMPLE ]]; then
  echo "SAMPLE is set"
else
  echo "SAMPLE is unset"
fi

SAMPLE=""
if [[ -v SAMPLE ]]; then
  echo "SAMPLE is set, value may be empty"
fi
```

## 7. Use Default Values

```bash
printf 'Environment: %s\n' "${APP_ENV:-development}"
```

`${APP_ENV:-development}` uses `development` when `APP_ENV` is unset or empty.

Require a value:

```bash
: "${APP_ENV:?APP_ENV must be set}"
```

If the variable is unset or empty, Bash prints an error and the command exits with a non-zero status.

## 8. Inspect and Safely Extend PATH

```bash
printf '%s\n' "$PATH" | tr ':' '\n'
command -v bash
command -v python3
```

Add a personal `bin` directory for the current shell:

```bash
mkdir -p "$HOME/bin"
export PATH="$HOME/bin:$PATH"
```

This prepends the directory to `PATH` for the current shell and child processes. Only add directories you control and trust. Avoid empty path elements and untrusted writable directories.

## 9. Make a Non-Sensitive Variable Persistent

For interactive Bash terminals, add a line to `~/.bashrc`:

```bash
export EDITOR="nano"
```

Then reload the file:

```bash
source ~/.bashrc
printf '%s\n' "$EDITOR"
```

This affects the current shell and shells that read that file. Startup-file behavior differs for login shells and other applications.

To edit carefully, use a text editor rather than blindly appending duplicate lines.

## 10. Use a Script with Environment Configuration

Create `show_config.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

APP_ENV="${APP_ENV:-development}"
LOG_LEVEL="${LOG_LEVEL:-info}"

printf 'APP_ENV=%s\n' "$APP_ENV"
printf 'LOG_LEVEL=%s\n' "$LOG_LEVEL"
```

Run with defaults:

```bash
bash show_config.sh
```

Run with temporary values:

```bash
APP_ENV=testing LOG_LEVEL=debug bash show_config.sh
```

## 11. Validate a Required Variable

Create `validate_config.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${APP_ENV:?APP_ENV is required}"

case "$APP_ENV" in
  development|testing|production)
    printf 'Valid APP_ENV: %s\n' "$APP_ENV"
    ;;
  *)
    printf 'Invalid APP_ENV: %s\n' "$APP_ENV" >&2
    exit 1
    ;;
esac
```

Test it:

```bash
APP_ENV=testing bash validate_config.sh
APP_ENV=unknown bash validate_config.sh
```

## 12. Environment Variables and Secrets

Avoid examples like these with real credentials:

```bash
# Do not use real credentials in examples or committed files.
export DATABASE_PASSWORD="replace-with-a-placeholder"
```

Environment variables can be exposed through process inspection, logs, debugging output, or application behavior depending on the environment. Prefer a secrets manager or platform-managed secret injection for production credentials, and grant access only to the processes that need them.

Never print all environment variables in production logs or commit secret-bearing `.env` files.

## 13. Run a Command with a Clean Environment

```bash
env -i PATH=/usr/bin:/bin HOME="$HOME" bash --noprofile --norc -c 'printf "HOME=%s\nPATH=%s\n" "$HOME" "$PATH"'
```

`env -i` starts the command with a cleared environment, after which only the variables explicitly provided are passed. A minimal environment may cause programs to behave differently.

## Cleanup

```bash
rm -f show_config.sh validate_config.sh
unset DEMO_MESSAGE DEMO_TEMP APP_ENV LOG_LEVEL SAMPLE
```

Only remove the dedicated files created for this lab.

## Key Takeaways

- `export` makes variables available to child processes.
- A one-command assignment does not persist in the current shell.
- `unset` removes a variable; an empty value is different from an unset value.
- Startup files make selected settings persist for shells that read them.
- Protect `PATH`, avoid secret leakage, and validate configuration.
