# JSON and YAML — Solutions

Reference implementations for `practical.md`. Attempt each lab before consulting the answer.

## Solution 1 — JSON basics

```python
import json

config = {
    "service": "api",
    "port": 443,
    "debug": False,
    "environment": "development",
}

text = json.dumps(config, indent=2)
print(text)

parsed = json.loads(text)
print(parsed)
```

Python `None` serializes to JSON `null`; Python booleans serialize to lowercase JSON `true` and `false`.

## Solution 2 — JSON file handling

```python
import json
from pathlib import Path

path = Path("config.json")
config = {"service": "api", "port": 443, "debug": False}

with path.open("w", encoding="utf-8") as file:
    json.dump(config, file, indent=2)

try:
    with path.open("r", encoding="utf-8") as file:
        loaded = json.load(file)
    print(loaded)
except FileNotFoundError:
    print("Configuration file not found")
except json.JSONDecodeError:
    print("Malformed JSON")
except OSError:
    print("Unable to read configuration file")
```

## Solution 3 — Malformed JSON

```python
import json

samples = [
    '{"service": "api", "port": 443}',
    '{"service": "api", "port": }',
    "{'service': 'api'}",
    '{"debug": True}',
]

for sample in samples:
    try:
        print("Valid:", json.loads(sample))
    except json.JSONDecodeError as error:
        print("Invalid JSON:", error.msg)
```

Only the first string is valid JSON. JSON requires double-quoted keys and strings and lowercase `true`, `false`, and `null`.

## Solution 4 — YAML structure

```python
import yaml

text = """
service: api
port: 443
debug: false
allowed_hosts:
  - app.example.test
  - api.example.test
owner:
  team: platform-security
  contact: security@example.test
"""

config = yaml.safe_load(text)
print(config["service"])
print(config["allowed_hosts"])
print(config["owner"]["team"])
```

## Solution 5 — YAML file handling

```python
import yaml
from pathlib import Path

path = Path("config.yaml")
config = {"service": "api", "port": 443, "debug": False}

path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")

try:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    print(loaded)
except FileNotFoundError:
    print("Configuration file not found")
except yaml.YAMLError:
    print("Malformed YAML")
except OSError:
    print("Unable to read configuration file")
```

## Solution 6 — JSON/YAML conversion

```python
import json
import yaml

json_text = '{"service": "api", "port": 443, "debug": false}'
data = json.loads(json_text)

yaml_text = yaml.safe_dump(data, sort_keys=False)
print(yaml_text)

round_trip = yaml.safe_load(yaml_text)
print(json.dumps(round_trip, indent=2))

assert round_trip == data
```

## Solution 7 — Configuration validator

```python
def validate_config(config):
    errors = []
    warnings = []
    required = {"service", "port", "debug", "environment"}

    if not isinstance(config, dict):
        return ["Configuration must be an object/mapping"], warnings

    missing = required - config.keys()
    if missing:
        errors.append(f"Missing keys: {', '.join(sorted(missing))}")

    if "service" in config:
        service = config["service"]
        if not isinstance(service, str) or not service.strip():
            errors.append("service must be a non-empty string")

    if "port" in config:
        port = config["port"]
        if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
            errors.append("port must be an integer from 1 to 65535")

    if "debug" in config and not isinstance(config["debug"], bool):
        errors.append("debug must be a Boolean")

    if config.get("environment") == "production" and config.get("debug") is True:
        warnings.append("Debug mode is enabled in production")

    return errors, warnings


valid = {
    "service": "api",
    "port": 443,
    "debug": False,
    "environment": "production",
}
print(validate_config(valid))
```

## Solution 8 — Vulnerability report summary

```python
import json
from collections import Counter

report = {
    "findings": [
        {"id": "V-001", "severity": "High", "status": "Open"},
        {"id": "V-002", "severity": "Medium", "status": "Open"},
        {"id": "V-003", "severity": "Critical", "status": "Closed"},
        {"id": "V-004", "severity": "Critical", "status": "Open"},
    ]
}

allowed = {"Critical", "High", "Medium", "Low"}
counts = Counter()
open_count = 0
priority = []

for finding in report["findings"]:
    if not isinstance(finding, dict):
        raise ValueError("Each finding must be an object")
    if not {"id", "severity", "status"}.issubset(finding):
        raise ValueError("Finding is missing required fields")
    if finding["severity"] not in allowed:
        raise ValueError("Unknown severity")

    counts[finding["severity"]] += 1
    if str(finding["status"]).casefold() == "open":
        open_count += 1
        if finding["severity"] in {"Critical", "High"}:
            priority.append(finding["id"])

summary = {
    "by_severity": dict(counts),
    "open_findings": open_count,
    "open_critical_high_ids": priority,
}

print(json.dumps(summary, indent=2))
```

## Solution 9 — Safe parsing and input size limits

```python
import json
from pathlib import Path
import yaml

MAX_BYTES = 1_000_000

def load_config(path):
    path = Path(path)
    raw = path.read_bytes()

    if len(raw) > MAX_BYTES:
        raise ValueError("Configuration exceeds maximum allowed size")

    text = raw.decode("utf-8")

    if path.suffix.lower() == ".json":
        return json.loads(text)
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(text)

    raise ValueError("Expected a .json, .yaml, or .yml file")
```

The size limit is an example policy; choose a limit appropriate to the application. Always validate the parsed object and values afterward.

## Solution 10 — Configuration Security Checker

`validator.py`:

```python
def validate_config(config):
    errors = []
    warnings = []
    required = {"service", "port", "debug", "environment"}

    if not isinstance(config, dict):
        return ["Top-level configuration must be an object/mapping"], warnings

    missing = required - config.keys()
    if missing:
        errors.append(f"Missing keys: {', '.join(sorted(missing))}")

    if "service" in config and (
        not isinstance(config["service"], str) or not config["service"].strip()
    ):
        errors.append("service must be a non-empty string")

    if "port" in config:
        port = config["port"]
        if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
            errors.append("port must be an integer from 1 to 65535")

    if "debug" in config and not isinstance(config["debug"], bool):
        errors.append("debug must be a Boolean")

    if config.get("environment") == "production" and config.get("debug") is True:
        warnings.append("Debug mode is enabled in production")

    return errors, warnings
```

`main.py`:

```python
import json
from pathlib import Path
import sys
import yaml

from validator import validate_config

MAX_BYTES = 1_000_000

def load_config(path):
    path = Path(path)
    raw = path.read_bytes()
    if len(raw) > MAX_BYTES:
        raise ValueError("Input file is too large")

    text = raw.decode("utf-8")
    suffix = path.suffix.lower()

    if suffix == ".json":
        return json.loads(text)
    if suffix in {".yaml", ".yml"}:
        return yaml.safe_load(text)
    raise ValueError("Unsupported file extension")

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <config.json|config.yaml>")
        return

    try:
        config = load_config(sys.argv[1])
        errors, warnings = validate_config(config)
    except FileNotFoundError:
        print("Configuration file not found")
        return
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"Unable to parse configuration: {type(error).__name__}")
        return

    for message in errors:
        print("ERROR:", message)
    for message in warnings:
        print("WARNING:", message)

    if not errors:
        print("Structural validation passed")

if __name__ == "__main__":
    main()
```

Run it with:

```bash
python main.py config.json
python main.py config.yaml
```

Structural validation is not a full security audit. Extend the schema and policies to match your application and deployment environment.

## Key takeaways

- JSON is supported by Python's standard library.
- PyYAML provides YAML parsing and serialization.
- Use safe YAML APIs for untrusted input.
- Handle parsing and file errors explicitly.
- Validate structure and policy after parsing.
- Never commit secrets or automatically apply unreviewed production changes.
