# GitLab Pipeline Hardening — Solutions and Explanations

These are reference solutions. GitLab menus and feature availability can vary by version and subscription tier. Adapt the exact settings to your instance.

## Solution 1 — Asset inventory

Example:

| Asset | Threat | Risk | Control |
|---|---|---:|---|
| Production deploy token | Theft from job log | Critical | External secret manager, protected scope |
| CI job token | Cross-project access abuse | High | Narrow allowlist |
| Shared runner | Malicious job persistence | Critical | Ephemeral isolated runner |
| `.gitlab-ci.yml` | Unauthorized pipeline change | High | CODEOWNERS and approvals |
| Production environment | Unauthorized deployment | Critical | Protected environment |
| Build artifact | Artifact substitution | High | Immutable promotion and provenance |
| Dependency cache | Poisoned cache | High | Separate trusted/untrusted caches |
| Container image | Mutable tag substitution | High | Digest pinning |

Prioritize assets by business impact, exposure, and ease of abuse.

## Solution 2 — Protect pipeline configuration

1. Protect the default branch under repository branch settings.
2. Add `CODEOWNERS` entries for pipeline and deployment files.
3. Configure merge-request approval rules that require the relevant owners.
4. Require a successful pipeline before merge.
5. Test with a feature branch and confirm the approval gate.

Example:
```text
/.gitlab-ci.yml       @platform-security
/ci/                  @platform-security
/deploy/              @release-engineering
```

CODEOWNERS syntax alone does not enforce review; configure the matching approval rules.

## Solution 3 — Safe variables

In project/group CI/CD variable settings:
- Key: `STAGING_DEPLOY_TOKEN`
- Value: dummy random string
- Masked: enabled
- Hidden: enabled where available
- Protected: enabled
- Environment scope: `staging`

A protected variable is intended for protected refs. Confirm the branch protection and environment-scope behavior in your GitLab version. Do not print the value; use only:
```yaml
check_secret_presence:
  script:
    - test -n "$STAGING_DEPLOY_TOKEN"
    - echo "Staging credential is available to this authorized job"
```

## Solution 4 — Log hygiene

Unsafe commands:
```bash
env
printenv
echo "$TOKEN"
set -x
```

Safer commands:
```bash
test -n "$TOKEN"
echo "Required credential is configured"
```

Do not assume masking makes unsafe output acceptable. Masking can fail for transformed, encoded, split, or otherwise modified values.

## Solution 5 — Dependency pinning

Node:
```yaml
script:
  - npm ci
  - npm test
```

Python:
```yaml
script:
  - python -m pip install --require-hashes -r requirements.txt
  - python -m pytest -q
```

Go:
```yaml
script:
  - go mod verify
  - go test ./...
```

Pin container images to verified digests for stronger integrity. Fixed tags improve repeatability but can still be moved by a registry publisher; digest pinning is stronger.

## Solution 6 — Job-token allowlist

A good policy has:
- A named consumer project.
- A documented target project.
- Only the required inbound access.
- A responsible owner.
- A periodic review date.

Remove wildcard or obsolete allowlist entries. Test both permitted and denied access using separate authorized test projects. Avoid broadening access just to make a failed test pass.

## Solution 7 — Runner isolation

Reference architecture:
```text
Untrusted merge request
        |
        v
Ephemeral isolated runner
        |
        v
Lint + unit tests (no production secrets)

Reviewed protected branch
        |
        v
Protected release runner
        |
        v
Package/sign/deploy with scoped credentials
```

Runner tags help select runners, but actual security requires protected-runner configuration, project/group scoping, executor isolation, host hardening, and network restrictions.

## Solution 8 — Production deployment

Example job:
```yaml
deploy_production:
  stage: deploy
  environment:
    name: production
  resource_group: production
  script:
    - test -n "$PRODUCTION_DEPLOY_TOKEN"
    - ./scripts/deploy.sh
  rules:
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
      when: manual
```

Then configure the environment as protected and limit deploy permissions. Add approvals where supported. A manual job is not a substitute for protected-environment permissions.

## Solution 9 — Artifacts and caches

Good controls:
- Exclude `.env`, private keys, tokens, and credential files.
- Keep only required build outputs.
- Use short retention for sensitive artifacts.
- Limit artifact download access where available.
- Separate caches by trust boundary and protected-ref status.
- Do not allow untrusted jobs to populate caches consumed by privileged release jobs.

## Solution 10 — Network security

- Use HTTPS with certificate verification.
- Avoid `curl -k` and equivalent certificate-validation bypasses.
- Restrict egress to required registries and deployment APIs.
- Document endpoints, ports, and data exchanged.
- Use private networking or mutual TLS where justified.
- Do not embed credentials in URLs.

## Solution 11 — Include pinning

Safer:
```yaml
include:
  - project: "platform/ci-templates"
    ref: "0123456789abcdef0123456789abcdef01234567"
    file: "/templates/security.yml"
```

The SHA is a placeholder. Use the real reviewed commit SHA. For components, pin a protected version. Review updates as code changes and test representative consumer projects.

## Solution 12 — Example remediation plan

| Priority | Finding | Remediation | Owner |
|---|---|---|---|
| P0 | Production token exposed to untrusted jobs | Move to protected scope/secret manager; isolate deploy job | Platform |
| P0 | Shared persistent runner | Replace with isolated ephemeral runner | Infrastructure |
| P1 | Unpinned image references | Pin verified digests | DevOps |
| P1 | Broad job-token allowlist | Restrict to required projects | GitLab admin |
| P1 | Pipeline changes lack review | CODEOWNERS and approval rules | Repository owners |
| P2 | Artifacts retained indefinitely | Set retention and access restrictions | Project team |
| P2 | Logs contain excessive diagnostics | Remove environment dumps and shell tracing | Developers |

## Evaluation rubric

| Area | Marks |
|---|---:|
| Threat model and asset inventory | 10 |
| Secrets and token protection | 20 |
| Runner isolation | 15 |
| Supply-chain integrity | 15 |
| Branch, pipeline, and deployment controls | 20 |
| Logs, artifacts, and caches | 10 |
| Evidence and remediation report | 10 |
| **Total** | **100** |

A strong submission demonstrates both positive access (authorized job succeeds) and negative access (unauthorized job is denied) without exposing real credentials.
