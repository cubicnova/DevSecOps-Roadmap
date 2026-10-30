# 01 – SCA Fundamentals

## Learning objectives
- Explain Software Composition Analysis (SCA) and its role in DevSecOps.
- Distinguish direct, transitive, runtime, and development dependencies.
- Understand manifests, lockfiles, vulnerability and license findings.
- Generate and inspect a Software Bill of Materials (SBOM).
- Triage and remediate dependency risks.

## 1. What is SCA?
SCA identifies and evaluates third-party and open-source components used by an application. It helps teams discover known vulnerabilities, license obligations, outdated or abandoned packages, malicious-package risks, and provenance concerns. SCA complements—not replaces—SAST, DAST, secrets scanning, and secure code review.

## 2. Dependency fundamentals
- **Direct:** declared by the application.
- **Transitive:** introduced by another dependency.
- **Runtime/production:** needed when the application runs.
- **Development:** used for tests, builds, linting, or development.
- **Manifest:** declares dependency requirements (e.g. `package.json`, `requirements.txt`).
- **Lockfile:** records resolved versions and dependency graph (e.g. `package-lock.json`, `poetry.lock`).

A manifest may not describe the exact resolved graph. Prefer committed lockfiles and reproducible install commands.

## 3. What SCA evaluates
| Risk | Questions |
|---|---|
| Vulnerabilities | Is the exact component version affected by an advisory? |
| Exploitability | Is vulnerable functionality reachable and exposed? |
| Severity | What are CVSS, EPSS, exploit availability, and business impact? |
| License | Is the exact version's license compatible with policy? |
| Maintenance | Is the project supported and patched? |
| Integrity | Is the package authentic and from the expected source? |
| Hygiene | Are dependencies pinned, necessary, and maintained? |

A severity score is only one input. Validate package identity, version range, reachability, exposure, available fix, and compensating controls.

## 4. SCA workflow
1. Discover manifests, lockfiles, vendored libraries, container packages, and build dependencies.
2. Resolve dependencies reproducibly.
3. Scan against vulnerability and license intelligence.
4. Generate an SBOM for the relevant artifact.
5. Triage findings and validate applicability.
6. Upgrade, replace, remove, or temporarily mitigate affected components.
7. Re-scan and verify; document exceptions with owners and expiry dates.
8. Monitor continuously as new advisories appear.

## 5. SBOM essentials
A Software Bill of Materials (SBOM) is a machine-readable inventory of software components and relationships. It supports incident response, impact analysis, procurement, and governance.

Common formats:
- **CycloneDX:** security and supply-chain use cases; includes related capabilities such as VEX.
- **SPDX:** software package and licensing transparency.

Useful data includes component name/version, supplier, Package URL (PURL), hashes where available, licenses, dependency relationships, SBOM author/time, and generation tool/process. Confirm format/version compatibility with downstream consumers.

## 6. Common tools
- **OWASP Dependency-Track:** consumes CycloneDX SBOMs and continuously evaluates vulnerability and policy risk.
- **Syft:** generates SBOMs from filesystems, images, and other supported sources.
- **Grype:** scans sources and SBOMs for known vulnerabilities.
- **OSV-Scanner:** checks supported ecosystems against OSV data.
- **Trivy:** scans repositories, images, and SBOMs.
- **GitHub dependency graph / Dependabot:** dependency visibility, alerts, and updates.
- **Dependency review:** evaluates dependency changes in pull requests.

Scanner output is not proof that a package is exploitable or safe. Check ecosystem coverage, database freshness, and configuration.

## 7. Example commands
```bash
python -m venv .venv
# Linux/macOS: . .venv/bin/activate
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pip-audit
pip-audit -r requirements.txt

# Install Syft and Grype separately from their official documentation
syft dir:. -o cyclonedx-json=sbom.cdx.json
grype sbom:sbom.cdx.json
```
Run tools only against software and environments you own or are authorized to assess.

## Lab deliverables
Complete `practical.md`. Use `templates/` to document findings and exceptions. Files in `examples/` are educational fixtures, not a production inventory.

## Further reading
- OWASP Component Analysis: https://community.owasp.org/Component_Analysis
- OWASP Developer Guide – Dependencies: https://devguide.owasp.org/en/05-implementation/02-dependencies/
- CycloneDX specification: https://github.com/CycloneDX/specification
- OWASP Dependency-Track: https://owasp.org/projects/dependency-track
- GitHub dependency review: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-review

## Knowledge check
1. How does a lockfile differ from a manifest?
2. How can a transitive dependency introduce risk?
3. Why is an SBOM not the same as a vulnerability scan?
4. What evidence should be checked before accepting a finding?
5. Why are license findings reviewed separately from CVEs?
