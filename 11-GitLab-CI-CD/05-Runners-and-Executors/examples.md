# GitLab Runners and Executors — Examples

> Examples are for a disposable lab. Never publish real runner authentication tokens or expose privileged runners to untrusted projects.

## 1. Select a tagged runner

```yaml
linux_job:
  image: alpine:3.20
  tags:
    - linux
    - docker
  script:
    - echo "This job needs a runner with both tags"
```

The runner must match all required tags and be eligible for the project.

## 2. Inspect job execution context

```yaml
runner_diagnostics:
  image: alpine:3.20
  script:
    - echo "Runner description: ${CI_RUNNER_DESCRIPTION}"
    - echo "Runner ID: ${CI_RUNNER_ID}"
    - echo "Project: ${CI_PROJECT_PATH}"
    - uname -a
    - cat /etc/os-release
```

Use only non-sensitive diagnostic values. Do not dump all environment variables.

## 3. Docker executor job

```yaml
docker_job:
  image: alpine:3.20
  tags:
    - docker
  script:
    - echo "Running inside a Docker job container"
    - id
    - cat /etc/os-release
```

The runner must be configured with the Docker executor and have an eligible Docker runner tag.

## 4. Docker service example

```yaml
test_with_database:
  image: alpine:3.20
  services:
    - name: postgres:16
      alias: db
  variables:
    POSTGRES_DB: app_test
    POSTGRES_USER: app_user
    POSTGRES_PASSWORD: "lab-only-password"
    POSTGRES_HOST_AUTH_METHOD: trust
  script:
    - echo "Database service is declared as db"
    - echo "Install a PostgreSQL client and add a readiness check for a real integration test"
```

This illustrates service wiring only. `POSTGRES_HOST_AUTH_METHOD: trust` is not appropriate for production. Use protected credentials and secure database authentication for real testing.

## 5. Shell executor job

```yaml
shell_job:
  tags:
    - shell-lab
  script:
    - echo "Running in the Shell executor environment"
    - whoami
    - pwd
    - uname -a
```

The commands run on the runner host, not in a job container. The host must contain the required commands.

## 6. Illustrative Docker runner config.toml

```toml
concurrent = 2
check_interval = 3

[[runners]]
  name = "docker-lab"
  url = "https://gitlab.example.com/"
  token = "REDACTED"
  executor = "docker"
  limit = 2

  [runners.docker]
    image = "alpine:3.20"
    privileged = false
    volumes = ["/cache"]
```

Replace the example URL and register the runner through GitLab's supported workflow. Do not manually invent or reuse a token.

## 7. Illustrative Shell runner config.toml

```toml
concurrent = 1

[[runners]]
  name = "trusted-shell-lab"
  url = "https://gitlab.example.com/"
  token = "REDACTED"
  executor = "shell"
  limit = 1
  shell = "bash"
```

Use a dedicated host and trusted projects only. Shell executor jobs have limited isolation.

## 8. Illustrative Kubernetes executor config.toml

```toml
concurrent = 4

[[runners]]
  name = "kubernetes-lab"
  url = "https://gitlab.example.com/"
  token = "REDACTED"
  executor = "kubernetes"

  [runners.kubernetes]
    namespace = "gitlab-runner"
    image = "alpine:3.20"
    poll_timeout = 180
```

This is a minimal conceptual example, not a complete production configuration. Configure Kubernetes credentials, RBAC, pod security, resource limits, and cleanup according to your environment.

## 9. Concurrency and per-runner limit

```toml
concurrent = 4

[[runners]]
  name = "runner-a"
  url = "https://gitlab.example.com/"
  token = "REDACTED"
  executor = "docker"
  limit = 2
  [runners.docker]
    image = "alpine:3.20"

[[runners]]
  name = "runner-b"
  url = "https://gitlab.example.com/"
  token = "REDACTED"
  executor = "docker"
  limit = 3
  [runners.docker]
    image = "alpine:3.20"
```

The global `concurrent` value caps the runner process. Per-runner `limit` values also apply; actual job throughput is constrained by the effective configuration and available resources.

## 10. Check runner service

```bash
gitlab-runner --version
sudo gitlab-runner status
sudo gitlab-runner verify
```

On a Linux systemd installation, service logs can be inspected with:

```bash
sudo journalctl -u gitlab-runner -n 100 --no-pager
```

Use the correct service manager for your OS and installation method.

## 11. Validate Docker availability on a runner host

```bash
docker version
docker info
sudo gitlab-runner verify
```

These are host administration commands. Do not grant broad Docker access to untrusted CI jobs merely to make a pipeline pass.

## 12. Security-oriented job image pinning

```yaml
controlled_image_job:
  # Example tag; for high-assurance builds prefer an approved immutable digest.
  image: alpine:3.20
  script:
    - echo "Use an organization-approved, scanned build image"
```

A mutable tag can point to different image contents over time. For reproducible, controlled environments, use reviewed images and immutable digests where practical.
