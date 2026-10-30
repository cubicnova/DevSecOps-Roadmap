# Linux Command-Line Scripts

A practical collection of beginner-friendly Bash scripts for Linux administration, automation, and DevSecOps learning.

## Learning objectives

- Write Bash scripts with a safe, predictable structure.
- Accept command-line arguments and validate input.
- Automate common file, system, and reporting tasks.
- Handle failures, permissions, and logs.
- Apply security-minded defaults such as least privilege and careful path validation.

## Requirements

- Linux, macOS, WSL, or another environment with Bash.
- Common utilities such as `date`, `find`, `du`, `df`, `tar`, `awk`, and `grep`.
- For system-level tasks, use a disposable lab VM and review every command before running it.

Check your shell:

```bash
bash --version
```

Make a script executable and run it:

```bash
chmod +x script.sh
./script.sh
```

Or run it explicitly with Bash:

```bash
bash script.sh
```

## Scripts in this folder

| Script | Purpose |
|---|---|
| `hello.sh` | Bash starter, variables, and output |
| `file_report.sh` | Report file metadata and size |
| `backup_directory.sh` | Create a timestamped compressed backup |
| `disk_usage.sh` | Report disk and directory usage |
| `log_summary.sh` | Count matching log levels in a supplied log file |
| `user_input_validator.sh` | Validate a simple username input |
| `system_health.sh` | Print basic CPU/load, memory, disk, and uptime information |
| `cleanup_old_files.sh` | Preview or remove old files under a chosen directory |
| `checksum_manifest.sh` | Generate SHA-256 checksums for files |
| `README.md` | This guide |
| `examples.md` | Walkthroughs and expected behavior |
| `practical.md` | Exercises to complete |
| `solutions.md` | Reference solutions and explanations |

## Quick start

```bash
cd scripts
chmod +x *.sh
./hello.sh
./system_health.sh
./disk_usage.sh /
```

For scripts that accept a path, pass an explicit path and begin with a test directory. Avoid running cleanup or backup scripts against important production paths until you have reviewed the code and tested it on sample data.

## Safe scripting conventions

- Use `#!/usr/bin/env bash` as the interpreter line.
- Prefer `set -Eeuo pipefail` for scripts where unset variables or failed commands should stop execution.
- Quote variable expansions, for example `"$target"`.
- Validate arguments before acting on them.
- Do not hard-code passwords, API keys, or other secrets in scripts.
- Avoid `sudo` unless it is genuinely required.
- For destructive operations, offer a dry-run/preview first.
- Treat log files and command output as untrusted data.
- Use `shellcheck` when available:

```bash
shellcheck ./*.sh
```

## Troubleshooting

- **Permission denied:** run `chmod +x script.sh` or use `bash script.sh`.
- **Bad interpreter / CRLF:** convert line endings with `dos2unix script.sh` if available.
- **Command not found:** check the dependency and install it through your distribution's trusted package manager.
- **Unexpected path behavior:** use absolute paths while learning and quote paths containing spaces.

## Suggested learning sequence

1. Run `hello.sh` and read each line.
2. Run `file_report.sh` against a sample file.
3. Create a temporary directory and test the backup script.
4. Read a sample log using `log_summary.sh`.
5. Run `cleanup_old_files.sh` in preview mode before trying deletion.
6. Complete `practical.md` and compare your work with `solutions.md`.

These examples are educational. Review them and test in a non-production environment before adapting them to real systems.
