# Solutions — Logging and Exceptions

Reference solutions for `practical.ipynb`.

## 1. Convert input with exception handling

```python
def parse_count(raw):
    try:
        return int(raw)
    except (TypeError, ValueError):
        return None
```

A `finally` block is unnecessary when there is no cleanup to perform.

## 2. Validate a port

```python
def validate_port(port):
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an integer")
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return port
```

## 3. Custom exception with chaining

```python
class EventFormatError(Exception):
    pass

def parse_event_id(raw_id):
    try:
        return int(raw_id)
    except (TypeError, ValueError) as exc:
        raise EventFormatError("Invalid event ID") from exc
```

## 4. Configure a logger

```python
import logging

logger = logging.getLogger("security_lab")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
    ))
    logger.addHandler(handler)

logger.info("Processor initialized")
```

Checking for existing handlers avoids duplicate output when rerunning a notebook cell.

## 5. Validate events without logging raw payloads

```python
def validate_event(event, logger):
    if not isinstance(event, dict):
        logger.warning("Rejected event: expected dictionary")
        return False
    if not isinstance(event.get("event_id"), int) or isinstance(event.get("event_id"), bool):
        logger.warning("Rejected event: invalid event_id")
        return False
    if event.get("severity") not in {"low", "medium", "high", "critical"}:
        logger.warning("Rejected event_id=%s: invalid severity", event["event_id"])
        return False
    return True
```

Follow your organization's policy even when deciding whether identifiers are safe to log.

## 6. Count event severities

```python
from collections import Counter

valid_events = [event for event in events if validate_event(event, logger)]
severity_counts = Counter(event["severity"] for event in valid_events)
logger.info("Severity summary: %s", dict(severity_counts))
```

## 7. Expected exceptions

```python
def read_required_key(record, key):
    try:
        return record[key]
    except KeyError as exc:
        raise ValueError(f"Required field missing: {key}") from exc
```

Avoid including the full record in the exception message.

## 8. Concepts to review

- `except` handles a matching exception.
- `else` runs only if `try` raises no exception.
- `finally` is for cleanup that must happen regardless of success or failure.
- `logger.exception()` adds traceback information and belongs inside an exception handler.
- `WARNING` indicates a concerning condition; `ERROR` indicates a failed operation.
- Log enough context to investigate failures, but never expose secrets or unnecessary sensitive content.
