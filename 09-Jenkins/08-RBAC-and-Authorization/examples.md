# Jenkins RBAC and Authorization Examples

These examples describe configuration patterns. Perform authorization changes in a test Jenkins instance first. Jenkins authorization is normally configured in the UI or configuration-as-code, not inside an ordinary Jenkinsfile.

## Example 1: Role model for a small team

| Role | Intended access | Avoid granting |
|---|---|---|
| `jenkins-admins` | Controller administration | Shared everyday developer use |
| `app-developers` | Read and run approved application jobs | Controller administration, script console |
| `release-managers` | Run release job and participate in approved release process | Plugin installation or security configuration |
| `auditors` | Read selected job/build information | Configure, delete, or credential management |
| `agent-operators` | Manage assigned agents only where required | Broad job and credential access |

Map these roles to groups from your configured security realm when possible. Keep individual exceptions rare and documented.

## Example 2: Permission planning matrix

This is a planning worksheet, not a copy-paste configuration. Exact permissions and names depend on Jenkins version and installed plugins.

| Capability | Admin | Developer | Release manager | Auditor |
|---|---:|---:|---:|---:|
| Read Jenkins | Yes | Yes | Yes | Yes |
| Read selected jobs | Yes | Yes | Yes | Yes |
| Build approved jobs | Yes | Yes | Yes | No |
| Configure application jobs | Yes | Only if required | No by default | No |
| Delete jobs | Yes | No by default | No | No |
| Manage credentials | Yes | No by default | Only scoped credentials if required | No |
| Configure agents | Yes | No | No | No |
| Administer Jenkins | Yes | No | No | No |

Before applying a matrix, verify which permissions imply others and which global permissions override item-level restrictions.

## Example 3: Role Strategy item-role patterns

Illustrative patterns for a Role Strategy configuration:

```text
Item role: app-team
Pattern: ^team-a/.*$
Permissions: Job/Read, Job/Build, Run/Replay (only if required)

Item role: release-jobs
Pattern: ^release/production-deploy$
Permissions: Job/Read, Job/Build
```

These are example patterns and permission names; verify the exact item names and available permissions in your instance. Test that the pattern matches intended jobs and excludes unrelated jobs. In a folder hierarchy, verify the full item name format used by your Jenkins setup.

## Example 4: Matrix-based authorization planning

A matrix-based strategy grants selected permissions to users or groups. A safe planning process is:

1. Add a known administrator identity with required administrative access.
2. Give developers only read/build permissions required for their jobs.
3. Give auditors read-only access to selected items.
4. Avoid anonymous access unless explicitly intended.
5. Test all grants and denials before ending the administrator session.

Do not blindly copy a permission matrix from another Jenkins installation: installed plugins can add permissions and permission implications can differ.

## Example 5: Configuration as Code concept

Jenkins Configuration as Code can represent some security configuration, but syntax depends on the installed authorization plugin and its version. Treat the following as a conceptual checklist, not a complete valid YAML configuration:

```yaml
# Conceptual only — not a complete Jenkins Configuration as Code file.
# Configure the security realm and authorization strategy together.
# Define explicit admin and team roles.
# Assign roles to groups from the configured identity provider.
# Keep controller administration restricted.
```

Use the official plugin documentation and configuration schema for your installed versions before applying any YAML to a controller.

## Example 6: Access verification test plan

| Test identity | Action | Expected result |
|---|---|---|
| Developer | Read assigned team job | Allowed |
| Developer | Build approved team job | Allowed if granted |
| Developer | Configure controller security | Denied |
| Auditor | Read assigned build records | Allowed |
| Auditor | Delete a job | Denied |
| Release manager | Trigger approved release job | Allowed if granted |
| Anonymous | Read private job | Denied unless explicitly configured otherwise |

Record the actual result, user/group membership, scope, and inherited permissions. A successful login does not prove authorization is correctly configured.

## Example 7: Avoid common mistakes

**Risky configuration choices**
- Giving every authenticated user full control.
- Giving developers `Overall/Administer` for convenience.
- Allowing broad global `Job/Configure` permissions.
- Using an item-role regex that accidentally matches production jobs.
- Forgetting permissions inherited from global or parent-folder scopes.
- Testing only allowed actions, not denied actions.

**Safer approach:** define the desired role, list required actions, grant the smallest permission set, and test with a non-admin account.

## Review checklist
- [ ] Authentication and authorization are configured separately and intentionally.
- [ ] Admin access is limited to a small trusted group.
- [ ] Developers and auditors have different roles.
- [ ] Sensitive release jobs have narrow access.
- [ ] Global and inherited permissions have been reviewed.
- [ ] Item-role patterns are tested against real item names.
- [ ] Denied actions are tested with non-admin accounts.
- [ ] Recovery and change documentation are available.
