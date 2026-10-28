# Deployment Strategies — Practical Exercises

Perform these exercises in a local lab or a non-production test repository. Do not change live traffic or deploy to production as part of this module.

## Lab setup

Requirements: Python 3.10+ and Git. For the optional workflow exercise, use a personal GitHub repository.

Create a folder and add `blue_green.py`, `test_blue_green.py`, and `canary.py` from `examples.md`.

## Exercises

### Exercise 1 — Compare strategies
Compare recreate, rolling, blue-green, canary, and feature flags by downtime, infrastructure cost, operational complexity, and rollback method.

**Deliverable:** A comparison table and a recommendation for a small internal web application.

### Exercise 2 — Run the blue-green simulation
Run:

```bash
python blue_green.py
```

**Deliverable:** Explain which environment receives traffic and why.

### Exercise 3 — Test health-gated switching
Run:

```bash
python -m unittest -v
```

Then set the candidate environment's `healthy` value to `False` and verify that the simulation refuses to switch.

**Deliverable:** Test output and a short explanation of the health gate.

### Exercise 4 — Implement a rollback decision
Extend the simulation so a failed health check keeps the original environment active.

**Deliverable:** A function or pseudocode that never switches traffic to an unhealthy candidate.

### Exercise 5 — Simulate a canary gate
Run `canary.py` with an error rate below and above the configured threshold.

**Deliverable:** Explain what action the pipeline should take for each result.

### Exercise 6 — Design a metric policy
Choose at least three signals for a canary rollout, such as error rate, latency, and a business-critical success rate.

**Deliverable:** Define thresholds, an observation window, and what happens if any threshold fails. Use illustrative values only and explain that real thresholds must come from service objectives.

### Exercise 7 — Add a deployment environment
Add the workflow template from `examples.md` to `.github/workflows/deploy.yml` in a test repository. Configure a `production` environment with a required reviewer, but keep the deployment command as a harmless placeholder.

**Deliverable:** Demonstrate the workflow's test job and describe how the environment gate behaves.

### Exercise 8 — Immutable artifact promotion
Design a pipeline that builds an artifact once, deploys it to staging, then promotes that same artifact to production.

**Deliverable:** Describe how the artifact is identified by version, commit SHA, and digest.

### Exercise 9 — Database compatibility review
A release adds a database column and the new application version uses it immediately.

**Deliverable:** Explain why rolling deployment can fail while old instances still run. Propose an expand-and-contract migration plan.

### Exercise 10 — Deployment security review
A workflow exposes a cloud administrator key to every job.

**Deliverable:** Identify the risks and propose least-privilege, short-lived credentials, environment protection, and secret-handling controls.

### Exercise 11 — Rollback runbook
Write a rollback runbook for a web application release.

**Deliverable:** Include the trigger, authorized owner, traffic/version rollback action, post-rollback checks, communication, and incident record.

### Exercise 12 — Choose a strategy by scenario
Recommend a strategy for each scenario and justify your choice:
- A low-traffic internal tool where brief downtime is acceptable.
- A high-availability API with a load balancer and compatible versions.
- A large public service that needs gradual user exposure.
- A release where a feature must be disabled without redeploying code.

**Deliverable:** Four recommendations with risks and mitigations.

## Stretch challenges

- Extend the canary simulation to accept multiple metrics and stop if any critical gate fails.
- Add a staged rollout plan such as 5%, 25%, 50%, and 100% traffic.
- Document when to pause for human review versus automatically roll back.
- Add release metadata to a JSON file: version, commit SHA, artifact digest, and deployment time.
- Research your target platform's rollout and rollback features.

## Submission checklist

- [ ] Strategy comparison completed.
- [ ] Blue-green tests pass.
- [ ] Canary gate behavior demonstrated.
- [ ] Rollout metrics and thresholds documented.
- [ ] Deployment access is least-privilege.
- [ ] Artifact promotion and traceability are documented.
- [ ] Database compatibility and rollback risks are addressed.
