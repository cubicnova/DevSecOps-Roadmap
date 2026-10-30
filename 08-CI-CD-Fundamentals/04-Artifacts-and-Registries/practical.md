# Practical Exercises — Artifacts and Registries

**Level:** Beginner to intermediate  
**Environment:** Local computer, a test Git repository, Docker, and optionally GitHub Container Registry (GHCR).  
**Safety:** Use a repository and registry you control. Never commit credentials, `.env` files, private keys, or production data.

## Exercise 1 — Identify artifact types

Classify each item as a source file, build artifact, container image, cache, test evidence, SBOM, or provenance record. Explain any overlap.

1. `app.py`
2. `dist/app-1.0.0.whl`
3. `ghcr.io/example/app@sha256:...`
4. Downloaded pip cache
5. `junit.xml`
6. `sbom.cdx.json`
7. A signed statement linking an image to a source commit and build workflow

**Deliverable:** A table with item, type, purpose, and sensitivity considerations.

## Exercise 2 — Create and hash an archive

1. Create a Git repository with a README and one sample source file.
2. Create a compressed archive from the current commit.
3. Calculate its SHA-256 checksum.
4. Modify the source, commit the change, and create another archive.
5. Compare the checksums.

**Questions:** Why did the checksum change? What information should be stored alongside the artifact to make it traceable?

## Exercise 3 — Verify integrity

1. Calculate a checksum for an archive.
2. Store the expected checksum separately in a trusted local file.
3. Change one byte of a copy of the archive.
4. Recalculate the checksum and compare it with the original.
5. Document the verification result.

**Acceptance criteria:** Explain why matching checksums are useful and why a checksum from an untrusted source is not proof of authenticity.

## Exercise 4 — Versioning design

Design an artifact naming convention for a web API with release versions, pull-request builds, and production deployments.

Your scheme must include:

- Human-readable release version
- Source commit identifier
- Registry path or package namespace
- Immutable identifier for production deployment
- Rules for avoiding accidental tag overwrite

**Deliverable:** Five sample artifact identifiers and a paragraph explaining the scheme.

## Exercise 5 — Build and inspect a Docker image

1. Create a minimal Dockerfile for a small application or use a harmless sample image.
2. Build it with a versioned tag.
3. Inspect the image metadata.
4. Push it only if you have a test registry and authorization.
5. Record the registry digest after publishing.

**Questions:** What is the difference between a local image ID, a tag, and a registry digest?

## Exercise 6 — Publish a test image to GHCR (optional)

1. Confirm you own or have permission to publish to the target GitHub organization/user.
2. Authenticate using the official registry instructions and a least-privilege token or supported identity.
3. Tag the image with your namespace.
4. Push it to GHCR.
5. Review package visibility and access settings.
6. Record the image digest and test pulling it by digest.

**Deliverable:** Redacted command history or screenshots. Never include tokens in the submission.

## Exercise 7 — Add artifact upload to CI

Use `examples.md` to create a workflow that archives source files, calculates a checksum, and uploads both files as a workflow artifact.

Verify:

- The workflow runs on a pull request or push.
- The uploaded artifact can be downloaded.
- The checksum file is present.
- A failed archive step causes the job to fail.
- Workflow permissions are no broader than needed.

## Exercise 8 — Plan an SBOM and provenance flow

For a containerized API, design where the pipeline will:

- Generate an SBOM
- Scan dependencies and the image
- Record source revision and builder identity
- Associate evidence with the artifact digest
- Verify the evidence before release

**Deliverable:** A diagram plus a table showing evidence type, generation stage, storage location, and verification policy.

## Exercise 9 — Design artifact promotion

**Scenario:** The staging environment has passed tests, but the current process rebuilds the image before production deployment.

Redesign the process to promote the same image. Include:

- Image tag and digest recording
- Registry access controls
- Staging test evidence
- Production approval
- Digest verification at deployment
- Rollback artifact retention

**Question:** What risks arise if the production image is rebuilt from the same source commit rather than promoted?

## Exercise 10 — Create a registry access matrix

Define read, write, delete, and promote permissions for these identities:

- Developer
- CI build job
- Release manager
- Production deploy job
- Security auditor

Use least privilege. Explain why the build job should not automatically have delete access to released artifacts.

## Exercise 11 — Write a retention policy

Create a policy for pull-request builds, nightly builds, release candidates, production releases, SBOMs, and audit logs.

Include:

- Retention duration or decision rule
- Artifact owner
- Deletion authorization
- Exceptions for active deployments and rollback
- Compliance and incident-response requirements

## Exercise 12 — Mini project: secure artifact lifecycle

Build a documented artifact lifecycle for a sample API or web application.

Required outputs:

- `artifact-lifecycle.md` with a diagram
- Versioning and naming policy
- Build artifact and checksum
- Registry choice and access matrix
- Security scanning and SBOM plan
- Provenance/signature verification plan
- Promotion and rollback plan
- Retention policy

**Evaluation rubric (100 points):**

| Area | Points |
|---|---:|
| Correct artifact terminology and lifecycle | 15 |
| Versioning and traceability | 15 |
| Integrity verification | 15 |
| Registry access control | 15 |
| SBOM, scanning, provenance, or signing plan | 15 |
| Artifact promotion and rollback | 15 |
| Retention and documentation | 10 |

## Submission checklist

- [ ] No credentials or sensitive files are included.
- [ ] Artifacts have clear version and source metadata.
- [ ] Checksums are verified against a trusted value.
- [ ] Production deployment uses an exact artifact identity.
- [ ] Registry permissions follow least privilege.
- [ ] SBOM/provenance expectations are documented.
- [ ] Retention does not remove active rollback artifacts.
