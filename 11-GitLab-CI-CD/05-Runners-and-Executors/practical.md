# GitLab Runners and Executors — Practical Exercises

## Lab safety
Use a disposable GitLab project and a machine or cluster you administer. Do not register a runner on a production host for practice. Do not expose Shell, privileged Docker, or Kubernetes runners to untrusted projects. Keep runner tokens private.

## Exercise 1: Inspect available runners
1. Open your test project's **Settings > CI/CD > Runners** (menu wording may vary).
2. Identify which instance, group, or project runners are available.
3. Record runner status, tags, and whether it is allowed for the project.
4. Run a simple pipeline and identify the runner that picked up the job.

**Deliverable:** A short table of runner scope, status, and tags.

## Exercise 2: Test runner tags
1. Add a job with a tag that matches an available runner.
2. Run the pipeline and confirm it is picked up.
3. Change the tag to a value that no runner has.
4. Observe the pending job.
5. Restore the correct tag.

**Question:** Why are tags useful for routing jobs, and why are they not a security boundary by themselves?

## Exercise 3: Install and verify a lab runner
On a disposable Linux VM that you administer:
1. Install GitLab Runner using the official instructions for your distribution.
2. Register it using the current GitLab runner authentication-token workflow.
3. Select an executor appropriate for the lab.
4. Run `gitlab-runner verify` and `gitlab-runner status`.
5. Confirm the runner appears online in GitLab.

Do not paste the token into screenshots, chat, source control, or shell history shared with others.

## Exercise 4: Compare Shell and Docker executors
1. Run a diagnostic job on a dedicated Shell runner.
2. Run the same job on a Docker runner using `alpine:3.20`.
3. Compare `whoami`, `pwd`, and `/etc/os-release`.
4. Explain where commands execute and what environment dependencies exist.

**Expected result:** Shell runs on the host; Docker runs inside the configured job container.

## Exercise 5: Inspect Docker executor configuration
Review the Docker runner's `config.toml`:
- Identify the default image.
- Identify `privileged`.
- Identify cache volume configuration.
- Identify runner concurrency and per-runner limit.

Do not enable privileged mode for this exercise.

## Exercise 6: Understand runner concurrency
1. Create three jobs in the same stage, each sleeping briefly.
2. Run them on a runner with capacity for multiple concurrent jobs.
3. If you administer the lab runner, change its concurrency limit and repeat.
4. Compare the pipeline timeline.

**Question:** What is the difference between global `concurrent` and a runner's `limit`?

## Exercise 7: Diagnose an offline runner
In a disposable lab only:
1. Stop the runner service.
2. Observe the runner status in GitLab and a job becoming pending.
3. Start the service again.
4. Verify the runner and observe job recovery.

Example Linux systemd commands:

```bash
sudo systemctl stop gitlab-runner
sudo systemctl start gitlab-runner
sudo gitlab-runner status
sudo gitlab-runner verify
```

## Exercise 8: Kubernetes executor research or lab
If you have a Kubernetes lab cluster:
1. Review the GitLab Runner Kubernetes executor prerequisites.
2. Inspect the runner namespace and service account permissions.
3. Run a harmless job and observe the job pod.
4. Inspect pod events and resource requests/limits.
5. Confirm the job pod is cleaned up as configured.

If you do not have a cluster, create an architecture diagram and document the pod lifecycle instead. Do not use a production cluster for an introductory exercise.

## Exercise 9: Runner security review
Review a lab runner configuration for:
- Runner scope and project access.
- Shell executor exposure.
- Docker privileged mode and socket mounts.
- Kubernetes service account permissions.
- Runner token handling.
- Image version pinning.
- Network egress and access to internal systems.
- Host patching, monitoring, and cleanup.

**Deliverable:** List at least five risks and recommended mitigations.

## Exercise 10: Troubleshooting scenarios
For each scenario, record the symptom, likely cause, evidence, and fix:
1. Job remains pending due to a tag mismatch.
2. Docker job cannot pull its image.
3. Shell job cannot find a required command.
4. Kubernetes job pod remains Pending.
5. Runner verification fails after a token or URL change.
6. Jobs queue because runner concurrency is exhausted.

## Submission checklist
- [ ] Runner scope and tags inspected.
- [ ] A matching tag job succeeded.
- [ ] A mismatched tag job was observed pending.
- [ ] Runner registration and verification documented.
- [ ] Shell and Docker behavior compared.
- [ ] Docker runner configuration reviewed.
- [ ] Concurrency behavior measured.
- [ ] Offline runner recovery demonstrated.
- [ ] Kubernetes executor architecture reviewed.
- [ ] Security review and troubleshooting notes submitted.

## Viva questions
1. What is GitLab Runner?
2. What is an executor?
3. Differentiate a project, group, and instance runner.
4. How do runner tags work?
5. How does the Shell executor differ from Docker?
6. What is the main security concern with Shell executor?
7. How does the Kubernetes executor run a job?
8. What does `concurrent` control?
9. What is the purpose of a per-runner `limit`?
10. Why should privileged Docker mode be avoided?
11. Why must runner tokens be protected?
12. What are common causes of a pending job?
