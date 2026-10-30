# Linux Package Management — Examples

This file demonstrates package management commands primarily for Debian-based systems such as Ubuntu, Debian, and Kali Linux.

> **Safety:** Use a lab VM. Review package-manager proposals before confirming. Do not remove core system packages or disable signature verification to bypass errors.

## 1. Identify the Distribution

```bash
cat /etc/os-release
uname -r
```

`/etc/os-release` identifies the distribution and version. `uname -r` displays the running kernel release.

## 2. Refresh APT Package Indexes

```bash
sudo apt update
```

This downloads current repository metadata. It does not install upgrades by itself.

If the command fails, inspect the repository URL, network connectivity, system clock, and signing errors before making configuration changes.

## 3. Upgrade Installed Packages

```bash
sudo apt upgrade
```

Review the list of packages to be upgraded and any prompts before proceeding.

For upgrades that may install or remove packages to resolve dependencies:

```bash
sudo apt full-upgrade
```

On important systems, take a backup or VM snapshot first and review removals carefully.

## 4. Search for and Inspect Packages

```bash
apt search curl
apt show curl
apt list --installed
apt list --upgradable
```

- `apt search` searches available package metadata.
- `apt show` displays package details.
- `apt list --installed` lists installed packages.
- `apt list --upgradable` shows packages with available upgrades.

## 5. Install a Package

Example using `tree`:

```bash
sudo apt update
sudo apt install tree
tree --version
```

`tree` displays directory structures. If it is unavailable in the configured repositories, inspect the distribution and repository setup rather than adding an unknown source automatically.

## 6. Remove and Purge a Package

```bash
sudo apt remove tree
```

To remove the package and its package-managed configuration:

```bash
sudo apt purge tree
```

The purge operation does not necessarily remove every file created by the application or user. Review the transaction before confirming.

## 7. Remove Unneeded Dependencies

```bash
sudo apt autoremove
```

Review the packages proposed for removal. Do not confirm if a required application or system component would be removed.

## 8. Query Installed Packages with DPKG

```bash
dpkg -l
dpkg -s bash
dpkg -L bash
dpkg -S /bin/bash
```

- `dpkg -l` lists package records.
- `dpkg -s` shows package status and metadata.
- `dpkg -L` lists files recorded as installed by a package.
- `dpkg -S` searches installed package records for a path.

On systems using merged `/usr`, paths such as `/bin/bash` may be symlinks or aliases of paths under `/usr/bin`.

## 9. Inspect Package Dependencies

```bash
apt depends curl
apt rdepends curl
```

`apt depends` shows declared dependencies of a package. `apt rdepends` shows reverse dependencies known to APT's metadata; it is not a complete runtime dependency analysis.

## 10. Download a Package Without Installing It

```bash
apt download tree
```

This downloads the package file into the current directory if it is available. Inspect untrusted package files cautiously and use trusted repositories.

To inspect a downloaded `.deb` archive:

```bash
dpkg-deb --info ./tree_*.deb
dpkg-deb --contents ./tree_*.deb
```

Shell wildcard expansion depends on the actual downloaded filename.

## 11. Check Held Packages

```bash
apt-mark showhold
apt-mark showmanual
apt-mark showauto
```

These commands show held packages and packages marked as manually or automatically installed.

Avoid placing important security updates on hold without a documented reason and a plan to revisit the hold.

## 12. Recover from an Interrupted Package Operation

First inspect the package manager's state and error output. If a package configuration was interrupted, a common recovery command is:

```bash
sudo dpkg --configure -a
```

If dependencies remain broken, inspect the proposed repair before running:

```bash
sudo apt --fix-broken install
```

Do not delete package lock files manually. Check whether another package-manager process is active and let it finish when appropriate.

## 13. Inspect Repository Configuration

```bash
grep -R --no-messages -E '^[[:space:]]*deb ' /etc/apt/sources.list /etc/apt/sources.list.d/
```

APT sources can also be configured using deb822 `.sources` files, so the command above will not display every possible configuration format.

Use only repositories trusted for your distribution. Prefer repository-specific keyrings and `Signed-By` configuration instead of trusting an unknown key globally.

## 14. Other Distribution Families

Fedora/RHEL-family systems commonly use DNF:

```bash
dnf search PACKAGE_NAME
dnf info PACKAGE_NAME
sudo dnf install PACKAGE_NAME
sudo dnf upgrade
```

Arch Linux commonly uses Pacman:

```bash
pacman -Ss PACKAGE_NAME
pacman -Si PACKAGE_NAME
sudo pacman -S PACKAGE_NAME
```

These are examples only. Package names, privilege requirements, and repository policies vary by distribution.

## Key Takeaways

- Refresh package indexes before searching for or installing recent versions.
- Read transaction summaries before confirming.
- Prefer signed packages from trusted repositories.
- Understand the difference between package removal and purging.
- Diagnose repository and dependency problems instead of bypassing security checks.
