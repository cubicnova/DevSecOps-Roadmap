# Secure SDLC — Exercises

Use a fictional application or a project you own or are authorized to test.

## Exercise 1: SDLC mapping

For each phase—requirements, design, development, build, testing, release, operations, and retirement—list two security activities and one piece of evidence.

## Exercise 2: Improve vague requirements

Rewrite these as testable requirements:
1. “The application must be secure.”
2. “Only authorized users can see data.”
3. “Secrets should be protected.”
4. “We must fix vulnerabilities quickly.”

Include a way to verify each requirement.

## Exercise 3: Threat modeling

For a web application with a browser, API, database, and third-party email provider:
- Identify at least four assets.
- Mark at least two trust boundaries.
- Write five plausible threats.
- Propose a mitigation and a verification method for each.

## Exercise 4: Choose security checks

Select appropriate checks for:
- A Python API repository
- A Terraform infrastructure repository
- A containerized web application

For each check, state what it can detect and one limitation.

## Exercise 5: Design a release gate

Create a release-gate policy that defines:
- Which findings block release
- Who reviews ambiguous or high-risk findings
- How exceptions are approved and expire
- What evidence is required before release
- How fixes are verified after deployment

## Exercise 6: Vulnerability ticket

Write a ticket for a confirmed high-risk dependency vulnerability. Include asset, evidence, risk rationale, owner, target date, remediation plan, test/rollback plan, verification, and closure evidence.

## Exercise 7: Secrets handling

A developer accidentally commits an API key to a repository.

Describe the response steps. Include revocation/rotation, history and log considerations, impact assessment, safe storage, and prevention. Explain why deleting the line from the latest commit alone may not be enough.

## Exercise 8: Review a pipeline

A pipeline runs unit tests but has no dependency scanning, secret scanning, or deployment permission controls.

Identify at least five risks and propose improvements. Include a way to avoid exposing production credentials to untrusted pull-request code.

## Exercise 9: Metrics

Choose four Secure SDLC metrics. Explain what each measures and one way it could be misinterpreted without context.

## Exercise 10: Practical mini-project

For a demo app:
1. Write five security requirements.
2. Create a lightweight threat model.
3. Add a code-review checklist.
4. Define at least three automated checks.
5. Specify a release gate and exception process.
6. Create a sample finding ticket.
7. Define post-release monitoring and verification.
8. Summarize the work in a short README section.

## Exercise 11: Reflection

In 150–250 words, explain why automated scanning is valuable but insufficient on its own for a Secure SDLC.
