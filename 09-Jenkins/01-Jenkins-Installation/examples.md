# Jenkins Installation — Examples

## Example 1: Check Java before installing Jenkins

```bash
java -version
```

If Java is not installed or the version is unsupported by the Jenkins release, install a supported version first. The Java version used to run Jenkins does not have to match the version used to build every application.

## Example 2: Install Jenkins on Debian/Ubuntu

```bash
sudo apt update
sudo apt install -y fontconfig openjdk-21-jre

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

Use the current official installation instructions if the repository key or supported package steps change.

## Example 3: Read the initial administrator password

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Copy the value into the Jenkins unlock page. Treat this password as sensitive and do not paste it into a public issue or commit it to a repository.

## Example 4: Inspect service logs

```bash
sudo journalctl -u jenkins.service -n 100 --no-pager
sudo systemctl status jenkins --no-pager
```

Look for the first relevant error, such as an unsupported Java version, a port conflict, or a permissions problem. Do not assume the last log line is the root cause.

## Example 5: Check whether port 8080 is in use

```bash
sudo ss -lntp | grep ':8080'
```

If another service owns the port, identify it before making changes. Either stop the conflicting service if appropriate or configure Jenkins to use an available port using the supported service configuration. Remember to update firewall rules and the browser URL if the port changes.

## Example 6: Run Jenkins with persistent Docker storage

```bash
docker volume create jenkins_home

docker run -d \
  --name jenkins \
  --restart unless-stopped \
  -p 127.0.0.1:8080:8080 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts-jdk21
```

Verify:

```bash
docker ps --filter name=jenkins
docker logs --tail 60 jenkins
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

The local-only port binding limits access to the host. Use an intentional secure setup before enabling remote access.

## Example 7: Stop and start a Docker container

```bash
docker stop jenkins
docker start jenkins
docker ps --filter name=jenkins
```

A named volume preserves Jenkins home when the container is replaced. It is not a backup by itself; use a tested backup process.

## Example 8: Install on Windows

1. Visit the official [Jenkins download page](https://www.jenkins.io/download/).
2. Download the Windows installer for the chosen LTS release.
3. Confirm a supported Java runtime is installed.
4. Run the installer and follow the setup wizard.
5. Use a dedicated service account with only the permissions needed; avoid running Jenkins as LocalSystem unless you have a specific, justified reason.
6. Open the configured Jenkins URL, unlock it, install plugins, and create an administrator user.
7. Verify the Jenkins Windows service is running.

Follow the current official Windows guide for exact installer options.

## Example 9: Check the Jenkins home directory

Package installations commonly use `/var/lib/jenkins`; official Docker images commonly use `/var/jenkins_home` inside the container.

```bash
# Package installation
sudo ls -la /var/lib/jenkins

# Docker installation
docker exec jenkins sh -c 'ls -la /var/jenkins_home'
```

Do not change ownership or permissions recursively without understanding which account runs Jenkins and which files need access.

## Example 10: Verify the web endpoint

```bash
curl -I http://127.0.0.1:8080/login
```

A successful HTTP response indicates that a web server responded; it does not by itself prove that authentication, plugins, or all Jenkins functions are healthy. Confirm the UI loads and log in.

## Example 11: Minimal installation report

```text
Installation method: Debian/Ubuntu package
Jenkins release channel: LTS
Java version: [record output]
Service status: [record output]
Web URL: http://localhost:8080
Initial setup completed: Yes/No
Admin account created: Yes/No
Security review completed: Yes/No
Known issues: [list issues or None]
```
