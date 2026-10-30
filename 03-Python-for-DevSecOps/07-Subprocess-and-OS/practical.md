# Subprocess and OS — Practical Exercises

**Level:** Beginner to intermediate  
**Requirements:** Python 3; no third-party packages.

Use the interactive version in `practical.ipynb`. Perform all exercises in a temporary workspace and avoid destructive or privileged commands.

## Lab 1 — Inspect the current environment

Print the current working directory, Python version, operating system, and CPU count.

Use `os`, `platform`, `sys`, and `pathlib`.

## Lab 2 — Directory inventory

Create a directory named `lab_workspace` containing two text files and one subdirectory. List its entries and identify files versus directories.

**Challenge:** Include file size in bytes without opening file contents.

## Lab 3 — Environment variables

Read `APP_ENV` using `os.getenv()` with a default value. Check whether `API_TOKEN` is configured, but never print its value.

Explain why environment variables can still leak through process inspection, logs, or misconfiguration.

## Lab 4 — Run a harmless command

Use `subprocess.run()` to run the current Python interpreter with `--version`. Capture output and print the version.

**Requirements:** Use a list of arguments, `capture_output=True`, `text=True`, and a timeout.

## Lab 5 — Capture stdout and stderr

Run a small Python child process that prints one line to stdout and one line to stderr. Display each stream separately and print the return code.

## Lab 6 — Handle non-zero exit status

Run a harmless child Python process that exits with status code 3. Detect and report the non-zero status without crashing.

Repeat using `check=True` and handle `subprocess.CalledProcessError`.

## Lab 7 — Timeout handling

Run a child Python process that sleeps longer than the configured timeout. Catch `subprocess.TimeoutExpired` and display a safe message.

## Lab 8 — Working directory

Use `cwd=` to execute a child Python process in a temporary directory. Have the child print its working directory and compare it with the expected path.

## Lab 9 — Environment override

Copy the current environment, set `APP_ENV` to `test` for a child process, and verify the child sees the override. Do not print secret environment values.

## Lab 10 — Safe argument passing

Pass a filename containing spaces as one argument to a child Python process. Show that it arrives intact. Explain why shell command concatenation is risky.

## Lab 11 — File inventory report

Use `pathlib` to inventory files inside your lab workspace. Record relative path, suffix, and size. Write the report to JSON.

Avoid traversing your whole home directory or system directories for this exercise.

## Lab 12 — Mini-project: DevSecOps preflight checker

Create:

```text
preflight-checker/
├── main.py
├── checks.py
├── README.md
└── output/
```

Requirements:
- Report Python version and platform.
- Check that a configured workspace exists.
- Run the Python interpreter's version command using `subprocess`.
- Capture stdout/stderr and return code.
- Apply a timeout.
- Write a JSON report.
- Handle expected errors without exposing secrets.
- Use `shell=False` and argument lists.
- Do not require root/admin privileges or modify system configuration.

## Reflection questions

1. What is the difference between `os` and `pathlib`?
2. What are stdout and stderr?
3. What does a process return code indicate?
4. Why should commands receive argument lists?
5. What is command injection?
6. Why are timeouts important?
7. Why should environment variables containing secrets not be printed?
8. What should a script do when a child process fails?

## Completion checklist

- [ ] Inspect environment and paths
- [ ] Inventory a test directory
- [ ] Read environment variables safely
- [ ] Run a harmless subprocess
- [ ] Capture output and inspect exit codes
- [ ] Handle timeouts and expected exceptions
- [ ] Use `cwd` and environment overrides
- [ ] Complete the preflight checker
