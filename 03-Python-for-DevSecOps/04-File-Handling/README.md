# 04 — File Handling with Python for DevSecOps

Learn how to read, create, update, and safely process files with Python. These skills support automation, log analysis, report generation, configuration management, and security tooling.

## Learning objectives

By the end of this module, you should be able to:

- Open, read, write, append, and close files safely.
- Use context managers (`with open(...)`) and choose suitable file modes.
- Work with text files, CSV, JSON, and paths.
- Handle missing files and common I/O errors.
- Process large text files line by line.
- Apply basic file-safety practices when writing automation scripts.

## Topics covered

| Topic | Key ideas | DevSecOps use case |
|---|---|---|
| Opening files | `open`, modes, encodings | Read tool output and configuration |
| Context managers | `with` statement | Ensure files are closed reliably |
| Reading | `read`, `readline`, iteration | Analyze log files |
| Writing and appending | `write`, `writelines`, modes | Generate reports |
| Paths and directories | `pathlib`, `exists`, `mkdir`, `glob` | Organize scan artifacts |
| CSV | `csv.reader`, `DictReader`, `DictWriter` | Process structured inventories |
| JSON | `json.load`, `json.dump`, `loads`, `dumps` | Read configuration and event data |
| Exceptions | `FileNotFoundError`, `PermissionError`, `OSError` | Make automation more resilient |
| Large files | Stream line by line | Avoid loading large logs entirely into memory |
| Safe file handling | Validation, least privilege, careful overwrite behavior | Reduce accidental data loss |

## Prerequisites

- Python fundamentals: variables, loops, functions, and exceptions.
- Python 3.10 or later recommended.
- Jupyter Notebook for the practical lab.

## Setup

The examples use Python's standard library only. No extra packages are required.

```bash
python --version
python -m pip install jupyter
jupyter notebook
```

Run the notebook in a dedicated practice directory. It creates a temporary `file_handling_lab` folder and sample files there.

## Suggested learning path

1. Review [`examples.md`](examples.md).
2. Complete the exercises in [`practical.ipynb`](practical.ipynb).
3. Check your approach against [`solutions.md`](solutions.md).
4. Extend the lab to produce a summary report from fictional security events.

## DevSecOps practice project: Log Summary Generator

Build a script that reads a sample log file, counts event levels, identifies lines containing a selected keyword, and writes a JSON summary report.

Use fictional sample data only. Do not commit passwords, API keys, access tokens, private keys, personal data, or production logs to this repository. Treat all external files as untrusted input.

## File mode quick reference

| Mode | Meaning |
|---|---|
| `r` | Read; file must exist |
| `w` | Write; creates or truncates the file |
| `a` | Append; creates the file if needed |
| `x` | Create a new file; fails if it already exists |
| `b` | Binary mode modifier, e.g. `rb` |
| `+` | Read and write modifier, e.g. `r+` |

Prefer explicit encodings for text files, such as `encoding="utf-8"`.

## Good practices

- Use `with open(...)` so files are closed even if an exception occurs.
- Use `pathlib.Path` for portable path manipulation.
- Use `try/except` for expected I/O failures; do not hide every exception with a bare `except`.
- Process large files line by line instead of using `read()` on the entire file.
- Be cautious with `w` mode because it truncates an existing file.
- Validate structured data and handle malformed CSV/JSON input.
- Use least-privilege file permissions and avoid following untrusted paths without validation.
- Do not use `eval()` to parse file contents.

## Completion checklist

- [ ] Read and write a UTF-8 text file.
- [ ] Explain the difference between `w`, `a`, and `x`.
- [ ] Work with `pathlib`, CSV, and JSON.
- [ ] Handle missing files and malformed input.
- [ ] Process a file line by line.
- [ ] Generate a summary report from sample security events.

## Further reading

- [Python file I/O tutorial](https://docs.python.org/3/tutorial/inputoutput.html)
- [Built-in `open()`](https://docs.python.org/3/library/functions.html#open)
- [The `pathlib` module](https://docs.python.org/3/library/pathlib.html)
- [The `csv` module](https://docs.python.org/3/library/csv.html)
- [The `json` module](https://docs.python.org/3/library/json.html)
