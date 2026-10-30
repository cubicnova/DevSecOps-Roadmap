# GitLab CI/CD Dependency Caching — Examples

These examples are focused on dependency caches. Adapt images and package commands to your project. Caches are optimizations, so each job must still work when a cache is empty.

## 1. Basic cache

```yaml
basic_cache:
  stage: test
  cache:
    key: "basic-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/
  script:
    - mkdir -p .cache
    - echo "cache sample" > .cache/example.txt
    - cat .cache/example.txt
```

## 2. Python pip cache

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

## 3. Node.js npm cache

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

## 4. Maven dependency cache

```yaml
maven_tests:
  image: maven:3.9-eclipse-temurin-21
  stage: test
  variables:
    MAVEN_OPTS: "-Dmaven.repo.local=$CI_PROJECT_DIR/.m2/repository"
  cache:
    key:
      files:
        - pom.xml
    paths:
      - .m2/repository/
  script:
    - mvn test
```

## 5. Ruby Bundler cache

```yaml
ruby_tests:
  image: ruby:3.3
  stage: test
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

## 6. Branch-specific cache with fallback

```yaml
npm_tests:
  image: node:22
  stage: test
  cache:
    key: "npm-$CI_COMMIT_REF_SLUG"
    fallback_keys:
      - "npm-$CI_DEFAULT_BRANCH"
      - "npm-default"
    paths:
      - .npm/
  script:
    - npm ci --cache .npm --prefer-offline
    - npm test
```

## 7. Pull-only cache for parallel jobs

```yaml
default:
  cache:
    key: "pip-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/pip/
    policy: pull

test_unit:
  image: python:3.12
  stage: test
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  script:
    - pip install -r requirements.txt
    - pytest tests/unit

test_integration:
  image: python:3.12
  stage: test
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
  script:
    - pip install -r requirements.txt
    - pytest tests/integration
```

These jobs only download the cache and do not upload updates. Ensure a separate job populates the same cache key if needed.

## 8. Dedicated cache builder

```yaml
stages: [prepare, test]

prepare_npm_cache:
  image: node:22
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

test_app:
  image: node:22
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
```

## 9. Multiple caches

```yaml
multi_dependency_job:
  image: alpine:3.20
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
    - echo "Use npm and Bundler commands for the project"
```

Use separate keys and paths for each ecosystem.

## 10. Disable cache for a sensitive job

```yaml
security_review:
  stage: test
  cache: []
  script:
    - echo "Run checks without restoring or saving dependency cache"
```

A cache-free job can reduce exposure to untrusted cache content, but it does not replace runner isolation or dependency verification.

## 11. Cache artifacts separately

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

test_output:
  stage: test
  script:
    - test -d dist
    - echo "Build output received as an artifact"
```

Cache speeds up dependency downloads; artifacts carry the `dist/` build output.

## 12. Clear or rotate a stale cache

```yaml
dependency_job:
  stage: test
  cache:
    key: "pip-v2-$CI_COMMIT_REF_SLUG"
    paths:
      - .cache/pip/
  script:
    - pip install -r requirements.txt
    - pytest
```

Changing the key creates a new cache namespace. You can also clear runner caches in the GitLab UI. Pin dependencies so a cache reset does not silently change the resolved versions.
