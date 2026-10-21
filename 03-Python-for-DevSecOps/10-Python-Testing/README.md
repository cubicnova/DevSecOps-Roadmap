# 10 — Python Testing for DevSecOps

Learn to verify Python code with repeatable tests before deploying automation, API clients, and security utilities.

## Learning objectives
- Explain unit, integration, and regression testing.
- Write tests with built-in `unittest` and `pytest`.
- Verify expected results, exceptions, and edge cases.
- Use fixtures, parameterization, temporary files, and mocks.
- Run tests from the command line and interpret failures.

## Topics
| Topic | Use |
|---|---|
| Arrange–Act–Assert | Structure readable tests |
| `assert` and pytest | Verify behavior |
| `unittest.TestCase` | Standard-library testing |
| Exceptions | Verify invalid-input behavior |
| Fixtures and parameterization | Reuse setup and cover edge cases |
| Temporary files | Test file-processing code safely |
| `unittest.mock` | Test without live APIs |
| Discovery and CI | Catch regressions before merge |

## Setup

```bash
python -m pip install pytest jupyter
jupyter notebook
```

The built-in `unittest` module requires no extra installation.

## Learning path
1. Read [`examples.md`](examples.md).
2. Complete [`practical.ipynb`](practical.ipynb).
3. Review [`solutions.md`](solutions.md).
4. Move exercises into `test_*.py` files and run `python -m pytest -q`.

## Common commands

```bash
python -m pytest
python -m pytest -q
python -m pytest tests/test_validators.py
python -m unittest discover -s tests -v
```

Pytest commonly discovers files named `test_*.py` or `*_test.py`. See the [official pytest getting-started guide](https://pytest.org/en/latest/getting-started.html).

## DevSecOps mini-project
Test a utility that validates port numbers and event records, summarizes fictional security events, and parses text files. Include valid inputs, invalid inputs, boundaries, and expected exceptions. Use local sample data or mocks instead of live production systems.

## Good practices
- Test observable behavior, not implementation details.
- Use clear test names and cover edge cases.
- Avoid dependence on test execution order.
- Do not call production APIs or run real scans from unit tests.
- Use temporary directories and mock external dependencies.
- Never include real credentials or sensitive production data in fixtures.
- Treat coverage as a signal, not proof of correctness.

## Completion checklist
- [ ] Write pytest tests with `assert`.
- [ ] Write a `unittest.TestCase`.
- [ ] Test an expected exception.
- [ ] Use parameterization and fixtures.
- [ ] Test files with temporary directories.
- [ ] Mock an external dependency.
- [ ] Run tests from the command line.

## Further reading
- [pytest — Get Started](https://pytest.org/en/latest/getting-started.html)
- [pytest — unittest integration](https://pytest.org/en/latest/how-to/unittest.html)
- [Python unittest](https://docs.python.org/3/library/unittest.html)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
