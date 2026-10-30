# Dependency Security — Suggested Solutions

These are reference answers. Actual remediation depends on the project's ecosystem, affected versions, deployment model, and internal risk policy.

## Solution 1: Direct vs. transitive dependencies

Use the package manager's dependency-tree command and inspect both the manifest and lockfile. Direct dependencies are explicitly declared by the project; transitive dependencies are brought in by other packages. An SBOM and SCA inventory can help map a newly disclosed vulnerable component to affected releases and deployed applications.

## Solution 2: Package adoption review

Verify the exact package name and official registry/source. Review maintainers, release history, project activity, advisory history, license, dependency graph, installation scripts, and whether a standard-library or existing dependency can meet the requirement. Record the decision and approved version in the repository.

## Solution 3: Lockfile review

The manifest and lockfile may no longer describe the same resolved graph, causing different versions to be installed in different environments. Update the lockfile using the intended package manager, inspect the diff, run tests, and commit both files. For npm projects, `npm ci` is commonly used in CI to install from the lockfile. Locking a direct dependency does not necessarily make every transitive version deterministic unless the package manager's lockfile captures the resolved graph.

## Solution 4: SCA triage

Confirm the package identifier and affected version range using the advisory and maintainer source. Trace the transitive dependency to its parent, determine whether the affected code path is reachable, assess exposure and impact, then update to a verified fixed version or replace the package. Rebuild and rescan. Close the ticket only when the deployed artifact is verified or a documented, approved mitigation/exception exists.

## Solution 5: Malicious package indicators

Review suspiciously similar names, new or unexplained maintainers, unusual release patterns, obfuscated code, unexpected install-time behavior, network access unrelated to package purpose, and poor provenance. Indicators are not conclusive by themselves. Use a clean sandbox, inspect package contents and scripts, verify official sources, and follow the organization's package approval process.

## Solution 6: SBOM design

Generate an SBOM during release builds and associate it with the exact artifact digest. Include component names, versions, suppliers/identifiers, dependency relationships, and other supported metadata. Cover application dependencies and relevant OS/container packages. Validate the SBOM format, retain it with release evidence, and continuously map new advisories to stored SBOMs and deployed artifacts. An SBOM can be incomplete, so document its scope and limitations.

## Solution 7: CI/CD gate

Run SCA on pull requests and scheduled builds, then scan final release artifacts. Define severity and exploitability thresholds, assign an owner and due date to findings, and require documented approval for exceptions. Keep an audit trail with rationale and expiry date. Provide an emergency remediation route that remains traceable and does not silently disable scanning.

## Solution 8: License compliance

Use package metadata and appropriate license scanning to identify the declared license, then review the actual license text and relevant obligations with the appropriate legal/compliance process. Record the approved decision and any conditions. Enforce the policy in CI and re-review when a dependency version or license changes.

## Solution 9: Dependency confusion

Configure package managers to use intended registries and namespaces for private packages. Prevent public packages from shadowing internal names where possible, verify sources and package identity, use lockfiles and integrity checks, and restrict who can publish internal packages. Do not rely on package-name similarity or version pinning alone.

## Solution 10: Remediation verification

1. Confirm the intended fixed version is resolved in the lockfile.
2. Run unit, integration, and compatibility tests.
3. Rebuild the application or container image.
4. Inspect the final artifact's dependency inventory.
5. Rescan the artifact with updated vulnerability data.
6. Deploy the verified artifact and map it to the release.
7. Retain evidence and close the finding only after confirming the deployed version.

## Solution 11: Mini incident response

Identify affected versions and every repository/artifact/deployment that contains them. Preserve relevant logs and metadata. Stop promotion of affected builds and isolate or roll back where warranted. Assess whether install scripts or package code could have accessed secrets; rotate potentially exposed credentials based on evidence and risk. Replace the package with a verified safe version or alternative, rebuild and test, scan the final artifact, and communicate the impact and remediation status.

## Solution 12: Mini-project checklist

A complete project includes:
- Manifest and committed lockfile.
- Reproducible CI install.
- Automated SCA scan for direct and transitive dependencies.
- SBOM generation and artifact association.
- A policy for severity, license, and exception handling.
- Clear ownership and due dates for findings.
- Tests and a rescan after upgrades.
- Documentation of scanner limitations and the process for newly disclosed vulnerabilities.

## Further reading

- [OWASP Software Supply Chain Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Software_Supply_Chain_Security_Cheat_Sheet.html)
- [OWASP Dependency Graph & SBOM Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/Dependency_Graph_SBOM_Cheat_Sheet.html)
- [OWASP Dependency-Check](https://owasp.org/projects/dependency-check)
