# Subprocess and OS Automation for DevSecOps

This module in the [CubicNova DevSecOps Roadmap](https://github.com/cubicnova/DevSecOps-Roadmap/tree/main/03-Python-for-DevSecOps/07-Subprocess-and-OS) teaches how to interact with the operating system and run external programs from Python safely.

## Learning objectives

- Use `os` and `pathlib` to inspect and manage paths.
- Read environment variables and understand process environments.
- Use `subprocess.run()` to launch programs and capture results.
- Set timeouts and handle errors and exit codes.
- Pass command arguments safely without shell interpolation.
- Work with working directories, output streams, and return codes.
- Automate simple defensive maintenance and reporting tasks.
- Identify common command-injection risks.

## Topics

1. `os.getcwd()`, `os.listdir()`, and directory navigation
2. `pathlib.Path` for portable file and directory operations
3. Environment variables with `os.environ` and `os.getenv`
4. Process execution with `subprocess.run`
5. Argument lists and `shell=False`
6. Capturing stdout and stderr
7. Return codes and `check=True`
8. Timeouts and exception handling
9. Working directories and environment overrides
10. Safe command construction
11. File inventory and system utility automation
12. Defensive mini-project

## Requirements

- Python 3
- A terminal or command prompt
- A code editor or Jupyter Notebook
- Familiarity with basic Python functions and exceptions

Examples are written to be portable where practical. Some commands differ between Windows, Linux, and macOS.

## Setup

```bash
python --version
mkdir subprocess-os-lab
cd subprocess-os-lab
python -m venv .venv
```

Activate the environment:

```bash
# Linux/macOS
source .venv/bin/activate
```

```powershell
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

No third-party packages are required.

## Companion files

- [`examples.md`](examples.md): runnable examples.
- [`practical.md`](practical.md): hands-on exercises and mini-project.
- [`practical.ipynb`](practical.ipynb): interactive Jupyter workbook.
- [`solutions.md`](solutions.md): reference solutions.

## Security guidelines

- Prefer `subprocess.run([...], shell=False)` using an argument list.
- Never concatenate untrusted input into shell command strings.
- Use absolute or carefully controlled executable paths for sensitive automation where practical.
- Apply timeouts to commands that might hang.
- Check return codes and handle expected failures.
- Avoid logging secrets from environment variables or command output.
- Use a minimal environment when running sensitive commands.
- Do not run destructive commands or elevated commands for practice.
- Only automate systems and tasks you are authorized to manage.

## Common patterns

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "--version"],
    capture_output=True,
    text=True,
    check=True,
    timeout=10,
)
print(result.stdout or result.stderr)
```

Use `pathlib` for path operations rather than manually joining strings with slashes.

## DevSecOps use cases

- Check a tool's version in a CI job.
- Collect non-sensitive command output for a report.
- Inventory files in a controlled workspace.
- Validate that required environment variables exist without printing their values.
- Run linters and tests with timeouts.
- Summarize return codes from defensive automation steps.

## Completion checklist

- [ ] Navigate paths with `pathlib`.
- [ ] Inspect directory contents safely.
- [ ] Read environment variables without exposing secrets.
- [ ] Run a harmless command using `subprocess.run`.
- [ ] Capture stdout and stderr.
- [ ] Handle non-zero exit codes and timeouts.
- [ ] Pass arguments as a list and avoid `shell=True`.
- [ ] Complete the practical workbook and mini-project.

## Learning resources

- [Python `subprocess` documentation](https://docs.python.org/3/library/subprocess.html)
- [Python `os` documentation](https://docs.python.org/3/library/os.html)
- [Python `pathlib` documentation](https://docs.python.org/3/library/pathlib.html)
- [Python security considerations](https://docs.python.org/3/library/security_warnings.html)
