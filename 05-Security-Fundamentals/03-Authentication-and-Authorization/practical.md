# Practical Lab — Authentication and Authorization

## Goal
Build a security test plan for a fictional web application with customers, support agents, and administrators.

## Safety
Use a local lab, your own application, or a system you are explicitly authorized to assess. Do not attempt to access other people's accounts or production data.

## Lab A — Create an access matrix
Define at least three roles:
- Customer
- Support agent
- Administrator

For each role, list allowed actions for profile, orders, user management, and security settings. Use least privilege and document which actions require auditing.

## Lab B — Design a secure login flow
Document the steps from login submission through session creation. Include:
- HTTPS
- Password verification using a suitable password-hashing function
- Rate limiting and abuse detection
- MFA or step-up authentication where appropriate
- Session identifier rotation after login
- Secure cookie attributes
- Generic authentication errors that avoid revealing whether an account exists
- Recovery and account lockout/rate-limit behavior

## Lab C — Test object-level authorization
Using two test accounts you control:
1. Create a record for Account A.
2. Authenticate as Account B.
3. Request Account A's record through the application's normal API.
4. Verify the server denies access without returning the protected record.
5. Repeat for list, read, update, and delete operations where applicable.
6. Record the endpoint, test identity, expected result, actual result, and evidence.

Do not use real customer identifiers or data.

## Lab D — Test function-level authorization
Attempt administrative operations using a low-privilege test account. Verify that the server denies requests even if the client UI is modified or the endpoint is called directly.

## Lab E — Review sessions and recovery
Create test cases for:
- Logout invalidates the session.
- Session IDs rotate after authentication and privilege changes.
- Expired sessions are rejected.
- Password reset tokens expire and are single-use.
- MFA recovery does not silently bypass identity verification.
- Role or project membership removal revokes access as expected.

## Lab F — Write findings
For each failure, record summary and affected endpoint, preconditions and safe reproduction steps, security impact, evidence with secrets redacted, recommended remediation, and retest criteria.

## Submission checklist
- [ ] Role-permission matrix completed.
- [ ] Login flow includes secure credential handling and session creation.
- [ ] Object-level authorization tests completed with test accounts.
- [ ] Function-level authorization tests completed.
- [ ] Session, logout, and recovery tests documented.
- [ ] Evidence redacted and remediation criteria included.
