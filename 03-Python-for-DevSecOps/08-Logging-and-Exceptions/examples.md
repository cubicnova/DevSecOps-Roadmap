# Logging and Exceptions — Python Examples

All examples use Python's standard library.

## 1. Basic exception handling

```python
raw_value = "42"

try:
    value = int(raw_value)
except ValueError:
    print("Input must be an integer.")
else:
    print("Parsed value:", value)
finally:
    print("Conversion attempt finished.")
```

`else` runs only when `try` succeeds. `finally` runs whether it succeeds or fails.

## 2. Raise an exception for invalid input

```python
def validate_port(port):
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an integer")
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return port
```

## 3. Custom exception

```python
class ConfigurationError(Exception):
    """Raised when required application configuration is invalid."""

def require_api_url(config):
    url = config.get("api_url")
    if not isinstance(url, str) or not url.startswith("https://"):
        raise ConfigurationError("A valid HTTPS API URL is required")
    return url
```

Avoid including secret configuration values in exception messages.

## 4. Configure logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("event_processor")

logger.debug("Detailed diagnostic")
logger.info("Processing started")
logger.warning("Optional field missing")
logger.error("Could not process record")
```

## 5. Log an exception traceback

```python
import logging
logger = logging.getLogger(__name__)

try:
    int("not-a-number")
except ValueError:
    logger.exception("Could not parse numeric input")
```

Call `logger.exception()` from inside an exception handler.

## 6. Avoid leaking secrets

```python
import logging
logger = logging.getLogger(__name__)
token = "example-token-do-not-use"

# Avoid: logger.info("Using token %s", token)
logger.info("Authentication token loaded")
```

Never log real tokens, passwords, private keys, or complete authorization headers.

## 7. Log to a file

```python
import logging

logger = logging.getLogger("file_job")
logger.setLevel(logging.INFO)
handler = logging.FileHandler("application.log", encoding="utf-8")
handler.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s %(name)s: %(message)s"
))
logger.addHandler(handler)

logger.info("Job started")
handler.close()
logger.removeHandler(handler)
```

For reusable applications, manage handler lifecycle carefully and avoid adding duplicate handlers each time a function runs.

## 8. Rotate log files

```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("rotating_job")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    "rotating.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8"
)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
logger.addHandler(handler)
logger.info("Rotating log handler configured")
```

## 9. Exception chaining

```python
class EventFormatError(Exception):
    pass

def parse_event_id(raw_id):
    try:
        return int(raw_id)
    except (TypeError, ValueError) as exc:
        raise EventFormatError("Event ID must be an integer") from exc
```

`raise ... from exc` preserves the original cause.

## 10. Process records defensively

```python
import logging
logger = logging.getLogger("triage")

def process_record(record):
    if not isinstance(record, dict):
        logger.warning("Skipped record with unexpected type")
        return False
    event_id = record.get("event_id")
    if not isinstance(event_id, int) or isinstance(event_id, bool):
        logger.warning("Skipped record with invalid event_id")
        return False
    logger.info("Validated event_id=%s", event_id)
    return True
```

Avoid logging raw payloads.

## 11. Test an expected exception

```python
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("b must not be zero")
    return a / b

try:
    divide(5, 0)
except ZeroDivisionError as exc:
    assert "zero" in str(exc)
else:
    raise AssertionError("Expected ZeroDivisionError")
```

## 12. Distinguish expected and unexpected failures

Catch only exceptions you can handle appropriately. Let unexpected failures propagate when continuing would leave the application in an invalid state.
