# Subprocess and OS — Code Examples

These examples use Python's standard library. Run them in a test directory and avoid destructive operations.

## 1. Current working directory

```python
import os
from pathlib import Path

print("Working directory:", os.getcwd())
print("Resolved path:", Path.cwd())
```

## 2. List directory entries

```python
from pathlib import Path

for entry in Path(".").iterdir():
    print("Directory" if entry.is_dir() else "File", entry.name)
```

Do not assume files found in a directory are trustworthy. Validate names and types before processing them.

## 3. Create a controlled workspace

```python
from pathlib import Path

workspace = Path("devsecops_workspace")
workspace.mkdir(parents=True, exist_ok=True)

sample = workspace / "sample.txt"
sample.write_text("Synthetic test data\n", encoding="utf-8")
print(sample.read_text(encoding="utf-8"))
```

## 4. Read environment variables

```python
import os

environment = os.getenv("APP_ENV", "development")
token_is_configured = bool(os.getenv("API_TOKEN"))

print("Environment:", environment)
print("API token configured:", token_is_configured)
```

Never print the token itself. Environment variables are configuration inputs, not a secure secret store by themselves.

## 5. Run a harmless command

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

Using `sys.executable` runs the Python interpreter associated with the current environment.

## 6. Capture standard output and error

```python
import subprocess
import sys

code = "print('standard output'); print('standard error', file=__import__('sys').stderr)"

result = subprocess.run(
    [sys.executable, "-c", code],
    capture_output=True,
    text=True,
    timeout=10,
)

print("Return code:", result.returncode)
print("stdout:", result.stdout.strip())
print("stderr:", result.stderr.strip())
```

## 7. Handle non-zero exit codes

```python
import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-c", "raise SystemExit(3)"],
    capture_output=True,
    text=True,
    timeout=10,
)

if result.returncode == 0:
    print("Command succeeded")
else:
    print("Command failed with code:", result.returncode)
```

Alternatively, use `check=True` and catch `subprocess.CalledProcessError`.

## 8. Handle timeouts

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

The timeout is a control, not a guarantee that a complex process tree is always terminated exactly as expected on every platform.

## 9. Set a working directory

```python
import subprocess
import sys
from pathlib import Path

workspace = Path("devsecops_workspace").resolve()
workspace.mkdir(exist_ok=True)

result = subprocess.run(
    [sys.executable, "-c", "from pathlib import Path; print(Path.cwd())"],
    cwd=workspace,
    capture_output=True,
    text=True,
    check=True,
    timeout=10,
)
print(result.stdout.strip())
```

## 10. Environment overrides

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

Copying the full environment may pass more variables than necessary. For sensitive automation, construct a minimal allowlisted environment.

## 11. Safe argument passing

```python
import subprocess
import sys

filename = "sample file.txt"

# The filename is a separate argument, not interpreted by a shell.
result = subprocess.run(
    [sys.executable, "-c", "import sys; print(repr(sys.argv[1]))", filename],
    capture_output=True,
    text=True,
    check=True,
    timeout=10,
)
print(result.stdout.strip())
```

Avoid this unsafe pattern:

```python
# Do not do this with untrusted input:
# subprocess.run("some-command " + user_input, shell=True)
```

## 12. File inventory with pathlib

```python
from pathlib import Path

root = Path("devsecops_workspace").resolve()

for path in root.rglob("*"):
    if path.is_file():
        print({
            "name": path.name,
            "suffix": path.suffix,
            "size_bytes": path.stat().st_size,
        })
```

Use an intentionally limited workspace. Be careful with symbolic links and files that may change during scanning.

## 13. Platform information

```python
import os
import platform
import sys

print("Operating system:", platform.system())
print("OS release:", platform.release())
print("Python version:", sys.version.split()[0])
print("CPU count:", os.cpu_count())
```

## 14. A reusable command runner

```python
import subprocess

def run_command(args, *, timeout=10, cwd=None):
    """Run a command argument list and return its completed process."""
    if not isinstance(args, (list, tuple)) or not args:
        raise ValueError("args must be a non-empty list or tuple")
    if not all(isinstance(arg, str) for arg in args):
        raise TypeError("Every command argument must be a string")

    return subprocess.run(
        list(args),
        capture_output=True,
        text=True,
        check=False,
        timeout=timeout,
        cwd=cwd,
        shell=False,
    )
```

This wrapper does not decide which executables are permitted. Applications should allowlist commands and validate arguments appropriate to their use case.

## Practice challenge

Build a file inventory report for a temporary workspace. Run the Python interpreter with `subprocess`, capture the version output, handle errors and timeouts, and write a JSON report. Do not invoke destructive commands or require administrator privileges.
