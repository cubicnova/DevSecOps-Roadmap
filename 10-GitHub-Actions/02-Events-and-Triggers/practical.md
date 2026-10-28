# Practical Exercises — Events and Triggers

## Lab setup
Create a practice repository and add workflow files under `.github/workflows/`. Use a branch you control. Avoid production secrets and deployments during these exercises.

## Exercise 1: Push trigger
Create a workflow that runs on pushes to `main`. Make a harmless README edit and verify the run.

**Deliverable:** Workflow YAML and a screenshot or link to the successful run.

## Exercise 2: Pull request activity types
Configure a workflow for `opened`, `synchronize`, and `reopened` pull-request activities targeting `main`. Test by opening a PR and pushing another commit to its source branch.

**Deliverable:** A table mapping each activity to the expected run.

## Exercise 3: Branch and path filters
Create a workflow that runs on pushes to `main` only when files in `src/` or `tests/` change. Make separate commits that modify `src/`, `tests/`, and `docs/`.

**Deliverable:** Observed-versus-expected trigger matrix.

## Exercise 4: Manual workflow inputs
Create a `workflow_dispatch` workflow with a `choice` input for `dev` and `staging` and a boolean `dry_run` input. Validate input values before using them.

**Deliverable:** Workflow YAML and evidence of two manual runs.

## Exercise 5: Schedule syntax
Configure a workflow to run weekly using POSIX cron. Explain the selected minute, hour, weekday, and timezone. Keep `workflow_dispatch` enabled so you can test it manually.

**Deliverable:** Cron expression explanation and a manual test run. Do not wait for the scheduled run to validate YAML.

## Exercise 6: Issue event
Create a workflow triggered when an issue is opened. Give it only the permissions needed to add a triage label, and confirm the label exists.

**Deliverable:** Workflow and successful issue-labeling result.

## Exercise 7: Tag event
Create a workflow that runs when a tag matching `v*` is pushed. Create a test tag such as `v0.1.0` and push it to your test repository.

**Deliverable:** Run log showing the tag name and a note explaining why tag-triggered validation is not, by itself, authorization to deploy.

## Exercise 8: Diagnose a workflow that did not run
Given a workflow that appears not to trigger, investigate:
- File location and YAML syntax
- Event name and activity type
- Branch/tag/path filters
- Default-branch requirements for the event
- Workflow disabled or approval-required status
- Whether the event was created by `GITHUB_TOKEN`

**Deliverable:** Root cause, supporting evidence, and fix.

## Exercise 9: Event payload safety
Use environment variables to pass selected event fields into a shell step. Explain why direct expression interpolation into shell source can create injection risk.

**Deliverable:** Safe and unsafe snippets, plus a corrected example.

## Exercise 10: Threat-model `pull_request_target`
Read the official documentation and write a short threat model explaining the risk of checking out and executing untrusted pull-request code in a workflow with base-repository secrets or write permissions.

**Deliverable:** Risk statement and at least three mitigations.

## Completion checklist
- [ ] Push, pull request, manual, and scheduled triggers are understood.
- [ ] Branch/path/activity filters are tested.
- [ ] A tag or issue event is demonstrated.
- [ ] Workflow permissions are minimal.
- [ ] Event values are passed safely.
- [ ] `GITHUB_TOKEN` recursion behavior is understood.
- [ ] `pull_request_target` risks are documented.
