# Secure Configuration — Suggested Solutions

These are sample answers, not universal settings. Confirm requirements with the system owner and test changes in a representative environment.

## Lab 1: Example findings

| Setting | Risk | Safer direction | Validation |
|---|---|---|---|
| `debug: true` | Detailed diagnostics may expose internals | Disable in production | Confirm generic client errors and protected server-side logs |
| `allowed_hosts: ["*"]` | Host-header abuse or routing confusion, depending on framework | Explicit approved hostnames | Test approved and unapproved host headers |
| CORS origin `*` with credentials | Invalid or unsafe cross-origin policy design; browsers reject wildcard credentialed access in standard CORS behavior, but policy intent is still flawed | Explicit trusted origins; only allow credentials when required | Test preflight and credentialed requests from trusted/untrusted origins |
| `secure_cookie: false` | Session cookie can be sent over HTTP | Set `Secure` when deployed over HTTPS | Inspect `Set-Cookie` and verify HTTP behavior |
| `http_only: false` | Client-side scripts can read the cookie | Set `HttpOnly` for session cookies | Inspect cookie attributes; test app behavior |
| `same_site: "None"` | Cross-site cookie sending may increase CSRF exposure; `None` requires `Secure` in modern browsers | Choose `Lax` or `Strict` where compatible; use CSRF defenses for required cross-site flows | Test sign-in, SSO, and state-changing requests |
| `admin.public_access: true` | Administrative surface exposed to broad attack traffic | Private access path, strong identity controls, MFA, audit logs | Verify public path is blocked and approved admin path works |
| Logging all request headers | Authorization tokens, cookies, or personal data may be captured | Allowlist safe fields and redact sensitive headers | Send a test token and verify it never appears in logs |

The final severity depends on exposure, business impact, compensating controls, and actual application behavior.

## Lab 2: Secrets and Git

- `.gitignore` prevents new untracked files matching a rule from being added by normal `git add`; it does not automatically untrack files already committed.
- Use `git rm --cached .env` to remove a tracked file from the index while leaving the local copy in place, then commit the removal.
- If a real secret was committed, revoke or rotate it immediately. Removing it from the latest commit does not erase it from previous commits, clones, caches, or logs.
- Keep a safe `.env.example` with placeholders and provide actual secrets through a secret manager or protected deployment mechanism.

## Lab 3: Container review

Potential improvements include:
- Run as a dedicated non-root user.
- Keep secrets out of build arguments, image layers, and environment baked into the image.
- Disable privileged mode and add only required capabilities.
- Use a read-only root filesystem where feasible.
- Pin image versions/digests and verify image provenance.
- Avoid unnecessary host mounts and published ports.
- Add CPU/memory limits and health checks where appropriate.
- Scan images and dependencies and rebuild from supported base images.

Validate the effective runtime configuration; a safer Dockerfile alone does not prove the deployed container is hardened.

## Lab 4: Linux host baseline

A good submission inventories listening ports and services before proposing changes. Confirm service ownership and dependencies before disabling services. For files, use narrow ownership and permission changes rather than broad recursive `chmod` commands. Keep a recovery path for remote access and verify SSH changes from a second session before ending the first.

## Lab 5: Network exposure

Example flow table:

| Source | Destination | Port/protocol | Decision | Reason |
|---|---|---|---|---|
| Internet | Load balancer | TCP 443 | Allow | Public HTTPS entry point |
| Load balancer | App tier | Required app port | Allow | Forward application traffic |
| App tier | Database | Required DB port | Allow | Application data access |
| Internet | Database | Any | Deny | No direct public database access |
| Internet | Admin interface | Any | Deny | Administration uses private access |
| Other internal networks | App/database | Unneeded ports | Deny | Limit lateral movement |

Use security groups, network policies, firewalls, or equivalent controls appropriate to the platform. Include egress requirements and monitoring in a real review.

## Lab 6: Configuration drift

A useful record includes the approved value, observed value, timestamp, source of evidence, impact, owner, due date, and remediation status. Drift detection should alert on meaningful deviations and route them to an owner; automated remediation should be used only when safe and tested.

## Lab 7: Secure change review

A complete change record defines the intended state, test cases, approval, deployment and rollback conditions, and post-deployment evidence. Exceptions should be risk-accepted by an authorized owner, have compensating controls, and expire or be reviewed on a defined date.
