# Functions and Modules for DevSecOps

This module in the [CubicNova DevSecOps Roadmap](https://github.com/cubicnova/DevSecOps-Roadmap/tree/main/03-Python-for-DevSecOps/03-Functions-and-Modules) teaches how to write reusable Python functions and organize code into modules and packages.

## Learning objectives

- Define functions with parameters, defaults, return values, and docstrings.
- Understand local scope, global scope, and variable lifetime.
- Use positional, keyword, and variable-length arguments.
- Work with lambdas, recursion, and higher-order functions.
- Import standard-library and custom modules.
- Create packages and understand `__init__.py`.
- Use the `__name__ == "__main__"` guard.
- Handle exceptions and build reusable, testable security utilities.

## Topics

1. Function definitions and calls
2. Parameters, arguments, and return values
3. Default and keyword arguments
4. `*args` and `**kwargs`
5. Scope and lifetime
6. Docstrings and type hints
7. Lambda functions and functional tools
8. Recursion and base cases
9. Standard-library imports
10. Custom modules and aliases
11. Packages and `__init__.py`
12. Main guard and command-line entry points
13. Exceptions in reusable functions
14. Testing and code organization

## Prerequisites

- Python 3
- Completion of the Python Fundamentals module
- A terminal and code editor
- Basic Git knowledge is useful

## Setup

```bash
python --version
mkdir functions-modules-lab
cd functions-modules-lab
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

No third-party packages are required for the core examples.

## Example project structure

```text
functions-modules-lab/
├── main.py
├── validators.py
├── log_utils.py
├── security_tools/
│   ├── __init__.py
│   ├── hashing.py
│   └── reporting.py
└── tests/
    └── test_validators.py
```

A module is a Python file that contains definitions and statements. Packages organize modules into a directory hierarchy. See the [official Python modules tutorial](https://docs.python.org/3/tutorial/modules.html).

## Companion files

- [`examples.md`](examples.md): explanations and runnable code snippets.
- [`practical.md`](practical.md): lab exercises and mini-projects.
- [`practical.ipynb`](practical.ipynb): interactive Jupyter workbook with TODOs.
- [`solutions.md`](solutions.md): reference solutions.

## DevSecOps use cases

Functions and modules help teams create reusable components for:
- Validating configuration and network addresses.
- Parsing and summarizing synthetic security logs.
- Calculating file hashes for integrity checks.
- Normalizing vulnerability scanner exports.
- Sharing common utilities across CI/CD checks.
- Keeping automation readable, testable, and maintainable.

## Secure coding reminders

- Validate inputs at module boundaries.
- Raise specific exceptions rather than silently hiding errors.
- Avoid mutable default arguments such as `items=[]`.
- Avoid `from module import *`; explicit imports are easier to audit.
- Do not execute untrusted strings with `eval()` or pass them to shell commands.
- Never hard-code secrets or commit credentials and sensitive logs.
- Keep module import side effects minimal; put executable behavior behind a main guard.

## Completion checklist

- [ ] Write functions with parameters and return values.
- [ ] Use default, keyword, `*args`, and `**kwargs` arguments.
- [ ] Explain local and global scope.
- [ ] Add docstrings and type hints.
- [ ] Import standard-library and custom modules.
- [ ] Create and import a small package.
- [ ] Use the main guard.
- [ ] Test success, boundary, and error cases.
- [ ] Complete the practical workbook and mini-project.

## Learning resources

- [Python Tutorial: Modules](https://docs.python.org/3/tutorial/modules.html)
- [Python Tutorial: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [Python `typing` module](https://docs.python.org/3/library/typing.html)
- [Python `unittest`](https://docs.python.org/3/library/unittest.html)
