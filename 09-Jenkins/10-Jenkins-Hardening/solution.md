# Solutions and Guidance: Jenkins Hardening

Use these reference points to evaluate the labs. The exact settings and steps depend on Jenkins core, plugins, operating system, and network architecture.

## Lab 1: Inventory
A useful inventory records each asset's owner, version, purpose, trust level, exposure, dependencies, and recovery method. Prioritize the controller, administrator identities, credentials, release jobs, agents, and artifact publication/deployment integrations.

## Lab 2: Access control
Use a supported security realm and a deliberate authorization strategy. Restrict administrator membership, remove unnecessary anonymous access, and carefully limit `Job/Configure`, credential, agent, and controller-management permissions. Test with separate non-admin identities.

## Lab 3: Network exposure
Compare listening ports with a documented service inventory. Keep only necessary listeners reachable, restrict the backend behind a reverse proxy, and disable the inbound agent TCP port or other services if unused. Verify agents and webhooks after each change.

## Lab 4: HTTPS and reverse proxy
Users should reach Jenkins through HTTPS. The proxy must forward the correct host and scheme information and support the features used by the deployment. Restrict direct access to the backend port. Test login, redirects, webhooks, agent connections, and CSRF-protected requests before production rollout.

## Lab 5: Controller isolation
Jenkins documentation recommends setting the built-in node executor count to zero and running builds on agents. Ensure at least one suitable agent is available first. Verify a real build's assigned node after the change.

## Lab 6: Trust zones
Separate untrusted pull-request validation from trusted release and deployment workloads. Use distinct agent pools, operating-system identities, network access, credentials, and job permissions. A Jenkins label by itself is not a security boundary; enforce the separation in agent provisioning and authorization.

## Lab 7: Plugin review
For each plugin, record whether it is needed, its owner, version, dependencies, security-advisory status, and regression plan. Test updates on a staging controller, then verify SCM, credentials, authentication, agents, and deployment pipelines. Remove unused plugins only after checking dependencies.

## Lab 8: Credentials
Remove broad credential access where possible. Limit credentials to the folders/jobs that need them, use short-lived credentials or workload identity where supported, and never expose deployment secrets to untrusted pull-request code. Rotate any credential that may have been exposed.

## Lab 9: Jenkins data
Protect the actual `JENKINS_HOME` path with service-account ownership and restrictive permissions. Protect backups and recovery keys with separate access controls, encryption, and retention rules. Test restoration in a safe environment and verify credentials/integrations after recovery.

## Lab 10: Monitoring
Useful signals include repeated failed logins, changes to authorization or security settings, administrator membership changes, plugin installation/removal, unexpected agent registration, unusual build execution, and suspected credential leakage. Route alerts to an owner and document triage steps.

## Lab 11: Recovery drill
A robust plan includes:
1. Pre-change backup and a tested restore procedure.
2. Versioned plugin/core change list and dependencies.
3. Maintenance window and communication.
4. Smoke tests for login, authorization, SCM, agents, credentials, and critical pipelines.
5. Rollback criteria and a known-good version/configuration.
6. Validation of administrator access and logs after rollback.

Keep recovery material protected; a backup can contain credentials and other sensitive controller data.

## Lab 12: Assessment report
Rank findings by likelihood, impact, and exposure. Each finding should include evidence, owner, due date, remediation, and a retest procedure. Track exceptions with a business justification, compensating controls, approver, and expiry date.

## Baseline checklist
- [ ] Supported Jenkins and Java versions
- [ ] Security realm and least-privilege authorization
- [ ] HTTPS and restricted network access
- [ ] Unused ports and services disabled
- [ ] Built-in node has zero executors
- [ ] Trusted and untrusted builds isolated
- [ ] Plugin inventory and update process maintained
- [ ] Credentials scoped and rotated
- [ ] `JENKINS_HOME`, logs, artifacts, and backups protected
- [ ] Monitoring and incident response documented
- [ ] Backup restoration and rollback tested

## Official references
- [Managing Security](https://www.jenkins.io/doc/book/managing/security/)
- [Controller Isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- [Exposed Services and Ports](https://www.jenkins.io/doc/book/security/services/)
- [Jenkins Security Advisories](https://www.jenkins.io/security/advisories/)
