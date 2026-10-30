# Scan Configuration - Practical Exercises

## Safety rules
- Work only against a disposable local lab or an explicitly authorized target.
- Define scope before starting the scanner.
- Begin with passive scanning.
- Do not run active scans against production or public systems without explicit authorization and a coordinated plan.
- Exclude destructive routes and external integrations.
- Use synthetic data and protect reports.

## Exercise 1 - Create a scan scope
1. Choose a local training application.
2. Record its exact scheme, hostname, and port.
3. Define included and excluded paths.
4. Test include/exclude patterns against sample URLs.
5. Explain how you prevent scope creep.

**Deliverable:** Completed `templates/scope-record.md`.

## Exercise 2 - Create a ZAP Context
1. Create a new Context in ZAP.
2. Add the local application URLs.
3. Configure include and exclude regexes.
4. Confirm that only the intended host is in scope.
5. Export the Context for review.

**Deliverable:** Context export and a short explanation of each regex.

## Exercise 3 - Configure passive scanning
1. Browse the target through ZAP.
2. Confirm passive rules are enabled.
3. Review passive alerts.
4. Record the scan duration and traffic volume.
5. Explain why passive scanning is not risk-free.

**Deliverable:** Passive scan summary.

## Exercise 4 - Review active scan policy
1. Open the Scan Policy Manager.
2. Review enabled rules and categories.
3. Compare threshold and strength settings.
4. Create a named policy for a small local lab.
5. Document why each change was made.

**Deliverable:** Policy decision record. Do not launch active scanning unless the target is isolated and explicitly approved.

## Exercise 5 - Tune crawl coverage
1. Run the traditional spider.
2. Run an AJAX/browser spider if the app uses client-side routing.
3. Compare discovered URLs.
4. Change crawl depth or duration in a controlled test.
5. Record additional routes and scan-time impact.

**Deliverable:** Crawl comparison table.

## Exercise 6 - Configure exclusions
1. Identify logout, account deletion, payment, and admin destructive routes.
2. Add precise exclusions.
3. Verify excluded routes are not crawled or tested.
4. Ensure exclusions do not hide adjacent safe routes.

**Deliverable:** Exclusion list with rationale.

## Exercise 7 - Configure resource limits
1. Set a bounded scan duration.
2. Configure per-rule time limits where available.
3. Set conservative concurrency.
4. Run a passive scan and observe resource use.
5. Explain when the scan should be stopped.

**Deliverable:** Resource-limit record.

## Exercise 8 - Compare threshold and strength
In an isolated lab only:
1. Run a small approved policy at low strength.
2. Compare with a medium-strength policy.
3. Record scan duration, request count, and alert changes.
4. Explain why a higher threshold can reduce false positives but miss findings.

**Deliverable:** Comparison table and conclusion.

## Exercise 9 - Technology selection
1. Identify the technologies actually used by the lab.
2. Review ZAP's technology settings for the Context.
3. Exclude only technologies known not to be present.
4. Compare scan duration and rule coverage.
5. Explain why guessing the technology stack can reduce coverage.

**Deliverable:** Technology selection rationale.

## Exercise 10 - Version and policy governance
1. Record ZAP and add-on versions.
2. Export or document the scan policy.
3. Store the configuration in a version-controlled branch.
4. Propose a review process for rule changes and suppressions.
5. Define how a scanner upgrade is validated.

**Deliverable:** Configuration change checklist.

## Exercise 11 - Build separate scan profiles
Design three profiles:
- Pull-request passive baseline.
- API scan using an approved API definition.
- Scheduled active scan for an isolated staging environment.

For each, define scope, authentication, exclusions, rules, limits, report handling, and cleanup.

**Deliverable:** Three profile specifications.

## Exercise 12 - Final assessment
Prepare a reproducible scan configuration package containing:
- Scope and Context.
- Exclusions and rationale.
- Scan policy and rule status.
- Threshold and strength decisions.
- Crawl settings.
- Time/concurrency limits.
- Authentication requirements.
- Scanner/add-on versions.
- CI execution and report handling.
- Known limitations.

### Evaluation rubric (100 points)
| Area | Points |
|---|---:|
| Scope and Context | 15 |
| Passive/active distinction and safety | 15 |
| Policy and rule configuration | 20 |
| Crawl coverage and exclusions | 15 |
| Resource limits and performance | 10 |
| Versioning and governance | 10 |
| Profile design and CI integration | 10 |
| Documentation quality | 5 |
