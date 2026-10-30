# Security Automation - Solutions

These are reference solutions. Try the notebook and practical tasks before reviewing them.

## 1. Input validation

```python
def validate_asset_id(value: str) -> str:
    if not isinstance(value, str):
        raise ValueError("Asset ID must be a string")
    value = value.strip()
    if not value:
        raise ValueError("Asset ID cannot be empty")
    if len(value) > 64:
        raise ValueError("Asset ID is too long")
    return value
```

## 2. Parse JSON with error handling

```python
import json
from pathlib import Path

def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON at line {exc.lineno}, column {exc.colno}") from exc
```

## 3. Severity normalization

```python
SEVERITY_MAP = {
    "critical": "Critical", "crit": "Critical",
    "high": "High",
    "medium": "Medium", "moderate": "Medium",
    "low": "Low",
    "info": "Informational", "informational": "Informational",
}

def normalize_severity(value):
    return SEVERITY_MAP.get(str(value or "").strip().lower(), "Unknown")
```

## 4. Validate, normalize, and deduplicate

```python
def process_findings(records):
    valid, errors = [], []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append({"index": index, "reason": "Record must be an object"})
            continue

        asset = record.get("asset")
        title = record.get("title")
        if not isinstance(asset, str) or not asset.strip():
            errors.append({"index": index, "reason": "Missing asset"})
            continue
        if not isinstance(title, str) or not title.strip():
            errors.append({"index": index, "reason": "Missing title"})
            continue

        valid.append({
            "asset": asset.strip(),
            "title": title.strip(),
            "severity": normalize_severity(record.get("severity")),
        })

    seen, unique = set(), []
    for item in valid:
        key = (item["asset"].casefold(), item["title"].casefold())
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique, errors, len(valid) - len(unique)
```

## 5. Severity summary

```python
from collections import Counter

SEVERITIES = ["Critical", "High", "Medium", "Low", "Informational", "Unknown"]

def severity_summary(records):
    counts = Counter(item["severity"] for item in records)
    return {severity: counts.get(severity, 0) for severity in SEVERITIES}
```

## 6. CSV export

```python
import csv

def write_csv(path, records):
    fields = ["asset", "title", "severity"]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
```

## 7. End-to-end local report generator

```python
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("security_automation")

def main(input_path="sample_findings.json"):
    try:
        raw = json.loads(Path(input_path).read_text(encoding="utf-8"))
        if not isinstance(raw, list):
            raise ValueError("Top-level JSON value must be a list")
        logger.info("Loaded %d input records", len(raw))

        findings, errors, duplicates = process_findings(raw)
        summary = severity_summary(findings)

        write_csv("security_report.csv", findings)
        Path("security_summary.json").write_text(
            json.dumps({"summary": summary, "invalid_count": len(errors),
                        "duplicates_removed": duplicates}, indent=2),
            encoding="utf-8",
        )
        logger.info("Valid findings: %d; invalid records: %d; duplicates: %d",
                    len(findings), len(errors), duplicates)
        logger.info("Wrote security_report.csv and security_summary.json")
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        logger.error("Report generation failed: %s", exc)
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

The functions `process_findings`, `normalize_severity`, `severity_summary`, and `write_csv` are defined above in this file and should be placed before `main()` in a complete script.

## Review question answers

1. Unknown values may indicate a source-format change or a mapping gap. Hiding them can understate risk.
2. Duplicates can inflate counts, waste remediation effort, and make dashboards misleading.
3. Dry runs let operators review intended changes before they affect a real system.
4. Never log passwords, API keys, access tokens, private keys, or unnecessary sensitive payloads.
5. Allowlists constrain scope, timeouts bound waiting, and rate limits reduce service impact.
6. Passing arguments as a list avoids asking a shell to parse a constructed command string; still validate inputs and control the executable.
