# Practical Exercises — Pipeline Security

**Level:** Intermediate. Use a test repository and non-production infrastructure. Do not attempt to compromise third-party workflows or steal secrets.

## Exercise 1 — Map trust boundaries

Draw an architecture containing an external pull request, repository/workflow configuration, runner, secrets store, third-party actions, artifact registry, cloud identity, staging, and production. Mark trust boundaries, credential availability, and artifact crossings.

**Deliverable:** Diagram and short threat model.

## Exercise 2 — Audit workflow permissions

1. Inspect workflows in a test repository.
2. List all `permissions` declarations and identify jobs with write access.
3. Explain why each permission is required.
4. Remove unnecessary permissions from a copy.
5. Confirm required jobs still work.

**Deliverable:** Before/after permission matrix.

## Exercise 3 — Review action references

Inventory third-party actions and reusable workflows. Record repository/name, reference type (tag, branch, SHA), purpose, job permissions, trust assessment, and update mechanism. Propose using verified full commit SHAs or an enforced dependency lockfile where supported.

## Exercise 4 — Handle untrusted event data

Find workflows that use pull-request titles, branch names, or other event data in shell commands. Rewrite direct expression interpolation to use an environment variable and quote it as data. Explain why validation is still needed when values are used in commands, paths, or queries.

Use harmless test strings; do not test malicious payloads against production.

## Exercise 5 — Review privileged triggers

Search for `pull_request_target` and `workflow_run`. For each, ask:
- Does it access secrets or write permissions?
- Does it check out or execute untrusted code?
- Does it consume artifacts from another workflow?
- Can privileged tasks be separated from untrusted validation?

**Deliverable:** Findings table with severity, evidence, and remediation.

## Exercise 6 — Design a secret-handling policy

Cover secret storage and scope, branch/environment restrictions, token lifetime and rotation, log masking limitations, avoiding secrets in artifacts, response to exposure, and preference for OIDC or other short-lived identity where supported. Do not create or expose a production secret.

## Exercise 7 — Harden runners

Compare hosted ephemeral runners with persistent self-hosted runners. Assess job isolation, patching, network egress, credentials on disk, untrusted PR access, workspace cleanup, admin access, and monitoring.

**Deliverable:** Risk matrix and runner standard.

## Exercise 8 — Secure artifact handling

Design controls for a container image: source revision, registry access, image digest, SBOM and vulnerability scan, provenance/signing where supported, verification before deployment, retention, and quarantine procedures. Explain why a tag alone may not identify exact content.

## Exercise 9 — Create a minimal secure workflow

Create a workflow in a test repository that:
- Runs on pull requests and pushes to `main`.
- Declares read-only `contents` permission.
- Performs harmless validation.
- Does not access deployment secrets or deploy from a PR.
- Uses reviewed action references.

Document what would need hardening before production use.

## Exercise 10 — Design an OIDC trust policy

For a hypothetical cloud deployment, document why OIDC is preferable to a long-lived key, which job needs `id-token: write`, allowed repository and branch/environment, audience and subject conditions, least-privilege cloud permissions, and how you would test/audit the policy. Do not include real JWTs or credentials. Confirm the actual claims format used by the repository.

## Exercise 11 — Pipeline incident tabletop

Scenario: a third-party action in a release workflow may be compromised. Plan how to identify affected runs, rotate credentials, quarantine artifacts, preserve evidence, identify affected releases, rebuild from a trusted source, verify replacement artifacts, communicate, and prevent recurrence.

## Exercise 12 — Mini project

Create a defensive review for a sample application.

Required outputs:
- `pipeline-threat-model.md`
- Trust-boundary diagram
- Workflow permission matrix
- Action dependency inventory
- Secret and OIDC policy
- Runner hardening standard
- Artifact integrity policy
- Incident response checklist
- Remediation backlog with severity, owner, and target date

### Evaluation rubric (100 points)

| Area | Points |
|---|---:|
| Trust boundaries and threat model | 15 |
| Least-privilege permissions | 15 |
| Untrusted PR and injection handling | 15 |
| Action/dependency supply-chain controls | 15 |
| Secrets and OIDC policy | 15 |
| Runner and artifact hardening | 15 |
| Incident response and documentation | 10 |

## Submission checklist

- [ ] Workflow permissions are minimal.
- [ ] Untrusted PR code cannot access privileged credentials.
- [ ] Event data is not directly interpolated into shell code.
- [ ] Action references and update procedures are documented.
- [ ] Runner isolation and artifact provenance are addressed.
- [ ] OIDC trust conditions are restrictive.
- [ ] Incident response includes credential rotation and artifact quarantine.
