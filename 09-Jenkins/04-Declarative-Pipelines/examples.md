# Declarative Pipeline Examples

Save these examples as a `Jenkinsfile` in a test repository. Replace demonstration commands with commands appropriate for your application and agent.

## Example 1: Minimal Declarative Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building application'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing application'
            }
        }
    }
}
```

## Example 2: Options and post conditions

```groovy
pipeline {
    agent any

    options {
        timeout(time: 20, unit: 'MINUTES')
        disableConcurrentBuilds()
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {
        stage('Validate') {
            steps {
                sh 'echo "Run validation commands here"'
            }
        }
    }

    post {
        always {
            echo 'Always run this reporting or cleanup step.'
        }
        success {
            echo 'Build completed successfully.'
        }
        failure {
            echo 'Build failed. Review the console output.'
        }
        cleanup {
            echo 'Cleanup actions go here.'
        }
    }
}
```

`timestamps()` requires the relevant plugin. Confirm plugin availability and version compatibility in your Jenkins instance.

## Example 3: Environment variables and parameters

```groovy
pipeline {
    agent any

    parameters {
        choice(name: 'TARGET_ENV', choices: ['dev', 'staging'], description: 'Target environment')
        booleanParam(name: 'RUN_EXTRA_CHECKS', defaultValue: true, description: 'Run extra checks')
    }

    environment {
        APP_NAME = 'demo-app'
    }

    stages {
        stage('Show Configuration') {
            steps {
                echo "Application: ${env.APP_NAME}"
                echo "Target: ${params.TARGET_ENV}"
            }
        }

        stage('Extra Checks') {
            when {
                expression { return params.RUN_EXTRA_CHECKS }
            }
            steps {
                echo 'Running extra checks'
            }
        }
    }
}
```

Parameters are user-controlled inputs, not an authorization mechanism. Restrict access to sensitive jobs separately.

## Example 4: Stage-specific agent

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

The Jenkins controller must have online agents with the configured labels. Commands must match the operating system of the assigned agent.

## Example 5: Conditional deployment

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
                echo 'Insert staging deployment command here.'
            }
        }
    }
}
```

The `branch` condition is intended for a multibranch Pipeline. It is not a replacement for Jenkins permissions or deployment approvals.

## Example 6: Parallel tests

```groovy
pipeline {
    agent any

    stages {
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
    }
}
```

Parallel branches should be independent or use isolated resources. If both branches write to the same files, databases, or test environment, collisions may occur.

## Example 7: Matrix build

```groovy
pipeline {
    agent any

    stages {
        stage('Test across runtimes') {
            matrix {
                axes {
                    axis {
                        name 'PYTHON_VERSION'
                        values '3.11', '3.12'
                    }
                }
                stages {
                    stage('Test') {
                        steps {
                            echo "Testing Python ${PYTHON_VERSION}"
                            sh 'python3 --version'
                            sh './run-tests.sh'
                        }
                    }
                }
            }
        }
    }
}
```

This example demonstrates matrix structure. The shown `python3` command uses whatever runtime is installed on the selected agent; configure the agent or tool setup so each matrix value actually selects the intended version before using this pattern for real testing.

## Example 8: Manual approval step

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh './build.sh'
            }
        }

        stage('Approve Staging Deployment') {
            input {
                message 'Proceed with staging deployment?'
                ok 'Deploy'
                submitter 'release-managers'
            }
            steps {
                echo 'Approval received; add the deployment command here.'
            }
        }
    }
}
```

Replace `release-managers` with valid Jenkins user or group names for your environment. Configure job permissions as well; an input prompt by itself does not secure all deployment paths.

## Example 9: Credential binding

Create a Jenkins secret-text credential with ID `demo-api-token`.

```groovy
pipeline {
    agent any

    stages {
        stage('Call Internal Service') {
            steps {
                withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
                    sh '''
                        set +x
                        ./scripts/call-service.sh
                    '''
                }
            }
        }
    }
}
```

The script should read `API_TOKEN` from its environment. Do not echo it, write it to an artifact, or interpolate it into a Groovy double-quoted command string. Keep the agent trusted and isolated.

## Example 10: JUnit reporting and cleanup

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
            junit testResults: 'reports/**/*.xml'
            echo 'Test reporting step completed.'
        }
    }
}
```

The test command must create JUnit-compatible XML files and the JUnit plugin must be installed. Do not silently accept missing reports if test reporting is mandatory.

## Review checklist

- [ ] Correct `pipeline`, `stages`, `stage`, and `steps` nesting
- [ ] Appropriate agent selected for each stage
- [ ] Required commands fail on errors
- [ ] Timeouts and post actions configured where useful
- [ ] Branch conditions are not used as the only authorization control
- [ ] Credentials are stored and bound securely
- [ ] Plugin dependencies are documented
