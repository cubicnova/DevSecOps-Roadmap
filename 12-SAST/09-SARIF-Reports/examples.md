# SARIF Reports — Examples

## 1. Minimal SARIF 2.1.0 example

Save as `samples/minimal.sarif`:

```json
{
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "CubicNovaDemoScanner",
          "version": "1.0.0",
          "rules": [
            {
              "id": "PY-DEMO-001",
              "shortDescription": {
                "text": "Potential unsafe SQL construction"
              },
              "fullDescription": {
                "text": "Review SQL statements constructed using untrusted input."
              },
              "help": {
                "text": "Use parameterized SQL statements."
              },
              "defaultConfiguration": {
                "level": "warning"
              }
            }
          ]
        }
      },
      "results": [
        {
          "ruleId": "PY-DEMO-001",
          "level": "warning",
          "message": {
            "text": "Potential SQL injection: review query construction."
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "src/repository.py"
                },
                "region": {
                  "startLine": 12,
                  "startColumn": 5
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

This is a small educational example. Production reports should follow the SARIF schema and the destination platform's supported subset.

## 2. Inspect SARIF with Python

```python
import json

with open("samples/minimal.sarif", encoding="utf-8") as f:
    sarif = json.load(f)

for run in sarif.get("runs", []):
    tool = run.get("tool", {}).get("driver", {})
    print(f"Tool: {tool.get('name')}")

    for result in run.get("results", []):
        rule_id = result.get("ruleId", "unknown")
        level = result.get("level", "none")
        message = result.get("message", {}).get("text", "")

        for location in result.get("locations", []):
            physical = location.get("physicalLocation", {})
            uri = physical.get("artifactLocation", {}).get("uri")
            region = physical.get("region", {})
            print(rule_id, level, uri, region.get("startLine"), message)
```

## 3. Validate JSON syntax

```bash
python -m json.tool samples/minimal.sarif > samples/minimal-pretty.json
```

This validates JSON syntax, not the complete SARIF schema or GitHub ingestion rules.

## 4. CodeQL CLI SARIF generation

```bash
codeql database analyze db-python \
  codeql/python-queries \
  --format=sarif-latest \
  --output=codeql-results.sarif
```

## 5. SARIF result with multiple locations

A result may include a primary location and related locations. These can help reviewers understand the context around a finding.

```json
{
  "ruleId": "PY-DEMO-002",
  "level": "error",
  "message": {
    "text": "Untrusted input reaches a sensitive operation."
  },
  "locations": [
    {
      "physicalLocation": {
        "artifactLocation": {
          "uri": "src/handler.py"
        },
        "region": {
          "startLine": 30
        }
      }
    }
  ],
  "relatedLocations": [
    {
      "id": 1,
      "message": {
        "text": "Input is read from the request."
      },
      "physicalLocation": {
        "artifactLocation": {
          "uri": "src/handler.py"
        },
        "region": {
          "startLine": 10
        }
      }
    }
  ]
}
```

## 6. Code-flow illustration

```json
{
  "ruleId": "PY-DEMO-003",
  "message": {
    "text": "Review the data flow to the sensitive operation."
  },
  "locations": [
    {
      "physicalLocation": {
        "artifactLocation": {
          "uri": "src/service.py"
        },
        "region": {
          "startLine": 25
        }
      }
    }
  ],
  "codeFlows": [
    {
      "threadFlows": [
        {
          "locations": [
            {
              "location": {
                "physicalLocation": {
                  "artifactLocation": {
                    "uri": "src/service.py"
                  },
                  "region": {
                    "startLine": 8
                  }
                },
                "message": {
                  "text": "Source: request input"
                }
              }
            },
            {
              "location": {
                "physicalLocation": {
                  "artifactLocation": {
                    "uri": "src/service.py"
                  },
                  "region": {
                    "startLine": 25
                  }
                },
                "message": {
                  "text": "Sink: sensitive operation"
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

## 7. GitHub Actions upload example

```yaml
name: Upload third-party SARIF

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

      # Add your scanner command here to generate reports/results.sarif.

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: reports/results.sarif
          category: custom-sast
```

The SARIF file must exist before the upload step. Confirm code scanning is available for the repository and that workflow permissions are sufficient.

## 8. Upload CodeQL analysis results

```bash
codeql github upload-results \
  --sarif=codeql-results.sarif \
  --repository=OWNER/REPOSITORY \
  --ref=refs/heads/main \
  --commit=COMMIT_SHA
```

Use a supported token with the required permission. Pass credentials securely, for example through standard input where supported; never put tokens in the command text.

## 9. Multiple analyses and categories

If a repository uploads separate reports from different tools or analysis slices for the same commit, give each result set a distinct category using the upload action's `category` input or the appropriate run metadata. Reusing the same category for the same tool can replace earlier analysis results.

## 10. Compare report counts

```python
import json
from collections import Counter

with open("results.sarif", encoding="utf-8") as f:
    report = json.load(f)

counts = Counter()
for run in report.get("runs", []):
    for result in run.get("results", []):
        counts[result.get("level", "none")] += 1

print("Findings by level:")
for level, count in sorted(counts.items()):
    print(f"{level}: {count}")
```

## 11. Redact sensitive report details

Before sharing SARIF outside the security team, review file paths, source snippets, messages, custom properties, and code-flow details. Prefer access controls and retention policies over ad hoc modifications that could invalidate the report or its fingerprints.
