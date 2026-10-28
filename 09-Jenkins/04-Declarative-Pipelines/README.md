# Declarative Pipelines in Jenkins

Jenkins Declarative Pipeline is a structured way to define continuous integration and delivery workflows as code. A pipeline is written in a `Jenkinsfile`, stored with the application, and reviewed through normal source-control practices.

## Learning objectives

By the end of this module, you should be able to:

- Explain the structure and purpose of a Declarative Pipeline.
- Use `agent`, `stages`, `stage`, and `steps`.
- Configure `environment`, `parameters`, `options`, `tools`, `triggers`, and `post`.
- Control execution with `when`, `input`, `parallel`, and `matrix`.
- Use credentials safely and avoid exposing secrets in logs.
- Troubleshoot common Declarative Pipeline syntax and runtime errors.

## Basic structure

```groovy
pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 20, unit: 'MINUTES')
    }

    stages {
        stage('Build') {
            steps {
                echo 'Build application'
            }
        }

        stage('Test') {
            steps {
                echo 'Run tests'
            }
        }
    }

    post {
        always {
            echo 'Pipeline completed'
        }
        success {
            echo 'Pipeline succeeded'
        }
        failure {
            echo 'Pipeline failed'
        }
    }
}
```

## Main sections and directives

| Directive | Purpose |
|---|---|
| `agent` | Selects the node or environment used to execute the pipeline or stage |
| `stages` | Holds the pipeline's stages |
| `stage` | Groups related work under a readable name |
| `steps` | Runs Pipeline steps and commands |
| `environment` | Defines environment variables |
| `parameters` | Defines inputs supplied when the job is triggered |
| `options` | Configures timeouts, concurrency, build retention, and other options |
| `tools` | Selects configured tools such as JDK or Maven |
| `triggers` | Defines supported scheduled or upstream triggers |
| `when` | Controls whether a stage runs |
| `input` | Pauses for user input or approval |
| `post` | Defines actions based on the final result |
| `parallel` | Runs independent branches concurrently |
| `matrix` | Runs stages across a set of axis combinations |

## Declarative Pipeline versus Scripted Pipeline

Declarative Pipeline uses a defined structure and is often the easiest choice for standard CI/CD workflows. Scripted Pipeline uses more direct Groovy control flow and may be useful for specialized logic. Prefer Declarative Pipeline when it can express the workflow clearly; keep complicated logic in scripts or shared libraries rather than building a large `script` block.

## Recommended design practices

1. Keep stages small and focused.
2. Use meaningful stage names so failures are easy to diagnose.
3. Use `agent none` at the top level when you want to allocate agents only for individual stages.
4. Add realistic timeouts to prevent stuck builds.
5. Use `post { always { ... } }` for cleanup and report publication that must run after success or failure.
6. Use `when` to express execution conditions, but do not treat a branch condition as authorization.
7. Set job permissions and credential scope separately from pipeline logic.
8. Store secrets in Jenkins Credentials; never commit them to source control.
9. Use least-privileged, isolated agents, especially for untrusted changes.
10. Review plugin requirements for steps such as `junit`, `cleanWs`, and Docker-related directives.

## Suggested practice order

1. Run the basic pipeline.
2. Add parameters and environment variables.
3. Add `when` and `post` conditions.
4. Create a parallel test stage.
5. Try a matrix build.
6. Add a protected staging approval.
7. Review the workflow for secret exposure, agent trust, and plugin dependencies.

## Requirements

- Jenkins with Pipeline and Declarative Pipeline support.
- A configured agent with the tools required by your application.
- A source-control repository containing a `Jenkinsfile`.
- Optional plugins for any plugin-provided steps used in your pipeline.

## Official references

- [Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
- [Getting started with Pipeline](https://www.jenkins.io/doc/book/pipeline/getting-started/)
