# Jenkins Agents and Executors — Suggested Solutions

## Lab 1: Node model

- **Controller:** Coordinates Jenkins and schedules work.
- **Node:** A machine or execution environment known to Jenkins.
- **Agent:** The process that connects to Jenkins and executes assigned work.
- **Executor:** A task execution slot on a node.

The built-in node is part of the controller. For security and stability, avoid running normal builds there where possible.

## Lab 2: Configure a permanent agent

A valid configuration typically includes:
- Unique node name.
- Correct remote root/work directory owned by the agent service account.
- Supported Java runtime.
- Labels that reflect installed tools and actual OS.
- A supported launch method with network connectivity and carefully scoped credentials.
- Online node status and useful node logs.

Do not copy credentials into the report. If SSH is used, verify host identity and use a dedicated account with least privilege.

## Lab 3: Pipeline on a labelled agent

```groovy
pipeline {
    agent { label 'linux' }
    stages {
        stage('Agent details') {
            steps {
                sh 'hostname'
                sh 'whoami'
                sh 'uname -a'
            }
        }
    }
}
```

When the label matches an online agent with an available executor, Jenkins can schedule the Pipeline there. A nonexistent or unavailable label generally leaves the job waiting for a matching executor.

## Lab 4: Multiple labels

```groovy
pipeline {
    agent { label 'linux && python' }
    stages {
        stage('Check') {
            steps {
                sh 'python3 --version'
            }
        }
    }
}
```

The `&&` operator requires both labels on the selected node. A label expression does not install tools, so confirm the runtime is actually present.

## Lab 5: Stage-level agents

```groovy
pipeline {
    agent none
    stages {
        stage('Linux') {
            agent { label 'linux' }
            steps {
                sh 'uname -s'
            }
        }
        stage('Windows') {
            agent { label 'windows' }
            steps {
                bat 'ver'
            }
        }
    }
}
```

This works only if both agent types are configured and online. Without a Windows agent, the Windows stage cannot be scheduled; explain the prerequisite rather than silently changing the stage to run elsewhere.

## Lab 6: Executor experiment

If an agent has two executors, it can generally run two eligible executor-consuming tasks simultaneously. Additional tasks wait until a slot becomes available. Increasing executor count may raise throughput for lightweight tasks but may slow CPU- or memory-heavy builds due to contention.

A useful table records executor count, simultaneous builds, queue length, build duration, CPU/memory use, and observations.

## Lab 7: Offline agent

Troubleshoot in this order:
1. Inspect node status and log.
2. Check whether the host is reachable and powered on.
3. Check SSH or inbound connection configuration.
4. Verify credentials and permissions without exposing secrets.
5. Confirm supported Java/runtime and agent process status.
6. Check host disk, memory, and other resource constraints.
7. Reconnect and run a small validation Pipeline.

## Lab 8: Missing tool

`python3: not found` means the command is unavailable in the execution environment's PATH, or the tool is not installed. Confirm the actual node and service account first. Install Python on the intended agent or update the label so only agents with Python are eligible. Re-run the same Pipeline to verify the fix.

## Lab 9: Security and isolation

Good recommendations include:
- Set the controller's built-in executor count to zero where practical.
- Use dedicated service accounts and least privilege.
- Keep untrusted pull-request builds away from deployment credentials and sensitive agents.
- Avoid sharing writable workspaces between trust boundaries.
- Restrict Docker daemon access; it can often grant powerful host control.
- Use ephemeral agents for disposable/untrusted work when feasible.
- Limit deployment labels and credentials to authorized jobs/users.

Labels help schedule work, but they are not an authorization system by themselves.

## Lab 10: Capacity plan

Do not blindly increase executor count. Gather utilization data first. Potential improvements include adding a second agent, reducing concurrent builds on a saturated host, using specialized agents for heavy workloads, caching dependencies safely, or provisioning ephemeral agents. Track queue time, build duration, CPU, memory, disk I/O, and failure rates after the change.

## Lab 11: Restrict deployment work

Example:

```groovy
pipeline {
    agent none
    stages {
        stage('Build') {
            agent { label 'linux' }
            steps {
                sh 'echo "Build stage"'
            }
        }
        stage('Deploy to test') {
            agent { label 'test-deploy' }
            steps {
                echo 'Approved test deployment would run here'
            }
        }
    }
}
```

For a real deployment, enforce Jenkins permissions, limit credential scope, use environment approvals where appropriate, and ensure untrusted branches cannot access the deployment stage. The label is a scheduling selector, not the complete security control.

## Lab 12: Acceptance test

Mark an item passed only after confirming it with evidence: node status, runtime/tool output, Pipeline logs, executor activity, and permission review. Record any missing prerequisite and avoid claiming a security property based only on a label or a successful build.

## Common troubleshooting reference

| Symptom | First checks |
|---|---|
| Agent offline | Node log, host/network, connection method, credentials, Java |
| Job queued | Label expression, online state, free executors |
| Tool missing | Agent OS, PATH, installation under service account |
| Permission denied | Workspace ownership, remote root, service account permissions |
| Builds slower with more executors | CPU, RAM, disk I/O, network contention |
| Build executes on controller | Built-in executor count and Pipeline agent configuration |
| Frequent disconnects | Network stability, host resources, agent process logs |

## Official references

- [Using Jenkins agents](https://www.jenkins.io/doc/book/using/using-agents/)
- [Managing nodes](https://www.jenkins.io/doc/book/managing/nodes/)
- [Controller isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- [Securing builds](https://www.jenkins.io/doc/book/security/securing-builds/)
