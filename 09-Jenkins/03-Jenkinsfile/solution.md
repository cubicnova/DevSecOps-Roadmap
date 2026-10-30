# Solutions and Guidance: Jenkinsfile

Use these as reference answers. Exact commands will vary by application, operating system, installed Jenkins plugins, and agent configuration.

## Lab 1: Basic Declarative Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Build stage'
            }
        }
        stage('Test') {
            steps {
                echo 'Test stage'
            }
        }
        stage('Package') {
            steps {
                echo 'Package stage'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
```

The `echo` statements demonstrate structure only. Replace them with actual build, test, and packaging commands.

## Lab 2: Validation

```groovy
stage('Validate') {
    steps {
        sh 'python3 -m compileall -q .'
    }
}
stage('Unit Tests') {
    steps {
        sh 'python3 -m unittest discover -s tests'
    }
}
```

A non-zero shell exit status normally fails the step and stage. Make sure the repository has the expected tests and that failures are not swallowed by shell constructs or `returnStatus` handling.

## Lab 3: Parameters

```groovy
parameters {
    choice(name: 'TARGET_ENV', choices: ['dev', 'staging'], description: 'Target environment')
    booleanParam(name: 'RUN_EXTRA_CHECKS', defaultValue: true, description: 'Run extra checks')
}
```

Use `params.TARGET_ENV` and `params.RUN_EXTRA_CHECKS` to read parameter values. Parameters are user input, not authorization. Protect sensitive jobs using Jenkins permissions, protected credentials, and deployment controls.

## Lab 4: Conditional stage

```groovy
stage('Deploy to Staging') {
    when {
        branch 'main'
    }
    steps {
        echo 'Deploying to staging'
    }
}
```

The stage is skipped if the condition is false. The `branch` condition is intended for multibranch Pipeline jobs; verify the branch metadata available in your job type.

## Lab 5: JUnit reports

```groovy
post {
    always {
        junit testResults: 'reports/**/*.xml'
    }
}
```

The test runner must generate compatible JUnit XML files at that path, and the Jenkins JUnit plugin must be installed. If reports are mandatory, do not enable `allowEmptyResults` merely to silence errors; missing reports may mean the tests never ran.

## Lab 6: Credentials

```groovy
withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
    sh '''
        set +x
        ./scripts/call-demo-service.sh
    '''
}
```

The script reads `API_TOKEN` from its environment. Avoid printing the variable or passing it through Groovy interpolation. Masking is not a substitute for careful handling of process arguments, logs, workspace files, and agent isolation.

## Lab 7: Timeout and concurrency

```groovy
options {
    timeout(time: 20, unit: 'MINUTES')
    disableConcurrentBuilds()
}
```

A timeout terminates a run that exceeds the configured duration. `disableConcurrentBuilds()` prevents overlapping executions of the same Pipeline; it is useful when shared resources could conflict, but may unnecessarily serialize independent builds.

## Lab 8: Staging gate

Use a `when` condition for branch intent, but enforce authorization separately through Jenkins job permissions, protected branches, environment controls, or a carefully restricted approval step. Keep deployment credentials scoped to the deployment stage where practical. A branch condition alone is not an access-control mechanism.

## Lab 9: Declarative vs Scripted

Declarative:

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { echo 'Build' }
        }
        stage('Test') {
            steps { echo 'Test' }
        }
    }
}
```

Scripted:

```groovy
node {
    stage('Build') {
        echo 'Build'
    }
    stage('Test') {
        echo 'Test'
    }
}
```

Declarative syntax has a more constrained structure and is usually easier to review. Scripted syntax can be useful when complex Groovy flow control is required, but it should not be used to make a simple pipeline harder to understand.

## Lab 10: Troubleshooting

| Symptom | Likely cause | Suggested check |
|---|---|---|
| Syntax error before stages | Missing braces, invalid directive placement, or unsupported syntax | Review the exact line and use Jenkins Pipeline validation tools |
| Command missing | Agent lacks the tool or `PATH` differs | Check agent image, tool installation, and environment |
| Local/CI mismatch | Different runtime, dependency versions, environment, or test data | Pin versions and compare the environment |
| Unknown `junit` step | JUnit plugin missing or unavailable | Check plugin installation and Jenkins logs |
| Branch stage never runs | Not a multibranch job or branch condition mismatch | Inspect `BRANCH_NAME` and job configuration |
| Build hangs | Long-running command or blocked process | Add timeout, inspect console output, and terminate safely |

## Lab 11: Security review examples

| Finding | Risk | Remediation |
|---|---|---|
| Hardcoded token in Jenkinsfile | Credential disclosure and reuse | Move it to Jenkins Credentials and rotate it |
| Secret interpolated in Groovy string | Potential exposure in process arguments or logs | Use single-quoted Groovy shell scripts and let the shell expand the environment variable |
| Untrusted code on privileged agent | Agent compromise or credential theft | Use isolated, disposable agents with no privileged secrets |
| Deployment available to all users | Unauthorized release | Restrict job permissions and use approval controls |
| No timeout | Resource exhaustion or stuck builds | Set realistic timeouts |
| Workspace retains sensitive output | Data leakage to later jobs or users | Clean workspaces and isolate agents |

## Lab 12: Final mini-project outline

A reasonable order is:

1. `Checkout` — retrieve the source.
2. `Static Validation` — syntax, lint, and policy checks.
3. `Unit Tests` — run required tests and publish reports.
4. `Package` — create the deployable output.
5. `Archive Artifact` — archive only expected outputs with fingerprinting where appropriate.
6. `Deploy to Staging` — restrict by branch and authorization.
7. `post` — report results and clean the workspace.

Example artifact archival step:

```groovy
archiveArtifacts artifacts: 'dist/**', fingerprint: true
```

Ensure `dist/` contains only the intended output. Jenkins artifact archiving is useful for basic build retention; a dedicated artifact repository may be more appropriate for long-term or production distribution.

## Further reading

- [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Getting started with Pipeline](https://www.jenkins.io/doc/book/pipeline/getting-started/)
