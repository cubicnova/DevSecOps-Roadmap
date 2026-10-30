# Python for DevSecOps - Reference Solutions

Try each exercise first. These are compact reference implementations.

## Task 1: Asset inventory

```python
assets = ["web-003", "api-001", "db-002", "web-001", "worker-001"]
for asset in sorted(assets):
    print(asset)
print("Count:", len(assets))
```

## Task 2: Reusable helper

```python
def format_finding(asset, title, severity):
    if not all(isinstance(x, str) and x.strip() for x in (asset, title, severity)):
        raise ValueError("All fields must be non-empty strings")
    return {
        "asset": asset.strip(),
        "title": title.strip(),
        "severity": severity.strip().title(),
    }
```

## Task 3: Validate a port

```python
def validate_port(value):
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError("Port must be an integer")
    if not 1 <= value <= 65535:
        raise ValueError("Port must be between 1 and 65535")
    return value
```

## Task 4: File handling

```python
from pathlib import Path

path = Path("notes.txt")
path.write_text("Practice file handling safely.\\n", encoding="utf-8")
try:
    print(path.read_text(encoding="utf-8"))
except OSError as exc:
    print(f"Could not read file: {exc}")
```

## Task 5: JSON configuration

```python
import json
from pathlib import Path

config = {
    "environment": "development",
    "log_level": "INFO",
    "checks_enabled": True,
}
path = Path("config.json")
path.write_text(json.dumps(config, indent=2), encoding="utf-8")
loaded = json.loads(path.read_text(encoding="utf-8"))

required = {"environment", "log_level", "checks_enabled"}
missing = required - loaded.keys()
if missing:
    raise ValueError(f"Missing keys: {sorted(missing)}")
```

## Task 6: Environment variable

```python
import os
environment = os.getenv("APP_ENV", "development")
print("Environment:", environment)
```

## Task 7: Logging

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

try:
    number = int("42")
except ValueError:
    logger.error("Input must be an integer")
else:
    logger.info("Parsed number successfully")
```

## Task 8: CSV findings

```python
import csv
from collections import Counter
from pathlib import Path

rows = [
    {"asset": "web-001", "severity": "High"},
    {"asset": "api-001", "severity": "Low"},
    {"asset": "db-001", "severity": "High"},
]
path = Path("findings.csv")
with path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["asset", "severity"])
    writer.writeheader()
    writer.writerows(rows)

with path.open(newline="", encoding="utf-8") as handle:
    counts = Counter(row["severity"] for row in csv.DictReader(handle))
print(dict(counts))
```

## Task 9: Unit testing

```python
import unittest

def normalize_severity(value):
    aliases = {
        "crit": "Critical", "critical": "Critical",
        "moderate": "Medium", "medium": "Medium",
        "low": "Low", "info": "Informational",
    }
    return aliases.get(str(value or "").strip().lower(), "Unknown")

class TestSeverity(unittest.TestCase):
    def test_alias(self):
        self.assertEqual(normalize_severity("crit"), "Critical")

    def test_regular_value(self):
        self.assertEqual(normalize_severity("low"), "Low")

    def test_unknown(self):
        self.assertEqual(normalize_severity("something-new"), "Unknown")

if __name__ == "__main__":
    unittest.main()
```

## Task 10: Safe subprocess

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "--version"],
    capture_output=True,
    text=True,
    timeout=5,
    check=False,
)
print(result.stdout.strip() or result.stderr.strip())
```

## Task 11: Dry-run planner

```python
def plan_action(asset, action, dry_run=True):
    if not isinstance(asset, str) or not asset.strip():
        raise ValueError("Asset is required")
    if not isinstance(action, str) or not action.strip():
        raise ValueError("Action is required")
    if dry_run:
        return f"[DRY RUN] Would {action.strip()} for {asset.strip()}"
    raise NotImplementedError("Real actions are intentionally disabled")
```

## Task 12: Capstone outline

Use `json.loads` to load the input, validate that the top-level value is a list, normalize records, and deduplicate by a stable key such as `(asset.casefold(), title.casefold())`. Use `csv.DictWriter` for CSV output and `json.dumps` for the summary. Catch `OSError`, `json.JSONDecodeError`, and validation errors at the application boundary. Log counts and error categories, not secrets or full sensitive payloads.
