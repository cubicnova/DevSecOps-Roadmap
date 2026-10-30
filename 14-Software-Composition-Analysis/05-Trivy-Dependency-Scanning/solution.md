# Solutions and Instructor Guidance

Results vary by Trivy release, target contents, supported ecosystems, scanner configuration, and vulnerability database snapshot.

## Lab 1
Record exact Trivy version and inspect installed help. Avoid assuming flags from old tutorials remain valid.

## Lab 2
Repository scanning analyzes supported dependency metadata, especially lockfiles. If no packages are detected, verify target path, lockfile presence/format, and ecosystem support. It does not replace scanning arbitrary compiled artifacts or final images.

## Lab 3
Current documentation enables vulnerability and secret scanning by default for repository/filesystem scans. Misconfiguration and license scanners must be explicitly selected. Record scanner selection in evidence.

## Lab 4
A CycloneDX SBOM should contain document metadata and component identities/versions. Compare it with the lockfile and built/deployed artifact; source SBOMs may omit OS packages included in a container image.

## Lab 5
`--exit-code 1` causes a non-zero status when findings match the configured filter. Severity threshold is a policy choice, not a universal standard. Use a documented exception process.

## Lab 6
Good triage records exact package/version, advisory range, dependency path, artifact presence, reachability, exposure, exploit intelligence, remediation, owner, and retest evidence. Severity alone is insufficient.

## Lab 7
Production CI should use immutable action SHAs, least privilege, safe secret handling, controlled artifact access, pinned scanner versions, and explicit policy ownership.

## Troubleshooting
- No packages: verify lockfile and target path.
- Unexpected findings: validate package identity and database freshness.
- CI failure: inspect exit code and severity filter.
- Missing scanner types: explicitly set `--scanners` and check release support.
- SBOM differences: confirm target type (repository, filesystem, or image).

## Assessment rubric
- Installation and target selection: 15%
- Repository/filesystem scans: 20%
- SBOM generation: 15%
- CI gate and reporting: 15%
- Evidence-based triage: 20%
- Workflow security/documentation: 15%
