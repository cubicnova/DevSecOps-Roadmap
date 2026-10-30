# OWASP Dependency-Check – Examples

## 1. CLI scan
```bash
./bin/dependency-check.sh \
  --project "Demo Service" \
  --scan ./target \
  --out ./reports \
  --format "HTML"
```
Scan the project root or built artifacts as appropriate. A scan of only `target/` may miss manifests or other dependency evidence; choose the path based on the project and analyzer support.

## 2. Maven plugin
```xml
<plugin>
  <groupId>org.owasp</groupId>
  <artifactId>dependency-check-maven</artifactId>
  <version>REPLACE_WITH_CURRENT_VERSION</version>
  <configuration>
    <failBuildOnCVSS>7.0</failBuildOnCVSS>
    <nvdApiKeyEnvironmentVariable>NVD_API_KEY</nvdApiKeyEnvironmentVariable>
    <formats>
      <format>HTML</format>
      <format>JSON</format>
    </formats>
  </configuration>
  <executions>
    <execution>
      <goals><goal>check</goal></goals>
    </execution>
  </executions>
</plugin>
```
This is an illustrative configuration. Confirm parameter names and supported report formats against the exact plugin version. Set a threshold only after defining triage and exception processes.

## 3. Suppression file structure
See `examples/suppression-example.xml`. A suppression should identify a specific, validated false positive and include a clear explanation and review date. Never suppress a whole family of CVEs simply to make a build green.

## 4. GitHub Actions
See `.github/workflows/dependency-check.yml`. The example uses an environment secret for the NVD key and uploads the report as an artifact. Before production, pin the action to a full commit SHA, review fork/PR secret exposure, and choose a cache strategy that avoids concurrent writes.

## 5. Report triage
For every high-priority result, verify:
- exact package and version;
- advisory's affected version range;
- dependency path and whether it is included in the shipped artifact;
- vulnerable functionality reachability and exposure;
- exploit intelligence and business impact;
- fixed release and regression test plan.

## 6. Maven sample project
`maven-demo/pom.xml` contains a small dependency set to practice plugin execution. It intentionally uses a placeholder plugin version; replace it with a current verified release before running.
