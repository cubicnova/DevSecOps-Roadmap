# GitLab CI/CD — Pipeline Policies

## Overview
GitLab pipeline policies let security and platform teams centrally enforce CI/CD behavior across multiple projects. Instead of relying on every project maintainer to copy the same checks into `.gitlab-ci.yml`, an organization can manage policy configuration in a security policy project and apply it to selected projects or groups.

This module focuses on pipeline execution policies, policy scope, configuration strategies, scan execution policies, policy governance, and safe rollout.

> **Availability:** Pipeline execution policies and several policy capabilities are GitLab Ultimate features. Confirm the tier, GitLab version, and offering for your instance before designing a rollout.

## Learning objectives
- Explain why centralized pipeline policies are used.
- Differentiate project CI configuration from centrally enforced policy configuration.
- Understand the role of a security policy project and `policy.yml`.
- Describe pipeline execution policy strategies.
- Scope policies to groups, projects, and compliance frameworks.
- Understand scan execution policies and how they differ from pipeline execution policies.
- Control policy variables and pipeline-skip behavior.
- Validate, test, monitor, and roll out policies safely.

## Why pipeline policies?
Without central enforcement, projects may use inconsistent CI configurations. A team might accidentally omit a required scan, weaken a job, or use a different process for releases.

Centralized policies can help enforce:
- Required security scanning.
- Organization-wide CI/CD checks.
- Approved pipeline stages and jobs.
- Restrictions on bypassing required pipelines.
- Standardized compliance or release checks.

Policies should be designed with project teams and tested against representative repositories. A badly designed policy can block many projects at once.

## Key components

| Component | Purpose |
|---|---|
| Security policy project | Stores policy definitions and referenced CI/CD configuration |
| `.gitlab/security-policies/policy.yml` | Defines security policies and their scope |
| Pipeline execution policy | Enforces CI/CD jobs or pipeline configuration |
| Scan execution policy | Enforces security scan jobs according to configured rules |
| Policy scope | Selects the groups, projects, or compliance frameworks affected |
| Policy strategy | Determines how policy CI configuration is combined with project CI |
| Policy job | CI job introduced or required by a policy |

## Policy project structure

A security policy project commonly contains:

```text
security-policy-project/
└── .gitlab/
    └── security-policies/
        └── policy.yml
└── pipeline-config/
    ├── required-checks.yml
    └── security-scans.yml
```

The exact referenced file paths must match the policy configuration. The policy project should be maintained with code review, protected branches, and tightly controlled write access.

## Pipeline execution policy
A pipeline execution policy manages and enforces CI/CD jobs across projects. The policy definition is stored in `policy.yml`, while the job configuration can be stored in a separate YAML file in the security policy project.

Illustrative policy structure:

```yaml
pipeline_execution_policy:
  - name: Required pipeline checks
    description: Enforce baseline CI checks
    enabled: true
    pipeline_config_strategy: inject_policy
    content:
      include:
        - project: my-group/security-policy-project
          file: pipeline-config/required-checks.yml
```

This is a structural example. Replace the project path and file path with real values and validate against the schema supported by your GitLab version.

The referenced CI configuration might contain:

```yaml
policy-validation:
  stage: .pipeline-policy-pre
  image: alpine:3.20
  script:
    - echo "Required policy validation"
```

The reserved `.pipeline-policy-pre` stage is intended for policy jobs that must complete before regular pipeline jobs. Review the current version-specific behavior before relying on it as a release gate.

## Pipeline configuration strategies

| Strategy | Behavior | Typical use |
|---|---|---|
| `inject_policy` | Adds policy CI configuration to the project pipeline | Enforce additional jobs while preserving project pipeline |
| `override_project_ci` | Replaces project CI configuration with policy configuration | Standardize or centrally control the whole pipeline |
| `inject_ci` | Deprecated legacy strategy | Do not use for new policies; migrate to `inject_policy` |

Choose `inject_policy` when teams need to keep their own pipeline while receiving mandatory policy jobs. Use `override_project_ci` only when the organization intentionally owns the full pipeline configuration and has tested the effect on project workflows.

With injected policy stages, stage ordering must be compatible with project stages. Conflicting stage constraints can cause pipeline creation to fail with cyclic dependency errors.

## Scan execution policies
Scan execution policies centrally enforce security scans, such as SAST, DAST, dependency scanning, and container scanning, based on policy configuration and scope.

They differ from pipeline execution policies:
- Pipeline execution policies enforce CI/CD jobs or pipeline configuration.
- Scan execution policies enforce supported security scanning behavior.

Use the policy type that matches the governance requirement. Avoid duplicating the same scan in project YAML and centrally enforced policies unless duplication is intentional and understood.

## Policy scope
A policy can be applied to selected projects, groups, or compliance framework labels, depending on supported policy fields and GitLab version.

Conceptual example:

```yaml
policy_scope:
  projects:
    including:
      - id: 123
    excluding:
      - id: 456
```

IDs in examples are placeholders. Check the exact schema and available scope dimensions for the policy type you use. An empty scope collection may be interpreted as no restriction for that dimension; do not assume an empty list disables a policy.

## Variables and bypass controls
Pipeline execution policies support controls for variable overrides and CI skip directives. These controls help prevent project-level configuration from disabling required policy jobs.

For example, a policy can restrict variable overrides while allowing a narrowly defined exception:

```yaml
variables_override:
  allowed: false
  exceptions:
    - CS_IMAGE
```

This is illustrative; use only supported fields for the policy type and GitLab version. Prefer a strict allowlist of permitted overrides over allowing arbitrary variables and attempting to block a few known disable flags.

Policies can also control use of `[skip ci]` and `[no_pipeline]` through documented policy fields. Understand the impact on developer workflows and automation before enforcing restrictions.

## Reserved policy stages
GitLab uses reserved stages such as `.pipeline-policy-pre` and `.pipeline-policy-post` for policy execution. Jobs in `.pipeline-policy-pre` are intended to run before normal project pipeline jobs. Current GitLab versions have defined failure behavior for this stage; verify the exact behavior in your instance's version documentation.

Do not assign ordinary project jobs to reserved stages unless the relevant policy mechanism explicitly permits it.

## Governance and rollout
1. Start with a test security policy project.
2. Define the smallest useful policy.
3. Scope it to a pilot project.
4. Validate policy schema and referenced CI YAML.
5. Test merge requests, branch pipelines, tags, schedules, and child pipelines as applicable.
6. Check policy/project stage compatibility.
7. Review permissions to the security policy project and referenced files.
8. Roll out to a small group, monitor results, then expand.
9. Document exceptions, owners, and a rollback procedure.

## Security best practices
- Protect the security policy project's default branch.
- Require code review for policy changes.
- Limit who can edit policy files.
- Use immutable or protected refs for shared policy configuration where appropriate.
- Grant only required read access to referenced CI configuration.
- Restrict policy scope intentionally and review it periodically.
- Avoid exposing secrets in policy jobs or logs.
- Test changes against representative projects before broad rollout.
- Monitor policy failures and maintain an emergency rollback plan.
- Migrate deprecated compliance pipeline configurations according to GitLab guidance before enabling pipeline execution policies in affected projects.

## Troubleshooting

| Symptom | Likely cause | What to check |
|---|---|---|
| Policy not applied | Scope mismatch or policy disabled | `enabled`, project/group scope, compliance framework |
| Pipeline creation fails | Invalid policy schema or YAML | Policy schema, CI Lint, referenced file path |
| Include cannot be read | Triggering user lacks access to policy project/file | Security policy project access and automatic access settings |
| Duplicate jobs | Same checks defined in project and policy pipelines | Remove duplication or intentionally configure ownership |
| Cyclic stage dependency | Policy and project stage order conflict | Align stage definitions and policy stage constraints |
| Policy job missing | Policy rules or pipeline source conditions exclude it | Inspect merged configuration and rules |
| Project pipeline replaced | `override_project_ci` selected | Confirm strategy and restore/integrate project config |
| Child pipeline not covered | Policy not configured for child pipelines | Review `enforce_on_child_pipelines` support and setting |

## References
- [GitLab policies overview](https://docs.gitlab.com/user/application_security/policies/)
- [Pipeline execution policies](https://docs.gitlab.com/user/application_security/policies/pipeline_execution_policies/)
- [Scan execution policies](https://docs.gitlab.com/user/application_security/policies/scan_execution_policies/)
- [Security policy project](https://docs.gitlab.com/user/application_security/policies/)
