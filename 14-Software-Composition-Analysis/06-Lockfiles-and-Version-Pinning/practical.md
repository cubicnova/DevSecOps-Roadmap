# Practical Exercises – Lockfiles and Version Pinning

## Lab 1: Inspect npm manifest and lockfile
1. Open `examples/node-app/package.json` and `package-lock.json`.
2. Identify declared ranges, exact resolved versions, direct/transitive dependencies, source URLs, and integrity fields.
3. Draw a small dependency tree.

## Lab 2: Reproducible install
From `examples/node-app`:
```bash
npm ci
npm ls --all
```
Record Node/npm versions and confirm tracked files were not unexpectedly changed. Do not commit `node_modules`.

## Lab 3: Detect drift
On a disposable copy, modify the dependency range in `package.json` without updating the lockfile. Run `npm ci`, record the failure, then restore the original files.

## Lab 4: Controlled update
Create a branch, update one dependency, inspect both manifest and lockfile diffs, and run tests, build, SCA, and license checks. Record new transitive packages and source/integrity changes.

## Lab 5: Python pinning and hashes
Inspect `examples/python-app/requirements.txt`. Generate real hashes for trusted artifacts in a controlled environment and test `pip install --require-hashes`. Do not use the placeholder as a real digest.

## Lab 6: Ecosystem comparison
Compare pnpm, Yarn, uv, pip, Cargo, and Gradle lock strategies. Find the current frozen/locked validation command for each in official documentation.

## Lab 7: CI policy review
Review `.github/workflows/lockfile-validation.yml`: action SHA pinning, permissions, runtime pinning, frozen install, tests, and validation gaps.

## Submission checklist
- [ ] Dependency tree
- [ ] Reproducible install evidence
- [ ] Drift failure evidence
- [ ] Controlled update diff
- [ ] Python hash-check evidence
- [ ] Ecosystem comparison
- [ ] CI review
