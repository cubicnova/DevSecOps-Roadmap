# Solutions and Instructor Guidance

Actual scan results vary by project, lockfile, scanner version, advisory database, and scan date.

## Lab 1
Record package name, resolved version, ecosystem, PURL where available, direct/transitive status, runtime/development classification, and source. Use the package manager's dependency-tree command. A package absent from the top-level manifest may still be present transitively.

## Lab 2
A strong finding record includes exact package/version, advisory and affected range, scanner/database timestamp, fixed version, evidence the package is in the artifact, reachability/exposure analysis, business impact, owner, and verification plan. For a clean scan, report what was actually scanned and unsupported ecosystems/files.

## Lab 3
Record format and version, generator/tool version, target artifact or source revision, generation time, and component identifiers. Source-only SBOMs may omit OS packages or runtime layers.

## Lab 4
Use exact-version metadata and upstream license files. Record `unknown` when evidence is absent or conflicting; do not make legal conclusions from a scanner label alone.

## Lab 5
Usually prefer upgrading to a supported fixed version, then replacing or removing an unnecessary dependency. If no safe fix exists, use a documented temporary mitigation. Record residual risk, owner, approval, expiry/review date, and retest evidence.

## Lab 6
Use least-privilege permissions, pin third-party actions to full commit SHAs, avoid exposing secrets to untrusted fork code, and report exact package/advisory/remediation. Policy thresholds should be explicit and actionable.

## Discussion
- An SBOM is a point-in-time inventory unless refreshed.
- A database match may be a false positive if identity/version or affected range is misidentified.
- Transitive dependencies require checking the resolved graph and parent path.
- License policy and vulnerability severity represent different risk domains.
