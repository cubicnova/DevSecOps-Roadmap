# Solutions — Pipeline Security

These are model answers. Adapt controls to your CI platform, repository trust model, cloud provider, and release requirements.

## Solution 1 — Trust boundaries

Separate untrusted pull-request validation from privileged release workflows; build/test execution from deployment credentials; artifact publication from consumption; and repository permissions from production permissions. Show where secrets are available and how artifacts are verified. Untrusted code should not execute in a job with production credentials.

## Solution 2 — Workflow permissions

A restrictive default is:

```yaml
permissions:
  contents: read
```

Grant extra permissions only to jobs that need them. A package-publishing job may require `packages: write`; a validation job generally should not. Avoid `write-all`. Run the workflow after changes to confirm it still has the permissions it genuinely needs.

| Job | Intended minimum permissions | Reason |
|---|---|---|
| Validate | `contents: read` | Read source and run checks |
| Test | `contents: read` | Read code and execute tests |
| Publish package | `contents: read`, `packages: write` if required | Publish package |
| Deploy with OIDC | `contents: read`, `id-token: write` | Read source and request identity token |
| Report | Read-only scopes required by reporting API | Submit required report |

Exact requirements depend on the platform and integrations.

## Solution 3 — Action references

Inventory action name, source repository, purpose, reference, job permissions, trust assessment, and update owner. Prefer verified full commit SHAs or a supported dependency lockfile. Confirm the SHA belongs to the intended upstream repository. Use controlled automation to propose updates and review them before merging. Pinning reduces mutable-reference risk but does not remove vulnerabilities in pinned code.

## Solution 4 — Safe event data

Unsafe:

```yaml
- run: echo "${{ github.event.pull_request.title }}"
```

Safer:

```yaml
- name: Print title as data
  env:
    PR_TITLE: ${{ github.event.pull_request.title }}
  run: |
    printf '%s\n' "$PR_TITLE"
```

This prevents the title from being substituted into the shell program text. It remains untrusted input. Validate and safely encode it if used in filenames, command arguments, queries, or APIs; never evaluate it as shell code.

## Solution 5 — Privileged triggers

Do not combine `pull_request_target` with checking out or executing untrusted pull-request code. A safer pattern is:
1. Validate PRs on `pull_request` with read-only permissions and no secrets.
2. Merge after required reviews and checks.
3. Run publishing/deployment from a trusted protected branch.
4. If a privileged workflow consumes another workflow's artifact, verify origin, expected commit, and contents.

`workflow_run` is not automatically safe; downloaded artifacts and referenced code must still be treated as potentially untrusted.

## Solution 6 — Secret policy

Store credentials in the approved secret store; scope them to the smallest job/environment; never commit or print them; use short-lived credentials/OIDC where supported; restrict branches and events allowed to request credentials; rotate any exposed credential and investigate access. Automatic log masking is not guaranteed to redact every transformed secret value.

## Solution 7 — Runner hardening

| Risk | Mitigation |
|---|---|
| State persists between jobs | Use ephemeral runners or verified cleanup |
| Untrusted PR reaches privileged runner | Separate runner groups and access policies |
| Outdated runner image | Patch and rebuild images regularly |
| Broad network access | Restrict egress where practical |
| Credentials remain on disk | Avoid long-lived credentials; clean sensitive state |
| Excessive administrative access | Limit and audit runner administration |
| Insufficient evidence | Centralize useful logs without recording secrets |

Self-hosted runners require explicit ownership of isolation, patching, network controls, and lifecycle management.

## Solution 8 — Artifact handling

Build from a reviewed revision in an isolated runner; run tests and scans; generate an SBOM where appropriate; publish to a restricted registry; record the digest and source commit; generate or verify provenance/signatures where supported; verify required evidence before deployment; retain release/rollback artifacts; quarantine artifacts if compromise is suspected.

A tag can be reassigned unless immutability is enforced. A digest identifies content; signatures and provenance provide additional evidence about origin and build process.

## Solution 9 — Minimal workflow

```yaml
name: Pipeline Security Check

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Check out source
        uses: actions/checkout@v4
      - name: Validate whitespace
        run: git diff --check
```

This demonstrates restrictive permissions and a harmless check. For production, pin the action to a verified full SHA or use a supported enforced dependency lockfile. Add tests/scans, protect workflow files, and ensure untrusted PRs cannot access deployment secrets.

## Solution 10 — OIDC policy

Grant `id-token: write` only to the deployment job. Restrict the cloud trust policy by issuer, audience, repository identity, branch or environment subject, and any relevant claims. The cloud role itself must have only the permissions required for deployment.

Do not assume a subject string without inspecting actual claims. GitHub's default subject format changed for some repositories created after July 15, 2026; confirm the format and update the provider trust policy. OIDC avoids storing a long-lived cloud key as a repository secret, but a broad trust policy can still allow unintended workflows to obtain credentials.

## Solution 11 — Incident response

1. Pause affected workflows and releases.
2. Identify action version/SHA, workflows, repositories, and time window.
3. Revoke or rotate credentials accessible to affected jobs.
4. Preserve audit logs, workflow logs, runner evidence, and release metadata.
5. Identify and quarantine artifacts built or published in the affected window.
6. Rebuild from a known-good commit and trusted build inputs.
7. Verify replacement digest and provenance before redeployment.
8. Monitor repository, registry, and cloud activity.
9. Document root cause, impact, recovery, and preventive actions.

## Solution 12 — Mini-project acceptance criteria

A strong submission includes a trust-boundary diagram, read-only defaults and job-specific permissions, safe PR/event-data handling, an action inventory and update process, a secrets policy and restrictive OIDC design, runner isolation, artifact integrity controls, incident response, and a prioritized remediation backlog.

## Final review checklist

- [ ] Workflow permissions are minimal and explicit.
- [ ] Privileged workflows do not execute untrusted PR code.
- [ ] Action dependencies are reviewed and pinned appropriately.
- [ ] Secrets are scoped and never printed or committed.
- [ ] Runner isolation matches job trust level.
- [ ] Artifact origin and integrity are verified before deployment.
- [ ] OIDC trust policies restrict credential access.
- [ ] Incident response includes credential rotation and artifact quarantine.
