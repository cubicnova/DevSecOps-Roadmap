# 03 – OWASP Dependency-Check

## Learning objectives
- Install and run OWASP Dependency-Check using its CLI and Maven integration.
- Explain how analyzers collect evidence and map components to CPEs and CVEs.
- Configure NVD data updates and API credentials safely.
- Generate, read, and triage HTML/JSON reports.
- Create narrowly scoped suppression rules and document exceptions.
- Integrate dependency scanning into CI/CD without exposing secrets.

## 1. Overview
OWASP Dependency-Check is an SCA tool that attempts to identify publicly disclosed vulnerabilities in project dependencies. Its analyzers gather evidence about components; the engine may map that evidence to a Common Platform Enumeration (CPE), then associate the CPE with known CVEs. It also uses ecosystem-specific analyzers where supported.

A match is a lead for investigation, not proof of exploitability. Incorrect or ambiguous component identification can produce false positives. Validate package identity, version, affected range, and application context.

## 2. Prerequisites and version notes
- Install a supported Java runtime. Current project documentation specifies Java 11 as the minimum for Dependency-Check 11+.
- Use a current supported Dependency-Check release; check release notes before upgrading.
- Ensure the scanner can reach the configured data sources, or configure approved proxy/mirror infrastructure.
- For npm, pnpm, Yarn, Ruby, Go, .NET, and other ecosystems, additional tools/runtimes may be needed by the corresponding analyzers.
- The NVD API key is highly recommended. Keep it in an environment variable or CI secret; never commit it to source control.

The project's current documentation contains important compatibility notices: Dependency-Check 12.1.0+ is required due to NVD API compatibility changes. Confirm the exact current release and migration notes before use.

## 3. CLI installation and first scan
Download the release archive from the official project release page, extract it, and inspect the help output.

Linux/macOS:
```bash
./bin/dependency-check.sh --version
./bin/dependency-check.sh --help
```

Windows PowerShell:
```powershell
.\bin\dependency-check.bat --version
.\bin\dependency-check.bat --help
```

Set the NVD key in the environment rather than placing it in a command committed to a script.

Linux/macOS:
```bash
export NVD_API_KEY="your-key-from-a-secret-store"
./bin/dependency-check.sh \
  --project "Training Application" \
  --scan ./sample-project \
  --out ./odc-reports \
  --format "HTML" \
  --nvdApiKey "$NVD_API_KEY"
```

Windows PowerShell:
```powershell
$env:NVD_API_KEY = "your-key-from-a-secret-store"
.\bin\dependency-check.bat `
  --project "Training Application" `
  --scan .\sample-project `
  --out .\odc-reports `
  --format HTML `
  --nvdApiKey $env:NVD_API_KEY
```

Avoid printing secrets in shell traces or CI logs. If your deployment supports the environment-variable configuration option, prefer it over a literal CLI argument.

## 4. Maven integration
Add the plugin to `pom.xml` (use a current version verified from official documentation/release notes):

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.owasp</groupId>
      <artifactId>dependency-check-maven</artifactId>
      <version>REPLACE_WITH_CURRENT_VERSION</version>
      <executions>
        <execution>
          <goals>
            <goal>check</goal>
          </goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

Run:
```bash
mvn verify
```

Or invoke the goal directly:
```bash
mvn org.owasp:dependency-check-maven:check
```

Configure the NVD API key through the documented environment-variable setting or Maven server credentials. Do not use a literal key in a committed POM. The plugin's `nvdApiKeyEnvironmentVariable` option is intended for CI environments.

## 5. Report formats and interpretation
Common report formats include HTML, JSON, and XML; supported formats depend on the installed release. HTML is useful for review; JSON/XML are useful for automation and evidence retention.

Review:
1. Identified dependency and evidence used.
2. CPE mapping and confidence/identification details shown by the report.
3. CVE identifier, severity, description, and affected version range.
4. Whether the exact version is present in the resolved dependency graph.
5. Whether the vulnerable code path is reachable and exposed.
6. Fixed version, upgrade compatibility, and remediation evidence.

Do not treat CVSS alone as the priority. Consider exploit availability, CISA KEV status where applicable, EPSS, exposure, business impact, and available mitigations.

## 6. Suppression files
Suppressions are appropriate for validated false positives or accepted findings under an approved process—not for hiding inconvenient results. Prefer the narrowest matching criteria:
- exact dependency coordinates or package URL where supported;
- specific CVE;
- explicit version scope where appropriate;
- a comment explaining evidence and a review/expiry date.

Avoid broad CPE or CVE suppressions that may hide future affected versions. Review suppression files periodically and remove obsolete entries.

Example XML structure is provided in `examples/suppression-example.xml`. Confirm the schema and supported fields for your installed version before use.

## 7. NVD updates, caching, and rate limits
Dependency-Check downloads vulnerability data from external sources. The initial data population can be large and slow. Keep the local database/cache between runs. An NVD API key is strongly recommended; concurrent jobs sharing a key can hit rate limits. Use a controlled cache/update strategy and avoid launching many independent database updates at once.

Do not share a writable H2 data directory between incompatible versions or concurrent jobs unless the official documentation explicitly supports that arrangement. Plan database migration and purge operations carefully.

## 8. CI/CD security
- Pin third-party GitHub Actions to immutable commit SHAs in production.
- Give jobs least-privilege permissions.
- Keep NVD credentials in repository/environment secrets.
- Do not expose secrets to untrusted pull-request code from forks.
- Cache the data directory safely and avoid concurrent database corruption.
- Publish reports as controlled artifacts; consider whether they expose internal package inventory.
- Define policy thresholds and exception handling before making a scan blocking.

An example workflow is in `.github/workflows/dependency-check.yml`. Review action versions, cache paths, secret handling, and the selected Dependency-Check version before production use.

## 9. Troubleshooting
| Symptom | Checks |
|---|---|
| Slow first scan | Initial NVD data population, network access, API key, proxy |
| 403/rate limit | Key validity, concurrent jobs, request delay, shared cache |
| No dependencies detected | Correct scan path, lockfiles/artifacts, ecosystem tools, analyzer support |
| False positive | Evidence, CPE mapping, exact version, suppression scope |
| Database errors after upgrade | Read migration notes; back up and follow documented purge/migration steps |
| Build fails on findings | Check configured CVSS threshold and policy; triage before changing threshold |

## Labs
Complete `practical.md`. Use `templates/` to retain scan and remediation evidence. The sample Maven project and fixtures are educational.

## Official references
- Project overview: https://owasp.org/projects/Dependency-Check
- CLI documentation: https://dependency-check.github.io/DependencyCheck/dependency-check-cli/
- Maven plugin: https://dependency-check.github.io/DependencyCheck/dependency-check-maven/
- Maven check goal: https://dependency-check.github.io/DependencyCheck/dependency-check-maven/check-mojo.html
- Data sources/network requirements: https://dependency-check.github.io/DependencyCheck/data/index.html
- NVD API key: https://nvd.nist.gov/developers/request-an-api-key
