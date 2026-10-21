# Python File Handling — Examples

These examples use Python's standard library. Run them in a practice directory and avoid pointing write operations at important files.

## 1. Write and read a text file

```python
from pathlib import Path

path = Path("sample.txt")
path.write_text("First line\nSecond line\n", encoding="utf-8")
content = path.read_text(encoding="utf-8")
print(content)
```

`Path.write_text()` overwrites the target file. Use it only when replacing the contents is intended.

## 2. Use a context manager

```python
with open("sample.txt", "r", encoding="utf-8") as file:
    for line in file:
        print(line.rstrip("\n"))
```

The context manager closes the file automatically, including when an exception occurs.

## 3. Append to a file

```python
with open("sample.txt", "a", encoding="utf-8") as file:
    file.write("Third line\n")
```

Append mode adds data to the end instead of truncating existing content.

## 4. Create a file only if it does not exist

```python
with open("new-report.txt", "x", encoding="utf-8") as file:
    file.write("Report created\n")
```

If the file already exists, mode `x` raises `FileExistsError`.

## 5. Handle expected errors

```python
from pathlib import Path

path = Path("missing-file.txt")
try:
    text = path.read_text(encoding="utf-8")
except FileNotFoundError:
    print("File does not exist.")
except PermissionError:
    print("Permission denied.")
```

Avoid a broad `except Exception` unless you can handle the failure meaningfully.

## 6. Find files with `pathlib`

```python
from pathlib import Path

folder = Path("logs")
folder.mkdir(parents=True, exist_ok=True)

for path in folder.glob("*.log"):
    print(path.name, path.stat().st_size)
```

Only scan directories that are intended for the task.

## 7. Read and write CSV

```python
import csv

rows = [
    {"event_id": 1, "severity": "high", "source_ip": "192.0.2.10"},
    {"event_id": 2, "severity": "low", "source_ip": "192.0.2.11"},
]

with open("events.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["event_id", "severity", "source_ip"])
    writer.writeheader()
    writer.writerows(rows)

with open("events.csv", "r", newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        print(row)
```

CSV values are usually read as strings. Convert and validate values explicitly when needed.

## 8. Read and write JSON

```python
import json

config = {"timeout_seconds": 10, "retries": 3, "verify_tls": True}

with open("config.json", "w", encoding="utf-8") as file:
    json.dump(config, file, indent=2)

with open("config.json", "r", encoding="utf-8") as file:
    loaded = json.load(file)

print(loaded["timeout_seconds"])
```

For untrusted JSON, catch `json.JSONDecodeError` and validate the resulting data's structure and types.

## 9. Process a large file line by line

```python
matches = []
with open("sample.txt", "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        if "error" in line.lower():
            matches.append((line_number, line.rstrip()))

print(matches)
```

Iterating over the file keeps memory usage lower than loading the entire file into a list.

## 10. Parse fictional log lines

```python
log_lines = [
    "INFO 192.0.2.10 service_started",
    "WARN 192.0.2.11 repeated_login_failure",
    "ERROR 192.0.2.10 policy_violation",
]

for line in log_lines:
    fields = line.split(maxsplit=2)
    if len(fields) == 3:
        level, source_ip, message = fields
        print(level, source_ip, message)
```

Real logs may have quoted fields, timestamps, or embedded spaces; use a format-specific parser when necessary.

## 11. Safely write a new report

```python
import json
from pathlib import Path

report_path = Path("summary.json")
report = {"total_events": 3, "high_severity": 1}

# Mode 'x' prevents accidental overwrite.
with report_path.open("x", encoding="utf-8") as file:
    json.dump(report, file, indent=2)
```

If the report already exists, choose a new filename or deliberately implement a reviewed overwrite policy.

## 12. Binary files

```python
from pathlib import Path

data = Path("sample.bin").read_bytes()
print(f"Read {len(data)} bytes")
```

Binary data should be read with byte APIs or modes such as `rb`/`wb`, not decoded as text without knowing its encoding.
