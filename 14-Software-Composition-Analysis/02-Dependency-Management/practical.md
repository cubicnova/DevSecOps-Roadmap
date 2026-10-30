# Dependency Management — Practical Exercises

## Lab safety
Use a local sample repository and disposable VM/container for package-risk exercises. Do not install unknown packages on a workstation containing credentials. Never test dependency confusion against a real organization's private namespace.

Suggested tools: npm, pip/uv, Go or Maven, Git, Dependabot or Renovate, an SCA scanner, and an SBOM generator.

## Exercise 1 — Identify dependency types
Inspect a sample project.
1. List direct dependencies.
2. Identify at least five transitive dependencies.
3. Separate runtime and development dependencies.
4. Identify optional dependencies.
5. Explain why transitive dependencies affect security.

**Deliverable:** `dependency-inventory.md`

## Exercise 2 — Reproducible npm build
1. Create a small Node project.
2. Add runtime and development dependencies.
3. Generate `package-lock.json`.
4. Commit manifest and lockfile.
5. Remove `node_modules` and run `npm ci`.
6. Compare the installed tree with the lockfile.

**Deliverable:** manifest, lockfile, command output, and explanation.

## Exercise 3 — Pin Python dependencies
1. Create a virtual environment.
2. Add packages to a requirements file.
3. Pin versions.
4. Install and run `pip check`.
5. Explain why a pin differs from a hash or signature.
6. Research hash-locking for your selected package manager.

**Deliverable:** `requirements.txt` and setup notes.

## Exercise 4 — Dependency due diligence
Assess a package from its official project source. Review package identity, publisher, maintenance, license, security policy, transitive footprint, install scripts, and provenance. Provide an approval recommendation.

**Deliverable:** completed assessment checklist.

## Exercise 5 — Typosquatting review
Create a fictional list of package names with deliberate spelling similarities. Compare exact spelling, official registry links, publisher identity, and repository URLs. Explain why download count alone is insufficient. Do not publish or install lookalike packages.

**Deliverable:** typosquatting risk worksheet.

## Exercise 6 — Review a lockfile diff
Update one dependency on a branch. Inspect manifest and lockfile diffs, added/removed transitive packages, registry URLs, and integrity values. Run tests and SCA. Write a PR review decision.

**Deliverable:** annotated lockfile review.

## Exercise 7 — Configure automated updates
Enable Dependabot or Renovate in a test repository. Configure weekly checks and PR limits, add release-age cooldown if supported, document emergency security exceptions, and review a generated PR.

**Deliverable:** update-bot configuration and review record.

## Exercise 8 — Private registry design
Design a package source architecture for public and private dependencies. Define internal scopes, registry mapping, precedence/fallback, CI read-only credentials, publish credentials, allow/block rules, and audit requirements. Explain how this reduces dependency confusion.

**Deliverable:** architecture diagram or Markdown design.

## Exercise 9 — Install-script threat model
Inspect lifecycle/build scripts in a trusted sample package or local demonstration package. Identify what runs and with what permissions. Propose isolation, egress restrictions, secret removal, and a build-script allowlist.

**Deliverable:** install-script risk assessment.

## Exercise 10 — Dependency update policy
Define patch/minor/major handling, security-update priority, review/testing requirements, cooldown and exceptions, owners/SLAs, rollback, and emergency release steps.

**Deliverable:** `dependency-update-policy.md`

## Exercise 11 — Remove an unused dependency
Identify a candidate and check imports, scripts, plugins, and dynamic loading. Confirm no other package requires it. Remove it with the package manager, regenerate the lockfile, run tests/SCA, and confirm it is absent from the resolved tree.

**Deliverable:** code diff and evidence.

## Exercise 12 — CI dependency gate
Create a pipeline that performs locked install, tests, package audit or SCA scan, report publication, and a policy-defined failure for new high/critical findings. Use a test repository and do not expose secrets to untrusted pull requests.

**Deliverable:** pipeline YAML and sample output.

## Exercise 13 — SBOM and vulnerability response
Generate an SBOM for a sample application. Record component name/version/ecosystem/relationship. Match a fictional or lab advisory to affected versions, identify impacted artifacts, and propose a patch/replacement and verification plan.

**Deliverable:** SBOM and impact-analysis note.

## Exercise 14 — Dependency maturity review
Assess lockfiles, frozen install, dependency review, approved registries, automated updates, scheduled SCA, license policy, SBOM generation, retirement of unused/EOL packages, and emergency override. Rate each Not Implemented, Partial, or Implemented and prioritize three improvements.

**Deliverable:** maturity assessment and action plan.

## Submission checklist
- [ ] Commands and tool versions recorded.
- [ ] No real secrets included.
- [ ] Manifests and lockfiles consistent.
- [ ] Findings supported by evidence.
- [ ] Dependency changes pass tests.
- [ ] Package identity and registry reviewed.
- [ ] Exceptions have owner and expiry.
