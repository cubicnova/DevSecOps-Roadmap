# Solutions — Environment Promotion

These are model answers. Adapt the details to your application, infrastructure, compliance requirements, and deployment platform.

## Solution 1 — Example environment matrix

| Environment | Purpose | Data | Identity | Promotion gate |
|---|---|---|---|---|
| Development | Rapid integration | Synthetic or non-sensitive test data | Developer/development identity | Basic tests pass |
| Test / QA | Regression and integration | Approved test dataset | Test-only identity | Required test suite passes |
| Staging | Production-like rehearsal | Synthetic or approved masked data | Staging-only identity | Smoke, readiness, and security checks pass |
| Production | Serve users | Authorized production data | Restricted production deploy identity | Required approval and release policy pass |

Keep secrets separate by environment. Use production-like settings in staging where practical without exposing sensitive data.

## Solution 2 — Build, deployment, and release

1. **Compile from a commit:** Build.
2. **Upload an image to a registry:** Artifact publication.
3. **Install image in staging:** Deployment.
4. **Enable feature for all users:** Release/feature exposure.
5. **Deploy with feature flag disabled:** Deployment without full feature release.
6. **Move approved digest from staging to production:** Artifact promotion followed by production deployment.

In practice, a release may involve multiple deployments, feature flags, and traffic changes.

## Solution 3 — Example promotion gate

```text
PROMOTE_TO_PRODUCTION only if:
  required automated tests passed
  AND security policy passed or a valid exception exists
  AND artifact digest equals the approved staging digest
  AND staging smoke tests passed
  AND production configuration validation passed
  AND rollback artifact is available
  AND required approval is recorded
```

For exceptions, record the finding, rationale, risk owner, compensating controls, expiry, and remediation task. Do not permit a missing or mismatched artifact digest.

## Solution 4 — GitHub Actions environments

Expected steps:

1. Create environments through repository **Settings → Environments**.
2. Set branch/tag restrictions for each environment.
3. Configure production required reviewers if supported by the repository plan and visibility.
4. Reference the exact environment name in a workflow job:

```yaml
jobs:
  deploy_staging:
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: echo "Staging placeholder"

  deploy_production:
    needs: deploy_staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - run: echo "Production placeholder"
```

The `echo` commands only demonstrate workflow structure; they do not deploy an application. The `needs` dependency ensures the production job waits for the staging job to succeed. Configured environment protection rules must be set in repository settings. Some protection features are plan- and visibility-dependent, so check the official GitHub documentation for your repository.

## Solution 5 — Promotion workflow

A valid test should demonstrate:

- Validation happens before staging.
- Staging checks are required for production to proceed.
- A failed staging job blocks the dependent production job.
- If configured, the production environment pauses for approval.
- A real deployment uses the same artifact digest validated in staging.

A placeholder workflow that only prints messages is not evidence of an actual deployment. Clearly distinguish structural tests from end-to-end deployment tests.

## Solution 6 — Build once, promote many

1. Build the application from a reviewed source commit.
2. Publish the artifact to a controlled registry.
3. Record the immutable digest and source commit.
4. Deploy the exact digest to staging.
5. Run tests and save results linked to the digest.
6. Require production approval according to policy.
7. Deploy the same digest to production.
8. Verify health and record the result.

Configuration that may differ includes service endpoints, resource sizing, feature settings, and environment-specific secrets. Avoid rebuilding application code just to change environment settings when runtime configuration is appropriate.

## Solution 7 — Example configuration matrix

| Setting | Development | Staging | Production | Classification |
|---|---|---|---|---|
| API endpoint | Dev endpoint | Staging endpoint | Production endpoint | Non-secret, environment-specific |
| Database endpoint | Dev DB | Staging DB | Production DB | Environment-specific |
| Database credential | Dev-only | Staging-only | Production-only | Secret |
| Debug mode | Local-only if needed | Off | Off | Restricted configuration |
| Logging | Developer-friendly | Release diagnostics | Centralized operational logs | Environment-specific |
| Feature flags | Test values | Release rehearsal | Controlled rollout | Configuration |
| Cloud identity | Dev role | Staging role | Production deploy/runtime role | Restricted identity |
| Alert destinations | Dev channel | Release channel | On-call / incident channel | Operational configuration |
| Test data | Synthetic | Approved synthetic/masked | Authorized live data | Data policy |

Never use the same high-privilege credential in all environments.

## Solution 8 — Approval model

A reasonable model separates code review, automated quality checks, production approval, and deployment execution. A release manager or authorized service owner approves the release after reviewing test evidence, security status, change information, and rollback readiness. The deployment job uses a restricted identity and records its actions.

Emergency releases should have a documented expedited path, an authorized decision-maker, an audit record, and a post-release review. Human approval is not a replacement for automated tests because reviewers cannot reliably repeat every functional and security check manually.

## Solution 9 — Rollback plan

1. Monitor error rate, latency, availability, and critical business indicators.
2. Define a threshold and observation window before release.
3. Alert the on-call owner and pause further rollout when the threshold is breached.
4. Identify the previous known-good artifact by immutable digest.
5. Revert traffic or redeploy the known-good artifact through the established deployment mechanism.
6. Check whether database changes are backward-compatible. Do not assume a code rollback reverses a schema or data migration.
7. Verify service health and key workflows.
8. Preserve release IDs, digests, metrics, logs, approvals, and timestamps.
9. Communicate recovery and create follow-up actions.

## Solution 10 — Risks and mitigations

| Risk | Mitigation |
|---|---|
| Production rebuilt separately | Promote the exact staging-tested artifact digest. |
| Shared administrator credential | Use separate least-privilege identities per environment. |
| Unapproved production customer data in staging | Use synthetic or approved masked data; enforce data access controls. |
| No production approval | Configure a protected production environment or equivalent release gate. |
| Mutable release tag | Enforce tag immutability where possible and record/verify the digest. |
| No post-deployment health check | Add smoke tests and monitored health criteria. |
| Previous artifact deleted immediately | Retain rollback artifacts for the required support and recovery window. |
| Unclear release traceability | Record commit, artifact digest, test results, approval, and deployment result. |

## Solution 11 — Sample release record

```yaml
release:
  application: sample-api
  source_commit: "abc123def456"
  artifact: "registry.example.com/team/sample-api"
  digest: "sha256:<actual-digest>"
  staging:
    result: "passed"
    smoke_tests: "passed"
    security_gate: "passed"
  approval:
    decision: "approved"
    reviewer: "<authorized-reviewer>"
    change_reference: "<ticket-id>"
  production:
    deployment_result: "success"
    health_check: "passed"
  rollback:
    previous_digest: "sha256:<previous-known-good-digest>"
```

The digest values and reviewer/ticket fields are placeholders. Replace them with real traceable values in your release system. Never store credentials in this record.

## Solution 12 — Mini-project acceptance criteria

A strong solution should demonstrate:

- A clear environment diagram and ownership model.
- Explicit quality and security gates.
- One immutable artifact promoted through the pipeline.
- Secure, environment-scoped configuration and secrets.
- Branch restrictions and production approval where required.
- Health checks after deployment.
- A tested rollback process that considers database compatibility.
- A release record that links source, artifact digest, validation, approval, and deployment result.

## Final review checklist

- [ ] Build, deployment, and release are distinguished.
- [ ] Staging and production use the same artifact digest.
- [ ] Environment secrets and identities are isolated.
- [ ] Approval and policy gates are documented.
- [ ] Deployment concurrency and failure behavior are considered.
- [ ] Rollback artifacts and database compatibility are addressed.
- [ ] Release evidence is retained for investigation and audit.
