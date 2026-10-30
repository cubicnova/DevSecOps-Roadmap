# DAST Scan Configuration Review Checklist

## Scope
- [ ] Exact target origin and environment recorded
- [ ] Context include regexes tested against full URLs
- [ ] Exclusions are narrow and justified
- [ ] External hosts are not followed unintentionally
- [ ] Written authorization and scan window confirmed

## Policy
- [ ] Passive and active scanning profiles are separate
- [ ] Active rules reviewed for the target and environment
- [ ] Threshold rationale documented
- [ ] Strength rationale documented
- [ ] Rule/add-on status and versions recorded
- [ ] Locked policy considered for repeatability

## Crawl and resources
- [ ] Spider type selected for application architecture
- [ ] Authentication and role coverage validated
- [ ] Crawl duration/depth bounded
- [ ] Scan and per-rule time limits configured
- [ ] Concurrency/request rate conservative
- [ ] Stop conditions defined

## Governance
- [ ] Configuration stored in version control
- [ ] Changes reviewed through pull request
- [ ] Suppressions include rationale, owner, and review date
- [ ] Scanner upgrades trigger policy validation
- [ ] Reports are access-controlled and retained appropriately
- [ ] Test data and environment cleaned up
