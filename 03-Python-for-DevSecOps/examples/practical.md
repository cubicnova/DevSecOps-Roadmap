# Python for DevSecOps - Practice Tasks

Complete these tasks using Python's standard library. Use local files and synthetic data only.

## Task 1: Asset inventory

Create a list of five synthetic asset IDs. Print them in sorted order and show the count.

## Task 2: Reusable helper

Write `format_finding(asset, title, severity)` that trims strings and returns a dictionary.

## Task 3: Validate a port

Implement `validate_port(value)` so it accepts integers from 1 through 65535 and rejects invalid values with `ValueError`.

## Task 4: File handling

Create a local text file, read it using `pathlib`, and handle the case where the file does not exist.

## Task 5: JSON configuration

Create a JSON configuration with `environment`, `log_level`, and `checks_enabled`. Write it to disk, read it back, and validate required keys.

## Task 6: Environment variables

Read `APP_ENV` with a default of `development`. Explain why secrets should not be printed or committed.

## Task 7: Logging

Add logging for the start and completion of a small script. Handle at least one expected exception without printing a traceback to the end user.

## Task 8: CSV findings

Write three synthetic findings to CSV. Read the file back and count findings by severity.

## Task 9: Unit testing

Write at least three `unittest` tests for a severity-normalization helper, including an alias, a regular value, and an unknown value.

## Task 10: Safe subprocess

Run the current Python interpreter with `--version` using `subprocess.run`, a list of arguments, and a five-second timeout. Do not use a shell command string.

## Task 11: Dry-run planner

Implement `plan_action(asset, action, dry_run=True)`. It should describe the proposed action without making changes. Refuse to perform real actions in this exercise.

## Task 12: Capstone

Build a local findings report tool that:

- Reads a JSON list of synthetic findings.
- Validates `asset`, `title`, and `severity`.
- Normalizes severity.
- Removes duplicates.
- Writes a CSV report and JSON summary.
- Logs totals without exposing sensitive details.
- Handles missing or malformed input gracefully.

## Reflection

1. Why is input validation important in automation?
2. What is the advantage of `pathlib` over manual path concatenation?
3. Why should subprocess calls have timeouts?
4. Why should secrets be excluded from logs and source control?
5. How do unit tests reduce the risk of regressions?
