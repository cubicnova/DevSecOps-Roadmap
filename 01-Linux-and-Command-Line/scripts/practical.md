# Practical Exercises: Linux Bash Scripts

Complete the tasks in a disposable working directory. Do not run destructive exercises on production files.

## Exercise 1 — Customize a greeting

1. Run `hello.sh` with and without a name.
2. Change the default name.
3. Add a line showing the current date.

**Success criteria:** no-name execution works, and names containing spaces are printed correctly.

## Exercise 2 — File inventory

1. Create three text files, including one with multiple lines.
2. Run `file_report.sh` on each file.
3. Modify a copy to also show the file's last-modified time.
4. Test behavior when a path does not exist.

**Success criteria:** invalid input produces a helpful error and a non-zero exit code.

## Exercise 3 — Backup and verification

1. Create a directory tree with nested folders and sample files.
2. Back it up with `backup_directory.sh`.
3. List the archive contents using `tar -tzf`.
4. Extract it into a different temporary directory.
5. Compare the restored files with the originals.

**Success criteria:** the archive is timestamped, readable, and contains the expected files.

## Exercise 4 — Disk usage report

1. Run `disk_usage.sh` for the current directory and `/tmp`.
2. Add a check that warns when a filesystem is at least 80% full.
3. Ensure a missing path is handled cleanly.

**Success criteria:** report includes both filesystem capacity and target directory size.

## Exercise 5 — Log analysis

1. Build a sample log containing `INFO`, `WARN`, `ERROR`, and `FATAL` entries.
2. Run `log_summary.sh`.
3. Add a count for failed authentication messages.
4. Test an empty log file.

**Success criteria:** the script does not fail just because a search finds no matches.

## Exercise 6 — Input validation

1. Try a valid username and several invalid values.
2. Change the permitted length range.
3. Explain why this format check does not establish account existence or authorization.

**Success criteria:** invalid input is rejected with a non-zero exit status.

## Exercise 7 — Health snapshot

1. Run `system_health.sh`.
2. Identify which commands provide uptime, memory, disk, and process data.
3. Add a check for available disk space on `/`.
4. Explain why a single snapshot is not continuous monitoring.

**Success criteria:** the script is read-only and gives useful output when optional tools are missing.

## Exercise 8 — Safe cleanup

1. Create a temporary directory with files of different modification ages.
2. Run the cleanup script without `--delete`.
3. Review every printed path.
4. Only in the disposable directory, test `--delete`.
5. Explain what `-type f`, `-mtime`, and `-xdev` do.

**Success criteria:** preview mode makes no changes; deletion requires an explicit flag.

## Exercise 9 — Integrity manifest

1. Generate a SHA-256 manifest for a directory.
2. Verify the files with `sha256sum -c`.
3. Change one file and verify again.
4. Explain the difference between integrity checking and malware detection.

**Success criteria:** the changed file fails checksum verification.

## Exercise 10 — Make a script more robust

Choose one script and add:
- a `usage()` function;
- clear validation for all arguments;
- helpful errors on standard error;
- meaningful exit codes;
- a short header comment describing its purpose.

Then run:

```bash
bash -n ./your_script.sh
shellcheck ./your_script.sh
```

`bash -n` checks syntax. `shellcheck` is optional and must be installed separately.

## Reflection questions

1. Why is `set -Eeuo pipefail` useful, and what are its limitations?
2. Why should file paths be quoted?
3. Why should destructive scripts provide preview mode?
4. Why should secrets not be embedded in source code?
5. What additional controls would be needed before running these scripts on production servers?
