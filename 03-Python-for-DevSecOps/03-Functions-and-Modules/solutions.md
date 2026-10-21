# Functions and Modules — Solutions

Reference answers for `practical.md`. Attempt the labs independently before using these solutions.

## Solution 1 — Basic function

```python
def greet(name: str) -> str:
    """Return a greeting for the supplied name."""
    return f"Hello, {name}!"

print(greet("Alex"))
print(greet("Sam"))
print(greet("DevSecOps learner"))
```

## Solution 2 — Percentage

```python
def calculate_percentage(part, total):
    if isinstance(part, bool) or isinstance(total, bool):
        raise TypeError("Inputs must be numeric")
    if not isinstance(part, (int, float)) or not isinstance(total, (int, float)):
        raise TypeError("Inputs must be numeric")
    if total == 0:
        raise ValueError("total cannot be zero")
    return part / total * 100
```

A production version may also constrain `part` and `total` according to the business domain.

## Solution 3 — Default and keyword arguments

```python
def format_event(event_type, severity="INFO", source="unknown"):
    if not isinstance(event_type, str) or not event_type.strip():
        raise ValueError("event_type must be a non-empty string")
    return {
        "event_type": event_type,
        "severity": severity,
        "source": source,
    }

print(format_event("service_started"))
print(format_event("login_failed", severity="WARNING", source="auth-service"))
```

## Solution 4 — `*args` and `**kwargs`

```python
def calculate_average(*values):
    if not values:
        raise ValueError("At least one value is required")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) for v in values):
        raise TypeError("All values must be numeric")
    return sum(values) / len(values)

def build_metadata(**fields):
    return dict(fields)

print(calculate_average(2, 4, 6))
print(build_metadata(environment="test", debug=False))
```

## Solution 5 — Scope

```python
DEFAULT_THRESHOLD = 5

def needs_review(count):
    return count >= DEFAULT_THRESHOLD

print(needs_review(3))  # False
print(needs_review(5))  # True
```

The function reads the module-level constant but does not reassign it.

## Solution 6 — Port validation

```python
def is_valid_port(port: int) -> bool:
    """Return True if port is an integer in the valid port range."""
    return (
        isinstance(port, int)
        and not isinstance(port, bool)
        and 1 <= port <= 65535
    )
```

Type hints document the interface but do not enforce runtime types, so explicit validation is still useful.

## Solution 7 — Lambda and custom severity order

```python
findings = [
    {"id": "V-1", "title": "Missing header", "severity": "Medium"},
    {"id": "V-2", "title": "Critical exposure", "severity": "Critical"},
    {"id": "V-3", "title": "Weak setting", "severity": "Low"},
]

by_title = sorted(findings, key=lambda item: item["title"])

severity_rank = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
by_severity = sorted(
    findings,
    key=lambda item: severity_rank.get(item["severity"], 99),
)
print(by_title)
print(by_severity)
```

## Solution 8 — Custom module

`validators.py`:

```python
import ipaddress

def is_valid_port(value):
    return isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 65535

def is_valid_ip(value):
    if not isinstance(value, str):
        return False
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False
```

`main.py`:

```python
from validators import is_valid_ip, is_valid_port

def main():
    print(is_valid_port(443))
    print(is_valid_port(True))
    print(is_valid_ip("192.0.2.10"))
    print(is_valid_ip("not-an-ip"))

if __name__ == "__main__":
    main()
```

Run `python main.py` from the `lab08` directory.

## Solution 9 — Main guard

```python
def make_message():
    return "Reusable module function"

def main():
    print(make_message())

if __name__ == "__main__":
    main()
```

Importing the file defines the functions but does not call `main()`.

## Solution 10 — File hashing module

`hashing.py`:

```python
import hashlib
from pathlib import Path

def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

Caller:

```python
from pathlib import Path
from hashing import sha256_file

path = Path("sample.txt")
path.write_text("baseline\n", encoding="utf-8")
baseline = sha256_file(path)

path.write_text("changed\n", encoding="utf-8")
current = sha256_file(path)

print("Unchanged" if baseline == current else "File contents changed")
```

For real integrity monitoring, protect the baseline from unauthorized modification.

## Solution 11 — Custom exception

```python
class InvalidFindingError(ValueError):
    """Raised when a finding does not match the expected schema."""

def validate_finding(finding):
    if not isinstance(finding, dict):
        raise InvalidFindingError("Finding must be a dictionary")
    if not isinstance(finding.get("id"), str) or not finding["id"].strip():
        raise InvalidFindingError("Finding requires a non-empty id")
    if finding.get("severity") not in {"Critical", "High", "Medium", "Low"}:
        raise InvalidFindingError("Unsupported severity")
    return True
```

## Solution 12 — Unit tests

Save as `test_validators.py` beside `validators.py`:

```python
import unittest
from validators import is_valid_port

class TestPortValidator(unittest.TestCase):
    def test_valid_port(self):
        self.assertTrue(is_valid_port(443))
        self.assertTrue(is_valid_port(1))
        self.assertTrue(is_valid_port(65535))

    def test_invalid_boundaries(self):
        self.assertFalse(is_valid_port(0))
        self.assertFalse(is_valid_port(65536))

    def test_invalid_types(self):
        self.assertFalse(is_valid_port(True))
        self.assertFalse(is_valid_port("443"))
        self.assertFalse(is_valid_port(None))

if __name__ == "__main__":
    unittest.main()
```

Run `python -m unittest -v`.

## Solution 13 — Suggested package implementation

`security_utils/__init__.py`:

```python
from .validators import is_valid_ip, is_valid_port
from .hashing import sha256_file

__all__ = ["is_valid_ip", "is_valid_port", "sha256_file"]
```

`security_utils/validators.py`:

```python
import ipaddress

def is_valid_port(value):
    return isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 65535

def is_valid_ip(value):
    if not isinstance(value, str):
        return False
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False
```

`security_utils/hashing.py`:

```python
import hashlib
from pathlib import Path

def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

`security_utils/reporting.py`:

```python
import json
from pathlib import Path

def write_json_report(data, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path
```

`security_utils/main.py`:

```python
from .validators import is_valid_ip, is_valid_port
from .reporting import write_json_report

def main():
    report = {
        "port_443_valid": is_valid_port(443),
        "documentation_ip_valid": is_valid_ip("192.0.2.10"),
    }
    write_json_report(report, "output/report.json")
    print("Report written to output/report.json")

if __name__ == "__main__":
    main()
```

Run the package from its parent directory with `python -m security_utils.main`. For a production project, add tests, schema validation, logging, and explicit error handling.

## Key takeaways

- Functions encapsulate reusable behavior.
- Modules organize code into importable files.
- Packages organize related modules into directories.
- The main guard separates import-time definitions from script execution.
- Unit tests help protect behavior as security utilities evolve.
- Keep imports explicit, validate inputs, and avoid side effects at import time.
