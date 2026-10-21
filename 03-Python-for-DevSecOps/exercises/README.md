# Python for DevSecOps — Exercises

A hands-on exercise bank for practicing Python skills used in DevSecOps workflows. Exercises progress from core programming to file processing, testing, and safe security automation.

## Learning objectives

- Practice variables, conditions, loops, functions, and data structures.
- Parse and validate text, CSV, and JSON data.
- Handle files and exceptions safely.
- Use logging and unit tests to make scripts maintainable.
- Build small, defensive automation utilities for authorized environments.

## Suggested workflow

1. Attempt each exercise without looking at `solutions.md`.
2. Write code in a separate `.py` file or in `practical.ipynb`.
3. Test normal inputs, empty inputs, malformed inputs, and boundary cases.
4. Use only synthetic data or systems you own / are authorized to assess.
5. Compare your approach with `solutions.md`, then refactor for readability.

## Exercise levels

| Level | Focus | Exercises |
|---|---|---|
| Beginner | Strings, numbers, lists, dictionaries | 1–5 |
| Intermediate | Functions, files, JSON/CSV, exceptions | 6–12 |
| Advanced | Logging, tests, API parsing, safe automation | 13–18 |
| Mini-projects | Combine multiple concepts | 19–21 |

## Exercises

### 1. Input validation
Write `validate_port(value)` that returns an integer port if `value` represents a number from 1 to 65535. Raise `ValueError` for invalid input.

### 2. Count log levels
Given a list of log lines, count occurrences of `INFO`, `WARNING`, `ERROR`, and `DEBUG`. Ignore lines that do not contain a recognized level.

### 3. Deduplicate indicators
Given a list of synthetic IP-address strings, return unique values in their original order.

### 4. Summarize findings
Given a list of dictionaries with `id`, `severity`, and `title`, return a count per severity. Handle missing severity as `Unknown`.

### 5. Redact secrets
Write `redact(text)` that replaces values after `api_key=`, `token=`, and `password=` with `[REDACTED]`. Do not print or log the original secret.

### 6. Parse a CSV inventory
Read `assets.csv` with columns `asset,environment,owner` and return assets grouped by environment. Include a useful error message for missing columns.

### 7. JSON configuration validator
Load a JSON file and verify that it contains `timeout_seconds` (positive number) and `retries` (non-negative integer). Handle malformed JSON and missing fields.

### 8. Safe file hashing
Create `sha256_file(path)` that streams a file in chunks and returns its SHA-256 hex digest. Do not load the entire file into memory.

### 9. File extension report
Walk a user-selected directory and count files by extension. Skip symlinks, handle permission errors, and do not modify files.

### 10. Exception-safe parser
Write `parse_int_list(values)` that converts a sequence of strings to integers. Raise a clear `ValueError` identifying the invalid item.

### 11. Structured logging
Create a function that records an event with timestamp, event type, and status. Avoid logging credentials, tokens, or personal data.

### 12. Retry helper
Implement `retry(operation, attempts)` for a callable that may raise a transient exception. Stop after `attempts`, validate that attempts is positive, and avoid retrying non-transient errors.

### 13. Unit tests
Write tests for `validate_port`, `redact`, and `parse_int_list`. Include valid inputs, invalid inputs, and boundary cases.

### 14. Mock an HTTP response
Without making a network request, mock a small function that interprets an HTTP response status and returns `ok`, `retry`, or `fail`.

### 15. Parse synthetic security events
Given JSON objects containing `timestamp`, `source`, and `event_type`, validate required fields and summarize event counts by type. Use only sample data.

### 16. Configuration diff
Compare two dictionaries and return keys whose values changed, were added, or were removed. Do not expose secret values in the result.

### 17. CLI argument validator
Use `argparse` to accept a directory and an optional `--json` flag. Validate the directory before processing and return a non-zero exit code on invalid input.

### 18. Defensive URL validation
Validate URL syntax and allow only `https` URLs to a configurable allowlist of hostnames. Do not fetch the URL.

### 19. Mini-project: Log summary CLI
Build a CLI that reads a local text log, counts levels, writes a summary JSON file, and reports malformed or unreadable input safely.

### 20. Mini-project: File integrity manifest
Create a manifest of SHA-256 hashes for regular files in a specified test directory. Exclude symlinks, sort output deterministically, and write JSON.

### 21. Mini-project: Security findings report
Read a synthetic JSON findings file, normalize severities, redact likely secrets, summarize counts, and emit a machine-readable report. Include tests.

## Completion checklist

- [ ] Functions have clear names and docstrings.
- [ ] Inputs are validated.
- [ ] Exceptions are handled at the correct boundary.
- [ ] Output is deterministic where practical.
- [ ] Tests cover success and failure cases.
- [ ] No secrets are printed, committed, or included in example data.

## References

- [The Python Tutorial](https://docs.python.org/3/tutorial/)
- [Python `unittest`](https://docs.python.org/3/library/unittest.html)
- [Python `argparse`](https://docs.python.org/3/library/argparse.html)
