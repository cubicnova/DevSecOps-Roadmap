# ✅ Bash Scripting — Solutions

These are suggested solutions. Run them from `~/bash-lab` and test both successful and unsuccessful inputs.

## Setup

```bash
mkdir -p ~/bash-lab
cd ~/bash-lab
```

## Lab 1 — Hello script

Create `hello.sh`:

```bash
#!/usr/bin/env bash
printf 'Hello from Bash!\n'
printf 'Learning with CubicNova.\n'
```

Run:

```bash
bash hello.sh
chmod u+x hello.sh
./hello.sh
```

## Lab 2 — Variables and input

```bash
#!/usr/bin/env bash

name="Linux Learner"
topic="Bash Scripting"

read -r -p "What command are you learning? " command_name

printf 'Name: %s\nTopic: %s\nFavorite command: %s\n' \
    "$name" "$topic" "$command_name"
```

Quoting preserves spaces in the input value.

## Lab 3 — File checker

Save as `file-check.sh`:

```bash
#!/usr/bin/env bash

if [[ $# -ne 1 ]]; then
    printf 'Usage: %s PATH\n' "$0" >&2
    exit 2
fi

path=$1

if [[ -f "$path" ]]; then
    printf 'Regular file: %s\n' "$path"
elif [[ -d "$path" ]]; then
    printf 'Directory: %s\n' "$path"
elif [[ -e "$path" ]]; then
    printf 'Path exists but is not a regular file or directory: %s\n' "$path"
else
    printf 'Path not found: %s\n' "$path" >&2
    exit 1
fi
```

Test:

```bash
bash file-check.sh hello.sh
bash file-check.sh .
bash file-check.sh "missing path.txt"
```

## Lab 4 — Number validation

```bash
#!/usr/bin/env bash

read -r -p "Enter an integer: " value

if [[ ! "$value" =~ ^-?[0-9]+$ ]]; then
    printf 'Error: please enter a whole integer.\n' >&2
    exit 2
fi

if (( value < 0 )); then
    echo "Negative"
elif (( value == 0 )); then
    echo "Zero"
else
    echo "Positive"
fi
```

This validates integer syntax before arithmetic. For applications that accept arbitrary-length integers, additional range handling may be necessary because Bash arithmetic uses bounded integer values.

## Lab 5 — Loops and functions

```bash
#!/usr/bin/env bash

for ((i = 1; i <= 10; i++)); do
    printf '%s\n' "$i"
done

for topic in Linux Bash Networking Security; do
    printf 'Topic: %s\n' "$topic"
done

path_exists() {
    local path=$1
    [[ -e "$path" ]]
}

if path_exists "hello.sh"; then
    echo "hello.sh exists"
else
    echo "hello.sh does not exist"
fi
```

## Lab 6 — Log analyzer

Create sample data:

```bash
mkdir -p logs
cat > logs/app.log <<'EOF'
INFO: Service started
ERROR: Sample timeout
INFO: Health check passed
ERROR: Sample failed request
INFO: Service stopped
EOF
```

Save as `log-analyzer.sh`:

```bash
#!/usr/bin/env bash

if [[ $# -ne 1 ]]; then
    printf 'Usage: %s LOG_FILE\n' "$0" >&2
    exit 2
fi

log_file=$1

if [[ ! -f "$log_file" || ! -r "$log_file" ]]; then
    printf 'Error: file is missing or unreadable: %s\n' "$log_file" >&2
    exit 1
fi

matches_file=$(mktemp)
trap 'rm -f -- "$matches_file"' EXIT

if grep -n 'ERROR' "$log_file" > "$matches_file"; then
    printf 'ERROR lines found: '
    wc -l < "$matches_file"
    cat "$matches_file"
else
    status=$?
    if [[ "$status" -eq 1 ]]; then
        echo "No ERROR lines found."
    else
        printf 'Error while searching log file.\n' >&2
        exit "$status"
    fi
fi
```

Run:

```bash
chmod u+x log-analyzer.sh
./log-analyzer.sh logs/app.log
```

This example uses a temporary file to separate `grep`'s output from its exit status. For more complex log formats, account for case sensitivity and log rotation.

## Lab 7 — Directory listing with validation

```bash
#!/usr/bin/env bash

if [[ $# -ne 1 ]]; then
    printf 'Usage: %s DIRECTORY\n' "$0" >&2
    exit 2
fi

directory=$1

if [[ ! -d "$directory" ]]; then
    printf 'Error: not a directory: %s\n' "$directory" >&2
    exit 1
fi

find "$directory" -maxdepth 1 -type f -print
```

The quoted `"$directory"` handles paths containing spaces.

## Lab 8 — Temporary files

```bash
#!/usr/bin/env bash
set -u

tmp_file=$(mktemp)

cleanup() {
    rm -f -- "$tmp_file"
}
trap cleanup EXIT

printf 'Temporary test content\n' > "$tmp_file"
cat "$tmp_file"
```

The exit trap removes the temporary file when the shell exits normally. For more complex programs, test interruption and signal-handling behavior as well.

## Lab 9 — System information script

```bash
#!/usr/bin/env bash

printf 'Timestamp: %s\n' "$(date)"
printf 'Hostname: %s\n' "$(hostname)"
printf 'Kernel: %s\n' "$(uname -r)"

if [[ -r /etc/os-release ]]; then
    echo "Distribution:"
    grep -E '^(PRETTY_NAME|NAME|VERSION)=' /etc/os-release
else
    echo "Distribution metadata unavailable."
fi

if command -v uptime >/dev/null 2>&1; then
    uptime
else
    echo "uptime command unavailable."
fi

if command -v free >/dev/null 2>&1; then
    free -h
else
    echo "free command unavailable."
fi

if command -v df >/dev/null 2>&1; then
    df -h
else
    echo "df command unavailable."
fi
```

## Lab 10 — Mini project solution

Save as `system-health.sh`:

```bash
#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="$SCRIPT_DIR/output"
REPORT="$OUT_DIR/system-health-report.txt"

mkdir -p "$OUT_DIR" || {
    printf 'Error: cannot create output directory.\n' >&2
    exit 1
}

if ! command -v date >/dev/null 2>&1 ||
   ! command -v hostname >/dev/null 2>&1 ||
   ! command -v uname >/dev/null 2>&1; then
    printf 'Error: a required command is unavailable.\n' >&2
    exit 1
fi

{
    echo "===== System Health Report ====="
    printf 'Generated: %s\n' "$(date)"
    printf 'Hostname: %s\n' "$(hostname)"
    printf 'Kernel: %s\n' "$(uname -r)"
    echo

    echo "===== Distribution ====="
    if [[ -r /etc/os-release ]]; then
        grep -E '^(PRETTY_NAME|NAME|VERSION)=' /etc/os-release || true
    else
        echo "Distribution metadata unavailable."
    fi
    echo

    echo "===== Uptime ====="
    if command -v uptime >/dev/null 2>&1; then
        uptime
    else
        echo "uptime command unavailable."
    fi
    echo

    echo "===== Memory ====="
    if command -v free >/dev/null 2>&1; then
        free -h
    else
        echo "free command unavailable."
    fi
    echo

    echo "===== Disk Usage ====="
    if command -v df >/dev/null 2>&1; then
        df -h
    else
        echo "df command unavailable."
    fi
    echo

    echo "===== Top Processes by CPU ====="
    if command -v ps >/dev/null 2>&1; then
        ps -eo pid,ppid,user,%cpu,%mem,stat,comm --sort=-%cpu | head -n 15
    else
        echo "ps command unavailable."
    fi
} > "$REPORT" 2>&1

chmod 600 "$REPORT"
printf 'Report saved to: %s\n' "$REPORT"
```

Run and verify:

```bash
chmod u+x system-health.sh
bash -n system-health.sh
./system-health.sh
less output/system-health-report.txt
```

The script gathers information only; it does not stop services or delete user files. Treat the report as sensitive because it contains system details.

## Bonus — Debugging and ShellCheck

```bash
bash -n system-health.sh
bash -x system-health.sh
shellcheck system-health.sh
```

`bash -x` prints commands as they execute and may expose sensitive values in other scripts. Use it carefully.

## Reflection — Suggested answers

1. **Shebang:** Selects the interpreter used when the script is executed directly.
2. **Arguments:** `$1` is the first argument, `$#` is the count, and `"$@"` preserves each argument as a separate word.
3. **Quoting:** Prevents unwanted word splitting and pathname expansion.
4. **Exit status:** Zero conventionally indicates success; non-zero usually indicates failure or another result.
5. **Redirection:** `>` overwrites a destination; `>>` appends.
6. **`grep` status 1:** Means no matching lines were found, not necessarily an execution error.
7. **Strict options:** `set -u` treats many unset-variable expansions as errors; `set -o pipefail` makes a pipeline return a failure if a command in it fails, subject to pipeline rules.
8. **`set -e`:** Has context-dependent exceptions and does not replace deliberate error checks.
9. **Avoid `eval`:** It can reinterpret data as shell code, creating command-injection risk.
10. **`trap`:** Runs cleanup or other handler commands on shell exit or selected signals.

## Completion criteria

You can write and run Bash scripts, validate arguments, use variables and loops, inspect files and logs, handle common failures, and explain how your script avoids unsafe operations.
