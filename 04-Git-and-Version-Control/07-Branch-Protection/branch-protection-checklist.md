# Branch Protection Checklist

Use this checklist when setting up or auditing an important branch.

## Scope and ownership

- [ ] Target branch or pattern is correct (`main`, `release/*`, etc.).
- [ ] Repository owners and reviewers are identified.
- [ ] Rule matches the intended repository plan and permission model.
- [ ] Overlapping branch rules and rulesets have been reviewed.

## Pull requests and reviews

- [ ] Pull requests are required before merging.
- [ ] Required approval count matches the project's risk.
- [ ] Stale approvals are handled intentionally.
- [ ] Code owner review is enabled where useful and supported.
- [ ] Conversations must be resolved where appropriate.

## Quality gates

- [ ] Required status checks are real, stable, and named unambiguously.
- [ ] Tests and build checks run on the relevant pull requests.
- [ ] Security checks are included where appropriate.
- [ ] Up-to-date branch requirements match the team's merge workflow.
- [ ] Required deployment checks are configured if needed and supported.

## History and access

- [ ] Force pushes are blocked.
- [ ] Branch deletion is blocked.
- [ ] Signed commits or linear history are enabled if required by policy.
- [ ] Administrator behavior and bypass permissions are understood.
- [ ] Emergency exceptions are documented, authorized, and auditable.

## Verification

- [ ] A test pull request was opened.
- [ ] A missing approval correctly blocks merging.
- [ ] A failing required check correctly blocks merging.
- [ ] A passing, approved pull request can be merged.
- [ ] Configuration is reviewed periodically.
