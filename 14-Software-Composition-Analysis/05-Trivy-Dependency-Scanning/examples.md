# Trivy Dependency Scanning – Examples

## Repository scan
```bash
trivy repo .
```

## Filesystem scan with additional scanners
```bash
trivy fs --scanners vuln,secret .
trivy fs --scanners vuln,misconfig,secret,license .
```
Misconfiguration and license scanners must be explicitly selected for repository/filesystem scans.

## Severity gate
```bash
trivy repo --severity HIGH,CRITICAL --exit-code 1 .
```
Use a documented policy; a non-zero result should trigger triage, not automatic suppression.

## JSON and SARIF
```bash
trivy repo --format json --output trivy-report.json .
trivy repo --format sarif --output trivy-report.sarif .
```

## CycloneDX SBOM
```bash
trivy repo --format cyclonedx --output sbom.cdx.json .
```
Inspect document metadata, component versions, package URLs, and dependency relationships.

## Dependency tree
```bash
trivy repo --dependency-tree .
```
Use when supported to investigate the origin of a transitive dependency. Check release documentation because the feature may be experimental.

## Ignore policy
`.trivyignore` is an empty teaching placeholder. Any approved exception must be narrow, evidenced, owned, and time-bound.
