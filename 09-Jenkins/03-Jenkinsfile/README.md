# Jenkinsfile

A **Jenkinsfile** is a text file that defines a Jenkins Pipeline as code. Keeping it in source control allows the pipeline to be reviewed, versioned, tested, and maintained alongside the application.

Jenkins supports two primary pipeline styles:

- **Declarative Pipeline** — structured syntax with a `pipeline {}` block; recommended for most standard workflows.
- **Scripted Pipeline** — Groovy-based syntax that offers more flexibility for complex logic.

## Learning objectives

After completing this module, you should be able to:

- Explain the purpose of a Jenkinsfile and Pipeline-as-Code.
- Recognize the main Declarative Pipeline sections and directives.
- Write a basic build, test, and package pipeline.
- Use parameters, environment variables, post actions, and conditional stages.
- Handle credentials without hardcoding secrets.
- Validate and troubleshoot a Jenkinsfile.

## Basic structure

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
                echo 'Running tests'
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
    }
}
```

### Key elements

| Element | Purpose |
|---|---|
| `pipeline` | Root block for Declarative Pipeline |
| `agent` | Selects where the pipeline or stage runs |
| `stages` | Groups the pipeline's stages |
| `stage` | Names a distinct phase |
| `steps` | Commands and Pipeline steps for a stage |
| `environment` | Defines environment variables |
| `parameters` | Declares user-supplied build parameters |
| `when` | Conditionally runs a stage |
| `post` | Runs actions after a pipeline or stage result |

## Suggested learning sequence

1. Start with the minimal pipeline in `examples.md`.
2. Add build and test commands that match your project.
3. Add a post-build action and test the failure path.
4. Add parameters and a conditional stage.
5. Review credential and agent security before adding deployment.

## Best practices

- Keep the Jenkinsfile in source control at the project root unless your repository convention says otherwise.
- Prefer Declarative Pipeline for common workflows; use Scripted Pipeline only when its flexibility is needed.
- Use small, clearly named stages.
- Fail the build when required tests fail; do not mask non-zero exit codes.
- Never hardcode passwords, API tokens, or private keys in a Jenkinsfile.
- Use Jenkins Credentials and the `withCredentials` step for secrets; avoid Groovy string interpolation of secret values.
- Do not execute untrusted pull-request code on privileged agents with production credentials.
- Keep agents isolated, use least privilege, and clean workspaces where appropriate.
- Use `post { always { ... } }` for cleanup or report collection that must run regardless of success.
- Review plugins and shared libraries as code dependencies.

## Running a Jenkinsfile

1. Ensure Jenkins has the Pipeline plugins required by your workflow.
2. Commit a `Jenkinsfile` to the source repository.
3. Create a **Pipeline** job in Jenkins.
4. Configure **Pipeline script from SCM**, select the SCM and branch, and set the script path to `Jenkinsfile`.
5. Save and run the job.
6. Inspect stage results and console output. Never print secrets while debugging.

## Requirements

- A Jenkins instance with Pipeline support.
- An agent with the tools used by your build.
- A Git repository containing the Jenkinsfile.
- Optional plugins for features such as JUnit test reports or specific build tools.

## Official documentation

- [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Getting started with Pipeline](https://www.jenkins.io/doc/book/pipeline/getting-started/)
