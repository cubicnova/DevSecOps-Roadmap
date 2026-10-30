# SCA Fundamentals – Examples

## Direct and transitive dependency graph
```text
web-service
├── requests       (direct)
│   ├── urllib3    (transitive)
│   └── certifi    (transitive)
└── pytest         (development)
    └── pluggy     (transitive)
```
A transitive package can affect the application even if it is absent from the top-level manifest.

## Manifest versus lockfile
`requirements.in` might declare `requests>=2.31,<3`. A generated lockfile records resolved versions (and sometimes hashes). Use the project's supported reproducible installation workflow.

## Python dependency audit
```bash
python -m pip install pip-audit
pip-audit -r requirements.txt
```
Review package, installed version, advisory, affected range, and fixed version. Test upgrades for compatibility.

## Illustrative component record
```json
{
  "type": "library",
  "name": "requests",
  "version": "2.31.0",
  "purl": "pkg:pypi/requests@2.31.0",
  "licenses": [{"license": {"id": "Apache-2.0"}}]
}
```
This fragment is not a complete SBOM; a complete BOM needs document metadata, format version, components, and appropriate dependency relationships.

## Prioritization examples
| Finding | Context | Suggested action |
|---|---|---|
| Critical CVE in internet-facing runtime package | High exposure; fix exists | Expedite upgrade, test, deploy, verify |
| High CVE in development tool | Build pipeline may still be exposed | Validate exposure and update promptly |
| Missing license metadata | Compliance uncertainty | Obtain authoritative evidence |
| Abandoned package | Maintenance risk | Evaluate supported replacement |

Do not infer exploitability solely from CVSS or assume development dependencies are harmless.
