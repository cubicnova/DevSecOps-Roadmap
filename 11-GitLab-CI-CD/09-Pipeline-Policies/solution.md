# GitLab Pipeline Policies — Solutions and Explanations

> Policy fields and behavior can change between GitLab versions. Validate against the schema and documentation for the instance where the lab is performed.

## Exercise 1: Explore policies
Record GitLab version, tier, offering, and which policy types are available in the UI. Pipeline execution policies require GitLab Ultimate. Other policy capabilities can have their own tier and version requirements.

**Explanation:** Do not design an implementation around a policy feature that the target GitLab instance does not support.

## Exercise 2: Security policy project
Recommended structure:

```text
security-policy-project/
├── .gitlab/
│   └── security-policies/
│       └── policy.yml
└── pipeline-config/
    └── required-checks.yml
```

Protect the default branch, restrict write access, require review, and keep policy ownership explicit.

## Exercise 3: Basic execution policy

`policy.yml`:

```yaml
pipeline_execution_policy:
  - name: Required pipeline validation
    description: Enforce a basic validation job
    enabled: true
    pipeline_config_strategy: inject_policy
    content:
      include:
        - project: my-group/security-policy-project
          file: pipeline-config/required-checks.yml
```

`pipeline-config/required-checks.yml`:

```yaml
policy-validation:
  stage: .pipeline-policy-pre
  image: alpine:3.20
  script:
    - echo "Required policy validation"
    - test -n "$CI_PROJECT_PATH"
```

Replace the project path with the actual path and validate the policy. Then link the security policy project and apply the policy to a pilot project.

**Explanation:** The policy file references reusable CI configuration stored centrally. Users triggering pipelines need the required read access to that configuration.

## Exercise 4: Configuration strategies

| Strategy | Result |
|---|---|
| `inject_policy` | Adds policy CI configuration to the project pipeline |
| `override_project_ci` | Replaces project CI configuration with the policy configuration unless the project configuration is explicitly included |
| `inject_ci` | Deprecated; use `inject_policy` for new implementations |

**Explanation:** Use `inject_policy` when you need centrally enforced jobs without replacing the team's pipeline. `override_project_ci` is a stronger control and can disrupt existing project workflows if not designed carefully.

## Exercise 5: Scope
Illustrative project inclusion:

```yaml
policy_scope:
  projects:
    including:
      - id: 123
```

Illustrative exclusion:

```yaml
policy_scope:
  projects:
    excluding:
      - id: 456
```

Replace IDs with actual IDs and use the exact scope schema supported by the policy type.

**Explanation:** Scope determines which projects, groups, or compliance frameworks receive the policy. Verify the effective scope in a pilot before broad rollout.

## Exercise 6: Policy stages
Example policy CI configuration:

```yaml
stages:
  - test
  - policy-review
  - deploy

policy-review:
  stage: policy-review
  image: alpine:3.20
  script:
    - echo "Policy review"
```

**Explanation:** Injected policy stages must be ordered compatibly with project stages. Conflicting dependencies can produce a cyclic dependency error and prevent pipeline creation. Keep stage order explicit and test against projects with different pipeline layouts.

## Exercise 7: Variable overrides

```yaml
variables_override:
  allowed: false
  exceptions:
    - CS_IMAGE
```

**Explanation:** This is an allowlist-style approach: project configurations cannot override policy variables except for the listed exception. Prefer a strict allowlist over allowing all variables and trying to deny a small set of dangerous variables.

Use non-sensitive values in the lab. Never print credentials to demonstrate variable behavior.

## Exercise 8: Skip directives
Use the current documented policy fields:

```yaml
skip_ci:
  allowed: false
  allowlist:
    users:
      - id: 75
```

A corresponding `no_pipeline` field can control use of the `[no_pipeline]` directive where supported.

**Explanation:** Restrictions help prevent required checks from being bypassed, but may affect release automation and developer workflows. Pilot the behavior and document authorized exceptions.

## Exercise 9: Pipeline execution vs scan execution

| Requirement | Appropriate policy |
|---|---|
| Enforce a custom approval or validation CI job | Pipeline execution policy |
| Centrally require supported SAST or DAST scans | Scan execution policy |

**Explanation:** These policy types have separate schemas and purposes. Avoid configuring the same scanner both in the project and a policy unless duplicate execution is intentional.

## Exercise 10: Policy access
The user triggering a pipeline must have the required read access to the project containing the referenced CI configuration. Access can be granted manually or, where supported and configured, automatically through the security policy project setting.

**Explanation:** A policy can be correctly configured but still fail if the user cannot read the referenced file. Review job-token permissions as well when downstream pipelines or API access are involved.

## Exercise 11: Child pipelines
Pipeline execution policies are not enforced in child pipelines by default. Where supported, use:

```yaml
enforce_on_child_pipelines: true
```

A job can distinguish pipeline sources with rules such as:

```yaml
rules:
  - if: '$CI_PIPELINE_SOURCE == "parent_pipeline"'
```

**Explanation:** Child pipeline enforcement is version-dependent. Test parent and child behavior carefully and avoid recursive pipeline triggers.

## Exercise 12: Governance proposal — sample

| Area | Recommendation |
|---|---|
| Objective | Ensure all selected projects run mandatory security checks |
| Policy type | Scan execution policy for centrally required scans; pipeline execution policy for custom jobs |
| Scope | Start with a pilot group and explicit project inclusion |
| Strategy | Prefer `inject_policy` unless the organization intentionally owns the full pipeline |
| Ownership | Security platform team owns policy; project teams own remediation |
| Validation | Schema validation, CI Lint, merge request tests, and representative project tests |
| Exceptions | Document approver, reason, expiry, and compensating control |
| Monitoring | Track policy failures, skipped jobs, and vulnerability remediation |
| Rollback | Disable or revert the policy through reviewed change control |

## Troubleshooting reference

| Symptom | Likely cause | Resolution |
|---|---|---|
| Policy not applied | Scope excludes project or policy disabled | Review `enabled` and scope |
| Invalid policy | Schema mismatch or unsupported field | Validate against current schema |
| Include access denied | Triggering user cannot read policy project | Grant appropriate read access or configure supported automatic access |
| Duplicate jobs | Checks exist in both project and policy | Decide single ownership or remove duplicates |
| Cyclic dependency error | Conflicting project and policy stages | Align stage order and constraints |
| Project jobs disappear | `override_project_ci` replaced project config | Use `inject_policy` or explicitly include project config |
| Child policy jobs absent | Child enforcement not enabled/supported | Review `enforce_on_child_pipelines` |
| Bypass still possible | Skip policy not configured as expected | Review supported `skip_ci` and `no_pipeline` fields |

## Viva answers
1. **Pipeline execution policy:** Centrally enforces CI/CD jobs or configuration across selected projects.
2. **Security policy project:** A project that stores centrally managed security policy definitions and related configuration.
3. **`policy.yml`:** Defines security policies, their behavior, and scope.
4. **Execution vs scan policy:** Execution policy enforces CI jobs/configuration; scan policy enforces supported security scans.
5. **`inject_policy`:** Adds centrally managed policy CI configuration to project pipelines.
6. **`override_project_ci`:** Replaces the project's CI configuration with centrally managed configuration.
7. **`inject_ci`:** Deprecated; new policies should use `inject_policy`.
8. **Policy scope:** Determines which projects, groups, or compliance frameworks a policy affects.
9. **Cyclic dependency:** Project and policy stage ordering constraints cannot be satisfied together.
10. **`variables_override`:** Controls whether project configuration can override policy variables.
11. **Skip controls:** Prevent required pipelines or checks from being bypassed without approved exceptions.
12. **Pilot rollout:** Limits risk, reveals compatibility issues, and provides evidence before broad enforcement.

## Further reading
- [GitLab policies overview](https://docs.gitlab.com/user/application_security/policies/)
- [Pipeline execution policies](https://docs.gitlab.com/user/application_security/policies/pipeline_execution_policies/)
- [Scan execution policies](https://docs.gitlab.com/user/application_security/policies/scan_execution_policies/)
