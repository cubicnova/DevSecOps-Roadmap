# Python for DevSecOps - Examples

A practical collection of small, safe Python examples that reinforce the concepts covered in `03-Python-for-DevSecOps`.

## Goals

- Practice Python syntax and reusable functions.
- Work with files, JSON, YAML-like configuration concepts, and environment variables.
- Learn safe operating-system and subprocess patterns.
- Add logging, exceptions, testing, and defensive input validation.
- Build reusable examples that can later become security automation utilities.

## Contents

```text
examples/
├── README.md
├── examples.md
├── practical.md
├── practical.ipynb
└── solutions.md
```

## How to use this folder

1. Read `examples.md` and run each short example locally.
2. Complete the exercises in `practical.md`.
3. Implement the TODOs in `practical.ipynb`.
4. Review `solutions.md` only after trying the tasks yourself.

## Requirements

- Python 3.10 or newer recommended.
- Examples use the Python standard library unless noted.
- No external systems are scanned or modified by these examples.

## Run examples

Save a code snippet as a `.py` file and run:

```bash
python example.py
```

For the notebook, open `practical.ipynb` in Jupyter Notebook, JupyterLab, or VS Code.

## Safe coding principles

- Validate input before using it.
- Use `pathlib` for file paths and handle expected errors.
- Do not hard-code passwords, API keys, or tokens.
- Prefer argument lists and `shell=False` when using `subprocess`.
- Add timeouts to subprocess calls that might wait indefinitely.
- Use synthetic data or systems you own or are explicitly authorized to assess.
- Keep logs useful, but do not log secrets or sensitive payloads.

## Further reading

- Python tutorial: https://docs.python.org/3/tutorial/
- Python standard library: https://docs.python.org/3/library/
- `pathlib`: https://docs.python.org/3/library/pathlib.html
- `logging`: https://docs.python.org/3/library/logging.html
- `subprocess`: https://docs.python.org/3/library/subprocess.html
- `unittest`: https://docs.python.org/3/library/unittest.html
