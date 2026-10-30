# 01 — Jenkins Installation

Learn to install Jenkins, complete the first-time setup, verify the service, and troubleshoot common installation issues.

## Learning objectives

By completing this module, you will be able to:

- Explain Jenkins controller, agent, job, and plugin basics.
- Choose an installation method suitable for a lab or team environment.
- Install the Java runtime version supported by the Jenkins release.
- Install Jenkins on Debian/Ubuntu or run it in Docker.
- Complete the setup wizard and create an administrator account.
- Verify service health and diagnose startup, port, and password problems.
- Apply basic security and maintenance practices.

## What is Jenkins?

Jenkins is an automation server commonly used to implement continuous integration and continuous delivery (CI/CD). It can check out source code, run tests, build packages, publish artifacts, and coordinate deployments through jobs and pipelines.

- **Controller:** Hosts the web UI and coordinates jobs.
- **Agent:** Executes work assigned by the controller.
- **Job/Pipeline:** Defines the steps to automate.
- **Plugin:** Adds integrations and features.

For a learning lab, a single machine is enough. For a production environment, plan for backups, access controls, resource capacity, upgrade procedures, and appropriate separation between controller and build agents.

## Prerequisites

Jenkins requires a supported Java runtime. Check the official Java support policy before installing or upgrading. Current Jenkins releases support Java 21 or Java 25; choose a version supported by the Jenkins release you intend to run.

Recommended starting point for a small learning environment:

- 4 GB RAM or more
- 50 GB disk space or more
- A supported 64-bit operating system
- Network access to the Jenkins package repository or container registry
- A modern browser
- Administrative privileges for installation

The official documentation lists lower minimums, but the minimum is not a practical performance target for many workloads.

## Option A: Install on Debian/Ubuntu

The following commands use the Jenkins **LTS** package repository. Check the official installation page for the current repository key and supported OS instructions.

### 1. Update package metadata and install Java

```bash
sudo apt update
sudo apt install -y fontconfig openjdk-21-jre
java -version
```

Confirm that Java is installed and the version is supported by your chosen Jenkins release.

### 2. Add the Jenkins LTS repository

```bash
sudo mkdir -p /etc/apt/keyrings
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2026.key

echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/" \
  | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
```

If the official Jenkins page has changed the key or repository instructions, follow that current documentation rather than reusing stale commands.

### 3. Install and start Jenkins

```bash
sudo apt update
sudo apt install -y jenkins
sudo systemctl enable --now jenkins
sudo systemctl status jenkins --no-pager
```

Jenkins normally listens on TCP port `8080`.

### 4. Read the initial administrator password

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Open `http://localhost:8080` from the same machine, or use `http://SERVER_IP:8080` from an authorized machine if network access is configured. Enter the password, install suggested plugins, and create a named administrator account.

Do not expose port 8080 directly to the public internet. For remote access, use a controlled network path and secure access configuration.

## Option B: Run Jenkins in Docker

Use the official Jenkins image and a persistent volume so Jenkins configuration and jobs survive container replacement.

```bash
docker volume create jenkins_home

docker run -d \
  --name jenkins \
  --restart unless-stopped \
  -p 127.0.0.1:8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts-jdk21
```

This binds the web UI to localhost only. To access it from another machine, deliberately configure a secure network binding, firewall, and preferably a reverse proxy with TLS. Do not publish the controller to an untrusted network by default.

Check the container and logs:

```bash
docker ps
docker logs jenkins
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

Then open `http://localhost:8080` and complete the setup wizard. The official Jenkins Docker image does not automatically include every build tool you may need; install tools on agents or build a controlled custom image when appropriate.

## First-time setup checklist

1. Open the Jenkins URL.
2. Unlock Jenkins with the initial administrator password.
3. Install suggested plugins, or select only the plugins required for the lab.
4. Create a personal administrator account.
5. Confirm the Jenkins dashboard loads.
6. Review **Manage Jenkins** for system information, plugins, and security configuration.
7. Create a small test job only after setup is complete.

## Verify installation

On Debian/Ubuntu:

```bash
systemctl is-active jenkins
systemctl is-enabled jenkins
sudo journalctl -u jenkins.service -n 80 --no-pager
ss -lntp | grep 8080
```

In Docker:

```bash
docker ps --filter name=jenkins
docker logs --tail 80 jenkins
docker volume inspect jenkins_home
```

Expected signs of success include a running service/container, a listener on the configured port, and a working Jenkins web UI.

## Common problems

| Problem | Checks |
|---|---|
| Service does not start | `systemctl status jenkins`, `journalctl -u jenkins`, Java version |
| Port 8080 already in use | `sudo ss -lntp \| grep :8080`; choose an unused port through supported service configuration |
| Browser cannot connect | Service status, local URL, firewall, port binding, host networking |
| Initial password file missing | Confirm correct installation method and Jenkins home path |
| Docker container exits | `docker logs jenkins`, memory, volume permissions, Java compatibility |
| Plugin installation fails | Network/proxy/DNS, update center connectivity, system clock, plugin compatibility |
| Disk fills up | Jenkins home, build history, workspaces, artifacts, log retention |

## Security and maintenance

- Use a supported Jenkins LTS release for a stable learning baseline.
- Keep Java, Jenkins, and plugins updated through a planned change process.
- Use named accounts and least privilege; avoid shared administrator accounts.
- Do not store credentials in job scripts or source control; use Jenkins Credentials.
- Back up `JENKINS_HOME` and test restoration.
- Restrict network access to the controller UI and agent ports.
- Do not run untrusted builds with privileged access to the controller or host.
- Treat plugins as executable code and install only what is needed.

## Module files

- [`examples.md`](examples.md) — installation and verification examples.
- [`practical.md`](practical.md) — guided installation labs and verification tasks.
- [`solutions.md`](solutions.md) — expected results and troubleshooting answers.

## Official references

- [Jenkins download page](https://www.jenkins.io/download/)
- [Installing Jenkins on Linux](https://www.jenkins.io/doc/book/installing/linux/)
- [Installing Jenkins with Docker](https://www.jenkins.io/doc/book/installing/docker/)
- [Installing Jenkins on Windows](https://www.jenkins.io/doc/book/installing/windows/)
- [Jenkins Java support policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/)
