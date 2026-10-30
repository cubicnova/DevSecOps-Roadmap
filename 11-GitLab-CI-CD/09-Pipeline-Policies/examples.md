# GitLab Pipeline Policies — Examples

> These are learning examples. Policy schema and feature availability depend on GitLab version and tier. Validate every policy in a test security policy project before enforcing it broadly.

## 1. Basic pipeline execution policy

File: `.gitlab/security-policies/policy.yml`

```yaml
pipeline_execution_policy:
  - name: Required pipeline validation
    description: Add a centrally managed validation job
    enabled: true
    pipeline_config_strategy: inject_policy
    content:
      include:
        - project: my-group/security-policy-project
          file: pipeline-config/required-checks.yml
```

The project path and file path are placeholders.

## 2. Referenced policy CI configuration

File: `pipeline-config/required-checks.yml`

```yaml
policy-validation:
  stage: .pipeline-policy-pre
  image: alpine:3.20
  script:
    - echo "Running centrally managed validation"
    - test -n "$CI_PROJECT_PATH"
```

The reserved stage is designed for policy checks that must run before regular pipeline jobs. Confirm the behavior for your GitLab version.

## 3. Inject a custom policy stage

Policy CI configuration:

```yaml
stages:
  - test
  - policy-review
  - deploy

policy-review-job:
  stage: policy-review
  image: alpine:3.20
  script:
    - echo "Policy review completed"
```

When injecting custom stages, ensure the ordering constraints are compatible with stages in each target project's `.gitlab-ci.yml`. Incompatible constraints can produce a cyclic dependency error.

## 4. Scope a policy to selected projects

Illustrative scope structure:

```yaml
pipeline_execution_policy:
  - name: Pilot policy
    description: Apply only to the pilot project
    enabled: true
    pipeline_config_strategy: inject_policy
    policy_scope:
      projects:
        including:
          - id: 123
    content:
      include:
        - project: my-group/security-policy-project
          file: pipeline-config/required-checks.yml
```

Replace the example project ID with a real project ID. Confirm the exact scope schema for the policy type and GitLab version.

## 5. Exclude a project from a policy scope

```yaml
policy_scope:
  projects:
    excluding:
      - id: 456
```

This is a scope fragment, not a complete policy. Combine it with the supported policy schema and confirm whether other scope dimensions are also configured.

## 6. Restrict variable overrides

```yaml
variables_override:
  allowed: false
  exceptions:
    - CS_IMAGE
```

This illustrates a strict allowlist: policy variables cannot be overridden except for the named variable. Only use supported policy fields and exceptions. Review all variables that projects genuinely need.

## 7. Deny variables that disable scans (less preferred)

```yaml
variables_override:
  allowed: true
  exceptions:
    - SAST_DISABLED
    - SECRET_DETECTION_DISABLED
    - DEPENDENCY_SCANNING_DISABLED
```

This denylist approach can be weaker because any variable not listed as an exception may still be overridden. Prefer a strict allowlist where practical.

## 8. Control skip-ci behavior

Illustrative policy fragment:

```yaml
skip_ci:
  allowed: false
  allowlist:
    users:
      - id: 75
```

This prevents general use of the skip directive while allowing the specified user. User IDs are examples only. Confirm the current policy schema and organizational requirements.

## 9. Control no-pipeline behavior

```yaml
no_pipeline:
  allowed: false
  allowlist:
    users:
      - id: 75
```

This fragment controls the `[no_pipeline]` directive where supported. Test developer workflows and automation before enforcing it.

## 10. Override project CI configuration

```yaml
pipeline_execution_policy:
  - name: Standardized pipeline
    description: Centrally managed CI configuration
    enabled: true
    pipeline_config_strategy: override_project_ci
    content:
      include:
        - project: my-group/security-policy-project
          file: pipeline-config/standard-pipeline.yml
```

This strategy replaces the project's existing CI configuration unless the policy explicitly includes it. Use only when the organization intends to own the complete pipeline and has tested the effect on all project workflows.

## 11. Child pipeline enforcement

```yaml
pipeline_execution_policy:
  - name: Enforce checks in child pipelines
    description: Apply policy jobs to child pipelines
    enabled: true
    pipeline_config_strategy: inject_policy
    enforce_on_child_pipelines: true
    content:
      include:
        - project: my-group/security-policy-project
          file: pipeline-config/required-checks.yml
```

Check that your GitLab version supports this field. Policy jobs can run in parent and child pipelines; use `rules` with `CI_PIPELINE_SOURCE` if the job should run in only one context.

## 12. Scan execution policy vs pipeline execution policy

A pipeline execution policy is appropriate for enforcing custom CI jobs or pipeline configuration. A scan execution policy is appropriate for centrally enforcing supported security scans. Configure each using its own documented schema rather than copying one policy type's YAML into another.

## 13. Policy CI job with a simple allowlist check

```yaml
approved-branch-check:
  stage: .pipeline-policy-pre
  image: alpine:3.20
  script:
    - |
      case "$CI_COMMIT_BRANCH" in
        main|release/*)
          echo "Branch is permitted for this example"
          ;;
        *)
          echo "This example policy rejects this branch"
          exit 1
          ;;
      esac
```

This is a simple demonstration, not a complete organization-wide branch governance control. Consider merge request pipelines, tags, schedules, detached pipelines, and default branch names before adopting any branch policy.

## 14. Policy change review checklist

```text
[ ] Policy schema validates
[ ] Referenced CI file exists
[ ] Target projects can read the policy configuration
[ ] Scope includes intended projects only
[ ] Project stages are compatible
[ ] Merge request and branch pipelines tested
[ ] Child pipeline behavior tested if applicable
[ ] No duplicate or missing mandatory jobs
[ ] Skip/bypass behavior reviewed
[ ] Rollback procedure documented
```
