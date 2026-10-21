# Reference Solutions and Explanations

The runnable reference scripts are included as individual `.sh` files. These notes explain important implementation choices and offer extensions for the practical exercises.

## Exercise 1 — Add the date

Add this line to `hello.sh`:

```bash
printf 'Date: %s\n' "$(date '+%Y-%m-%d')"
```

The command substitution runs `date` and places its output in the formatted string.

## Exercise 2 — Add modification time

On GNU/Linux, add to `file_report.sh`:

```bash
printf 'Modified: %s\n' "$(stat -c '%y' -- "$file")"
```

`stat` options vary across operating systems. The existing script already includes a fallback for permissions, but a portable production script should explicitly handle platform differences.

## Exercise 3 — Verify a backup

```bash
tar -tzf /path/to/backup.tar.gz
mkdir -p /tmp/restore-test
tar -xzf /path/to/backup.tar.gz -C /tmp/restore-test
```

For stronger verification, compare file lists and checksums between source and restored directories. Avoid extracting untrusted archives; archive paths and links should be reviewed first.

## Exercise 4 — Warn on high disk usage

A GNU/Linux example:

```bash
usage_pct=$(df -P / | awk 'NR == 2 {gsub(/%/, "", $5); print $5}')
if [[ "$usage_pct" =~ ^[0-9]+$ ]] && (( usage_pct >= 80 )); then
  printf 'Warning: root filesystem usage is %s%%\n' "$usage_pct" >&2
fi
```

This is a simple threshold check. Production monitoring should account for multiple filesystems, alert routing, and transient readings.

## Exercise 5 — Count authentication failures

For a basic text log:

```bash
grep -Eic 'failed password|authentication failure|invalid user' sample.log || true
```

Patterns differ by service and log format. Avoid assuming every log message is trustworthy or follows the same schema.

## Exercise 6 — Adjust username length

For example, this expression accepts 4–20 characters:

```bash
[[ "$username" =~ ^[a-zA-Z_][a-zA-Z0-9_-]{3,19}$ ]]
```

Regex validation only checks the supplied string's format. It does not check whether the account exists, whether the caller is authorized, or whether a remote system will accept the name.

## Exercise 7 — Disk space check

```bash
df -h /
```

This reports current filesystem usage. For a recurring alert, schedule the script carefully and send results to a monitored destination; a local printout alone is not an alerting system.

## Exercise 8 — Understand cleanup filters

The reference script uses:

```bash
find "$target" -xdev -type f -mtime "+$days" -print
```

- `-xdev`: do not descend into directories on other filesystems.
- `-type f`: match regular files, not directories or symlinks.
- `-mtime "+$days"`: match files whose age in 24-hour periods is greater than the threshold.
- `-print`: display matching paths without deleting them.

The deletion version adds `-delete`. Preview first and use only a disposable directory when learning.

## Exercise 9 — Verify checksums

```bash
sha256sum -c /path/to/SHA256SUMS
```

A changed file should fail verification. If an attacker can replace both the file and its manifest, the manifest alone is not a trusted source of truth. Protect the manifest separately or use a trusted signed artifact process.

## Exercise 10 — Syntax and lint checks

```bash
bash -n ./script.sh
shellcheck ./script.sh
```

Use quoted expansions, check exit statuses, avoid parsing `ls` output, and prefer `find ... -print0` with null-delimited reading when filenames may contain spaces or newlines.

## General production-readiness checklist

- [ ] Inputs are validated and paths are quoted.
- [ ] The script handles errors and returns meaningful exit codes.
- [ ] Destructive actions require explicit intent and have a preview.
- [ ] It does not store credentials or print secrets.
- [ ] Permissions are least-privilege.
- [ ] Logs do not expose sensitive information.
- [ ] It has been tested on representative sample data.
- [ ] A reviewer has inspected the code before production use.
