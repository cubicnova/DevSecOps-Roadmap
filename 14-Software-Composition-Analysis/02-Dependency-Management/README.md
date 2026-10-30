# 02 — Dependency Management

## Overview
Dependency management is the process of selecting, sourcing, pinning, updating, reviewing, and retiring third-party components. It complements Software Composition Analysis (SCA): SCA discovers and evaluates components; dependency management controls which components enter an application and how they are maintained.

Use only repositories and systems you own or are authorized to assess. Examples use synthetic projects.

## Learning objectives
- Distinguish direct, transitive, runtime, development, optional, and build dependencies.
- Understand manifests, lockfiles, version constraints, and reproducible installs.
- Assess package identity, maintainers, license, security history, and provenance.
- Reduce dependency confusion, typosquatting, malicious release, and install-script risks.
- Automate updates and vulnerability checks.
- Control registries, define emergency exceptions, and retire unused dependencies.
- Integrate dependency policy into CI/CD and measure its effectiveness.

## 1. Dependency types

| Type | Meaning | Example |
|---|---|---|
| Direct | Declared by your project | Express in package.json |
| Transitive | Required by another package | A library used by Express |
| Runtime | Required by the deployed application | Web framework |
| Development | Used for tests/build/lint | pytest |
| Optional | Needed only for a feature | Optional database adapter |
| Build/tooling | Used to compile/package | Compiler plugin |

Transitive dependencies matter because their code may execute in your application even though your team did not select them directly.

## 2. Manifests and lockfiles

A manifest declares intended dependencies and version constraints. A lockfile records the resolved dependency graph and exact versions, often with integrity hashes and source information.

| Ecosystem | Manifest | Lockfile | Locked install/check |
|---|---|---|---|
| npm | package.json | package-lock.json | npm ci |
| pnpm | package.json | pnpm-lock.yaml | pnpm install --frozen-lockfile |
| Yarn | package.json | yarn.lock | yarn install --immutable |
| Python uv | pyproject.toml | uv.lock | uv sync --locked |
| Python pip | requirements input | hashed requirements.txt | pip install --require-hashes -r requirements.txt |
| Go | go.mod | go.sum | go mod verify |
| Rust | Cargo.toml | Cargo.lock | cargo build --locked |
| .NET | .csproj | packages.lock.json | dotnet restore --locked-mode |

Commit application lockfiles. Review lockfile changes as code: unexpected package additions, registry changes, or integrity changes require investigation.

### Version constraints
- Exact pin: `library==2.4.1`
- Range: `library>=2.4,<3.0`
- Floating wildcard: `library=*` — avoid for controlled application builds.

Pins improve repeatability but do not keep software secure automatically. Establish a regular update process.

## 3. Selecting a dependency

Before adding a package, evaluate:
1. Business need and whether existing platform functionality is sufficient.
2. Exact package identity, registry entry, official repository, and publisher.
3. Maintenance activity, release history, support status, and security policy.
4. Known vulnerabilities and responsiveness to security reports.
5. License compatibility with your product and distribution model.
6. Transitive dependency footprint and install/build scripts.
7. Signatures, provenance attestations, and artifact integrity where available.
8. Runtime compatibility, platform support, and exit/replacement options.

Popularity or download count alone does not prove that a package is safe.

## 4. Supply-chain threats

### Dependency confusion
A public package shadows an internal package name, sometimes with a higher version. Reserve internal namespaces/scopes, map them explicitly to private registries, and avoid ambiguous public/private index precedence.

### Typosquatting
A package uses a name similar to a legitimate project. Verify spelling, scope, publisher, repository link, and release history before adding it.

### Slopsquatting
A package name suggested by an AI coding assistant may be hallucinated and then registered by an attacker. Verify the package exists and is the intended project before installing it.

### Compromised release or maintainer
A legitimate publisher account or release pipeline may be compromised. Review unexpected release changes, publisher changes, provenance, and install scripts. Consider a release-age cooldown for routine updates.

### Install-time scripts
Install hooks can execute arbitrary code on developer machines and CI runners. Install in isolated environments, restrict egress, remove unrelated secrets, and explicitly approve scripts that are genuinely required.

## 5. Pinning and integrity

Good practices:
- Commit lockfiles and use frozen/locked install commands in CI.
- Verify artifact integrity with package-manager-supported hashes/signatures.
- Pin container images by digest and CI actions by immutable commit SHA.
- Avoid unreviewed floating tags and `latest`.
- Review lockfile registry/source URL changes.
- Separate read-only install credentials from publishing credentials.
- Prefer short-lived credentials where supported.

Example npm workflow:

```bash
npm install
git add package.json package-lock.json
git commit -m "Add application dependency"
# CI:
npm ci
```

Example Go checks:

```bash
go mod tidy
go mod verify
go list -m all
```

For pip hash-checking, use hashes generated for the exact approved artifacts. Never copy placeholder or unrelated hashes.

## 6. Updating dependencies

| Update type | Typical risk | Review |
|---|---|---|
| Patch | Often lower, not zero | Fix details, tests, advisories |
| Minor | Moderate | New features and transitive changes |
| Major | Higher | Breaking changes and migration |
| Security | Depends on exposure/exploitability | Urgency, affected paths, fixed version |

Recommended process:
1. Detect new versions and advisories.
2. Identify affected applications and dependency paths.
3. Review release notes, changelog, publisher, and source changes.
4. Update manifest and lockfile.
5. Run unit, integration, compatibility, and security tests.
6. Scan the resolved dependency tree.
7. Review and approve the PR.
8. Deploy progressively and monitor.
9. Record the deployed version and verification result.

Dependabot and Renovate can create update PRs. Automation should create reviewable changes, not blindly auto-merge every update.

## 7. Cooldown and emergency updates

A cooldown delays adoption of newly published releases to allow time for malicious or compromised versions to be detected. Choose a duration based on ecosystem, package criticality, release cadence, and risk appetite.

Renovate example:

```json
{
  "extends": ["config:recommended"],
  "minimumReleaseAge": "7 days",
  "internalChecksFilter": "strict"
}
```

Dependabot example:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    cooldown:
      default-days: 7
      semver-major-days: 30
      semver-minor-days: 7
      semver-patch-days: 3
```

Check current tool documentation and versions before adopting configuration keys. Cooldowns must not delay urgent fixes for actively exploited vulnerabilities. Define an audited override with approver, reason, evidence review, and expiry.

## 8. Private registries and proxies

An internal registry/proxy can cache approved packages, improve availability, centralize allow/deny policies, enforce license and release-age rules, and provide an audit trail. Use read-only CI credentials for installation and protected publishing credentials only in release jobs. Define explicit package scopes and registry precedence.

## 9. Removing and retiring dependencies

Remove packages that are unused, duplicated, unmaintained, unsupported, or too risky:
1. Identify direct and transitive usage.
2. Search imports, scripts, plugins, and dynamic loading.
3. Check whether another component requires it.
4. Replace functionality or remove dead code.
5. Update manifest and regenerate lockfile with the package manager.
6. Run tests and SCA.
7. Confirm absence from the built artifact/SBOM.
8. Document the change.

Do not manually delete a transitive lockfile entry. Upgrade or remove the parent dependency instead.

## 10. CI/CD integration

A dependency pipeline should use locked installs, scan manifests/lockfiles on pull requests, run scheduled scans for new advisories, generate SBOMs for releases, and gate policy-defined risk. Protect registry credentials and keep scanner permissions minimal.

Illustrative GitHub Actions workflow:

```yaml
name: Dependency checks
on:
  pull_request:
  schedule:
    - cron: "17 4 * * 1"
permissions:
  contents: read
jobs:
  dependencies:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - run: npm ci
      - run: npm audit --audit-level=high
```

Pin actions to reviewed commit SHAs in production. Understand audit semantics and manage exceptions through approval rather than broad suppression.

## 11. Governance and metrics

Define approved ecosystems/registries, lockfile requirements, dependency review criteria, vulnerability SLAs, license policy, update cadence, emergency path, application ownership, and end-of-life process.

Useful metrics:
- Repositories with committed lockfiles and frozen CI installs.
- Dependencies with known owners.
- Vulnerability age by severity.
- Time to remediate actively exploited vulnerabilities.
- Update PR success rate.
- Unapproved license and end-of-life component counts.
- Releases with an SBOM.
- Emergency overrides with documented approval.

## 12. Checklist
- [ ] Direct and transitive dependencies inventoried.
- [ ] Manifests and lockfiles committed.
- [ ] CI uses locked installation.
- [ ] New packages receive security and license review.
- [ ] Registry sources and scopes are controlled.
- [ ] Install scripts and CI credentials are restricted.
- [ ] Automated updates and scheduled scans enabled.
- [ ] Cooldown and emergency override documented.
- [ ] Unused and end-of-life dependencies tracked.
- [ ] Dependency changes tested and reviewed.
- [ ] SBOM and ownership information maintained.

## References
- [OWASP Dependency Management and Cooldown Policies](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-3-Build/2-3-2-Software-Composition-Analysis/2-3-2-2-Dependency-Management-and-Cooldown-Policies/)
- [OWASP Developer Guide — Dependencies](https://devguide.owasp.org/en/05-implementation/02-dependencies/)
- [GitHub — Best practices for maintaining dependencies](https://docs.github.com/en/code-security/concepts/supply-chain-security/best-practices-for-maintaining-dependencies)
- [Google Cloud — Dependency management](https://cloud.google.com/software-supply-chain-security/docs/dependencies)
