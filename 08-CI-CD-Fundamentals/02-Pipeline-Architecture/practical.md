# Practical Exercises — Pipeline Architecture

**Level:** Beginner to intermediate  
**Environment:** A test Git repository; GitHub Actions is optional for exercises 1–5.  
**Safety:** Use a repository you control. Do not test production deployment or use real secrets in practice exercises.

## Exercise 1 — Draw a basic pipeline

**Task:** Draw a pipeline for a small Python web application. Include at least:

- Source / pull request
- Lint
- Unit tests
- Build/package
- Security checks
- Artifact publication
- Staging deployment
- Smoke tests
- Production approval
- Production deployment and health verification

**Deliverables:** A Mermaid diagram or image and a short explanation of why the stages are ordered this way.

**Acceptance criteria:** The production deployment cannot run before all required checks and approval.

## Exercise 2 — Identify pipeline components

For each item, label it as a **stage**, **job**, **step**, **runner**, **artifact**, **cache**, **environment**, or **quality gate**. Some items may fit more than one description; explain your choice.

1. A Linux VM that executes a workflow.
2. A command that runs `pytest`.
3. A compressed application package retained after the run.
4. A rule requiring tests to pass before merging.
5. A staging server group.
6. A job that scans dependencies.
7. Downloaded package data reused to speed up the next run.
8. The logical “Test” phase containing multiple jobs.

## Exercise 3 — Create a basic GitHub Actions CI workflow

**Task:** Create `.github/workflows/ci.yml` that:

1. Runs on pull requests and pushes to `main`.
2. Checks out the source.
3. Uses Python 3.12.
4. Installs `pytest`.
5. Runs tests.
6. Uses the minimum repository permissions needed for the workflow.

**Test:** Introduce a deliberately failing test in a branch and confirm the workflow fails. Remove or fix the test afterward.

**Deliverable:** Workflow file and a screenshot or notes showing one passing and one failing run.

## Exercise 4 — Add job dependencies

**Task:** Create three jobs named `lint`, `test`, and `package`. Run lint and test independently. Make package depend on both.

**Questions:**

- What happens if `lint` fails?
- What happens if `test` fails?
- Why is an explicit dependency better than assuming jobs run in the written order?

## Exercise 5 — Add a security gate

**Task:** Propose where to add these checks and what each should block:

- Secret scanning
- Static application security testing (SAST)
- Software composition analysis (SCA)
- Infrastructure-as-code scanning
- Container image scanning

**Deliverable:** A table with columns `Check`, `Pipeline stage`, `Blocking condition`, and `Exception owner`.

Use a documented threshold rather than treating every informational finding as equally severe.

## Exercise 6 — Design artifact promotion

**Scenario:** Your application is built and tested in CI. The team currently rebuilds it separately for staging and production.

**Task:** Redesign the flow to build once and promote the same artifact.

Include:

- Artifact naming/versioning
- Checksum or digest
- Artifact repository
- Staging validation
- Production release gate
- Audit trail

**Question:** Why can rebuilding independently for production invalidate confidence in the staging test?

## Exercise 7 — Calculate pipeline duration

Tasks and durations:

| Task | Duration |
|---|---:|
| Lint | 2 minutes |
| Unit tests | 5 minutes |
| Secret scan | 3 minutes |
| Package | 2 minutes |
| Staging smoke test | 4 minutes |

Assume lint, unit tests, and secret scan can run in parallel. Package waits for all three, and smoke tests run after packaging and staging deployment. Ignore deployment and runner queue time.

**Task:** Calculate the total time for:
1. Sequential execution of all five tasks.
2. Parallel first three tasks, then package, then smoke test.

Show your working.

## Exercise 8 — Choose a deployment strategy

Choose rolling, blue/green, canary, or feature flags for each scenario. Explain trade-offs.

1. A low-risk internal service with several identical instances.
2. A high-traffic public service where the team wants to observe a small share of users before full release.
3. A service requiring a fast traffic switch back to the previous version.
4. A feature that should be deployed now but enabled for only selected users next week.

## Exercise 9 — Plan rollback

**Scenario:** A new release passes CI and staging tests, but production error rates increase after deployment.

**Task:** Write a rollback plan containing:

- Detection signal and threshold
- Who or what makes the rollback decision
- Previous known-good artifact/version
- How traffic or deployment is reverted
- Database migration considerations
- Communication and audit steps
- Post-incident follow-up

**Acceptance criteria:** The plan does not assume that rolling back application code automatically reverses a destructive database migration.

## Exercise 10 — Pipeline threat review

Review a hypothetical pipeline with these properties:

- All jobs use a shared administrator credential.
- Pull requests from forks run on a persistent self-hosted runner.
- Any developer can edit the production workflow.
- The build job has production deployment credentials.
- Third-party actions are referenced by mutable tags.
- Artifacts are rebuilt for each environment.
- Logs are deleted immediately after successful deployment.

**Task:** Identify at least six risks and propose one mitigation for each.

## Exercise 11 — Review a failed pipeline

**Task:** Create a failure matrix with at least five failure points. For each, record:

- Expected pipeline status
- Whether later jobs should run
- Evidence to retain
- Person/team responsible
- Recovery action

Include a failed test, a detected secret, a staging smoke-test failure, and a production health-check failure.

## Exercise 12 — Mini project

Design a secure CI/CD architecture for a sample Flask API or static website.

**Required outputs:**

- `pipeline-design.md` with a diagram and stage descriptions
- CI workflow file
- Quality-gate policy
- Artifact promotion plan
- Failure and rollback matrix
- Short security threat review

**Evaluation rubric (100 points):**

| Area | Points |
|---|---:|
| Correct pipeline stages and dependencies | 20 |
| Testing and security gates | 20 |
| Artifact integrity and promotion | 15 |
| Least privilege and secret handling | 15 |
| Environment protection and release approval | 10 |
| Failure handling and rollback | 15 |
| Documentation clarity | 5 |

## Submission checklist

- [ ] All required deliverables are included.
- [ ] Pipeline stages and dependencies are explicit.
- [ ] At least one failure path was tested.
- [ ] Secrets and credentials are not committed.
- [ ] Security gates have clear thresholds and owners.
- [ ] The same artifact is promoted between environments.
- [ ] Rollback limitations are documented.
