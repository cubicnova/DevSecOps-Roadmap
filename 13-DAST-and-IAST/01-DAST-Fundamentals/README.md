# 01 - DAST Fundamentals

## Learning objectives
By the end of this module, learners will be able to:

- Explain Dynamic Application Security Testing (DAST) and its black-box approach.
- Compare DAST with SAST, IAST, and manual penetration testing.
- Prepare an authorized, isolated target and define scan scope.
- Run a safe passive baseline scan and understand when active scanning is appropriate.
- Interpret alerts, validate evidence, prioritize risk, and document remediation.
- Explain crawling, authentication, API definition imports, coverage gaps, and CI/CD use.

## 1. What is DAST?
Dynamic Application Security Testing assesses an application while it is running. A scanner or tester sends HTTP(S) requests, observes responses, and looks for security weaknesses. It does not need access to source code. DAST is therefore commonly described as black-box testing.

Typical areas assessed include:
- Injection and output-handling weaknesses observable at runtime.
- Authentication and session-management behavior.
- Access-control behavior reachable through tested requests.
- Security headers, TLS configuration, and information disclosure.
- Server and application misconfiguration.
- API behavior when endpoints and schemas are supplied.

DAST reports are evidence for investigation, not automatic proof that every alert is exploitable.

## 2. DAST in the application security toolkit

| Approach | Primary view | When it is useful | Common limitation |
|---|---|---|---|
| SAST | Source code | Early feedback during development | May not observe deployed configuration or runtime behavior |
| DAST | Running application | Runtime behavior, deployed configuration, reachable endpoints | Requires a running target; coverage depends on crawling and authentication |
| IAST | Instrumented application during execution | Runtime findings with application execution context | Requires supported instrumentation and test execution |
| Manual penetration test | Human-led attacker perspective | Business logic, chained flaws, nuanced authorization | Time and tester expertise limit scale |

Use complementary techniques. DAST does not replace code review, threat modeling, or manual testing.

## 3. DAST workflow
1. **Authorization:** obtain written permission and identify the approved target.
2. **Environment:** prefer a disposable local or staging environment with synthetic data.
3. **Scope:** define hostnames, ports, paths, APIs, excluded routes, and scan window.
4. **Discovery:** map pages, forms, links, APIs, and application states.
5. **Authentication:** configure test accounts and verify that protected pages are reachable.
6. **Scanning:** start with passive checks; run active checks only in a controlled environment.
7. **Triage:** inspect the alert, request, response, evidence, and reproducibility.
8. **Remediation:** assign an owner, fix the root cause, and retest.
9. **Reporting:** record coverage, limitations, findings, and residual risk.

## 4. Safe target preparation
- Use only applications you own or are explicitly authorized to test.
- Recommended training targets: OWASP Juice Shop or WebGoat in a local container/VM.
- Keep vulnerable targets isolated; bind services to localhost where practical.
- Use synthetic accounts and data. Never put production secrets in scan configuration.
- Back up disposable data and reset the lab after destructive tests.
- Do not run active scans against public sites, production, or shared environments without explicit authorization and a coordinated test plan.

## 5. Scanner concepts
- **Spider/crawler:** discovers links and reachable resources.
- **AJAX/browser spider:** discovers client-side routes in JavaScript-heavy applications.
- **Passive scan:** evaluates observed traffic without sending attack payloads. Usually safer, but still creates traffic and may expose sensitive data in reports.
- **Active scan:** sends test payloads and may alter data, trigger workflows, or affect availability. Use only in isolated, approved environments.
- **Context/scope:** defines which URLs and applications belong to the assessment.
- **Authentication:** allows the scanner to reach protected functionality.
- **API import:** OpenAPI/Swagger or GraphQL definitions can improve endpoint discovery.
- **Alert confidence:** scanner confidence is not the same as business impact or confirmed exploitability.

## 6. Getting started with OWASP ZAP
Install ZAP from its official site and use the current supported release for your platform. The following examples assume ZAP is available as `zap.sh` on Linux/macOS or `zap.bat` on Windows.

### Passive baseline scan
For an authorized local lab:
```bash
zap-baseline.py -t http://127.0.0.1:3000 -r baseline-report.html
```
Depending on installation method, the script may be exposed through the ZAP Docker image or command-line package. Check the current ZAP documentation for the supported invocation on your platform.

### Docker-based baseline example
```bash
docker run --rm -t \
  -v "$(pwd):/zap/wrk/:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://host.docker.internal:3000 \
  -r baseline-report.html
```
`host.docker.internal` behavior differs by operating system and Docker configuration. On Linux, configure a suitable host gateway or place the scanner and target on the same isolated Docker network. Do not assume the hostname resolves in every environment.

### Active scan
An active scan is intentionally omitted as a copy/paste default. First review ZAP's active-scan guidance, scope, exclusions, policy, and target safety. Run it only against a disposable authorized lab.

## 7. Reading a DAST finding
For each alert, capture:
- Alert name and scanner rule ID.
- Affected URL, method, parameter, and user role.
- Severity and confidence as reported by the scanner.
- Evidence and the exact request/response.
- Reproduction steps in the approved lab.
- Business impact and affected data.
- Root cause, recommended fix, owner, due date, and retest result.

A useful validation sequence:
1. Reproduce with a harmless request in the lab.
2. Confirm the behavior is not expected application functionality.
3. Check encoding, validation, authorization, and server-side handling.
4. Test relevant roles and adjacent endpoints.
5. Record whether the issue is confirmed, false positive, accepted risk, or needs more investigation.

## 8. Coverage and limitations
DAST can miss:
- Unlinked routes, hidden APIs, and functionality behind login.
- Features that require complex multi-step workflows.
- Business-logic flaws that need human reasoning.
- Vulnerabilities that do not produce observable responses.
- Code paths not reached during the scan.
- Issues requiring specific roles, tenant boundaries, or unusual data states.

Improve coverage with authenticated contexts, role-specific test accounts, OpenAPI imports, recorded workflows, and manual testing. Report what was not tested.

## 9. CI/CD integration principles
A safe progression:
1. Run passive baseline checks against a disposable preview deployment.
2. Publish reports as build artifacts with access controls and retention limits.
3. Establish a reviewed baseline for existing alerts.
4. Add targeted active scans in isolated ephemeral environments.
5. Fail builds only on carefully selected, validated policy conditions.
6. Always tear down test infrastructure, including after failures.

Pin third-party CI actions to reviewed immutable commit SHAs where feasible. Protect credentials with the CI secret store and least privilege. Do not print tokens or full authenticated requests in logs.

## 10. Key terms
- **Black-box:** testing without source-code knowledge.
- **Attack surface:** reachable entry points and functionality.
- **Coverage:** proportion of relevant application behavior actually exercised.
- **False positive:** an alert that does not represent the claimed weakness.
- **False negative:** a real weakness the test failed to identify.
- **Baseline:** known findings used to compare later scans.
- **Retest:** validation that a remediation is effective.

## Knowledge check
1. Why does DAST require a running application?
2. What is the difference between passive and active scanning?
3. Why can a scan of only the home page provide poor coverage?
4. Why should authenticated scans use dedicated test accounts?
5. Why is a scanner alert not automatically a confirmed vulnerability?
6. Name two limitations of automated DAST.

## Further reading
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- OWASP DevSecOps Guideline - DAST: https://owasp.github.io/DevSecOpsGuideline/2-Process/2-4-Test/2-4-2-Dynamic-Application-Security-Testing/
- OWASP ZAP documentation: https://www.zaproxy.org/docs/
- OWASP Developer Guide - DAST tools: https://devguide.owasp.org/en/06-verification/02-tools/01-dast/
