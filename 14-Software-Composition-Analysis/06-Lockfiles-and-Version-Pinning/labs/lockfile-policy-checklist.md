# Lockfile Policy Checklist

- [ ] Correct lockfile committed for package manager
- [ ] Manifest and lockfile reviewed together
- [ ] CI uses frozen/immutable/locked install mode
- [ ] Package manager and runtime versions controlled
- [ ] No unexpected registries, URLs, or Git sources
- [ ] Integrity metadata changes reviewed
- [ ] Transitive dependency changes understood
- [ ] Updates include tests and SCA
- [ ] Overrides/exceptions have owner and expiry
- [ ] Rollback path documented
