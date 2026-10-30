# Finding Triage — Solutions and Reference Answers

These are reference approaches. Adapt status names, severity mappings, risk scoring, and SLAs to your organization's policy and contractual requirements.

## Solution 1 — Finding inventory

A useful minimum schema:

```text
finding_id
source_tool
source_rule_id
title
asset
repository_or_endpoint
commit_or_version
location
severity_original
severity_normalized
confidence
status
first_seen
last_seen
owner
evidence_reference
```

Keep the raw report immutable or versioned. The normalized record should link back to it.

## Solution 2 — Normalize scanner output

Example normalized record:

```json
{
  "finding_id": "APPSEC-1042",
  "source": {
    "tool": "ExampleScanner",
    "rule_id": "PY-SQL-001",
    "raw_severity": "ERROR"
  },
  "asset": "customer-api",
  "location": {
    "file": "src/search.py",
    "line": 42
  },
  "severity": "high",
  "confidence": "high",
  "status": "needs-triage",
  "evidence_ref": "restricted://evidence/APPSEC-1042"
}
```

Normalization must not discard original severity, tool identifiers, or evidence. Document how each source scale maps to the common scale.

## Solution 3 — Deduplication

Good deduplication keys depend on finding type.

| Finding type | Useful comparison fields |
|---|---|
| SAST | Rule/CWE, file, method, source-to-sink path |
| DAST/API | Host, method, endpoint, parameter, root cause |
| SCA | Package URL/name, version, CVE, dependency path |
| Container | Image digest, package, version, CVE |
| IaC | Resource identity, configuration path, rule ID |

Do not merge two findings just because they share a CWE or CVE. Preserve scanner-specific instances and evidence under a canonical issue.

## Solution 4 — SAST validation

Example unsafe code:

```python
def search_users(name, db):
    sql = "SELECT * FROM users WHERE name = '" + name + "'"
    return db.execute(sql)
```

Validation:
1. Confirm the exact commit and line.
2. Trace `name` to its source.
3. Confirm it is untrusted input.
4. Confirm the string reaches SQL execution.
5. Check for parameterized queries or effective controls.
6. Reproduce in a local test database if needed.

Safer code:

```python
def search_users(name, db):
    return db.execute(
        "SELECT * FROM users WHERE name = ?",
        (name,)
    )
```

Retest the original case and verify the parameter is treated as data.

## Solution 5 — DAST/API validation

A sound validation record includes:
- Authorized target and test identity.
- Exact method and endpoint.
- Sanitized request and response.
- Expected versus observed behavior.
- Reproduction steps.
- Impact and scope.
- Reviewer and verdict.

A scanner status code alone is not enough. Check response content and side effects.

## Solution 6 — Disposition decisions

Example classification guidance:

| Disposition | Evidence required |
|---|---|
| Confirmed | Reproducible or sufficiently supported vulnerability |
| False positive | Evidence shows the reported condition is not present |
| Duplicate | Same root cause/remediation already tracked |
| Accepted risk | Real residual risk with accountable approval and expiry |
| Needs investigation | Missing evidence, owner, and next action |
| Not applicable | Asset or behavior is demonstrably outside scope |

Never use “false positive” to mean “we do not plan to fix it.”

## Solution 7 — Risk prioritization

A useful decision process:
1. Identify known exploitation signals for CVEs (CISA KEV).
2. Consider exploit probability (EPSS) as one signal, not proof.
3. Confirm affected component and reachability.
4. Evaluate internet exposure and authentication barriers.
5. Assess data sensitivity and asset criticality.
6. Review compensating controls.
7. Record the reason for the final priority.

A public-facing reachable issue affecting sensitive customer data should generally receive more urgency than an unreachable component in an isolated development tool, even if the latter has a higher base score. Validate actual context before assigning priority.

## Solution 8 — False-positive handling

A complete record should state:
- The exact alert and affected instance.
- Why it is not exploitable or not applicable.
- Evidence supporting the decision.
- Narrow suppression scope.
- Reviewer and date.
- Expiry/review date.
- Conditions that would invalidate the decision.

Example: a credential-like string is a placeholder only if it is confirmed non-functional, not deployed, and not present as a valid credential in repository history or runtime. If a real credential was exposed, rotate it.

## Solution 9 — Risk acceptance

A valid risk acceptance should include:
- Finding and affected service.
- Residual risk and business impact.
- Business reason for delay.
- Compensating controls.
- Accountable risk owner and approval.
- Expiry and review date.
- Monitoring and early-review triggers.

A security analyst can provide a recommendation, but acceptance must come from the authorized risk owner under organizational policy.

## Solution 10 — Remediation verification

Retest sequence:
1. Record the fixed commit/build.
2. Repeat the original test.
3. Run the relevant scanner or regression test.
4. Confirm the vulnerable behavior is gone.
5. Check alternate paths and regression risk.
6. Attach evidence.
7. Close if passed; reopen if it still reproduces.

## Solution 11 — Dashboard metrics

Example Python summary:

```python
import json
from collections import Counter
from pathlib import Path

items = json.loads(
    Path("normalized-findings.json").read_text(encoding="utf-8")
)

severity = Counter(x.get("severity", "unknown") for x in items)
status = Counter(x.get("status", "unknown") for x in items)
source = Counter(x.get("source", {}).get("tool", "unknown") for x in items)

print("Total findings:", len(items))
print("By severity:", dict(severity))
print("By status:", dict(status))
print("By source:", dict(source))
```

For operational metrics such as overdue count and mean time to remediate, records need reliable created, assigned, fixed, and closed timestamps. Define the metric calculation before comparing teams.

## Solution 12 — CI/CD gate

Example policy script:

```python
import json
import sys
from pathlib import Path

report = Path("normalized-findings.json")
if not report.exists():
    raise SystemExit("Missing report: scan result is inconclusive")

try:
    findings = json.loads(report.read_text(encoding="utf-8"))
except json.JSONDecodeError as exc:
    raise SystemExit(f"Invalid findings JSON: {exc}")

blocking = [
    item for item in findings
    if item.get("status") == "confirmed"
    and item.get("severity") in {"critical", "high"}
]

for item in blocking:
    print(
        "BLOCK",
        item.get("finding_id"),
        item.get("severity"),
        item.get("title", "")
    )

sys.exit(1 if blocking else 0)
```

This script only evaluates a normalized report. Each scanner, parser, and normalization stage must independently fail if execution fails. Do not write an empty report after an upstream failure.

## Solution 13 — SLA and backlog

Example training policy:

| Priority | Target |
|---|---|
| Critical | Contain immediately; remediation target within 7 days |
| High | 14 days |
| Medium | 30–60 days |
| Low | 90 days or planned maintenance |

Assign owners, record due dates, and escalate breaches. Adjust these targets to your organization's actual risk appetite and obligations.

## Solution 14 — Capstone architecture

```text
SAST / DAST / IAST / SCA / Manual
                |
                v
        Raw evidence store
                |
                v
       Normalize and enrich
                |
                v
          Deduplicate
                |
                v
        Human validation
                |
                v
       Disposition + priority
                |
        +-------+--------+
        |                |
        v                v
    Remediate        Risk accept
        |                |
        v                v
       Retest       Review by expiry
        |
        v
       Close / Reopen
        |
        v
    Metrics and reporting
```

## Further reading

- [OWASP Vulnerability Management](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-7-Operate/2-7-4-Vulnerability-Management/)
- [NCSC Vulnerability Triage](https://www.ncsc.gov.uk/collection/vulnerability-management/guidance/carry-out-assessments)
- [OWASP DSOMM false-positive treatment](https://dsomm.owasp.org/activity-description?activityName=Simple+false+positive+treatment&dimension=Test+and+Verification&level=1&subDimension=Consolidation)
- [FIRST CVSS](https://www.first.org/cvss/)
- [FIRST EPSS](https://www.first.org/epss/)
- [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
