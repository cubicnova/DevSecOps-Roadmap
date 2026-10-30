# SARIF Reports — Reference Solutions

## 1. SARIF overview

SARIF is a JSON-based interchange format for static-analysis results. It allows different scanners to represent tool metadata, rules, findings, locations, and optional code-flow details in a consistent structure.

A SARIF document contains a `version`, optional `$schema`, and one or more `runs`. Each run contains information about the tool invocation and its results.

## 2. Sample report field map

For `samples/minimal.sarif`:

| Field | Value |
|---|---|
| Tool | `CubicNovaDemoScanner` |
| Version | `1.0.0` |
| Rule ID | `PY-DEMO-001` |
| Level | `warning` |
| File | `src/repository.py` |
| Line | `12` |
| Message | Potential SQL injection; review query construction |

The rule describes the type of issue. The result is a specific occurrence in source code.

## 3. JSON validation

```bash
python -m json.tool samples/minimal.sarif > samples/minimal-pretty.json
```

A successful command indicates valid JSON syntax. It does not prove that the document satisfies the SARIF schema or GitHub ingestion requirements. Use a SARIF 2.1.0 schema validator and, where applicable, platform-specific validation.

## 4. Python parser

```python
import json

with open("samples/minimal.sarif", encoding="utf-8") as f:
    report = json.load(f)

assert report.get("version") == "2.1.0"

for run in report.get("runs", []):
    driver = run.get("tool", {}).get("driver", {})
    print("Tool:", driver.get("name"))

    for result in run.get("results", []):
        rule_id = result.get("ruleId", "unknown")
        level = result.get("level", "none")
        message = result.get("message", {}).get("text", "")

        for loc in result.get("locations", []):
            physical = loc.get("physicalLocation", {})
            uri = physical.get("artifactLocation", {}).get("uri", "")
            region = physical.get("region", {})
            print(rule_id, level, uri, region.get("startLine"), message)
```

For an empty report, the loops simply produce no findings. A production parser should validate input types and handle malformed or incomplete fields defensively.

## 5. Add a second result

Add a second rule object under `tool.driver.rules`, then add a result under `runs[0].results` with the matching `ruleId`. Ensure each result's file URI and line region correspond to the training repository.

A result that references a missing rule definition may still be syntactically valid JSON but can produce incomplete presentation or ingestion issues.

## 6. Location handling

Use paths relative to the repository root where practical, for example `src/handler.py`. Absolute paths from a temporary CI workspace may not map to the repository. For GitHub ingestion, ensure the analysis checkout path and artifact URIs are consistent.

## 7. Code flows

A code flow helps explain how data moves through a program. A typical security path might include:

1. An HTTP request parameter (source).
2. A transformation or assignment.
3. A helper function.
4. A sensitive SQL or command operation (sink).

A code flow is optional. A simple local pattern finding may have only one primary location.

## 8. Generate SARIF with CodeQL

```bash
codeql database analyze db-python \
  codeql/python-queries \
  --format=sarif-latest \
  --output=codeql-results.sarif
```

Record the CLI version and query suite. The output format should be compatible with the intended destination.

## 9. Compare reports

Compare results using rule ID, location, message, and stable fingerprints where available. Classify findings as:

- New: present in the later scan only.
- Resolved: present in the earlier scan only.
- Persistent: present in both scans.

Do not rely solely on line numbers because code changes can shift locations. Fingerprints and platform correlation help, but they should be checked when tool versions or query definitions change.

## 10. GitHub Actions upload

Example:

```yaml
name: Upload SARIF

on:
  push:
    branches: [main]

permissions:
  contents: read
  security-events: write

jobs:
  upload:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: reports/results.sarif
          category: third-party-sast
```

The file must exist before upload. If a scanner generates it in an earlier step, make sure the output path matches. Confirm repository code-scanning eligibility and workflow permissions.

## 11. Troubleshooting

| Problem | Corrective action |
|---|---|
| Invalid JSON | Repair syntax and rerun JSON parser |
| SARIF schema errors | Validate against SARIF 2.1.0 and correct structure |
| Missing annotations | Fix artifact URIs and line regions |
| Missing/duplicate alerts | Review fingerprints and analysis categories |
| Upload permission error | Review repository settings and `security-events: write` |
| Upload size error | Reduce report size or split analysis appropriately with unique categories |
| Results not visible | Check commit SHA, branch/ref, processing status, and repository eligibility |

## 12. Secure artifact handling

SARIF can contain source paths, code snippets, and vulnerability details. Restrict access to CI artifacts, use suitable retention, and avoid publishing reports from private repositories. Keep the original evidence protected; if an external sanitized copy is needed, create it separately and document the transformation.

## 13. Final project checklist

- [ ] Scanner execution is reproducible.
- [ ] SARIF output uses the intended version.
- [ ] JSON syntax validation passes.
- [ ] SARIF schema/platform compatibility is checked.
- [ ] Rule IDs and messages are meaningful.
- [ ] File paths and regions map to the repository.
- [ ] Categories/fingerprints support result tracking.
- [ ] Upload permissions are least-privilege.
- [ ] Reports are stored securely.
- [ ] Errors and limitations are documented.

## Key lesson

SARIF makes security findings portable, but useful ingestion depends on accurate rule metadata, stable locations, result correlation, supported schema properties, correct permissions, and careful handling of sensitive reports.
