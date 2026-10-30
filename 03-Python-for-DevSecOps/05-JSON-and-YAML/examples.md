# JSON and YAML — Code Examples

These examples use Python's built-in `json` module and PyYAML. Install PyYAML with `python -m pip install PyYAML` before running YAML examples.

## 1. Python dictionary to JSON string

```python
import json

config = {
    "service": "web",
    "port": 443,
    "debug": False,
    "allowed_hosts": ["app.example.test", "api.example.test"],
}

text = json.dumps(config, indent=2, sort_keys=True)
print(text)
```

## 2. Parse JSON

```python
import json

payload = '{"event": "login_failed", "count": 3, "active": true}'
data = json.loads(payload)

print(data["event"])
print(data["count"])
print(data["active"])
```

## 3. Read and write JSON files

```python
import json
from pathlib import Path

path = Path("config.json")
config = {"service": "api", "debug": False, "port": 443}

path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
loaded = json.loads(path.read_text(encoding="utf-8"))
print(loaded)
```

For large files, prefer `json.load(file)` and `json.dump(data, file)` rather than reading the whole file into a string.

## 4. Handle malformed JSON

```python
import json

raw = '{"service": "api", "port": }'

try:
    data = json.loads(raw)
except json.JSONDecodeError as error:
    print(f"Invalid JSON at line {error.lineno}, column {error.colno}")
```

## 5. YAML mapping and sequence

```yaml
service: api
port: 443
debug: false
allowed_hosts:
  - app.example.test
  - api.example.test
```

YAML uses indentation to express structure. Use spaces consistently, not tabs.

## 6. Read YAML safely

```python
import yaml

text = """
service: api
port: 443
debug: false
"""

config = yaml.safe_load(text)
print(config["service"])
print(config["port"])
```

Use `safe_load()` for untrusted YAML. Avoid unsafe YAML loaders because YAML can support object construction features beyond plain data.

## 7. Write YAML

```python
import yaml

config = {
    "service": "api",
    "port": 443,
    "debug": False,
    "allowed_hosts": ["app.example.test", "api.example.test"],
}

print(yaml.safe_dump(config, sort_keys=False))
```

## 8. Convert JSON to YAML

```python
import json
import yaml

json_text = '{"service": "web", "port": 443, "debug": false}'
data = json.loads(json_text)
yaml_text = yaml.safe_dump(data, sort_keys=False)
print(yaml_text)
```

## 9. Convert YAML to JSON

```python
import json
import yaml

yaml_text = """
service: web
port: 443
debug: false
"""

data = yaml.safe_load(yaml_text)
json_text = json.dumps(data, indent=2)
print(json_text)
```

## 10. Validate configuration

```python
def validate_config(config):
    errors = []
    warnings = []

    if not isinstance(config, dict):
        return ["Configuration must be a mapping/object"], warnings

    for key in ("service", "port", "debug", "environment"):
        if key not in config:
            errors.append(f"Missing required key: {key}")

    service = config.get("service")
    if "service" in config and (
        not isinstance(service, str) or not service.strip()
    ):
        errors.append("service must be a non-empty string")

    port = config.get("port")
    if "port" in config and (
        isinstance(port, bool)
        or not isinstance(port, int)
        or not 1 <= port <= 65535
    ):
        errors.append("port must be an integer from 1 to 65535")

    if "debug" in config and not isinstance(config["debug"], bool):
        errors.append("debug must be a Boolean")

    if config.get("environment") == "production" and config.get("debug") is True:
        warnings.append("Debug mode is enabled in production")

    return errors, warnings


sample = {
    "service": "web",
    "port": 443,
    "debug": False,
    "environment": "production",
}
print(validate_config(sample))
```

Parsing is only the first step. Validate types, allowed values, and policy requirements separately.

## 11. Parse a vulnerability JSON report

```python
import json
from collections import Counter

report = {
    "findings": [
        {"id": "V-001", "severity": "High", "status": "Open"},
        {"id": "V-002", "severity": "Medium", "status": "Open"},
        {"id": "V-003", "severity": "Critical", "status": "Closed"},
    ]
}

counts = Counter()
open_count = 0

for finding in report["findings"]:
    counts[finding["severity"]] += 1
    if finding["status"].casefold() == "open":
        open_count += 1

summary = {"by_severity": dict(counts), "open_findings": open_count}
print(json.dumps(summary, indent=2))
```

In production, validate the report structure before indexing keys.

## 12. Safe file loader with error handling

```python
import json
from pathlib import Path

def load_json_file(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise FileNotFoundError("Configuration file was not found")
    except json.JSONDecodeError as error:
        raise ValueError("Configuration contains malformed JSON") from error
    except OSError as error:
        raise OSError("Configuration file could not be read") from error
```

Do not include secret values in error messages or logs.

## Practice challenge

Create a validator that accepts either JSON or YAML configuration, verifies required keys and value types, and produces a concise report. Use `json.loads()` for JSON and `yaml.safe_load()` for YAML. Test missing files, malformed syntax, wrong data types, and production debug mode.
