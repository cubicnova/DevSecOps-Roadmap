# Solutions — Python Data Structures

Use these after attempting the notebook exercises. Several exercises can have multiple valid solutions.

## 1. Remove duplicate IP addresses while preserving input order

```python
ips = ["192.0.2.10", "192.0.2.11", "192.0.2.10", "192.0.2.12"]
unique_ips = list(dict.fromkeys(ips))
print(unique_ips)
# ['192.0.2.10', '192.0.2.11', '192.0.2.12']
```

A set alone removes duplicates but does not express a guaranteed meaningful order. `dict.fromkeys` preserves first-seen insertion order in modern Python.

## 2. Count event severity

```python
from collections import Counter

events = [
    {"id": 1, "severity": "high"},
    {"id": 2, "severity": "medium"},
    {"id": 3, "severity": "high"},
    {"id": 4, "severity": "low"},
]
severity_counts = Counter(event["severity"] for event in events)
print(dict(severity_counts))
# {'high': 2, 'medium': 1, 'low': 1}
```

## 3. Filter high-severity events

```python
high_events = [event for event in events if event["severity"] == "high"]
```

## 4. Compare observed and approved indicators

```python
observed = {"192.0.2.10", "192.0.2.11", "192.0.2.12"}
approved = {"192.0.2.10", "192.0.2.12", "192.0.2.13"}

unexpected = observed - approved
missing = approved - observed
print(unexpected)  # {'192.0.2.11'}
print(missing)     # {'192.0.2.13'}
```

Set print order may vary.

## 5. Process a queue in FIFO order

```python
from collections import deque

queue = deque(["event-1", "event-2", "event-3"])
processed = []

while queue:
    processed.append(queue.popleft())

print(processed)
# ['event-1', 'event-2', 'event-3']
```

## 6. Create a dictionary indexed by event ID

```python
events_by_id = {event["id"]: event for event in events}
```

Dictionary keys must be hashable. If IDs can be duplicated, a dictionary comprehension keeps only the last value for a duplicate key.

## 7. Validate required fields

```python
required_fields = {"event_id", "severity", "source_ip"}
record = {"event_id": 10, "severity": "high", "source_ip": "192.0.2.10"}

missing_fields = required_fields - record.keys()
is_valid = not missing_fields
```

For real input, also validate value types and formats; field presence alone is not full validation.

## 8. Stack reversal

```python
items = ["a", "b", "c"]
stack = []
for item in items:
    stack.append(item)

reversed_items = []
while stack:
    reversed_items.append(stack.pop())

print(reversed_items)  # ['c', 'b', 'a']
```

## 9. Frequency of words

```python
from collections import Counter

text = "failed login failed access allowed login"
word_counts = Counter(text.split())
print(word_counts["failed"])  # 2
```

For production text, normalize case and punctuation as appropriate for the task.

## 10. Complexity questions

- Why use a set for duplicate removal? Membership checks are typically O(1) on average, making a set-based approach efficient.
- Why use `deque` for a queue? Removing from the left is O(1), unlike `list.pop(0)`, which shifts the remaining elements.
- Why use a dictionary for lookup by ID? Average-case key lookup is O(1).
- Why not always use a set? Sets do not preserve duplicates or provide sequence indexing, and their elements must be hashable.
