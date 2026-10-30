# SAST Fundamentals — Solutions and Explanations

## Exercise 1: SAST comparison

| Technique | Analysis target | Execution needed? |
|---|---|---:|
| SAST | Source code and related artifacts | No |
| DAST | Running application | Yes |
| IAST | Runtime behavior with instrumentation | Yes |
| SCA | Third-party dependencies | Usually no |

**Explanation:** SAST finds potential weaknesses in code early. It does not fully understand all runtime states, deployment configuration, or business logic.

## Exercise 2: Sources and sinks

Example for a web application:

| Source | Sink | Security concern |
|---|---|---|
| HTTP query parameter | SQL execution | SQL injection |
| HTTP request body | HTML response | Cross-site scripting |
| Uploaded filename | File read/write | Path traversal |
| HTTP parameter | Shell command | Command injection |

Validation and encoding must be appropriate to the specific operation. Validation alone is not a universal replacement for parameterized APIs or context-aware output encoding.

## Exercise 3: SQL injection

Vulnerable:

```python
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)
```

Safer:

```python
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

**Explanation:** Parameter binding separates SQL syntax from the value supplied by the user.

## Exercise 4: XSS

Vulnerable:

```python
return Response(f"<h1>Hello {name}</h1>", mimetype="text/html")
```

Safer:

```python
return render_template_string("<h1>Hello {{ name }}</h1>", name=name)
```

**Explanation:** Normal template interpolation escapes untrusted values. Do not mark user-controlled data as safe HTML.

## Exercise 5: Command injection

Vulnerable:

```python
os.system("ls " + directory)
```

Safer:

```python
subprocess.run(
    ["ls", "--", directory],
    check=True,
    shell=False,
    text=True,
    capture_output=True,
)
```

**Explanation:** Argument arrays avoid shell parsing. Also validate that the requested directory is within an approved set of locations.

## Exercise 6: Path traversal

```python
from pathlib import Path

BASE = Path("uploads").resolve()

def safe_read(filename):
    target = (BASE / filename).resolve()
    if target != BASE and BASE not in target.parents:
        raise ValueError("Path outside upload directory")
    if not target.is_file():
        raise FileNotFoundError(target)
    return target.read_text(encoding="utf-8")
```

**Explanation:** Resolving the path and checking its parent relationship prevents the resolved target from escaping the intended base directory. Production applications should also enforce authorization and safe file handling.

## Exercise 7: Enable GitLab SAST

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml
```

Commit the file to a feature branch and run a pipeline. Inspect the SAST job and artifacts.

**Explanation:** GitLab's template adds analyzer jobs based on detected supported languages and its job rules. If no supported source files exist, a scanner job may not be created or may have nothing to analyze. The `test` stage must exist when stages are explicitly defined.

## Exercise 8: Analyze a finding

Use this template:

| Field | What to record |
|---|---|
| Rule/CWE | Rule identifier and weakness category |
| Location | File and line |
| Severity | Scanner severity |
| Confidence | Scanner confidence if available |
| Source | Where untrusted data enters |
| Sink | Sensitive operation receiving the data |
| Flow | Transformations and validation between source and sink |
| Impact | Potential effect on confidentiality, integrity, or availability |
| Fix | Secure coding change and regression test |

**Explanation:** A scanner finding is a lead for investigation. Validate reachability and context before classifying it as exploitable or false positive.

## Exercise 9: Fix and rescan
1. Apply the appropriate remediation.
2. Add a regression test.
3. Commit the change.
4. Run the pipeline again.
5. Compare the SAST reports.

**Expected result:** The original finding should no longer appear if the vulnerable code path was fixed and the analyzer recognizes the remediation. If it remains, inspect whether the code path still exists, whether the scan ran, and whether the analyzer report is current.

## Exercise 10: Excluded paths

Example:

```yaml
include:
  - template: Jobs/SAST.gitlab-ci.yml

variables:
  SAST_EXCLUDED_PATHS: "spec,test,tests,tmp,training/fixtures"
```

**Explanation:** Exclusions reduce the files or findings considered by the scan. The value can override defaults, so preserve the defaults when needed. Document exclusions and review them periodically.

## Exercise 11: False-positive triage
A finding should be considered a possible false positive only after reviewing:
- Whether the input is attacker-controlled.
- Whether the source reaches the sink.
- Whether effective validation or encoding exists.
- Whether the relevant code path can execute.
- Whether framework behavior changes the result.

Record evidence and have the appropriate reviewer approve suppression or risk acceptance. Do not suppress a finding based only on its inconvenience.

## Exercise 12: Sample SAST workflow

```yaml
stages:
  - build
  - test

include:
  - template: Jobs/SAST.gitlab-ci.yml

syntax_check:
  stage: build
  image: python:3.12
  script:
    - python -m compileall -q .
```

**Explanation:** The syntax check is illustrative and assumes a Python repository. The SAST template adds supported analyzer jobs to the pipeline. Confirm the actual merged configuration and inspect scanner artifacts after execution.

## Troubleshooting

| Symptom | Likely cause | Action |
|---|---|---|
| No SAST job | Template absent, rules exclude job, or no supported source | Inspect merged CI config, pipeline source, and supported languages |
| Analyzer image pull fails | Registry/network/auth issue | Check runner connectivity and registry access |
| Analyzer runs out of memory | Large repository or insufficient runner resources | Allocate suitable resources; review supported analyzer options |
| No report artifact | Job failed before report creation or unsupported input | Inspect full job log and analyzer output |
| Finding not shown in UI | Invalid report, missing report artifact, or tier/UI limitation | Validate report schema and feature availability |
| Too many findings | Legacy code, ruleset, duplicates, or broad scan scope | Triage by context; tune with reviewed exclusions or rules |
| Finding persists after fix | Code path remains, stale report, or analyzer behavior | Verify commit and pipeline, inspect source-to-sink path, rerun scan |

## Viva answers
1. **SAST:** Static analysis of code to identify potential security weaknesses without running the application.
2. **SAST vs DAST:** SAST analyzes code; DAST tests a running application.
3. **Source:** An origin of potentially untrusted data.
4. **Sink:** A sensitive operation where unsafe input may cause a vulnerability.
5. **Taint analysis:** Tracks untrusted data from sources toward sensitive sinks.
6. **False positive:** A reported issue that is not a real vulnerability in the context.
7. **False negative:** A real issue that the scanner fails to detect.
8. **Examples:** SQL injection, XSS, command injection, path traversal, insecure deserialization.
9. **Parameterized SQL:** It separates query syntax from user-supplied values.
10. **Shell command concatenation:** It can allow input to alter the command interpreted by the shell.
11. **CWE:** Common Weakness Enumeration, a catalog of software and hardware weakness types.
12. **Clean scan:** No. It only means the configured scanner did not report findings within its coverage and rules.

## Further reading
- [GitLab SAST](https://docs.gitlab.com/user/application_security/sast/)
- [GitLab SAST analyzers](https://docs.gitlab.com/user/application_security/sast/analyzers/)
- [GitLab SAST rules](https://docs.gitlab.com/user/application_security/sast/rules/)
