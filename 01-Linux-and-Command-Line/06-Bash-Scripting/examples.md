# 💡 Bash Scripting — Examples

Run these examples in `~/bash-lab`. Read each script before executing it.

## 1. Hello World

```bash
cat > hello.sh <<'EOF'
#!/usr/bin/env bash
echo "Hello from Bash!"
EOF

chmod u+x hello.sh
./hello.sh
```

## 2. Variables and formatting

```bash
name="DevSecOps Learner"
topic="Bash Scripting"

printf 'Name: %s\nTopic: %s\n' "$name" "$topic"
```

Assignments must not contain spaces around `=`.

## 3. Input

```bash
read -r -p "Enter your name: " name
printf 'Hello, %s!\n' "$name"
```

## 4. Conditions

```bash
path="hello.sh"

if [[ -f "$path" ]]; then
    echo "Regular file exists."
elif [[ -d "$path" ]]; then
    echo "Path is a directory."
else
    echo "Path does not exist as a regular file or directory."
fi
```

## 5. Numeric comparisons

```bash
read -r -p "Enter an integer: " number

if [[ "$number" =~ ^-?[0-9]+$ ]]; then
    if (( number >= 0 )); then
        echo "Non-negative integer"
    else
        echo "Negative integer"
    fi
else
    echo "Invalid integer"
fi
```

Validate user input before using it in arithmetic or system commands.

## 6. Loops

```bash
for item in files processes services; do
    printf 'Topic: %s\n' "$item"
done

for ((i = 1; i <= 5; i++)); do
    echo "$i"
done

count=1
while (( count <= 3 )); do
    echo "Count: $count"
    ((count += 1))
done
```

## 7. Functions

```bash
path_exists() {
    local path="$1"
    [[ -e "$path" ]]
}

if path_exists "hello.sh"; then
    echo "Found."
else
    echo "Not found."
fi
```

A function's exit status is the status of its last command unless explicitly changed.

## 8. Arguments and usage messages

```bash
#!/usr/bin/env bash

if [[ $# -ne 1 ]]; then
    printf 'Usage: %s FILE\n' "$0" >&2
    exit 2
fi

file=$1

if [[ -f "$file" && -r "$file" ]]; then
    wc -l -- "$file"
else
    printf 'Error: file does not exist or is not readable: %s\n' "$file" >&2
    exit 1
fi
```

Save as `count-lines.sh`, then run:

```bash
chmod u+x count-lines.sh
./count-lines.sh hello.sh
```

## 9. Exit status

```bash
test -f hello.sh
status=$?
printf 'Exit status: %s\n' "$status"
```

Capture `$?` immediately after the command you want to inspect. A zero status conventionally means success.

## 10. Create and analyze a sample log

```bash
mkdir -p output
cat > output/app.log <<'EOF'
INFO: Service started
ERROR: Example failed request
INFO: Service running
ERROR: Example timeout
EOF

grep -n "ERROR" output/app.log
grep -c "ERROR" output/app.log
wc -l output/app.log
```

`grep -c` counts matching lines, not necessarily the total number of occurrences.

## 11. Read a file line by line

```bash
while IFS= read -r line || [[ -n "$line" ]]; do
    printf 'Read: %s\n' "$line"
done < output/app.log
```

This handles spaces and backslashes and also processes a final line that lacks a newline.

## 12. Logging to a file

```bash
log_file="output/script.log"
mkdir -p output

printf '[%s] Script started\n' "$(date '+%F %T')" >> "$log_file"
printf '[%s] Script completed\n' "$(date '+%F %T')" >> "$log_file"

tail -n 10 "$log_file"
```

Treat logs as potentially sensitive. Choose an appropriate location and permissions.

## 13. Temporary files and cleanup

```bash
tmp_file=$(mktemp)
cleanup() {
    rm -f -- "$tmp_file"
}
trap cleanup EXIT

printf 'Temporary sample\n' > "$tmp_file"
cat "$tmp_file"
```

`mktemp` creates a unique temporary file. `trap` runs the cleanup function when the shell exits. For more complex scripts, consider signals and cleanup behavior carefully.

## 14. Safer script template

```bash
#!/usr/bin/env bash
set -Eeuo pipefail

log() {
    printf '[%s] %s\n' "$(date '+%F %T')" "$*"
}

if [[ $# -ne 1 ]]; then
    printf 'Usage: %s DIRECTORY\n' "$0" >&2
    exit 2
fi

target=$1

if [[ ! -d "$target" ]]; then
    printf 'Error: not a directory: %s\n' "$target" >&2
    exit 1
fi

log "Listing regular files in $target"
find "$target" -maxdepth 1 -type f -print
```

`set -Eeuo pipefail` changes error handling but does not make every failure automatically safe or obvious. Test branches and expected failure cases.

## 15. Debugging

```bash
bash -n hello.sh
bash -x hello.sh
```

- `bash -n` checks syntax without running the script.
- `bash -x` traces commands as Bash executes them. Be careful: traces can expose secrets if the script handles sensitive values.

If installed, run ShellCheck:

```bash
shellcheck hello.sh
```
