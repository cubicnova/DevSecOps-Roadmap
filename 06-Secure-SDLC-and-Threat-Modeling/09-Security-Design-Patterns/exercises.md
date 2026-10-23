# Security Design Patterns — Exercises

Use a local lab or a system you are authorized to assess. Explain assumptions and trade-offs; more than one design can be valid when justified.

## Exercise 1: Identify the pattern

Match each situation to one or more patterns.

1. A service account has administrator access to every cloud resource.
2. A policy-service timeout causes a protected export to proceed.
3. A client can access another tenant's record by changing an ID.
4. Developers place production credentials in a `.env` file committed to Git.
5. Repeated OTP attempts are unlimited.
6. A single person can modify code, approve it, and deploy it to production.
7. A public API accepts unlimited request bodies.
8. A client receives stack traces and connection strings after an exception.

For each, state the risk and a safer pattern.

## Exercise 2: Design a secure document API

A SaaS application stores confidential documents for multiple organizations. It has users, tenant administrators, and a background report worker.

Write design requirements for:
- Authentication and MFA
- Tenant isolation and resource authorization
- Workload identity and least privilege
- Encryption in transit and at rest
- Secrets and key management
- Rate limiting and abuse monitoring
- Audit logging and retention
- Safe errors and dependency failures

Include at least eight requirements and make each one verifiable.

## Exercise 3: Gateway-only authorization review

A design diagram shows a gateway validating a token. Internal services accept any request arriving from the private network and trust an `X-User-Role` header supplied by the gateway.

1. Identify at least three assumptions or weaknesses.
2. Propose a safer trust model.
3. Explain which controls belong at the gateway and which belong in each service.
4. Write three negative tests.

## Exercise 4: Choose between patterns

For each case, choose a suitable pattern and explain a trade-off:
- Centralized identity provider versus custom authentication.
- Fail-closed authorization versus availability during policy-service outage.
- API gateway versus direct service exposure.
- Synchronous policy lookup versus cached authorization decisions.
- Long-lived static secret versus short-lived workload identity.

Your answer must identify conditions under which the choice might change.

## Exercise 5: Create an ADR

Write an Architecture Decision Record for one of these decisions:
- Adopt a centralized identity provider.
- Introduce a secrets manager.
- Add an API gateway.
- Require independent production deployment approval.
- Adopt mutual TLS between selected services.

Include context, decision, alternatives, security consequences, operational consequences, and validation plan.

## Exercise 6: Security test plan

For a multi-tenant document API, write test cases covering:
- Valid access within the same tenant
- Cross-tenant read and write
- Expired or invalid tokens
- Read-only role attempting a privileged action
- Authorization service timeout
- Oversized request
- Rate-limit behavior
- Sensitive data in logs
- Duplicate submission of a sensitive operation

State expected results and evidence to collect.

## Exercise 7: Review a weak design

A service has the following properties:
- Public database port
- Hardcoded API key
- No resource-level authorization
- Debug errors enabled in production
- Logs contain bearer tokens
- One broad service account is shared by all workloads

Create a prioritized remediation plan. Explain immediate containment, architecture changes, testing, and ownership.

## Exercise 8: Pattern limitations

Choose three patterns from the README. For each:
1. State the problem it addresses.
2. Describe what it does not protect against.
3. Identify a failure mode or misuse.
4. Name a test or monitoring signal that provides evidence the pattern works.

## Exercise 9: Abuse case and controls

An attacker creates many accounts and uses a password-reset flow to enumerate users and overwhelm support.

Identify:
- Assets and trust boundaries
- Abuse cases
- Design patterns and controls
- Privacy and usability trade-offs
- Detection and response signals
- Negative tests

## Exercise 10: Mini design review

Draw or describe the architecture of a small web application with a browser, API, identity provider, database, and background worker. Mark trust boundaries and annotate at least six security patterns. For each pattern, identify an implementation owner and a test.

## Submission checklist

- [ ] Requirements are specific and testable.
- [ ] Authentication and authorization are distinguished.
- [ ] Trust boundaries and data flows are documented.
- [ ] Failure behavior is explicitly designed.
- [ ] Least privilege applies to users and workloads.
- [ ] Logging and monitoring avoid leaking sensitive data.
- [ ] Tests include denial paths and abuse cases.
- [ ] Trade-offs and residual risks are documented.
