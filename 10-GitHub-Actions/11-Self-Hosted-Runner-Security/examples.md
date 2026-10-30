# Self-Hosted Runner Security - Examples

These examples illustrate secure configuration patterns. Adapt runner groups, labels, and host controls to your GitHub organization. Do not copy registration tokens or secrets into source files.

## 1. Target a restricted runner group

```yaml
name: Restricted CI Runner

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    runs-on:
      group: ci-low-privilege
      labels: [self-hosted, linux, x64]
    steps:
      - uses: actions/checkout@v4
      - name: Run build checks
        run: |
          id
          uname -a
          echo "Use this runner only for approved low-privilege tasks"
```

The runner group must exist and allow this repository. Labels select a runner within the accessible group; labels alone do not grant access.

## 2. Separate untrusted validation from deployment

```yaml
name: Trust-Separated Pipeline

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  pull-request-checks:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Run untrusted PR validation on a hosted runner"

  trusted-build:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on:
      group: trusted-build-runners
      labels: [self-hosted, linux]
    steps:
      - uses: actions/checkout@v4
      - run: echo "Run trusted-branch build tasks"
```

This is an illustrative separation. Configure group access so only intended repositories and workflows can use the trusted runner. Review every trigger and workflow modification.

## 3. Register a Linux runner as ephemeral

Run the following interactively on a dedicated runner host after downloading the runner application from GitHub and obtaining a registration token through GitHub's supported UI or API:

```bash
./config.sh \
  --url https://github.com/OWNER/REPOSITORY \
  --token "$RUNNER_REGISTRATION_TOKEN" \
  --ephemeral
```

The registration token is short-lived and sensitive. Retrieve it securely, avoid command-history persistence, and do not print it. After configuration, run the runner service using the supported installation procedure for your operating system.

## 4. Run the runner service under a dedicated account

Example Linux administrative outline:

```bash
# Create a dedicated system account
sudo useradd --system --create-home --shell /usr/sbin/nologin actions-runner

# Ensure the runner directory is owned by the dedicated account
sudo chown -R actions-runner:actions-runner /opt/actions-runner

# Review permissions
sudo find /opt/actions-runner -maxdepth 2 -type f -printf '%m %u:%g %p\n'
```

Adapt paths and service configuration to your installation. Do not recursively change permissions on unrelated system directories. The runner account should not have unrestricted sudo access.

## 5. Basic host audit

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "== Identity =="
id

echo "== OS =="
cat /etc/os-release

echo "== Listening sockets =="
ss -tulpen

echo "== Recent authentication events (system dependent) =="
if command -v journalctl >/dev/null 2>&1; then
  sudo journalctl -u ssh --since "24 hours ago" --no-pager || true
fi

echo "== Runner directory permissions =="
stat -c '%A %U:%G %n' /opt/actions-runner
```

This is an audit starting point, not a complete hardening script. Adapt service names and logging permissions to your Linux distribution.

## 6. Example firewall policy outline

Use your host firewall or cloud network controls to implement a deny-by-default inbound policy and narrowly allow required outbound destinations.

```text
Inbound:
  - Deny unsolicited inbound connections.
  - Permit administrative access only from a controlled management network.

Outbound:
  - Permit required GitHub Actions runner endpoints over HTTPS.
  - Permit explicitly required package registries and artifact services.
  - Deny access to production subnets unless the job has a documented need.
  - Block cloud metadata endpoints unless specifically required and protected.
```

GitHub endpoint requirements can change. Use current official networking documentation and validate rules before enforcing them.

## 7. Workflow with minimal token permissions

```yaml
name: Read-only Runner Task

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inspect:
    runs-on:
      group: ci-low-privilege
      labels: [self-hosted, linux]
    steps:
      - uses: actions/checkout@v4
      - name: Inspect source
        run: find . -maxdepth 2 -type f -print
```

Grant write permissions only to the specific job that requires them. Avoid exposing secrets to jobs that process untrusted content.

## 8. Cleanup and evidence preservation

```bash
#!/usr/bin/env bash
set -euo pipefail

# Stop the runner service using the service manager configured for this host.
# Forward required runner and OS logs to external storage before teardown.
# Destroy or re-image the disposable VM after the job.
echo "Confirm external log forwarding and host teardown in the infrastructure workflow."
```

Do not treat deleting the workspace as proof that a host is clean. A compromised process may have modified system files, services, users, or credentials.
