# Jenkins Installation — Suggested Solutions

## Lab 1: Check prerequisites

A good answer records the OS, architecture, memory, disk, Java version, installation method, and source of the compatibility check. The Java runtime used by Jenkins must be supported by the Jenkins release. Check the official Java support policy rather than relying on old tutorials.

## Lab 2: Install Jenkins on Debian/Ubuntu

A typical LTS installation sequence is:

```bash
sudo apt update
sudo apt install -y fontconfig openjdk-21-jre
java -version

sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null

sudo apt update
sudo apt install -y jenkins
sudo systemctl enable --now jenkins
sudo systemctl status jenkins --no-pager
```

If the official page changes the key or repository instructions, use the current official documentation. Successful installation should be confirmed through service status and logs.

## Lab 3: Complete the setup wizard

For a package installation, the initial password is commonly available at:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Use it only in the local unlock wizard. Install suggested plugins, create a named administrator, and log in. Do not place the password in source control or lab screenshots.

## Lab 4: Verify the service

Useful commands:

```bash
systemctl is-active jenkins
systemctl is-enabled jenkins
sudo journalctl -u jenkins.service -n 80 --no-pager
sudo ss -lntp | grep 8080
```

Expected results are an active service, enabled startup if configured, no fatal startup error in recent logs, a listener on the expected port, and a working web UI.

## Lab 5: Docker installation

Example:

```bash
docker volume create jenkins_home

docker run -d \
  --name jenkins \
  --restart unless-stopped \
  -p 127.0.0.1:8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts-jdk21
```

Then:

```bash
docker ps --filter name=jenkins
docker logs --tail 80 jenkins
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

The named volume keeps Jenkins home outside the disposable container layer. A persistence test should confirm that jobs/settings remain after a container restart. A backup is still required.

## Lab 6: Port conflict

Identify the listener:

```bash
sudo ss -lntp | grep ':8080'
```

Determine whether the owning process is needed before stopping it. If Jenkins must use a different port, update its service configuration according to the current package documentation, restart the service, inspect logs, and open the new URL. Do not simply open more firewall ports without checking the intended exposure.

## Lab 7: Java compatibility

Check service logs:

```bash
sudo journalctl -u jenkins.service -n 100 --no-pager
java -version
```

The `java` command in your shell may not be the same runtime selected by the service. Check service environment and configuration, compare the runtime with the official Jenkins Java support policy, then configure a supported version and restart Jenkins. Verify the new service status and logs.

## Lab 8: Basic security review

A strong answer includes:
- Named users instead of shared accounts.
- Least-privilege authorization.
- Restricted network access and TLS for remote access.
- Credentials stored in Jenkins Credentials rather than source files.
- Minimal plugin installation and planned updates.
- Untrusted builds isolated from privileged controller and host access.

## Lab 9: Backup planning

For package installation, Jenkins home is commonly `/var/lib/jenkins`; for the official Docker image it is `/var/jenkins_home` inside the container. Confirm the actual configured location.

A practical plan includes scheduled backups, retention, access-controlled storage, a documented restore process, and periodic restore tests. Coordinate backups with Jenkins activity or use an appropriate backup method to avoid inconsistent data. A Docker volume is persistent storage, but it can still be deleted, corrupted, or lost with the host.

## Lab 10: Acceptance test

Mark an item passed only after collecting evidence. For example, a running process alone does not prove the web UI is usable. The acceptance test should include the service/container state, login, restart persistence, logs, network exposure, and backup plan.

## Troubleshooting quick reference

| Symptom | First action |
|---|---|
| Jenkins service is inactive | `systemctl status jenkins` and `journalctl -u jenkins` |
| Java error at startup | Verify service runtime against the supported Java policy |
| Port bind error | Identify the process listening on the configured port |
| Browser connection refused | Check service/container, port binding, host, and firewall |
| Unlock password not found | Verify install method and Jenkins home path |
| Container exits repeatedly | Inspect `docker logs`, resource limits, and volume access |
| Plugins cannot download | Check DNS, proxy, outbound access, system time, and update center reachability |

## Official references

- [Installing Jenkins on Linux](https://www.jenkins.io/doc/book/installing/linux/)
- [Installing Jenkins with Docker](https://www.jenkins.io/doc/book/installing/docker/)
- [Installing Jenkins on Windows](https://www.jenkins.io/doc/book/installing/windows/)
- [Jenkins Java support policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
