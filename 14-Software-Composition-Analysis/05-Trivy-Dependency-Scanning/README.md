# 05 – Trivy Dependency Scanning

## Learning objectives
- Scan repositories, filesystems, container images, and SBOMs with Trivy.
- Detect vulnerabilities in supported dependencies and lockfiles.
- Generate and inspect CycloneDX SBOMs.
- Configure severity filters, output formats, and CI exit codes.
- Triage findings and integrate Trivy securely into CI/CD.

## 1. Trivy overview
Trivy is an open-source security scanner. Depending on the target and selected scanners, it detects vulnerabilities, misconfigurations, secrets, and licenses.

Relevant targets:
- `trivy repo`: local or remote Git repository; analyzes supported dependency metadata such as lockfiles.
- `trivy fs`: local filesystem and supported dependency/artifact files.
- `trivy image`: container image, including OS packages and application libraries.
- `trivy sbom`: scans an SBOM for vulnerabilities (confirm syntax with the installed release's help).

Choose the target that matches the software being assessed. Repository scanning focuses on source dependency metadata; it is not a substitute for scanning arbitrary compiled artifacts or the final container image.

## 2. Installation and version check
Install Trivy using the official installation guide for your OS/package manager. Verify:
```bash
trivy --version
trivy repo --help
trivy fs --help
```
Pin the Trivy version in CI and review release notes when upgrading.

## 3. Repository scanning
From the root of an authorized project:
```bash
# Vulnerability and secret scanners are enabled by default
trivy repo .

# Explicitly select all relevant scanner types
trivy repo --scanners vuln,misconfig,secret,license .

# Filter displayed vulnerability severity
trivy repo --severity HIGH,CRITICAL .
```
Misconfiguration and license scanning are not enabled by default for repository/filesystem scans; explicitly select them when required. Confirm supported scanner names for your installed release.

## 4. Filesystem scanning
```bash
trivy fs --scanners vuln,secret .
trivy fs --scanners vuln,misconfig,secret,license .
```
Use committed lockfiles for reproducible dependency visibility. Results depend on supported ecosystems, file formats, and scanner coverage.

## 5. SBOM generation
Generate CycloneDX:
```bash
trivy repo --format cyclonedx --output sbom.cdx.json .
# Or scan a local filesystem
trivy fs --format cyclonedx --output sbom.cdx.json .
```
Inspect metadata, component names/versions, package identifiers, and dependency relationships. An SBOM is an inventory, not proof that all components are vulnerability-free.

To scan an existing SBOM, check `trivy sbom --help` for the installed release. Current CLI syntax commonly uses:
```bash
trivy sbom sbom.cdx.json
```

## 6. Reports and CI exit codes
Trivy supports table and machine-readable formats including JSON and SARIF:
```bash
trivy repo --format json --output trivy-report.json .
trivy repo --format sarif --output trivy-report.sarif .
```
A severity gate:
```bash
trivy repo --severity HIGH,CRITICAL --exit-code 1 .
```
The command returns a non-zero exit code when findings match the configured filter. Set thresholds through a documented risk policy and provide an exception process.

## 7. Dependency origin and triage
Where supported, `--dependency-tree` can help trace the origin of vulnerable transitive dependencies; consult current documentation because this option may be experimental.

For each finding, validate:
1. Exact package identity, ecosystem, and resolved version.
2. Advisory and affected version range.
3. Direct/transitive relationship and dependency path.
4. Whether the component is present in the shipped artifact.
5. Reachability, exposure, exploit intelligence, and business impact.
6. Fixed version or replacement and compatibility tests.

CVSS is one input. Consider exploit availability, KEV/EPSS context, deployment exposure, and compensating controls.

## 8. Ignore rules and exceptions
Use Trivy ignore mechanisms only for documented, approved cases. Prefer narrow identifiers and scoped exceptions. Record owner, rationale, evidence, expiry/review date, and revalidation plan. Check the exact ignore-file syntax supported by your installed release.

The included `.trivyignore` is intentionally empty. Do not add real CVE identifiers without an approved finding and evidence.

## 9. CI/CD security
The workflow example is for training. Before production:
- Pin third-party actions to immutable full commit SHAs, not mutable tags.
- Use least-privilege token permissions.
- Do not expose secrets to untrusted pull-request code.
- Restrict report artifact access; reports may expose internal dependency inventory or secret findings.
- Pin Trivy's version and define an update process.
- Document blocking thresholds and exceptions.

## 10. Limitations
Coverage depends on supported ecosystems and lockfile formats. Repository, filesystem, and image scans inspect different package sources. A finding does not automatically prove runtime reachability or exploitability. A clean scan is not proof of security; record target scope, version, database status, and coverage gaps.

## Labs
Complete `practical.md` and use the templates under `templates/`.

## Official references
- Trivy docs: https://trivy.dev/docs/latest/
- Repository scanning: https://trivy.dev/docs/latest/target/repository/
- Filesystem scanning: https://trivy.dev/docs/latest/target/filesystem/
- Vulnerability scanning: https://trivy.dev/docs/latest/scanner/vulnerability/
- Reporting: https://trivy.dev/docs/latest/configuration/reporting/
- Installation: https://trivy.dev/docs/latest/getting-started/installation/
