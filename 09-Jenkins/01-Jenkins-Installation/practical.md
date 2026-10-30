# Jenkins Installation — Practical Exercises

Use a personal lab machine, virtual machine, or local Docker environment. Do not expose a new Jenkins controller to the public internet.

## Lab 1: Check prerequisites

Tasks:
1. Record operating system and architecture.
2. Check available memory and disk space.
3. Run `java -version`.
4. Compare the Java version with the official Jenkins support policy.
5. Choose package installation or Docker and explain why.

Commands you may use:

```bash
uname -a
free -h
df -h
java -version
```

**Deliverable:** A prerequisite checklist.

## Lab 2: Install Jenkins on Debian/Ubuntu

Tasks:
1. Update apt metadata.
2. Install a supported Java runtime.
3. Add the official Jenkins LTS repository using current official instructions.
4. Install Jenkins.
5. Enable and start the service.
6. Capture service status without including secrets.

**Deliverable:** Installation commands and service status.

## Lab 3: Complete the setup wizard

Tasks:
1. Open `http://localhost:8080`.
2. Read the initial administrator password from the appropriate local file.
3. Unlock Jenkins.
4. Install suggested plugins.
5. Create a named administrator account.
6. Sign in and confirm the dashboard loads.

**Deliverable:** A checklist of completed setup steps. Do not include the initial password in your report.

## Lab 4: Verify the service

Tasks:
1. Check `systemctl is-active jenkins`.
2. Check `systemctl is-enabled jenkins`.
3. Inspect recent logs with `journalctl`.
4. Confirm which port is listening.
5. Open the UI and log in.

**Deliverable:** A verification report.

## Lab 5: Docker installation

Tasks:
1. Confirm Docker is installed and running.
2. Create a named volume for Jenkins home.
3. Run the official Jenkins LTS image with port 8080 bound to localhost.
4. Read the initial password from the container.
5. Complete the setup wizard.
6. Restart the container and confirm that configuration persists.

Suggested commands:

```bash
docker volume create jenkins_home

docker run -d \
  --name jenkins \
  --restart unless-stopped \
  -p 127.0.0.1:8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts-jdk21
```

**Deliverable:** Container status and a persistence test.

## Lab 6: Troubleshoot a port conflict

Scenario: Jenkins fails to start because port 8080 is already in use.

Tasks:
1. Inspect service status and logs.
2. Identify the process listening on port 8080.
3. Decide whether to stop the conflicting process or change Jenkins' port.
4. Apply the change using supported configuration.
5. Verify the service and access the correct URL.

**Deliverable:** Root cause and verification evidence.

## Lab 7: Troubleshoot Java compatibility

Scenario: Jenkins exits on startup after a Java upgrade.

Tasks:
1. Check the Java version used by the Jenkins service, not only your interactive shell.
2. Inspect Jenkins service logs.
3. Compare the version with the official Java support policy for your Jenkins release.
4. Install or configure a supported Java runtime.
5. Restart Jenkins and verify service health.

**Deliverable:** A brief root-cause report.

## Lab 8: Basic security review

Tasks:
1. Confirm that an administrator account was created.
2. Review user and authorization settings.
3. Confirm the controller is reachable only from the intended network.
4. Identify where credentials should be stored for later pipelines.
5. Explain why builds from untrusted sources should not receive privileged access to the controller or host.

**Deliverable:** Five security findings or checks.

## Lab 9: Backup planning

Tasks:
1. Identify Jenkins home for your installation method.
2. List the important configuration and job data to protect.
3. Propose a backup frequency and retention policy.
4. Describe how you would restore the backup to a test environment.
5. Explain why a Docker volume alone is not a backup.

**Deliverable:** A short backup and recovery plan.

## Lab 10: Installation acceptance test

Create an acceptance checklist and mark each item passed or failed:

- [ ] Supported Java runtime confirmed
- [ ] Jenkins package or container starts
- [ ] Service/container restarts successfully
- [ ] Web UI responds
- [ ] Initial setup completed
- [ ] Named administrator account created
- [ ] Network access is restricted appropriately
- [ ] Jenkins home persistence is understood
- [ ] Logs can be inspected
- [ ] Backup plan documented

**Deliverable:** Completed checklist and unresolved issues.

## Assessment rubric

| Criterion | Points |
|---|---:|
| Prerequisite and Java checks | 15 |
| Correct installation steps | 25 |
| Setup wizard and verification | 20 |
| Troubleshooting approach | 20 |
| Security and backup awareness | 20 |
| **Total** | **100** |
