# 📁 Files and Directories

[![Linux](https://img.shields.io/badge/Linux-Command_Line-FCC624?logo=linux&logoColor=black)](https://www.kernel.org/)
[![Level](https://img.shields.io/badge/Level-Beginner-success)](.)
[![Roadmap](https://img.shields.io/badge/Path-DevSecOps-blue)](../../README.md)

Welcome to **Files and Directories**, the second module in the Linux and Command Line section of the **CubicNova DevSecOps Roadmap**. Learn how to create, inspect, organize, copy, move, search, link, archive, and safely remove files and directories in Linux.

These skills are foundational for system administration, shell scripting, incident response, log analysis, secure configuration, and DevSecOps automation.

## 📚 Table of Contents

- [Learning Objectives](#-learning-objectives)
- [Prerequisites](#-prerequisites)
- [Topics Covered](#-topics-covered)
- [Command Quick Reference](#-command-quick-reference)
- [Paths and Hidden Files](#-paths-and-hidden-files)
- [Create and Inspect](#-create-and-inspect)
- [Copy, Move, and Rename](#-copy-move-and-rename)
- [Search for Files](#-search-for-files)
- [Links](#-links)
- [Metadata and Disk Usage](#-metadata-and-disk-usage)
- [Archives](#-archives)
- [Permissions and Safe File Handling](#-permissions-and-safe-file-handling)
- [Hands-On Practice](#-hands-on-practice)
- [Mini Project](#-mini-project)
- [Files in This Module](#-files-in-this-module)
- [Learning Resources](#-learning-resources)
- [Next Steps](#-next-steps)

## 🎯 Learning Objectives

By the end of this module, you should be able to:

1. Explain absolute and relative paths.
2. Create nested directories and files.
3. List normal and hidden files with useful metadata.
4. Copy, move, rename, and remove files and directories.
5. Find files by name, type, size, and modification time.
6. Understand wildcard patterns and quoted paths.
7. Explain symbolic links and hard links at a beginner level.
8. Inspect file metadata and directory disk usage.
9. Create and extract common archives.
10. Apply safe file-handling practices suitable for DevSecOps work.

## 🧰 Prerequisites

- A Linux terminal, Linux VM, WSL distribution, or another authorized Linux environment.
- Completion of [01-Linux-Fundamentals](../01-Linux-Fundamentals/README.md) is recommended.
- Basic familiarity with `pwd`, `ls`, `cd`, and `sudo`.

All exercises should be completed in a practice directory, not on important system files.

## 📖 Topics Covered

| Topic | Commands / Concepts |
|---|---|
| Paths | Absolute paths, relative paths, `.`, `..`, `~` |
| Listing | `ls`, `ls -la`, `file`, `stat` |
| Creating | `touch`, `mkdir`, `mkdir -p` |
| Copying | `cp`, `cp -r`, `cp -a` |
| Moving and renaming | `mv`, `mv -i` |
| Removing | `rm`, `rm -i`, `rmdir` |
| Searching | `find`, `locate` (if installed) |
| Wildcards | `*`, `?`, `[abc]` |
| Links | `ln`, `ln -s`, `readlink` |
| Disk usage | `du`, `df` |
| Archives | `tar`, `gzip`, `zip` (if installed) |
| Safe handling | Quoting, backups, least privilege, cautious deletion |

## 🧭 Command Quick Reference

| Task | Command | Example |
|---|---|---|
| Show current directory | `pwd` | `pwd` |
| List files, including hidden | `ls -la` | `ls -la ~/Documents` |
| Create a file | `touch` | `touch notes.txt` |
| Create nested directories | `mkdir -p` | `mkdir -p lab/docs/drafts` |
| Copy a file | `cp` | `cp notes.txt notes-copy.txt` |
| Copy a directory tree | `cp -r` | `cp -r project project-backup` |
| Move / rename | `mv` | `mv old.txt new.txt` |
| Remove a file | `rm -i` | `rm -i old.txt` |
| Remove an empty directory | `rmdir` | `rmdir empty-dir` |
| Find by name | `find` | `find . -name "*.log"` |
| Show metadata | `stat` | `stat notes.txt` |
| Show directory size | `du -sh` | `du -sh ~/Downloads` |
| Create a tar archive | `tar` | `tar -czf backup.tar.gz project/` |
| Extract a tar archive | `tar` | `tar -xzf backup.tar.gz` |

## 🗺️ Paths and Hidden Files

- An **absolute path** starts at `/`, such as `/home/alex/projects`.
- A **relative path** is interpreted from the current working directory, such as `projects/app`.
- `.` refers to the current directory; `..` refers to its parent; `~` usually expands to the current user's home directory.
- Filenames beginning with `.` are hidden from ordinary `ls` output, but they are not inherently more secure.

```bash
pwd
ls
ls -la
cd ..
cd ~
```

Use quotes around names containing spaces or shell-special characters:

```bash
mkdir "incident response"
touch "incident response/notes for review.txt"
ls -l "incident response"
```

## ✨ Create and Inspect

```bash
mkdir -p ~/file-lab/{documents,logs,backups}
touch ~/file-lab/documents/notes.txt
printf 'Practice file handling\n' > ~/file-lab/documents/notes.txt
ls -lah ~/file-lab
file ~/file-lab/documents/notes.txt
stat ~/file-lab/documents/notes.txt
```

`touch` creates an empty file if it does not exist and updates timestamps if it does. `printf` writes predictable text; redirection with `>` overwrites a file, so use it carefully.

## 📦 Copy, Move, and Rename

```bash
cp notes.txt notes-copy.txt
cp -i notes.txt existing-file.txt
cp -r project/ project-copy/
mv notes-copy.txt archive-notes.txt
mv -i archive-notes.txt backups/
```

- `cp` copies files; `cp -r` copies directories recursively.
- `mv` moves or renames a path.
- `-i` asks before overwriting in common GNU implementations.
- `cp -a` is useful when preserving attributes is important, subject to permissions and filesystem support.

Always verify source and destination paths before a bulk operation.

## 🔎 Search for Files

```bash
find ~/file-lab -type f
find ~/file-lab -type d
find ~/file-lab -type f -name "*.txt"
find ~/file-lab -type f -iname "*.log"
find ~/file-lab -type f -size +1M
find ~/file-lab -type f -mtime -7
```

Common `find` predicates:

- `-type f`: regular files.
- `-type d`: directories.
- `-name`: case-sensitive name pattern.
- `-iname`: case-insensitive name pattern.
- `-size +1M`: larger than the specified size threshold.
- `-mtime -7`: modified within the last seven 24-hour periods, approximately.

To see matching files before acting, run `find` alone first. Avoid combining broad searches with destructive actions.

## 🔗 Links

A symbolic link points to a path:

```bash
ln -s notes.txt notes-link.txt
readlink notes-link.txt
ls -l notes-link.txt
```

A hard link is another directory entry for the same underlying file data, subject to filesystem restrictions:

```bash
ln notes.txt notes-hardlink.txt
ls -li notes.txt notes-hardlink.txt
```

A symbolic link can point to a directory or a path that does not currently exist. Hard links generally cannot cross filesystem boundaries and are not normally created for directories.

## 📊 Metadata and Disk Usage

```bash
stat notes.txt
du -sh ~/file-lab
du -ah ~/file-lab | sort -h
df -h
```

- `stat` shows file metadata such as size, ownership, permissions, and timestamps.
- `du` estimates space used by files and directories.
- `df` reports filesystem space usage.

## 🗜️ Archives

Create and inspect a compressed tar archive:

```bash
tar -czf file-lab-backup.tar.gz ~/file-lab
tar -tzf file-lab-backup.tar.gz
mkdir -p ~/restore-test
tar -xzf file-lab-backup.tar.gz -C ~/restore-test
```

Check archive contents before extraction, especially when the archive comes from an untrusted source. Extract into a dedicated directory rather than a sensitive system location.

## 🔐 Permissions and Safe File Handling

```bash
chmod 600 ~/file-lab/documents/notes.txt
ls -l ~/file-lab/documents/notes.txt
```

Key practices:

- Follow least privilege; do not use `chmod 777` as a general fix.
- Avoid `sudo` for routine file operations unless necessary.
- Review a target before using `rm -r` or wildcard patterns.
- Prefer interactive options such as `rm -i` and `mv -i` when learning.
- Back up important files before modifying them.
- Quote paths containing spaces: `"file name.txt"`.
- Treat archives, logs, and backups as potentially sensitive.
- Do not assume deleting a file securely erases it from storage.

## 🧪 Hands-On Practice

1. Create a `~/file-lab` workspace with `documents`, `logs`, and `backups` subdirectories.
2. Create three text files and add sample content.
3. List all files, including hidden files.
4. Copy one file into the backup directory.
5. Rename another file and move it into `documents`.
6. Find every `.txt` file under the workspace.
7. Create a symbolic link and inspect it.
8. Display the workspace's disk usage.
9. Create a compressed tar archive.
10. Extract the archive into a separate test directory and verify the contents.

See [`practical.md`](practical.md) for the full lab worksheet and [`solutions.md`](solutions.md) for suggested solutions.

## 🚀 Mini Project: File Organizer and Backup

Create a practice workspace containing `documents/`, `logs/`, `images/`, and `backups/`. Add sample files, organize them by type, and create a timestamped archive. Verify the archive listing and extract it into a temporary restore directory.

**Acceptance criteria**

- No files outside your practice workspace are changed.
- Files are organized into the expected directories.
- The archive can be listed and extracted.
- The original files remain intact.
- You can explain the purpose of every command used.

Optional: automate the process with a Bash script after you understand each command individually.

## 📂 Files in This Module

| File | Purpose |
|---|---|
| `README.md` | Concepts, command reference, and module overview |
| `examples.md` | Copyable command examples with explanations |
| `practical.md` | Guided labs and independent exercises |
| `solutions.md` | Suggested answers and verification commands |

## 📚 Learning Resources

- [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/coreutils.html) — listing, copying, moving, removing, and metadata commands.
- [GNU Findutils Manual](https://www.gnu.org/software/findutils/manual/) — `find` and related utilities.
- [GNU tar Manual](https://www.gnu.org/software/tar/manual/) — archive creation and extraction.
- [Linux man-pages](https://www.kernel.org/doc/man-pages/) — Linux command and system-interface documentation.

## 🗺️ Next Steps

Continue to the next module in the [Linux and Command Line](../README.md) section of the [CubicNova DevSecOps Roadmap](../../README.md).

**Learn Linux. Automate intelligently. Build securely.**
