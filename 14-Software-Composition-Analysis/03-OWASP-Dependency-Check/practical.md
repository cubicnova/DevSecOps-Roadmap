# Practical Exercises – OWASP Dependency-Check

## Lab 1: Install and validate the CLI
1. Install a supported Java runtime.
2. Download a current official Dependency-Check release.
3. Verify `--version` and inspect `--help`.
4. Record the installed version and Java version.
**Deliverable:** installation record.

## Lab 2: First dependency scan
1. Use the included `maven-demo` or another authorized project.
2. Run Dependency-Check against the project root.
3. Generate an HTML report.
4. Identify at least three dependency records (or document why fewer were identified).
5. Record scanner version, scan date, and data-update status.

## Lab 3: Configure NVD API access
1. Request an API key from the official NVD site.
2. Store it in an environment variable or CI secret.
3. Configure Dependency-Check using the documented environment-variable setting.
4. Confirm logs do not print the key.
5. Document how your team will handle shared-key rate limits and cache updates.
Never put a real API key in the repository or in screenshots.

## Lab 4: Maven integration
1. Replace the placeholder plugin version in `maven-demo/pom.xml` with a current supported version.
2. Configure the environment variable for the NVD key.
3. Run `mvn verify`.
4. Inspect generated reports and note whether the build gate triggered.
5. Run tests after any dependency upgrade.

## Lab 5: False-positive investigation and suppression
1. Select a report entry that appears to be a false positive (use a lab fixture if none exists).
2. Verify package identity, CPE evidence, version, and advisory range.
3. Record the evidence in `templates/finding-triage.md`.
4. Create a narrowly scoped suppression based on the official schema.
5. Re-run the scan and confirm only the intended finding is suppressed.
Do not suppress a real vulnerability simply to pass the lab.

## Lab 6: CI/CD integration
1. Review `.github/workflows/dependency-check.yml`.
2. Replace mutable action tags with full commit SHAs before production use.
3. Configure `NVD_API_KEY` as a repository or environment secret.
4. Test on a trusted branch and an untrusted fork PR; confirm secrets are not exposed.
5. Retain reports as controlled artifacts and define a failure/exception policy.

## Lab 7: Troubleshooting
Investigate one scenario: slow NVD update, HTTP 403/rate limit, missing dependency, false positive, or database migration issue. Use official documentation and record root cause, evidence, fix, and prevention.

## Submission checklist
- [ ] CLI and Java version record
- [ ] HTML/JSON scan report
- [ ] NVD key handling notes (no key value)
- [ ] Maven configuration and execution result
- [ ] Triage and suppression evidence
- [ ] CI/CD security review
- [ ] Troubleshooting report
