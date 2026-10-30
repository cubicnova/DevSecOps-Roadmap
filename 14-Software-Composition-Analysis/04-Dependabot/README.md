# 04 – Dependabot

## Learning objectives
- Explain Dependabot alerts, security updates, and version updates.
- Configure `.github/dependabot.yml` for supported package ecosystems.
- Understand schedules, directories, groups, ignore rules, cooldowns, and registries.
- Review Dependabot pull requests and validate dependency changes.
- Secure CI workflows and private registry credentials.
- Triage alerts and document exceptions.

## 1. What is Dependabot?
Dependabot is GitHub's dependency automation feature. It helps keep dependencies current and highlights known vulnerable dependencies. Its key capabilities are related but distinct:

| Capability | Purpose |
|---|---|
| Dependency graph | Builds an inventory of dependencies recognized by GitHub |
| Dependabot alerts | Notifies about known vulnerabilities in dependencies |
| Security updates | Opens pull requests to update vulnerable dependencies when a suitable fix is available |
| Version updates | Opens scheduled pull requests to keep dependencies current |
| Dependabot configuration | Controls ecosystems, directories, schedules, grouping, and update behavior |

Alerts and security updates are not the same as scheduled version updates. Security updates are driven by vulnerability information; version updates follow the configured schedule.

## 2. Configuration file
The configuration file must be located at `.github/dependabot.yml` or `.github/dependabot.yaml` on the repository's default branch. The file uses YAML and starts with `version: 2`.

A package ecosystem entry generally specifies:
- `package-ecosystem`: package manager / ecosystem identifier;
- `directory` or `directories`: location(s) containing manifest files;
- `schedule.interval`: `daily`, `weekly`, or `monthly`;
- optional labels, reviewers, assignees, groups, ignore rules, registry access, and PR limits.

The directory points to manifest files, not the location where build output happens to be stored. Consult the official ecosystem list for exact supported values.

## 3. Example configuration
See `.github/dependabot.yml`. It demonstrates npm, pip, Maven, Docker, and GitHub Actions. Adapt entries to ecosystems and manifest locations that actually exist in your repository; remove unused entries.

## 4. Security updates versus version updates
- **Security updates:** Dependabot attempts to update dependencies affected by known vulnerabilities when a suitable update is available and repository settings permit it.
- **Version updates:** Dependabot checks according to `schedule.interval` and creates pull requests for newer versions.
- A `dependabot.yml` file configures version-update behavior and can customize security-update pull requests.
- Enabling Dependabot alerts/security updates is also managed through repository or organization settings.
- Grouped security updates require the dependency graph, alerts, and security updates to be enabled.

Do not assume that adding a YAML file alone enables every security feature. Verify repository settings and permissions.

## 5. Grouping, ignore rules, and cooldown
- `groups` combines matching updates into fewer pull requests. Rules are evaluated in order; a dependency matching an earlier group is assigned there.
- `ignore` excludes specified dependencies or update types. Use it sparingly and document why an update is excluded.
- `open-pull-requests-limit` controls the number of open version-update PRs for an ecosystem.
- `cooldown` delays version updates for a specified period. It does **not** delay security updates. Current documentation describes a default three-day cooldown for version updates; confirm current behavior in the options reference.

Grouping reduces noise but can make a PR larger and harder to review. Separate production, development, and high-risk infrastructure dependencies where that improves review quality.

## 6. Private registries and credentials
Private registry definitions belong under `registries`. Use the registry type and URL required by the ecosystem. Reference credentials through GitHub Actions/repository secrets using the supported Dependabot syntax, and grant only the required access.

Never commit tokens, passwords, or personal access tokens in the YAML file. Rotate exposed credentials and review access scopes.

## 7. Reviewing Dependabot pull requests
For each update:
1. Read the package name, old/new versions, and changelog/release notes.
2. Check the advisory and affected version range if security-related.
3. Review lockfile and manifest changes.
4. Run unit, integration, security, and compatibility tests.
5. Inspect transitive dependency changes and license implications.
6. Confirm CI passes and the update is appropriate for the target branch.
7. Merge through the repository's normal review process.

Do not automatically merge every update without an appropriate testing and risk policy. Major version updates deserve particular compatibility review.

## 8. Troubleshooting
| Symptom | Checks |
|---|---|
| No update PRs | Default-branch config path, YAML syntax, manifest directory, supported ecosystem, schedule |
| Security alert but no PR | Fix availability, security-update setting, target branch, permissions, ecosystem support |
| Private dependency cannot resolve | Registry type/URL, secret name, token scope, package-manager configuration |
| Too many PRs | Groups, schedule, PR limit, dependency scope |
| Update PR fails CI | Breaking changes, lockfile, runtime compatibility, tests |
| Config validation error | Exact ecosystem identifier and supported option names |

## 9. Lab deliverables
Complete `practical.md`. Use templates in `templates/` to record review decisions and exceptions.

## Official references
- About Dependabot: https://docs.github.com/en/code-security/dependabot
- Dependabot configuration file: https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file
- Options reference: https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference
- Configure security updates: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/configure-security-updates
- Supported ecosystems: https://docs.github.com/en/code-security/dependabot/ecosystems-supported-by-dependabot
