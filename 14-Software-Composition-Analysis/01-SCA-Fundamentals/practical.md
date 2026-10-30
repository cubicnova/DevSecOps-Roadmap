# Practical Exercises – SCA Fundamentals

## Lab 1: Dependency inventory
1. Choose an authorized sample application.
2. Locate its manifest and lockfile.
3. Record package manager and reproducible build/install command.
4. Generate a dependency tree using the package manager.
5. Mark direct/transitive and runtime/development dependencies.
**Deliverable:** inventory of at least 10 entries, or all entries if smaller.

## Lab 2: Vulnerability audit
For a Python project in an isolated virtual environment:
```bash
python -m venv .venv
# Activate it for your operating system
python -m pip install --upgrade pip
python -m pip install pip-audit
pip-audit -r requirements.txt
```
Record package, installed version, advisory, affected range, fix version, scanner/database timestamp, and applicability evidence. A clean result is not proof of absence; record coverage limitations.

## Lab 3: SBOM generation
1. Install Syft using its official documentation.
2. Generate an SBOM for an authorized project:
   `syft dir:. -o cyclonedx-json=sbom.cdx.json`
3. Inspect metadata, component names, versions, PURLs, and dependency relationships.
4. Compare it with the lockfile and deployed artifact; note gaps.
5. Upload only a test SBOM to a properly secured Dependency-Track test instance.

## Lab 4: License review
Select five dependencies. Identify exact-version license evidence from authoritative package metadata/upstream files. Record missing or conflicting data. Refer legal interpretation to the organization's legal/compliance process.

## Lab 5: Remediation decision
For one finding, compare upgrade, replacement, removal, and temporary mitigation. Include compatibility tests, owner, target date, residual risk, and verification evidence.

## Lab 6: CI/CD integration design
Design a PR check that scans dependency changes, applies an explicit policy threshold, reports actionable findings, protects secrets from untrusted PR code, and supports exceptions with owners and expiry dates. Review permissions and pin third-party actions to immutable commit SHAs before production use.

## Submission checklist
- [ ] Dependency inventory and graph
- [ ] Scanner output and coverage notes
- [ ] SBOM and format/version
- [ ] License review
- [ ] Remediation decision
- [ ] CI/CD design and risk notes
