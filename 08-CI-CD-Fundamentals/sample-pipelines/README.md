# Sample CI/CD Pipelines

This module contains practical, learning-focused examples of CI/CD pipelines. The samples illustrate common pipeline patterns from validation through build, testing, artifact creation, and deployment.

> **Safety note:** These examples are educational starting points. Review permissions, pin third-party actions to verified full commit SHAs, protect environments, and adapt commands to your application before using them in production.

## Learning objectives

By completing this module, you should be able to:

- Recognize common pipeline stages and their dependencies.
- Build a pull-request validation pipeline.
- Separate build/test, packaging, and deployment responsibilities.
- Reuse shared workflow logic to reduce duplication.
- Add quality gates and least-privilege permissions.
- Identify risks involving secrets, untrusted pull requests, artifacts, and deployment credentials.

## Suggested folder layout

```text
sample-pipelines/
├── README.md
├── examples.md
├── practical.md
└── solution.md
```

The examples are documented in Markdown so they can be reviewed before being copied into a repository's `.github/workflows/` directory.

## Pipeline patterns

| Pattern | Typical trigger | Purpose |
|---|---|---|
| Pull request CI | `pull_request` | Fast feedback: lint, unit tests, static checks |
| Main-branch CI | `push` to `main` | Verify integration and produce a versioned artifact |
| Release pipeline | tag or release event | Validate release inputs and package release outputs |
| Deployment pipeline | approved manual trigger or protected environment | Deploy a previously validated artifact |
| Reusable workflow | `workflow_call` | Centralize repeatable build or test logic |
| Scheduled checks | `schedule` | Run periodic quality or dependency checks |

## Recommended flow

```text
Pull request
   |
   v
Lint -> Unit tests -> Static checks
   |
   v
Merge to main
   |
   v
Build once -> Test artifact -> Publish artifact
   |
   v
Approval / protected environment
   |
   v
Deploy the same artifact -> Smoke test -> Record result
```

## Design principles

1. **Fail fast:** run cheap validation before expensive build or integration stages.
2. **Build once, promote many:** promote the same immutable artifact between environments instead of rebuilding it for each environment.
3. **Use explicit permissions:** set the minimum required `GITHUB_TOKEN` permissions at workflow or job level.
4. **Keep secrets out of logs and source control:** use a secrets manager or protected environment secrets.
5. **Treat pull-request code as untrusted:** avoid exposing privileged secrets or write tokens to untrusted code.
6. **Pin dependencies:** pin actions and reusable workflows to reviewed full commit SHAs where practical.
7. **Protect deployment environments:** use reviewers, branch restrictions, and scoped credentials.
8. **Keep artifacts traceable:** include commit SHA, build metadata, test results, and provenance where supported.

## How to use the samples

1. Read `examples.md` and choose a pattern matching your project.
2. Replace placeholder application commands with your real build and test commands.
3. Check the required permissions and secret names.
4. Run in a test repository first.
5. Complete the exercises in `practical.md`.
6. Compare your design with the guidance in `solution.md`.

## Further reading

- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Reusing workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)

See also the parent [CI/CD Fundamentals](../README.md) directory, if present.
