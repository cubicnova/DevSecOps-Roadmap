# 05 — Deployment Strategies

This module introduces common software deployment strategies, when to use them, how to reduce release risk, and how to incorporate deployment safety into a DevSecOps pipeline.

## Learning objectives

After completing this module, you should be able to:

- Explain rolling, blue-green, canary, recreate, and feature-flag deployments.
- Compare deployment approaches by risk, cost, complexity, and rollback speed.
- Describe health checks, smoke tests, observability, and rollback criteria.
- Explain how CI/CD artifacts should be promoted across environments.
- Identify security controls for deployment credentials, approvals, and pipeline permissions.
- Design a basic release plan with a safe recovery path.

## Prerequisites

- Familiarity with CI/CD pipelines and build/test stages.
- Basic understanding of application environments, load balancers, and monitoring.
- Basic Git and deployment terminology.

## 1. What is a deployment strategy?

A deployment strategy defines how a new software version is introduced into an environment and how traffic or users are moved to that version. The strategy affects downtime, release risk, infrastructure cost, operational complexity, and recovery options.

A deployment is not complete merely because a command succeeds. Teams should verify application health and business-critical behavior after the change.

## 2. Common deployment strategies

### Recreate deployment
Stop the old version, then start the new version.

- **Advantages:** simple and inexpensive.
- **Trade-offs:** may cause downtime; rollback requires redeploying the prior version.
- **Use when:** downtime is acceptable, or for non-critical environments.

### Rolling deployment
Gradually replace old instances with new ones.

- **Advantages:** often avoids full downtime and uses existing capacity.
- **Trade-offs:** old and new versions coexist temporarily; compatibility and capacity planning matter.
- **Use when:** the application supports mixed-version operation and the platform supports controlled rollouts.

### Blue-green deployment
Maintain two production-like environments. Deploy and verify the new version in the inactive environment, then switch traffic.

- **Advantages:** fast traffic switch and straightforward application rollback.
- **Trade-offs:** may require nearly double application capacity; database changes can complicate rollback.
- **Use when:** quick cutover and recovery justify the infrastructure cost.

### Canary deployment
Release the new version to a small portion of traffic or users first, then expand if metrics remain healthy.

- **Advantages:** limits initial exposure and supports real-world validation.
- **Trade-offs:** requires reliable routing, monitoring, and a meaningful comparison window.
- **Use when:** gradual exposure can reveal issues before a full rollout.

### Feature flags
Deploy code while keeping a feature disabled, then enable it for selected users or cohorts.

- **Advantages:** separates code deployment from feature release and enables controlled exposure.
- **Trade-offs:** stale flags increase complexity; flags must be access-controlled and eventually removed.
- **Use when:** feature exposure should be controlled independently of deployment.

Feature flags are a release-control technique and can be combined with rolling, blue-green, or canary deployments.

## 3. Comparison table

| Strategy | Downtime potential | Infrastructure cost | Rollback / recovery | Main concern |
|---|---|---|---|---|
| Recreate | High unless downtime is hidden | Low | Redeploy old version | Service interruption |
| Rolling | Low when configured well | Low to moderate | Roll back rollout or redeploy | Mixed-version compatibility |
| Blue-green | Low during traffic switch | Higher | Switch traffic back, if compatible | Environment and data compatibility |
| Canary | Usually low | Moderate; depends on routing and capacity | Stop rollout or shift traffic back | Detecting issues reliably |
| Feature flags | Deployment may be independent of release | Low to moderate | Disable the flag | Flag governance and hidden code paths |

These are general tendencies; actual behavior depends on the application, platform, data model, and configuration.

## 4. Release lifecycle

```text
Build immutable artifact
        |
        v
Run automated tests and security checks
        |
        v
Deploy to test / staging
        |
        v
Smoke tests + health checks
        |
        v
Choose rollout strategy
        |
        v
Monitor error rate, latency, saturation, and key workflows
        |
        +---- Healthy? ---- No ----> Stop rollout / rollback / incident response
        |
       Yes
        |
        v
Continue rollout and verify
        |
        v
Record release metadata and close deployment
```

## 5. Health checks and rollout gates

Useful checks may include:

- **Readiness:** can the instance safely receive traffic?
- **Liveness:** is the process running well enough to continue?
- **Smoke tests:** do critical paths work after deployment?
- **Service-level indicators:** error rate, latency, throughput, and resource saturation.
- **Business signals:** successful checkout, login, or other critical transaction rates.
- **Security signals:** unexpected authentication failures, authorization errors, or security alerts.

Define thresholds and observation windows before the rollout. Do not rely only on a successful deployment command.

## 6. Database and state considerations

Application rollback is not always equivalent to data rollback.

- Prefer backward-compatible, expand-and-contract schema changes.
- Add new fields or tables before relying on them; remove old structures only after old versions are retired.
- Back up important data and test restore procedures.
- Avoid destructive migrations during a release that may need rollback.
- Consider session, cache, queue, and API compatibility when old and new versions coexist.
- Use roll-forward recovery when reverting a schema or data change would be unsafe.

## 7. DevSecOps deployment controls

- Build once and promote the same immutable artifact across environments.
- Use short-lived credentials or workload identity where supported.
- Limit deployment permissions to the target environment and required actions.
- Protect production environments with branch protections and required approvals.
- Separate untrusted pull-request validation from privileged deployment jobs.
- Keep secrets out of source files, artifacts, and logs.
- Record who approved and deployed each version, the commit SHA, artifact digest, and outcome.
- Monitor deployments and define an incident owner and rollback authority.
- Test rollback and disaster-recovery procedures before an emergency.

## 8. Hands-on lab

The `examples.md` file provides a local simulation of blue-green and canary traffic selection, plus a GitHub Actions workflow outline with a protected deployment environment. It does not deploy to a real service or change live traffic.

For platform-specific details, consult the official documentation for your chosen deployment platform, such as [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) and [GitHub Actions deployment environments](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments).

## Module files

- `README.md` — strategy overview, comparisons, and deployment controls.
- `examples.md` — Python rollout simulation and CI/CD examples.
- `practical.md` — hands-on exercises.
- `solution.md` — suggested answers and design guidance.

## Completion checklist

- [ ] I can explain recreate, rolling, blue-green, canary, and feature flags.
- [ ] I can choose a strategy based on service requirements.
- [ ] I can define rollout health checks and rollback triggers.
- [ ] I understand why database changes complicate rollback.
- [ ] I can describe least-privilege deployment permissions.
- [ ] I can plan a release that uses an immutable, traceable artifact.
