# Lockfiles and Version Pinning – Examples

## npm: create and enforce lockfile
```bash
npm install
git add package.json package-lock.json
npm ci
npm ls --all
git diff -- package.json package-lock.json
```

## npm: update one dependency deliberately
```bash
npm update is-number
npm test
git diff -- package.json package-lock.json
```
Review the resulting direct and transitive changes before committing.

## npm overrides
```json
{
  "overrides": {
    "some-transitive-package": "1.2.3"
  }
}
```
Illustrative only: replace with a verified compatible package/version and document the reason.

## Frozen installs
```bash
pnpm install --frozen-lockfile
yarn install --immutable
uv sync --locked
cargo build --locked
```

## pip hashes
```text
# requirements-hashed.txt – example shape only
requests==2.32.3 \
    --hash=sha256:REPLACE_WITH_VERIFIED_SHA256
```
```bash
pip install --require-hashes -r requirements-hashed.txt
```
The placeholder is deliberately invalid. Generate real hashes from trusted, approved artifacts.

## Gradle
```bash
./gradlew dependencies --write-locks
```
Use `--write-locks` only when intentionally generating/updating lock state; review and commit the resulting files.
