# GitLab CI/CD — Runners and Executors

## Overview
A **GitLab Runner** is an agent that receives and executes CI/CD jobs. An **executor** defines the environment in which a runner executes those jobs. Choosing and configuring runners correctly affects reliability, performance, isolation, and security.

This module covers runner architecture, registration, tags, concurrency, common executor types, configuration, and operational security.

## Learning objectives
- Explain the role of GitLab Runner in a CI/CD pipeline.
- Differentiate runner scope, runner tags, and executor types.
- Understand the job lifecycle from scheduling to completion.
- Compare Shell, Docker, and Kubernetes executors.
- Read basic `config.toml` settings.
- Register and validate a runner in a disposable lab.
- Diagnose pending jobs and runner failures.
- Apply least privilege and isolation to runner infrastructure.

## Runner architecture

1. A GitLab pipeline creates jobs from `.gitlab-ci.yml`.
2. GitLab schedules eligible jobs to runners based on availability, scope, tags, and other settings.
3. A runner polls GitLab for jobs.
4. The selected executor prepares an environment.
5. The runner checks out source, restores cache/downloads artifacts, and runs the job script.
6. The runner uploads artifacts and reports job status.

A runner is not the same thing as an executor:
- **Runner:** the agent/service that requests and manages jobs.
- **Executor:** the mechanism/environment used to run a job (for example Docker or Kubernetes).

## Runner scope

| Scope | Typical use |
|---|---|
| Instance runner | Shared across projects on a GitLab instance, subject to administrator configuration |
| Group runner | Available to projects in a group or subgroup, subject to settings |
| Project runner | Dedicated or specifically assigned to a project |

Availability and naming of runner scopes can vary with GitLab offering and configuration. Check the project's runner settings.

## Runner tags
Tags route jobs to runners with matching capabilities. A job with tags can be picked up only by a runner that has all the job's required tags and is otherwise eligible.

```yaml
linux_docker_job:
  image: alpine:3.20
  tags:
    - linux
    - docker
  script:
    - echo "Executed by an eligible Linux Docker runner"
```

If no eligible online runner matches, the job can remain pending. Tags are scheduling labels, not a security boundary by themselves.

## Executors at a glance

| Executor | Job environment | Advantages | Considerations |
|---|---|---|---|
| Shell | Local host shell | Simple; useful for trusted local tasks | Limited isolation; host dependencies; jobs can affect shared host state |
| Docker | Container per job | Consistent container environment; convenient dependencies | Requires Docker Engine; container isolation is not a complete security boundary |
| Kubernetes | Pod per job | Cluster scheduling; resource controls; scalable | Requires Kubernetes API access and cluster operations knowledge |
| Docker Autoscaler | Docker containers on autoscaled instances | Adapts capacity to demand | Cloud/autoscaler setup and lifecycle management |
| Instance | Autoscaled instance | Runs jobs directly on provisioned instances | Host-level isolation and image lifecycle need careful design |

GitLab also lists other executors. Some older executors are in maintenance mode; consult current executor documentation before selecting one for a new deployment.

## Shell executor
The Shell executor runs job scripts locally on the runner host. Dependencies must already exist on that host.

Example registration command (interactive; use a runner authentication token from GitLab and follow current registration guidance):

```bash
sudo gitlab-runner register
```

Choose the Shell executor when prompted. Then verify the runner:

```bash
sudo gitlab-runner verify
sudo gitlab-runner status
```

Security note: Shell jobs execute with the runner service account's permissions and have limited isolation. Use only for trusted workloads on a host dedicated to those jobs. Do not run untrusted merge-request code on a shared privileged Shell runner.

## Docker executor
The Docker executor runs each job in a container using a configured image. A runner's `config.toml` includes a Docker section and a default image.

Illustrative configuration:

```toml
concurrent = 2

[[runners]]
  name = "lab-docker-runner"
  url = "https://gitlab.example.com/"
  token = "REDACTED"
  executor = "docker"

  [runners.docker]
    image = "alpine:3.20"
    privileged = false
    volumes = ["/cache"]
```

Do not copy real runner tokens into documentation or commit `config.toml` with live credentials. Keep runner authentication tokens protected and rotate/revoke them if exposed.

A job can select its image:

```yaml
container_job:
  image: alpine:3.20
  script:
    - cat /etc/os-release
    - echo "Container job"
```

Docker executor jobs run in separate containers. However, privileged mode, host socket mounts, host bind mounts, and unsafe container configuration can significantly weaken isolation. Avoid privileged mode unless there is a reviewed requirement.

## Kubernetes executor
The Kubernetes executor uses the Kubernetes API to create a pod for each CI job. The pod contains the job and helper containers, plus service containers when configured.

Conceptual flow:
1. Runner requests a job.
2. Runner creates a Kubernetes pod.
3. Job container runs the script.
4. Helper processes source checkout and artifact/cache operations.
5. Pod is cleaned up according to runner configuration.

Use Kubernetes executor when your organization already operates a suitable cluster and needs cluster-based scheduling. Apply namespace isolation, RBAC least privilege, pod security controls, resource requests/limits, network policies, and cleanup policies.

## Important `config.toml` settings

| Setting | Purpose |
|---|---|
| `concurrent` | Maximum number of jobs a runner process can run concurrently |
| `check_interval` | Polling interval behavior for checking jobs |
| `executor` | Selects execution environment |
| `limit` | Per-runner job concurrency limit |
| `request_concurrency` | Limits concurrent job requests |
| `builds_dir` | Build working directory |
| `cache_dir` | Cache directory |
| `[runners.docker]` | Docker executor configuration |
| `[runners.kubernetes]` | Kubernetes executor configuration |

`concurrent` is global to the runner process; `limit` applies to an individual runner entry. Effective capacity is also constrained by runner availability, project settings, and executor resources.

## Basic runner operations

```bash
# Check installed version
gitlab-runner --version

# Check service status (Linux systemd installation)
sudo gitlab-runner status

# Validate registered runners
sudo gitlab-runner verify

# Restart after configuration changes (Linux systemd)
sudo systemctl restart gitlab-runner
```

Use commands appropriate to your operating system and installation method. Avoid sharing runner tokens or full configuration output in public logs.

## Security best practices
- Use dedicated runners for sensitive workloads.
- Separate trusted protected-branch jobs from untrusted merge-request jobs.
- Prefer ephemeral or isolated execution environments for untrusted code.
- Run jobs with the least privileges required.
- Avoid privileged containers and Docker socket mounts unless strictly necessary.
- Restrict runner scope and project access.
- Protect runner tokens and rotate them after suspected exposure.
- Pin job images to controlled versions or immutable digests.
- Patch the runner host, Docker Engine, Kubernetes nodes, and helper images.
- Apply network egress controls and avoid unnecessary access to internal services.
- Monitor runner logs, job activity, and infrastructure changes.

## Troubleshooting

| Symptom | Checks |
|---|---|
| Job pending | Runner online? Correct scope? Tags match? Runner allowed for project? Concurrency available? |
| Runner offline | Service status, network/DNS, TLS, token validity, GitLab reachability |
| Docker job fails | Docker daemon, image pull, shell in image, permissions, disk space |
| Kubernetes pod pending | Namespace quota, RBAC, node capacity, image pull, pod events |
| Permission denied | Runner service user, file ownership, mounted volume permissions |
| Jobs slow or queued | Concurrency, CPU/memory, executor capacity, registry latency |
| Runner not verifying | URL, token, outbound connectivity, certificate trust |

## Suggested lab sequence
1. Inspect available runners in a test project.
2. Run a simple job and inspect its runner details.
3. Add and test a runner tag.
4. Compare Shell and Docker execution in isolated environments.
5. Inspect runner service status and verify commands.
6. Review runner logs and diagnose a deliberately incorrect tag.
7. Write a short security review of the runner configuration.

## References
- [GitLab Runner documentation](https://docs.gitlab.com/runner/)
- [Executors overview](https://docs.gitlab.com/runner/executors/)
- [Docker executor](https://docs.gitlab.com/runner/executors/docker/)
- [Shell executor](https://docs.gitlab.com/runner/executors/shell/)
- [Kubernetes executor](https://docs.gitlab.com/runner/executors/kubernetes/)
- [Advanced runner configuration](https://docs.gitlab.com/runner/configuration/advanced-configuration/)
