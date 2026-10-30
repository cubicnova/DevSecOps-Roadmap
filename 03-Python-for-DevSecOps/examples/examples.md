# Python for DevSecOps - Example Gallery

These examples are deliberately small and use local or synthetic data.

## 1. Variables and collections

```python
assets = ["web-001", "api-001", "db-001"]
asset_count = len(assets)

for asset in assets:
    print(asset)

print("Total assets:", asset_count)
```

## 2. Functions and type hints

```python
def format_finding(asset: str, title: str, severity: str) -> dict:
    return {
        "asset": asset.strip(),
        "title": title.strip(),
        "severity": severity.strip().title(),
    }

finding = format_finding(" web-001 ", "Missing security header", "medium")
print(finding)
```

## 3. Input validation

```python
def validate_port(value: int) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError("Port must be an integer")
    if not 1 <= value <= 65535:
        raise ValueError("Port must be between 1 and 65535")
    return value

print(validate_port(443))
```

## 4. Read a text file safely

```python
from pathlib import Path

path = Path("notes.txt")
try:
    text = path.read_text(encoding="utf-8")
except FileNotFoundError:
    print("File not found:", path)
else:
    print(text)
```

## 5. JSON serialization

```python
import json
from pathlib import Path

config = {
    "environment": "development",
    "logging": {"level": "INFO"},
    "checks_enabled": True,
}

path = Path("config.json")
path.write_text(json.dumps(config, indent=2), encoding="utf-8")
loaded = json.loads(path.read_text(encoding="utf-8"))
print(loaded["environment"])
```

## 6. Read environment variables

```python
import os

environment = os.getenv("APP_ENV", "development")
print("Application environment:", environment)
```

Do not print secret environment variables such as API tokens.

## 7. Logging and exception handling

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)

try:
    result = 10 / 2
except ZeroDivisionError:
    logger.exception("Calculation failed")
else:
    logger.info("Calculation succeeded: %s", result)
```

## 8. Use `pathlib` to inspect a directory

```python
from pathlib import Path

root = Path(".")
for path in sorted(root.iterdir()):
    kind = "directory" if path.is_dir() else "file"
    print(f"{kind}: {path.name}")
```

Only inspect directories that are appropriate for your task.

## 9. Run a local subprocess safely

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

Use a list of arguments, avoid `shell=True` for untrusted input, and apply a timeout. Reference: https://docs.python.org/3/library/subprocess.html#security-considerations

## 10. CSV data processing

```python
import csv
from pathlib import Path

rows = [
    {"asset": "web-001", "severity": "High"},
    {"asset": "api-001", "severity": "Low"},
]

with Path("findings.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=["asset", "severity"])
    writer.writeheader()
    writer.writerows(rows)
```

## 11. Unit test a helper

```python
import unittest

def normalize_severity(value):
    aliases = {"crit": "Critical", "critical": "Critical", "moderate": "Medium"}
    return aliases.get(str(value).strip().lower(), str(value).strip().title())

class TestNormalizeSeverity(unittest.TestCase):
    def test_alias(self):
        self.assertEqual(normalize_severity("crit"), "Critical")

    def test_unknown_label(self):
        self.assertEqual(normalize_severity("low"), "Low")

if __name__ == "__main__":
    unittest.main()
```

## 12. Safe dry-run planning

```python
def plan_action(asset: str, action: str, dry_run: bool = True) -> str:
    if not asset.strip() or not action.strip():
        raise ValueError("Asset and action are required")
    if dry_run:
        return f"[DRY RUN] Would {action} for {asset}"
    raise NotImplementedError("Connect only to an approved, reviewed workflow")

print(plan_action("web-001", "create a remediation ticket"))
```

## Suggested mini-projects

- JSON configuration validator
- Log file summary tool
- CSV findings normalizer
- File integrity checker for a test directory
- Unit-tested security report generator
