# DAST CI/CD Pipeline Security Checklist

## Target environment
- [ ] Target is owned or explicitly authorized
- [ ] Preview/staging environment is isolated
- [ ] Synthetic data and dedicated test identities are used
- [ ] Exact host/path scope is documented
- [ ] Destructive routes and external integrations are controlled

## Workflow security
- [ ] CI permissions are least privilege
- [ ] Secrets are unavailable to untrusted fork pull requests
- [ ] Third-party actions are reviewed and pinned to immutable SHAs
- [ ] Scanner images are pinned to reviewed versions/digests
- [ ] Runner isolation and Docker privileges reviewed
- [ ] No public/untrusted access to ZAP API

## Scan execution
- [ ] Application readiness is verified
- [ ] Baseline and active profiles are separate
- [ ] Scan duration and request volume are bounded
- [ ] Authentication is verified when needed
- [ ] Scanner errors are not treated as a clean result

## Reports and cleanup
- [ ] Reports are access-controlled
- [ ] Artifact retention is appropriate
- [ ] Reports/logs do not expose secrets
- [ ] Gate policy is documented and reviewed
- [ ] Cleanup runs after success and failure
- [ ] Temporary credentials are revoked
- [ ] Ephemeral environment is removed
