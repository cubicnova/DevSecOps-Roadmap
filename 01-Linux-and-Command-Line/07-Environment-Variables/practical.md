# Linux Environment Variables — Practical Lab

## Lab Information

**Level:** Beginner to Intermediate

**Objective:** Practice inspecting, setting, exporting, unsetting, persisting, and safely using environment variables in Bash scripts.

**Environment:** Linux VM using Bash (Ubuntu, Debian, Kali, or another distribution).

## Safety Rules

- Do not use real passwords, API keys, or production secrets in the lab.
- Do not replace `PATH` with a guessed or incomplete value.
- Do not share full environment dumps publicly; they may contain sensitive values.
- Modify only your own shell startup files, and keep a backup before editing.
- Use dedicated lab files and remove them after the exercise.

---

## Practical 1: Inspect Your Environment

**Tasks**

1. Display `HOME`, `USER`, `SHELL`, `PWD`, and `PATH`.
2. List exported variables.
3. Explain the difference between `printenv`, `env`, and `set`.
4. Explain why `set` output should not be shared without review.

Explore:

```bash
printf 'HOME=%s\n' "$HOME"
printf 'USER=%s\n' "$USER"
printf 'SHELL=%s\n' "$SHELL"
printf 'PWD=%s\n' "$PWD"
printf 'PATH=%s\n' "$PATH"
printenv
export -p
```

## Practical 2: Shell Variable vs. Environment Variable

**Tasks**

1. Create a variable named `LAB_MESSAGE` without `export`.
2. Display it in the current shell.
3. Check whether `printenv LAB_MESSAGE` displays it.
4. Export the variable.
5. Verify that a child Bash process can read it.

**Challenge:** Explain why a child process does not normally inherit an unexported shell variable.

## Practical 3: Temporary Command Variables

**Tasks**

1. Run `LAB_MODE=testing printenv LAB_MODE`.
2. Check `LAB_MODE` in the current shell afterward.
3. Run a script with `LAB_MODE=development`.
4. Explain when a one-command assignment is useful.

## Practical 4: Unset vs. Empty

**Tasks**

1. Unset `LAB_VALUE`.
2. Use a Bash conditional to test whether it is set.
3. Assign an empty string to it.
4. Test again.
5. Explain why checking only its printed value is insufficient.

## Practical 5: Use Defaults and Validate Configuration

Create a script that:

1. Uses `APP_ENV=development` when the variable is unset or empty.
2. Uses `LOG_LEVEL=info` when the variable is unset or empty.
3. Accepts only `development`, `testing`, or `production` for `APP_ENV`.
4. Prints an error to standard error and exits non-zero for invalid input.

Test the script with valid, invalid, unset, and empty values.

## Practical 6: Modify PATH Safely

**Tasks**

1. Display `PATH` as one directory per line.
2. Locate `bash` and `python3` using `command -v`.
3. Create `$HOME/bin`.
4. Add it to `PATH` for the current shell.
5. Verify the change.
6. Explain the risk of adding an untrusted writable directory to `PATH`.

Do not overwrite the existing `PATH`.

## Practical 7: Persist a Non-Sensitive Variable

**Tasks**

1. Back up `~/.bashrc` if it exists.
2. Add a non-sensitive variable such as `EDITOR=nano` using the correct Bash syntax.
3. Reload the file or open a new terminal.
4. Verify the variable.
5. Explain why `~/.bashrc` may not be read by every process or login shell.

Do not add credentials to shell startup files.

## Practical 8: Build an Application Configuration Script

Create `app_config.sh` that reads:

- `APP_ENV`
- `LOG_LEVEL`
- `APP_PORT`

Requirements:

1. Use safe defaults for non-sensitive configuration.
2. Validate that `APP_PORT` is an integer within the range 1–65535.
3. Reject invalid input with a useful error message.
4. Quote variable expansions.
5. Do not print secrets or dump the entire environment.

## Practical 9: Inspect a Clean Environment

**Tasks**

1. Run a command with `env -i`.
2. Provide only `PATH` and `HOME`.
3. Print those variables from the child process.
4. Explain why a clean environment can help with reproducibility.
5. Identify why some programs may fail if expected variables are missing.

## Practical 10: Environment Variables and Secret Handling

Review this proposed practice:

```bash
echo "DATABASE_PASSWORD=real-password" >> ~/.bashrc
git add .env
```

Explain at least four risks and recommend a safer approach for local development and production. Use placeholder values only.

## Practical 11: Troubleshooting

A script reports that `APP_ENV` is missing, even though you assigned it in your terminal.

**Tasks**

1. Determine whether the variable is a shell variable or exported environment variable.
2. Verify its availability with `printenv`.
3. Run the script with an explicit command-scoped assignment.
4. Explain why changing a variable in one shell does not update already-running processes.

## Final Challenge: DevSecOps Configuration

Design a configuration approach for a small application with separate development, testing, and production environments.

Document:

1. Which settings can safely use defaults.
2. Which settings must be provided externally.
3. How required variables are validated.
4. How secrets are supplied without committing them to Git.
5. How logs avoid exposing sensitive configuration.
6. How you would reproduce the same configuration in CI/CD without exposing credentials.

## Submission Checklist

- [ ] Inspected common environment variables.
- [ ] Demonstrated export and child-process inheritance.
- [ ] Used a command-scoped variable.
- [ ] Distinguished unset from empty.
- [ ] Created a configuration-validation script.
- [ ] Modified `PATH` safely.
- [ ] Persisted a non-sensitive variable.
- [ ] Tested a clean environment.
- [ ] Documented safe secret handling.
- [ ] Completed the DevSecOps configuration challenge.

Compare your work with `solution.md`.
