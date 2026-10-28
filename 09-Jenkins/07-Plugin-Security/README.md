# 07 — Jenkins Plugin Security

## Overview
Jenkins plugins extend CI/CD functionality, but each plugin adds code, permissions, dependencies, and maintenance risk to the controller. Plugin security is the practice of selecting, installing, configuring, updating, monitoring, and removing plugins in a controlled way.

This module teaches you to build a repeatable plugin-governance process for a Jenkins environment.

## Learning objectives
By the end of this module, you should be able to:
- Explain why plugins expand the Jenkins attack surface.
- Assess plugin ownership, maintenance, compatibility, dependencies, and permissions.
- Review official Jenkins security advisories and plugin warnings.
- Install plugins through approved update sources and test updates safely.
- Inventory plugins and track versions, dependencies, and owners.
- Plan mitigations for vulnerable, abandoned, or unnecessary plugins.
- Apply least privilege, change control, backups, and rollback procedures.

## Core concepts

### 1. Plugin attack surface
A plugin executes as part of Jenkins and may interact with jobs, credentials, agents, files, web requests, or the UI. A vulnerable or malicious plugin can therefore affect more than the feature it provides.

### 2. Plugin selection
Before adopting a plugin, review:
- Whether the capability is genuinely needed.
- The plugin's official Jenkins plugin page and source repository.
- Release history, recent maintenance, open issues, and maintainer activity.
- Required Jenkins core version and dependency chain.
- Published security warnings and fixed-version guidance.
- License, support expectations, and organizational approval.

Popularity alone does not prove that a plugin is safe.

### 3. Advisories and patching
Check the official [Jenkins Security Advisories](https://www.jenkins.io/security/advisories/) and [Handling Vulnerabilities in Plugins](https://www.jenkins.io/security/plugins/). For every relevant advisory, record the affected plugin, affected versions, fixed version (if available), severity, exposure, mitigation, owner, and target date. If no fix is available, consider disabling or uninstalling the plugin and follow the advisory's workaround.

### 4. Trusted update sources
Use the configured, approved Jenkins update center. Avoid installing arbitrary `.hpi` or `.jpi` files from unverified websites. Validate plugin provenance and compatibility before deployment. The official [Jenkins Update Sites](https://updates.jenkins.io/) page documents the default update site.

### 5. Least privilege and secrets
- Restrict who can install, configure, disable, and upgrade plugins.
- Keep credentials in Jenkins Credentials rather than hard-coding them in jobs.
- Do not assume a plugin's masking behavior makes secrets safe to print.
- Use scoped credentials, short-lived tokens where practical, and rotation after suspected exposure.
- Avoid granting builds administrative permissions.

### 6. Lifecycle management
Maintain an inventory, review it regularly, remove unused plugins, test updates in a staging controller, back up the controller configuration and plugin list, and define a rollback path. An old plugin should not remain installed merely because it was installed years ago.

## Suggested workflow
1. Export or record the current plugin inventory.
2. Identify business purpose and owner for each plugin.
3. Review official security advisories and plugin metadata.
4. Classify each plugin: keep, update, replace, disable, or remove.
5. Test proposed changes in a representative non-production controller.
6. Back up relevant configuration and document rollback steps.
7. Apply approved changes during a controlled window.
8. Verify startup, jobs, credentials integrations, agents, and audit logs.
9. Record evidence and schedule the next review.

## Lab safety
Use a disposable Jenkins instance or a non-production controller. Do not test plugin vulnerabilities against systems you do not own or have explicit authorization to assess. Never install a deliberately malicious plugin on a production controller.

## Knowledge check
1. Why can a plugin vulnerability affect stored credentials or build execution?
2. What is the difference between a vulnerable plugin with a fix and one with no available fix?
3. Why should updates be tested before production rollout?
4. What information belongs in a plugin inventory?
5. Why is plugin minimization a security control?

## Further reading
- [Jenkins Security Advisories](https://www.jenkins.io/security/advisories/)
- [Handling Vulnerabilities in Plugins](https://www.jenkins.io/security/plugins/)
- [Jenkins Security](https://www.jenkins.io/security/)
- [Jenkins Update Sites](https://updates.jenkins.io/)
