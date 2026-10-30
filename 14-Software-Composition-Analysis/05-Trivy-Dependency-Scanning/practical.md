# Practical Exercises – Trivy Dependency Scanning

## Lab 1: Install and verify
1. Install Trivy from its official guide.
2. Record Trivy and OS versions.
3. Inspect `trivy repo --help` and `trivy fs --help`.
4. Confirm supported scanner names and output formats.
**Deliverable:** installation/version record.

## Lab 2: Repository scan
1. Scan `examples/sample-node-app`:
   ```bash
   trivy repo examples/sample-node-app
   ```
2. Repeat with JSON output.
3. Record detected packages and findings (if any).
4. Note whether the lockfile was recognized and any coverage gaps.

## Lab 3: Filesystem scanner comparison
Run:
```bash
trivy fs --scanners vuln,misconfig,secret,license examples/sample-node-app
```
Identify default scanners versus explicitly enabled scanners. Do not place real credentials in the lab directory.

## Lab 4: SBOM generation
Run:
```bash
trivy repo --format cyclonedx --output sbom.cdx.json examples/sample-node-app
```
Inspect metadata, component names/versions, package URLs, and relationships. Record limitations.

## Lab 5: CI severity gate
1. Review `.github/workflows/trivy-sca.yml`.
2. Run locally:
   ```bash
   trivy repo --severity HIGH,CRITICAL --exit-code 1 examples/sample-node-app
   ```
3. Explain the non-zero exit behavior.
4. Define how false positives and accepted risks are handled.

## Lab 6: Finding triage
Use an authorized project finding or a provided report. Complete `templates/finding-triage.md`. Verify package/version, advisory range, dependency path, artifact presence, reachability, exposure, fix, and tests.

## Lab 7: CI/CD security review
Review action SHA pinning, token permissions, fork PR secret exposure, report access, Trivy version pinning, thresholds, and exception ownership.

## Submission checklist
- [ ] Installation/version record
- [ ] Repository scan report
- [ ] Filesystem scan comparison
- [ ] CycloneDX SBOM
- [ ] CI gate explanation
- [ ] Finding triage record
- [ ] Workflow security review
