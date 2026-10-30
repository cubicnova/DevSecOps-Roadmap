# Security Automation - Examples

These examples use synthetic data and local files. They do not scan external systems.

## 1. Basic structured logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("security_automation")

logger.info("Starting report generation")
logger.warning("A sample finding needs review")
```

Avoid putting secrets, session tokens, or sensitive payloads in logs.

## 2. Validate a simple input

```python
def validate_asset_id(asset_id: str) -> str:
    asset_id = asset_id.strip()
    if not asset_id:
        raise ValueError("Asset ID cannot be empty")
    if len(asset_id) > 64:
        raise ValueError("Asset ID is too long")
    return asset_id

print(validate_asset_id(" app-001 "))
```

Validation should be specific to the data type and the operation being performed.

## 3. Load JSON findings

```python
import json
from pathlib import Path

sample = [
    {"asset": "app-001", "title": "Missing security header", "severity": "medium"},
    {"asset": "api-001", "title": "Verbose error response", "severity": "low"},
]

path = Path("findings.json")
path.write_text(json.dumps(sample, indent=2), encoding="utf-8")

records = json.loads(path.read_text(encoding="utf-8"))
print(f"Loaded {len(records)} records")
```

For production data, validate the schema and handle missing or malformed fields.

## 4. Normalize severity labels

```python
SEVERITY_MAP = {
    "critical": "Critical",
    "crit": "Critical",
    "high": "High",
    "medium": "Medium",
    "moderate": "Medium",
    "low": "Low",
    "info": "Informational",
    "informational": "Informational",
}

def normalize_severity(value):
    key = str(value or "").strip().lower()
    return SEVERITY_MAP.get(key, "Unknown")

print(normalize_severity("moderate"))  # Medium
```

Keep unknown values visible rather than silently assigning them a severity.

## 5. Deduplicate findings

```python
def finding_key(item):
    return (
        str(item.get("asset", "")).strip().lower(),
        str(item.get("title", "")).strip().lower(),
    )

def deduplicate(records):
    seen = set()
    unique = []
    for record in records:
        key = finding_key(record)
        if key not in seen:
            seen.add(key)
            unique.append(record)
    return unique
```

Choose a key that reflects your workflow. In real systems, include a stable finding ID when one is available.

## 6. Summarize severity

```python
from collections import Counter

records = [
    {"severity": "High"},
    {"severity": "high"},
    {"severity": "Medium"},
    {"severity": "Informational"},
]

counts = Counter(normalize_severity(r.get("severity")) for r in records)
for severity in ("Critical", "High", "Medium", "Low", "Informational", "Unknown"):
    print(f"{severity}: {counts.get(severity, 0)}")
```

## 7. Write a CSV report

```python
import csv

rows = [
    {"asset": "app-001", "title": "Missing security header", "severity": "Medium"},
    {"asset": "api-001", "title": "Verbose error response", "severity": "Low"},
]

fields = ["asset", "title", "severity"]
with open("report.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
```

## 8. Dry-run before taking an action

```python
def schedule_action(asset, action, dry_run=True):
    if dry_run:
        print(f"[DRY RUN] Would {action} for {asset}")
        return
    # Put an approved, well-scoped implementation here.
    print(f"[ACTION] {action} for {asset}")

schedule_action("app-001", "open a remediation ticket")
```

A dry run should show the proposed action without making changes.

## 9. Use a subprocess safely when it is genuinely required

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

Use a list of arguments, a timeout, and `shell=False` (the default). Do not concatenate untrusted input into a shell command. See the official Python security notes: https://docs.python.org/3/library/subprocess.html#security-considerations

## 10. Mini-project design

Build a local report generator that:

1. Reads synthetic findings from JSON.
2. Validates each record.
3. Normalizes severity.
4. Removes duplicates.
5. Produces a severity summary.
6. Writes a sanitized CSV report.
7. Logs counts and errors without exposing secrets.
