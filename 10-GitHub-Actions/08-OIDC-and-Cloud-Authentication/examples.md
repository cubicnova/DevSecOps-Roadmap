# Examples — OIDC and Cloud Authentication

These are templates for a lab or authorized cloud account. Replace all sample account, project, subscription, role, and region values. Configure the cloud-side identity provider and restrictive trust policy before running a workflow.

## Example 1: OIDC permission block
```yaml
permissions:
  contents: read
  id-token: write
```

Use `id-token: write` only for the workflow or job that needs to request an OIDC token. It does not grant cloud resource permissions on its own.

## Example 2: AWS OIDC role assumption
```yaml
name: AWS identity check

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  identity:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubActionsReadOnly
          aws-region: us-east-1
      - name: Verify assumed identity
        run: aws sts get-caller-identity
```

Before running:
1. Create/configure the AWS IAM OIDC provider for GitHub.
2. Configure the role trust policy to restrict the intended repository and branch or environment.
3. Attach a least-privilege permissions policy to the role.
4. Replace the sample ARN and region.
5. Verify the actual `sub` claim format for your repository.

## Example 3: Illustrative AWS trust condition
A traditional subject condition may look like the following **only when it matches your repository's actual subject format**:

```json
{
  "StringEquals": {
    "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
    "token.actions.githubusercontent.com:sub": "repo:OWNER/REPOSITORY:ref:refs/heads/main"
  }
}
```

This is a condition fragment for learning, not a complete IAM role trust policy. Replace `OWNER/REPOSITORY`, and follow the current GitHub OIDC reference if your repository uses immutable subject claims. Restrict the role to the minimum resources and actions required.

## Example 4: Azure Login using OIDC
```yaml
name: Azure OIDC identity check

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  identity:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - name: Verify Azure context
        run: az account show
```

Configure a federated credential in Microsoft Entra ID with the matching issuer, audience, and subject. The IDs shown as variables are not secrets, but they must be set to your environment's real values. Assign the identity only the required Azure roles.

## Example 5: Google Cloud Workload Identity Federation
```yaml
name: Google Cloud OIDC identity check

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  identity:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/POOL_ID/providers/PROVIDER_ID
          service_account: ci-readonly@PROJECT_ID.iam.gserviceaccount.com
      - name: Verify identity
        run: gcloud auth list
```

Configure Workload Identity Federation first. Replace all placeholders, map trusted GitHub claims, and grant the service account only required permissions. Use current provider guidance to verify the expected audience and attribute mapping.

## Example 6: Restrict cloud access to a protected environment
```yaml
name: Protected deployment identity

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - run: echo "Run the approved deployment command here"
```

Configure required reviewers and deployment branch rules on the `production` environment. The cloud trust policy must also match the intended environment identity; a YAML `environment` declaration alone does not create cloud-side trust.

## Example 7: Audit token claims safely
Use a reviewed OIDC debugging action in a dedicated test repository to inspect claims. Avoid printing the full JWT: it is a bearer token and should be treated as a credential. If you need to validate a trust policy, inspect non-sensitive claim fields through a trusted debugger and verify the cloud audit logs.

## Example 8: Separate build and cloud deployment permissions
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4
      - run: echo "Build and test without cloud credentials"

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      id-token: write
    steps:
      - run: echo "Authenticate with OIDC and deploy using least-privilege role"
```

This separates token-request capability from ordinary build activity. Add actual cloud authentication only after configuring the trust policy and environment protections. A branch condition alone is not a complete deployment security boundary.
