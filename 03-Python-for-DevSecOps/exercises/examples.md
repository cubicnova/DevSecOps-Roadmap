# Python for DevSecOps — Exercise Examples

These are small starter examples, not complete solutions to every exercise. Use synthetic data and authorized environments only.

## 1. Validate a port

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
LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")

def count_levels(lines):
    counts = {level: 0 for level in LEVELS}
    for line in lines:
        for level in LEVELS:
            if level in line:
                counts[level] += 1
                break
    return counts
```

## 3. Preserve order while deduplicating

```python
def unique_in_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
```

## 4. Redact common key-value secrets

```python
import re

SECRET_PATTERN = re.compile(
    r"(?i)\b(api_key|token|password)\s*=\s*([^\s&,;]+)"
)

def redact(text):
    return SECRET_PATTERN.sub(r"\1=[REDACTED]", text)
```

## 5. Stream a file hash

```python
import hashlib

def sha256_file(path, chunk_size=1024 * 1024):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()
```

## 6. Safe URL allowlist check

```python
from urllib.parse import urlparse

def allowed_https_url(value, allowed_hosts):
    parsed = urlparse(value)
    return (
        parsed.scheme == "https"
        and parsed.hostname is not None
        and parsed.hostname.lower() in {h.lower() for h in allowed_hosts}
        and parsed.username is None
        and parsed.password is None
    )
```

## 7. Test a function

```python
import unittest

class PortTests(unittest.TestCase):
    def test_valid_port(self):
        self.assertEqual(validate_port("443"), 443)

    def test_out_of_range(self):
        with self.assertRaises(ValueError):
            validate_port("70000")

if __name__ == "__main__":
    unittest.main()
```

## Practice guidance

For every exercise, include at least:
- one expected-success example;
- one invalid-input example;
- one edge case;
- a short explanation of assumptions.
