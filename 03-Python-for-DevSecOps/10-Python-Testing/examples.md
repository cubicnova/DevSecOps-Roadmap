# Python Testing — Examples

Install pytest with `python -m pip install pytest`.

## 1. Basic function and test

`math_utils.py`:
```python
def add(a, b):
    return a + b
```

`test_math_utils.py`:
```python
from math_utils import add

def test_add_two_numbers():
    assert add(2, 3) == 5
```

Run with `python -m pytest -q`.

## 2. Validate ports and test exceptions

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

def test_port_zero_rejected():
    with pytest.raises(ValueError):
        validate_port(0)

def test_bool_is_not_a_port():
    with pytest.raises(TypeError):
        validate_port(True)
```

## 3. Parameterized tests

```python
import pytest

@pytest.mark.parametrize("port", [1, 22, 80, 443, 65535])
def test_valid_port_boundaries(port):
    assert validate_port(port) == port
```

## 4. Test with unittest

```python
import unittest

def normalize_name(value):
    return value.strip().lower()

class TestNormalizeName(unittest.TestCase):
    def test_strips_and_lowercases(self):
        self.assertEqual(normalize_name("  ADMIN "), "admin")
```

## 5. Use a pytest fixture

```python
import pytest

@pytest.fixture
def sample_event():
    return {"event_id": 7, "severity": "high"}

def test_event_has_severity(sample_event):
    assert sample_event["severity"] == "high"
```

## 6. Test file handling with tmp_path

```python
def write_summary(path, text):
    path.write_text(text, encoding="utf-8")

def test_write_summary(tmp_path):
    output = tmp_path / "summary.txt"
    write_summary(output, "all clear")
    assert output.read_text(encoding="utf-8") == "all clear"
```

## 7. Mock an external dependency

```python
from unittest.mock import Mock

def fetch_status(client, url):
    response = client.get(url, timeout=5)
    response.raise_for_status()
    return response.status_code

def test_fetch_status():
    client = Mock()
    client.get.return_value.status_code = 200
    client.get.return_value.raise_for_status.return_value = None

    assert fetch_status(client, "https://example.test/status") == 200
    client.get.assert_called_once_with("https://example.test/status", timeout=5)
```

This does not make a real network request.

## 8. Validate fictional event records

```python
def is_valid_event(event):
    return (
        isinstance(event, dict)
        and isinstance(event.get("event_id"), int)
        and not isinstance(event.get("event_id"), bool)
        and event.get("severity") in {"low", "medium", "high", "critical"}
    )

def test_missing_severity_is_invalid():
    assert is_valid_event({"event_id": 1}) is False
```

## 9. Test expected exceptions with unittest

```python
import unittest

class TestParseCount(unittest.TestCase):
    def test_invalid_count_raises(self):
        with self.assertRaises(ValueError):
            int("not-a-number")
```

## 10. Run tests

```bash
python -m pytest -v
python -m pytest -q
python -m unittest discover -s tests -v
```

Investigate failures rather than weakening tests without understanding the cause.
