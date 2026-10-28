# 05 — Jenkins Agents and Executors

This module explains how Jenkins distributes build work across nodes, how executors control concurrency, and how Pipeline labels select suitable agents.

## Learning objectives

By the end of this module, you should be able to:

- Distinguish the Jenkins controller, node, agent, and executor.
- Explain why builds should generally run on agents rather than the controller.
- Create and configure an agent node in Jenkins.
- Use labels to select agents by OS, tools, or workload.
- Configure Pipeline stages to run on selected agents.
- Estimate executor capacity and diagnose offline or busy agents.
- Apply least privilege and isolation to build agents.

## 1. Core concepts

- **Controller:** The Jenkins service that hosts the UI, stores configuration, schedules work, and coordinates agents.
- **Node:** A machine or execution environment managed by Jenkins. The built-in node is part of the controller.
- **Agent:** A process on a node that connects to Jenkins and performs assigned work.
- **Executor:** A slot on a node that allows one task to run at a time. The executor count controls concurrent task capacity.

A node with two executors can generally run up to two executor-consuming tasks concurrently, subject to labels, resources, and scheduling rules. More executors do not automatically make builds faster; they may increase CPU, memory, disk, and network contention.

## 2. Why use agents?

Agents can:
- Offload builds from the controller.
- Provide different operating systems or CPU architectures.
- Separate toolchains and build dependencies.
- Scale capacity horizontally.
- Isolate workloads, provided the host, permissions, and agent configuration are designed appropriately.

For security and stability, Jenkins recommends avoiding builds on the built-in controller node. A common starting point is setting the controller's executor count to `0` and running jobs on dedicated agents.

## 3. Labels

Labels describe an agent's capabilities. Examples:

- `linux`
- `windows`
- `docker`
- `python`
- `high-memory`
- `arm64`

An agent can have multiple labels. A Pipeline can use one label or a label expression to require capabilities.

```groovy
pipeline {
    agent {
        label 'linux && python'
    }

    stages {
        stage('Verify agent') {
            steps {
                sh 'uname -a'
                sh 'python3 --version'
            }
        }
    }
}
```

The agent must actually have both labels and the required tools installed. Labels are scheduling metadata, not a security boundary by themselves.

## 4. Create an agent node in the UI

Exact labels and menu wording can vary slightly by Jenkins version and installed plugins.

1. Sign in with an account allowed to manage nodes.
2. Open **Manage Jenkins** and locate **Nodes** (sometimes shown as **Manage Nodes and Clouds**).
3. Select **New Node**.
4. Enter a unique node name, such as `linux-agent-01`.
5. Select **Permanent Agent** and continue.
6. Configure a remote root directory, such as `/home/jenkins/agent`.
7. Add labels such as `linux python`.
8. Set the number of executors based on the machine's resources and expected workload.
9. Choose an appropriate launch method, commonly SSH for a reachable Unix agent, or an inbound agent for environments where the agent initiates the connection.
10. Save and review the connection instructions and node log.

Do not give the agent account unnecessary sudo or administrator privileges. Install required build tools on the agent and test the connection using the same account Jenkins will use.

## 5. Agent connection options

Common approaches include:

- **SSH-launched agent:** Jenkins connects to a Unix-like agent over SSH and starts the agent process. Requires network reachability and correctly configured SSH credentials.
- **Inbound agent:** The agent initiates a connection to the controller. Useful when network topology prevents the controller from opening a connection to the agent. Follow the current Jenkins UI instructions and secure the connection.
- **Cloud or ephemeral agents:** A plugin or cloud integration provisions agents on demand, such as containers or virtual machines.

Use the method supported by your environment and Jenkins version. Do not copy old JNLP or Java Web Start tutorials blindly; follow current agent launch instructions shown by Jenkins.

## 6. Pipeline agent syntax

### Run the whole Pipeline on a label

```groovy
pipeline {
    agent { label 'linux' }

    stages {
        stage('Build') {
            steps {
                sh 'echo "Building on Linux"'
            }
        }
    }
}
```

### Allocate an agent separately for each stage

```groovy
pipeline {
    agent none

    stages {
        stage('Linux checks') {
            agent { label 'linux' }
            steps {
                sh 'uname -s'
            }
        }

        stage('Windows checks') {
            agent { label 'windows' }
            steps {
                bat 'ver'
            }
        }
    }
}
```

With `agent none`, each stage that needs an executor should declare its own agent. The example requires both Linux and Windows agents to exist and have the corresponding labels.

### Use a Docker-capable agent

```groovy
pipeline {
    agent { label 'docker' }

    stages {
        stage('Check Docker') {
            steps {
                sh 'docker --version'
            }
        }
    }
}
```

The `docker` label does not install Docker; it only selects a matching node. Docker access can be highly privileged, so do not grant it to untrusted builds without a deliberate isolation design.

## 7. Executors and capacity planning

Consider:
- CPU and memory demand per build.
- Disk I/O and workspace size.
- Network downloads and artifact transfers.
- Build duration and queue length.
- Whether tasks can safely run concurrently.
- Isolation requirements between projects and teams.

A conservative starting point is one executor per agent, then adjust using observed utilization. For a Jenkins controller, use zero executors where practical so it coordinates work instead of running builds.

## 8. Common problems

| Symptom | First checks |
|---|---|
| Agent is offline | Node log, network, SSH/inbound configuration, credentials |
| Jobs remain queued | Label expression, agent online status, executor availability |
| `No such DSL method: sh` or shell failure | Agent OS, Pipeline/plugin syntax, available shell |
| Tool not found | Install tool on the agent; verify PATH under Jenkins service account |
| Builds slow after adding executors | CPU, RAM, disk I/O, network and queue metrics |
| Workspace permission error | Remote root/workspace ownership and service account |
| Agent disconnects repeatedly | Connectivity, JVM/runtime, host resources, logs |
| Build runs on controller unexpectedly | Controller executor count, job restrictions, Pipeline `agent` configuration |

## 9. Security best practices

- Run builds on agents rather than the built-in controller where possible.
- Use dedicated, minimally privileged service accounts.
- Separate trusted and untrusted workloads; do not share sensitive workspaces carelessly.
- Treat Docker socket access and privileged containers as high risk.
- Keep agent operating systems, Java runtime, and tools patched.
- Avoid storing credentials on agents longer than necessary.
- Restrict which jobs can use deployment or signing agents.
- Use ephemeral agents for disposable or untrusted workloads when feasible.
- Remember that a compromised controller can control connected agents; network segmentation alone does not remove that trust relationship.

## Module files

- [`examples.md`](examples.md) — Labels, stage-level agents, executors, and troubleshooting examples.
- [`practical.md`](practical.md) — Hands-on node setup, scheduling, capacity, and security labs.
- [`solutions.md`](solutions.md) — Suggested configurations and lab solutions.

## Official references

- [Using Jenkins agents](https://www.jenkins.io/doc/book/using/using-agents/)
- [Managing nodes](https://www.jenkins.io/doc/book/managing/nodes/)
- [Controller isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- [Securing builds](https://www.jenkins.io/doc/book/security/securing-builds/)
