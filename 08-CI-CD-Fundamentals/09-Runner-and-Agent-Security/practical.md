# Runner and Agent Security — Practical Exercises

Complete these exercises in a personal test repository or a local lab. Do not attempt to compromise shared runners, access real credentials, or run untrusted code on a production-connected host.

## Lab setup

Requirements: Python 3.10+, Git, and GitHub for the optional workflow exercise.

Create `runner_risk.py` and `test_runner_risk.py` using `examples.md`.

## Exercises

### Exercise 1 — Runner inventory
Compare hosted, self-hosted, persistent, and ephemeral runners.

**Deliverable:** A table listing ownership, isolation assumptions, maintenance tasks, and suitable use cases.

### Exercise 2 — Run the risk model
Run:

```bash
python runner_risk.py
python -m unittest -v
```

**Deliverable:** Record the risks detected and explain why the script is only a teaching model.

### Exercise 3 — Analyze untrusted pull requests
A workflow runs tests from a fork on a self-hosted runner that can access internal services.

**Deliverable:** Identify at least four risks and propose mitigations.

### Exercise 4 — Least privilege
Review a workflow with broad token permissions.

**Deliverable:** Rewrite its permissions to the minimum needed for checkout and tests, and explain why deployment permissions do not belong in the validation job.

### Exercise 5 — Isolate release jobs
Design a separate release workflow that runs only from a protected branch or approved release event and references a protected environment.

**Deliverable:** A diagram showing trusted source, approval, runner, credential, and target-environment boundaries. Keep deployment commands as placeholders.

### Exercise 6 — Persistent runner cleanup
List files and resources that could survive a job: workspaces, processes, Docker images, credentials, temporary files, caches, and modified tools.

**Deliverable:** A cleanup and reimaging policy. Explain why a fresh ephemeral runner is generally safer than relying on cleanup alone for untrusted workloads.

### Exercise 7 — Network boundaries
A runner can access the internet, internal databases, cloud metadata, and a deployment control plane.

**Deliverable:** Propose an allow-list or segmentation policy that limits access to the minimum required endpoints.

### Exercise 8 — Supply-chain risk
A pipeline installs dependencies and third-party actions.

**Deliverable:** Describe version pinning, lockfiles, action review, trusted registries, checksum/signature verification where supported, and artifact provenance.

### Exercise 9 — Secret exposure tabletop
A test log accidentally prints a deployment token.

**Deliverable:** Write the first five response steps, including revocation/rotation, log review, affected-system assessment, and evidence preservation.

### Exercise 10 — Runner incident response
Assume a self-hosted runner may have been compromised.

**Deliverable:** Create a response runbook covering isolation, credential rotation, evidence preservation, artifact validation, rebuild, and recovery approval.

### Exercise 11 — Cache poisoning review
Explain how an untrusted workflow could create cache content later consumed by a privileged build.

**Deliverable:** Propose cache key separation by trust level, restricted cache use, and a policy that prevents untrusted output from being trusted automatically.

### Exercise 12 — Runner policy review
Use the example `runner_policy` in `examples.md`.

**Deliverable:** Convert it into a human-readable policy with an owner, scope, enforcement method, and review frequency.

## Stretch challenges

- Add a test case for every risk combination in `assess_runner()`.
- Add a CI job that runs the risk-model tests with read-only repository permissions.
- Design a runner group strategy separating public pull requests, internal CI, and privileged release jobs.
- Document patch cadence and how runner images are rebuilt.
- Define log retention and artifact retention without collecting unnecessary sensitive data.

## Submission checklist

- [ ] Runner types and trust boundaries documented.
- [ ] Risk model and tests run locally.
- [ ] Untrusted code is isolated from secrets and private networks.
- [ ] Workflow permissions are minimal.
- [ ] Runner lifecycle and patching policy documented.
- [ ] Supply-chain and cache risks addressed.
- [ ] Incident response and credential rotation steps documented.
