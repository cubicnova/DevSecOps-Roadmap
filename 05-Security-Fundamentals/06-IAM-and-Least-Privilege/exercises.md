# IAM and Least Privilege - Exercises

Use a lab account or fictional scenarios. Do not change production access policies without authorization and an approved rollback plan.

## Part A: Knowledge Check

1. Explain the difference between identification, authentication, authorization, and auditing.
2. Define the principle of least privilege.
3. Why should least privilege apply to service accounts and CI/CD jobs?
4. Compare RBAC and ABAC.
5. Name three controls that reduce risk from privileged accounts.
6. What should happen to access when an employee changes teams?
7. Why are temporary credentials often preferable to long-lived static credentials?
8. Why is a wildcard permission such as `*` worth reviewing carefully?

## Part B: Scenario Analysis

For each scenario, identify the problem, propose least-privilege changes, and describe how you would verify the fix.

1. Every developer has administrator permissions in the cloud account.
2. A CI pipeline needs to upload build artifacts but can also delete production databases.
3. A former contractor's account remains enabled after their contract ended.
4. A support analyst needs to view customer tickets but does not need to export all customer records.
5. An engineer uses a privileged administrator account for email and routine browsing.
6. A role grants access based on a resource tag that ordinary users can freely modify.
7. A production emergency requires elevated access outside normal working hours.

## Part C: Practical Labs

### Lab 1: Build a Role-Permission Matrix

Create a fictional application with these roles:
- Viewer
- Developer
- SecurityReviewer
- PlatformAdmin

Define at least six actions, such as viewing logs, editing source code, deploying to development, deploying to production, changing IAM policies, and reviewing audit logs.

Create a matrix showing `Allow`, `Deny`, or `Approval required`. Explain why each role needs each permission.

### Lab 2: Review an Over-Privileged Policy

Review this illustrative pseudo-policy:

```text
Principal: deployment-pipeline
Actions: *
Resources: *
Purpose: deploy the web application to staging
```

1. Identify at least three risks.
2. Propose a narrower set of actions and resources.
3. State which production actions should not be granted to this identity.
4. Describe how to test that staging deployment still works and unrelated actions are denied.

This is intentionally platform-neutral pseudo-policy, not valid cloud policy syntax.

### Lab 3: Joiner-Mover-Leaver Checklist

Write a checklist for:
- A new employee joining the development team.
- A developer moving to the security team.
- A contractor leaving the organization.

Include approval, access assignment/removal, credential/session revocation, ownership transfer, and audit evidence.

### Lab 4: Access Review

Create a table of five fictional identities with their roles, granted permissions, last-used date, business owner, and recommended action. Include at least one stale account and one excessive permission.

### Lab 5: IAM for CI/CD

Design access for a pipeline that builds code, runs tests, publishes an artifact, and deploys to staging. Separate the permissions by job or stage where practical. Explain how you would protect secrets and prevent untrusted pull-request code from receiving deployment credentials.

## Part D: Short Written Task

Write a one-page least-privilege policy for a small DevSecOps team. Include:
- Account and MFA requirements
- Role assignment and approval
- Privileged access and emergency access
- Service identity and CI/CD requirements
- Periodic reviews
- Offboarding and credential revocation
- Logging and exception handling

## Submission Checklist

- [ ] Role permissions are based on tasks.
- [ ] Excessive permissions are identified and narrowed.
- [ ] Identity lifecycle steps are documented.
- [ ] CI/CD access is scoped to required resources and stages.
- [ ] Verification includes both allowed and denied access tests.
