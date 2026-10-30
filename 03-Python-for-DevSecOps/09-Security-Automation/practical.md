# Security Automation - Practical Exercises

Use synthetic or explicitly authorized data only. Do not run scans against public systems as part of these exercises.

## Lab 1: Input validation

Write `validate_asset_id(value)` that trims whitespace, rejects empty values, and rejects values longer than 64 characters.

**Expected:** valid IDs are returned in trimmed form; invalid values raise `ValueError`.

## Lab 2: Parse a JSON file

Create a `findings.json` file containing at least five synthetic findings. Load it with `json`, and print the record count.

**Expected:** malformed JSON is handled gracefully with a useful error message.

## Lab 3: Normalize severity

Implement a function that maps `crit`, `critical`, `high`, `medium`, `moderate`, `low`, `info`, and `informational` to consistent labels. Preserve unknown labels as `Unknown`.

## Lab 4: Validate records

For each finding, require non-empty `asset` and `title` fields. Normalize severity. Keep invalid records in a separate error list rather than silently dropping them.

## Lab 5: Deduplicate

Remove duplicate findings using a stable key such as normalized asset plus normalized title. Report how many duplicates were removed.

## Lab 6: Severity summary

Produce counts for Critical, High, Medium, Low, Informational, and Unknown, including zero-count categories.

## Lab 7: Export a CSV report

Write validated, deduplicated findings to `security_report.csv`. Use explicit column names and UTF-8 encoding. Do not include secret fields if they appear in source data.

## Lab 8: Add logging and error handling

Add `logging` statements for start, number of input records, invalid records, duplicate count, output path, and completion. Avoid printing sensitive record contents.

## Lab 9: Dry-run action planner

Create `plan_action(asset, action, dry_run=True)`. In dry-run mode, display the proposed action. Ensure no real change is performed in the exercise.

## Lab 10: Mini-project - Security Findings Report Generator

Build a script with these requirements:

- Input: a local JSON file containing synthetic findings.
- Validate record shape and required fields.
- Normalize severity.
- Deduplicate findings.
- Create a severity summary.
- Export a CSV report and a JSON summary.
- Return a non-zero exit code if the input file is missing or invalid.
- Log errors without exposing secrets or full sensitive payloads.

### Suggested test data

```json
[
  {"asset": "app-001", "title": "Missing security header", "severity": "medium"},
  {"asset": "app-001", "title": "Missing security header", "severity": "Medium"},
  {"asset": "api-001", "title": "Verbose error response", "severity": "low"},
  {"asset": "web-001", "title": "Outdated dependency", "severity": "high"},
  {"asset": "db-001", "title": "Backup access review", "severity": "informational"}
]
```

### Review questions

1. Why should unknown severity labels remain visible?
2. What can go wrong if duplicate findings are not removed?
3. Why is dry-run mode useful before an automation changes a system?
4. What should never be written to a security log?
5. Why should a network automation enforce an allowlist, timeout, and rate limit?
6. Why is an argument list safer than building a shell command string?
