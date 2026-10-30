# Jenkins Jobs and Pipelines — Examples

## Example 1: Simple Freestyle job

In Jenkins, create a **Freestyle project** and add an **Execute shell** build step:

```bash
echo "Hello from Jenkins"
echo "Build number: ${BUILD_NUMBER}"
date
```

Run the job and inspect **Console Output**. `BUILD_NUMBER` is a Jenkins-provided environment variable.

## Example 2: Minimal Declarative Pipeline

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
    }
}
```

This demonstrates the `pipeline`, `agent`, `stages`, `stage`, and `steps` structure.

## Example 3: Run shell commands

```groovy
pipeline {
    agent any

    stages {
        stage('System Info') {
            steps {
                sh 'whoami'
                sh 'pwd'
                sh 'uname -a'
            }
        }
    }
}
```

Use `sh` on Unix-like agents. For Windows agents, use `bat` or the appropriate PowerShell step.

## Example 4: Environment variables

```groovy
pipeline {
    agent any

    environment {
        APP_NAME = 'demo-app'
        BUILD_LABEL = 'learning'
    }

    stages {
        stage('Show configuration') {
            steps {
                echo "Application: ${APP_NAME}"
                echo "Label: ${BUILD_LABEL}"
            }
        }
    }
}
```

Do not put secrets in plain-text environment declarations.

## Example 5: Parameters

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging'], description: 'Choose a test environment')
        string(name: 'RELEASE_NOTE', defaultValue: 'Training build', description: 'Short note')
    }

    stages {
        stage('Show input') {
            steps {
                echo "Target: ${params.DEPLOY_ENV}"
                echo "Note: ${params.RELEASE_NOTE}"
            }
        }
    }
}
```

Treat parameter values as untrusted input. Validate them before using them in shell commands or deployment operations.

## Example 6: Conditional stage

```groovy
pipeline {
    agent any

    parameters {
        booleanParam(name: 'RUN_LINT', defaultValue: true, description: 'Run lint stage')
    }

    stages {
        stage('Build') {
            steps {
                echo 'Build completed'
            }
        }
        stage('Lint') {
            when {
                expression { params.RUN_LINT }
            }
            steps {
                echo 'Lint checks would run here'
            }
        }
    }
}
```

The `Lint` stage is skipped when `RUN_LINT` is false.

## Example 7: Archive a build artifact

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'mkdir -p dist && echo "training artifact" > dist/app.txt'
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

After a successful build, inspect the build page for archived artifacts. This example creates a harmless text file instead of compiling a real application.

## Example 8: Post actions

```groovy
pipeline {
    agent any

    stages {
        stage('Check') {
            steps {
                echo 'Running checks'
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
            echo 'Final cleanup/reporting can run here'
        }
    }
}
```

Use `post` conditions to report outcomes or perform cleanup. Avoid printing secret values in notification messages.

## Example 9: Timeout and timestamps

```groovy
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 5, unit: 'MINUTES')
    }

    stages {
        stage('Quick check') {
            steps {
                echo 'This pipeline has a five-minute timeout'
            }
        }
    }
}
```

A timeout helps prevent a job from running indefinitely.

## Example 10: Load a Pipeline from source control

1. Commit a `Jenkinsfile` to the repository root.
2. In Jenkins, choose **New Item** → **Pipeline**.
3. Under **Pipeline**, choose **Pipeline script from SCM**.
4. Select Git and enter the repository URL.
5. Configure credentials only if the repository is private.
6. Set the branch and script path (`Jenkinsfile`).
7. Save and run the job.

For repositories with many branches, consider a Multibranch Pipeline and the appropriate branch source plugin.

## Example 11: Use Jenkins credentials without exposing values

Create a credential in **Manage Jenkins → Credentials** with ID `demo-api-token` in a lab instance. Then use it in a Pipeline step:

```groovy
pipeline {
    agent any

    stages {
        stage('Authenticated check') {
            steps {
                withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
                    sh '''
                      set +x
                      test -n "$API_TOKEN"
                      echo "Credential is available"
                    '''
                }
            }
        }
    }
}
```

This example checks presence only and does not send the token to a real service. Avoid echoing the secret or enabling shell tracing around secret use.

## Example 12: Basic failure handling

```groovy
pipeline {
    agent any

    stages {
        stage('Validate') {
            steps {
                sh 'test -f README.md'
            }
        }
    }

    post {
        failure {
            echo 'Validation failed. Inspect the console log.'
        }
    }
}
```

A failing shell command returns a non-zero status and normally causes the stage to fail.

## Example 13: Windows agent example

```groovy
pipeline {
    agent any

    stages {
        stage('Windows check') {
            steps {
                bat 'echo Running on Windows'
                bat 'ver'
            }
        }
    }
}
```

The agent assigned to this Pipeline must be a Windows node. Use labels and agent configuration to ensure the correct operating system is selected.
