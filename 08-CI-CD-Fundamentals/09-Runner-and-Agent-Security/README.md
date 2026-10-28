# 09 — Runner and Agent Security

This module explains how to secure the machines and execution environments that run CI/CD jobs. Runners and agents can access source code, build artifacts, tokens, internal networks, and sometimes deployment credentials, so they are important security boundaries.

## Learning objectives

- Explain hosted runners, self-hosted runners, and build agents.
- Identify risks from untrusted pull requests, persistent workspaces, and over-privileged runners.
- Apply isolation, least privilege, patching, network restrictions, and credential hygiene.
- Design safer CI workflows for trusted and untrusted code.
- Describe runner lifecycle, monitoring, and incident response.
- Review a runner security checklist for a DevSecOps pipeline.

## Prerequisites

- Basic Git and GitHub Actions knowledge.
- Familiarity with CI/CD jobs, workflow permissions, artifacts, and secrets.
- Basic operating-system and network security knowledge.

## 1. What is a runner or agent?

A **runner** (or **agent**) is the execution environment that runs CI/CD workflow jobs. It checks out code, installs dependencies, executes scripts and tests, builds packages, and may publish artifacts or deploy applications.

Common types:

- **Hosted runner:** provided and managed by the CI/CD platform.
- **Self-hosted runner:** deployed and managed by the organization on its own infrastructure.
- **Ephemeral runner:** created for a job or short-lived workload and then discarded.
- **Persistent runner:** reused across multiple jobs or workflow runs.

Exact isolation and cleanup behavior depends on the platform and runner configuration. Do not assume a runner is clean simply because a job ended.

## 2. Why runner security matters

A job can execute arbitrary code from the repository, dependencies, build scripts, tests, and sometimes pull requests. If a runner has a token, cloud credential, internal network access, or residual files from earlier jobs, malicious code may use them.

Potential impact includes:

- Theft of repository or cloud credentials.
- Exfiltration of source code, artifacts, or secrets.
- Persistence on a self-hosted runner.
- Lateral movement into internal networks.
- Tampering with build outputs or release artifacts.
- Unauthorized deployment or changes to infrastructure.

Treat the runner as a security boundary, not merely a convenient build machine.

## 3. Hosted vs. self-hosted runners

| Consideration | Hosted runner | Self-hosted runner |
|---|---|---|
| Infrastructure maintenance | Mostly handled by provider | Organization patches and maintains it |
| Customization | Platform-defined options | Greater control |
| Network access | Usually constrained by provider setup | May reach private networks if configured |
| Isolation | Depends on platform and runner offering | Must be deliberately designed |
| Operational burden | Lower | Higher |
| Main responsibility | Configure workflows and permissions safely | Secure both workflow and runner infrastructure |

Choose based on security requirements, network needs, compliance, cost, and operational capacity. Hosted does not mean risk-free; self-hosted does not automatically mean insecure.

## 4. Threat model

Important threats include:

1. **Untrusted pull-request code:** a malicious change executes during tests.
2. **Credential exposure:** a job can read a token or secret it does not need.
3. **Cross-job contamination:** files, processes, caches, Docker state, or credentials survive between jobs.
4. **Runner persistence:** an attacker modifies a persistent host or installs a backdoor.
5. **Network pivoting:** a compromised job reaches internal services or metadata endpoints.
6. **Dependency compromise:** install scripts execute malicious code during the build.
7. **Artifact tampering:** a compromised runner publishes modified binaries or packages.
8. **Over-privileged token:** workflow permissions allow unnecessary repository writes or releases.

## 5. Core security controls

### Isolation and lifecycle
- Prefer ephemeral or clean, isolated runners for workloads that execute untrusted code.
- Separate trusted release jobs from untrusted pull-request validation.
- Do not run untrusted code on a self-hosted runner that has production credentials or sensitive internal access.
- Rebuild or reimage runners from a known-good base rather than relying only on cleanup scripts.
- Restrict concurrency and access to runner groups; isolate workloads by trust level.

### Least privilege
- Set restrictive workflow-level token permissions.
- Grant additional permissions only to jobs that require them.
- Scope cloud roles and deployment identities to the specific target and action.
- Keep deployment secrets out of build/test jobs.
- Prefer short-lived credentials and workload identity federation where supported.

### Network and host hardening
- Limit outbound and inbound network access to required destinations.
- Restrict access to cloud metadata services and internal control planes where appropriate.
- Patch the OS, runner software, container runtime, and installed tools.
- Use non-root execution where feasible.
- Disable unnecessary services and remove unused tools.
- Monitor runner registration, job execution, process activity, and configuration changes.

### Supply chain and artifacts
- Pin and review third-party actions and build dependencies.
- Use lockfiles and verify downloaded artifacts where possible.
- Keep build logs free of secrets.
- Record source commit, workflow run, artifact digest, and builder identity.
- Restrict who can publish or overwrite release artifacts.
- Use provenance and signing where supported by the platform and organization.

## 6. GitHub Actions-specific cautions

- A `pull_request` workflow can run code supplied by a contributor. Treat that code as untrusted.
- Avoid using privileged `pull_request_target` workflows to check out and execute pull-request code unless the design has been carefully reviewed.
- Use minimal `GITHUB_TOKEN` permissions.
- Do not expose secrets to workflows triggered by untrusted forks.
- Do not attach sensitive self-hosted runners to repositories or runner groups that accept untrusted workloads.
- Protect workflow files and runner administration with code review and restricted permissions.
- Pin third-party actions to reviewed full commit SHAs for production use.

## 7. Example trust boundaries

```text
Untrusted Pull Request
        |
        v
Isolated / disposable validation runner
        |
        +--> lint, tests, safe scans
        |
        v
No production secrets or private-network access

Trusted Release Workflow
        |
        v
Protected branch + required checks + approval
        |
        v
Isolated deployment runner
        |
        v
Short-lived, narrowly scoped deployment identity
        |
        v
Target environment
```

Do not promote artifacts from an untrusted workflow without validating their origin and integrity.

## 8. Incident response

If runner compromise is suspected:

1. Disable or isolate the affected runner.
2. Revoke and rotate credentials the runner could access.
3. Preserve relevant logs and forensic evidence.
4. Identify jobs, repositories, artifacts, and systems that may have been affected.
5. Rebuild the runner from a trusted image; do not rely on deleting one suspicious file.
6. Verify artifacts and releases produced during the suspected exposure window.
7. Review network and identity logs for lateral movement or credential use.
8. Restore service only after containment and validation.
9. Document root cause and improve controls.

## 9. Hands-on lab

`examples.md` includes a safe workflow review, a local runner-risk simulation, and a GitHub Actions workflow with minimal permissions. It does not attempt to exploit a runner or access real secrets.

Official documentation:
- [GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners)
- [Self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners)
- [Secure use reference](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)

## Module files

- `README.md` — runner concepts, threat model, and security controls.
- `examples.md` — safe code examples and workflow patterns.
- `practical.md` — hands-on exercises.
- `solution.md` — suggested answers and review guidance.

## Completion checklist

- [ ] I can explain the difference between hosted, self-hosted, persistent, and ephemeral runners.
- [ ] I can identify runner-specific threat scenarios.
- [ ] I can design safe handling for untrusted pull requests.
- [ ] I can apply least privilege and reduce secret exposure.
- [ ] I understand runner isolation, patching, and network controls.
- [ ] I can describe a runner compromise response plan.
