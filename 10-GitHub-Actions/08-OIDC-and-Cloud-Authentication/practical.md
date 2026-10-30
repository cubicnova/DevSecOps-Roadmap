# Practical Exercises — OIDC and Cloud Authentication

## Lab prerequisites
- A GitHub test repository with Actions enabled.
- An authorized sandbox account in AWS, Azure, or Google Cloud (for cloud labs).
- Permission to configure a federated identity provider and a low-privilege test role/identity.
- No production credentials or sensitive data.

If you do not have a cloud sandbox, complete the workflow design and trust-policy review exercises without requesting cloud credentials.

## Exercise 1: Draw the OIDC flow
Draw the steps from GitHub Actions job to GitHub OIDC provider, cloud identity provider, temporary credentials, and cloud resource.

**Deliverable:** Diagram plus a brief explanation of each trust decision.

## Exercise 2: Add `id-token: write`
Create a manual workflow that grants `id-token: write` to one job only. Explain why the permission does not grant repository write access or cloud resource authorization by itself.

**Deliverable:** Workflow YAML and permission analysis.

## Exercise 3: Inspect OIDC claims
In a dedicated test repository, use an approved OIDC claims debugging method. Record issuer, audience, subject, repository, ref, and environment claims as applicable. Do not print or store the full JWT.

**Deliverable:** Redacted claims table and notes about the subject format.

## Exercise 4: Configure a least-privilege AWS role
In a sandbox account, configure the GitHub OIDC provider and a role trust policy that allows only the intended repository and trusted branch or environment. Attach a policy limited to a harmless read-only task.

**Deliverable:** Redacted trust-policy excerpt, role permission summary, and successful identity check.

## Exercise 5: Test a trust-policy mismatch
In a sandbox, deliberately use a nonmatching branch or subject condition and verify that token exchange is rejected. Restore the intended condition.

**Deliverable:** Failure evidence, root cause, and corrected policy. Do not weaken trust conditions to make the test pass.

## Exercise 6: Configure Azure or Google Cloud federation
Choose one provider and configure its federated identity using the official instructions. Restrict issuer, audience, subject/attribute mapping, and cloud role permissions.

**Deliverable:** Configuration checklist and identity verification output with sensitive identifiers redacted as needed.

## Exercise 7: Protect production with a GitHub Environment
Create a `production` environment in a test repository, configure required reviewers and allowed deployment branches, and reference the environment from the deployment job.

**Deliverable:** Environment settings checklist and workflow YAML.

## Exercise 8: Separate test and deployment jobs
Create a read-only build/test job and a separate deployment job with `id-token: write`. Ensure the deployment job depends on successful tests and is restricted to a trusted ref/environment.

**Deliverable:** Workflow and a permission comparison table.

## Exercise 9: Troubleshoot authentication versus authorization
Create a troubleshooting guide distinguishing:
- Failure to request an OIDC token
- Cloud rejection of the token's claims
- Successful token exchange but denied cloud API call

**Deliverable:** Decision tree with checks for each failure class.

## Exercise 10: Review OIDC subject changes
Read the current GitHub OIDC reference. Explain how immutable subject claims can affect trust policies and why teams should verify the actual `sub` format rather than copy a legacy policy blindly.

**Deliverable:** Short migration checklist for reviewing existing trust policies.

## Completion checklist
- [ ] OIDC flow and trust boundary are understood.
- [ ] Only the necessary job has `id-token: write`.
- [ ] Trust conditions restrict repository and ref/environment.
- [ ] Cloud permissions are least privilege.
- [ ] Production environments have protection rules.
- [ ] JWTs and cloud credentials are never printed.
- [ ] Authentication errors are distinguished from authorization errors.
