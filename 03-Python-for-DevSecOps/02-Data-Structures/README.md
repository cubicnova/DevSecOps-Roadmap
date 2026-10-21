# 02 — Data Structures for Python and DevSecOps

Learn how Python data structures store, organize, and process information, with examples connected to automation and defensive security workflows.

## Learning objectives

By the end of this module, you should be able to:

- Choose an appropriate built-in data structure for a task.
- Create, access, update, and remove values in lists, tuples, sets, and dictionaries.
- Use stacks, queues, and comprehensions for common programming patterns.
- Count events and remove duplicates efficiently.
- Explain common operation costs and make sensible choices for security scripts.

## Topics covered

| Topic | Key ideas | DevSecOps use case |
|---|---|---|
| Lists | Ordered, mutable collections; indexing, slicing, append, remove, sort | Store scan targets or findings |
| Tuples | Ordered, immutable collections | Represent fixed configuration values |
| Sets | Unique values; union, intersection, difference | Deduplicate IPs, compare allowlists |
| Dictionaries | Key-value mapping; lookup, update, iteration | Parse configuration and event records |
| Strings | Immutable sequences; split, strip, search | Normalize log lines and indicators |
| Stack | Last in, first out (LIFO) | Track nested operations or undo steps |
| Queue | First in, first out (FIFO) | Process events in arrival order |
| Comprehensions | Concise collection construction | Filter and transform records |
| `collections` | `Counter`, `defaultdict`, `deque` | Count events and efficiently queue work |
| Complexity | Typical lookup and update costs | Avoid slow processing on large datasets |

## Prerequisites

- Python fundamentals: variables, conditions, loops, functions.
- Python 3.10 or later recommended.
- Jupyter Notebook or JupyterLab for the practical notebook.

## Setup

From your project directory, create and activate a virtual environment if desired, then install Jupyter:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

python -m pip install jupyter
jupyter notebook
```

The notebook uses only Python's standard library, so no third-party packages are required for the exercises.

## Suggested learning path

1. Read [`examples.md`](examples.md) and run each snippet.
2. Open [`practical.ipynb`](practical.ipynb) and complete the TODO cells before checking solutions.
3. Use [`solutions.md`](solutions.md) to review the expected approach.
4. Modify the examples to process a small, fictional security-event dataset.

## Practice project: Security Event Triage

Create a small script that:
- Stores sample security events in a list of dictionaries.
- Uses a set to find unique source IP addresses.
- Uses a dictionary or `Counter` to count events by severity.
- Filters high-severity events.
- Processes a queue of events in arrival order.

Use fictional sample data only. Do not place real credentials, tokens, personal data, or sensitive production logs in this learning repository.

## Quick reference

```python
# List: ordered and mutable
targets = ["192.0.2.10", "192.0.2.11"]
targets.append("192.0.2.12")

# Tuple: ordered and immutable
port_range = (1, 1024)

# Set: unique values
unique_ips = set(["192.0.2.10", "192.0.2.10", "192.0.2.11"])

# Dictionary: key-value mapping
event = {"severity": "high", "source_ip": "192.0.2.10"}

# Stack: LIFO
stack = []
stack.append("first")
stack.append("second")
last_added = stack.pop()

# Queue: FIFO
from collections import deque
queue = deque(["event-1", "event-2"])
first_added = queue.popleft()
```

## Common mistakes

- Assuming sets preserve a meaningful order.
- Trying to mutate a tuple or a string in place.
- Using a list for repeated front-of-queue removals on large workloads; prefer `collections.deque`.
- Modifying a list while iterating over that same list.
- Assuming dictionary keys can be mutable objects such as lists.
- Using real secrets or production data in examples.

## Completion checklist

- [ ] Explain the difference between list, tuple, set, and dictionary.
- [ ] Demonstrate stack and queue operations.
- [ ] Use `Counter` to summarize event severity.
- [ ] Filter and deduplicate sample indicators.
- [ ] Complete all notebook exercises and explain the time/space trade-offs.

## Further reading

- [Python built-in types](https://docs.python.org/3/library/stdtypes.html)
- [Data structures tutorial](https://docs.python.org/3/tutorial/datastructures.html)
- [The `collections` module](https://docs.python.org/3/library/collections.html)
