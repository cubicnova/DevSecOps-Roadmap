# Secure Configuration — Examples

These examples are educational starting points. Adapt them to the application's architecture, threat model, and supported platform versions; validate settings in a test environment before production use.

## 1. Application configuration

### Risky example

```python
# Insecure: do not use these settings in production.
DEBUG = True
SECRET_KEY = "development-secret-change-me"
ALLOWED_HOSTS = ["*"]
```

### Safer pattern

```python
import os

DEBUG = os.environ.get("APP_DEBUG", "false").lower() == "true"
SECRET_KEY = os.environ["APP_SECRET_KEY"]  # inject from a secret store
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ["APP_ALLOWED_HOSTS"].split(",")
    if host.strip()
]
```

Notes:
- Production deployment should explicitly set `APP_DEBUG=false`.
- The secret must be generated securely and provided through a protected runtime mechanism.
- Validate allowed hosts against a known list; do not use `*` as a shortcut.
- Avoid printing environment variables during troubleshooting.

## 2. Safe environment template

Use a template containing placeholders, not real credentials:

```dotenv
APP_ENV=development
APP_DEBUG=false
APP_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_HOST=localhost
DATABASE_NAME=app_db
DATABASE_USER=app_runtime
# Supply DATABASE_PASSWORD via a secret manager or protected runtime injection.
# Do not commit a real password or private key.
```

A `.env.example` file may be committed if it contains only non-sensitive examples. Add actual local secret files to `.gitignore`, and ensure production secrets are not stored in the repository.

## 3. Container hardening

### Risky Dockerfile pattern

```dockerfile
FROM example/app:latest
ENV DATABASE_PASSWORD=real-password
USER root
```

### Safer illustrative pattern

```dockerfile
FROM example/app:1.2.3
WORKDIR /app
COPY --chown=appuser:appgroup . /app
USER appuser
```

The base image and version above are illustrative. Prefer trusted images, verify provenance where available, scan dependencies, and use an approved immutable digest in production. Inject secrets at runtime rather than baking them into an image. Do not enable privileged mode or add capabilities unless a documented requirement exists.

## 4. Nginx security headers

Illustrative configuration; confirm compatibility with the application and avoid duplicating headers in multiple layers.

```nginx
server {
    listen 443 ssl;
    server_name app.example.test;

    # TLS certificate/key configuration is managed separately.
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header X-Frame-Options "DENY" always;

    location / {
        proxy_pass http://application_upstream;
    }
}
```

A Content Security Policy should be tailored to actual application resources and tested before enforcement. Use HSTS only when HTTPS is correctly deployed for the domain and its subdomains as intended. Security headers do not replace authorization or output encoding.

## 5. Least-privilege network policy

Example intent (not a directly deployable cloud policy):
- Internet → load balancer: TCP 443 only.
- Load balancer → web tier: only the application's required port.
- Web tier → database: only the database port and only from the web-tier identity/network.
- Administration: private network or approved identity-aware access path.
- Default inbound: deny.
- Egress: restrict where feasible; document necessary destinations.

Avoid exposing database ports, metrics endpoints, debug consoles, or management APIs directly to the public internet.

## 6. File permissions

For a Linux service, illustrative commands might be:

```bash
# Make a configuration file readable only by its owner and designated group.
sudo chown root:appgroup /etc/example-app/app.conf
sudo chmod 0640 /etc/example-app/app.conf

# Inspect permissions and ownership.
stat -c '%A %U:%G %n' /etc/example-app/app.conf
```

Use the actual service group and platform-specific conventions. Do not blindly apply recursive permission changes to system directories.

## 7. Secure configuration review snippet

```python
def review_config(config):
    findings = []

    if config.get("debug") is True:
        findings.append("High: debug mode is enabled")

    if "*" in config.get("allowed_hosts", []):
        findings.append("High: wildcard host allowlist")

    if config.get("admin_publicly_accessible") is True:
        findings.append("High: administrative interface is public")

    if config.get("tls_min_version") in {"TLSv1", "TLSv1.1"}:
        findings.append("High: obsolete TLS minimum version")

    if config.get("secrets_committed") is True:
        findings.append("Critical: secret material is committed to source control")

    return findings
```

This is a simple teaching example, not a complete scanner. Real configuration review needs schema validation, context-aware checks, and confirmation of effective runtime settings.
