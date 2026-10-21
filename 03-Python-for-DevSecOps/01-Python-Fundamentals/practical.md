# Python Fundamentals — Practical Exercises

**Level:** Beginner to early intermediate  
**Requirements:** Python 3; no third-party packages required.

Attempt each exercise before checking `solutions.md`. For the interactive version, use [`practical.ipynb`](practical.ipynb).

## Lab 1: First Python Script

Create `lab01_hello.py`. Print:

```text
Welcome to Python for DevSecOps!
Team: Blue Team
```

Add comments and use a variable for the team name.

## Lab 2: Variables and Data Types

Create variables for hostname (`"app-server-01"`), port (`443`), CPU usage (`68.5`), and monitoring status (`True`). Print each value and its type. Explain why `443` and `"443"` are different.

## Lab 3: Severity Classifier

Write `classify_severity(score)` for a score from 0 to 10:

- 9–10: Critical
- 7–less than 9: High
- 4–less than 7: Medium
- 0–less than 4: Low

Reject invalid types and out-of-range values. Test 0, 4, 7, 9, 10, 12, and `"hello"`.

## Lab 4: Failed Login Counts

Use:

```python
failed_attempts = [1, 4, 8, 0, 6, 2, 10, 3]
```

Calculate total records, the number of counts at least 5, the maximum, and the average.

Expected: 8 records, 3 counts at least 5, maximum 10, average 4.25.

## Lab 5: Validation Functions

Implement:
- `is_valid_port(value)`: integer 1–65535, rejecting booleans.
- `validate_ip(value)`: valid IPv4 or IPv6 string.
- `validate_service_name(value)`: non-empty string after trimming.

Use Python's `ipaddress` module for IP validation.

## Lab 6: Exception Handling

Write `parse_non_negative_integer(value)`. Test `"10"`, `"0"`, `"-1"`, `"hello"`, and `""`. Handle invalid input clearly.

## Lab 7: Log File Analyzer

Create `sample.log`:

```text
INFO service_started
WARNING disk_usage_high
ERROR database_connection_failed
INFO health_check_passed
ERROR authentication_service_failed
```

Count INFO, WARNING, and ERROR records. Save the summary to `log_summary.txt`. Handle missing files.

Expected: INFO 2, WARNING 1, ERROR 2.

## Lab 8: IP Address Validation

Validate:

```python
addresses = [
    "192.0.2.10",
    "198.51.100.25",
    "999.1.1.1",
    "2001:db8::1",
    "not-an-ip",
]
```

Identify IPv4 and IPv6 values and handle invalid strings. This exercise does not perform network activity.

## Lab 9: JSON Configuration Validator

Create `config.json`:

```json
{
  "service": "web",
  "port": 443,
  "debug": false,
  "environment": "production"
}
```

Check required keys, a valid integer port, a Boolean `debug` field, and warn if debug mode is enabled in production. Handle missing or malformed JSON.

## Lab 10: Vulnerability CSV Report

Create `findings.csv`:

```csv
id,title,severity,status
VULN-001,Outdated library,High,Open
VULN-002,Missing security header,Medium,Open
VULN-003,Debug endpoint,Critical,Open
VULN-004,Verbose error message,Low,Closed
VULN-005,Weak configuration,High,Open
```

Count findings by severity, count open findings, list open Critical and High findings, and write a report to `findings_summary.txt`.

Expected: 5 findings, 4 open, 1 Critical, 2 High, 1 Medium, 1 Low.

## Lab 11: File Integrity Manifest

Use `hashlib.sha256` to hash a sample file. Save the filename and digest in a JSON manifest, modify the file, and compare the new digest with the original. Explain why the baseline must be protected separately.

## Lab 12: Security Log Summary Mini-Project

Build a small program that:
- Reads a local synthetic log file.
- Counts INFO, WARNING, and ERROR records.
- Counts records containing `login_failed`.
- Handles malformed records and missing files.
- Writes a JSON summary.
- Uses functions and a main guard.
- Never prints secrets from log data.

Example output structure:

```json
{
  "total_records": 5,
  "levels": {"INFO": 2, "WARNING": 1, "ERROR": 2},
  "failed_login_events": 1
}
```

The values are illustrative; your output must match your data. A text pattern alone does not prove malicious activity.

## Lab 13: Code Quality and Git

Review your code, add docstrings, test boundary cases, and initialize a Git repository. Consider this `.gitignore`:

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
output/
```

Never commit real credentials, private keys, or sensitive logs.

## Reflection Questions

1. What is the difference between a list and a tuple?
2. Why should programs handle exceptions?
3. Why use a virtual environment?
4. Why use `json.loads()` instead of `eval()`?
5. What does a SHA-256 digest tell you, and what does it not prove?
6. Why avoid putting untrusted input into shell commands?
7. What does the Python main guard do?
8. Why is a count of failed logins insufficient to prove an attack?

## Completion Checklist

- [ ] Complete Labs 1–6.
- [ ] Complete Labs 7–10.
- [ ] Complete Labs 11–12.
- [ ] Complete code quality review and reflection.
- [ ] Compare your work with `solutions.md`.
