# Solutions and Instructor Guidance

Output depends on package manager version and platform; record tool versions.

## Lab 1
The manifest declares acceptable dependency versions. The lockfile captures the resolved tree, including exact versions and source/integrity metadata. Transitive dependencies are introduced by another dependency.

## Lab 2
`npm ci` installs from the lockfile, removes existing `node_modules`, and fails if manifest and lockfile are inconsistent. It is suitable for CI reproducibility checks.

## Lab 3
A changed manifest range that is inconsistent with the lockfile should cause `npm ci` to fail. Regenerate intentionally with `npm install`, then review the lockfile diff.

## Lab 4
A good update diff contains only expected packages and metadata. Investigate new transitive packages, changed registries/URLs, integrity values, Git sources, and lifecycle scripts. Run tests and security scans.

## Lab 5
pip hash-checking requires pinned requirements and valid hashes for every permitted artifact, including transitive requirements. Hashes verify artifact bytes, not package safety.

## Lab 6
- pnpm: `pnpm install --frozen-lockfile`
- Yarn modern: `yarn install --immutable`
- uv: `uv sync --locked`
- Cargo: `cargo build --locked`
- Gradle: enable dependency locking and commit generated lock state; do not rewrite it during routine validation.

## Lab 7
Production CI should use immutable action SHAs, least-privilege permissions, a controlled runtime, frozen installs, tests, and SCA. A lockfile check alone does not prove dependencies are secure.

## Assessment rubric
- Manifest/lockfile concepts: 15%
- npm reproducibility and drift: 20%
- Controlled updates and review: 20%
- Python hashes/integrity: 15%
- Ecosystem comparison: 15%
- CI review and evidence: 15%
