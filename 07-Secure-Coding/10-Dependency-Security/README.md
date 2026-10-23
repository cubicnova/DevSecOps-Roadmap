# Dependency Security

This module explains how to manage third-party and open-source dependencies securely throughout the software development lifecycle. It covers dependency inventory, vulnerability scanning, lockfiles, supply-chain risks, Software Bills of Materials (SBOMs), and remediation workflows.

## Learning objectives

By completing this module, you should be able to:

- Explain direct and transitive dependencies.
- Identify common dependency risks, including known vulnerabilities, abandoned packages, malicious packages, typosquatting, and dependency confusion.
- Use lockfiles and reproducible installation practices.
- Run Software Composition Analysis (SCA) and interpret findings.
- Generate and review an SBOM.
- Prioritize remediation based on severity, exposure, exploitability, and business impact.
- Integrate dependency checks into CI/CD without treating a scanner as a complete security guarantee.

## Why dependency security matters

Applications often rely on libraries, frameworks, build tools, plugins, container base images, and operating-system packages maintained by other parties. A vulnerability or compromise in one component can affect applications that include it, even if developers never directly call the vulnerable functionality.

A **direct dependency** is selected explicitly by a project. A **transitive dependency** is pulled in by another dependency. Inventory both: an application can ship a vulnerable transitive package without naming it in its main manifest.

## Common risks

| Risk | Description | Example mitigation |
|---|---|---|
| Known vulnerability | A package version has a published security advisory | SCA scanning, upgrade or documented mitigation |
| Unmaintained dependency | No reliable security updates or support | Assess maintenance; replace when appropriate |
| Typosquatting | Package name imitates a popular package | Verify package identity and publisher |
| Dependency confusion | A package manager retrieves a malicious package from an unintended source | Configure trusted registries and namespace controls |
| Compromised maintainer/account | A legitimate package or release is altered | Verify provenance and integrity; monitor advisories |
| Malicious install scripts | Package installation executes unexpected code | Review scripts, restrict CI permissions, use isolated builds |
| License risk | Dependency license conflicts with product obligations | License inventory and policy review |
| Lockfile drift | Builds resolve different versions unexpectedly | Commit lockfiles and use reproducible install commands |

## Secure dependency workflow

1. **Choose deliberately:** confirm package name, source, maintainer, release history, support status, license, and necessity.
2. **Minimize:** remove unused dependencies and avoid adding a large package for a small requirement.
3. **Pin resolved versions:** commit the appropriate lockfile and use the package manager's reproducible installation mode.
4. **Verify source and integrity:** use trusted registries, package signatures or provenance where available, and integrity checks.
5. **Scan continuously:** run SCA against direct and transitive dependencies in pull requests, builds, and released artifacts.
6. **Create an SBOM:** record components and relationships for each release.
7. **Triage findings:** verify affected versions and applicability; prioritize exploitable and high-impact issues.
8. **Remediate:** update to a fixed version, replace or remove the component, or apply a documented mitigation where an update is not possible.
9. **Test and rebuild:** run tests, rebuild artifacts, rescan, and confirm the deployed artifact contains the intended version.
10. **Monitor releases:** new advisories can affect software already deployed.

## Lockfiles and reproducible installs

A manifest describes declared dependencies; a lockfile records a resolved dependency graph. Commit lockfiles for applications when supported, review changes, and use package-manager commands designed for deterministic installs.

Examples:

```bash
# Node.js / npm: install exactly from package-lock.json
npm ci

# Python: install from a pinned requirements file
python -m pip install -r requirements.txt

# Python: inspect installed packages
python -m pip list
```

A pinned requirements file alone may not capture every transitive package unless all relevant versions are pinned or a lock tool is used. Follow the ecosystem's recommended locking workflow. Never update dependencies blindly in production without testing.

## Software Composition Analysis (SCA)

SCA tools identify packages and compare them with vulnerability and policy data. Examples include:

- **OWASP Dependency-Check** — identifies dependencies with known publicly disclosed vulnerabilities.
- **OSV-Scanner** — checks dependencies against the Open Source Vulnerabilities database.
- **Trivy** — scans source repositories, dependencies, container images, and other artifacts.
- **GitHub dependency review / Dependabot alerts** — helps detect vulnerable dependency changes and known advisories in GitHub projects.

Tool coverage differs. A scan may miss unsupported ecosystems, embedded libraries, runtime-loaded components, or vulnerabilities not represented in its data sources. Review the report and compare inventories against the final artifact.

## SBOM fundamentals

A **Software Bill of Materials (SBOM)** is a machine-readable inventory of software components. Common formats include CycloneDX and SPDX. A useful SBOM can record:

- Component name, version, supplier, and identifiers.
- Direct and transitive dependency relationships.
- License and hashes where available.
- Product/release identity, creation time, and generation tool.

Generate an SBOM for each release and, where relevant, compare source-level inventory with the final container or binary. An SBOM improves visibility but does not prove that a component is safe or that the inventory is complete.

## Remediation priority

Do not prioritize solely by a CVSS score or dependency depth. Consider:

- Whether the deployed version is affected.
- Whether vulnerable functionality is reachable in your application.
- Network exposure and privileges required for exploitation.
- Known exploitation, such as inclusion in an authoritative exploited-vulnerability catalog.
- Data sensitivity, business criticality, and available mitigations.
- Fixed-version availability and upgrade risk.

Record the decision, owner, due date, validation evidence, and any accepted residual risk. Reassess exceptions when the application or threat information changes.

## Dependency security checklist

- [ ] Review direct and transitive dependencies.
- [ ] Verify package identity, source, publisher, and maintenance status.
- [ ] Commit and review lockfiles.
- [ ] Use reproducible package-manager installation commands.
- [ ] Configure trusted registries and namespaces.
- [ ] Scan dependencies in pull requests and CI.
- [ ] Generate and retain an SBOM for each release.
- [ ] Check licenses and policy requirements.
- [ ] Restrict install/build scripts and CI credentials.
- [ ] Prioritize and track remediation.
- [ ] Rebuild, retest, and rescan after fixes.
- [ ] Monitor released artifacts for newly disclosed vulnerabilities.

## Safe lab boundaries

Run scans and package experiments in your own repository or a system you are authorized to assess. Use isolated environments for untrusted packages; do not install suspicious packages on a workstation with production credentials.

## Further reading

- [OWASP Software Supply Chain Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)
- [OWASP Dependency Graph & SBOM Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Dependency_Graph_SBOM_Cheat_Sheet.html)
- [OWASP Developer Guide: Dependencies](https://devguide.owasp.org/en/05-implementation/02-dependencies/)
- [OWASP Dependency-Check](https://owasp.org/projects/dependency-check)
- [OWASP Top 10:2025 — Software Supply Chain Failures](https://top10.owasp.org/2025/A03_2025-Software_Supply_Chain_Failures/)
