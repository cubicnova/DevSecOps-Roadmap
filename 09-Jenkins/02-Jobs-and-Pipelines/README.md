# 02 — Jenkins Jobs and Pipelines

This module introduces Jenkins jobs, Freestyle projects, Pipeline jobs, Jenkinsfiles, and common CI/CD pipeline patterns.

## Learning objectives

By the end of this module, you should be able to:

- Explain the difference between a Jenkins job and a Pipeline.
- Create and configure a basic Freestyle job.
- Create a Pipeline job and run a Declarative `Jenkinsfile`.
- Use stages, steps, environment variables, parameters, and post actions.
- Connect a Pipeline to source control.
- Understand build results, console output, and common failure modes.
- Apply basic credential-handling and pipeline security practices.

## 1. Jobs and Pipelines

A **job** is a configured unit of work in Jenkins. A job can build software, run tests, perform scheduled tasks, or coordinate other jobs.

Common job types include:

- **Freestyle project:** Configured mainly through the Jenkins UI. Useful for learning and simple tasks.
- **Pipeline:** Defines a sequence of automation steps, often in a `Jenkinsfile`.
- **Multibranch Pipeline:** Discovers branches in a source repository that contain a `Jenkinsfile`.
- **Organization folder / multibranch discovery:** Can organize and discover repositories when the appropriate plugins are configured.

A **Pipeline** is an automated workflow that can include checkout, build, test, package, artifact publishing, and deployment stages.

## 2. Freestyle job versus Pipeline

| Feature | Freestyle project | Pipeline |
|---|---|---|
| Main configuration | Jenkins UI | `Jenkinsfile` or UI |
| Version control | UI configuration needs separate management | Pipeline code can be committed and reviewed |
| Multi-stage workflow | Possible, but less expressive | Native stage structure |
| Branch-aware workflow | Requires extra setup/plugins | Multibranch Pipeline supports branch discovery |
| Reproducibility | Depends on recorded UI configuration | Pipeline definition can be versioned |
| Best fit | Simple tasks and introductory labs | Repeatable CI/CD workflows |

For team workflows, prefer storing the Pipeline definition in source control so changes can be reviewed and audited.

## 3. Create a Freestyle job

1. Sign in to Jenkins.
2. Select **New Item**.
3. Enter a name such as `hello-freestyle`.
4. Select **Freestyle project**, then **OK**.
5. Under **Build Steps**, add **Execute shell** on a Linux agent, or the corresponding Windows batch step.
6. Enter a harmless command:

```bash
echo "Hello from Jenkins"
date
```

7. Save and select **Build Now**.
8. Open the build number and choose **Console Output**.

If the job runs on a Windows agent, use Windows commands instead of `sh`/Execute shell.

## 4. Create a Pipeline job in the UI

1. Select **New Item**.
2. Name it `hello-pipeline`.
3. Select **Pipeline**, then **OK**.
4. In the Pipeline section, select **Pipeline script**.
5. Paste this Declarative Pipeline:

```groovy
pipeline {
    agent any

    stages {
        stage('Hello') {
            steps {
                echo 'Hello from Jenkins Pipeline'
            }
        }
        stage('Environment') {
            steps {
                sh 'echo "Running on a Linux agent"'
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution finished'
        }
    }
}
```

6. Save and select **Build Now**.
7. Open the build to review stage results and console output.

The `sh` step requires a Unix-like agent. On Windows, use `bat 'echo Running on a Windows agent'`.

## 5. Pipeline as code: Jenkinsfile

Create a file named `Jenkinsfile` at the root of your source repository:

```groovy
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 10, unit: 'MINUTES')
    }

    environment {
        APP_NAME = 'demo-app'
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Source checkout is handled by the job configuration or default checkout"
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "Building ${APP_NAME}"
                sh 'mkdir -p build && echo "demo artifact" > build/app.txt'
            }
        }

        stage('Test') {
            steps {
                sh 'test -s build/app.txt'
                echo 'Basic test passed'
            }
        }

        stage('Package') {
            steps {
                archiveArtifacts artifacts: 'build/**', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Build completed successfully'
        }
        failure {
            echo 'Build failed; inspect the first failing stage'
        }
        always {
            echo 'Pipeline finished'
        }
    }
}
```

This sample is for a Linux agent and uses `checkout scm`, which is appropriate when the Pipeline is configured to load from source control. If you paste the script directly into the UI without SCM context, configure source checkout explicitly or remove the checkout stage for the first test.

## 6. Important Pipeline concepts

- `pipeline`: Root of a Declarative Pipeline.
- `agent`: Where the Pipeline or stage runs; `agent any` uses any eligible agent.
- `stages`: Ordered collection of stages.
- `stage`: Named part of the workflow.
- `steps`: Commands and Jenkins steps performed in a stage.
- `environment`: Environment variables for a Pipeline or stage.
- `parameters`: User inputs provided when starting a build.
- `when`: Conditional execution of a stage.
- `post`: Actions run after the Pipeline or stage finishes.
- `options`: Pipeline settings such as timestamps and timeouts.

## 7. Parameters and conditional stages

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
                expression { params.RUN_EXTRA_CHECKS }
            }
            steps {
                echo 'Additional checks enabled'
            }
        }
    }
}
```

Use parameters for controlled input, not as a replacement for authorization. Production deployment should have explicit approvals and permission boundaries.

## 8. Build results and console output

Typical results:

- **SUCCESS:** All required steps completed successfully.
- **UNSTABLE:** Build completed but one or more checks, often tests, reported a problem.
- **FAILURE:** A step or Pipeline failed.
- **ABORTED:** Execution was stopped before normal completion.
- **NOT BUILT:** A build did not run in the normal way.

When a build fails, inspect the earliest relevant error in **Console Output** and the stage view. Do not rely only on the final error message.

## 9. Security basics

- Do not commit passwords, API keys, private keys, or tokens into a `Jenkinsfile`.
- Store secrets in Jenkins Credentials and scope them to the smallest practical set of jobs.
- Avoid printing secrets or dumping the full environment to logs.
- Use least-privilege agents and separate trusted deployment jobs from untrusted pull-request builds.
- Review plugins and Pipeline changes as code.
- Use input approvals and restricted permissions for sensitive deployments.

## Module files

- [`examples.md`](examples.md) — Freestyle, Declarative Pipeline, parameters, artifacts, and credential examples.
- [`practical.md`](practical.md) — Guided tasks for building and troubleshooting jobs and pipelines.
- [`solutions.md`](solutions.md) — Sample Jenkinsfiles and suggested lab solutions.

## Official references

- [Getting started with Jenkins Pipeline](https://www.jenkins.io/doc/book/pipeline/getting-started/)
- [Pipeline overview](https://www.jenkins.io/doc/book/pipeline/)
- [Pipeline syntax reference](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
