# Jenkins Hardening Examples

These examples are assessment and configuration patterns. Test changes in a non-production Jenkins instance first. Exact settings depend on Jenkins version, operating system, reverse proxy, and installed plugins.

## Example 1: Controller executor baseline

**Goal:** keep builds off the built-in node.

In Jenkins, open **Manage Jenkins → Nodes** (the exact menu may vary), select the built-in node, and configure its number of executors to `0`. Save only after at least one suitable agent is configured and online; otherwise builds may remain queued.

Verify the setting through the UI and confirm normal builds execute on an agent rather than the controller.

## Example 2: Inventory commands

Run these on the Jenkins host with appropriate administrative access. Paths and service names vary by OS and installation.

```bash
# Confirm service status on a systemd-based Linux host
sudo systemctl status jenkins

# Inspect recent service logs
sudo journalctl -u jenkins --since "24 hours ago"

# Inspect listener sockets; choose the command available on the host
sudo ss -lntp
```

Do not paste logs into public issue trackers without removing tokens, usernames, internal hostnames, and other sensitive data.

## Example 3: Filesystem permissions

On a Linux installation, inspect the Jenkins home directory and service identity:

```bash
sudo systemctl show jenkins --property=User --property=Group
sudo stat -c '%U:%G %a %n' /var/lib/jenkins
```

Use the actual `JENKINS_HOME` path for your installation. Set ownership and permissions according to the service account and documented deployment method. Do not apply a blanket recursive permission change without reviewing the consequences; builds and plugins may depend on specific subdirectory permissions.

## Example 4: Reverse-proxy baseline (Nginx illustration)

This is a **starting illustration**, not a complete deployment-ready configuration. Adapt the host, TLS certificate, upstream address, headers, WebSocket behavior, and timeouts to your environment.

```nginx
server {
    listen 443 ssl;
    server_name jenkins.example.invalid;

    ssl_certificate     /etc/ssl/certs/jenkins.crt;
    ssl_certificate_key /etc/ssl/private/jenkins.key;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Also restrict direct network access to the Jenkins backend port. Follow Jenkins' reverse-proxy documentation for the exact deployment and WebSocket/agent requirements. Test login, redirects, webhook delivery, and CSRF-protected actions before rollout.

## Example 5: Check exposed listeners

```bash
sudo ss -lntp
```

Compare the output with an approved service inventory. The web UI, inbound agent listener, SSH server plugin, and other plugins may expose different ports. Disable or firewall any service that is not required, but verify agent connectivity before changing listener settings.

## Example 6: Safe plugin inventory process

1. Export or record the installed plugin list from the Jenkins UI or an approved administrative process.
2. Record plugin name, version, purpose, owner, and dependent jobs.
3. Compare installed versions with official security advisories and plugin documentation.
4. Remove unused plugins after testing dependencies.
5. Upgrade in staging and verify key pipelines before production rollout.

Avoid blind bulk upgrades on a production controller.

## Example 7: Separate agent trust pools

Use distinct labels and infrastructure for untrusted and privileged workloads:

```groovy
pipeline {
    agent { label 'untrusted-ci' }

    stages {
        stage('Validate Pull Request') {
            steps {
                sh './lint.sh'
                sh './test.sh'
            }
        }
    }
}
```

This example only selects a label. The real security boundary must be enforced by agent provisioning, operating-system permissions, network controls, credential scope, and Jenkins job authorization. Do not let an untrusted job choose a privileged agent label.

## Example 8: Hardening assessment script

The following Python script checks a supplied text file containing a *manually collected* assessment. It does not query Jenkins or make configuration changes.

```python
from pathlib import Path

required_checks = [
    "admin_access_reviewed",
    "https_configured",
    "csrf_protection_reviewed",
    "built_in_node_executors_zero",
    "agent_pools_separated",
    "plugins_reviewed",
    "credentials_scoped",
    "jenkins_home_protected",
    "backups_protected",
    "recovery_tested",
]

assessment = Path("hardening-status.txt").read_text(encoding="utf-8")
completed = set(
    line.strip()
    for line in assessment.splitlines()
    if line.strip() and not line.lstrip().startswith("#")
)

missing = [check for check in required_checks if check not in completed]

if missing:
    print("Checks requiring evidence:")
    for check in missing:
        print(f"- {check}")
    raise SystemExit(1)

print("All listed checks have a recorded status entry.")
```

For this simple script, each line in `hardening-status.txt` should contain a check identifier. A recorded identifier means only that a status entry exists, not that the control is actually effective. Store evidence and outcome separately for a real audit.

## Example 9: Example hardening-status.txt

```text
admin_access_reviewed
https_configured
csrf_protection_reviewed
built_in_node_executors_zero
agent_pools_separated
plugins_reviewed
credentials_scoped
jenkins_home_protected
backups_protected
recovery_tested
```

Use evidence links, dates, owners, and results in your real assessment record. Do not treat this demonstration list as proof of compliance.

## Review checklist

- [ ] No unnecessary public or internal listener exposure
- [ ] HTTPS and reverse-proxy behavior verified
- [ ] Built-in node is not used for builds
- [ ] Agent trust boundaries are enforced outside the Jenkinsfile
- [ ] Plugin updates are staged and reviewed
- [ ] Credentials and controller files are protected
- [ ] Recovery has been tested
