# Practical Exercises: Sample CI/CD Pipelines

Use a personal or training repository. Do not test deployment workflows against production infrastructure.

## Lab 1: Map a pipeline

Draw a pipeline with these stages: checkout, lint, unit tests, build, artifact upload, approval, deployment, smoke test.

**Tasks**
1. Identify which stages can run in parallel.
2. Mark the stages that must block release.
3. Explain where the deployable artifact is created and stored.

**Deliverable:** a diagram and a short explanation.

## Lab 2: Create pull-request validation

Create a workflow that runs on pull requests targeting `main`.

**Requirements**
- Read-only repository permissions.
- A lint step and a unit-test step.
- Clear step names.
- Failed tests must fail the workflow.

**Deliverable:** `.github/workflows/ci.yml`.

## Lab 3: Add a build stage

Extend Lab 2 to produce an application artifact only after validation passes.

**Questions**
- What files should be included?
- How will you name the artifact?
- How will you prevent temporary files or secrets from entering it?

## Lab 4: Add an artifact checksum

Generate a SHA-256 checksum for the packaged artifact and explain how a recipient can verify it.

## Lab 5: Use a reusable workflow

Move the test steps into a reusable workflow using `workflow_call`.

**Tasks**
1. Define an optional input for the language version.
2. Call it from a separate workflow.
3. Keep permissions minimal.
4. Explain when a reusable workflow is preferable to a composite action.

## Lab 6: Add a quality gate

Create a release or publish job that depends on the test job.

**Acceptance criteria**
- The publish job depends on successful tests.
- It does not run after test failure.
- It does not receive write permissions unless publishing actually requires them.

## Lab 7: Protect staging deployment

Create a manually triggered staging workflow.

**Tasks**
1. Configure a `staging` environment.
2. Add required reviewers if supported by your repository plan.
3. Use an environment-scoped secret.
4. Explain how this differs from putting a secret at repository scope.

## Lab 8: Build once, promote many

Design a flow that builds an artifact once and promotes that exact artifact from test to staging to production.

**Deliverable:** a sequence diagram or written process showing artifact identity, approvals, and rollback.

## Lab 9: Secure untrusted pull requests

Review a hypothetical workflow that runs code from a public fork and has access to deployment secrets.

**Tasks**
1. Identify the risk.
2. Remove secret exposure from untrusted code.
3. Explain why privileged pull-request triggers need careful review.

## Lab 10: Add a smoke test

After a staging deployment, run a basic health check against a test endpoint.

**Tasks**
- Use a configurable non-secret URL.
- Fail on a non-success HTTP response.
- Add a timeout.
- Avoid printing sensitive response bodies or headers.

## Lab 11: Troubleshoot failures

For each situation, write the likely cause and next diagnostic step:

1. A workflow never starts on a pull request.
2. A job is skipped even though the workflow started.
3. An artifact upload fails because no files matched.
4. Deployment is blocked waiting for approval.
5. A test passes locally but fails in CI.

## Lab 12: Pipeline security review

Review one workflow using this checklist:

- Least-privilege `GITHUB_TOKEN` permissions
- Action and reusable workflow pinning
- Secret handling and log hygiene
- Pull-request trigger safety
- Dependency installation and lockfiles
- Artifact contents and integrity
- Environment protection
- Clear failure handling and audit trail

**Final deliverable:** a short risk register with finding, impact, likelihood, and remediation.
