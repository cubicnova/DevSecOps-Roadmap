# JSON and YAML for DevSecOps

This module in the [CubicNova DevSecOps Roadmap](https://github.com/cubicnova/DevSecOps-Roadmap/tree/main/03-Python-for-DevSecOps/05-JSON-and-YAML) teaches how to read, validate, transform, and write JSON and YAML data with Python.

JSON and YAML are widely used for application configuration, API payloads, CI/CD pipelines, infrastructure definitions, and security-tool reports.

## Learning objectives

- Explain JSON and YAML structures and common data types.
- Parse and serialize JSON with Python's built-in `json` module.
- Read and write YAML with PyYAML.
- Handle malformed input and file errors.
- Validate required keys, data types, ports, and environment settings.
- Convert data between JSON and YAML.
- Process sample API responses and security findings.
- Apply secure parsing practices to untrusted input.

## Topics covered

1. JSON objects, arrays, strings, numbers, booleans, and null
2. `json.load`, `json.loads`, `json.dump`, and `json.dumps`
3. JSON formatting, sorting, and validation
4. YAML mappings, sequences, scalars, and indentation
5. PyYAML installation and `safe_load` / `safe_dump`
6. JSON and YAML conversion
7. Configuration validation
8. API and vulnerability-report data processing
9. Exception handling
10. Security considerations and mini-project

## Requirements

- Python 3
- A terminal or command prompt
- A code editor or Jupyter Notebook
- PyYAML for YAML labs

## Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
# Linux/macOS
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

Install PyYAML:

```bash
python -m pip install PyYAML
```

Check the installation:

```bash
python -c "import yaml; print(yaml.__version__)"
```

The JSON examples use Python's standard library and do not require an extra package.

## Companion files

- [`examples.md`](examples.md): JSON/YAML examples and security notes.
- [`practical.md`](practical.md): practical exercises and mini-projects.
- [`practical.ipynb`](practical.ipynb): interactive Jupyter workbook.
- [`solutions.md`](solutions.md): reference solutions.

## JSON vs YAML

| Feature | JSON | YAML |
|---|---|---|
| Common use | APIs and machine-readable payloads | Human-edited configuration |
| Syntax | Braces, brackets, quoted keys and strings | Indentation, mappings, and sequences |
| Comments | Not supported by the JSON standard | Supported |
| Python support | Built-in `json` module | Commonly PyYAML |
| Main caution | Validate schema and input size | Use safe parsing for untrusted data |

## Security guidelines

- Use `json.loads()` or `json.load()` for JSON; never use `eval()` to parse data.
- For PyYAML, prefer `yaml.safe_load()` for untrusted YAML and `yaml.safe_dump()` for serialization.
- Do not use `yaml.load()` with an unsafe loader on untrusted content.
- Validate schema and values after parsing; successful parsing does not mean a configuration is safe.
- Treat secrets as secrets. Do not commit API tokens, passwords, private keys, or production credentials.
- Limit the size of data accepted from untrusted sources.
- Avoid logging entire configuration objects if they may contain secrets.
- Do not automatically apply changes to production infrastructure from a learning script.

## DevSecOps use cases

- Validate application configuration before deployment.
- Read and summarize vulnerability scanner JSON exports.
- Parse CI/CD workflow and infrastructure configuration.
- Convert test fixtures between JSON and YAML.
- Check that debug mode is disabled in production.
- Verify required fields and acceptable port values.

## Completion checklist

- [ ] Read and write JSON files.
- [ ] Handle invalid JSON.
- [ ] Understand YAML indentation and data types.
- [ ] Load YAML safely and serialize it.
- [ ] Convert JSON to YAML and back.
- [ ] Validate configuration values.
- [ ] Process a synthetic security findings report.
- [ ] Complete the practical workbook and mini-project.

## Learning resources

- [Python `json` documentation](https://docs.python.org/3/library/json.html)
- [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [PyYAML safe loading guidance](https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load%28input%29-Deprecation)
- [YAML specification](https://yaml.org/spec/1.2.2/)

Continue to the next module in the [CubicNova DevSecOps Roadmap](https://github.com/cubicnova/DevSecOps-Roadmap/tree/main/03-Python-for-DevSecOps).
