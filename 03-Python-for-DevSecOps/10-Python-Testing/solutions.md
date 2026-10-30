# Solutions — Python Testing

Reference answers for `practical.ipynb`. Attempt each task first.

## 1. Basic assertions

```python
def add(a, b):
    return a + b

assert add(2, 3) == 5
assert add(-1, 1) == 0
```

## 2. Port validation

```python
def validate_port(port):
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an integer")
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    return port
```

```python
import pytest

def test_valid_port():
    assert validate_port(443) == 443

@pytest.mark.parametrize("port", [0, -1, 65536])
def test_invalid_range(port):
    with pytest.raises(ValueError):
        validate_port(port)

@pytest.mark.parametrize("port", ["443", True, None])
def test_invalid_type(port):
    with pytest.raises(TypeError):
        validate_port(port)
```

## 3. Event validation

```python
def is_valid_event(event):
    return (
        isinstance(event, dict)
        and isinstance(event.get("event_id"), int)
        and not isinstance(event.get("event_id"), bool)
        and event.get("severity") in {"low", "medium", "high", "critical"}
    )
```

## 4. Temporary file test

```python
def write_summary(path, text):
    path.write_text(text, encoding="utf-8")

def test_write_summary(tmp_path):
    output = tmp_path / "summary.txt"
    write_summary(output, "test complete")
    assert output.read_text(encoding="utf-8") == "test complete"
```

## 5. Mocked client test

```python
from unittest.mock import Mock

def fetch_status(client, url):
    response = client.get(url, timeout=5)
    response.raise_for_status()
    return response.status_code

def test_fetch_status():
    client = Mock()
    response = client.get.return_value
    response.status_code = 200
    response.raise_for_status.return_value = None

    assert fetch_status(client, "https://example.test/status") == 200
    client.get.assert_called_once_with("https://example.test/status", timeout=5)
```

## 6. Event summary

```python
def summarize_events(events):
    valid = sum(1 for event in events if is_valid_event(event))
    return {"total": len(events), "valid": valid, "invalid": len(events) - valid}
```

## 7. Useful commands

```bash
python -m pytest -q
python -m pytest -v
python -m pytest tests/test_validators.py
python -m unittest discover -s tests -v
```

## Concepts
- Unit tests cover a small component; integration tests verify components working together.
- `pytest.raises()` checks expected exceptions.
- Fixtures provide reusable setup and cleanup.
- `tmp_path` isolates file tests from project files.
- Mocks remove dependency on live services.
- Coverage can reveal untested paths, but high coverage does not guarantee correctness.
