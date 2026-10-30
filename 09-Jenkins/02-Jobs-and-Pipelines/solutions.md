# Jenkins Jobs and Pipelines — Suggested Solutions

## Lab 1: Freestyle job

Example shell commands:

```bash
echo "Hello from Jenkins"
echo "Build number: ${BUILD_NUMBER}"
pwd
```

Build numbers normally increase with each successful job scheduling/execution, including runs that may fail. Inspect the build history and console output to confirm.

## Lab 2: Simple Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Build stage completed'
            }
        }
        stage('Test') {
            steps {
                echo 'Test stage completed'
            }
        }
    }
}
```

A Declarative Pipeline must have a top-level `pipeline` block. `stages` contains the ordered stages, and each stage contains `steps` or another permitted stage structure.

## Lab 3: Shell commands

Linux example:

```groovy
pipeline {
    agent any
    stages {
        stage('System info') {
            steps {
                sh 'pwd'
                sh 'whoami'
                sh 'uname -a'
            }
        }
    }
}
```

Windows example:

```groovy
pipeline {
    agent any
    stages {
        stage('System info') {
            steps {
                bat 'echo Running on Windows'
                bat 'ver'
            }
        }
    }
}
```

The agent operating system determines which shell commands are available.

## Lab 4: Environment variables

```groovy
pipeline {
    agent any
    environment {
        APP_NAME = 'demo-app'
        BUILD_LABEL = 'training'
    }
    stages {
        stage('Show values') {
            environment {
                STAGE_NAME = 'validation'
            }
            steps {
                echo "Application: ${APP_NAME}"
                echo "Label: ${BUILD_LABEL}"
                echo "Stage: ${STAGE_NAME}"
            }
        }
    }
}
```

Pipeline-level values are available throughout the Pipeline; stage-level values apply within that stage. Never put secret values in a plain `environment` declaration.

## Lab 5: Parameters

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'TARGET_ENV', choices: ['dev', 'staging'], description: 'Test target')
        booleanParam(name: 'RUN_LINT', defaultValue: true, description: 'Run lint checks')
    }

    stages {
        stage('Build') {
            steps {
                echo "Target selected: ${params.TARGET_ENV}"
            }
        }
        stage('Lint') {
            when {
                expression { params.RUN_LINT }
            }
            steps {
                echo 'Lint checks passed'
            }
        }
    }
}
```

Run once with `RUN_LINT` true and once false to confirm the stage is skipped when disabled. For real deployment parameters, validate allowed values and enforce authorization separately.

## Lab 6: Archive an artifact

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'mkdir -p dist && printf "training artifact\n" > dist/app.txt'
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'dist/**', fingerprint: true
            }
        }
    }
}
```

A workspace file exists in the agent workspace and may be removed by cleanup. An archived artifact is attached to the build record according to Jenkins retention settings.

## Lab 7: Pipeline from SCM

Expected configuration:
- A committed `Jenkinsfile` at the configured script path.
- **Pipeline script from SCM** selected in the job.
- Git repository URL and correct branch configured.
- Credentials configured only if the repository requires them.
- A successful run that reflects the committed Pipeline content.

A Multibranch Pipeline can be useful when each repository branch should be discovered and built independently.

## Lab 8: Credential use

```groovy
pipeline {
    agent any
    stages {
        stage('Credential check') {
            steps {
                withCredentials([string(credentialsId: 'lab-dummy-token', variable: 'LAB_TOKEN')]) {
                    sh '''
                      set +x
                      test -n "$LAB_TOKEN"
                      echo "Credential is available"
                    '''
                }
            }
        }
    }
}
```

Create the credential with the exact ID `lab-dummy-token` in your lab. The code deliberately avoids printing the value. Credential masking is a defense-in-depth feature, not permission to expose secrets in logs.

## Lab 9: Post actions and timeout

```groovy
pipeline {
    agent any
    options {
        timestamps()
        timeout(time: 5, unit: 'MINUTES')
    }
    stages {
        stage('Validation') {
            steps {
                echo 'Validation running'
            }
        }
    }
    post {
        success {
            echo 'Pipeline succeeded'
        }
        failure {
            echo 'Pipeline failed'
        }
        always {
            echo 'Pipeline finished'
        }
    }
}
```

To test failure handling, use a temporary branch and a deliberate non-zero exit code. Remove it after observing the `failure` message.

## Lab 10: Broken Pipeline

The command `test -f missing-file.txt` exits with a non-zero status when the file does not exist. In Jenkins, that normally fails the shell step and stage.

One correction is to create the expected file first:

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'printf "test data\n" > test-file.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'test -s test-file.txt'
                echo 'File exists and is not empty'
            }
        }
    }
}
```

The correct fix should reflect the intended test. Replacing a meaningful test with `true` can conceal the defect rather than resolve it.

## Lab 11: Freestyle versus Pipeline

Suggested conclusion: Freestyle projects are useful for small UI-configured tasks and introductory practice. Pipelines are generally better for complex, repeatable CI/CD workflows because a `Jenkinsfile` can be reviewed, versioned, and shared through source control.

## Lab 12: Mini CI pipeline

```groovy
pipeline {
    agent any
    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }
    stages {
        stage('Build') {
            steps {
                sh 'mkdir -p dist && printf "artifact\n" > dist/app.txt'
            }
        }
        stage('Test') {
            steps {
                sh 'test -s dist/app.txt'
                echo 'Artifact check passed'
            }
        }
        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'dist/**', fingerprint: true
            }
        }
    }
    post {
        success {
            echo 'Mini CI pipeline succeeded'
        }
        failure {
            echo 'Mini CI pipeline failed; inspect console output'
        }
        always {
            echo 'Run finished'
        }
    }
}
```

If the Pipeline is loaded from SCM and the job performs the default checkout, add an explicit `Checkout` stage with `checkout scm` only when appropriate. A UI-entered script without SCM context may need an explicit checkout configuration.

## Common errors and first checks

| Error | First checks |
|---|---|
| `No such DSL method` | Check plugin/step availability and spelling |
| `sh` fails on Windows | Use `bat`/PowerShell or select a Linux agent |
| `checkout scm` fails | Confirm Pipeline SCM configuration and repository credentials |
| Artifact not found | Confirm path relative to workspace and archive step ran |
| Credential ID not found | Check credential scope and exact ID |
| Stage skipped | Review `when`, parameters, and upstream stage results |
| Pipeline syntax rejected | Check Declarative structure and use Pipeline Syntax help |

## Official references

- [Getting started with Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/getting-started/)
- [Pipeline syntax reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
