# 🐚 Bash Scripting

[![Bash](https://img.shields.io/badge/Shell-Bash-4EAA25?logo=gnubash&logoColor=white)](https://www.gnu.org/software/bash/)
[![Level](https://img.shields.io/badge/Level-Beginner_to_Intermediate-success)](.)
[![Roadmap](https://img.shields.io/badge/Path-DevSecOps-blue)](../../README.md)

Welcome to **Bash Scripting**, a module in the Linux and Command Line section of the **CubicNova DevSecOps Roadmap**. Learn to turn Linux commands into reusable scripts for automation, system checks, file management, log analysis, and DevSecOps workflows.

This module follows a step-by-step approach: start with a simple script, learn variables and input, add conditions and loops, build functions, handle errors safely, and finish with a system health report.

## 📚 Table of Contents

- [Learning Objectives](#-learning-objectives)
- [Prerequisites](#-prerequisites)
- [Step 1: Check Your Environment](#step-1-check-your-environment)
- [Step 2: Create Your First Script](#step-2-create-your-first-script)
- [Step 3: Understand the Shebang and Execution](#step-3-understand-the-shebang-and-execution)
- [Step 4: Variables and Quoting](#step-4-variables-and-quoting)
- [Step 5: Read User Input](#step-5-read-user-input)
- [Step 6: Exit Codes and Conditions](#step-6-exit-codes-and-conditions)
- [Step 7: Loops](#step-7-loops)
- [Step 8: Functions](#step-8-functions)
- [Step 9: Arguments](#step-9-arguments)
- [Step 10: Files and Text Processing](#step-10-files-and-text-processing)
- [Step 11: Safer Scripts and Error Handling](#step-11-safer-scripts-and-error-handling)
- [Step 12: Scheduling Basics](#step-12-scheduling-basics)
- [Hands-On Labs](#-hands-on-labs)
- [Mini Project](#-mini-project)
- [Module Files](#-module-files)
- [Best Practices](#-best-practices)
- [Learning Resources](#-learning-resources)
- [Next Steps](#-next-steps)

## 🎯 Learning Objectives

By the end of this module, you should be able to:

1. Create and run Bash scripts.
2. Use variables, input, arguments, and exit codes.
3. Write conditions, loops, and reusable functions.
4. Work with files and command output.
5. Handle errors and quote variables safely.
6. Use basic logging and validation.
7. Automate routine Linux administration tasks.
8. Explain safe practices for scripts used in DevSecOps.

## 🧰 Prerequisites

- A Linux terminal, Linux VM, WSL distribution, or another Bash environment.
- Basic commands such as `pwd`, `ls`, `mkdir`, `cat`, and `grep`.
- A text editor such as `nano`, `vim`, or VS Code.

Examples assume Bash. Some commands and options may differ on other shells or operating systems.

---

## Step 1: Check Your Environment

Confirm Bash is available:

```bash
bash --version
command -v bash
pwd
```

Create a dedicated practice folder:

```bash
mkdir -p ~/bash-lab
cd ~/bash-lab
```

Keep practice scripts and generated files inside this directory.

## Step 2: Create Your First Script

Create a file named `hello.sh`:

```bash
nano hello.sh
```

Add:

```bash
#!/usr/bin/env bash
echo "Hello from Bash!"
echo "Welcome to the CubicNova DevSecOps Roadmap."
```

Save and close the editor. Run it explicitly with Bash:

```bash
bash hello.sh
```

Expected output:

```text
Hello from Bash!
Welcome to the CubicNova DevSecOps Roadmap.
```

## Step 3: Understand the Shebang and Execution

The first line, `#!/usr/bin/env bash`, tells the operating system to use Bash to interpret the script when executed directly.

Make the script executable:

```bash
chmod u+x hello.sh
./hello.sh
```

Important distinctions:

- `bash hello.sh` asks Bash to read the file; the executable bit is not required.
- `./hello.sh` executes the file directly and normally requires execute permission.
- `./` specifies a path in the current directory; the current directory is not usually searched through `PATH`.

## Step 4: Variables and Quoting

Create `variables.sh`:

```bash
#!/usr/bin/env bash

name="DevSecOps Learner"
roadmap="CubicNova DevSecOps Roadmap"

echo "Hello, $name"
printf 'Learning path: %s\n' "$roadmap"
```

Run:

```bash
bash variables.sh
```

Key ideas:

- Assignments have no spaces around `=`.
- Use `$variable` or `${variable}` to expand a variable.
- Quote variable expansions: `"$name"`.
- Use `printf` when you want predictable formatting.

Example with a path containing spaces:

```bash
report_name="weekly report.txt"
printf '%s\n' "$report_name"
```

## Step 5: Read User Input

Create `input.sh`:

```bash
#!/usr/bin/env bash

read -r -p "Enter your name: " name
printf 'Welcome, %s!\n' "$name"
```

`read -r` prevents backslashes from being interpreted as escape characters. Always quote variables when using them as arguments.

## Step 6: Exit Codes and Conditions

Commands generally return an exit status: `0` usually means success; non-zero means failure or another condition.

```bash
if [[ -f "hello.sh" ]]; then
    echo "Script exists."
else
    echo "Script not found."
fi
```

Check a command's exit status immediately:

```bash
grep -q "Bash" hello.sh
status=$?

if [[ "$status" -eq 0 ]]; then
    echo "Pattern found."
else
    echo "Pattern not found or grep encountered an error."
fi
```

`grep` commonly returns `0` for a match, `1` for no match, and a larger non-zero status for an error. Exit codes are command-specific.

Useful tests:

| Test | Meaning |
|---|---|
| `-e PATH` | Path exists |
| `-f PATH` | Regular file exists |
| `-d PATH` | Directory exists |
| `-r PATH` | Path is readable |
| `-w PATH` | Path is writable |
| `-x PATH` | Path is executable or traversable, depending on type |
| `-z STRING` | String is empty |
| `-n STRING` | String is non-empty |
| `"$a" -eq "$b"` | Integer equality inside `[[ ... ]]` |

## Step 7: Loops

### `for` loop

```bash
for item in alpha beta gamma; do
    printf '%s\n' "$item"
done
```

### Numeric loop

```bash
for ((i = 1; i <= 5; i++)); do
    echo "Iteration $i"
done
```

### `while` loop

```bash
count=1
while [[ "$count" -le 3 ]]; do
    echo "Count: $count"
    ((count += 1))
done
```

Use loops to process a known set of items or repeat a task while a condition holds.

## Step 8: Functions

```bash
#!/usr/bin/env bash

greet() {
    local name="$1"
    printf 'Hello, %s!\n' "$name"
}

greet "Linux Learner"
```

Functions help keep scripts readable and avoid repeated code. Use `local` for function variables when appropriate.

## Step 9: Arguments

Create `arguments.sh`:

```bash
#!/usr/bin/env bash

printf 'Script: %s\n' "$0"
printf 'First argument: %s\n' "${1:-not provided}"
printf 'Number of arguments: %s\n' "$#"
```

Run:

```bash
bash arguments.sh Linux Security
```

Common argument variables:

- `$0`: Script name or invocation path.
- `$1`, `$2`, etc.: Positional arguments.
- `$#`: Number of positional arguments.
- `"$@"`: All positional arguments, preserved as separate words when quoted.
- `"$*"`: Arguments combined into one string when quoted.

Validate arguments before using them in file operations or other sensitive actions.

## Step 10: Files and Text Processing

```bash
mkdir -p output
printf 'INFO: Started\nERROR: Example failure\nINFO: Finished\n' > output/app.log

grep -n "ERROR" output/app.log
wc -l output/app.log
head -n 2 output/app.log
tail -n 2 output/app.log
```

Read files safely, including lines with backslashes:

```bash
while IFS= read -r line || [[ -n "$line" ]]; do
    printf 'Line: %s\n' "$line"
done < output/app.log
```

Avoid parsing `ls` output in scripts. Use shell globs or `find` with null delimiters when filenames may contain unusual characters.

## Step 11: Safer Scripts and Error Handling

A common starting point is:

```bash
#!/usr/bin/env bash
set -Eeuo pipefail
```

This enables several strict behaviors, but it is not a substitute for validation and error handling. `set -e` has exceptions in conditions, pipelines, and other contexts; understand the script's control flow.

Example argument validation:

```bash
#!/usr/bin/env bash
set -u

if [[ $# -ne 1 ]]; then
    printf 'Usage: %s DIRECTORY\n' "$0" >&2
    exit 2
fi

target=$1

if [[ ! -d "$target" ]]; then
    printf 'Error: not a directory: %s\n' "$target" >&2
    exit 1
fi

find "$target" -maxdepth 1 -type f -print
```

Security essentials:

- Quote variables.
- Validate arguments and paths.
- Avoid `eval`.
- Avoid constructing shell commands from untrusted input.
- Use `mktemp` for temporary files when appropriate.
- Use traps to clean up temporary resources.
- Do not store passwords, API keys, or tokens in scripts or Git.
- Test destructive operations on disposable data.

## Step 12: Scheduling Basics

On systems with cron, edit your own crontab:

```bash
crontab -e
crontab -l
```

Example entry to run a script every day at 8:00 AM:

```cron
0 8 * * * /home/USERNAME/bash-lab/hello.sh
```

Replace `USERNAME` with the correct account name and use the actual absolute path. Cron uses a limited environment, so scripts should use absolute paths where practical and send output to a controlled log if needed. Confirm the machine's timezone and cron service behavior before relying on a schedule.

---

## 🧪 Hands-On Labs

1. **Hello script:** Create and run `hello.sh`.
2. **Variables:** Print a name and learning path using variables.
3. **Input:** Ask the user for a name and greet them.
4. **File checker:** Accept a path and report whether it is a regular file.
5. **Loop:** Print numbers from 1 to 10.
6. **Function:** Create a reusable function that checks whether a path exists.
7. **Log analyzer:** Count `ERROR` lines in a sample log.
8. **Argument validation:** Require a directory argument and list its regular files.
9. **Error handling:** Report invalid input with a non-zero exit code.
10. **Mini project:** Generate a system health report.

See [`practical.md`](practical.md) for detailed tasks and [`solutions.md`](solutions.md) for suggested solutions.

## 🚀 Mini Project: Linux System Health Report

Build a script that reports:

- Timestamp and hostname.
- Kernel and distribution details.
- Uptime and memory usage.
- Disk usage.
- Top processes by CPU usage.
- A clear success or error message if a required command is unavailable.

Keep the report in `~/bash-lab/output/`, restrict its permissions where appropriate, and avoid including secrets. The script should only inspect the system; it must not modify services or delete files.

## 📂 Module Files

| File | Purpose |
|---|---|
| `README.md` | Step-by-step tutorial and reference |
| `examples.md` | Small runnable Bash examples |
| `practical.md` | Guided labs and exercises |
| `solutions.md` | Suggested solutions and project implementation |

## ✅ Best Practices

- Use a clear shebang such as `#!/usr/bin/env bash`.
- Use meaningful variable and function names.
- Quote variable expansions.
- Validate arguments and handle failures.
- Use `printf` for predictable output.
- Prefer `[[ ... ]]` for Bash conditional expressions.
- Avoid `eval` and unsafe command construction.
- Keep secrets out of scripts and repositories.
- Test scripts with sample data before using them on important systems.
- Consider ShellCheck for static analysis.

## 📚 Learning Resources

- [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/) — authoritative Bash syntax and behavior.
- [ShellCheck](https://www.shellcheck.net/) — static analysis for shell scripts.
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html) — practical style and safety guidance.
- [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/coreutils.html) — common command-line utilities.

## 🗺️ Next Steps

Continue to the next module in the [Linux and Command Line](../README.md) section of the [CubicNova DevSecOps Roadmap](../../README.md).

**Automate repetitive tasks. Validate every input. Build scripts securely.**
