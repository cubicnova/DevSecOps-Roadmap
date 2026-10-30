# Dependency Management — Solutions and Guidance

These are reference approaches. Exact commands and configuration depend on the package manager and version.

## Exercise 1 — Dependency types
Direct dependencies are explicitly declared. Transitive dependencies are introduced by another component. Runtime dependencies are needed by the deployed app; development dependencies support tests, linting, and builds. Optional dependencies support selected features. Transitive packages remain important because their code can execute in the application and introduce vulnerabilities or license obligations.

## Exercise 2 — Reproducible npm build

```bash
npm init -y
npm install express
npm install --save-dev jest
git add package.json package-lock.json
git commit -m "Add locked Node dependencies"

rm -rf node_modules
npm ci
npm ls --all
```

On Windows, use the appropriate PowerShell command to remove `node_modules`. `npm ci` uses the committed lockfile. Do not edit lockfiles manually.

## Exercise 3 — Python pinning
Example requirement:

```text
requests==2.32.3
```

A pin constrains version selection. A hash verifies artifact bytes. A signature or provenance attestation provides information about publisher/build origin. These controls address different risks and are not interchangeable.

## Exercise 4 — Due diligence
Verify package identity from official documentation, repository and publisher, release activity, security policy, license, transitive footprint, install hooks, and provenance. Record business need and alternatives. Popularity is not proof of safety.

## Exercise 5 — Typosquatting
Do not install lookalikes. Compare exact name/scope, official registry and repository, publisher identity, and project metadata. Independently verify AI-generated package suggestions.

## Exercise 6 — Lockfile review
Record direct version changes, added/removed transitive packages, registry/source changes, integrity/checksum changes, changelog/advisory review, and test/SCA results. Investigate unexplained package additions or registry redirection before approval.

## Exercise 7 — Automated updates
Minimal Dependabot example:

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

Consult current documentation for cooldown support and ecosystem behavior. Maintain an expedited route for security updates.

## Exercise 8 — Private registry design
1. Reserve internal scopes/namespaces.
2. Map internal scopes explicitly to the private registry.
3. Route public dependencies through a controlled proxy.
4. Avoid ambiguous fallback/index precedence.
5. Give CI read-only credentials.
6. Keep publishing credentials in protected release jobs.
7. Log package retrieval and enforce allow/deny rules.

## Exercise 9 — Install scripts
Install/build scripts may execute arbitrary commands with the install process's permissions. Use isolated workers, remove unrelated secrets, restrict egress, and allowlist required scripts. Prefer prebuilt artifacts where appropriate and test after restricting scripts.

## Exercise 10 — Update policy
Define patch/minor/major review paths, fast-track for actively exploited issues, test/SCA requirements, suitable cooldown, named exception approver, owner, due date, rollback, and post-deployment verification. Set timelines using organizational risk and asset criticality.

## Exercise 11 — Remove unused dependency
Use the package manager to remove the direct dependency and regenerate the lockfile. Search source, scripts, plugins, and dynamic imports first. Run tests and SCA; inspect the resolved tree and artifact. Never manually delete a transitive lockfile entry.

## Exercise 12 — CI dependency gate

```yaml
name: Dependency security
on:
  pull_request:
  schedule:
    - cron: "17 4 * * 1"
permissions:
  contents: read
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - run: npm ci
      - run: npm test --if-present
      - run: npm audit --audit-level=high
```

For production, pin actions to reviewed commit SHAs, use least privilege, and protect secrets. Confirm audit semantics for the selected npm version and approve exceptions explicitly.

## Exercise 13 — SBOM response
Match advisory package and affected version range against the SBOM. Identify all affected artifacts, determine whether the component is used at runtime, prioritize remediation, then record the fixed version/replacement, test result, and release containing the change.

## Exercise 14 — Maturity review
A good baseline includes committed lockfiles, frozen installs, dependency review, approved sources, automated update PRs, scheduled SCA, and ownership. Mature programs add SBOMs, malicious-package checks, provenance validation, registry curation, EOL tracking, and measured emergency response.

## Example dependency PR review

```markdown
Decision: Approve / Request changes
- Package identity verified:
- Publisher/source verified:
- Version change understood:
- Changelog reviewed:
- Lockfile diff reviewed:
- Advisory impact assessed:
- License acceptable:
- Tests passed:
- SCA passed:
- Rollback understood:
- Reviewer:
```

## Final reviewer checklist
- [ ] Dependency is necessary and correctly identified.
- [ ] Maintainer, license, and support status reviewed.
- [ ] Direct and transitive changes understood.
- [ ] Lockfile and integrity data reviewed.
- [ ] Registry source is approved.
- [ ] Install scripts and permissions considered.
- [ ] Tests and SCA checks passed.
- [ ] Exceptions have approval and expiry.
- [ ] SBOM/inventory updated where required.
