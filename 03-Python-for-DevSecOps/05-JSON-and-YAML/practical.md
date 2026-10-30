# JSON and YAML — Practical Exercises

**Level:** Beginner to intermediate  
**Requirements:** Python 3 and PyYAML (`python -m pip install PyYAML`).

Use the interactive version in `practical.ipynb` for cell-by-cell practice. Use only synthetic configuration and security data.

## Lab 1 — JSON basics

Create a Python dictionary with service name, port, debug flag, and environment. Convert it to JSON with `json.dumps(..., indent=2)`. Parse it back with `json.loads()`.

**Tasks:** Print the result, inspect types, and explain the difference between Python `None` and JSON `null`.

## Lab 2 — JSON file handling

Write a `config.json` file using `json.dump()`, then load it using `json.load()`.

**Tasks:** Use UTF-8 encoding, handle a missing file, and keep the output formatted for review.

## Lab 3 — Malformed JSON

Try parsing these strings:

```python
samples = [
    '{"service": "api", "port": 443}',
    '{"service": "api", "port": }',
    "{'service': 'api'}",
    '{"debug": True}',
]
```

Identify valid JSON and catch `json.JSONDecodeError` for invalid input. Remember JSON uses double-quoted strings and lowercase `true`/`false`/`null`.

## Lab 4 — YAML structure

Write a YAML document with:
- a service name,
- a port,
- a Boolean debug setting,
- a list of allowed hosts,
- nested owner information.

Load it with `yaml.safe_load()` and inspect the Python object. Use spaces for indentation.

## Lab 5 — YAML file handling

Write a dictionary to `config.yaml` with `yaml.safe_dump()`. Read it back with `yaml.safe_load()`. Handle missing files and YAML parsing errors.

## Lab 6 — JSON/YAML conversion

Convert a JSON string into YAML, then convert the YAML back into JSON. Compare the resulting Python objects rather than comparing whitespace or key ordering.

## Lab 7 — Configuration validator

Implement `validate_config(config)` with these requirements:
- Required keys: `service`, `port`, `debug`, `environment`.
- `service` must be a non-empty string.
- `port` must be an integer from 1 through 65535; reject Boolean values.
- `debug` must be a Boolean.
- Warn if `debug` is `true` in production.

Test both valid and invalid configurations.

## Lab 8 — Vulnerability report summary

Create synthetic JSON data containing finding IDs, severity, and status.

**Tasks:**
- Count findings by severity.
- Count open findings.
- List open Critical and High findings.
- Validate that each record contains the expected fields.
- Save a summary to JSON.

## Lab 9 — Safe parsing and security review

1. Explain why `yaml.safe_load()` is preferred for untrusted YAML.
2. Explain why `eval()` must not be used for JSON parsing.
3. Add a maximum input size check before parsing externally supplied data.
4. Avoid printing full configurations that may contain secrets.
5. Confirm that parsing success does not mean configuration policy checks have passed.

## Lab 10 — Mini-project: Configuration Security Checker

Build a script with this structure:

```text
config-security-checker/
├── main.py
├── validator.py
├── config.json
├── config.yaml
└── README.md
```

Requirements:
- Accept a JSON or YAML input file.
- Parse JSON with the built-in `json` module.
- Parse YAML with `yaml.safe_load()`.
- Validate required keys and types.
- Flag debug mode enabled in production.
- Handle missing files, malformed input, and unexpected top-level data types.
- Print errors and warnings without exposing secrets.
- Do not modify or deploy production settings automatically.

## Reflection questions

1. What is the difference between `json.load()` and `json.loads()`?
2. What is the difference between `json.dump()` and `json.dumps()`?
3. Why does YAML depend on indentation?
4. Why should untrusted YAML be loaded with `safe_load()`?
5. Why is parsing not the same as validation?
6. Why should configuration secrets not be committed to Git?

## Completion checklist

- [ ] Read/write JSON
- [ ] Handle malformed JSON
- [ ] Read/write YAML safely
- [ ] Convert between JSON and YAML
- [ ] Validate configuration schema and values
- [ ] Summarize a synthetic security report
- [ ] Complete the configuration security checker
