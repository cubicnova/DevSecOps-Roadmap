# GitLab Pipeline Policies — Practical Exercises

## Lab prerequisites
- A GitLab instance and account with permissions to create a test group/project and security policy project.
- Confirm whether your GitLab tier supports the policy features used in this module. Pipeline execution policies are an Ultimate feature.
- A disposable project with a basic `.gitlab-ci.yml`.
- An eligible runner.
- Do not apply experimental policies to production projects.

## Exercise 1: Explore GitLab policies
1. Open the test group's or project's security policy area.
2. Identify available policy types.
3. Check whether pipeline execution policies and scan execution policies are available.
4. Record the GitLab version and tier.
5. Note which policy types are unavailable in your environment.

**Deliverable:** A short feature availability report.

## Exercise 2: Create a security policy project
1. Create a dedicated project for policy configuration.
2. Protect its default branch.
3. Restrict write access to a small policy-maintainer group.
4. Create `.gitlab/security-policies/policy.yml`.
5. Add a referenced directory such as `pipeline-config/`.

**Expected result:** A centrally managed repository for policy definitions and CI configuration.

## Exercise 3: Create a basic pipeline execution policy
1. Create a simple `required-checks.yml` file in the policy project.
2. Define one harmless policy job.
3. Add a pipeline execution policy referencing the file.
4. Apply it to a disposable pilot project.
5. Run a pipeline and confirm the policy job appears.

Use the current GitLab UI or API workflow and the current documented schema.

## Exercise 4: Compare configuration strategies
In a disposable project, compare:
- `inject_policy`
- `override_project_ci`

Record which project jobs remain, which policy jobs are added, and what happens to the project's existing pipeline configuration.

Do not use `override_project_ci` on a project whose pipeline must be preserved.

## Exercise 5: Test policy scope
1. Create two disposable projects.
2. Configure the policy to include only one project.
3. Run pipelines in both projects.
4. Confirm the policy is applied only where intended.
5. Add an exclusion and repeat.

**Deliverable:** A scope test matrix showing included and excluded projects.

## Exercise 6: Add a policy stage
1. Add a custom policy stage to the referenced CI configuration.
2. Test against a project using standard `build`, `test`, and `deploy` stages.
3. Change the project stage order in the lab to create an incompatible ordering.
4. Observe the pipeline creation error.
5. Correct the stage ordering.

**Expected result:** You can explain how conflicting stage constraints can create cyclic dependencies.

## Exercise 7: Test variable override controls
1. Define a non-sensitive test variable in project CI configuration.
2. Configure the policy's `variables_override` behavior.
3. Test with an allowed exception and a variable that is not allowed.
4. Review the effective values in job output without printing secrets.

**Deliverable:** A table showing allowed and blocked overrides.

## Exercise 8: Review skip directives
In a disposable project:
1. Review the policy fields for `[skip ci]` and `[no_pipeline]`.
2. Configure a test policy according to current documentation.
3. Test the behavior with an authorized test user.
4. Document how the policy affects developer workflows and automation.

Do not use skip directives to bypass production controls.

## Exercise 9: Compare pipeline execution and scan execution policies
1. Read the documentation for both policy types.
2. Identify one requirement best implemented by a pipeline execution policy.
3. Identify one requirement best implemented by a scan execution policy.
4. Explain why duplicating scan jobs in both project YAML and policy configuration can create confusion.

## Exercise 10: Test policy access
1. Identify the user who triggers the target project's pipeline.
2. Confirm the user has the required read access to the policy configuration.
3. Test pipeline creation with a permitted user.
4. In a disposable test only, review the failure behavior when access is missing.
5. Document the security policy project setting that can grant access automatically, if available.

## Exercise 11: Child pipeline behavior
1. Create a parent pipeline that triggers a child pipeline.
2. Review whether the policy applies to child pipelines by default.
3. If supported, enable `enforce_on_child_pipelines`.
4. Use `CI_PIPELINE_SOURCE` rules to limit a job to parent or child context.
5. Confirm no recursive pipeline creation occurs.

## Exercise 12: Policy governance review
Prepare a policy change proposal containing:
- Business and security objective.
- Policy type and scope.
- Configuration strategy.
- Required jobs and stages.
- Permissions and policy owners.
- Test evidence.
- Exception process.
- Monitoring and rollback plan.

## Submission checklist
- [ ] GitLab policy feature availability recorded.
- [ ] Security policy project created and protected.
- [ ] Basic pipeline execution policy tested in a pilot project.
- [ ] `inject_policy` and `override_project_ci` compared.
- [ ] Policy scope inclusion and exclusion tested.
- [ ] Custom policy stage tested.
- [ ] Variable override behavior reviewed.
- [ ] Skip directive behavior researched/tested.
- [ ] Scan execution policy compared with pipeline execution policy.
- [ ] Policy configuration access tested.
- [ ] Child pipeline behavior reviewed.
- [ ] Governance proposal submitted.

## Viva questions
1. What is a GitLab pipeline execution policy?
2. What is a security policy project?
3. What is the purpose of `policy.yml`?
4. Differentiate pipeline execution and scan execution policies.
5. What does `inject_policy` do?
6. What does `override_project_ci` do?
7. Why is `inject_ci` not recommended for new policies?
8. What is policy scope?
9. Why can stage conflicts cause a cyclic dependency error?
10. What is the purpose of `variables_override`?
11. Why control `[skip ci]` and `[no_pipeline]`?
12. Why should policies be rolled out to a pilot project first?
