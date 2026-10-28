# Runner and Agent Security — Suggested Solutions

These are reference answers. Adapt them to your CI/CD platform, infrastructure, and threat model.

## Solution 1 — Runner inventory

| Type | Ownership | Main consideration | Suitable use |
|---|---|---|---|
| Hosted | CI/CD provider manages the runner infrastructure | Understand platform isolation and available network access | Most standard build/test jobs |
| Self-hosted | Organization manages host, software, network, and patching | More control but greater security responsibility | Private-network needs or specialized hardware |
| Persistent | Reused across jobs | Residual files, processes, credentials, or host changes may survive | Only with strong isolation and controlled trust levels |
| Ephemeral | Discarded or reimaged after a job | Provisioning and image hygiene still matter | Untrusted workloads and sensitive release jobs |

These categories can overlap: a self-hosted runner can be ephemeral, and hosted-runner behavior depends on the provider's offering.

## Solution 2 — Run the risk model

Run:

```bash
python runner_risk.py
python -m unittest -v
```

The example configuration should flag untrusted code combined with a production secret, a persistent host, and private network access. The tests validate these modeled combinations. The code does not inspect a real machine or discover actual misconfigurations.

## Solution 3 — Untrusted pull requests

Risks include:
1. Pull-request code can attempt to read credentials accessible to the runner.
2. It can modify files or processes that affect later jobs on a persistent host.
3. It can probe or attack internal services reachable from the runner.
4. It can tamper with build outputs or caches.
5. It can exploit vulnerable dependencies or tools.

Mitigations:
- Use isolated, disposable runners for untrusted code.
- Do not expose deployment secrets or privileged cloud identities.
- Restrict network access.
- Separate untrusted validation from privileged release workflows.
- Use least-privilege tokens and protect workflow files.
- Do not let untrusted caches or artifacts become trusted release inputs without verification.

## Solution 4 — Least privilege

For a job that checks out source and runs tests, a typical starting point is:

```yaml
permissions:
  contents: read
```

Grant additional permissions only to the job that needs them. Test jobs generally should not have release publishing, package writing, deployment, or repository administration permissions.

## Solution 5 — Isolate release jobs

A safer design:

```text
Pull request -> isolated validation runner -> required checks
                                      |
Protected branch / release event -> approval gate
                                      |
                         isolated deployment runner
                                      |
                         short-lived scoped identity
                                      |
                              target environment
```

Keep deployment credentials out of pull-request validation. Configure environment protection and branch rules in the platform, not only through a workflow input or shell condition.

## Solution 6 — Persistent runner cleanup

Potential residual state includes workspaces, temporary files, processes, containers/images, Docker sockets, cached packages, modified binaries, credentials, and shell history. A cleanup script may miss persistence mechanisms or malicious modifications. For untrusted workloads, prefer disposable runners built from a known-good image and discarded after the job.

## Solution 7 — Network boundaries

Allow only destinations required for source checkout, dependency retrieval, artifact storage, and the job's intended service. Block unnecessary access to internal databases, management interfaces, and cloud metadata endpoints. Use network segmentation, egress filtering, firewall rules, and platform-specific identity controls. Verify that the allow-list does not silently expand over time.

## Solution 8 — Supply-chain risk

- Pin dependencies through supported lockfiles.
- Review version updates and use trusted package sources.
- Pin third-party actions to reviewed full commit SHAs for production.
- Verify signatures or checksums where supported.
- Limit scripts that run during dependency installation.
- Record source commit, workflow run, builder identity, and artifact digest.
- Protect release artifact publication and avoid mutable artifact substitution.

No single measure eliminates supply-chain risk; use layered controls.

## Solution 9 — Secret exposure tabletop

1. Revoke or rotate the exposed token immediately.
2. Restrict access to the affected logs and preserve evidence according to policy.
3. Review audit logs to identify token use during the exposure window.
4. Identify affected repositories, cloud resources, artifacts, and downstream systems.
5. Remove the exposure path, update workflow/logging practices, and document the incident.

Deleting the printed value from a later log or source file does not invalidate a leaked credential.

## Solution 10 — Runner incident response

1. Isolate or disable the runner.
2. Revoke/rotate all credentials it could access.
3. Preserve relevant logs, disk snapshots, and execution records where appropriate.
4. Identify jobs and artifacts processed during the suspected period.
5. Validate artifact digests and re-build releases from a trusted environment if needed.
6. Reimage from a known-good base and patch the underlying cause.
7. Review network, identity, and repository audit logs for lateral movement.
8. Restore runner service only after verification and authorization.
9. Document root cause and corrective actions.

## Solution 11 — Cache poisoning

An untrusted job may populate a cache key that a later privileged job restores. Separate caches by trust level and workflow, use carefully designed keys, avoid restoring untrusted caches in privileged release jobs, and validate build inputs. Do not treat cache contents as a trusted release artifact.

## Solution 12 — Runner policy review

A good policy should specify:
- **Scope:** which repositories, workflow types, and runner groups it covers.
- **Owner:** the team responsible for runner configuration and maintenance.
- **Enforcement:** runner groups, isolation, token permissions, network controls, and environment protections.
- **Monitoring:** registration changes, job activity, suspicious processes, and credential use.
- **Review frequency:** periodic review and review after significant incidents or platform changes.
- **Exceptions:** owner, reason, expiry, compensating controls, and approval.

## Stretch challenge guidance

- **Risk combinations:** test each Boolean combination and document which are accepted or flagged.
- **CI for the model:** use a read-only token and do not add deployment secrets.
- **Runner groups:** keep public/untrusted pull requests separate from internal and privileged release jobs.
- **Patch cadence:** rebuild images regularly and urgently after relevant critical vulnerabilities.
- **Retention:** retain enough information for audit and incident response while minimizing sensitive logs and artifacts.

## Final review

Runner security depends on treating job execution as potentially hostile, limiting the runner's privileges and network reach, isolating trust levels, maintaining clean runner images, and preserving enough evidence to investigate a compromise.
