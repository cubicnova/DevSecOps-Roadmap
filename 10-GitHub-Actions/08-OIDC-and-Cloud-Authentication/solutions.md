# Solutions — OIDC and Cloud Authentication

These model answers show the expected reasoning. Adapt them to your provider and current GitHub OIDC subject format. Never copy sample trust policies into production without validating every condition.

## Solution 1: OIDC flow
1. GitHub Actions runs a job with `id-token: write`.
2. The job requests a signed OIDC JWT from GitHub.
3. The workflow presents the JWT to the configured cloud identity provider.
4. The cloud validates issuer, audience, signature, expiry, and configured identity claims.
5. A matching trust policy permits exchange for temporary cloud credentials.
6. Cloud IAM/RBAC policy decides what those credentials can do.
7. Credentials expire; logs and audit events support review.

OIDC federation establishes identity, but the cloud role's authorization policy still controls resource access.

## Solution 2: Minimal workflow permission
```yaml
permissions:
  contents: read

jobs:
  authenticate:
    permissions:
      contents: read
      id-token: write
```
The job can request a GitHub OIDC token and read repository content. It does not automatically have permission to change GitHub repository content or access any cloud resource. The cloud provider must trust the token and the assumed identity must have appropriate IAM/RBAC permissions.

## Solution 3: Trust-policy checklist
- Correct issuer: `https://token.actions.githubusercontent.com`
- Correct audience for the provider/action
- Exact repository identity
- Trusted branch, tag, or protected environment
- Current `sub` format, including immutable subject claims if enabled
- No broad wildcard that unintentionally trusts other repositories or refs
- Separate least-privilege cloud permissions policy
- Audit logging enabled and an owner assigned

For repositories created after July 15, 2026, or repositories using immutable subject claims, verify the subject format in the current GitHub reference. Legacy conditions may no longer match.

## Solution 4: AWS example reasoning
A conventional subject condition may resemble:
```json
{
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
    "token.actions.githubusercontent.com:sub": "repo:OWNER/REPOSITORY:ref:refs/heads/main"
  }
}
```
This is an illustrative condition fragment, not a complete policy. Replace placeholders, confirm the actual subject claim, and use a role policy limited to required AWS actions and resources. The trust policy determines who may assume the role; the role permissions policy determines what the role may do.

## Solution 5: Azure / Google Cloud
- **Azure:** Configure a federated credential on the intended Entra identity. Match issuer, audience, and subject. Grant only the required Azure role at the narrowest scope.
- **Google Cloud:** Configure Workload Identity Federation and attribute conditions that identify the intended repository and trusted branch/environment. Grant only the needed IAM roles to the service account or federated principal.

Use each provider's official setup instructions because field names and policy syntax differ.

## Solution 6: Production environment
A good configuration includes:
- A GitHub Environment named `production`.
- Required reviewers or another appropriate approval rule.
- Allowed deployment branches/tags.
- A deployment job that declares `environment: production`.
- A cloud trust policy that matches the intended environment identity.
- A cloud role with least-privilege deployment permissions.

The environment setting in YAML is only one part of the control; repository configuration and cloud-side trust must agree.

## Solution 7: Troubleshooting decision tree

| Symptom | Likely checks |
|---|---|
| Workflow cannot request OIDC token | `id-token: write`, supported job context, action inputs, audience |
| Cloud rejects token exchange | Issuer, audience, subject, branch/environment, federated provider setup, subject format |
| Exchange succeeds but API call fails | Cloud IAM/RBAC role, resource scope, service API, organization policy |
| Works on one branch only | Trust conditions and actual `ref`/`sub` claims |
| Fails after repository migration or policy update | Current immutable subject format and repository/owner IDs |
| Works in test but not production | Environment claims, required reviewers, allowed branches, separate role trust |

Avoid resolving failures by using administrator roles or unrestricted wildcard trust.

## Solution 8: Token handling
- Do not print the JWT or cloud access token.
- Do not upload tokens to artifacts or logs.
- Use official provider actions where appropriate.
- Use temporary credentials and limit their duration.
- Restrict job permissions and trust policy.
- Review cloud audit logs after tests.

## Solution 9: Why OIDC is safer—and what it does not solve
OIDC reduces reliance on long-lived cloud secrets and supports claim-based trust decisions. It does not protect against a compromised workflow that is legitimately trusted, an overprivileged cloud role, a malicious third-party action, or unsafe deployment logic. Secure the workflow, pin/review actions, restrict trust claims, protect environments, and minimize cloud IAM permissions.

## Final acceptance criteria
- Token-request permission is granted only where needed.
- Cloud trust conditions identify the intended workflow.
- The cloud role cannot perform unrelated administrative actions.
- Environment and branch protections are in place.
- Tokens are treated as secrets.
- Authentication and authorization failures are diagnosed separately.
