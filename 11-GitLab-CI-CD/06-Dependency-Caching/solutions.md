# GitLab CI/CD Dependency Caching — Solutions and Explanations

## Solution 1: Basic cache

```yaml
basic_cache:
  stage: test
  cache:
    key: "basic-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/
  script:
    - mkdir -p .cache
    - echo "sample" > .cache/example.txt
    - cat .cache/example.txt
```

The first run may create and upload the cache. A later run with the same key may restore it, depending on runner and storage configuration.

## Solution 2: Python pip cache

```yaml
python_tests:
  image: python:3.12
  stage: test
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  cache:
    key:
      files:
        - requirements.txt
    paths:
      - .cache/pip/
  script:
    - pip install -r requirements.txt
    - pytest
```

Pin package versions in `requirements.txt`. A lockfile-based key changes when the dependency specification changes.

## Solution 3: npm cache

```yaml
node_tests:
  image: node:22
  stage: test
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
  script:
    - npm ci --cache .npm --prefer-offline
    - npm test
```

Caching `.npm/` stores npm's package download cache. `npm ci` installs from the lockfile and is appropriate for reproducible CI installs.

## Solution 4: Lockfile-based invalidation

```yaml
cache:
  key:
    files:
      - package-lock.json
  paths:
    - .npm/
```

GitLab calculates the cache key from the content of the listed files. When the lockfile changes, a different key is used. If none of the listed files exist, GitLab uses its documented fallback behavior; validate the result in CI Lint and job logs.

## Solution 5: Fallback keys

```yaml
cache:
  key: "npm-$CI_COMMIT_REF_SLUG"
  fallback_keys:
    - "npm-$CI_DEFAULT_BRANCH"
    - "npm-default"
  paths:
    - .npm/
```

GitLab tries the primary key first, then fallback keys in order. If none are found, the job proceeds without a cache and can upload a new one according to the policy.

## Solution 6: Cache policies

```yaml
prepare:
  stage: build
  cache:
    key: "pip-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/pip/
    policy: push
  script:
    - pip download -r requirements.txt -d .cache/pip

tests:
  stage: test
  cache:
    key: "pip-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/pip/
    policy: pull
  script:
    - pip install --no-index --find-links .cache/pip -r requirements.txt
    - pytest
```

This pattern uses a writer job and read-only consumers. Ensure the cache content is compatible with the consumer environment. `pull-push` remains the default.

## Solution 7: Cache versus artifacts

```yaml
stages: [build, test]

build:
  stage: build
  cache:
    key: "npm-$CI_COMMIT_REF_SLUG"
    paths:
      - .npm/
  script:
    - npm ci --cache .npm
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

verify:
  stage: test
  script:
    - test -d dist
    - echo "Artifact is available"
```

The cache accelerates dependency installation. The artifact preserves the required `dist/` output for later jobs and downloads.

## Solution 8: Multiple caches

```yaml
multi_cache:
  stage: test
  cache:
    - key:
        files:
          - package-lock.json
      paths:
        - .npm/
    - key:
        files:
          - Gemfile.lock
      paths:
        - vendor/ruby/
  script:
    - echo "Run the relevant package-manager commands"
```

Each cache entry should have a focused path and key. Avoid overlapping paths that can be overwritten by different cache archives.

## Solution 9: Runner storage

Cache availability depends on runner executor and configuration. A local cache on one runner host may not be available to another runner host. Distributed cache storage, commonly object storage, can provide shared access when configured by the runner administrator.

## Solution 10: Cache security

Recommended actions:
- Cache only dependency-manager directories.
- Never cache `.env`, tokens, private keys, or credentials.
- Avoid `untracked: true` unless you have a specific, reviewed reason.
- Keep protected and unprotected cache boundaries enabled unless there is a justified need to share.
- Avoid `cache:unprotect: true` for sensitive caches.
- Use separate keys for trusted and untrusted workloads when appropriate.
- Use `cache: []` for jobs that should not restore or upload a cache.
- Treat cached executable content as untrusted unless its origin and integrity are verified.

## Solution 11: Rotate a stale cache

```yaml
dependency_job:
  stage: test
  cache:
    key: "deps-v2-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/pip/
  script:
    - pip install -r requirements.txt
    - pytest
```

Changing the key creates a new cache namespace. GitLab also provides a UI action to clear runner caches. Pin dependencies before clearing caches so fresh downloads do not unexpectedly resolve to new versions.

## Solution 12: Example optimized pipeline

```yaml
stages: [prepare, test]

default:
  image: node:22

prepare_dependencies:
  stage: prepare
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
    policy: push
  script:
    - npm ci --cache .npm --prefer-offline

unit_tests:
  stage: test
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
    policy: pull
  script:
    - npm ci --cache .npm --prefer-offline
    - npm test

build:
  stage: test
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
    policy: pull
  script:
    - npm ci --cache .npm --prefer-offline
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week
```

Measure multiple runs. A cache can reduce downloads but may add archive upload/download overhead. The best design depends on dependency size, runner topology, storage latency, and job parallelism.

## Common troubleshooting

| Problem | Likely cause | Recommended action |
|---|---|---|
| No cache restored | New key, missing archive, or runner storage issue | Check key and runner cache configuration |
| Cache path empty | Package manager writes elsewhere | Configure tool cache directory inside `$CI_PROJECT_DIR` |
| Stale package data | Key does not depend on lockfile | Use `cache:key:files` |
| Cache overwritten | Multiple jobs write different data to same key | Separate keys or use a single writer with `pull` consumers |
| No sharing between runners | Local cache only | Configure distributed cache |
| Cache archive huge | Too many paths or untracked files | Narrow `paths`, avoid broad untracked caching |
| Protected cache not shared | Protected/unprotected separation | Keep separation for security; review policy before changing |
| Cache miss after clear | Cache index/key changed | Allow a fresh cache to be populated |

## Official documentation
- [Caching in GitLab CI/CD](https://docs.gitlab.com/ci/caching/)
- [CI/CD YAML syntax reference](https://docs.gitlab.com/ci/yaml/)
- [GitLab Runner configuration](https://docs.gitlab.com/runner/configuration/)
