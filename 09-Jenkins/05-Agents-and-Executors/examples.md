# Jenkins Agents and Executors — Examples

## Example 1: Print details about the assigned agent

```groovy
pipeline {
    agent any
    stages {
        stage('Agent details') {
            steps {
                sh 'hostname'
                sh 'whoami'
                sh 'pwd'
            }
        }
    }
}
```

This is for a Unix-like agent. Use `bat` for Windows commands.

## Example 2: Select a Linux agent

```groovy
pipeline {
    agent { label 'linux' }
    stages {
        stage('Linux build') {
            steps {
                sh 'uname -s'
            }
        }
    }
}
```

At least one online agent must have the `linux` label and an available executor.

## Example 3: Require multiple labels

```groovy
pipeline {
    agent { label 'linux && python' }
    stages {
        stage('Check Python') {
            steps {
                sh 'python3 --version'
            }
        }
    }
}
```

The label expression requires an agent carrying both labels. Labels should reflect actual installed tools and capabilities.

## Example 4: Run separate stages on separate operating systems

```groovy
pipeline {
    agent none
    stages {
        stage('Linux') {
            agent { label 'linux' }
            steps {
                sh 'echo "Linux stage"'
            }
        }
        stage('Windows') {
            agent { label 'windows' }
            steps {
                bat 'echo Windows stage'
            }
        }
    }
}
```

This requires both agents. If either label has no available agent, the relevant stage may remain queued.

## Example 5: Check executor capacity from the UI

1. Open **Manage Jenkins → Nodes**.
2. Select a node.
3. Review its executor count and current build activity.
4. If builds are queued, check whether the node is online, whether its labels match, and whether all executors are occupied.
5. Check CPU, RAM, disk, and I/O before increasing executor count.

Executor capacity is not the same as CPU-core count; workload resource demand matters.

## Example 6: Limit a stage to a deployment-capable agent

```groovy
pipeline {
    agent none
    stages {
        stage('Build') {
            agent { label 'linux' }
            steps {
                sh 'echo "Build artifact created"'
            }
        }
        stage('Deploy to test') {
            agent { label 'test-deploy' }
            steps {
                echo 'Run the approved deployment command here'
            }
        }
    }
}
```

Only grant the `test-deploy` label to jobs and users that are authorized for the target environment. A label alone does not enforce authorization.

## Example 7: Add a timeout for agent allocation and execution

```groovy
pipeline {
    agent { label 'linux' }
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
    stages {
        stage('Build') {
            steps {
                sh 'echo "Running with a timeout"'
            }
        }
    }
}
```

If a suitable agent cannot be allocated or the Pipeline exceeds the timeout, the run can be interrupted. Inspect the log to determine which condition occurred.

## Example 8: Use a Windows agent

```groovy
pipeline {
    agent { label 'windows' }
    stages {
        stage('Windows environment') {
            steps {
                bat 'hostname'
                bat 'ver'
            }
        }
    }
}
```

The label must map to an online Windows agent, and the service account must have the expected PATH and permissions.

## Example 9: Agent tool discovery

```groovy
pipeline {
    agent { label 'linux' }
    stages {
        stage('Tool versions') {
            steps {
                sh 'command -v git'
                sh 'git --version'
                sh 'command -v python3'
                sh 'python3 --version'
            }
        }
    }
}
```

This helps confirm which tools are available to the Jenkins agent process. Interactive shell PATH settings may differ from the environment of a service account.

## Example 10: Diagnose a queued job

A Pipeline uses:

```groovy
agent { label 'linux && docker' }
```

But no agent is assigned. Check:
- Is there an online node with both labels?
- Does the node have an available executor?
- Is the node temporarily offline or marked temporarily offline by an administrator?
- Are the labels spelled exactly as configured?
- Are cloud/ephemeral agents configured to provision the required node?

Do not remove label restrictions until you understand why the job requires those capabilities.

## Example 11: Basic capacity illustration

Suppose two agents each have two executors. They offer up to four concurrent executor-consuming tasks in total, assuming both are online, the labels match, and sufficient resources are available. Four executors do not guarantee four builds will finish faster; builds can compete for CPU, memory, disk, or network.

## Example 12: Keep the controller from running builds

In the Jenkins UI, open the built-in node configuration and set its number of executors to `0`, if consistent with your setup. Then verify that jobs have eligible agents and correct labels. If no agent can satisfy a job, it may remain queued rather than running on the controller.
