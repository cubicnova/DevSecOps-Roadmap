# Jenkinsfile Examples

These examples use **Declarative Pipeline** unless noted otherwise. Adapt commands and tool versions to your application and Jenkins agent.

## Example 1: Minimal pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }

        stage('Package') {
            steps {
                echo 'Packaging...'
            }
        }
    }
}
```

This illustrates structure only; the `echo` commands do not actually build or test an application.

## Example 2: Python validation pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate') {
            steps {
                sh '''
                    python3 --version
                    python3 -m compileall -q .
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh 'python3 -m unittest discover -s tests'
            }
        }
    }

    post {
        always {
            echo 'Validation pipeline completed.'
        }
        failure {
            echo 'Review the failed stage and console output.'
        }
    }
}
```

The agent must have Python installed and the repository must contain the expected tests. On Windows agents, use suitable `bat` steps instead of `sh`.

## Example 3: Parameters and conditional stage

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'TARGET_ENV', choices: ['dev', 'staging'], description: 'Target environment')
        booleanParam(name: 'RUN_EXTRA_CHECKS', defaultValue: true, description: 'Run additional checks')
    }

    stages {
        stage('Build') {
            steps {
                echo "Building for ${params.TARGET_ENV}"
            }
        }

        stage('Extra Checks') {
            when {
                expression { return params.RUN_EXTRA_CHECKS }
            }
            steps {
                echo 'Running additional checks'
            }
        }
    }
}
```

Parameters should not be used as a substitute for authorization. Restrict who can trigger sensitive jobs and validate values before using them in shell commands.

## Example 4: Environment variables

```groovy
pipeline {
    agent any

    environment {
        APP_NAME = 'sample-app'
        BUILD_MODE = 'test'
    }

    stages {
        stage('Show Configuration') {
            steps {
                echo "Application: ${env.APP_NAME}"
                echo "Mode: ${env.BUILD_MODE}"
            }
        }
    }
}
```

Only put non-sensitive configuration in plain environment declarations. Do not echo secrets.

## Example 5: Credential binding

Create a Jenkins credential with ID `demo-api-token` before using this example.

```groovy
pipeline {
    agent any

    stages {
        stage('Authenticated Task') {
            steps {
                withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
                    sh '''
                        set +x
                        ./scripts/call-demo-service.sh
                    '''
                }
            }
        }
    }
}
```

The script should read the `API_TOKEN` environment variable itself. Avoid Groovy interpolation such as `sh "curl -H 'Authorization: Bearer ${API_TOKEN}' ..."` because the secret may be exposed in process arguments or logs. Masking is helpful but is not a guarantee that every secret exposure is prevented.

## Example 6: Test report and cleanup

```groovy
pipeline {
    agent any

    stages {
        stage('Test') {
            steps {
                sh './run-tests.sh'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/**/*.xml'
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
```

This requires the JUnit and Workspace Cleanup plugins for the relevant steps. Use `allowEmptyResults: true` only when missing reports are acceptable; otherwise, require reports so broken test execution is not hidden.

## Example 7: Conditional deployment stage

```groovy
pipeline {
    agent any

    stages {
        stage('Build and Test') {
            steps {
                sh './build.sh'
                sh './test.sh'
            }
        }

        stage('Deploy to Staging') {
            when {
                branch 'main'
            }
            steps {
                echo 'Insert approved staging deployment command here.'
            }
        }
    }
}
```

The `branch` condition requires a multibranch Pipeline context. Deployment commands and credentials are intentionally omitted.

## Example 8: Scripted Pipeline equivalent

```groovy
node {
    stage('Build') {
        echo 'Building...'
    }
    stage('Test') {
        echo 'Testing...'
    }
}
```

Scripted Pipeline uses Groovy control flow directly. Declarative syntax is generally easier to read and validate for conventional pipelines.

## Example 9: Timeout and concurrency control

```groovy
pipeline {
    agent any

    options {
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
    }

    stages {
        stage('Check') {
            steps {
                echo 'Run bounded validation here.'
            }
        }
    }
}
```

These options can help prevent stuck builds and conflicting runs. Check plugin and Jenkins version compatibility in your environment.

## Review checklist

- [ ] Jenkinsfile is stored in source control.
- [ ] The selected agent has the required tools.
- [ ] Commands fail the build when required checks fail.
- [ ] Secrets are retrieved from Jenkins Credentials.
- [ ] Parameters are validated and cannot bypass authorization.
- [ ] Plugins used by the file are installed and maintained.
- [ ] Deployment stages have appropriate controls.
