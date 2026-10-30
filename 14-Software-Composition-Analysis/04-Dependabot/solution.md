# Solutions and Instructor Guidance

## Lab 1
A good inventory lists ecosystem, manifest location, lockfile, and whether GitHub recognizes the dependencies. Detection depends on supported manifest formats and repository configuration.

## Lab 2
The configuration must be on the default branch under `.github/`. The ecosystem identifier must match GitHub's supported list, and the directory must contain the relevant manifest. A weekly schedule is a reasonable starting point for many repositories, but cadence should reflect release velocity and risk.

## Lab 3
Do not add ecosystems just because they appear in an example. Each entry should map to a real manifest directory. For monorepos, consider `directories` and verify each path.

## Lab 4
Security updates depend on repository settings, dependency graph/alert availability, supported ecosystems, and an available safe update. A good review validates the advisory, package version, fixed release, test results, and transitive changes.

## Lab 5
Groups reduce PR count but increase the size of each change. Use separate groups for development and production dependencies where appropriate. Cooldown is for version updates; security updates are not delayed by cooldown.

## Lab 6
Use a least-privilege test token, store it in GitHub secrets, and ensure logs do not print it. Verify private registry access works only for the intended package scope. Revoke credentials after testing.

## Lab 7
A complete review records old/new versions, changelog, advisory context, lockfile changes, CI status, compatibility risk, reviewer, and decision. Major updates normally need deeper compatibility testing.

## Common troubleshooting
- Check `.github/dependabot.yml` spelling and default-branch placement.
- Check YAML indentation and valid ecosystem identifiers.
- Verify manifest directory paths.
- Check repository settings for alerts and security updates.
- Check registry type, secret names, and token permissions.
- Inspect open PR limits and group matching order.

## Assessment rubric
- Correct configuration and ecosystem selection: 25%
- Security-update understanding: 20%
- Grouping, ignore, and cooldown: 15%
- Private registry security: 15%
- PR review and validation: 20%
- Documentation: 5%
