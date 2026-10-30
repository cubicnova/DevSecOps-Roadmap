# Linux System Hardening — Examples

These examples focus on safe auditing and controlled changes for Linux systems. Commands may differ by distribution.

> **Important:** Use a VM or staging host. Do not apply firewall or SSH changes to a remote production host without tested access and rollback.

## 1. Identify the Operating System and Kernel

```bash
cat /etc/os-release
uname -a
uname -r
```

Record the distribution, version, and running kernel before choosing hardening guidance.

## 2. Inspect Running Services

```bash
systemctl --type=service --state=running
systemctl list-unit-files --type=service
```

Review services against the workload's requirements. Do not disable a service simply because its purpose is unfamiliar.

Inspect a specific service:

```bash
systemctl status ssh
systemctl cat ssh
```

The SSH service name can differ across distributions (for example, `sshd`).

## 3. Inspect Listening Network Sockets

```bash
sudo ss -tulpn
```

This shows listening TCP/UDP sockets and, where permissions allow, the associated process. Confirm whether each listener is required and whether network filtering restricts access appropriately.

## 4. Review Accounts and Privileged Access

```bash
getent passwd
getent group sudo
sudo -l
```

On some distributions the administrative group may be `wheel` rather than `sudo`. Review membership according to your system's policy.

Inspect one account:

```bash
id username
passwd -S username
```

Replace `username` with an actual account. Do not assume a locked password means all login methods are disabled.

## 5. Review Installed Packages and Updates

Debian-based systems:

```bash
apt list --upgradable
dpkg -l
```

Fedora/RHEL-family systems:

```bash
dnf check-update
rpm -qa
```

Package inventories can be large. Use them to identify unnecessary or unsupported software, and test removals before implementation.

## 6. Review SSH Configuration

Inspect effective settings where supported:

```bash
sudo sshd -t
sudo sshd -T | grep -E 'permitrootlogin|passwordauthentication|pubkeyauthentication'
```

`sshd -t` validates configuration syntax. `sshd -T` prints effective configuration; includes, match blocks, and platform details can affect interpretation.

Before changing SSH:
1. Confirm key-based access works in a separate session.
2. Ensure console or out-of-band recovery is available.
3. Back up the configuration.
4. Validate with `sshd -t`.
5. Reload or restart only after validation.
6. Keep the existing session open until a new login is confirmed.

Never disable password authentication until the alternative access method is tested.

## 7. Inspect UFW Firewall Status

On systems using UFW:

```bash
sudo ufw status verbose
sudo ufw app list
```

For a disposable VM, a sample policy might allow SSH before enabling the firewall:

```bash
sudo ufw allow OpenSSH
sudo ufw status numbered
```

Only enable UFW after confirming the correct management port and reviewing the rules. Enabling or changing a firewall remotely can block your access. UFW may not be installed or used on all distributions.

## 8. Audit World-Writable Files

Limit the search to a chosen lab directory:

```bash
mkdir -p ~/hardening-lab
touch ~/hardening-lab/example.txt
chmod 666 ~/hardening-lab/example.txt

find ~/hardening-lab -xdev -type f -perm -0002 -print
```

Investigate each finding. World-writable files may be intentional in some contexts, but should be justified and controlled.

## 9. Inspect File and Directory Permissions

```bash
stat -c '%A %a %U %G %n' ~/hardening-lab/example.txt
namei -l ~/hardening-lab/example.txt
```

`namei -l` helps review permissions on the path components leading to a file.

## 10. Review Logs

```bash
sudo journalctl -p warning..alert --since "24 hours ago"
sudo journalctl -u ssh --since "24 hours ago"
```

The service unit may be called `sshd` on your distribution. Review authentication logs using the logging system available on the host. Avoid sharing logs without removing sensitive information.

## 11. Inspect AppArmor and SELinux

AppArmor systems:

```bash
command -v aa-status && sudo aa-status
```

SELinux systems:

```bash
command -v getenforce && getenforce
```

Availability and default enforcement differ by distribution. Do not disable mandatory access control to work around an application issue without investigating the policy.

## 12. Inspect Kernel Parameters

```bash
sysctl kernel.randomize_va_space
sysctl net.ipv4.ip_forward
```

These are examples of kernel parameters, not a universal checklist. Whether IP forwarding should be enabled depends on the host's role. Review workload requirements before changing any `sysctl` value.

To inspect a configuration file:

```bash
grep -R --line-number --no-messages 'net.ipv4.ip_forward' /etc/sysctl.conf /etc/sysctl.d/
```

## 13. Review Systemd Service Hardening Options

Inspect a service's current configuration:

```bash
systemctl cat example.service
systemctl show example.service -p User -p Group -p NoNewPrivileges -p PrivateTmp -p ProtectSystem
```

Replace `example.service` with a real service. These properties are not supported or suitable for every workload. Test any override in a staging environment.

## 14. Baseline and Record Evidence

```bash
mkdir -p ~/hardening-lab/baseline
cat /etc/os-release > ~/hardening-lab/baseline/os-release.txt
uname -a > ~/hardening-lab/baseline/kernel.txt
sudo ss -tulpn > ~/hardening-lab/baseline/listeners.txt
systemctl --type=service --state=running > ~/hardening-lab/baseline/running-services.txt
```

The listener output may include sensitive network details. Store the baseline securely and review it before sharing.

## Cleanup

Remove only the dedicated lab files created for these exercises:

```bash
rm -rf ~/hardening-lab
```

Do not use this command if the directory contains data you want to keep.

## Key Takeaways

- Audit before changing system settings.
- Reduce unnecessary services and privileges.
- Protect SSH and firewall access with a recovery plan.
- Monitor logs and verify hardening controls.
- Tailor benchmarks to the workload rather than applying them blindly.
