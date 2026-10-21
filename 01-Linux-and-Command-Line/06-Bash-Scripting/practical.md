# 🧪 Bash Scripting — Practical Labs

**Level:** Beginner to intermediate  
**Estimated time:** 90–120 minutes  
**Environment:** Linux, WSL, or another Bash environment

## Safety checklist

- Work in `~/bash-lab`.
- Inspect every script before running it.
- Use sample files, not production logs or system directories.
- Quote variables and validate user input.
- Do not store passwords or tokens in scripts.
- Do not run scripts with `sudo` unless the task genuinely requires it.

## Setup

```bash
mkdir -p ~/bash-lab
cd ~/bash-lab
```

## Lab 1 — Your first script

**Tasks**

1. Create `hello.sh`.
2. Add a Bash shebang.
3. Print two lines of text.
4. Run it with `bash hello.sh`.
5. Add execute permission and run `./hello.sh`.

**Hints:** `nano`, `chmod`, `echo`, `printf`

## Lab 2 — Variables and input

**Tasks**

1. Store your name in a variable.
2. Store the current learning topic in another variable.
3. Ask the user for a favorite Linux command.
4. Print the responses using `printf`.
5. Try a value containing spaces.

**Hints:** `read -r`, `printf`, quoted expansions.

## Lab 3 — File checker

Write `file-check.sh` that accepts exactly one path argument.

**Requirements**

- Print a usage message if no argument or too many arguments are provided.
- Report whether the path is a regular file, directory, or missing.
- Return a non-zero exit code for invalid usage or a missing path.
- Handle paths containing spaces.

Test it with a file, a directory, a missing path, and a path containing spaces.

## Lab 4 — Number validation

Write a script that asks for an integer and reports whether it is negative, zero, or positive.

**Requirements**

- Reject empty input and non-integer input.
- Do not pass unvalidated input into arithmetic expressions.
- Test values such as `-3`, `0`, `8`, `abc`, and an empty response.

**Hint:** Bash regular-expression matching with `[[ "$value" =~ ... ]]`.

## Lab 5 — Loops and functions

**Tasks**

1. Print numbers from 1 to 10.
2. Loop over a list of Linux topics.
3. Write a function that checks whether a path exists.
4. Call the function with both existing and missing paths.
5. Use `local` for function-specific variables.

## Lab 6 — Log analyzer

Create `logs/app.log` containing at least five sample lines, including two lines containing `ERROR`.

Write `log-analyzer.sh` to:

1. Accept a log-file path as an argument.
2. Verify the file exists and is readable.
3. Count lines containing `ERROR`.
4. Print matching lines with line numbers.
5. Report a useful error for invalid input.

**Hint:** `grep -c`, `grep -n`, and remember that `grep` returns `1` when no matches are found. No matches should not automatically be treated as a script failure.

## Lab 7 — Error handling

Create a script that:

1. Requires one directory argument.
2. Checks that the path exists and is a directory.
3. Lists regular files in the directory.
4. Writes errors to standard error.
5. Returns meaningful exit codes.
6. Handles a directory name containing spaces.

**Hint:** `"$1"`, `>&2`, `exit`, `find`.

## Lab 8 — Temporary files

Write a script that creates a temporary file with `mktemp`, writes a sample message, displays it, and removes the temporary file when the script exits.

**Requirements**

- Use a cleanup function and `trap`.
- Do not use a predictable fixed temporary filename.
- Verify cleanup occurred without printing sensitive data.

## Lab 9 — System information script

Create `system-info.sh` that prints:

- Date and time.
- Hostname.
- Distribution information, if available.
- Kernel version.
- Uptime.
- Memory summary.
- Disk usage.

The script should handle missing optional commands gracefully and should not change system configuration.

## Lab 10 — Mini project: System health report

Create `system-health.sh` that:

1. Creates `output/` under your lab directory.
2. Writes a timestamped report.
3. Includes hostname, kernel, uptime, memory, disk, and top CPU-consuming processes.
4. Checks the availability of required commands.
5. Uses safe quoting and clear error messages.
6. Restricts report permissions where appropriate.
7. Does not restart services, delete user files, or expose secrets.

Test with `bash -n system-health.sh` before running it.

## Bonus challenges

- Add a `--help` option.
- Add a log function with timestamps.
- Add a summary of missing commands.
- Use ShellCheck to identify potential bugs.
- Add an optional directory argument for report output, validating it first.

## Submission checklist

- [ ] Scripts have a Bash shebang.
- [ ] Variables are quoted appropriately.
- [ ] User input and arguments are validated.
- [ ] Exit codes are meaningful.
- [ ] File operations are limited to the lab directory.
- [ ] Temporary files are cleaned up.
- [ ] Syntax checks pass.
- [ ] The system health report runs successfully.

## Reflection questions

1. What does the shebang do?
2. What is the difference between `$1`, `$#`, and `"$@"`?
3. Why is `"$variable"` usually safer than `$variable`?
4. What does exit status `0` usually mean?
5. How do `>` and `>>` differ?
6. Why can `grep` return `1` without an error?
7. What do `set -u` and `set -o pipefail` do?
8. Why is `set -e` not a complete error-handling strategy?
9. Why should `eval` be avoided with untrusted input?
10. How can `trap` help clean up temporary files?
