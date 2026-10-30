# 07 — Environment Variables

![Linux](https://img.shields.io/badge/Linux-Environment%20Variables-FCC624?logo=linux&logoColor=black)
![Level](https://img.shields.io/badge/Level-Beginner%20to%20Intermediate-blue)
![Focus](https://img.shields.io/badge/Focus-DevSecOps%20%7C%20Shell%20Scripting-red)

## Overview

Environment variables are name-value pairs passed to processes. They help configure shells, applications, development tools, and automation without hard-coding configuration into programs. Each process has its own environment and commonly inherits a copy from its parent process.

This module covers environment variables in Bash, including how to inspect, set, export, unset, persist, and use them safely in scripts and DevSecOps workflows.

## Learning Objectives

By the end of this module, you will be able to:

- Explain the difference between shell variables and environment variables.
- Inspect variables with `printenv`, `env`, and shell expansion.
- Set variables with assignments and `export`.
- Pass temporary variables to a single command.
- Remove variables with `unset`.
- Understand common variables such as `PATH`, `HOME`, `USER`, `SHELL`, `PWD`, `LANG`, and `EDITOR`.
- Safely modify `PATH`.
- Persist configuration using appropriate shell startup files.
- Use variables in Bash scripts.
- Identify environment-variable risks and avoid exposing secrets.

## Topics Covered

### 1. Fundamentals

- Variable names and values
- Case sensitivity
- Shell variables vs. exported environment variables
- Parent and child process inheritance
- Empty vs. unset variables

### 2. Inspecting Variables

- `echo "$VARIABLE"`
- `printf`
- `printenv`
- `env`
- `set`
- `export -p`

### 3. Creating and Modifying Variables

- `NAME=value`
- `export NAME=value`
- Exporting an existing shell variable
- Temporary command-specific variables
- `unset`

### 4. Common Environment Variables

| Variable | Typical purpose |
|---|---|
| `HOME` | User's home directory |
| `USER` | Commonly the current username |
| `LOGNAME` | Login name in many environments |
| `SHELL` | Configured login shell in many environments |
| `PWD` | Current working directory maintained by the shell |
| `PATH` | Directories searched for executable commands |
| `LANG` | Default locale |
| `EDITOR` | Preferred editor for some programs |
| `TERM` | Terminal type |
| `TMPDIR` | Optional temporary directory setting |

Values and availability can differ by session, distribution, and application.

### 5. Persistence and Startup Files

- `~/.bashrc`
- `~/.profile`
- `~/.bash_profile`
- `/etc/profile`
- `/etc/environment`
- `/etc/profile.d/`

Startup-file behavior depends on whether Bash is interactive, a login shell, and on distribution configuration. `/etc/environment` is commonly processed by PAM-based login environments and is not a shell script; use plain `NAME=value` entries there.

### 6. Environment Variables in Scripts

- Reading variables
- Default values with `${VAR:-default}`
- Required values with `${VAR:?message}`
- Passing configuration into scripts
- Quoting variable expansions
- Exit status and validation

### 7. PATH Management

- Viewing `PATH`
- Adding a personal `bin` directory
- Avoiding empty or untrusted path entries
- Command lookup with `command -v`
- Diagnosing command-not-found issues

### 8. Security and DevSecOps

- Avoiding secrets in source control
- Minimizing secret exposure
- Restricting permissions on configuration files
- Avoiding environment dumps in logs
- Using dedicated secret managers for sensitive production credentials
- Separating development, test, and production configuration

## Essential Commands

| Command | Purpose |
|---|---|
| `printenv` | Print exported environment variables |
| `env` | Display or modify an environment for a command |
| `set` | Display shell variables, functions, and shell options |
| `export` | Mark variables for inheritance by child processes |
| `unset` | Remove a variable |
| `printf` | Print formatted values |
| `source FILE` | Read a shell file in the current shell |
| `command -v NAME` | Find how the shell resolves a command |
| `declare -p NAME` | Inspect a Bash variable declaration |

## Key Concepts

### Shell variable vs. environment variable

```bash
GREETING="Hello"
```

This creates a shell variable. Child processes do not normally inherit it.

```bash
export GREETING="Hello"
```

This exports the variable so subsequently started child processes inherit it.

### One-command variable

```bash
MODE=development ./app.sh
```

The assignment is available to that command and its child processes, without setting `MODE` in the current shell.

### Remove a variable

```bash
unset GREETING
```

This removes the shell variable and its exported status from the current shell.

## Safe Lab Environment

Use a Linux VM or a non-production shell. Do not overwrite `PATH` with an incomplete value. Do not place real credentials in example files or commit secrets to Git. Environment variables are convenient configuration inputs, but they are not a dedicated secrets vault; they may be exposed through process inspection, diagnostics, logs, crash reports, or application behavior depending on the system.

## Repository Files

- `README.md` — concepts, commands, and learning objectives
- `examples.md` — command demonstrations
- `practical.md` — hands-on exercises
- `solution.md` — suggested solutions and explanations

## Completion Checklist

- [ ] Explain shell variables and environment variables.
- [ ] Inspect environment variables.
- [ ] Export a variable and verify child-process inheritance.
- [ ] Set a variable for one command only.
- [ ] Unset a variable and distinguish unset from empty.
- [ ] Explain common variables such as `PATH` and `HOME`.
- [ ] Persist a non-sensitive variable appropriately.
- [ ] Write a Bash script that validates required configuration.
- [ ] Update `PATH` safely.
- [ ] Explain why environment variables are not a complete secrets-management solution.

## Further Reading

- [GNU Bash Manual — Environment](https://www.gnu.org/software/bash/manual/html_node/Environment.html)
- [Linux `environ(7)` Manual](https://man7.org/linux/man-pages/man7/environ.7.html)
- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
- [Linuxize — Environment Variables](https://linuxize.com/post/how-to-set-and-list-environment-variables-in-linux/)

## Next Module

Continue to the next module in the repository to build on shell configuration and command-line automation.
