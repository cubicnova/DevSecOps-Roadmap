# Examples — Jenkins Plugin Security

These examples are intended for a test or approved Jenkins environment. Commands and API access may vary with authentication, authorization, and Jenkins version.

## Example 1: Create a plugin inventory with the Script Console
The Jenkins Script Console is highly privileged. Run this only as an authorized administrator, and do not expose the output publicly.

```groovy
Jenkins.instance.pluginManager.plugins
    .sort { a, b -> a.shortName <=> b.shortName }
    .each { p ->
        println("${p.shortName},${p.version},active=${p.active},enabled=${p.enabled}")
    }
```

For routine operations, prefer approved administrative interfaces or automation that uses a narrowly scoped account. Treat inventory output as internal operational information.

## Example 2: Query the plugin manager API
If your Jenkins instance permits it, an authenticated API request can help retrieve plugin metadata:

```bash
curl --fail --silent --show-error \
  --user "$JENKINS_USER:$JENKINS_API_TOKEN" \
  "$JENKINS_URL/pluginManager/api/json?depth=1" \
  -o plugins.json
```

Store credentials in environment variables or a secret manager, not in source control. Avoid printing tokens in shell history or CI logs. Confirm the endpoint and response schema for your Jenkins version.

## Example 3: Filter an inventory using Python
Save a reviewed inventory as `plugins.csv` with columns `shortName,version,owner,purpose,lastReviewed`.

```python
import csv

with open("plugins.csv", newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))

print(f"Inventory entries: {len(rows)}")
for row in rows:
    if not row.get("owner", "").strip() or not row.get("purpose", "").strip():
        print(
            f"REVIEW: {row.get('shortName', '<unknown>')} "
            "is missing an owner or documented purpose"
        )
```

This checks inventory completeness only. It does not establish whether a plugin is vulnerable or safe.

## Example 4: Declarative change record
Use a record like this for each plugin update:

```yaml
plugin: example-plugin
current_version: "1.2.0"
target_version: "1.2.3"
reason: "Security advisory / compatibility / maintenance"
risk_owner: "CI Platform Team"
test_plan:
  - Verify Jenkins starts cleanly
  - Run representative pipelines
  - Verify required credentials integrations
  - Review controller and agent logs
rollback:
  - Restore approved backup or revert to the known-good plugin version
  - Follow the plugin's documented downgrade guidance
status: "Pending approval"
```

Replace illustrative values with verified facts. A version change may require dependency updates or a Jenkins core upgrade; validate this in staging.

## Example 5: Advisory review checklist
For each advisory, record:
- Advisory URL and publication date
- Plugin short name and affected version range
- Fixed version, if one exists
- Whether the plugin is installed and enabled
- Whether relevant functionality is exposed
- Temporary mitigation and permanent remediation
- Owner, due date, validation evidence

Do not infer affected status from a plugin name alone; compare your installed version with the advisory.

## Example 6: Safe pipeline policy
Do not allow untrusted pull-request code to access production credentials or administrative Jenkins APIs. Keep privileged deployment stages on protected branches/environments, use credentials scoped to the job's need, and review shared libraries and plugin configuration that can execute code.

```groovy
pipeline {
    agent any
    stages {
        stage('Build and test') {
            steps {
                sh 'echo "Run non-privileged build and tests here"'
            }
        }
        stage('Production deployment') {
            when {
                branch 'main'
            }
            steps {
                echo 'Use an approved deployment process and narrowly scoped credentials.'
            }
        }
    }
}
```

This is a teaching example, not a complete production authorization boundary. Enforce branch protection and credential permissions outside this Jenkinsfile too.
