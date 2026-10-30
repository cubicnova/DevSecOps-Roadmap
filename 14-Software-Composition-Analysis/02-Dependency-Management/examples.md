# Dependency Management — Examples

Examples are educational. Verify current package versions and advisories before using dependencies in a real project.

## 1. npm manifest and lockfile

`package.json`:

```json
{
  "name": "dependency-lab",
  "private": true,
  "scripts": { "test": "node --test" },
  "dependencies": { "express": "4.21.2" },
  "devDependencies": { "jest": "29.7.0" }
}
```

Generate and commit the lockfile:

```bash
npm install
git add package.json package-lock.json
```

Reproduce the install in CI:

```bash
npm ci
npm ls --all
```

The versions shown are illustrative, not a claim that they are latest or suitable for every project.

## 2. Python pinned requirements

`requirements.txt`:

```text
requests==2.32.3
urllib3==2.2.3
```

Create an isolated environment:

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip check
```

For stronger integrity, use a lock workflow that generates hashes and install with `--require-hashes`. A version pin is not a cryptographic integrity check.

## 3. Go dependency inspection

```bash
go mod tidy
go list -m all
go mod verify
```

Review both `go.mod` and `go.sum` when dependencies change.

## 4. Maven dependency tree

```bash
mvn dependency:tree
mvn versions:display-dependency-updates
```

Inspect why a transitive component is present before excluding or overriding it. Run tests after changes.

## 5. Dependency assessment template

```markdown
# Dependency assessment
- Package and ecosystem:
- Exact version:
- Official repository:
- Publisher/maintainer:
- License:
- Release and maintenance status:
- Direct or transitive:
- Transitive footprint:
- Known advisories:
- Install/build scripts:
- Provenance/signature:
- Approved registry:
- Business justification:
- Reviewer:
- Decision: Approved / Rejected / More review
```

## 6. Dependabot configuration

`.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

Review changelog, lockfile diff, security results, and tests for each PR.

## 7. Renovate cooldown example

`renovate.json`:

```json
{
  "extends": ["config:recommended"],
  "minimumReleaseAge": "7 days",
  "internalChecksFilter": "strict",
  "packageRules": [
    {
      "matchUpdateTypes": ["major"],
      "minimumReleaseAge": "30 days"
    }
  ]
}
```

Validate behavior against the installed Renovate version and preserve an emergency security-update route.

## 8. Private npm scope

`.npmrc`:

```ini
@cubicnova:registry=https://packages.example.internal/npm/
always-auth=true
```

Supply authentication through a secret store or CI environment variable. Never commit a real token.

## 9. npm audit

```bash
npm ci
npm audit --audit-level=high
npm audit --json > npm-audit.json
```

Review the full dependency path and fixed version. Avoid blindly using force upgrades that may introduce breaking major versions.

## 10. Lockfile review checklist

- New packages and unexpected transitive dependencies.
- Changed versions and integrity values.
- Registry/source URL changes.
- Removed or replaced packages.
- Package-manager version effects.
- Manifest/lockfile consistency.

## 11. Simple pinned requirements inventory script

This intentionally simple script does not parse every pip requirements syntax:

```python
from pathlib import Path

for raw in Path("requirements.txt").read_text().splitlines():
    line = raw.strip()
    if not line or line.startswith("#"):
        continue
    if "==" in line:
        name, version = line.split("==", 1)
        print(f"{name.strip()} -> {version.strip()}")
    else:
        print(f"REVIEW CONSTRAINT: {line}")
```

## 12. Dependency update PR template

```markdown
## Dependency update
- Package:
- Previous version:
- New version:
- Reason: security / bug fix / maintenance
- Advisory references:
- Direct/transitive:
- Lockfile updated:
- Changelog reviewed:
- Tests passed:
- SCA passed:
- Breaking changes:
- Rollback plan:
- Reviewer:
```

## 13. Emergency override record

```yaml
package: example-library
version: 3.4.2
override_type: release-age-cooldown
reason: "Approved urgent security fix"
advisory: "Internal advisory reference"
approved_by: "Security lead"
reviewed_at: "2026-10-30"
expires_at: "2026-11-06"
verification:
  changelog_reviewed: true
  publisher_checked: true
  tests_passed: true
```

Use fictional data in training. Real records must follow organizational change and audit policy.

## 14. Conceptual dependency policy

```yaml
dependency_policy:
  lockfiles_required: true
  frozen_install_in_ci: true
  new_dependency_review_required: true
  approved_registries_only: true
  scan_on_pull_request: true
  scheduled_rescan: true
  sbom_for_release: true
  emergency_override_requires_approval: true
```

This is a conceptual policy, not a native configuration format for a specific scanner.
