# Subprocess and OS — Solutions

Reference answers for `practical.md`. Try each lab before reading the solution.

## Solution 1 — Inspect the environment

```python
import os
import platform
import sys
from pathlib import Path

print("Working directory:", Path.cwd())
print("Python version:", sys.version.split()[0])
print("Operating system:", platform.system())
print("CPU count:", os.cpu_count())
```

## Solution 2 — Directory inventory

```python
from pathlib import Path

workspace = Path("lab_workspace")
(workspace / "subdir").mkdir(parents=True, exist_ok=True)
(workspace / "one.txt").write_text("one\n", encoding="utf-8")
(workspace / "two.txt").write_text("two\n", encoding="utf-8")

for entry in workspace.iterdir():
    if entry.is_dir():
        print("Directory:", entry.name)
    elif entry.is_file():
        print("File:", entry.name, "bytes:", entry.stat().st_size)
```

## Solution 3 — Environment variables

```python
import os

app_env = os.getenv("APP_ENV", "development")
token_is_configured = bool(os.getenv("API_TOKEN"))

print("APP_ENV:", app_env)
print("API_TOKEN configured:", token_is_configured)
```

Do not print the token itself.

## Solution 4 — Run Python version command

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
print(result.stdout.strip() or result.stderr.strip())
```

## Solution 5 — Capture stdout and stderr

```python
import subprocess
import sys

child_code = (
    "import sys; "
    "print('hello stdout'); "
    "print('hello stderr', file=sys.stderr)"
)

result = subprocess.run(
    [sys.executable, "-c", child_code],
    capture_output=True,
    text=True,
    timeout=10,
)

print("stdout:", result.stdout.strip())
print("stderr:", result.stderr.strip())
print("return code:", result.returncode)
```

## Solution 6 — Non-zero exit status

```python
import subprocess
import sys

try:
    subprocess.run(
        [sys.executable, "-c", "raise SystemExit(3)"],
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
except subprocess.CalledProcessError as error:
    print("Child process failed with code:", error.returncode)
```

Use `check=True` when a non-zero status should be treated as an exception.

## Solution 7 — Timeout handling

```python
import subprocess
import sys

try:
    subprocess.run(
        [sys.executable, "-c", "import time; time.sleep(5)"],
        timeout=1,
        check=True,
    )
except subprocess.TimeoutExpired:
    print("Command exceeded the allowed time")
```

## Solution 8 — Working directory

```python
import subprocess
import sys
from pathlib import Path

workspace = Path("lab_workspace").resolve()
workspace.mkdir(parents=True, exist_ok=True)

result = subprocess.run(
    [sys.executable, "-c", "from pathlib import Path; print(Path.cwd())"],
    cwd=workspace,
    capture_output=True,
    text=True,
    check=True,
    timeout=10,
)
print(result.stdout.strip())
print("Expected:", workspace)
```

## Solution 9 — Environment override

```python
import os
import subprocess
import sys

child_env = os.environ.copy()
child_env["APP_ENV"] = "test"

result = subprocess.run(
    [sys.executable, "-c", "import os; print(os.getenv('APP_ENV'))"],
    env=child_env,
    capture_output=True,
    text=True,
    check=True,
    timeout=10,
)
print(result.stdout.strip())
```

For sensitive jobs, consider constructing a minimal environment rather than copying all variables.

## Solution 10 — Safe argument passing

```python
import subprocess
import sys

filename = "report with spaces.txt"
code = "import sys; print(repr(sys.argv[1]))"

result = subprocess.run(
    [sys.executable, "-c", code, filename],
    capture_output=True,
    text=True,
    check=True,
    timeout=10,
)
print(result.stdout.strip())
```

The filename is passed as one argument. Avoid composing shell command strings with untrusted input.

## Solution 11 — File inventory report

```python
import json
from pathlib import Path

root = Path("lab_workspace").resolve()
report = []

for path in root.rglob("*"):
    if path.is_file():
        report.append({
            "relative_path": str(path.relative_to(root)),
            "suffix": path.suffix,
            "size_bytes": path.stat().st_size,
        })

output = Path("inventory.json")
output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(report)} records to {output}")
```

Keep the traversal scoped to a test directory. In production, account for symbolic links, permissions, and files that change during inventory.

## Solution 12 — Mini-project: Preflight checker

`checks.py`:

```python
import platform
import subprocess
import sys
from pathlib import Path

def check_python_version():
    try:
        result = subprocess.run(
            [sys.executable, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
            shell=False,
        )
        return {
            "executable": sys.executable,
            "return_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"error": "Python version command timed out"}
    except OSError:
        return {"error": "Python version command could not be started"}

def build_preflight_report(workspace):
    path = Path(workspace).resolve()
    return {
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "workspace": str(path),
        "workspace_exists": path.is_dir(),
        "python_command": check_python_version(),
    }
```

`main.py`:

```python
import json
from pathlib import Path
from checks import build_preflight_report

def main():
    workspace = Path("preflight_workspace")
    workspace.mkdir(parents=True, exist_ok=True)

    report = build_preflight_report(workspace)
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "preflight.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
```

Run `python main.py`. The example records basic environment details and command status; extend it with project-specific checks as needed.

## Key takeaways

- Use `pathlib` for portable path handling.
- Use `subprocess.run()` with argument lists and `shell=False`.
- Capture output deliberately and check return codes.
- Apply timeouts to external processes.
- Avoid printing secrets from environment variables or process output.
- Keep automation scoped, authorized, and non-destructive.
