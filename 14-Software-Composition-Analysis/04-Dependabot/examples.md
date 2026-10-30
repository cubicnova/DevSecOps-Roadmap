# Dependabot – Examples

## 1. Basic configuration
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
```

## 2. Multi-ecosystem configuration
The included `.github/dependabot.yml` has separate entries for npm, pip, Maven, Docker, and GitHub Actions. Each entry must point to a directory containing the corresponding manifest or configuration file.

## 3. Group version updates
```yaml
groups:
  development-dependencies:
    dependency-type: "development"
    patterns:
      - "*"
```
Review the official options reference for the exact supported group keys for your use case. Keep production dependency updates separate when that improves reviewability.

## 4. Group security updates
```yaml
groups:
  security-patches:
    applies-to: security-updates
    patterns:
      - "*"
    update-types:
      - "patch"
      - "minor"
```
Security-update grouping requires the dependency graph, Dependabot alerts, and security updates to be enabled. Grouping rules are per package ecosystem.

## 5. Ignore a specific update
```yaml
ignore:
  - dependency-name: "example-package"
    update-types: ["version-update:semver-major"]
```
Use ignore rules only with a documented reason and periodic review. Do not ignore security fixes as a substitute for remediation.

## 6. Cooldown
```yaml
cooldown:
  default-days: 7
  semver-major-days: 30
  semver-minor-days: 7
  semver-patch-days: 3
```
Cooldown applies to version updates, not security updates. Validate current support and constraints in the options reference.

## 7. Private registry
A registry entry should use the exact registry type and authentication fields supported for the package ecosystem. Reference credentials from GitHub secrets; never paste actual credentials into this example or a committed config.

## 8. Pull request review
See `templates/update-review.md` for a repeatable checklist covering release notes, dependency graph changes, tests, security advisories, and merge decision.
