# GitLab Runners and Executors — Solutions

## Exercise 1: Inspect runners
Record the runners visible to the project, their scope, online/offline status, tags, and project eligibility. Run a harmless job and inspect the runner information in the job details.

**Explanation:** A runner must be eligible for the project and match the job's scheduling requirements. Instance, group, and project runner availability depends on GitLab configuration.

## Exercise 2: Runner tags

```yaml
tagged_job:
  image: alpine:3.20
  tags:
    - docker
  script:
    - echo "Runner matched"
```

**Explanation:** A runner must have all tags requested by the job. If no eligible online runner matches, the job can remain pending. Tags route work; they do not isolate permissions or make an unsafe runner safe.

## Exercise 3: Install and verify
Use the official installation instructions for your operating system, then register the runner with the current authentication-token flow. Typical verification commands on Linux include:

```bash
sudo gitlab-runner verify
sudo gitlab-runner status
```

**Explanation:** Verification checks whether registered runners can communicate with GitLab. Service status checks whether the local runner service is running. Exact commands and service management can differ by installation method.

## Exercise 4: Shell vs Docker

```yaml
shell_diagnostics:
  tags: [shell-lab]
  script:
    - whoami
    - pwd
    - uname -a

docker_diagnostics:
  image: alpine:3.20
  tags: [docker]
  script:
    - whoami
    - pwd
    - cat /etc/os-release
```

**Explanation:** The Shell executor runs commands on the runner host. The Docker executor runs the job in a container image. Shell offers limited isolation; Docker provides a more consistent job environment but must still be hardened.

## Exercise 5: Docker config review

```toml
concurrent = 2

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

**Explanation:** `concurrent` is the maximum number of jobs the runner process can run at once. `limit` sets the maximum jobs for this runner entry. `privileged = false` avoids granting broad container privileges. The token shown is a placeholder only.

## Exercise 6: Concurrency

```yaml
stages: [test]

job_one:
  stage: test
  image: alpine:3.20
  tags: [docker]
  script:
    - sleep 10
    - echo "one done"

job_two:
  stage: test
  image: alpine:3.20
  tags: [docker]
  script:
    - sleep 10
    - echo "two done"

job_three:
  stage: test
  image: alpine:3.20
  tags: [docker]
  script:
    - sleep 10
    - echo "three done"
```

**Explanation:** Jobs can overlap if enough eligible runner capacity exists. Global `concurrent` limits the runner process; a per-runner `limit` further constrains that runner entry. CPU, memory, network, and executor capacity also affect throughput.

## Exercise 7: Offline runner
On a disposable Linux systemd lab host:

```bash
sudo systemctl stop gitlab-runner
sudo gitlab-runner status
sudo systemctl start gitlab-runner
sudo gitlab-runner verify
```

**Explanation:** While the runner is offline, jobs assigned to it cannot execute. Once it is online and eligible, pending jobs may be picked up.

## Exercise 8: Kubernetes executor
A typical job pod contains the build container and helper container, plus service containers when configured. The runner uses the Kubernetes API to create and manage the pod. The helper performs checkout and artifact/cache operations.

**Review points:**
- Service account has only required permissions.
- Namespace is dedicated or appropriately isolated.
- Pod security context uses non-root execution where supported.
- Resource requests and limits are set.
- Network policies restrict unnecessary access.
- Job pods are cleaned up according to policy.

## Exercise 9: Security review — sample findings

| Risk | Mitigation |
|---|---|
| Shared Shell runner executes untrusted code | Use isolated, dedicated runners for trusted workloads |
| Docker privileged mode enabled unnecessarily | Disable privileged mode; use safer build approaches |
| Docker socket mounted into job | Avoid host socket exposure; isolate builders |
| Broad Kubernetes service account permissions | Apply least-privilege RBAC and namespace restrictions |
| Runner token committed to Git | Revoke/rotate token and store credentials securely |
| Unpinned or untrusted job images | Use approved images and immutable digests |
| Runner can reach sensitive internal services | Apply network segmentation and egress restrictions |
| Old runner host or executor components | Patch and monitor the host and runtime |

## Exercise 10: Troubleshooting

| Symptom | Likely cause | Resolution |
|---|---|---|
| Job pending with tag mismatch | No eligible runner has all required tags | Correct job tags or configure an appropriate runner |
| Docker image pull fails | Registry DNS/authentication, rate limit, or image name/tag issue | Verify image reference, registry access, and pull credentials |
| Shell command not found | Dependency absent on runner host or PATH differs | Install dependency on a controlled host or use a suitable container image |
| Kubernetes pod Pending | Insufficient resources, quota, scheduling constraints, image pull, or RBAC issue | Inspect `kubectl describe pod`, events, quota, and runner permissions |
| Runner verification fails | Incorrect URL/token, network, TLS, or revoked runner | Verify endpoint and connectivity; re-register using current workflow if required |
| Jobs queue | Concurrency limit reached or insufficient runner capacity | Review limits and add capacity safely |

## Viva answers
1. **GitLab Runner:** An agent that polls GitLab and executes CI/CD jobs.
2. **Executor:** The environment or mechanism used to run a job.
3. **Runner scope:** Project runners are assigned to a project; group runners serve a group; instance runners can be shared across an instance according to admin settings.
4. **Tags:** A job's tags are matched against runner tags to route it to eligible runners.
5. **Shell vs Docker:** Shell runs directly on the host; Docker runs in a job container.
6. **Shell risk:** Jobs have access to the host filesystem and permissions of the runner service account, with limited isolation.
7. **Kubernetes executor:** It creates a pod for each CI job through the Kubernetes API.
8. **`concurrent`:** Maximum jobs that the runner process can run simultaneously.
9. **`limit`:** Per-runner maximum job concurrency.
10. **Privileged mode:** It grants broader capabilities and can weaken container isolation.
11. **Runner token:** It authenticates the runner; exposure can allow unauthorized runner access or abuse.
12. **Pending causes:** Offline or ineligible runner, tag mismatch, paused runner, project access restriction, or exhausted concurrency.

## Further reading
- [Executors overview](https://docs.gitlab.com/runner/executors/)
- [Docker executor](https://docs.gitlab.com/runner/executors/docker/)
- [Shell executor](https://docs.gitlab.com/runner/executors/shell/)
- [Kubernetes executor](https://docs.gitlab.com/runner/executors/kubernetes/)
