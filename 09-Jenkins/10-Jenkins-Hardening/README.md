# Jenkins Hardening

Jenkins hardening reduces the risk that a compromised account, vulnerable plugin, malicious build, or exposed controller can affect the wider software delivery environment. Treat the controller as a sensitive production service and assume pipeline code can execute commands on its assigned agents.

## Learning objectives

- Identify the most important Jenkins attack surfaces.
- Harden controller access, authorization, networking, and service configuration.
- Separate controller responsibilities from build execution.
- Manage Jenkins core and plugin updates safely.
- Protect credentials, agents, backups, and build artifacts.
- Perform a repeatable hardening assessment and document exceptions.

## Hardening domains

| Domain | Baseline goal |
|---|---|
| Authentication and authorization | Strong identity controls and least-privilege permissions |
| Network exposure | HTTPS, restricted network access, minimal open ports |
| Controller isolation | Do not run builds on the built-in node; use isolated agents |
| Agents | Separate trust levels, use least privilege, and rebuild disposable agents |
| Plugins and core | Maintain supported versions and review security advisories |
| Credentials | Narrow scope, short-lived credentials where possible, rotation and audit |
| Pipeline execution | Treat code and build scripts as untrusted unless reviewed |
| Data protection | Restrict `JENKINS_HOME`, backups, logs, and artifacts |
| Monitoring | Collect authentication, configuration, plugin, and build audit signals |
| Recovery | Test backups, document rollback, and rehearse incident response |

## Practical hardening sequence

1. **Inventory:** document Jenkins core version, Java runtime, plugins, users/groups, credentials, agents, jobs, exposed services, and integrations.
2. **Secure access:** configure a supported security realm, least-privilege authorization, and strong administrator authentication.
3. **Reduce exposure:** place the controller on a private network or behind a properly configured HTTPS reverse proxy; expose only required endpoints.
4. **Isolate builds:** set the built-in node's executor count to `0` and use dedicated agents.
5. **Patch deliberately:** review Jenkins security advisories, test core/plugin updates in staging, then deploy with a rollback plan.
6. **Protect secrets:** narrow credential scope and avoid giving secrets to untrusted pull-request builds.
7. **Review agents:** isolate untrusted jobs from release agents and restrict agent-to-controller access.
8. **Protect data:** restrict filesystem access to `JENKINS_HOME`; encrypt and control backups.
9. **Monitor:** alert on unexpected administrator changes, authentication failures, plugin changes, and unusual build behavior.
10. **Verify:** test both expected access and denied access, record exceptions, and repeat regularly.

## Network and reverse-proxy notes

- Serve the user interface over HTTPS.
- Ensure the Jenkins URL and reverse-proxy forwarding configuration are correct.
- Restrict direct access to the backend listener so users cannot bypass the proxy's controls.
- Disable the inbound agent TCP listener if unused; if required, restrict it to trusted networks and agents.
- Disable unused services and plugins that expose additional endpoints.
- Keep webhook endpoints accessible only as required, using provider verification and network controls where appropriate.

Do not blindly copy reverse-proxy or firewall settings from another environment. Validate webhook delivery, redirects, WebSocket/agent connections, and CSRF behavior in staging.

## Controller and agent isolation

Jenkins documentation recommends not running builds on the built-in node because builds can access the controller process's filesystem and privileges. Set the built-in node's executor count to `0` and provision agents. Agent isolation is still necessary: a compromised agent can threaten credentials and workloads available to that agent.

Separate agents by trust level, for example:
- Untrusted pull-request validation
- Trusted branch CI
- Release/package publication
- Production deployment

Use distinct credentials, labels, network access, and operating-system identities for these pools.

## Plugin and core management

- Maintain a supported Jenkins LTS line and compatible Java runtime.
- Review official security advisories and upgrade guidance.
- Inventory plugins and remove those that are unused.
- Install plugins only from trusted sources and restrict plugin administration.
- Test upgrades in a staging controller, including authentication, SCM, agents, credentials, and deployment paths.
- Avoid treating a successful upgrade as proof of security; verify configuration and known exposure paths afterwards.

## Operational checklist

- [ ] Admin access is limited and reviewed.
- [ ] Anonymous access is explicitly reviewed.
- [ ] CSRF protection remains enabled unless a documented, reviewed exception exists.
- [ ] Jenkins UI is HTTPS-only from user networks.
- [ ] Unused agent listener ports and services are disabled.
- [ ] Built-in node has zero executors.
- [ ] Untrusted and privileged workloads use separate agents.
- [ ] Credentials are scoped and rotated.
- [ ] Core and plugins are maintained.
- [ ] `JENKINS_HOME` and backups are access-controlled.
- [ ] Logs and alerts cover sensitive changes.
- [ ] Recovery and incident response are tested.

## Official references

- [Managing Security](https://www.jenkins.io/doc/book/managing/security/)
- [Controller Isolation](https://www.jenkins.io/doc/book/security/controller-isolation/)
- [Exposed Services and Ports](https://www.jenkins.io/doc/book/security/services/)
- [Jenkins Security Advisories](https://www.jenkins.io/security/advisories/)
- [Jenkins Upgrade Guide](https://www.jenkins.io/doc/upgrade-guide/)
