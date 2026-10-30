# SAST Fundamentals

## Overview
Static Application Security Testing (SAST) analyzes source code, bytecode, or related application files without requiring the application to run. It helps developers identify security weaknesses early in the software development lifecycle.

SAST is commonly integrated into CI/CD pipelines so code can be scanned during commits and merge requests. Findings should be reviewed, validated, prioritized, fixed, and verified with a subsequent scan.

## Learning objectives
- Explain SAST and its role in the Secure Software Development Lifecycle (SSDLC).
- Differentiate SAST from DAST, IAST, SCA, and manual code review.
- Understand source, sink, sanitization, and taint analysis.
- Identify common weakness classes such as injection, XSS, path traversal, and insecure deserialization.
- Understand static analyzer rules, findings, severity, confidence, and false positives.
- Enable GitLab SAST in a project.
- Interpret a SAST report and remediate a finding.
- Understand SAST limitations and secure scanning practices.

## What is SAST?
SAST examines application code and related files to identify potentially insecure patterns. Depending on the scanner, analysis can include:
- Pattern and rule-based matching.
- Abstract syntax tree (AST) analysis.
- Data-flow and control-flow analysis.
- Taint analysis across sources and sinks.
- Framework-aware analysis.

SAST is generally performed early in development, often before deployment or execution of the application.

## SAST in the SSDLC

| SDLC phase | SAST contribution |
|---|---|
| Requirements | Define secure coding requirements and security acceptance criteria |
| Design | Identify trust boundaries and potential sources/sinks |
| Development | Scan code as developers implement features |
| Code review | Provide findings for reviewer validation |
| CI/CD | Run automated scans on branches and merge requests |
| Release | Review unresolved high-risk findings |
| Maintenance | Rescan after changes and update scanner rules |

## SAST vs other testing approaches

| Approach | Target | Requires running application? | Typical use |
|---|---|---:|---|
| SAST | Source code or compiled artifacts | No | Find insecure code patterns and data flows |
| DAST | Running application | Yes | Test externally observable runtime behavior |
| IAST | Application runtime with instrumentation | Yes | Observe data flows during test execution |
| SCA | Third-party components and dependencies | Usually no | Identify vulnerable or risky packages and licenses |
| Manual code review | Source code and design | No | Validate logic, context, and complex security issues |

These techniques complement one another. No single scanner proves that an application is secure.

## Core SAST concepts

### Source
A source is an origin of data that may be controlled by an attacker. Examples:
- HTTP query parameters.
- Request body fields.
- HTTP headers.
- Uploaded files.
- Environment variables or external input.

### Sink
A sink is a sensitive operation where unsafe data can cause a security issue. Examples:
- SQL query execution.
- Shell command execution.
- HTML output rendering.
- File path operations.
- Deserialization functions.

### Sanitization and validation
Validation checks whether input meets expected constraints. Sanitization or context-aware encoding transforms data to reduce risk. The correct defense depends on the sink and output context.

### Taint analysis
Taint analysis follows potentially untrusted data from a source through program operations toward a sensitive sink. A finding may be reported when the analyzer detects a path without an effective recognized defense.

## Common weakness classes

| Weakness | Example | Typical mitigation |
|---|---|---|
| SQL injection | Concatenating user input into SQL | Parameterized queries |
| Cross-site scripting (XSS) | Rendering untrusted data as HTML | Context-aware output encoding and safe templating |
| Command injection | Building shell commands from input | Avoid shell invocation; use safe APIs and argument arrays |
| Path traversal | Joining user-controlled paths without validation | Canonicalize paths and enforce a trusted base directory |
| Insecure deserialization | Deserializing untrusted data | Avoid unsafe formats/APIs; validate types and integrity |
| Hard-coded secrets | API key committed in source | Secret manager and credential rotation |
| Weak cryptography | Deprecated algorithm or insecure mode | Approved cryptographic libraries and modern algorithms |
| Improper access control | Missing authorization check | Enforce server-side authorization on every protected action |

## Static analysis workflow
1. Select the repository and supported language.
2. Select a SAST analyzer and ruleset.
3. Parse or build the source as required by the analyzer.
4. Analyze source patterns, control flow, or data flow.
5. Generate findings with locations and metadata.
6. Review findings and validate their context.
7. Fix confirmed weaknesses.
8. Rescan and verify remediation.

## GitLab SAST fundamentals

GitLab provides SAST templates and analyzers. The standard template can automatically select analyzers based on languages detected in the repository.

Add this to `.gitlab-ci.yml`:

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

The default SAST jobs generally use the `test` stage. If you redefine `stages`, include the required `test` stage or configure jobs according to the current template documentation.

Basic pipeline example:

```yaml
stages:
  - build
  - test

include:
  - template: Jobs/SAST.gitlab-ci.yml

build_app:
  stage: build
  image: alpine:3.20
  script:
    - echo "Build step placeholder"
```

SAST runs only when the relevant template rules and project conditions are met. A repository must contain supported files for an analyzer to scan.

## Understanding SAST findings
Review each finding using:
- **Rule / identifier:** Which weakness or rule was triggered?
- **Location:** File and line or code region.
- **Severity:** Potential impact rating.
- **Confidence:** How certain the analyzer is.
- **Data flow:** Source-to-sink path, if provided.
- **CWE:** Common Weakness Enumeration reference.
- **Remediation:** Recommended code change.
- **Reachability and context:** Is the vulnerable path reachable and exploitable in this application?

A finding is not automatically a confirmed exploitable vulnerability. Validate it with code context and tests.

## False positives and false negatives
- **False positive:** The scanner reports a weakness that is not actually present or exploitable in the relevant context.
- **False negative:** A real weakness is not detected.

Reduce false positives by understanding the code path, framework, validation, and scanner rules. Reduce false negatives by combining scanners, code review, testing, and threat modeling.

Do not suppress findings simply to make a pipeline green. Document the rationale, owner, scope, and review date for accepted risks or exclusions.

## GitLab SAST configuration basics
Common configuration options include:
- `SAST_EXCLUDED_PATHS`: Excludes selected paths from scanning.
- `SAST_ANALYZER_IMAGE_TAG`: Pins an analyzer image version for a specific analyzer job.
- `SAST_IMAGE_SUFFIX`: Selects an image suffix, such as a FIPS-enabled image where supported.
- Job overrides: Customize a SAST job by declaring a job with the same name after including the template.

Example path exclusion:

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml

variables:
  SAST_EXCLUDED_PATHS: "spec,test,tests,tmp"
```

Be careful: setting this variable can override default excluded paths. Copy the defaults when adding exclusions if you intend to preserve them. Exclusions reduce coverage and should be reviewed.

## Limitations
- SAST may not understand all runtime behavior or application configuration.
- Language and framework support differs by analyzer and version.
- Dynamic code generation and reflection can be difficult to analyze.
- Some analyzers need a successful build or dependency resolution.
- Findings can require manual validation.
- SAST cannot fully assess business logic, deployment configuration, or runtime infrastructure.
- A clean scan does not guarantee the absence of vulnerabilities.

## Recommended practices
1. Run SAST frequently, including on merge requests where supported.
2. Use supported analyzer versions and review updates.
3. Keep scan configuration under version control.
4. Use a test branch before changing rules or exclusions.
5. Prioritize reachable, high-impact findings.
6. Fix root causes instead of applying superficial filters.
7. Combine SAST with DAST, SCA, secret detection, and manual review.
8. Protect source code and scan reports as sensitive information.
9. Monitor scan failures; do not silently ignore missing results.
10. Record risk acceptance with an owner and review date.

## References
- [GitLab SAST documentation](https://docs.gitlab.com/user/application_security/sast/)
- [GitLab SAST analyzers](https://docs.gitlab.com/user/application_security/sast/analyzers/)
- [GitLab SAST rules](https://docs.gitlab.com/user/application_security/sast/rules/)
- [OWASP Source Code Analysis Tools](https://owasp.org/www-community/Source_Code_Analysis_Tools)
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)
