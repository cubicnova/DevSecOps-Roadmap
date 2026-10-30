# GitLab CI/CD Dependency Caching

## Overview

Dependency caching helps reduce pipeline execution time by reusing downloaded packages and generated dependency data across jobs and pipelines. In GitLab CI/CD, cache behavior is configured with the `cache` keyword in `.gitlab-ci.yml`.

Use cache for dependencies such as Python packages, Node.js packages, Ruby gems, and Maven dependencies. Use artifacts to pass required build outputs between jobs. A cache is an optimization: it may be unavailable, so jobs must still be able to complete correctly when a cache miss occurs.

## Learning objectives

- Explain GitLab cache behavior and how it differs from artifacts.
- Configure cache paths, keys, and policies.
- Use lockfiles to invalidate caches when dependencies change.
- Configure fallback keys and multiple caches.
- Share cache configuration using `default`, anchors, and `extends`.
- Optimize Python, Node.js, Java/Maven, and Ruby workflows.
- Understand runner storage and distributed cache.
- Apply cache security and troubleshooting practices.

## 1. Cache fundamentals

A job can download a cache at startup and upload updated cache content at completion. By default, the policy is `pull-push`.

```yaml
python_tests:
  image: python:3.12
  stage: test
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  cache:
    key: "pip-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/pip/
  script:
    - pip install -r requirements.txt
    - pytest
```

The cache path must be inside the project working directory (`$CI_PROJECT_DIR`). Cache keys identify cache archives. Jobs using the same key can share cache data, subject to runner configuration and GitLab's protected/unprotected cache separation.

## 2. Cache versus artifacts

| Feature | Cache | Artifacts |
|---|---|---|
| Main purpose | Reuse dependencies and speed up jobs | Preserve job outputs and pass them to later jobs |
| Availability | Best effort; can be missing | Managed as pipeline job outputs |
| Typical contents | Package download directories | Build output, reports, binaries |
| Key behavior | Explicit cache key and fallback keys | Associated with job and pipeline |
| Recommended use | `node_modules` package cache, pip cache | `dist/`, test reports, compiled output |

Do not rely on cache as the only way to transfer a required build output to another job.

## 3. Cache paths

`cache:paths` accepts paths relative to the project directory and supports glob patterns. Files can be cached even when they are ignored or untracked.

```yaml
cache:
  key: "npm-$CI_COMMIT_REF_SLUG"
  paths:
    - .npm/
    - node_modules/
```

Cache only the directories needed for performance. Avoid broad paths such as the entire project directory.

## 4. Cache keys

A key identifies a cache archive. If omitted, jobs using cache can share the default key, which is usually too broad for unrelated dependency sets.

Branch-specific key:

```yaml
cache:
  key: "deps-$CI_COMMIT_REF_SLUG"
  paths:
    - .cache/pip/
```

Lockfile-based key:

```yaml
cache:
  key:
    files:
      - package-lock.json
  paths:
    - .npm/
```

`cache:key:files` changes when the content of the listed files changes, allowing caches to be reused across branches with the same lockfile content. It supports a limited number of paths; consult the current GitLab YAML reference for the version-specific limit and feature availability. CI/CD variables are not supported inside the `files` list.

## 5. Fallback cache keys

Fallback keys let a job try a shared cache when its primary key is not found.

```yaml
cache:
  key: "npm-$CI_COMMIT_REF_SLUG"
  fallback_keys:
    - "npm-$CI_DEFAULT_BRANCH"
    - "npm-default"
  paths:
    - .npm/
```

GitLab tries fallback keys in order. If no cache is found, the job continues without one and can create a new cache. Each cache entry supports up to five fallback keys in current documentation.

## 6. Cache policies

| Policy | Downloads cache | Uploads cache | Common use |
|---|---:|---:|---|
| `pull-push` | Yes | Yes | Default; a job both consumes and updates cache |
| `pull` | Yes | No | Parallel test jobs consuming a prepared cache |
| `push` | No | Yes | A dedicated job building/updating cache |

Example:

```yaml
prepare_cache:
  stage: build
  cache:
    key: "npm-$CI_COMMIT_REF_SLUG"
    paths:
      - .npm/
    policy: push
  script:
    - npm ci --cache .npm --prefer-offline

test:
  stage: test
  cache:
    key: "npm-$CI_COMMIT_REF_SLUG"
    paths:
      - .npm/
    policy: pull
  script:
    - npm ci --cache .npm --prefer-offline
    - npm test
```

The cache builder must use the same key and compatible paths as its consumers.

## 7. Multiple caches

A job can define multiple cache entries. Use different keys for different dependency ecosystems or directories.

```yaml
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
```

Current GitLab documentation limits the number of cache entries per job. Keep cache entries focused and avoid overlapping paths with different keys.

## 8. Language-specific patterns

### Python / pip

```yaml
python_tests:
  image: python:3.12
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

Pin dependency versions and use a lockfile or fully pinned requirements file for reproducible builds.

### Node.js / npm

```yaml
node_tests:
  image: node:22
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

Caching the npm download cache is often safer than caching `node_modules`, which can be platform- and runtime-dependent.

### Java / Maven

```yaml
maven_tests:
  image: maven:3.9-eclipse-temurin-21
  cache:
    key:
      files:
        - pom.xml
    paths:
      - .m2/repository/
  variables:
    MAVEN_OPTS: "-Dmaven.repo.local=$CI_PROJECT_DIR/.m2/repository"
  script:
    - mvn test
```

For stronger invalidation, include the dependency lock/descriptor files that control the resolved dependency graph.

### Ruby / Bundler

```yaml
ruby_tests:
  image: ruby:3.3
  cache:
    key:
      files:
        - Gemfile.lock
    paths:
      - vendor/ruby/
  script:
    - bundle config set --local path 'vendor/ruby'
    - bundle install
    - bundle exec rake test
```

## 9. Shared cache configuration

Use `default:cache` to provide a common cache configuration:

```yaml
default:
  cache: &dependency_cache
    key:
      files:
        - package-lock.json
    paths:
      - .npm/
    policy: pull-push

test:
  cache:
    <<: *dependency_cache
    policy: pull
  script:
    - npm ci --cache .npm
    - npm test
```

A job-level cache configuration can override the default cache. YAML anchors can help preserve and selectively override settings.

## 10. Runner and distributed cache

Cache availability depends on runner executor, runner configuration, and whether jobs use the same runner or a shared distributed cache. A local runner cache may not be available to another runner machine.

For scalable deployments, administrators can configure distributed cache storage such as object storage. This is a runner administration task; the YAML `cache` block alone does not configure the storage backend.

## 11. Cache security

- Do not cache secrets, credentials, private keys, or `.env` files.
- Avoid sharing writable caches between untrusted and privileged jobs.
- Be careful with `cache:unprotect`; it can allow protected-branch cache access from unprotected contexts.
- Use separate cache keys for unrelated dependency sets.
- Do not execute untrusted scripts or binaries from a cache without validation.
- Keep dependency versions pinned and verify package integrity.
- Consider disabling cache in sensitive jobs with `cache: []`.
- Remember that caches may contain untracked or ignored files.

## 12. Troubleshooting

| Symptom | Likely cause | What to check |
|---|---|---|
| Cache never restored | Key mismatch or cache storage unavailable | Key, path, runner configuration |
| Cache restored but dependencies reinstall | Wrong directory or package manager configuration | Tool cache path and install flags |
| Stale dependencies | Key does not track lockfile changes | Use `cache:key:files` |
| Different jobs overwrite cache | Same key used for different paths/content | Separate keys by job or ecosystem |
| Cache unavailable across runners | Local-only cache storage | Configure distributed cache |
| Cache too large | Broad paths or `untracked: true` | Narrow `paths` and clean old data |
| Protected branch cache differs | Protected/unprotected cache separation | Review project cache settings and ref protection |

## Further reading

- [Caching in GitLab CI/CD](https://docs.gitlab.com/ci/caching/)
- [CI/CD YAML syntax reference](https://docs.gitlab.com/ci/yaml/)
- [GitLab Runner configuration](https://docs.gitlab.com/runner/configuration/)
