# Self-Hosted Runner Security - Practical Exercises

Use a dedicated lab organization or private test repository. Do not expose a runner with access to sensitive networks or credentials to untrusted code.

## Lab 1: Threat-model a self-hosted runner

1. Draw the path from pull-request event to workflow job to runner host.
2. Identify all users who can trigger workflows or modify workflow YAML.
3. List secrets, tokens, files, and network services accessible to the runner account.
4. Identify how malicious code could persist or exfiltrate data.
5. Propose controls for each risk.

**Deliverable:** Threat model with assets, trust boundaries, threats, and mitigations.

## Lab 2: Create a restricted runner group

1. In a test organization, create a runner group named `ci-low-privilege`.
2. Restrict access to a selected test repository.
3. Register a disposable test runner into the group.
4. Add a workflow that targets the group and a matching label.
5. Confirm that an unauthorized repository cannot use the group, where you have permission to test this.

## Lab 3: Harden the Linux host

1. Create a dedicated, unprivileged runner account.
2. Install the runner in a dedicated directory.
3. Remove unnecessary packages and services.
4. Restrict SSH or interactive access to approved administrators.
5. Review file ownership and permissions.
6. Enable host patching and security logging.
7. Document the baseline configuration.

Do not run workflow jobs as root.

## Lab 4: Configure an ephemeral runner

1. Provision a disposable VM from a trusted image.
2. Register the runner using the supported `--ephemeral` option.
3. Run one harmless workflow job.
4. Verify that the runner is automatically deregistered after the job.
5. Destroy or re-image the VM.
6. Confirm that logs were forwarded to external storage before teardown.

## Lab 5: Separate trust levels

Design two runner groups:

- Low-privilege CI runners for trusted, non-deployment checks.
- Restricted deployment runners for approved deployment workflows.

Document repository access, workflow restrictions, secrets, network access, and approval requirements for each group. Do not run untrusted pull-request code on the deployment group.

## Lab 6: Network isolation review

1. Draw the runner's network path to GitHub and package registries.
2. Identify internal networks and cloud metadata endpoints reachable from the host.
3. Define required inbound and outbound connections.
4. Propose firewall and egress filtering rules.
5. Validate that the runner can still perform its required jobs after restrictions are applied.

## Lab 7: Monitoring and incident response

Create a response runbook for suspected runner compromise. Include:

- Runner disablement and host isolation.
- Log preservation.
- Registration token revocation and secret rotation.
- Review of workflow runs and repository changes.
- Cloud audit log review.
- Trusted rebuild and re-enrollment criteria.

## Lab 8: Security assessment

Review your runner design against the checklist in `README.md`. Identify at least five gaps, assign risk levels, and propose remediation owners and due dates.

## Completion checklist

- [ ] Can explain self-hosted runner risks.
- [ ] Can restrict runner access with groups.
- [ ] Understands host and service-account hardening.
- [ ] Can explain ephemeral and JIT runner behavior.
- [ ] Can design network isolation.
- [ ] Can separate untrusted CI from privileged deployment.
- [ ] Has a monitoring and incident response plan.
