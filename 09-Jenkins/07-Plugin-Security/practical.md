# Practical Exercises — Jenkins Plugin Security

Use a lab controller you own or are authorized to administer. Do not install untrusted plugin binaries or conduct destructive tests on production.

## Exercise 1: Build a plugin inventory
**Task**
1. Open **Manage Jenkins → Plugins** and review installed plugins.
2. Record plugin short name, installed version, enabled status, purpose, owner, and review date.
3. Mark plugins whose business purpose is unclear.

**Deliverable:** `plugin-inventory.csv` or a Markdown table.

**Acceptance criteria:** Every installed plugin is represented; unknown owners and purposes are flagged rather than guessed.

## Exercise 2: Review a security advisory
**Task**
1. Open the official Jenkins Security Advisories page.
2. Select an advisory that names a plugin.
3. Record affected versions, fixed version if provided, impact, and mitigation.
4. Compare the advisory with a lab plugin inventory.

**Deliverable:** A one-page advisory assessment with source URL and date reviewed.

**Acceptance criteria:** The assessment distinguishes confirmed exposure from an item requiring further investigation.

## Exercise 3: Risk-rank installed plugins
Assign each plugin a likelihood score (1–5) and impact score (1–5). Calculate `risk score = likelihood × impact`. Document the rationale and caveat that this simple score is a prioritization aid, not a formal vulnerability rating.

**Deliverable:** A prioritized list with action: keep, update, replace, disable, or remove.

## Exercise 4: Test an update in staging
**Task**
1. Back up the lab controller configuration and document the current plugin versions.
2. Select a plugin update from the approved update center.
3. Check Jenkins core compatibility and dependencies.
4. Apply the update in staging.
5. Restart if required and test jobs, agents, credentials integrations, and logs.
6. Record results and rollback steps.

**Deliverable:** Test report with pass/fail results and evidence.

## Exercise 5: Create a plugin approval checklist
Include:
- Business need and alternative considered
- Official plugin page and source repository
- Maintenance and release activity
- Security advisory review
- Core compatibility and dependency review
- Permissions and credential access
- License/support requirements
- Test plan, approver, and rollback plan

**Deliverable:** A reusable approval checklist.

## Exercise 6: Find unused or redundant plugins
Ask the relevant job owners whether each candidate plugin is still needed. Review job and pipeline references before removal. Disable only in a lab or approved maintenance window first, then verify dependent jobs.

**Deliverable:** A removal proposal with impact analysis and rollback plan.

## Exercise 7: Design an update cadence
Propose a schedule for checking advisories and reviewing the inventory. Define who owns urgent fixes, how exceptions are approved, and how evidence is retained. Critical advisories may require action outside the routine schedule.

**Deliverable:** A short plugin patch-management procedure.

## Exercise 8: Secure a pipeline that uses plugins
Review a sample pipeline for:
- Credentials exposed to untrusted pull requests
- Overly broad service accounts
- Secrets echoed to logs
- Unprotected deployment stages
- Unreviewed shared libraries
- Plugin-provided steps that execute shell commands or load external content

**Deliverable:** Findings, risk ratings, and specific remediation recommendations.

## Submission checklist
- [ ] Inventory includes owner and purpose.
- [ ] At least one official advisory is assessed.
- [ ] Risk scoring has documented rationale.
- [ ] Staging update test includes rollback steps.
- [ ] Approval and patch-management checklists are complete.
- [ ] Pipeline review includes credentials and trust boundaries.
