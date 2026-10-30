# Dependency Security — Examples

These examples are starting points for a learning repository. Tool output and command options can vary by version; consult the current official documentation before adopting them in a production pipeline.

## 1. Inspect Node.js dependencies

```bash
# List the dependency tree, including transitive packages
npm ls --all

# Check known advisories for the current dependency graph
npm audit

# Install exactly the versions represented in package-lock.json
npm ci
```

Review audit results before applying fixes. Avoid using forceful upgrade commands without checking breaking changes and test coverage.

## 2. Python dependency inventory

```bash
# Show installed packages in the active environment
python -m pip list

# Show metadata and dependencies for a package
python -m pip show requests

# Install declared versions from a requirements file
python -m pip install -r requirements.txt
```

Use a virtual environment for project isolation. For reproducible deployments, maintain a lock or fully pinned dependency set that includes transitive dependencies and hashes where appropriate. A plain unpinned requirements file may not be sufficient.

## 3. Run OSV-Scanner

```bash
# Scan the current project using OSV-Scanner
osv-scanner scan source -r .
```

Install OSV-Scanner from its official source first and verify the command syntax for your installed version. Treat results as triage input; confirm package version, advisory range, and applicability.

## 4. Run OWASP Dependency-Check

```bash
# Example Maven plugin invocation
mvn org.owasp:dependency-check-maven:check
```

Configure the plugin and vulnerability-data updates according to the official documentation. Findings may require manual review, especially when package identification is uncertain.

## 5. Scan a container image with Trivy

```bash
trivy image --severity HIGH,CRITICAL myapp:local
```

Build the image locally first. Use a trusted scanner installation and review the current Trivy documentation for image, filesystem, and exit-code options. A scanner result is not a substitute for checking whether the final image matches the release being deployed.

## 6. Generate an SBOM with Syft

```bash
# Example: generate a CycloneDX JSON SBOM from a local image
syft myapp:local -o cyclonedx-json > sbom.cdx.json
```

Keep the SBOM associated with the exact artifact digest or release identifier. Validate the output and review whether the scanner covers operating-system packages, bundled libraries, and application dependencies.

## 7. Example GitHub Actions dependency checks

```yaml
name: Dependency Security

on:
  pull_request:
  push:
    branches: [main]
  schedule:
    - cron: "17 5 * * 1"

permissions:
  contents: read

jobs:
  dependency-audit:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install locked dependencies
        run: npm ci

      - name: Audit dependencies
        run: npm audit
```

This is an illustrative workflow for a Node.js repository with a valid `package-lock.json`. Review action versions and pin actions to verified full commit SHAs where your supply-chain policy requires it. Define an explicit severity and exception policy rather than assuming every audit report has the same risk.

## 8. Example dependency change review

Before merging a dependency update, review:

- Package name and source registry.
- Old and new versions, including transitive changes.
- Maintainer release notes and security advisories.
- Lockfile changes and package integrity metadata.
- License changes.
- Test results and build reproducibility.
- Whether the update removes the reported vulnerability.

## 9. Example triage record

```text
Finding: Vulnerable transitive package
Affected application: inventory-api
Detected version: 2.4.1
Fixed version: 2.4.4
Source: SCA scan + maintainer advisory
Reachability: Under review
Exposure: Internet-facing API
Action: Upgrade parent dependency, regenerate lockfile, run tests
Owner: Application team
Due date: Defined by internal severity policy
Validation: Rescan final artifact and verify resolved version
```

Use real package and advisory data in a real ticket. Avoid inventing a fixed version without verifying the upstream advisory.

## 10. Dependency hygiene checks

- Remove unused packages.
- Avoid installing a package only because its name looks familiar.
- Verify package names and publishers before installation.
- Use separate credentials and minimal permissions in CI.
- Restrict network access for builds where practical.
- Avoid exposing production secrets to package installation scripts.
- Keep dependency scanners and vulnerability data current.
