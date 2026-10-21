# Functions and Modules — Practical Workbook

**Level:** Beginner to intermediate  
**Requirements:** Python 3; no third-party packages needed.

Use `practical.ipynb` for the interactive notebook version. Try each task before reviewing `solutions.md`.

## Lab 1 — Basic function

Create `greetings.py` with a `greet(name)` function that returns a greeting string. Test it with at least three names.

## Lab 2 — Parameters and return values

Write `calculate_percentage(part, total)` that returns a percentage. Validate inputs and handle `total == 0`. Test normal, zero, and invalid values.

## Lab 3 — Default and keyword arguments

Write `format_event(event_type, severity="INFO", source="unknown")` that returns a dictionary. Call it using positional and keyword arguments.

## Lab 4 — `*args` and `**kwargs`

1. Implement `calculate_average(*values)` and reject an empty argument list.
2. Implement `build_metadata(**fields)` and return a copy of the supplied fields.
3. Explain when variable-length arguments make an API more flexible and when they make it harder to validate.

## Lab 5 — Scope

Create a module-level constant `DEFAULT_THRESHOLD = 5`. Write a function that compares a count to the threshold. Do not modify the global variable. Explain local versus global scope.

## Lab 6 — Docstrings and type hints

Write `is_valid_port(port: int) -> bool`. Include a docstring and reject Boolean values, strings, zero, and values above 65535.

## Lab 7 — Lambda and sorting

Given a list of dictionaries representing findings, sort them by title and then by severity. For bonus credit, implement a custom severity order: Critical, High, Medium, Low.

## Lab 8 — Custom module

Create these files:

```text
lab08/
├── main.py
└── validators.py
```

In `validators.py`, implement IP and port validators. Import them explicitly into `main.py` and test valid and invalid values.

## Lab 9 — Main guard and imports

Create a module with one reusable function and a `main()` function. Demonstrate that importing the module does not run the main routine. Avoid wildcard imports.

## Lab 10 — Reusable file hashing module

Create `hashing.py` with `sha256_file(path)`. Import it into another file, hash a sample file, change the file, and compare the digest against a stored baseline.

Protect the baseline in real systems; do not treat a hash alone as proof that a file is trustworthy.

## Lab 11 — Custom exceptions

Define `InvalidFindingError`. Write `validate_finding(finding)` that checks for an ID and a severity from `Critical`, `High`, `Medium`, or `Low`. Raise your custom exception for invalid data.

## Lab 12 — Unit tests

Use `unittest` to test your port validator. Include valid ports, boundary values, Boolean input, strings, zero, and out-of-range values.

Run:

```bash
python -m unittest -v
```

## Lab 13 — Mini-project: DevSecOps utility package

Build this project:

```text
security_utils/
├── __init__.py
├── validators.py
├── hashing.py
├── reporting.py
├── main.py
└── tests/
    └── test_validators.py
```

Requirements:
- Keep validation, hashing, and reporting logic in separate modules.
- Export only intended public helpers from `__init__.py`.
- Use a main guard.
- Handle expected errors and avoid leaking sensitive values.
- Test normal, boundary, and invalid inputs.
- Write a JSON report from synthetic data.
- Include a README explaining how to run the project.

## Reflection questions

1. What is a Python module?
2. How is a package different from a single module?
3. Why should imports generally be explicit?
4. What is the purpose of the main guard?
5. What is the difference between a parameter and an argument?
6. Why should mutable default arguments be avoided?
7. Why are unit tests useful for security utilities?
8. Why should a module avoid side effects during import?

## Completion checklist

- [ ] Functions with positional, keyword, and default arguments
- [ ] `*args` and `**kwargs`
- [ ] Scope, docstrings, and type hints
- [ ] Custom modules and package layout
- [ ] Main guard and custom exceptions
- [ ] Unit tests
- [ ] DevSecOps utility mini-project
