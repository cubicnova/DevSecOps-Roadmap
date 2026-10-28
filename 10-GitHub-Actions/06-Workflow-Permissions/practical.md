# Practical Exercises — Workflow Permissions

## Lab prerequisites
- A test GitHub repository with Actions enabled.
- Permission to edit workflow files and view run logs.
- No production credentials or deployments are required.

## Exercise 1: Audit an existing workflow
Review a workflow and list all token permissions, actions, and operations that need GitHub API access. Identify broad or undocumented permissions.

**Deliverable:** Permission inventory with current scope, required scope, and rationale.

## Exercise 2: Create read-only CI
Create a workflow that checks out code and runs a harmless test with `contents: read`. Set `persist-credentials: false` if later steps do not need Git authentication.

**Deliverable:** Passing run and explanation of why write access is unnecessary.

## Exercise 3: Apply default-deny permissions
Set top-level `permissions: {}` and grant a single job only `contents: read`. Confirm that checkout and tests work.

**Deliverable:** Workflow and a brief scope-by-scope explanation.

## Exercise 4: Add issue labeling
Create a workflow triggered by a new issue. Grant only `issues: write` to the labeling job and use `GITHUB_TOKEN` safely.

**Deliverable:** Workflow and successful label result.

## Exercise 5: Diagnose a 403 error
Use a harmless API operation that your token is allowed to perform. Then remove the needed permission in a test branch and observe the failure. Restore the correct permission.

**Deliverable:** Error message, missing scope, fix, and evidence of least privilege.

## Exercise 6: Separate test and publish jobs
Design a workflow with a read-only test job and a package-publishing job that has `packages: write`. Use `needs` so publishing follows successful tests.

**Deliverable:** Workflow and explanation of why the test job should not receive publish permissions.

## Exercise 7: Review fork pull-request behavior
Read the official documentation and explain what changes for token permissions and secrets when a pull request comes from a fork. Do not enable write tokens for fork workflows as part of this exercise.

**Deliverable:** Short security note and safe workflow design.

## Exercise 8: Review `pull_request_target`
Write a threat model for a privileged `pull_request_target` workflow. Explain why checking out and executing untrusted pull-request code is dangerous.

**Deliverable:** Risk statement and at least three mitigations.

## Exercise 9: Review an OIDC workflow
Explain the purpose of `id-token: write`, the role of cloud trust policies, and why the workflow should not be granted unrelated repository write permissions.

**Deliverable:** A sample permission block and cloud trust-policy checklist.

## Exercise 10: Permission review checklist
Create a reusable checklist covering token scopes, action trust, checkout credentials, fork events, secrets, third-party API calls, and environment protections.

**Deliverable:** `workflow-permissions-checklist.md`.

## Completion checklist
- [ ] Workflow and job-level permissions are understood.
- [ ] A read-only workflow runs with minimal access.
- [ ] A write scope is added only for a demonstrated need.
- [ ] A 403 error is diagnosed without granting broad access.
- [ ] Fork and `pull_request_target` risks are documented.
- [ ] OIDC trust and permissions are distinguished.
