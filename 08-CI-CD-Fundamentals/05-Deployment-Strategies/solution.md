# Deployment Strategies — Suggested Solutions

These are reference answers. Actual deployment decisions depend on availability objectives, architecture, platform capabilities, and risk tolerance.

## Solution 1 — Compare strategies

| Strategy | Suitable when | Main risk | Mitigation |
|---|---|---|---|
| Recreate | Downtime is acceptable | Service interruption | Maintenance window and tested recovery |
| Rolling | Instances can coexist across versions | Version incompatibility or reduced capacity | Backward compatibility, readiness checks, rollout limits |
| Blue-green | Fast traffic switch and rollback are valuable | Higher capacity cost; data changes may not roll back | Validate inactive environment and keep schema compatible |
| Canary | Gradual exposure and metric-based decisions are possible | Poor signals may miss regressions | Compare baseline, set observation windows, use multiple metrics |
| Feature flags | Release timing should be separate from deployment | Stale flags or incorrect targeting | Access controls, audits, expiry/removal plan |

For a small internal application, recreate may be adequate if a maintenance window is acceptable. Rolling may be a better default if uptime matters and the app supports mixed versions.

## Solution 2 — Blue-green simulation

The script begins with blue active and green as the candidate. If green is healthy, the simulated traffic switch returns `green`. This is application logic only; no real load balancer or infrastructure is changed.

## Solution 3 — Health-gated switching

The unit tests verify that a healthy target can be selected and that an unhealthy target raises `RuntimeError`. If the candidate is unhealthy, the calling release process should retain the old active environment, stop rollout, and investigate.

## Solution 4 — Rollback decision

One possible design:

```python
def release(active_environment, candidate_environment):
    if not candidate_environment.healthy:
        return active_environment.name
    return candidate_environment.name
```

In a real system, health should come from actual readiness checks and service metrics, not a hard-coded Boolean. Switching traffic back is safe only if the previous application version remains compatible with current data and dependencies.

## Solution 5 — Canary gate

The sample function returns `True` when the observed error rate is at or below the configured maximum and `False` when it is above. For a failed gate, pause traffic expansion and investigate; roll back when the predefined policy says the regression is release-related or service health is unacceptable.

## Solution 6 — Example metric policy

Illustrative policy only:

- Error rate: pause if it rises materially above the baseline or breaches the service's error budget.
- Latency: pause if p95 latency exceeds the service objective for a sustained observation window.
- Business success rate: stop if critical transactions decline beyond an agreed tolerance.
- Resource saturation: pause expansion if CPU, memory, or connection pools approach unsafe limits.

Choose thresholds from historical data and service-level objectives. Avoid relying on a single metric or on very low traffic counts that make the percentage unstable.

## Solution 7 — Deployment environment

Store the workflow at `.github/workflows/deploy.yml` and configure a `production` environment with required reviewers and suitable restrictions. The example deploy job runs only for a manual dispatch on `main` and only after `test` succeeds. Its placeholder command does not deploy anything.

A real production workflow needs additional platform-specific controls and a genuine deployment command reviewed for safety. A manual trigger by itself is not authorization.

## Solution 8 — Immutable artifact promotion

A reliable sequence is:

1. Build once from a specific commit.
2. Record the commit SHA, version, build run ID, and artifact checksum or image digest.
3. Test the artifact and deploy it to staging.
4. Run smoke and integration tests.
5. Approve production release according to policy.
6. Promote the same artifact or image digest to production.
7. Record the release result and monitor health.

Do not rebuild separately from a moving branch for each environment, because the resulting bits may differ.

## Solution 9 — Database compatibility

During a rolling deployment, old and new application versions can run simultaneously. If the new version requires a column that old code cannot handle, requests may fail.

An expand-and-contract approach:

1. Add the new schema in a backward-compatible way.
2. Deploy code that can work with both old and new schema forms.
3. Backfill or migrate data safely.
4. Switch reads and writes to the new schema.
5. Wait until old application instances are retired.
6. Remove obsolete schema only in a later, separately verified change.

Back up important data and test restoration. Some migrations require roll-forward recovery rather than schema rollback.

## Solution 10 — Deployment security review

Risks include credential theft from logs or compromised dependencies, excessive permissions, and unintended production changes. Mitigations:

- Remove administrator credentials from general-purpose jobs.
- Use short-lived workload identity or narrowly scoped deployment credentials.
- Scope permissions to the required service and environment.
- Require protected branches and production approvals.
- Keep secrets out of source and logs.
- Separate untrusted pull-request workflows from privileged deployment jobs.
- Audit deployment activity and rotate any exposed credentials.

## Solution 11 — Rollback runbook

A useful runbook includes:

1. **Trigger:** predefined error, latency, health-check, or business metric breach.
2. **Owner:** named on-call role or authorized release operator.
3. **Action:** stop rollout and restore the prior known-good version or route traffic back.
4. **Data check:** verify schema and data compatibility before reverting.
5. **Verification:** run smoke tests and confirm service metrics recover.
6. **Communication:** notify stakeholders and incident responders.
7. **Record:** capture release ID, commit, artifact digest, timeline, symptoms, and outcome.
8. **Follow-up:** preserve evidence, investigate root cause, and update tests/runbooks.

## Solution 12 — Strategy by scenario

- **Internal tool with acceptable downtime:** recreate can be reasonable because it is simple and inexpensive. Use a maintenance window and tested recovery.
- **High-availability API with compatible versions:** rolling deployment can work well with readiness checks, capacity headroom, and controlled rollout limits.
- **Large public service requiring gradual exposure:** canary deployment allows staged traffic and metric-based promotion or rollback.
- **Feature can be disabled independently of code deployment:** feature flags provide a quick release control, with access controls and a cleanup policy.

## Stretch challenge guidance

- **Multiple canary metrics:** fail closed when a critical signal breaches its defined limit; handle missing telemetry explicitly.
- **Traffic steps:** define how long to observe each stage and which metrics authorize expansion.
- **Human review:** use for high-impact changes, uncertain telemetry, or policy-required approvals; automate clear, well-tested safety gates.
- **Release metadata:** record version, commit SHA, artifact digest, environment, timestamp, and outcome without storing secrets.
- **Platform research:** confirm exact behavior of rollout pauses, readiness probes, traffic shifting, and rollback for the chosen platform.

## Final review

A safe deployment strategy limits exposure, verifies real service health, protects production access, preserves artifact traceability, and provides a tested recovery path. No single strategy eliminates the need for monitoring, compatible data changes, and operational ownership.
