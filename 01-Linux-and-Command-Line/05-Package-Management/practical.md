# Linux Package Management — Practical Lab

## Lab Information

**Level:** Beginner to Intermediate

**Objective:** Learn to inspect repositories, query package metadata, install and remove software, inspect package files, and troubleshoot common package-manager issues.

**Environment:** Kali Linux, Ubuntu, or Debian virtual machine.

## Safety Rules

- Use a disposable VM or a snapshot-backed environment.
- Do not remove essential packages.
- Review every proposed package transaction before confirming.
- Do not disable signature verification or install packages from untrusted repositories.
- Never delete package lock files to force an operation.
- Do not run unknown installation scripts as root.

---

## Practical 1: Identify Your Linux Distribution

**Tasks**

1. Display distribution name and version.
2. Display the kernel release.
3. Identify whether the system is Debian-based.
4. Record which package manager is appropriate.

Explore:

```bash
cat /etc/os-release
uname -r
command -v apt
command -v dnf
command -v pacman
```

## Practical 2: Refresh Package Metadata

**Tasks**

1. Run `sudo apt update`.
2. Record which repositories were contacted.
3. Identify any failed downloads, expired metadata, or signature errors.
4. Explain why updating the package index is different from upgrading installed packages.

Do not change repository keys or disable signature checks just to make an error disappear.

## Practical 3: Search and Inspect a Package

Use `curl` as the example package.

**Tasks**

1. Search for the package.
2. Display package metadata.
3. Determine whether it is installed.
4. Find its installed version, if present.
5. Identify its declared dependencies.

Explore:

```bash
apt search curl
apt show curl
dpkg -s curl
apt depends curl
```

Some commands may report that a package is not installed or unavailable. Explain the difference.

## Practical 4: Install and Verify a Test Package

Use `tree` if it is available in your configured repositories.

**Tasks**

1. Refresh package metadata.
2. Inspect the package details.
3. Install the package.
4. Display its version.
5. Identify which package owns its executable path.

Explore:

```bash
apt show tree
sudo apt install tree
tree --version
command -v tree
dpkg -S "$(command -v tree)"
```

If installation is unavailable, document the reason rather than adding an unknown repository.

## Practical 5: Remove and Reinstall a Package

Use only the dedicated test package from Practical 4.

**Tasks**

1. Remove the package.
2. Verify whether it remains installed.
3. Reinstall it.
4. Explain what `remove` and `purge` do differently.
5. If desired, purge the test package after documenting the result.

Explore:

```bash
sudo apt remove tree
dpkg -s tree
sudo apt install tree
```

Review the proposed changes before confirming.

## Practical 6: Inspect Package Files

Choose an installed package such as `bash` or `coreutils`.

**Tasks**

1. Display its package status.
2. List the files recorded for the package.
3. Identify which package owns a known executable path.
4. Explain why a package file list is useful during incident response.

Explore:

```bash
dpkg -s bash
dpkg -L bash
dpkg -S /bin/bash
```

Path ownership results can vary due to symbolic links and merged `/usr` layouts.

## Practical 7: Review Upgrades and Held Packages

**Tasks**

1. List packages that can be upgraded.
2. Display held packages.
3. Identify a package with an available update, if any.
4. Explain why production systems may stage updates rather than applying all upgrades immediately.

Explore:

```bash
apt list --upgradable
apt-mark showhold
apt-mark showmanual
```

Do not create a package hold just to complete this exercise.

## Practical 8: Inspect Dependencies

**Tasks**

1. Display the declared dependencies for `curl`.
2. Display packages that depend on `curl`, according to available metadata.
3. Explain why removing a shared dependency may affect other applications.
4. Distinguish package dependencies from dependencies loaded dynamically at runtime.

Explore:

```bash
apt depends curl
apt rdepends curl
```

## Practical 9: Download and Inspect a Package Archive

**Tasks**

1. Download the `tree` package without installing it.
2. Identify the downloaded `.deb` filename.
3. Display its package metadata.
4. List its archive contents.
5. Delete only the downloaded lab file when finished.

Explore:

```bash
apt download tree
ls -lh ./*.deb
dpkg-deb --info ./tree_*.deb
dpkg-deb --contents ./tree_*.deb
```

The wildcard assumes a matching package archive exists in the current directory. Check the filename before running commands.

## Practical 10: Review Repository Trust

**Tasks**

1. Inspect the configured APT repository files.
2. Identify the distribution's official repositories.
3. Explain what repository signing verifies.
4. Explain why adding an arbitrary repository can introduce supply-chain risk.
5. Describe the purpose of a repository-specific `Signed-By` keyring.

Do not add or remove repositories as part of this exercise.

## Practical 11: Troubleshooting Scenario

A package installation fails with an unmet-dependencies error.

**Tasks**

1. Capture the complete error.
2. Check whether another package-manager process is active.
3. Inspect repository configuration and recent package-index errors.
4. Explain when `dpkg --configure -a` may help.
5. Explain what `apt --fix-broken install` attempts to do.
6. Review all proposed changes before accepting a repair.

Do not remove lock files manually or disable signature checks.

## Practical 12: Compare Package Managers

Research the commands for the distribution you use and complete this table:

| Task | Debian-based | Fedora/RHEL-family | Arch Linux |
|---|---|---|---|
| Search for a package |  |  |  |
| Show package information |  |  |  |
| Install a package |  |  |  |
| Upgrade packages |  |  |  |
| Query installed package files |  |  |  |

## Final Challenge: Secure Software Installation

A developer suggests installing a security tool by downloading an unknown shell script and running it with root privileges.

Write a short assessment that answers:

1. What can go wrong if the script is malicious or compromised?
2. How would you identify the official project source?
3. Why are trusted, signed repositories preferable when available?
4. How can package origin and integrity be reviewed?
5. How would you test the installation in an isolated VM?
6. What evidence would you retain for a reproducible DevSecOps build?

## Submission Checklist

- [ ] Distribution and package manager identified.
- [ ] APT metadata refreshed.
- [ ] Package search and metadata queries completed.
- [ ] A safe test package installed and verified.
- [ ] Package removal and purge behavior explained.
- [ ] DPKG file ownership queried.
- [ ] Dependencies and held packages reviewed.
- [ ] Package archive inspected.
- [ ] Repository trust explained.
- [ ] Troubleshooting and secure-installation assessment completed.

Compare your work against `solution.md`.
