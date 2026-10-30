# Attack Trees and Abuse Cases

Learn to model attacker goals as attack trees, describe malicious or unintended use through abuse cases, and translate the analysis into security requirements and testable acceptance criteria.

## Learning objectives

By completing this module, you should be able to:

- Distinguish normal use cases, misuse cases, abuse cases, threats, and vulnerabilities.
- Build attack trees with a clear root goal, subgoals, prerequisites, and AND/OR relationships.
- Identify attacker goals, capabilities, opportunities, and constraints without assuming every path is feasible.
- Write structured abuse cases with preconditions, steps, outcomes, business impact, and mitigations.
- Connect attack paths and abuse cases to risk decisions, security requirements, and negative tests.
- Review and update models as application features and trust boundaries change.

## Prerequisites

Recommended: basic application threat modeling, assets, trust boundaries, STRIDE, and risk assessment.

## Key concepts

| Concept | Meaning | Example |
|---|---|---|
| Use case | A legitimate actor achieves an intended goal | A customer downloads their invoice |
| Misuse case | A system or feature is used in an unintended way, not necessarily malicious | A user repeatedly retries a workflow and causes duplicate records |
| Abuse case | A malicious actor intentionally uses a feature to cause harm or bypass intended controls | A user attempts to download another customer's invoice |
| Attack tree | A hierarchical model of ways an attacker might reach a goal | Root goal: access a private invoice |
| Attack path | A possible route through a tree to the root goal | Exploit missing authorization after signing in |
| Prerequisite | A condition needed for a path to work | Attacker has a valid low-privilege account |
| Mitigation | A control or design change that reduces a path's feasibility or impact | Enforce server-side object-level authorization |
| Negative security test | A test that verifies a forbidden action is denied or safely handled | User A cannot retrieve User B's invoice |

Terminology varies across teams and references. The important practice is to describe the intended behavior, the harmful scenario, and the protection required.

## Attack trees

An attack tree begins with an attacker goal at the root and decomposes it into subgoals or actions.

- **OR relationship:** any one child path can achieve the parent goal.
- **AND relationship:** all required child conditions or steps must be satisfied.
- **Leaf node:** a lower-level action or prerequisite that may be assessed or tested.
- **Prerequisite:** a condition such as account access, a leaked token, or a vulnerable configuration.

### Example: access another user's invoice

```text
Goal: Access a private invoice
|
+-- OR: Abuse an application feature
|   +-- Change invoice ID in a request
|   +-- Exploit missing object-level authorization
|
+-- OR: Abuse a sharing mechanism
|   +-- Obtain a valid share link
|   +-- Use the link outside its intended audience or lifetime
|
+-- OR: Compromise an authorized session
    +-- Obtain a session token through a separate compromise
    +-- Reuse the token before it is revoked or expires
```

The branches are alternative conceptual paths. The tree does not assert that any path works in a real application. Validate each path against architecture, controls, and authorized test evidence.

### Building an attack tree

1. Define one precise, attacker-centered root goal.
2. Set the scope and identify protected assets.
3. Ask what broad alternatives could achieve the goal.
4. Decompose alternatives into concrete actions and prerequisites.
5. Mark AND/OR logic clearly.
6. Record assumptions, attacker capability, and required access.
7. Estimate likelihood, impact, and uncertainty for important paths.
8. Select controls that break or constrain paths.
9. Derive negative tests to verify the controls.
10. Revisit the tree when architecture or features change.

Avoid trees that are too broad (“hack the system”) or that simply list vulnerability names without explaining how they lead to the root goal.

## Abuse cases

An abuse case describes how a feature could be used to achieve an unintended or harmful outcome. A useful record includes:

- ID and title
- Feature and legitimate use case
- Threat actor and motivation
- Preconditions and required access
- Abuse scenario, step by step
- Expected secure behavior
- Impact and risk rationale
- Preventive and detective controls
- Security requirements and validation tests
- Owner, status, and residual-risk decision

### Example: password reset abuse case

**Legitimate use case:** A user who cannot sign in requests a password-reset link.

**Abuse case:** An attacker repeatedly submits reset requests to overwhelm the user or uses differences in responses to discover registered accounts.

**Preconditions:** Public reset endpoint; attacker can send requests.

**Expected secure behavior:**
- Responses do not unnecessarily disclose whether an account exists.
- Requests are rate-limited and monitored.
- Reset tokens are unpredictable, time-limited, single-use, and protected from leakage.
- Successful password changes invalidate appropriate outstanding reset tokens and follow the session-revocation policy.

**Validation:** Test existing and nonexistent accounts for response behavior, controlled rate-limit tests, expired-token tests, replay tests, and token-redaction checks.

## From model to engineering work

| Model finding | Engineering output |
|---|---|
| Attack path depends on trusting a client-supplied role | Requirement: authorization decisions use trusted server-side identity and permissions |
| Abuse case allows unlimited password-reset requests | Requirement: documented throttling and monitoring behavior |
| Share links remain valid indefinitely | Requirement: links have defined scope, expiry, and revocation behavior |
| Attack path relies on cross-account object access | Test: one test account cannot access another account's private object |
| Important action cannot be investigated | Requirement: protected audit event with actor, target, timestamp, and outcome |

A useful security requirement states observable behavior and can be verified. “Make it secure” is not sufficient.

## Prioritization

Use the organization's approved risk method. For each path, consider:
- Asset value and business impact
- Required attacker access and capability
- Exposure and ease of reaching the feature
- Existing controls and their reliability
- Likelihood, uncertainty, and exploit prerequisites
- Number of affected users or records
- Cost and feasibility of mitigation

Do not assume a complex attack tree is automatically higher risk than a short path. One low-effort path with severe impact may deserve priority.

## Deliverables checklist

- [ ] Root attacker goal is specific and in scope.
- [ ] AND/OR relationships and prerequisites are clear.
- [ ] Abuse cases describe steps and harmful outcomes.
- [ ] Assumptions and unknowns are recorded.
- [ ] Important paths have risk rationale.
- [ ] Mitigations map to paths or abuse steps.
- [ ] Negative tests demonstrate the expected secure behavior.
- [ ] Owners and review triggers are documented.

## References

- [OWASP Abuse Case Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Abuse_Case_Cheat_Sheet.html)
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
- [OWASP Threat Modeling Project](https://owasp.github.io/www-project-threat-modeling/)
- [OWASP Web Security Testing Guide: use and misuse cases](https://owasp.org/www-project-web-security-testing-guide/)

## Responsible practice

Use attack trees for defensive design reviews and authorized security testing. The examples in this module are conceptual and should not be used to test third-party systems without permission.
