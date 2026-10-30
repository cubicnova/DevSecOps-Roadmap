# Practical Exercises: Jenkins Hardening

Perform these exercises in a lab or staging environment. For production systems, use approved change control and a tested recovery plan.

## Lab 1: Build an asset inventory
Record Jenkins core and Java versions, plugins, users/groups, jobs, credentials, agents, exposed ports, reverse proxy, backups, and SCM/cloud integrations. Identify the highest-impact assets.

## Lab 2: Review access control
Check the configured security realm and authorization strategy. Review administrator membership, anonymous permissions, broad authenticated-user grants, and who can configure jobs or credentials. Record evidence without including secrets.

## Lab 3: Review network exposure
Inspect listening sockets and firewall rules. Map each exposed port to a documented purpose. Identify unnecessary services and propose a staged disablement or restriction plan.

## Lab 4: Verify HTTPS and reverse proxy
Check that users reach Jenkins through HTTPS, the backend cannot be accessed to bypass required controls, and redirects/webhooks/CSRF-protected actions work. Document certificate renewal and proxy ownership.

## Lab 5: Isolate the controller
Check the built-in node's executor count. Configure or verify a separate agent before setting the built-in node to zero executors. Confirm a test build runs on the intended agent.

## Lab 6: Separate trust zones
Design separate pools for untrusted pull requests, trusted CI, release packaging, and production deployment. Document label restrictions, network access, credentials, OS identity, and disposal/rebuild strategy.

## Lab 7: Plugin risk review
Export the plugin list. For each plugin, record purpose, owner, version, dependency, advisory status, and update plan. Select one low-risk plugin for a staging update and regression test.

## Lab 8: Credential exposure review
Review which jobs can access global, folder, and item credentials. Identify credentials available to untrusted builds. Recommend narrower scope, short-lived credentials, rotation, and separation of publish/deploy jobs.

## Lab 9: Protect Jenkins data
Inspect the actual `JENKINS_HOME` location, service account, filesystem permissions, backup access, retention, encryption, and restoration process. Do not print secret files or copy them to a public location.

## Lab 10: Logging and monitoring
Define alerts for unexpected administrator changes, repeated authentication failures, plugin installations, authorization changes, unusual build behavior, and credential exposure. Identify log sources, retention, and response owners.

## Lab 11: Recovery drill
Write a recovery plan for a failed core/plugin upgrade or a bad authorization change. Include backups, maintenance window, rollback criteria, service validation, administrator access checks, and communication.

## Lab 12: Final hardening assessment
Create a prioritized report with:
- Finding and affected asset
- Evidence and business impact
- Likelihood/severity
- Recommended remediation
- Owner and due date
- Validation method
- Exception and expiry, if a control cannot be implemented

Include at least one verified fix and its retest evidence. Do not claim a control is effective based only on a configuration value; test the actual behavior.
