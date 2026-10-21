# Python for DevSecOps — Suggested Solutions

These are reference implementations. Alternative solutions are welcome if they are clear, tested, and safe.

## 1. Input validation

```python
def validate_port(value):
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("port must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return port
```

## 2. Count log levels

```python
def count_levels(lines):
    levels = ("DEBUG", "INFO", "WARNING", "ERROR")
    counts = dict.fromkeys(levels, 0)
    for line in lines:
        upper = line.upper()
        for level in levels:
            if level in upper:
                counts[level] += 1
                break
    return counts
```

## 3. Deduplicate in original order

```python
def unique_in_order(items):
    seen, result = set(), []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

## 4. Summarize findings

```python
from collections import Counter

def summarize_findings(findings):
    return dict(Counter(
        str(item.get("severity") or "Unknown").title()
        for item in findings
    ))
```

## 5. Redact secrets

```python
import re

_PATTERN = re.compile(
    r"(?i)\b(api_key|token|password)(\s*=\s*)([^\s&,;]+)"
)

def redact(text):
    return _PATTERN.sub(lambda m: m.group(1) + m.group(2) + "[REDACTED]", text)
```

## 6. Parse CSV inventory

```python
import csv

def group_assets_by_environment(path):
    required = {"asset", "environment", "owner"}
    grouped = {}
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(f"CSV must contain columns: {sorted(required)}")
        for row in reader:
            env = (row.get("environment") or "Unknown").strip()
            grouped.setdefault(env, []).append({
                "asset": (row.get("asset") or "").strip(),
                "owner": (row.get("owner") or "").strip(),
            })
    return grouped
```

## 7. Validate JSON configuration

```python
import json

def load_config(path):
    try:
        with open(path, encoding="utf-8") as handle:
            config = json.load(handle)
    except json.JSONDecodeError as exc:
        raise ValueError("configuration is not valid JSON") from exc

    if not isinstance(config, dict):
        raise ValueError("configuration must be a JSON object")
    if "timeout_seconds" not in config or "retries" not in config:
        raise ValueError("missing timeout_seconds or retries")

    timeout, retries = config["timeout_seconds"], config["retries"]
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or timeout <= 0:
        raise ValueError("timeout_seconds must be positive")
    if isinstance(retries, bool) or not isinstance(retries, int) or retries < 0:
        raise ValueError("retries must be a non-negative integer")
    return config
```

## 8. Stream a SHA-256 hash

```python
import hashlib

def sha256_file(path, chunk_size=1024 * 1024):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

## 9. File extension report

```python
from collections import Counter
from pathlib import Path

def extension_report(root):
    counts = Counter()
    for path in Path(root).rglob("*"):
        try:
            if path.is_symlink() or not path.is_file():
                continue
            counts[path.suffix.lower() or "[no extension]"] += 1
        except OSError:
            continue
    return dict(sorted(counts.items()))
```

## 10. Parse integer list

```python
def parse_int_list(values):
    result = []
    for index, value in enumerate(values):
        try:
            result.append(int(value))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid integer at index {index}") from exc
    return result
```

## 11. Structured logging

```python
import logging

logger = logging.getLogger("security_automation")

def record_event(event_type, status):
    # Keep event_type/status controlled and non-sensitive.
    logger.info("event_type=%s status=%s", event_type, status)
```

## 12. Retry helper

```python
import time

def retry(operation, attempts, transient=(TimeoutError, ConnectionError), delay=0):
    if not isinstance(attempts, int) or isinstance(attempts, bool) or attempts < 1:
        raise ValueError("attempts must be a positive integer")
    for attempt in range(attempts):
        try:
            return operation()
        except transient:
            if attempt == attempts - 1:
                raise
            if delay > 0:
                time.sleep(delay)
```

## 13. Unit tests

```python
import unittest

class UtilityTests(unittest.TestCase):
    def test_port(self):
        self.assertEqual(validate_port("443"), 443)

    def test_port_invalid(self):
        with self.assertRaises(ValueError):
            validate_port("0")

    def test_redaction(self):
        result = redact("token=abc123")
        self.assertNotIn("abc123", result)
        self.assertIn("[REDACTED]", result)

    def test_parse_ints(self):
        self.assertEqual(parse_int_list(["1", "2"]), [1, 2])

    def test_parse_ints_invalid(self):
        with self.assertRaises(ValueError):
            parse_int_list(["1", "nope"])
```

## 14. Interpret HTTP status without network access

```python
def classify_status(status):
    if not isinstance(status, int) or isinstance(status, bool):
        raise ValueError("status must be an integer")
    if 200 <= status < 300:
        return "ok"
    if status in (408, 429) or 500 <= status < 600:
        return "retry"
    return "fail"
```

## 15. Summarize synthetic security events

```python
from collections import Counter

def summarize_events(events):
    counts = Counter()
    for index, event in enumerate(events):
        if not isinstance(event, dict):
            raise ValueError(f"event {index} must be an object")
        for field in ("timestamp", "source", "event_type"):
            if not event.get(field):
                raise ValueError(f"event {index} missing {field}")
        counts[str(event["event_type"])] += 1
    return dict(sorted(counts.items()))
```

## 16. Configuration diff without values

```python
def config_changes(before, after):
    keys = set(before) | set(after)
    return {
        key: (
            "added" if key not in before
            else "removed" if key not in after
            else "changed"
        )
        for key in sorted(keys)
        if key not in before or key not in after or before[key] != after[key]
    }
```

## 17. CLI validation

```python
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error("directory must exist and be a directory")
    print("Input directory validated")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

## 18. Defensive URL validation

```python
from urllib.parse import urlparse

def allowed_https_url(value, allowed_hosts):
    parsed = urlparse(value)
    hosts = {host.lower() for host in allowed_hosts}
    return (
        parsed.scheme.lower() == "https"
        and parsed.hostname is not None
        and parsed.hostname.lower() in hosts
        and parsed.username is None
        and parsed.password is None
    )
```

## Mini-project implementation guidance

For exercises 19–21, separate parsing, validation, transformation, and output into functions. Add tests for malformed input, empty files, unreadable paths, and secret redaction. Write output to a user-selected destination and avoid overwriting input files.
