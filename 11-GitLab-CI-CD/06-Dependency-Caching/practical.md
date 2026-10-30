# GitLab CI/CD Dependency Caching — Practical Exercises

## Prerequisites
- A GitLab project with a working runner.
- Basic GitLab CI/CD and YAML knowledge.
- One sample project using Python, Node.js, Java/Maven, or Ruby.
- A dependency manifest or lockfile.

## Lab 1: Create a basic cache
1. Add a job with `cache:key` and `cache:paths`.
2. Create a sample file in the cached directory.
3. Run the pipeline twice.
4. Inspect job logs for cache restore and upload messages.

**Expected result:** You can identify cache download and upload phases.

## Lab 2: Cache Python dependencies
1. Create `requirements.txt` with pinned package versions.
2. Set `PIP_CACHE_DIR` to `$CI_PROJECT_DIR/.cache/pip`.
3. Cache `.cache/pip/`.
4. Run `pip install -r requirements.txt`.
5. Run the pipeline again and compare the install behavior.

**Expected result:** Pip's download cache is reused when available.

## Lab 3: Cache npm dependencies
1. Create a Node.js project with `package-lock.json`.
2. Cache `.npm/`.
3. Run `npm ci --cache .npm --prefer-offline`.
4. Run the pipeline a second time.
5. Change the lockfile and observe cache-key behavior.

**Expected result:** The cache key is tied to the dependency lockfile.

## Lab 4: Use cache:key:files
1. Configure `cache:key:files` using the project's lockfile.
2. Run the pipeline.
3. Make a dependency change that updates the lockfile.
4. Run the pipeline again.
5. Explain why a new cache key is generated.

**Expected result:** Dependency changes invalidate the relevant cache.

## Lab 5: Configure fallback keys
1. Create a branch-specific cache key.
2. Add a default-branch fallback key.
3. Run from a new feature branch where no branch cache exists.
4. Inspect logs to see whether a fallback cache was restored.
5. Record what happens if no cache exists at all.

**Expected result:** You understand fallback lookup order and cache-miss behavior.

## Lab 6: Compare cache policies
1. Create one job using `pull-push`.
2. Create a cache-preparation job using `push`.
3. Create a consumer job using `pull`.
4. Run the pipeline and inspect cache logs.
5. Explain why multiple parallel jobs should generally avoid all writing the same cache.

**Expected result:** You can select a cache policy based on the job's role.

## Lab 7: Cache and artifacts comparison
1. Cache a package-manager directory.
2. Create a build output directory such as `dist/`.
3. Store `dist/` as an artifact.
4. Add a downstream job that reads the artifact.
5. Explain why `dist/` should not rely only on cache.

**Expected result:** You can choose the correct mechanism for dependencies versus required outputs.

## Lab 8: Configure multiple caches
1. Create a project that uses two dependency ecosystems, or create two illustrative cache entries.
2. Give each entry its own key and path.
3. Run the pipeline.
4. Inspect cache restore and upload messages.
5. Document why overlapping paths and identical keys can cause confusion.

**Expected result:** Multiple dependency caches are isolated by key and path.

## Lab 9: Investigate runner cache behavior
1. Run a job on one runner.
2. Run a later job on another runner if available.
3. Compare cache availability.
4. Ask the runner administrator whether distributed cache is configured.
5. Document how executor and storage configuration affect cache sharing.

**Expected result:** You understand that a YAML cache declaration does not guarantee cross-runner availability.

## Lab 10: Cache security review
1. Search the repository for `.env`, credentials, private keys, and token files.
2. Review all configured cache paths.
3. Remove sensitive files from cache paths.
4. Consider `cache: []` for a sensitive job.
5. Review protected/unprotected branch cache separation and `cache:unprotect`.
6. Document trust boundaries between fork/MR pipelines and protected deployment jobs.

**Expected result:** The cache contains only appropriate reusable dependencies.

## Lab 11: Recover from stale cache
1. Identify a dependency cache that is stale or incompatible.
2. Change its key prefix, such as from `deps-v1` to `deps-v2`.
3. Run the pipeline.
4. Verify dependencies are downloaded again.
5. Explain when manual cache clearing is appropriate.

**Expected result:** You can safely rotate a cache namespace.

## Lab 12: Optimize a pipeline
1. Select a sample project and record its baseline pipeline duration.
2. Add lockfile-based caching.
3. Narrow cache paths to package-manager directories.
4. Use `pull` for parallel consumers and one cache writer if suitable.
5. Run at least three pipeline executions.
6. Compare durations and cache hit/miss behavior.
7. Document limitations and security trade-offs.

**Expected result:** You can evaluate whether caching improves the pipeline rather than assuming it does.

## Lab deliverables
- Updated `.gitlab-ci.yml`.
- Screenshots or log excerpts showing cache restore/upload (no secrets).
- Before/after pipeline duration observations.
- Cache key and policy explanation.
- Cache-versus-artifact comparison.
- Security review of cache paths and trust boundaries.
