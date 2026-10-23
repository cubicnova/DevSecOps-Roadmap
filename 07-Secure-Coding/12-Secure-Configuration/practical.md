# Secure Configuration — Practical Labs

## Lab 1: Review an application configuration

### Scenario

You receive this fictional configuration:

```yaml
environment: production
debug: true
allowed_hosts:
  - "*"
cors:
  allow_credentials: true
  allowed_origins:
    - "*"
session:
  secure_cookie: false
  http_only: false
  same_site: "None"
admin:
  public_access: true
logging:
  include_request_headers: true
```

### Tasks

1. Identify at least seven security concerns.
2. Rate each finding by severity and explain the exposure.
3. Propose a safer setting for each item.
4. Identify which changes require functional testing.
5. Draft a short change and rollback plan.

### Deliverable

Create `lab1-findings.md` with columns for setting, risk, recommended fix, validation, and owner.

## Lab 2: Secrets in source control

### Tasks

1. Create a disposable local Git repository.
2. Add a file containing a clearly fake value such as `EXAMPLE_PASSWORD=not-a-real-secret`.
3. Demonstrate why `.gitignore` alone does not remove a file already tracked by Git.
4. Move secret handling to a runtime-injected value or local ignored file.
5. Remove the tracked sample from the index and confirm the intended file is no longer tracked.
6. Explain why any real credential that was committed must be rotated, even after deleting the file.

Useful commands:

```bash
git status --short
git ls-files
git check-ignore -v .env
```

Do not put real credentials in this lab. Do not push test secrets to a public remote.

## Lab 3: Container review

Review a sample Dockerfile and deployment manifest. Check:
- Is the process running as root?
- Are secrets included in `ENV`, `ARG`, copied files, or build output?
- Is privileged mode enabled?
- Are Linux capabilities broader than required?
- Is the root filesystem writable unnecessarily?
- Are image references mutable or unverified?
- Are host paths mounted unnecessarily?
- Are resource limits configured?
- Is the container exposed through an unnecessary host port?

Write at least five findings and validate each proposed correction using a local test container.

## Lab 4: Linux host baseline

On a disposable Linux VM you administer:

1. Inventory listening sockets with `ss -lntup`.
2. Review enabled services using the platform's service manager.
3. Identify unused services and confirm with the owner before disabling anything.
4. Review local accounts, privileged groups, and SSH settings.
5. Check permissions on application configuration and private-key files.
6. Record the before/after state and rollback commands.

Do not disable services on a production host or alter remote SSH settings without a tested recovery path.

## Lab 5: Network exposure review

Draw a simple three-tier architecture: load balancer, application, and database.

1. List required inbound and outbound flows.
2. Write a default-deny policy.
3. Restrict database access to the application tier.
4. Keep administrative endpoints private.
5. Add an owner and business justification for each exception.
6. Test allowed and denied paths in an authorized lab.

## Lab 6: Configuration drift

Create a baseline table with expected values, actual values, evidence, and remediation. Simulate one harmless deviation in a disposable environment. Explain how a scheduled scan, configuration management tool, or cloud policy could detect the drift.

## Lab 7: Secure change review

For a proposed configuration change, write:
- Purpose and scope
- Security impact
- Dependencies and compatibility checks
- Reviewer and approver
- Test evidence
- Deployment window
- Rollback trigger and procedure
- Post-deployment validation
- Exception expiry date, if applicable

## Submission checklist

- [ ] No real secrets in source, logs, or images.
- [ ] Production debug features disabled.
- [ ] Unnecessary services and ports identified.
- [ ] Privileged access is scoped and attributable.
- [ ] Network paths follow least privilege.
- [ ] TLS and security headers are appropriate to the deployment.
- [ ] Configuration changes are reviewed and reproducible.
- [ ] Runtime behavior is tested after deployment.
- [ ] Findings include evidence, owner, severity, and remediation.
