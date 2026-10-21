# Solutions — Python File Handling

These are reference answers for the exercises in `practical.ipynb`.

## 1. Write and read a text file

```python
from pathlib import Path

sample_path = LAB_DIR / "notes.txt"
sample_path.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
read_back = sample_path.read_text(encoding="utf-8")
print(read_back)
```

## 2. Count lines and non-empty lines

```python
with open(sample_path, "r", encoding="utf-8") as file:
    lines = list(file)

line_count = len(lines)
non_empty_count = sum(1 for line in lines if line.strip())
print(line_count, non_empty_count)
```

For very large files, calculate counts during iteration instead of building a list.

## 3. Append a line

```python
with open(sample_path, "a", encoding="utf-8") as file:
    file.write("delta\n")
```

## 4. Process sample log lines

```python
error_lines = []
with open(log_path, "r", encoding="utf-8") as file:
    for line_number, line in enumerate(file, start=1):
        if "ERROR" in line:
            error_lines.append({"line_number": line_number, "text": line.rstrip()})
```

## 5. Write and read CSV

```python
import csv

with open(csv_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["event_id", "severity", "source_ip"])
    writer.writeheader()
    writer.writerows(events)

with open(csv_path, "r", newline="", encoding="utf-8") as file:
    loaded_events = list(csv.DictReader(file))
```

The CSV reader returns field values as strings unless you convert them.

## 6. Write and read JSON

```python
import json

with open(json_path, "w", encoding="utf-8") as file:
    json.dump(events, file, indent=2)

with open(json_path, "r", encoding="utf-8") as file:
    loaded_events = json.load(file)
```

## 7. Handle missing files and malformed JSON

```python
import json

try:
    with open(LAB_DIR / "missing.json", "r", encoding="utf-8") as file:
        data = json.load(file)
except FileNotFoundError:
    print("Input file was not found.")
except json.JSONDecodeError as exc:
    print(f"Invalid JSON: {exc}")
```

In production, log enough context to diagnose the problem without exposing sensitive file contents.

## 8. Create a severity summary report

```python
from collections import Counter
import json

severity_counts = Counter(event["severity"] for event in events)
summary = {
    "total_events": len(events),
    "unique_source_ips": len({event["source_ip"] for event in events}),
    "severity_counts": dict(severity_counts),
}

with open(summary_path, "w", encoding="utf-8") as file:
    json.dump(summary, file, indent=2)

print(summary)
```

## 9. Concepts to review

- Why use `with open(...)`? It ensures the file is closed reliably.
- What does `w` do? It creates or truncates a file.
- What does `a` do? It appends to a file.
- What does `x` do? It creates a new file and fails if the path already exists.
- Why specify UTF-8? It makes text encoding explicit and portable.
- Why iterate line by line? It limits memory usage for large files.
- Why validate CSV/JSON? Syntactically valid input can still have unexpected fields or types.
- Why use `pathlib`? It provides readable, cross-platform path operations.
