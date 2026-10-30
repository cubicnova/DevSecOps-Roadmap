# Finding Triage — Practical Examples

## 1. Example normalized finding

```yaml
finding_id: APPSEC-1042
source: SAST
tool: ExampleScanner
rule_id: PY-SQL-001
title: User input reaches SQL query
asset: customer-api
repository: org/customer-api
commit: 8d31a9f
location:
  file: src/search.py
  line: 42
severity: high
confidence: high
status: needs-triage
owner: team-customer-api
first_seen: 2026-10-01
evidence_ref: restricted://security-evidence/APPSEC-1042
```

This is an illustrative internal record, not a standard schema. Store raw scanner output separately and restrict access to evidence.

## 2. Example: confirm a SQL injection finding

Unsafe code:

```python
def search_users(name, db):
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    return db.execute(query)
```

Triage:
1. Confirm the file and line match the scanned commit.
2. Identify the source of `name`.
3. Confirm the value is externally controllable.
4. Confirm it reaches SQL execution.
5. Review whether parameterization or an effective control exists.
6. Reproduce only in an authorized test environment.
7. Classify as confirmed if the evidence supports the issue.

Safer implementation:

```python
def search_users(name, db):
    return db.execute(
        "SELECT * FROM users WHERE name = ?",
        (name,)
    )
```

Retest with the same test case and confirm that input is treated as data.

## 3. Example: false-positive decision

**Finding:** Scanner reports a secret in `config/example.env`.

**Evidence to review:**
- Is the value a documented placeholder?
- Is it used by any deployed configuration?
- Does it match a real credential format?
- Is it present in repository history or a deployed environment?

**Possible disposition:** False positive only if evidence confirms the value is non-functional sample data and cannot authenticate. Record the exact file/line and narrow suppression scope. If uncertain, keep it in “needs investigation.” If a real credential was committed, treat it as exposed and rotate it even if the current file has been changed.

## 4. Example: duplicate findings

Two tools report the same vulnerable dependency version in the same lockfile.

Recommended handling:
- Create one canonical finding for the vulnerable package/version.
- Link both scanner alerts as evidence.
- Preserve each tool's identifier and raw report.
- Assign one owner and remediation ticket.
- Verify the upgraded version removes the issue from both tools.

Do not merge findings that refer to different package instances, affected versions, or remediation paths.

## 5. Example: accepted risk

```yaml
finding_id: APPSEC-2088
status: accepted-risk
reason: "Upgrade requires a vendor compatibility change; compensating network control is active."
asset: internal-reporting-service
owner: team-reporting
risk_owner: application-business-owner
controls:
  - "Service is not internet reachable."
  - "Access restricted to dedicated service identity."
  - "Monitoring alert enabled for suspicious requests."
approved_by: "Authorized risk owner"
approved_date: "2026-10-15"
expiry_date: "2026-11-15"
review_date: "2026-11-08"
```

This is a template only. A real approval must identify the actual accountable person and evidence. Never invent an approver.

## 6. Example: prioritization matrix

| Finding | Technical severity | Exposure | Reachability | Asset impact | Suggested action |
|---|---|---|---|---|---|
| SQL injection in public API | High | Internet | Confirmed | Customer data | Urgent remediation |
| Vulnerable library, unused code path | Critical CVSS | Internal | Not observed | Low | Investigate reachability and exposure |
| Missing header on internal admin app | Low | Internal | Confirmed | Moderate | Planned remediation |
| KEV-listed flaw on exposed service | Varies | Internet | Affected component present | High | Immediate mitigation and remediation |

This table illustrates context-driven prioritization. Validate the actual exploitability, component usage, and asset context before deciding.

## 7. Example: severity and risk are not identical

A finding may have high technical severity but low current exposure due to strong isolation. Another may have medium technical severity but high business impact because it affects a public payment workflow.

Record both:
- Original technical severity and scoring version.
- Contextual risk rationale.
- Final priority and reason for any adjustment.

Never silently overwrite the scanner's original severity.

## 8. Example: triage status transitions

```text
NEW
 |
 v
NEEDS_TRIAGE
 |
 +--> CONFIRMED --> ASSIGNED --> IN_PROGRESS --> REMEDIATED --> RETEST
 |                                                         |
 |                                                   +-----+-----+
 |                                                   |           |
 |                                                 PASS         FAIL
 |                                                   |           |
 |                                                 CLOSED     REOPENED
 |
 +--> FALSE_POSITIVE --> DOCUMENTED_SUPPRESSION
 |
 +--> DUPLICATE --> LINKED_TO_CANONICAL
 |
 +--> ACCEPTED_RISK --> APPROVED_WITH_EXPIRY
 |
 +--> NEEDS_INVESTIGATION --> OWNER_AND_DUE_DATE
```

## 9. Example: Python triage report summary

Input `findings.json`:

```json
[
  {"id":"F-1","severity":"high","status":"confirmed","source":"SAST"},
  {"id":"F-2","severity":"medium","status":"false-positive","source":"DAST"},
  {"id":"F-3","severity":"critical","status":"needs-investigation","source":"SCA"},
  {"id":"F-4","severity":"high","status":"accepted-risk","source":"IAST"}
]
```

Script:

```python
import json
from collections import Counter
from pathlib import Path

findings = json.loads(
    Path("findings.json").read_text(encoding="utf-8")
)

by_status = Counter(item.get("status", "unknown") for item in findings)
by_severity = Counter(item.get("severity", "unknown") for item in findings)

print("Total:", len(findings))
print("By status:", dict(by_status))
print("By severity:", dict(by_severity))

print("\nActionable review queue:")
for item in findings:
    if item.get("status") in {"new", "needs-triage", "needs-investigation"}:
        print(item.get("id"), item.get("severity"), item.get("source"))
```

The script summarizes labels; it does not validate whether findings are true positives or assign risk.

## 10. Example: remediation verification record

```yaml
finding_id: APPSEC-1042
fixed_commit: 19b8d77
fixed_version: 2.4.1
retest_date: 2026-10-30
retest_method:
  - "Repeat original API request with test input."
  - "Run SAST rule against fixed commit."
result: passed
evidence_ref: restricted://security-evidence/APPSEC-1042/retest
closed_by: "Assigned security reviewer"
```

Use actual commit IDs, versions, dates, and reviewers in real records.

## 11. Example: GitHub Actions policy gate

This illustrative Python check blocks a build on confirmed critical/high findings. It assumes the input is a normalized JSON list created by a trusted pipeline step.

```python
import json
import sys
from pathlib import Path

BLOCKING_SEVERITIES = {"critical", "high"}
BLOCKING_STATUSES = {"confirmed"}

path = Path("normalized-findings.json")
if not path.exists():
    raise SystemExit("Finding report missing: cannot claim a clean scan")

findings = json.loads(path.read_text(encoding="utf-8"))
blocking = [
    item for item in findings
    if item.get("severity", "").lower() in BLOCKING_SEVERITIES
    and item.get("status", "").lower() in BLOCKING_STATUSES
]

for item in blocking:
    print(
        "BLOCK:",
        item.get("id"),
        item.get("severity"),
        item.get("title", "")
    )

sys.exit(1 if blocking else 0)
```

The scanner and normalization steps must have their own failure handling. Do not generate an empty normalized file after scanner failure and then pass this gate.

## 12. Example: triage ticket template

```text
Title:
Finding ID:
Source tool and rule:
Affected application/asset:
Affected commit/version:
Severity and confidence:
Evidence reference:
Validation result:
Business impact:
Exploitability/reachability:
Disposition:
Owner:
Remediation plan:
Target date:
Risk approver (if accepted):
Exception expiry:
Retest plan:
```
