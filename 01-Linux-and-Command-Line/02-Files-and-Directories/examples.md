# 💡 Files and Directories — Examples

This file contains practical, copyable examples for managing files and directories in Linux. Run examples inside a dedicated lab directory, not against important system files.

## 1. Prepare a workspace

```bash
mkdir -p ~/file-lab/{documents,logs,images,backups}
cd ~/file-lab
pwd
find . -maxdepth 2 -print
```

The brace expression creates several sibling directories in one command in Bash.

## 2. Create files and add content

```bash
touch documents/notes.txt
printf 'Linux file management\n' > documents/notes.txt
printf 'Second line\n' >> documents/notes.txt
cat documents/notes.txt
```

`>` overwrites the destination; `>>` appends. Confirm the target path before using redirection.

## 3. Names with spaces and hidden files

```bash
touch "documents/incident notes.txt"
mkdir "documents/Case Files"
touch .lab-config
ls -la
```

Quote paths containing spaces. A leading dot makes a name hidden from normal `ls` output, not protected.

## 4. Copy, move, and rename

```bash
cp documents/notes.txt backups/notes-copy.txt
cp -i documents/notes.txt backups/notes-copy.txt
mv documents/notes.txt documents/linux-notes.txt
mv "documents/incident notes.txt" "documents/incident-notes.txt"
```

The `-i` option requests confirmation before an overwrite in common GNU implementations.

Copy a directory tree:

```bash
cp -r documents backups/documents-copy
```

For a preservation-oriented copy:

```bash
cp -a documents backups/documents-preserved
```

## 5. Remove files and directories safely

```bash
touch logs/temporary.log
rm -i logs/temporary.log
mkdir empty-dir
rmdir empty-dir
```

For a non-empty practice directory, inspect it first:

```bash
find backups -maxdepth 2 -print
```

Only after verifying that the target is the intended disposable practice directory should you remove it. Avoid practicing recursive deletion on real data.

## 6. List and filter

```bash
ls -lah
ls -lt
find . -type f
find . -type d
find . -type f -name "*.txt"
find . -type f -iname "*.log"
```

The `-iname` predicate matches filename patterns without case sensitivity.

## 7. Find files by size and age

```bash
find . -type f -size +100k
find . -type f -mtime -7
find . -type f -empty
```

`-size +100k` finds files larger than the selected size unit according to `find`'s size rules. `-mtime -7` selects files modified within approximately the last seven 24-hour periods.

## 8. File metadata and disk usage

```bash
file documents/linux-notes.txt
stat documents/linux-notes.txt
du -sh .
du -ah . | sort -h
df -h
```

`du` reports space used by paths; `df` reports usage of mounted filesystems.

## 9. Symbolic and hard links

```bash
ln -s documents/linux-notes.txt notes-shortcut
readlink notes-shortcut
ls -li documents/linux-notes.txt
ln documents/linux-notes.txt notes-hardlink
ls -li documents/linux-notes.txt notes-hardlink
```

The symbolic link stores a path reference. The hard link is another directory entry for the same underlying file data. Hard links have filesystem and permission constraints.

## 10. Create and inspect an archive

```bash
tar -czf backups/file-lab.tar.gz documents logs images
tar -tzf backups/file-lab.tar.gz
mkdir -p restore-check
tar -xzf backups/file-lab.tar.gz -C restore-check
find restore-check -maxdepth 3 -print
```

Inspect archives from untrusted sources before extraction. This example extracts into a separate workspace directory.

## 11. Permission examples

```bash
touch documents/private.txt
chmod 600 documents/private.txt
stat documents/private.txt
```

Mode `600` gives read/write access to the owner and no permission to group or others, subject to ownership and filesystem behavior.

## 12. Wildcards

```bash
printf 'one\n' > a.txt
printf 'two\n' > b.txt
printf 'log\n' > app.log
ls *.txt
ls ?.txt
```

- `*` matches zero or more characters.
- `?` matches one character.
- `[abc]` matches one character from the listed set.

Check what a wildcard matches before using it with a command that changes or deletes files.

## 13. Robust handling of unusual filenames

Prefer quoting variables in scripts:

```bash
filename="documents/incident notes.txt"
printf '%s\n' "$filename"
test -f "$filename" && echo "File exists"
```

When processing arbitrary filenames with `find`, use null delimiters instead of newline-based parsing:

```bash
find . -type f -print0
```

Do not parse `ls` output in scripts; filenames can contain spaces, tabs, and newlines.

## 14. Troubleshooting checklist

- `No such file or directory`: check `pwd`, spelling, and parent directories.
- `Permission denied`: inspect directory traversal permissions and file ownership; do not immediately use `sudo`.
- `File exists`: inspect the destination before overwriting.
- `Directory not empty`: use `rmdir` only for empty directories; review contents before any recursive removal.
- Unexpected wildcard matches: quote patterns when you intend to pass them literally to a command, and inspect expansions before destructive operations.

## Suggested practice

Repeat each example, explain the command options in your own words, and verify the result with `ls -la`, `stat`, or `find`.
