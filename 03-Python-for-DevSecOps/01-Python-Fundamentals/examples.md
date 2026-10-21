# Python Fundamentals — Code Examples

These examples are for the `01-Python-Fundamentals` module. Run them with Python 3.

## 1. Hello World

```python
# A simple Python program
print("Hello, DevSecOps!")
```

## 2. Variables and Data Types

```python
username = "analyst"
failed_attempts = 5
cpu_usage = 72.5
monitoring_enabled = True
result = None

print(type(username))
print(type(failed_attempts))
print(type(cpu_usage))
print(type(monitoring_enabled))
print(type(result))
```

## 3. Operators and Conditions

```python
failed = 8
threshold = 5

print(failed > threshold)
print(failed > 0 and threshold > 0)

status = "review" if failed > threshold else "normal"
print(status)
```

## 4. Strings

```python
service = "authentication"
status_code = 401

message = f"Service: {service}, status: {status_code}"
print(message)
print(service.upper())
print(message.startswith("Service"))
```

Do not put passwords, tokens, or other secrets into log messages.

## 5. Data Structures

```python
services = ["web", "api", "database"]
services.append("monitoring")

ports = (22, 80, 443)
severities = {"high", "medium", "high"}

finding = {"id": "VULN-001", "severity": "high", "status": "open"}

print(services)
print(ports)
print(severities)
print(finding["severity"])
```

## 6. Loops

```python
failed_attempts = [0, 2, 7, 1, 9]

for count in failed_attempts:
    if count >= 5:
        print(f"Review required: {count} failed attempts")
```

## 7. Functions

```python
def classify_severity(score):
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError("Score must be numeric")
    if not 0 <= score <= 10:
        raise ValueError("Score must be between 0 and 10")
    if score >= 9:
        return "critical"
    if score >= 7:
        return "high"
    if score >= 4:
        return "medium"
    return "low"

print(classify_severity(9.5))
```

## 8. Exception Handling

```python
def parse_attempts(value):
    try:
        attempts = int(value)
        if attempts < 0:
            raise ValueError("Attempts cannot be negative")
        return attempts
    except ValueError as error:
        print(f"Invalid attempt count: {error}")
        return None

print(parse_attempts("4"))
print(parse_attempts("unknown"))
```

## 9. File Handling

```python
from pathlib import Path

path = Path("status.txt")
path.write_text("Security monitoring enabled\n", encoding="utf-8")
print(path.read_text(encoding="utf-8"))
```

## 10. JSON

```python
import json

configuration = {"service": "web", "debug": False, "port": 443}
serialized = json.dumps(configuration, indent=2)
print(serialized)

parsed = json.loads(serialized)
print(parsed["port"])
```

Never use `eval()` to parse JSON or untrusted input.

## 11. CSV

```python
import csv
from pathlib import Path

rows = [
    {"event": "login_failed", "count": 7},
    {"event": "login_success", "count": 12},
]

path = Path("events.csv")
with path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["event", "count"])
    writer.writeheader()
    writer.writerows(rows)

with path.open("r", newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        print(row["event"], row["count"])
```

## 12. IP Address Validation

```python
import ipaddress

for value in ["192.0.2.10", "999.1.1.1", "2001:db8::1"]:
    try:
        address = ipaddress.ip_address(value)
        print(f"{value}: valid IPv{address.version}")
    except ValueError:
        print(f"{value}: invalid IP address")
```

## 13. SHA-256 File Hashing

```python
import hashlib
from pathlib import Path

def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()

Path("sample.txt").write_text("Example content\n", encoding="utf-8")
print(sha256_file("sample.txt"))
```

A hash can help identify changes against a trusted baseline. It does not prove a file is safe or authentic by itself.

## 14. Safe Subprocess Usage

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "--version"],
    capture_output=True,
    text=True,
    check=True,
)
print(result.stdout or result.stderr)
```

Prefer argument lists over shell command strings. Do not pass untrusted input into shell commands.

## Practice Challenge

Read synthetic log events from a file, count levels, validate candidate IP addresses, write a JSON summary, and handle missing files and malformed records.
