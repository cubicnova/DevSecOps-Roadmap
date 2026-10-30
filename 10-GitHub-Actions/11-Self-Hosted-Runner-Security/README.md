# 11 - Self-Hosted Runner Security

Self-hosted GitHub Actions runners execute workflow jobs on infrastructure that you manage. They can provide access to private networks, specialized hardware, and custom software, but they also create a significant security boundary: workflow code runs on your runner host.

This module covers runner threat models, host hardening, isolation, ephemeral runners, runner groups, network controls, secrets, monitoring, and incident response.

## Learning objectives

- Explain the security risks of self-hosted runners.
- Identify trust boundaries between repositories, workflows, jobs, and runner hosts.
- Restrict which repositories and workflows can use a runner.
- Harden Linux runner hosts and protect runner credentials.
- Understand persistent versus ephemeral and just-in-time runners.
- Isolate workloads and restrict network access.
- Monitor runner activity and respond to compromise.

## 1. Self-hosted runner threat model

A self-hosted runner executes code defined by a workflow. That code may come from application source, build scripts, dependencies, pull requests, and third-party actions. Malicious or compromised workflow code can attempt to:

- Read files, credentials, caches, or environment variables accessible to the runner account.
- Persist on a long-lived host and affect later jobs.
- Access internal services or cloud metadata endpoints.
- Exfiltrate secrets or build artifacts.
- Abuse a runner's network location or host permissions.
- Compromise other repositories that share the same runner.

GitHub warns that self-hosted runners do not provide the same clean, isolated VM guarantees as GitHub-hosted runners. Untrusted workflow code can persistently compromise a self-hosted runner. Avoid using self-hosted runners for public repositories; carefully assess fork and pull-request workflows even in private repositories.

## 2. Architecture and trust boundaries

A safer design separates runners by trust and privilege:

```text
GitHub repository
       |
       v
Workflow trigger and policy
       |
       v
Runner group access policy
       |
       +-----------------------------+
       |                             |
       v                             v
Low-privilege runner group     Restricted deployment group
Lint / tests / scans           Protected deployment workflows
No production credentials      Limited network and short-lived identity
       |                             |
       v                             v
Ephemeral isolated host        Ephemeral isolated host
       |                             |
       v                             v
Destroy / re-image             Destroy / re-image
```

Do not let untrusted pull-request jobs share infrastructure with deployment jobs or runners that have access to sensitive networks.

## 3. Runner groups and labels

Runner groups control which repositories can access a set of organization or enterprise runners. Labels help workflows select a compatible runner.

Example workflow:

```yaml
jobs:
  build:
    runs-on:
      group: ci-low-privilege
      labels: [self-hosted, linux, x64]
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - run: echo "Run non-privileged build checks"
```

Configure the group and repository access policy in GitHub settings. A workflow label is not a security boundary by itself; access policy and host isolation are essential.

## 4. Host hardening

Recommended controls for a Linux runner host:

- Use a dedicated VM or physical host; do not use a personal workstation or a domain controller.
- Run the runner service under a dedicated, unprivileged account.
- Keep the operating system, runner application, and installed tools patched.
- Remove unnecessary packages, services, users, and credentials.
- Restrict interactive logins and administrative access.
- Use host firewall rules and network segmentation.
- Protect runner work directories and configuration files.
- Avoid storing long-lived SSH keys, cloud keys, or personal credentials on the host.
- Monitor disk, CPU, process, authentication, and network activity.
- Rebuild from a trusted image after suspected compromise.

Do not run arbitrary workflow jobs as root. If a workload requires elevated privileges, isolate it on a dedicated disposable runner and narrowly scope the access.

## 5. Ephemeral and just-in-time runners

An ephemeral runner is registered to process at most one job and is automatically deregistered afterward. Registering a runner with `--ephemeral` is one way to enable this behavior:

```bash
./config.sh --url https://github.com/OWNER/REPOSITORY \
  --token RUNNER_REGISTRATION_TOKEN \
  --ephemeral
```

Use a real short-lived registration token from the supported GitHub process. Never place it in a committed script, workflow log, or shared shell history.

Just-in-time (JIT) runners can be provisioned through GitHub's REST API and are configured for one job. They can reduce persistence risk when paired with a clean, disposable environment.

Important: ephemeral registration alone does not clean reused hardware. Destroy or re-image the VM/container after the job, and forward runner logs to external storage before destroying the host if they are needed for investigation.

## 6. Workflow trust and pull requests

- Prefer GitHub-hosted runners for untrusted pull-request validation.
- Do not execute untrusted pull-request code on a runner that can access internal systems or production secrets.
- Be especially careful with `pull_request_target`; it runs in a privileged context and must not check out and execute untrusted code.
- Restrict who can modify workflow files and runner settings.
- Separate untrusted validation, trusted branch builds, and deployment workflows.
- Require review and branch protection for changes to workflows that target privileged runners.

## 7. Network isolation

Place runner hosts in a dedicated network segment. Allow only the outbound destinations required for GitHub connectivity, source retrieval, package registries, and explicitly approved services.

- Block unnecessary inbound access.
- Restrict access to internal production networks.
- Prevent access to cloud metadata endpoints unless strictly required and safely controlled.
- Use egress filtering, DNS controls, and network monitoring.
- Avoid sharing a runner network namespace with sensitive workloads.
- Do not assume that a container alone isolates a malicious job from the host.

## 8. Secrets and cloud identity

- Do not bake secrets into runner images.
- Avoid persistent cloud access keys on runner hosts.
- Prefer short-lived credentials and OIDC federation where supported.
- Scope credentials to one job and one environment where possible.
- Use environment approvals for sensitive deployments.
- Ensure one job cannot inspect another job's process arguments, temporary files, or credentials.
- Rotate credentials immediately if a runner may have been compromised.

## 9. Monitoring and incident response

Monitor:

- Runner registration, removal, and group changes.
- Unexpected workflow execution and repository access.
- OS logins, privilege escalation, and new services.
- Unexpected outbound connections and DNS queries.
- Changes to runner binaries, configuration, and work directories.
- Secret access and cloud identity activity.

If compromise is suspected:

1. Disable or remove the affected runner from GitHub.
2. Isolate the host from internal networks.
3. Preserve relevant logs and forensic evidence.
4. Revoke runner registration credentials and rotate accessible secrets.
5. Review workflow runs, artifacts, repository changes, and cloud audit logs.
6. Rebuild the runner from a trusted image; do not simply restart it.
7. Identify the entry point and improve controls before re-enabling the runner.

## 10. Security checklist

- [ ] Self-hosted runners are not used for untrusted public-repository pull requests.
- [ ] Runner groups restrict access to approved repositories.
- [ ] High-privilege jobs use dedicated runner groups.
- [ ] Hosts use dedicated unprivileged accounts.
- [ ] Runners are ephemeral or rebuilt between jobs.
- [ ] Network access is restricted and monitored.
- [ ] No long-lived credentials are stored on runner hosts.
- [ ] Runner and host software are patched.
- [ ] Logs are forwarded off-host.
- [ ] Incident response and credential rotation procedures are documented.

## Further reading

- [GitHub Actions secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Managing access to self-hosted runners using groups](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access)
- [Self-hosted runner reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)
- [OWASP GitHub Actions Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/GitHub_Actions_Security_Cheat_Sheet.html)
