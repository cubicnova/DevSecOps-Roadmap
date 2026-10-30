# 🧪 Files and Directories — Practical Labs

**Level:** Beginner  
**Environment:** Linux VM, WSL, or another authorized Linux system  
**Estimated time:** 60–90 minutes

## Lab safety rules

1. Work only in `~/file-lab-practical`.
2. Do not use important personal or system files for practice.
3. Read commands before executing them.
4. Inspect paths before using overwrite or deletion commands.
5. Do not use `sudo` unless a lab specifically requires it.
6. If a command behaves differently on your distribution, check `man COMMAND`.

## Setup

Run:

```bash
mkdir -p ~/file-lab-practical
cd ~/file-lab-practical
pwd
```

Confirm that the printed path ends with `file-lab-practical`.

---

## Lab 1 — Create a directory structure

**Tasks**

1. Create directories named `documents`, `logs`, `images`, and `backups`.
2. Under `documents`, create `reports` and `notes`.
3. List the structure, including directories.

**Hints:** `mkdir -p`, `find`, `ls -la`

**Expected structure**

```text
file-lab-practical/
├── backups/
├── documents/
│   ├── notes/
│   └── reports/
├── images/
└── logs/
```

## Lab 2 — Create and inspect files

**Tasks**

1. Create `readme.txt` inside `documents/notes`.
2. Add two lines of sample text.
3. Create an empty `application.log` inside `logs`.
4. Display file type, size, and metadata for both files.

**Hints:** `touch`, `printf`, `file`, `stat`, `cat`

## Lab 3 — Copy, rename, and move

**Tasks**

1. Copy `readme.txt` to `backups/readme-backup.txt`.
2. Rename the original file to `linux-notes.txt`.
3. Move the backup into `documents/reports`.
4. Verify that both files exist at the correct paths.

**Hints:** `cp`, `mv`, `ls -l`

## Lab 4 — Handle spaces and hidden files

**Tasks**

1. Create a directory named `Case Notes`.
2. Create a file named `incident summary.txt` in it.
3. Create a hidden file named `.lab-settings`.
4. Show the hidden file in a directory listing.

**Hints:** Quote paths containing spaces; use `ls -la`.

## Lab 5 — Search for files

Create these sample files:

```bash
touch logs/app.log logs/security.log documents/reports/weekly.txt
```

**Tasks**

1. Find all regular files under the workspace.
2. Find files ending in `.log`.
3. Find `.TXT` and `.txt` files without case sensitivity.
4. Find empty files.
5. Find directories only.

**Hints:** `find`, `-type`, `-name`, `-iname`, `-empty`

## Lab 6 — Inspect disk usage and metadata

**Tasks**

1. Display metadata for `logs/app.log`.
2. Show the total workspace size.
3. Show the size of each first-level directory.
4. Display filesystem free space.

**Hints:** `stat`, `du -sh`, `du -h --max-depth=1`, `df -h`

## Lab 7 — Links

**Tasks**

1. Create a symbolic link to `documents/notes/linux-notes.txt`.
2. Display the link target.
3. Compare the link and target using `ls -l`.
4. If supported, create a hard link and compare inode numbers using `ls -li`.

**Hints:** `ln -s`, `ln`, `readlink`, `ls -li`

**Reflection:** What happens to a symbolic link if its target is renamed? How is a hard link different?

## Lab 8 — Archive and restore

**Tasks**

1. Create a compressed archive of `documents` and `logs`.
2. List the archive contents without extracting.
3. Extract the archive into `restore-check`.
4. Verify that the restored files exist.

**Hints:** `tar -czf`, `tar -tzf`, `tar -xzf`, `find`

## Lab 9 — Permissions

**Tasks**

1. Create `documents/private.txt`.
2. Set its permissions to `600`.
3. Verify the permissions.
4. Explain why private files should not be made world-readable without a reason.

**Hints:** `chmod`, `stat`, `ls -l`

## Lab 10 — Safe cleanup

**Tasks**

1. List the workspace contents.
2. Identify temporary files you created.
3. Remove one temporary file using interactive mode.
4. Remove an empty directory with `rmdir`.
5. Leave the main workspace intact for review.

**Hints:** `find`, `ls -la`, `rm -i`, `rmdir`

Do not use `rm -rf` as a shortcut for this exercise.

---

## Independent challenge

Write a short command sequence that:

1. Creates `project/{src,docs,logs,backup}` under your practice directory.
2. Creates two `.txt` files and one `.log` file.
3. Finds all `.txt` files.
4. Copies the documentation files into `backup`.
5. Archives `project` into `project-backup.tar.gz`.
6. Lists the archive contents.
7. Confirms the source files remain present.

## Submission checklist

- [ ] All labs completed inside the practice directory.
- [ ] Directory structure matches the requested layout.
- [ ] Copy/move operations verified.
- [ ] Search commands return expected files.
- [ ] Metadata and disk usage inspected.
- [ ] Links created and understood.
- [ ] Archive listed and restored successfully.
- [ ] Permissions verified.
- [ ] Cleanup performed without deleting the main workspace.

## Reflection questions

1. What is the difference between `cp` and `mv`?
2. Why is `mkdir -p` useful?
3. How do `*` and `?` differ?
4. Why should scripts avoid parsing `ls` output?
5. What is the difference between a symbolic link and a hard link?
6. What is the difference between `du` and `df`?
7. Why should archive contents be inspected before extraction?
8. Why is recursive deletion risky?
9. What does `chmod 600` mean?
10. How can you safely handle filenames containing spaces?
