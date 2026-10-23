# Dependency Security — Exercises

Use a local repository or a project you are authorized to assess. Do not install suspicious packages on a machine containing production credentials.

## Exercise 1: Direct vs. transitive dependencies

Draw a dependency tree for a small application. Identify:
- Three direct dependencies.
- At least five transitive dependencies.
- Which manifest or lockfile records each dependency.
- How you would find all applications affected if a transitive package receives a security advisory.

## Exercise 2: Review a package before adoption

Choose a package you might use in a demo project. Create a review record covering package identity, registry/source, maintainer, release history, maintenance activity, security advisories, license, dependency count, and whether the package is necessary.

## Exercise 3: Lockfile review

A developer changes `package.json` but does not commit the updated `package-lock.json`.

1. Explain why builds may become inconsistent.
2. Describe the correct lockfile workflow.
3. List the CI command you would use for a reproducible install.
4. Explain why pinning only a direct dependency may not pin its entire transitive graph.

## Exercise 4: Triage an SCA finding

An SCA scanner reports a high-severity vulnerability in a transitive package.

1. Verify the affected version range and fixed versions.
2. Identify which direct dependency introduces the package.
3. Assess whether the affected functionality is reachable and exposed.
4. Recommend an update, replacement, or documented mitigation.
5. Define evidence required before closing the finding.

## Exercise 5: Malicious package indicators

List warning signs that deserve review before installing a package, such as confusing package names, unusual maintainer changes, unexpected install scripts, suspicious network behavior, or a lack of credible project history. Explain why any single indicator should be investigated rather than treated as conclusive proof.

## Exercise 6: SBOM design

Design a release SBOM process. Specify:
- When the SBOM is generated.
- Whether it covers source dependencies, container/OS packages, and final artifacts.
- Required component metadata.
- Where the SBOM is stored.
- How it is associated with the exact release artifact.
- How new advisories are mapped to deployed versions.

## Exercise 7: CI/CD security gate

Design a pipeline that runs dependency checks on pull requests, scheduled scans, and release artifacts. Define a reasonable policy for high/critical findings, false positives, exceptions, and emergency fixes. Include the person or team responsible for approving exceptions.

## Exercise 8: License compliance

A new dependency has a license not currently on the project's approved list.

Describe how you would identify the license, review obligations, record a decision, and prevent unapproved licenses from silently entering future releases.

## Exercise 9: Dependency confusion and registry trust

A company uses both private and public package registries. Explain how namespace controls, registry configuration, package-source verification, and immutable dependency references can reduce dependency-confusion risk.

## Exercise 10: Remediation verification

A vulnerable package was upgraded. List the steps required to verify that the fix actually reached the deployed application, including lockfile checks, tests, rebuilt artifact inspection, rescan, and deployment mapping.

## Exercise 11: Mini incident response

A maintainer announces that a package version used by your application may have been compromised.

Write an initial response checklist that covers:
- Identify affected repositories and deployed artifacts.
- Determine exact versions and installation times if available.
- Isolate or remove affected builds where necessary.
- Rotate credentials if there is evidence they may have been exposed.
- Pin or replace with a verified safe release.
- Preserve relevant logs and evidence.
- Rebuild, validate, and communicate status.

## Exercise 12: Mini-project

Create a small Node.js or Python project with:
- A committed dependency manifest and lockfile.
- An automated SCA scan.
- An SBOM generation step.
- A documented remediation policy.
- A license review checklist.
- CI that fails on findings defined by your policy.
- A short report describing limitations and exception handling.

**Acceptance criteria:** direct and transitive dependencies are inventoried; installs are reproducible; findings have owners and remediation evidence; the SBOM is linked to the exact release artifact.
