# Python Fundamentals for DevSecOps

Welcome to **Python Fundamentals**, the first module in the Python for DevSecOps section of the [CubicNova DevSecOps Roadmap](https://github.com/cubicnova/DevSecOps-Roadmap).

This module introduces Python programming and shows how core concepts support security automation, log analysis, file processing, and DevSecOps workflows.

## Learning Objectives

- Understand Python syntax, indentation, variables, and data types.
- Work with strings, lists, tuples, sets, and dictionaries.
- Use conditions, loops, and functions.
- Import modules and handle exceptions.
- Read and write text, JSON, and CSV files.
- Validate input and IP addresses.
- Use regular expressions and SHA-256 hashes.
- Build small defensive security automation scripts.

## Topics

1. Python introduction and environment setup
2. Syntax, indentation, and comments
3. Variables, data types, and operators
4. Strings and data structures
5. Conditional statements and loops
6. Functions and modules
7. Exception handling
8. File handling
9. JSON and CSV processing
10. Regular expressions
11. Input validation and secure coding basics
12. Security-focused mini-projects

## Requirements

- Python 3
- A terminal or command prompt
- A code editor such as Visual Studio Code
- Basic familiarity with folders and files

## Setup

Check Python:

```bash
python --version
```

On Linux, you may need:

```bash
python3 --version
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Run a script:

```python
print("Welcome to Python for DevSecOps!")
```

Save it as `hello.py`, then run `python hello.py` (or `python3 hello.py` on Linux).

## Companion Files

- [`examples.md`](examples.md): runnable code examples.
- [`practical.md`](practical.md): practical exercises and mini-projects in Markdown.
- [`practical.ipynb`](practical.ipynb): interactive Jupyter Notebook workbook.
- [`solutions.md`](solutions.md): reference solutions.

## Python in DevSecOps

Python can be used to parse logs, validate configuration, summarize vulnerability exports, generate file-integrity manifests, and automate repetitive defensive tasks.

**Security reminder:** Use synthetic data and systems you own or are authorized to assess. Never commit passwords, API tokens, private keys, or real sensitive logs.

## Mini-Project Ideas

- Login log analyzer
- File integrity checker
- JSON configuration validator
- Vulnerability report summarizer
- Security event summary generator

## Learning Resources

- [Official Python Tutorial](https://docs.python.org/3/tutorial/)
- [Python Standard Library](https://docs.python.org/3/library/)
- [Virtual Environments](https://docs.python.org/3/library/venv.html)
- [JSON](https://docs.python.org/3/library/json.html)
- [CSV](https://docs.python.org/3/library/csv.html)
- [Regular Expressions](https://docs.python.org/3/library/re.html)
- [Hashlib](https://docs.python.org/3/library/hashlib.html)

## Completion Checklist

- [ ] Set up Python and a virtual environment.
- [ ] Practice data types, conditions, loops, and functions.
- [ ] Read and write text, JSON, and CSV files.
- [ ] Handle invalid input and expected errors.
- [ ] Complete the practical workbook.
- [ ] Build one security-focused mini-project.
- [ ] Review the solutions and document your learning.

Continue to the next module in the [CubicNova DevSecOps Roadmap](https://github.com/cubicnova/DevSecOps-Roadmap/tree/main/03-Python-for-DevSecOps).
