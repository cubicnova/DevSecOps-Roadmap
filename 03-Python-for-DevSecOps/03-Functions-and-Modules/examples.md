# Functions and Modules — Code Examples

Run these snippets with Python 3. For examples involving multiple files, create the files in the same directory as shown.

## 1. Define a function

```python
def greet(name):
    """Return a greeting for a user."""
    return f"Hello, {name}!"

print(greet("DevSecOps learner"))
```

Prefer returning a value when callers may need to reuse the result.

## 2. Parameters, defaults, and keyword arguments

```python
def summarize_event(event_type, count=1, source="unknown"):
    return {
        "event_type": event_type,
        "count": count,
        "source": source,
    }

print(summarize_event("login_failed"))
print(summarize_event("file_changed", count=3, source="integrity-check"))
```

## 3. Variable-length arguments

```python
def average(*values):
    if not values:
        raise ValueError("At least one value is required")
    return sum(values) / len(values)

def describe_config(**settings):
    # Example only: don't pass secrets into logging/reporting functions.
    return {key: value for key, value in settings.items()}

print(average(2, 4, 6))
print(describe_config(environment="test", debug=False))
```

## 4. Scope

```python
DEFAULT_THRESHOLD = 5

def needs_review(count):
    """Use a module-level constant without modifying it."""
    return count >= DEFAULT_THRESHOLD

print(needs_review(7))
```

Avoid unnecessary global state; passing dependencies as arguments usually makes code easier to test.

## 5. Type hints and docstrings

```python
def is_valid_port(port: int) -> bool:
    """Return whether port is an integer in the range 1..65535."""
    return isinstance(port, int) and not isinstance(port, bool) and 1 <= port <= 65535

print(is_valid_port(443))
print(is_valid_port(True))  # False
```

Type hints document expectations; Python does not enforce them automatically at runtime.

## 6. Lambda and sorting

```python
findings = [
    {"id": "V-1", "severity": "Medium"},
    {"id": "V-2", "severity": "Critical"},
    {"id": "V-3", "severity": "Low"},
]

ordered = sorted(findings, key=lambda item: item["severity"])
print(ordered)
```

For a fixed severity order, use an explicit mapping rather than alphabetical sorting.

## 7. Recursion with a base case

```python
def factorial(number):
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError("number must be an integer")
    if number < 0:
        raise ValueError("number must be non-negative")
    if number in (0, 1):
        return 1
    return number * factorial(number - 1)

print(factorial(5))
```

For large inputs, iterative solutions may be safer because Python limits recursion depth.

## 8. Import standard-library modules

```python
import hashlib
import ipaddress
from pathlib import Path

print(ipaddress.ip_address("192.0.2.10"))
print(hashlib.sha256(b"example").hexdigest())
print(Path(".").resolve())
```

## 9. Create and import a custom module

Create `validators.py`:

```python
import ipaddress

def is_valid_port(value):
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and 1 <= value <= 65535
    )

def is_valid_ip(value):
    if not isinstance(value, str):
        return False
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False
```

Create `main.py` in the same directory:

```python
from validators import is_valid_ip, is_valid_port

def main():
    print(is_valid_port(443))
    print(is_valid_ip("2001:db8::1"))

if __name__ == "__main__":
    main()
```

Run `python main.py`.

## 10. Use aliases and explicit imports

```python
import json as json_lib
from pathlib import Path

payload = {"service": "api", "debug": False}
text = json_lib.dumps(payload, indent=2)
Path("config-output.json").write_text(text, encoding="utf-8")
```

Prefer explicit imports over `from module import *`, which can obscure where names came from.

## 11. Main guard

```python
def main():
    print("This runs when the file is executed directly.")

if __name__ == "__main__":
    main()
```

When the file is imported, the `main()` call is not executed.

## 12. Reusable file hashing module

Create `hashing.py`:

```python
import hashlib
from pathlib import Path

def sha256_file(path: str | Path) -> str:
    """Return a SHA-256 digest for a file's contents."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

Use it from `main.py`:

```python
from pathlib import Path
from hashing import sha256_file

Path("sample.txt").write_text("test data\n", encoding="utf-8")
print(sha256_file("sample.txt"))
```

A hash comparison can help detect changes relative to a trusted baseline; it does not by itself prove authenticity or safety.

## 13. Custom exceptions

```python
class InvalidFindingError(ValueError):
    """Raised when a finding record fails validation."""

def validate_finding(finding):
    if not isinstance(finding, dict):
        raise InvalidFindingError("Finding must be a dictionary")
    if not finding.get("id"):
        raise InvalidFindingError("Finding requires an id")
    if finding.get("severity") not in {"Critical", "High", "Medium", "Low"}:
        raise InvalidFindingError("Unsupported severity")
    return True

print(validate_finding({"id": "V-1", "severity": "High"}))
```

## 14. Test a function

```python
import unittest

def is_valid_port(value):
    return isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 65535

class TestPortValidator(unittest.TestCase):
    def test_valid_port(self):
        self.assertTrue(is_valid_port(443))

    def test_invalid_boundaries(self):
        self.assertFalse(is_valid_port(0))
        self.assertFalse(is_valid_port(65536))

    def test_reject_bool_and_string(self):
        self.assertFalse(is_valid_port(True))
        self.assertFalse(is_valid_port("443"))

if __name__ == "__main__":
    unittest.main()
```

Save as `test_validators.py` and run `python test_validators.py`.

## Practice challenge

Build a small package that contains reusable IP validation, port validation, file hashing, and report-formatting functions. Import them from a `main.py` entry point and add unit tests for normal, boundary, and invalid inputs.
