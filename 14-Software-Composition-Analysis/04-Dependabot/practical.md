# Practical Exercises – Dependabot

## Lab 1: Enable dependency visibility
1. Open a GitHub repository where you have permission.
2. Review the repository's dependency graph and manifest detection.
3. Enable Dependabot alerts if available for the repository.
4. Record ecosystems and manifests detected.
**Deliverable:** dependency visibility record.

## Lab 2: Configure version updates
1. Create `.github/dependabot.yml` on the default branch.
2. Start with one ecosystem (for example, npm or pip).
3. Set the correct manifest directory and weekly schedule.
4. Validate YAML syntax and commit the configuration.
5. Observe the next scheduled run or trigger a supported manual check.
**Deliverable:** configuration and update PR evidence.

## Lab 3: Configure multiple ecosystems
Add entries only for ecosystems actually used in your repository. Include GitHub Actions if you want workflow action references monitored. Check every directory path and package ecosystem identifier against GitHub's official documentation.

## Lab 4: Security update workflow
1. Enable Dependabot alerts and security updates in repository settings.
2. Review an existing alert or use a deliberately vulnerable training repository.
3. Inspect the proposed security update PR.
4. Confirm the advisory, affected range, fixed version, and tests.
5. Record the merge or exception decision.
Do not introduce known vulnerable packages into production projects for this exercise.

## Lab 5: Grouping and cooldown
1. Add one version-update group for a low-risk dependency class.
2. Configure a cooldown for version updates.
3. If available, configure a separate security-update group using `applies-to: security-updates`.
4. Confirm the distinction: cooldown does not delay security updates.
5. Evaluate whether grouped PRs remain small and reviewable.

## Lab 6: Private registry security
Use a test registry and non-production token. Store credentials as repository or organization secrets, restrict token scope, and verify no secret is exposed in PR logs. Revoke the test token after the lab.

## Lab 7: Update PR review
Select a Dependabot PR and complete `templates/update-review.md`. Run project tests and inspect lockfile/transitive changes before recommending merge.

## Submission checklist
- [ ] Dependency graph review
- [ ] `.github/dependabot.yml`
- [ ] Security update settings evidence
- [ ] Grouping/cooldown configuration
- [ ] Private registry credential handling notes
- [ ] Completed update PR review
