# Python Fundamentals — Solutions

Reference solutions for the exercises in `practical.md`. Attempt the labs before reviewing this file.

## Solution 1: First Python Script

```python
def main():
    print("Welcome to Python for DevSecOps!")
    team = "Blue Team"
    print(f"Team: {team}")

if __name__ == "__main__":
    main()
```

## Solution 2: Variables and Types

```python
hostname = "app-server-01"
port = 443
cpu_usage = 68.5
monitoring_enabled = True

for value in [hostname, port, cpu_usage, monitoring_enabled]:
    print(value, type(value).__name__)
```

`443` is an integer; `"443"` is a string.

## Solution 3: Severity Classifier

```python
def classify_severity(score):
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        return "Invalid input"
    if not 0 <= score <= 10:
        return "Invalid score"
    if score >= 9:
        return "Critical"
    if score >= 7:
        return "High"
    if score >= 4:
        return "Medium"
    return "Low"
```

## Solution 4: Failed Login Counts

```python
failed_attempts = [1, 4, 8, 0, 6, 2, 10, 3]
threshold = 5

print("Total records:", len(failed_attempts))
print("At least five:", sum(count >= threshold for count in failed_attempts))
print("Maximum:", max(failed_attempts))
print("Average:", sum(failed_attempts) / len(failed_attempts))
```

## Solution 5: Validation Functions

```python
import ipaddress

def is_valid_port(value):
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and 1 <= value <= 65535
    )

def validate_ip(value):
    if not isinstance(value, str):
        return False
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False

def validate_service_name(value):
    return isinstance(value, str) and bool(value.strip())
```

## Solution 6: Exception Handling

```python
def parse_non_negative_integer(value):
    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError("Enter a valid integer") from error

    if number < 0:
        raise ValueError("Value cannot be negative")
    return number
```

## Solution 7: Log Analyzer

```python
from collections import Counter
from pathlib import Path

def analyze_log(path):
    counts = Counter()
    with Path(path).open(encoding="utf-8") as file:
        for line in file:
            parts = line.split(maxsplit=1)
            if parts and parts[0] in {"INFO", "WARNING", "ERROR"}:
                counts[parts[0]] += 1
    return counts

try:
    counts = analyze_log("sample.log")
    report = (
        f"INFO: {counts['INFO']}\n"
        f"WARNING: {counts['WARNING']}\n"
        f"ERROR: {counts['ERROR']}\n"
    )
    Path("log_summary.txt").write_text(report, encoding="utf-8")
    print(report)
except FileNotFoundError:
    print("Error: sample.log was not found")
except OSError:
    print("Error: unable to read or write a file")
```

## Solution 8: IP Validation

```python
import ipaddress

addresses = ["192.0.2.10", "198.51.100.25", "999.1.1.1",
             "2001:db8::1", "not-an-ip"]

for value in addresses:
    try:
        address = ipaddress.ip_address(value)
        print(value, f"valid IPv{address.version}")
    except ValueError:
        print(value, "invalid IP address")
```

## Solution 9: JSON Configuration Validator

```python
import json
from pathlib import Path

def validate_config(config):
    errors = []
    warnings = []
    required = {"service", "port", "debug", "environment"}

    if not isinstance(config, dict):
        return ["Configuration must be a JSON object"], warnings

    missing = required - config.keys()
    if missing:
        errors.append(f"Missing keys: {', '.join(sorted(missing))}")

    if "service" in config and (
        not isinstance(config["service"], str) or not config["service"].strip()
    ):
        errors.append("service must be a non-empty string")

    if "port" in config:
        port = config["port"]
        if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
            errors.append("port must be an integer from 1 to 65535")

    if "debug" in config and not isinstance(config["debug"], bool):
        errors.append("debug must be a Boolean")

    if config.get("environment") == "production" and config.get("debug") is True:
        warnings.append("Debug mode is enabled in production")

    return errors, warnings

try:
    config = json.loads(Path("config.json").read_text(encoding="utf-8"))
    errors, warnings = validate_config(config)
    print("Errors:", errors)
    print("Warnings:", warnings)
except FileNotFoundError:
    print("Configuration file not found")
except json.JSONDecodeError:
    print("Invalid JSON")
except OSError:
    print("Unable to read configuration")
```

## Solution 10: Vulnerability CSV Report

```python
import csv
from collections import Counter
from pathlib import Path

severity_counts = Counter()
open_count = 0
priority = []
total = 0

try:
    with Path("findings.csv").open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        required = {"id", "title", "severity", "status"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("CSV is missing required columns")

        for row in reader:
            total += 1
            severity = row["severity"].strip()
            status = row["status"].strip()
            severity_counts[severity] += 1

            if status.casefold() == "open":
                open_count += 1
                if severity in {"Critical", "High"}:
                    priority.append(f"{row['id']}: {row['title']} ({severity})")

    lines = [f"Total findings: {total}", f"Open findings: {open_count}"]
    for severity in ("Critical", "High", "Medium", "Low"):
        lines.append(f"{severity}: {severity_counts[severity]}")
    lines.append("\nOpen Critical and High findings:")
    lines.extend(priority or ["None"])

    report = "\n".join(lines)
    Path("findings_summary.txt").write_text(report + "\n", encoding="utf-8")
    print(report)
except FileNotFoundError:
    print("findings.csv was not found")
except (OSError, ValueError) as error:
    print("Unable to generate report:", error)
```

## Solution 11: File Integrity

```python
import hashlib
from pathlib import Path

def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()

sample = Path("sample.txt")
sample.write_text("Original content\n", encoding="utf-8")
baseline = sha256_file(sample)

sample.write_text("Modified content\n", encoding="utf-8")
current = sha256_file(sample)

print("Integrity check passed" if current == baseline else "File changed")
```

For a real integrity checker, store the baseline in a trusted location and protect it against modification.

## Solution 12: Security Log Summary

```python
import json
from collections import Counter
from pathlib import Path

KNOWN_LEVELS = {"INFO", "WARNING", "ERROR"}

def build_security_summary(path):
    levels = Counter()
    total = 0
    failed_login_events = 0

    with Path(path).open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            parts = line.strip().split(maxsplit=1)
            if len(parts) != 2 or parts[0] not in KNOWN_LEVELS:
                continue

            level, message = parts
            total += 1
            levels[level] += 1
            if "login_failed" in message:
                failed_login_events += 1

    return {
        "total_records": total,
        "levels": {level: levels[level] for level in ("INFO", "WARNING", "ERROR")},
        "failed_login_events": failed_login_events,
    }

try:
    summary = build_security_summary("sample.log")
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))
except FileNotFoundError:
    print("Log file was not found")
except OSError:
    print("Unable to read the log or write the report")
```

This example uses a simple literal match and is not a full detection system.

## Solution 13: Git and Code Quality

Example `.gitignore`:

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
output/
```

Example commands:

```bash
git init
git add README.md examples.md practical.md solutions.md practical.ipynb
git commit -m "Add Python fundamentals learning materials"
```

Review staged files before committing. Never commit credentials, private keys, or sensitive logs.

## Reflection: Key Takeaways

- Lists are mutable; tuples are immutable.
- Exceptions let programs handle expected failures gracefully.
- Virtual environments isolate project dependencies.
- `json.loads()` parses JSON without evaluating arbitrary Python expressions.
- Hashes can detect content differences against a trusted baseline.
- Argument lists for subprocess calls reduce shell-injection risk.
- The main guard prevents the main routine from running on import.
- Failed-login counts need context, correlation, and investigation before drawing conclusions.
