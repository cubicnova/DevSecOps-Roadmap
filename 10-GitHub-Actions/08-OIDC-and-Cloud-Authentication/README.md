# 08 — OIDC and Cloud Authentication

## Overview
GitHub Actions can authenticate to cloud providers using OpenID Connect (OIDC) instead of storing long-lived cloud access keys as GitHub secrets. A workflow requests a signed OIDC JSON Web Token (JWT) from GitHub, and the cloud identity provider validates the token's claims against a configured trust policy before issuing short-lived cloud credentials.

This module covers the authentication flow, GitHub Actions permissions, trust policies, AWS/Azure/GCP examples, and practical security checks.

## Learning objectives
By the end of this module, you should be able to:
- Explain federation, identity tokens, access tokens, and the OIDC trust relationship.
- Configure the `id-token: write` permission correctly.
- Describe the issuer, audience, subject, repository, ref, and environment claims.
- Create least-privilege cloud trust policies restricted to trusted repositories and branches/environments.
- Configure a workflow to exchange a GitHub OIDC token for short-lived cloud credentials.
- Explain why `id-token: write` does not grant cloud resource permissions by itself.
- Troubleshoot failed token exchange and cloud authorization.
- Avoid exposing cloud access to untrusted pull requests or overly broad workflow identities.

## 1. Why use OIDC?
Long-lived cloud keys stored in GitHub secrets can be copied, leaked, forgotten, or reused outside their intended workflow. With OIDC, GitHub issues a job-specific identity token and the cloud provider exchanges it for short-lived credentials. This reduces the need to store long-lived cloud credentials in the repository's secret store.

OIDC is not automatically secure just because it removes static secrets. The cloud trust policy must strictly limit which workflows can obtain credentials, and the resulting cloud role must have only the permissions required.

## 2. Authentication flow
1. An administrator configures a federated identity provider and trust policy in the cloud.
2. A GitHub Actions job receives permission to request an OIDC token using `id-token: write`.
3. The workflow requests a signed JWT from GitHub's OIDC provider.
4. The cloud provider validates the token's signature, issuer, audience, expiry, and configured claims.
5. If the trust policy matches, the provider issues temporary credentials.
6. The job uses those credentials for a limited task, then they expire.

## 3. Key claims
| Claim | Meaning | Security use |
|---|---|---|
| `iss` | Token issuer | Confirm GitHub's OIDC provider |
| `aud` | Intended audience | Ensure the token is intended for the expected exchange |
| `sub` | Subject identity | Restrict repository, ref, or environment identity |
| `repository` | Repository name | Additional repository condition where supported |
| `ref` | Git ref | Restrict branch or tag |
| `sha` | Commit SHA | Audit the exact source revision |
| `environment` | GitHub Environment, when used | Gate deployments through protected environments |

Cloud providers differ in how they express claim conditions. Configure conditions in the cloud trust policy, not just in the workflow YAML.

**Important 2026 note:** GitHub's OIDC subject (`sub`) format can differ depending on repository creation date and whether immutable subject claims are enabled. Repositories created after July 15, 2026, or that opt in to immutable subject claims may include owner and repository IDs in `sub`. Match the actual subject format for your repository and follow the current GitHub reference rather than copying an older example unchanged.

## 4. Minimal workflow permission

```yaml
permissions:
  contents: read
  id-token: write
```

`contents: read` is commonly needed for checkout. `id-token: write` lets the job request an OIDC JWT; it does **not** grant permission to modify GitHub repository contents or authorize cloud resources on its own.

Prefer job-level `permissions` so only the deployment job can request the token.

## 5. AWS example

The official AWS credentials action supports OIDC role assumption. Before using the workflow, configure the AWS IAM OIDC provider and a role trust policy restricted to the correct repository and branch/environment. The role's permissions policy must also restrict the AWS resources and actions the job can access.

```yaml
name: AWS OIDC authentication

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  authenticate:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsReadOnly
          aws-region: us-east-1
      - name: Verify identity
        run: aws sts get-caller-identity
```

Replace the account ID, role ARN, and region with your own values. The role name is illustrative. Do not grant broad administrator access to a CI role merely to make authentication succeed.

## 6. Azure and Google Cloud
For Azure, configure a federated credential on an Entra application or managed identity and use the official Azure Login action with OIDC. For Google Cloud, configure Workload Identity Federation and use the official Google authentication action. In both cases, match the provider's expected audience and subject/attribute conditions, then grant only the required resource permissions.

Consult the provider's current documentation for exact configuration fields and action inputs. Do not reuse AWS trust-policy syntax for Azure or Google Cloud.

## 7. Security checklist
- Restrict cloud trust to the exact repository and trusted branch or protected environment.
- Check `aud` and `sub` (or equivalent attribute conditions) in the cloud provider.
- Grant `id-token: write` only to jobs that need cloud authentication.
- Use protected GitHub Environments and required reviewers for production deployments.
- Never expose OIDC access to untrusted pull-request code.
- Pin third-party actions according to your supply-chain policy.
- Give the assumed cloud role least-privilege permissions.
- Prefer short-lived credentials and avoid logging tokens.
- Audit cloud role sessions and correlate them with repository, workflow, commit, and deployment records.
- Revisit trust policies when repositories, branch names, environments, or OIDC subject formats change.

## 8. Troubleshooting
**No OIDC token available**
- Check that `id-token: write` is granted at workflow or job level.
- Check whether the token request occurs inside a supported GitHub Actions job.
- Confirm the action requests the correct audience.

**Cloud provider rejects the token**
- Check issuer and audience.
- Compare the actual `sub` claim to the trust policy.
- Check branch, tag, environment, and repository conditions.
- Verify the cloud-side federated identity provider configuration and clock/expiry assumptions.

**Authentication succeeds but resource access fails**
- Token exchange succeeded, but the assumed role/service principal likely lacks the required cloud permissions.
- Check role assignment, IAM policy, resource scope, and audit logs.
- Do not solve a resource authorization problem by making the trust policy or role administrator-wide.

## Further reading
- [GitHub Actions OpenID Connect](https://docs.github.com/en/actions/concepts/security/openid-connect)
- [Configure OIDC in cloud providers](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-cloud-providers)
- [OIDC reference and claims](https://docs.github.com/en/actions/reference/security/oidc)
- [AWS credentials action](https://github.com/aws-actions/configure-aws-credentials)
- [Azure Login action](https://github.com/Azure/login)
- [Google GitHub Actions authentication](https://github.com/google-github-actions/auth)
