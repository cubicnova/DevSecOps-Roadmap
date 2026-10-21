# 09 - Security Automation

Learn how to use Python to automate repeatable, defensive security tasks safely and consistently.

## Learning objectives

By the end of this module, you should be able to:

- Design small automation workflows with clear inputs, outputs, and failure handling.
- Validate targets and configuration before running checks.
- Parse structured scan or inventory data using JSON and CSV.
- Normalize findings and remove duplicates.
- Produce actionable reports and audit-friendly logs.
- Add safe limits, timeouts, dry-run behavior, and error handling.
- Explain how to keep automation scoped to systems you own or are authorized to assess.

## Prerequisites

- Python fundamentals, functions, files, exceptions, JSON/CSV, and basic command-line usage.
- Familiarity with security concepts such as assets, findings, severity, and remediation.

## Suggested folder contents

```text
09-Security-Automation/
├── README.md
├── examples.md
├── practical.md
├── practical.ipynb
└── solutions.md
```

## Topics

1. Automation workflow design
2. Input validation and scope control
3. Parsing JSON and CSV security data
4. Finding normalization and deduplication
5. Severity summaries and report generation
6. Logging, exceptions, and audit trails
7. Safe execution patterns: dry run, limits, and timeouts
8. Mini-project: Security Findings Report Generator

## Setup

Python 3.10+ is recommended. The practical notebook uses only the Python standard library, so no additional packages are required.

Run a Python script from this folder:

```bash
python script_name.py
```

Open `practical.ipynb` in Jupyter Notebook, JupyterLab, or VS Code.

## Safety rules

- Run automation only on systems and data you own or are explicitly authorized to assess.
- Start with sample files and a dry run.
- Do not store passwords, API keys, tokens, or other secrets in source code or reports.
- Validate and constrain user-supplied paths, hostnames, URLs, and command arguments.
- Prefer APIs or library functions over shell commands where possible.
- If a subprocess is necessary, pass an argument list and avoid `shell=True` with untrusted input.
- Apply timeouts, rate limits, and explicit scope allowlists to any network activity.
- Log what the automation did, but avoid logging secrets or unnecessary personal data.

Python's official documentation explains the security considerations for subprocesses and why invoking a shell with untrusted input can create command-injection risks: https://docs.python.org/3/library/subprocess.html#security-considerations

## Suggested learning path

1. Read `examples.md`.
2. Complete the tasks in `practical.md`.
3. Work through the TODO cells in `practical.ipynb`.
4. Compare your work with `solutions.md` only after attempting the exercises.

## Completion checklist

- [ ] Validate and load a sample findings file.
- [ ] Normalize severity values.
- [ ] Deduplicate findings using a stable key.
- [ ] Generate a summary by severity.
- [ ] Write a CSV or JSON report.
- [ ] Add useful logs and graceful error handling.
- [ ] Explain the safeguards that make the workflow safe.
