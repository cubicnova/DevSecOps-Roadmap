# Trivy Scan Review Checklist

- [ ] Correct target type selected
- [ ] Target path / image digest recorded
- [ ] Lockfiles and manifests are current
- [ ] Trivy version recorded and pinned in CI
- [ ] Vulnerability database status reviewed
- [ ] Required scanners explicitly enabled
- [ ] Severity threshold documented
- [ ] Findings validated against exact package/version
- [ ] Direct/transitive path investigated
- [ ] Reports stored with appropriate access controls
- [ ] Exceptions have owner, evidence, and expiry
- [ ] Re-scan verifies remediation
