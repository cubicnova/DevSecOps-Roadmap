# Practical Labs: Security Review Checklists

Use a toy application, intentionally vulnerable training environment, or code you are authorized to review. Do not test production systems without explicit authorization.

## Lab 1 — Review an API change
Scenario: A pull request adds an endpoint to download an invoice using an ID from the URL.

Tasks:
1. Select applicable checklist sections.
2. Write at least eight review questions.
3. Identify positive and negative authorization tests.
4. Record one hypothetical finding with evidence and remediation.

## Lab 2 — Review authentication changes
Scenario: A feature adds password reset and session invalidation.

Tasks:
- Review reset-token generation, expiry, single-use behavior, and storage.
- Check for account enumeration and rate limiting.
- Check session invalidation after password reset.
- Review logs and error messages for secret leakage.
- Create a small test matrix for success and failure paths.

## Lab 3 — Review a dependency update
Tasks:
- Inspect package name, version, lockfile, and source.
- Identify known vulnerabilities and maintenance signals.
- Review permissions, install scripts, and transitive dependencies where relevant.
- Record a decision: approve, request changes, or escalate.

## Lab 4 — Review CI/CD workflow permissions
Scenario: A pull request workflow needs tests, while a release workflow deploys to production.

Tasks:
- Separate untrusted build/test work from privileged deployment.
- Define minimum permissions for each workflow.
- Explain how secrets are protected from forked pull requests.
- Check action pinning, artifact provenance, and branch protections.

## Lab 5 — Review file upload
Tasks:
- Apply the input-validation, API, authorization, data-storage, and logging checklists.
- Identify at least six abuse cases.
- Write positive and negative tests.
- Propose safe quarantine and scanning behavior.

## Lab 6 — Review infrastructure-as-code
Scenario: A Terraform change creates a storage bucket and a service role.

Tasks:
- Review public access, encryption, logging, retention, and access policy.
- Review role permissions and trust policy.
- Check environment separation and secret handling.
- Record what static scans can validate and what requires deployment/runtime verification.

## Lab 7 — Review a business workflow
Scenario: A user can request a refund and an administrator can approve it.

Tasks:
- Identify required states and allowed transitions.
- Test direct API calls that skip a workflow step.
- Consider concurrent approvals, duplicate requests, and replay.
- Check object-level authorization and audit trails.

## Lab 8 — Run a mock security review
Pick a small feature and complete:
1. Scope and risk summary.
2. Relevant checklist statuses.
3. Evidence links or test names.
4. Findings with severity rationale.
5. Owners and due dates.
6. Merge/release decision.
7. Retest and closure notes.

## Lab 9 — Checklist quality review
Review the included `checklists.md`.

Tasks:
- Identify items that are too vague for a pass/fail decision.
- Rewrite three items as verifiable questions.
- Identify two technology-specific items that should be marked N/A when irrelevant.
- Suggest one checklist improvement based on a realistic failure mode.

## Submission checklist
- [ ] Scope and diff are recorded.
- [ ] Relevant checklists are selected.
- [ ] Statuses are supported by evidence.
- [ ] Findings include impact and remediation.
- [ ] High-risk issues are escalated according to policy.
- [ ] Retest and closure evidence are recorded.
