# Bash Script Examples and Walkthroughs

This guide explains how to run and understand the scripts in this folder.

## 1. Hello script

```bash
./hello.sh
./hello.sh "DevSecOps Learner"
```

The first argument becomes the name. `${1:-Learner}` uses `Learner` when no argument is supplied.

## 2. File report

```bash
printf 'first line\nsecond line\n' > sample.txt
./file_report.sh sample.txt
```

The script validates the input and reports the byte count, line count, and permissions.

## 3. Back up a directory

```bash
mkdir -p demo/source demo/backups
printf 'sample content\n' > demo/source/notes.txt
./backup_directory.sh demo/source demo/backups
tar -tzf demo/backups/source_*.tar.gz
```

The backup is timestamped and compressed. The script refuses a destination nested inside the source, which avoids recursively archiving its own output.

## 4. Check disk usage

```bash
./disk_usage.sh .
./disk_usage.sh /tmp
```

`df` reports filesystem capacity; `du` reports the target's disk usage. Use paths you can read.

## 5. Summarize logs

Create a sample log:

```bash
cat > sample.log <<'EOF'
INFO service started
WARNING disk usage is high
ERROR failed to connect
INFO retry scheduled
FATAL request failed
EOF

./log_summary.sh sample.log
```

The counts are based on simple text matches, not a full log parser. A line may contain more than one matching keyword.

## 6. Validate an input format

```bash
./user_input_validator.sh learner_01
./user_input_validator.sh "not valid!"
```

This checks a sample username format only. It does not create a Linux account or prove that a username is available.

## 7. System health snapshot

```bash
./system_health.sh
```

The script reads system information and does not change system configuration. Process and memory values are only a snapshot.

## 8. Cleanup preview

```bash
mkdir -p demo/old-files
touch demo/old-files/keep.txt
./cleanup_old_files.sh demo/old-files 30
```

The default mode is preview-only. To test the age filter without waiting, you can set a file's timestamp in a disposable test directory:

```bash
touch -d '45 days ago' demo/old-files/old.txt
./cleanup_old_files.sh demo/old-files 30
```

Only after reviewing the output should you try deletion in a disposable directory:

```bash
./cleanup_old_files.sh demo/old-files 30 --delete
```

**Caution:** `--delete` permanently removes matching regular files. Do not test it against system directories or important data.

## 9. Checksum manifest

```bash
mkdir -p demo/checksum-input
printf 'alpha\n' > demo/checksum-input/a.txt
printf 'beta\n' > demo/checksum-input/b.txt
./checksum_manifest.sh demo/checksum-input demo/SHA256SUMS
sha256sum -c demo/SHA256SUMS
```

A checksum can help detect later changes. It does not prove that a file is safe or that the original source was trustworthy.

## Bash safety basics

- Quote paths: `"$path"`.
- Check required arguments before using them.
- Prefer a preview before destructive operations.
- Do not paste untrusted text into `eval`.
- Avoid `chmod 777`; grant only required permissions.
- Use `shellcheck` to identify common shell scripting mistakes.
