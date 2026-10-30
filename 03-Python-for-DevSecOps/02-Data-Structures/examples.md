# Python Data Structures — Examples

Small, runnable examples for the `02-Data-Structures` module.

## 1. Lists

```python
targets = ["192.0.2.10", "192.0.2.11"]
targets.append("192.0.2.12")
targets[0]                  # '192.0.2.10'
targets[1:]                 # ['192.0.2.11', '192.0.2.12']
```

Lists are ordered and mutable. Indexing is typically O(1); searching and removing an arbitrary value are O(n).

## 2. Tuples

```python
scan_config = ("tcp", 443, 3)
protocol, port, retries = scan_config
print(protocol, port, retries)
```

Tuples are useful for fixed records and can be used as dictionary keys when all their elements are hashable.

## 3. Sets: uniqueness and comparison

```python
observed = {"192.0.2.10", "192.0.2.11", "192.0.2.10"}
approved = {"192.0.2.10", "192.0.2.12"}

duplicates_removed = set(observed)
unexpected = observed - approved
common = observed & approved
all_ips = observed | approved
```

Set membership is typically O(1) on average. Sets do not represent a meaningful sequence order.

## 4. Dictionaries

```python
event = {"event_id": 101, "severity": "high", "source_ip": "192.0.2.10"}
event["severity"]
event["status"] = "open"

for key, value in event.items():
    print(key, value)
```

Dictionary key lookup and insertion are typically O(1) on average.

## 5. Safe lookup with `get`

```python
event = {"severity": "medium"}
severity = event.get("severity", "unknown")
source_ip = event.get("source_ip", "not-provided")
```

Use `get` when a key may be absent and a default is appropriate.

## 6. List and dictionary comprehensions

```python
ports = [22, 80, 443, 8080]
web_ports = [port for port in ports if port in {80, 443, 8080}]

events = [
    {"id": 1, "severity": "high"},
    {"id": 2, "severity": "low"},
    {"id": 3, "severity": "high"},
]
high_severity = [event for event in events if event["severity"] == "high"]
severity_by_id = {event["id"]: event["severity"] for event in events}
```

## 7. Stack (LIFO)

```python
stack = []
stack.append("parse")
stack.append("validate")
stack.append("report")
step = stack.pop()  # 'report'
```

A list is a good simple stack because appending and popping at the end are amortized O(1).

## 8. Queue (FIFO) with `deque`

```python
from collections import deque

queue = deque(["event-A", "event-B"])
queue.append("event-C")
next_event = queue.popleft()  # 'event-A'
```

`deque.popleft()` is O(1), while removing index 0 from a list requires shifting remaining elements.

## 9. Count events with `Counter`

```python
from collections import Counter

severities = ["high", "low", "high", "medium", "high"]
counts = Counter(severities)
counts["high"]      # 3
counts.most_common(2)
```

## 10. Group values with `defaultdict`

```python
from collections import defaultdict

events_by_severity = defaultdict(list)
events = [
    {"id": 1, "severity": "high"},
    {"id": 2, "severity": "low"},
    {"id": 3, "severity": "high"},
]

for event in events:
    events_by_severity[event["severity"]].append(event["id"])

dict(events_by_severity)
```

## 11. Normalize and split log-like text

```python
line = "  WARN  192.0.2.44 login_failed  "
fields = line.strip().split()
level, source_ip, event_type = fields
```

This is a toy example only. Real log formats may require a parser and careful validation.

## 12. Complexity at a glance

| Operation | Typical cost |
|---|---:|
| List index access | O(1) |
| List membership test | O(n) |
| Append/pop at list end | Amortized O(1) |
| Set membership | Average O(1) |
| Dictionary key lookup | Average O(1) |
| `deque.append` / `deque.popleft` | O(1) |
| Sorting a list | O(n log n) |

These are typical average-case descriptions, not guarantees for every possible input.
