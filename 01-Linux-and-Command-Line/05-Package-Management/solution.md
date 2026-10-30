# Linux Package Management — Solutions

These are reference solutions for the tasks in `practical.md`. Examples primarily target Ubuntu, Debian, and Kali Linux.

> Use a lab VM. Package availability and output vary by distribution, version, and configured repositories.

## Solution 1: Identify Your Linux Distribution

```bash
cat /etc/os-release
uname -r
command -v apt
command -v dnf
command -v pacman
```

`/etc/os-release` identifies the distribution. `uname -r` displays the running kernel version. Use the package manager supported by the distribution; the presence of a command alone does not mean it is the preferred manager.

## Solution 2: Refresh Package Metadata

```bash
sudo apt update
```

This refreshes local package indexes from configured repositories. It does not itself upgrade installed packages.

If it fails, inspect the full error, repository URLs, connectivity, system time, and signing metadata. Do not disable signature verification or blindly import an unknown key.

## Solution 3: Search and Inspect a Package

```bash
apt search curl
apt show curl
dpkg -s curl
apt depends curl
```

- `apt search` searches package metadata.
- `apt show` displays package information for an available package.
- `dpkg -s` reports installed-package status; it may report that the package is not installed.
- `apt depends` shows declared package dependencies.

A package can be available in a repository without being installed locally.

## Solution 4: Install and Verify a Test Package

```bash
sudo apt update
apt show tree
sudo apt install tree
tree --version
command -v tree
dpkg -S "$(command -v tree)"
```

Review the proposed transaction before confirming. The final command identifies the installed package that owns the executable path when that path is recorded by DPKG.

If `tree` is unavailable, document the repository issue rather than adding an unknown source.

## Solution 5: Remove and Reinstall a Package

```bash
sudo apt remove tree
dpkg -s tree
sudo apt install tree
```

`remove` removes the program package but generally retains package-managed configuration files. `purge` also removes package-managed configuration. Neither operation necessarily removes every user-created file.

If purging the test package:

```bash
sudo apt purge tree
```

Review the proposed transaction before confirming.

## Solution 6: Inspect Package Files

```bash
dpkg -s bash
dpkg -L bash
dpkg -S /bin/bash
```

- `dpkg -s` displays package status and metadata.
- `dpkg -L` lists files recorded as installed by a package.
- `dpkg -S` searches installed package records for a path.

On systems with merged `/usr`, `/bin/bash` may resolve through a symlink to `/usr/bin/bash`. Check the actual path and ownership result on your system.

## Solution 7: Review Upgrades and Held Packages

```bash
sudo apt update
apt list --upgradable
apt-mark showhold
apt-mark showmanual
```

`apt list --upgradable` lists packages with available upgrades based on current metadata. `apt-mark showhold` identifies packages held back from automatic upgrades. `apt-mark showmanual` lists packages marked as manually installed.

For production systems, use staged updates, backups, and validation where appropriate.

## Solution 8: Inspect Dependencies

```bash
apt depends curl
apt rdepends curl
```

`apt depends` shows declared dependencies of `curl`. `apt rdepends` shows reverse dependencies known to APT's metadata; it is not a complete analysis of every runtime relationship.

A package can be required by other installed software, so review proposed removals carefully.

## Solution 9: Download and Inspect a Package Archive

```bash
apt download tree
ls -lh ./*.deb
```

Identify the actual downloaded filename, then use that exact path:

```bash
dpkg-deb --info ./ACTUAL_PACKAGE_FILENAME.deb
dpkg-deb --contents ./ACTUAL_PACKAGE_FILENAME.deb
```

Replace the example filename with the one shown by `ls`. Do not run these commands on an assumed filename that does not exist.

When finished, remove only the downloaded lab archive after verifying its path.

## Solution 10: Review Repository Trust

Inspect common traditional APT source entries:

```bash
cat /etc/apt/sources.list
ls -la /etc/apt/sources.list.d/
```

Some systems use deb822 `.sources` files rather than traditional `deb` lines.

Repository signing allows APT to validate signed repository metadata against configured trusted keys. A repository-specific `Signed-By` keyring limits which key is trusted for that source. An unknown repository can distribute altered or malicious software, even if its packages install successfully.

Use official distribution documentation to verify repository configuration.

## Solution 11: Troubleshooting Scenario

Start with read-only checks:

```bash
ps aux | grep -E '[a]pt|[d]pkg'
sudo apt update
dpkg --audit
```

If a package configuration was interrupted, a common recovery command is:

```bash
sudo dpkg --configure -a
```

If dependency problems remain, inspect the proposed changes before running:

```bash
sudo apt --fix-broken install
```

The repair operation may install, upgrade, or remove packages to resolve dependency issues. Review its plan before confirming.

Never delete lock files manually. First determine whether another package operation is active and let it complete when appropriate.

## Solution 12: Compare Package Managers

Typical commands:

| Task | Debian-based | Fedora/RHEL-family | Arch Linux |
|---|---|---|---|
| Search | `apt search NAME` | `dnf search NAME` | `pacman -Ss NAME` |
| Package information | `apt show NAME` | `dnf info NAME` | `pacman -Si NAME` |
| Install | `sudo apt install NAME` | `sudo dnf install NAME` | `sudo pacman -S NAME` |
| Upgrade packages | `sudo apt upgrade` | `sudo dnf upgrade` | `sudo pacman -Syu` |
| Query package files | `dpkg -L NAME` | `rpm -ql NAME` | `pacman -Ql NAME` |

Commands and privilege requirements may vary. On Arch Linux, full system upgrades are generally preferred over partial upgrades.

## Solution 13: Secure Software Installation

Running an unknown script with root privileges can let an attacker alter system files, install persistence, steal credentials, or compromise the build environment.

A safer workflow is:

1. Verify the official project and maintainer source.
2. Prefer the distribution's trusted, signed repository when suitable.
3. Review release notes, provenance, signatures, and checksums where provided.
4. Inspect the installer's contents before execution.
5. Test in an isolated VM or disposable container.
6. Record package names, versions, repository origins, and build steps.
7. Keep secrets out of logs and source control.
8. Review required privileges and minimize them.

A checksum obtained from the same compromised source is not, by itself, proof of authenticity.

## Final Review

You should now be able to:

- Explain repositories, package indexes, and dependencies.
- Search for, install, inspect, upgrade, and remove packages.
- Query package contents and ownership.
- Distinguish `apt update` from `apt upgrade`.
- Explain repository signing and supply-chain risk.
- Troubleshoot package operations without bypassing security controls.

## References

- [APT User's Guide](https://www.debian.org/doc/manuals/apt-guide/)
- [APT Manual](https://manpages.debian.org/apt/apt.8.en.html)
- [DPKG Manual](https://manpages.debian.org/dpkg/dpkg.1.en.html)
- [Debian Sources List](https://wiki.debian.org/SourcesList)
- [Fedora DNF Documentation](https://docs.fedoraproject.org/en-US/quick-docs/dnf/)
