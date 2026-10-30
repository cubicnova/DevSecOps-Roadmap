# ✅ Files and Directories — Solutions

These are suggested solutions to the practical labs. Run them from your own practice directory. Output may vary by Linux distribution and system state.

## Setup

```bash
mkdir -p ~/file-lab-practical
cd ~/file-lab-practical
```

## Lab 1 — Directory structure

```bash
mkdir -p documents/{reports,notes} logs images backups
find . -maxdepth 3 -print
```

This creates the required directories. `find` displays the structure.

## Lab 2 — Create and inspect files

```bash
touch documents/notes/readme.txt
printf 'Linux file handling practice\nSecond line of sample text\n' > documents/notes/readme.txt
touch logs/application.log
cat documents/notes/readme.txt
file documents/notes/readme.txt logs/application.log
stat documents/notes/readme.txt logs/application.log
```

The redirection operator `>` writes the supplied text and replaces any existing content in the target file.

## Lab 3 — Copy, rename, and move

Run in order:

```bash
cp documents/notes/readme.txt backups/readme-backup.txt
mv documents/notes/readme.txt documents/notes/linux-notes.txt
mv backups/readme-backup.txt documents/reports/readme-backup.txt
ls -l documents/notes documents/reports
```

The original is renamed, while its copied backup is moved into `documents/reports`.

## Lab 4 — Spaces and hidden files

```bash
mkdir -p "Case Notes"
touch "Case Notes/incident summary.txt"
touch .lab-settings
ls -la
ls -l "Case Notes"
```

Quote paths with spaces. `ls -a` includes hidden names that start with a dot.

## Lab 5 — Search

Create the sample files first:

```bash
touch logs/app.log logs/security.log documents/reports/weekly.txt
```

Find regular files:

```bash
find . -type f
```

Find `.log` files:

```bash
find . -type f -name "*.log"
```

Find text files without case sensitivity:

```bash
find . -type f -iname "*.txt"
```

Find empty files:

```bash
find . -type f -empty
```

Find directories:

```bash
find . -type d
```

Quote wildcard patterns passed to `find` so the shell does not expand them before `find` receives them.

## Lab 6 — Metadata and disk usage

```bash
stat logs/app.log
du -sh .
du -h --max-depth=1 .
df -h
```

`du` reports space used by paths; `df` reports capacity and usage for mounted filesystems. The `--max-depth` option is supported by GNU `du`; use `man du` if your implementation differs.

## Lab 7 — Links

Create a symbolic link using a relative path from the workspace root:

```bash
ln -s documents/notes/linux-notes.txt notes-link.txt
readlink notes-link.txt
ls -l notes-link.txt documents/notes/linux-notes.txt
```

If hard links are supported and you have permission:

```bash
ln documents/notes/linux-notes.txt notes-hardlink.txt
ls -li documents/notes/linux-notes.txt notes-hardlink.txt
```

The target and hard link should show the same inode on the same filesystem. The symbolic link has its own inode and stores a path. A relative symbolic link may stop resolving if the target is moved relative to the link.

## Lab 8 — Archive and restore

```bash
tar -czf documents-logs.tar.gz documents logs
tar -tzf documents-logs.tar.gz
mkdir -p restore-check
tar -xzf documents-logs.tar.gz -C restore-check
find restore-check -maxdepth 4 -print
```

The archive contains the selected `documents` and `logs` directory trees. Inspect archives from untrusted sources before extracting them.

## Lab 9 — Permissions

```bash
touch documents/private.txt
chmod 600 documents/private.txt
stat documents/private.txt
ls -l documents/private.txt
```

Typical permission display: `-rw-------`. This means the owner can read and write; group and others have no file permissions. Access is also affected by directory permissions, ACLs, and other system controls.

## Lab 10 — Safe cleanup

Inspect before removing anything:

```bash
find . -maxdepth 3 -print
```

Remove a temporary file interactively:

```bash
rm -i logs/application.log
```

Remove an empty directory:

```bash
mkdir empty-practice-dir
rmdir empty-practice-dir
```

Keep the main `file-lab-practical` workspace intact. Do not run broad recursive deletion commands.

## Independent challenge — One possible solution

```bash
mkdir -p project/{src,docs,logs,backup}
printf 'Project overview\n' > project/docs/README.txt
printf 'Build instructions\n' > project/docs/build.txt
printf 'Sample log entry\n' > project/logs/app.log

find project -type f -name "*.txt"
cp project/docs/*.txt project/backup/
tar -czf project-backup.tar.gz project
tar -tzf project-backup.tar.gz
find project -type f
```

The final `find` verifies that source files still exist. If you repeat this challenge, inspect destination files before copying because an existing file with the same name may be overwritten.

## Reflection — Suggested answers

1. **`cp` vs `mv`:** `cp` makes a copy; `mv` moves a path or renames it.
2. **`mkdir -p`:** Creates missing parent directories and does not complain if the requested directory already exists.
3. **`*` vs `?`:** `*` matches zero or more characters; `?` matches one character in shell filename expansion.
4. **Avoid parsing `ls`:** Filenames can contain spaces, tabs, and newlines, making line-based parsing unreliable. Use `find` and safe delimiters such as `-print0` in scripts.
5. **Symbolic vs hard link:** A symbolic link stores a path and can become broken; a hard link is another name for the same file data on a filesystem.
6. **`du` vs `df`:** `du` estimates space used by selected files/directories; `df` reports usage of mounted filesystems.
7. **Inspect archives:** Archives can contain unexpected paths or files. Listing first helps you understand what will be extracted.
8. **Recursive deletion:** It can remove entire directory trees, so an incorrect path can cause significant data loss.
9. **`chmod 600`:** Owner read/write; no permissions for group or others.
10. **Spaces in filenames:** Quote the path, e.g. `cat "incident summary.txt"`.

## Completion criteria

You have completed this module when you can create and organize a directory tree, copy and rename files, search safely, inspect metadata, use links, archive and restore files, and explain the relevant safety precautions without copying commands blindly.
