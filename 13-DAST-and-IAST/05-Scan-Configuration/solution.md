# Scan Configuration - Solutions and Guidance

Actual menu labels and configuration fields vary by ZAP release and add-ons. Verify all settings in the current ZAP documentation.

## Exercise 1 - Create a scan scope
A good scope identifies one exact origin, approved paths, excluded paths, scan window, and environment owner. Include only the application being tested. Document any external domains and do not automatically follow them.

## Exercise 2 - Create a Context
ZAP Context URL patterns are regular expressions matched against the whole URL. Test each expression with both expected matches and expected non-matches. Export the Context and review it before using it in automation.

## Exercise 3 - Configure passive scanning
Passive scanning evaluates traffic already observed by ZAP. It is generally less intrusive than active scanning, but crawling still generates requests and reports may retain sensitive response data. Protect artifacts and use bounded crawling.

## Exercise 4 - Review active scan policy
A policy defines which active rules run and how. Threshold affects the likelihood of alerts; strength affects how many attack requests a rule sends. Start conservatively. Record each rule change and the reason. Active scanning must be limited to owned or explicitly authorized environments.

## Exercise 5 - Tune crawl coverage
Traditional spidering is useful for link-based content. AJAX/browser spidering can discover client-side routes. Compare URL lists, but also review workflows, roles, and state transitions. More URLs do not necessarily mean better security coverage.

## Exercise 6 - Configure exclusions
Use narrow, tested patterns for logout and destructive actions. Avoid broad exclusions such as all `/admin/` routes unless the entire area is explicitly out of scope. Record the reason and owner for each exclusion.

## Exercise 7 - Configure resource limits
Set bounded duration, per-rule limits, and conservative concurrency. Monitor the lab application and stop if it becomes unstable or begins interacting with external systems. Tune based on observed lab behavior, not guesswork.

## Exercise 8 - Compare threshold and strength
Lower thresholds may produce more candidate alerts and false positives. Higher thresholds may suppress weaker evidence and increase false negatives. Higher strength usually increases requests and scan time. Compare alert instances and evidence, not only totals.

## Exercise 9 - Technology selection
Only exclude technologies that are confirmed absent. If the stack is unknown, retain broader coverage until it is identified. Record the basis for each technology decision and review it after application architecture changes.

## Exercise 10 - Version and policy governance
Record:
- ZAP version and add-on versions.
- Context and policy export.
- Enabled/disabled rules and rule status.
- Threshold and strength.
- Exclusions and suppression rationale.
- Scan duration and other limits.

Review configuration changes through pull requests. Revalidate policies when ZAP or add-ons are upgraded because rules and behavior can change.

## Exercise 11 - Build separate scan profiles

| Profile | Purpose | Typical safeguards |
|---|---|---|
| PR baseline | Fast feedback | Passive-only, bounded crawl, ephemeral app |
| API scan | Endpoint-focused testing | Imported API schema, exact host scope, test credentials |
| Scheduled active | Deeper probing | Isolated staging, approval, conservative policy, monitoring |

Keep the profiles separate. Do not allow a pull-request baseline to inherit active scan settings accidentally.

## Exercise 12 - Final assessment checklist
A complete package is reproducible and explains its trade-offs. Another tester should be able to identify the target, scope, exclusions, scanner versions, policy, crawl limits, and authentication setup without asking for undocumented information.

## Sample configuration review
> The scan configuration targets one isolated training application and uses a dedicated Context with explicit include and exclude patterns. The pull-request profile performs bounded passive scanning. Active rules are maintained in a separate approved policy and are not run by default. Threshold, strength, scanner version, add-ons, and resource limits are recorded. Exclusions have a rationale and are reviewed when routes change. Reports are access-controlled and the lab is removed after the scan.
