# 06 – Lockfiles and Version Pinning

## Learning objectives
- Distinguish dependency manifests from lockfiles.
- Understand exact versions, semantic version ranges, and transitive dependencies.
- Generate and review lockfiles and enforce deterministic installs in CI.
- Understand integrity hashes, dependency sources, and safe update practices.

## Manifest vs lockfile
A manifest declares acceptable dependencies and often version ranges. A lockfile records the resolved dependency graph and exact versions, commonly including package source and integrity metadata. For application repositories, commit both manifest and lockfile.

A lockfile improves reproducibility; it does not prove dependencies are safe or guarantee identical results across every operating system and architecture.

## npm version ranges
- `1.2.3`: exact version.
- `^1.2.3`: compatible updates below 2.0.0 (with special zero-major rules).
- `~1.2.3`: patch updates within 1.2.x.
- `>=1.2.3 <2.0.0`: explicit interval.
- `*` / `latest`: broad or dynamic selection; avoid for production declarations.

For applications, a committed lockfile plus a frozen CI install is a practical baseline. Exact manifest pins can reduce drift but require disciplined updates.

## npm workflow
```bash
npm install                 # intentionally generate/update package-lock.json
npm ci                      # reproducible CI install from lockfile
npm ls --all                # inspect installed dependency tree
git diff -- package.json package-lock.json
```
`npm ci` requires a lockfile, fails when it disagrees with `package.json`, and removes existing `node_modules`. Review both files together.

Use npm `overrides` only for a reviewed transitive dependency constraint; test compatibility and document the reason.

## Other ecosystems
| Ecosystem | Lockfile | Frozen/locked mode |
|---|---|---|
| pnpm | `pnpm-lock.yaml` | `pnpm install --frozen-lockfile` |
| Yarn modern | `yarn.lock` | `yarn install --immutable` |
| Python uv | `uv.lock` | `uv sync --locked` |
| pip | pinned requirements + hashes | `pip install --require-hashes -r requirements.txt` |
| Cargo | `Cargo.lock` | `cargo build --locked` |
| Gradle | `gradle.lockfile` when locking enabled | resolve against committed lock state |

Check current tool documentation and version; flags and behavior can change.

## Python hash checking
Example pinned requirements:
```text
requests==2.32.3
urllib3==2.2.3
```
For artifact integrity enforcement, generate and review hashes for every permitted distribution, then use:
```bash
pip install --require-hashes -r requirements-hashed.txt
```
Hash mode requires pinned requirements and valid hashes for all dependencies, including transitive ones. Never copy placeholder hashes from tutorials. A hash verifies bytes, not that the package is benign.

## Integrity and provenance review
Review unexpected changes to resolved URLs, registries, Git sources/commit IDs, integrity hashes, transitive packages, optional/platform-specific packages, and install scripts. Confirm package source provenance and investigate unexpected source changes.

## Safe dependency update process
1. Create a dedicated update branch.
2. Update one package or a small related group.
3. Regenerate the lockfile with the intended package manager.
4. Review manifest and lockfile diffs, including transitive changes and sources.
5. Run tests, build, SCA, and license checks.
6. Obtain review and retain rollback details.

## CI enforcement
Use frozen/immutable/locked install commands. Pin runtime/toolchain versions and third-party CI actions to immutable full commit SHAs. Use least-privilege permissions. Lockfile validation does not replace vulnerability scanning, malware review, or license checks.

## Official references
- npm lockfiles: https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/
- npm ci: https://docs.npmjs.com/cli/v11/commands/npm-ci/
- OWASP dependency management: https://owasp.github.io/DevSecOpsGuideline/2-Process/2-3-Build/2-3-2-Software-Composition-Analysis/2-3-2-2-Dependency-Management-and-Cooldown-Policies/
- pip secure installs: https://pip.pypa.io/en/stable/topics/secure-installs/
- uv: https://docs.astral.sh/uv/concepts/projects/sync/
- Gradle: https://docs.gradle.org/current/userguide/dependency_locking.html
- Cargo: https://doc.rust-lang.org/cargo/commands/cargo-build.html
