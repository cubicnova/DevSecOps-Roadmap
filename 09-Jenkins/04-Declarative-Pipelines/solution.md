# Solutions and Guidance: Declarative Pipelines

These are reference solutions. Adapt commands, labels, plugins, and tool setup to the Jenkins environment.

## Lab 1: Basic pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build') {
            steps {
                echo 'Replace with the application build command'
            }
        }
        stage('Test') {
            steps {
                echo 'Replace with the test command'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed'
        }
        failure {
            echo 'Review the failed stage and console log'
        }
    }
}
```

The demonstration messages should be replaced with real commands. Ensure a failing build or test returns a non-zero status so Jenkins can detect the failure.

## Lab 2: Pipeline options

```groovy
options {
    timeout(time: 30, unit: 'MINUTES')
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
    disableConcurrentBuilds()
}
```

A timeout limits resource consumption. Concurrency protection is useful when jobs share a mutable environment, but it can slow independent builds. Confirm that the plugins required for any chosen option are installed.

## Lab 3: Parameters

```groovy
parameters {
    choice(name: 'TARGET_ENV', choices: ['dev', 'staging'], description: 'Target environment')
    booleanParam(name: 'RUN_EXTRA_CHECKS', defaultValue: true, description: 'Run optional checks')
}
```

Read values through `params.TARGET_ENV` and `params.RUN_EXTRA_CHECKS`. Validate values before using them in commands. Use Jenkins permissions, protected environments, and scoped credentials to control access; parameters only describe requested behavior.

## Lab 4: Branch condition

```groovy
stage('Deploy to Staging') {
    when {
        branch 'main'
    }
    steps {
        echo 'Staging deployment placeholder'
    }
}
```

The `branch` condition is intended for multibranch Pipeline jobs. A branch condition can control execution flow but is not an authorization mechanism. Restrict who can trigger the job and access deployment credentials.

## Lab 5: Stage-level agents

```groovy
pipeline {
    agent none
    stages {
        stage('Linux Validation') {
            agent { label 'linux' }
            steps {
                sh 'uname -a'
            }
        }
        stage('Windows Validation') {
            agent { label 'windows' }
            steps {
                bat 'ver'
            }
        }
    }
}
```

The labels must exist and be assigned to online agents. `agent none` avoids allocating a top-level executor; each stage must specify its own agent if it needs one.

## Lab 6: Parallel tests

```groovy
stage('Test Suites') {
    parallel {
        stage('Unit Tests') {
            steps {
                sh './run-unit-tests.sh'
            }
        }
        stage('API Tests') {
            steps {
                sh './run-api-tests.sh'
            }
        }
    }
}
```

Use isolated temporary directories, test databases, and output paths. Shared mutable resources can introduce race conditions. Parallel execution may reduce elapsed time but increases resource demand.

## Lab 7: Matrix testing

A matrix defines combinations, but the build commands must actually use the selected values. Configure an agent image, tool installation, or runtime manager so each matrix cell receives the expected version. Log the runtime version and fail if it does not match the cell's expected value.

## Lab 8: Approval

```groovy
stage('Approve Staging') {
    input {
        message 'Proceed with staging deployment?'
        ok 'Deploy'
        submitter 'release-managers'
    }
    steps {
        echo 'Approval received'
    }
}
```

Replace `release-managers` with valid configured identities. Also restrict job access, scope credentials, and protect the deployment environment. Verify which identities can approve in your Jenkins version and configuration.

## Lab 9: Credential safety

```groovy
withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
    sh '''
        set +x
        ./scripts/call-service.sh
    '''
}
```

The called script should consume `API_TOKEN` from the environment without printing it. Do not write it to files or artifacts. Prefer trusted, isolated agents and limit which jobs can use the credential.

## Lab 10: JUnit reports

```groovy
post {
    always {
        junit testResults: 'reports/**/*.xml'
    }
}
```

The test runner must produce the XML files, and the Jenkins JUnit plugin must be installed. Keep missing reports as a failure when reporting is a required quality gate.

## Lab 11: Troubleshooting

| Symptom | Likely cause | Next step |
|---|---|---|
| Declarative syntax error | Invalid nesting, braces, or directive placement | Review the reported line and validate the Pipeline syntax |
| Branch stage always skipped | Job is not multibranch or branch metadata differs | Check job type and branch name |
| Wrong matrix runtime | Axis value is not wired to tool selection | Configure per-cell tool/runtime and verify the version |
| Intermittent parallel failure | Shared files, database, port, or environment | Isolate test resources and outputs |
| Unknown `junit` step | JUnit plugin unavailable | Check plugin installation and Jenkins logs |
| Waiting indefinitely | No matching agent, blocked command, or pending input | Inspect queue, agent labels, timeouts, and approval state |

## Lab 12: Final mini-project outline

Recommended sequence:

1. Checkout source.
2. Run lint and static validation.
3. Run independent test suites in parallel.
4. Create the deployable package only after required checks pass.
5. Archive only expected artifacts.
6. Use a branch condition to control staging-stage execution.
7. Require authorized approval and protected deployment credentials.
8. Publish reports and clean up in `post`.

Example artifact archival step:

```groovy
archiveArtifacts artifacts: 'dist/**', fingerprint: true
```

Inspect `dist/` before archiving. Exclude credentials, local configuration, test dumps, and unrelated files.

## Security review checklist

- [ ] Minimal job and credential permissions
- [ ] No hardcoded secrets
- [ ] No untrusted code on privileged agents
- [ ] Required checks fail the pipeline on failure
- [ ] Timeouts prevent stuck jobs
- [ ] Deployment approval and authorization are distinct and both addressed
- [ ] Artifacts are traceable and contain only intended files
- [ ] Plugin requirements and versions are documented

## Official references

- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
- [Getting started with Pipeline](https://www.jenkins.io/doc/book/pipeline/getting-started/)
