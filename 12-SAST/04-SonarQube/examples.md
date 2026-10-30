# SonarQube — Examples

The following are training examples. Replace project keys and server URLs with values from your own instance. Keep credentials out of source control.

## 1. Basic project configuration

`sonar-project.properties`:
```properties
sonar.projectKey=training-python-app
sonar.projectName=Training Python App
sonar.projectVersion=1.0
sonar.sources=src
sonar.tests=tests
sonar.sourceEncoding=UTF-8
```

Run:
```bash
sonar-scanner
```

## 2. Run analysis with command-line properties

```bash
sonar-scanner \
  -Dsonar.projectKey=training-python-app \
  -Dsonar.sources=src \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.token="$SONAR_TOKEN"
```

The token should be supplied securely using the scanner's supported authentication configuration. Avoid committing it or printing it.

## 3. Python coverage integration

Run tests:
```bash
python -m pip install pytest coverage
coverage run -m pytest
coverage xml -o coverage.xml
```

Configure:
```properties
sonar.projectKey=training-python-app
sonar.sources=src
sonar.tests=tests
sonar.python.coverage.reportPaths=coverage.xml
```

Run `sonar-scanner` after the coverage report exists. SonarQube imports the coverage report; the test framework generates it.

## 4. Java Maven analysis

Example:
```bash
mvn clean verify sonar:sonar \
  -Dsonar.projectKey=training-java-app \
  -Dsonar.host.url="$SONAR_HOST_URL"
```

Provide authentication using a secure environment or Maven/CI secret configuration supported by your scanner version. Avoid placing tokens in committed `pom.xml` files.

## 5. Java Gradle analysis

A typical workflow uses the SonarQube Gradle plugin in the build configuration and runs:
```bash
./gradlew test sonar
```

The exact plugin declaration and task configuration depend on the Gradle plugin and SonarQube version. Follow the current official Gradle scanner documentation.

## 6. GitLab CI scanner job

```yaml
stages:
  - test
  - quality

variables:
  GIT_DEPTH: "0"

sonarqube:
  stage: quality
  image: sonarsource/sonar-scanner-cli:latest
  script:
    - sonar-scanner
      -Dsonar.projectKey="$SONAR_PROJECT_KEY"
      -Dsonar.host.url="$SONAR_HOST_URL"
      -Dsonar.qualitygate.wait=true
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

Set `SONAR_PROJECT_KEY`, `SONAR_HOST_URL`, and `SONAR_TOKEN` in GitLab CI/CD settings. Use protected and masked/hidden settings appropriate to your trust model. Pin the scanner image in production.

## 7. Quality Gate wait

Add this property to wait for the server's Quality Gate result:
```properties
sonar.qualitygate.wait=true
```

Or pass it to the scanner:
```bash
sonar-scanner -Dsonar.qualitygate.wait=true
```

This causes the scanner process to wait for the Quality Gate result and fail when the gate fails. Account for the longer job duration and configure an appropriate CI timeout.

## 8. Exclude generated files

```properties
sonar.exclusions=**/generated/**,**/vendor/**,**/build/**
sonar.coverage.exclusions=**/tests/**,**/migrations/**
```

Use exclusions sparingly and document their reason. Excluding files from coverage is different from excluding them from source analysis.

## 9. Test and source paths

```properties
sonar.sources=src,services
sonar.tests=tests,integration-tests
sonar.test.inclusions=**/*Test.py,**/test_*.py
```

Ensure the paths and inclusion patterns match the actual repository layout and the language analyzer's supported conventions.

## 10. New-code quality strategy

A sensible team policy can be:
- Use a consistent new-code definition.
- Require no new blocker or critical issues according to the team's policy.
- Review all new security hotspots.
- Set coverage and duplication targets that fit the project.
- Avoid adding arbitrary thresholds without a reliable baseline.

Configure the actual conditions in the Quality Gate UI or supported API. Do not assume the illustrative policy is the default.

## 11. Local Docker-based lab instance

For a local disposable lab, use the current official SonarQube container instructions and system requirements. A minimal illustrative command is:

```bash
docker run -d --name sonarqube-lab \
  -p 9000:9000 \
  sonarqube:community
```

This is for a local learning environment only. Production deployments need persistent storage, supported database configuration where required, resource sizing, backups, access controls, TLS, and a supported version. The default image tag may change; pin a version for repeatable labs.

## 12. Review issues and hotspots

In the project dashboard:
1. Open **Issues** to review bugs, vulnerabilities, and code smells.
2. Open **Security Hotspots** to review security-sensitive code.
3. Inspect the rule description and highlighted code.
4. Review the source, sink, execution context, and mitigations.
5. Record the decision and remediation evidence.

Do not mark a hotspot safe without a reasoned review.

## 13. Example secure coding issue

Training code:
```python
import sqlite3

def get_user(connection, username):
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    return connection.execute(query).fetchall()
```

Safer parameterized query:
```python
def get_user(connection, username):
    return connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchall()
```

A static analyzer may detect some unsafe query patterns, but verify the actual rule, language support, and data-flow coverage for the analyzer version in use.

## 14. Scanner troubleshooting with debug logs

```bash
sonar-scanner -X
```

Debug logs may contain internal paths, hostnames, or other sensitive metadata. Redact before sharing. Never paste a token into a command that may be saved in shell history.
