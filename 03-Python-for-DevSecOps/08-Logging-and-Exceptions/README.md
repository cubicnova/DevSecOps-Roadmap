# 08 — Logging and Exceptions with Python for DevSecOps

Learn to record useful diagnostic events, handle expected failures, and build Python automation that is easier to troubleshoot and safer to operate.

## Learning objectives

- Use `try`, `except`, `else`, and `finally`.
- Raise built-in and custom exceptions.
- Configure logging levels, formatters, and handlers.
- Record useful context without exposing credentials or sensitive data.
- Use exception tracebacks and log rotation.
- Process fictional security events robustly.

## Topics covered

| Topic | Key ideas | DevSecOps use case |
|---|---|---|
| Exceptions | `try`, `except`, `else`, `finally` | Recover from expected failures |
| Raising errors | `raise`, exception chaining | Reject invalid input clearly |
| Custom exceptions | Domain-specific errors | Separate validation and configuration failures |
| Logging levels | DEBUG, INFO, WARNING, ERROR, CRITICAL | Classify operational events |
| Formatting | Timestamps, levels, logger names | Make logs searchable |
| Handlers | Console and file output | Route logs to appropriate destinations |
| Tracebacks | `logger.exception()` | Diagnose failures |
| Safe logging | Redaction and data minimization | Avoid leaking secrets |
| Rotation | `RotatingFileHandler` | Keep logs bounded |
| Testing | Assert expected exceptions | Verify failure behavior |

## Prerequisites

- Python fundamentals, functions, file handling, and modules.
- Python 3.10 or later recommended.
- Jupyter Notebook for the practical exercises.

## Setup

The exercises use Python's standard library.

```bash
python --version
python -m pip install jupyter
jupyter notebook
```

## Suggested learning path

1. Read [`examples.md`](examples.md).
2. Complete the TODO cells in [`practical.ipynb`](practical.ipynb).
3. Review [`solutions.md`](solutions.md) after attempting the exercises.
4. Extend the mini-project to log a fictional security-event processing run.

## Logging levels

| Level | Typical use |
|---|---|
| `DEBUG` | Detailed diagnostic information |
| `INFO` | Normal milestones and successful operations |
| `WARNING` | Unexpected conditions that do not stop the workflow |
| `ERROR` | An operation failed |
| `CRITICAL` | A severe failure may prevent continued operation |

## Mini project: Safe Security Event Processor

Validate fictional event records, count valid events, record malformed records, and write an operational log. Include timestamps and severity levels, but never log passwords, tokens, private keys, or full sensitive payloads.

## Good practices

- Use `logging` rather than relying exclusively on `print()` in larger scripts.
- Configure logging once at the application entry point.
- Catch specific exceptions when you can take meaningful action.
- Avoid bare `except:` and do not silently swallow exceptions.
- Use `logger.exception()` inside an exception handler when a traceback is useful.
- Do not log secrets, authorization headers, session cookies, or unnecessary personal data.
- Use `finally` for cleanup that must occur regardless of success or failure.
- Rotate log files for long-running applications.
- Keep detailed internal diagnostics in appropriately protected logs.

## Completion checklist

- [ ] Use `try/except/else/finally`.
- [ ] Raise and define a custom exception.
- [ ] Configure logging levels and formatting.
- [ ] Log a traceback with `logger.exception()`.
- [ ] Avoid leaking sensitive values in logs.
- [ ] Process valid and invalid sample events robustly.

## Further reading

- [Python logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [Logging reference](https://docs.python.org/3/library/logging.html)
- [Built-in exceptions](https://docs.python.org/3/library/exceptions.html)
- [Errors and exceptions tutorial](https://docs.python.org/3/tutorial/errors.html)
