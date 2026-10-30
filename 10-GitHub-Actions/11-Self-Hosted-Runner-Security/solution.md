# Self-Hosted Runner Security - Solutions and Explanations

Use these reference answers to evaluate the practical exercises. The exact host commands and GitHub settings depend on your operating system, account type, and runner deployment model.

## Lab 1: Threat model

| Asset | Threat | Example mitigation |
|---|---|---|
| Runner registration credentials | Theft or misuse | Short-lived registration token; restrict access |
| `GITHUB_TOKEN` | Excessive repository access | Minimal workflow permissions |
| Cloud identity | Lateral movement or resource abuse | OIDC with narrow trust and short-lived credentials |
| Runner filesystem | Persistence between jobs | Ephemeral disposable VM and clean image |
| Internal network | Unauthorized access | Network segmentation and egress filtering |
| Workflow definition | Malicious command injection | Protected branches, review, and trusted workflows |
| Build artifacts | Tampering or disclosure | Provenance, access controls, and integrity checks |

The runner must be treated as a remote code execution environment because workflow jobs execute commands on its host.

## Lab 2: Runner groups

A secure group policy should allow only explicitly approved repositories. A workflow can select a group and labels:

```yaml
runs-on:
  group: ci-low-privilege
  labels: [self-hosted, linux, x64]
```

Runner group settings enforce repository access. Labels are scheduling selectors, not authorization controls. Verify group access in organization settings and test with a repository that is not allowed.

## Lab 3: Linux host hardening

Example account and directory setup:

```bash
sudo useradd --system --create-home --shell /usr/sbin/nologin actions-runner
sudo mkdir -p /opt/actions-runner
sudo chown -R actions-runner:actions-runner /opt/actions-runner
sudo chmod 750 /opt/actions-runner
```

The runner should not run as root or have broad sudo rights. Restrict interactive access, patch the OS and runner, and keep credentials out of the runner home directory. Validate service configuration for the distribution in use.

## Lab 4: Ephemeral runner

Registration example:

```bash
./config.sh \
  --url https://github.com/OWNER/REPOSITORY \
  --token "$RUNNER_REGISTRATION_TOKEN" \
  --ephemeral
```

An ephemeral runner is automatically deregistered after one job. This limits reuse but does not itself guarantee the underlying machine is clean. Use automation to destroy or re-image the VM and forward logs externally before teardown.

## Lab 5: Trust separation

| Runner group | Workloads | Secrets | Network |
|---|---|---|---|
| `ci-low-privilege` | Approved builds, lint, tests | None or minimal | Public package and GitHub endpoints only |
| `restricted-deploy` | Protected deployment workflows | Short-lived, environment-scoped credentials | Only approved deployment endpoints |

Use GitHub-hosted runners for untrusted pull-request validation where possible. Do not let untrusted workflow code access the deployment runner group.

## Lab 6: Network isolation

A reasonable baseline:

- Deny unsolicited inbound connections.
- Permit administrative access only from a controlled management network.
- Permit outbound GitHub runner connectivity and required package registries.
- Deny access to production subnets unless explicitly required.
- Block cloud metadata endpoints unless a documented design requires controlled access.
- Log and alert on unexpected outbound connections.

GitHub's endpoint requirements can change. Confirm current documentation before implementing an allowlist.

## Lab 7: Incident response

1. Disable or remove the compromised runner from GitHub.
2. Isolate its host from internal networks.
3. Preserve system, runner, network, and workflow logs.
4. Revoke registration credentials and rotate all secrets the runner could access.
5. Review repository changes, workflow runs, artifacts, and cloud audit events.
6. Rebuild from a trusted image rather than merely restarting the runner.
7. Identify the root cause and validate controls before re-enrollment.

## Lab 8: Example assessment findings

| Finding | Risk | Recommended remediation |
|---|---|---|
| Long-lived runner processes multiple trust levels | Critical/High | Separate groups and use ephemeral hosts |
| Runner can reach production database subnet | High | Restrict routes and egress |
| Runner account has unrestricted sudo | High | Dedicated unprivileged account and limited elevation |
| Registration token stored in shell history | High | Remove exposure and use secure short-lived retrieval |
| No external log forwarding | Medium | Centralize runner and host logs |
| Runner group allows all repositories | High | Restrict to selected repositories |
| No documented rebuild process | Medium | Automate trusted-image rebuild and re-enrollment |

Risk levels should be adjusted based on actual exposure, access, and business impact.

## Common troubleshooting

| Symptom | Likely cause | Resolution |
|---|---|---|
| Runner does not receive a job | Group policy or labels do not match | Verify repository access, group, and labels |
| Registration fails | Invalid/expired token or incorrect URL | Generate a new supported registration token and verify scope |
| Ephemeral runner remains online | Job has not completed or lifecycle automation is incomplete | Review job state and runner service logs |
| Job cannot reach a package registry | Egress rules are too restrictive | Add only the documented required destination |
| Runner cannot access a deployment resource | Intended network or identity restriction | Verify the approved path and least-privilege identity |
| Logs disappear after teardown | Logs were not forwarded | Configure external log forwarding before rollout |

## Security answer guide

Self-hosted runners are high-trust infrastructure that executes workflow-controlled code. Restrict access with runner groups, use dedicated unprivileged hosts, isolate networks, avoid persistent credentials, separate untrusted validation from deployment, and prefer ephemeral disposable systems. A one-job runner reduces persistence risk but must be paired with clean host lifecycle management and external logging.

## Suggested grading rubric

| Area | Points |
|---|---:|
| Threat model | 15 |
| Runner group access control | 15 |
| Host hardening | 15 |
| Ephemeral runner lifecycle | 15 |
| Trust separation | 10 |
| Network isolation | 10 |
| Monitoring and incident response | 10 |
| Security assessment | 10 |
| **Total** | **100** |
