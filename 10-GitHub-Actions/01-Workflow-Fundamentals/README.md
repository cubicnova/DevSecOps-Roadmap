# 01 - Workflow Fundamentals

Learn the core concepts and structure of GitHub Actions workflows: YAML files, events, jobs, runners, steps, and actions.

## Learning objectives

By the end of this module, you should be able to:

- Explain what GitHub Actions automates and when workflows run.
- Locate workflow files in `.github/workflows/`.
- Identify the roles of `name`, `on`, `permissions`, `jobs`, `runs-on`, and `steps`.
- Distinguish a job, a step, a shell command, and a reusable action.
- Create and troubleshoot a small workflow.
- Apply basic security practices to workflow design.

## Core concepts

| Concept | Meaning |
|---|---|
| Workflow | An automated process defined in a YAML file |
| Event / trigger | The event that starts a workflow, such as `push`, `pull_request`, or `workflow_dispatch` |
| Job | A group of steps executed on a runner |
| Runner | The machine/environment that executes a job |
| Step | A command or action within a job |
| Action | A reusable unit of automation referenced with `uses` |
| Workflow run | One execution of a workflow |

Workflow files must be saved under `.github/workflows/` and use a `.yml` or `.yaml` extension.

## Basic workflow anatomy

```yaml
name: Workflow Fundamentals

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  hello:
    name: Say hello
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Print a message
        run: echo "Hello from GitHub Actions"
```

> For production workflows, review action versions and pin third-party actions to full commit SHAs when stronger supply-chain assurance is required.

## Key fields

- `name`: Friendly workflow name shown in the Actions tab.
- `on`: Event(s) that trigger a run. Quote the key as `'on'` in some YAML tooling contexts if that tooling parses it as a boolean.
- `permissions`: Sets the permissions available to the workflow token. Start with least privilege.
- `jobs`: Defines one or more jobs.
- `runs-on`: Selects the runner environment.
- `steps`: Lists commands (`run`) or actions (`uses`) executed in order.
- `needs`: Makes a job wait for another job.
- `if`: Conditionally runs a job or step.
- `env`: Defines environment variables.

## Common triggers

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
  schedule:
    - cron: "17 4 * * 1"
```

Schedules use UTC and can be delayed during high load. Use manual or event-based triggers where timing is important.

## Job dependencies

Jobs run in parallel by default when they have no dependency. Use `needs` to express ordering:

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Linting"

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - run: echo "Testing after lint succeeds"
```

## Security basics

1. Set minimal `permissions`, for example `contents: read` when write access is not needed.
2. Never hard-code tokens, passwords, or private keys in workflow YAML.
3. Treat pull-request code and external actions as untrusted until reviewed.
4. Prefer maintained, versioned actions; pin actions to full commit SHAs for high-assurance pipelines.
5. Use `pull_request` for ordinary PR validation. Understand the risks before using `pull_request_target`.
6. Do not expose sensitive secrets to workflows that execute untrusted code.
7. Review logs and artifacts for accidental secret disclosure.

## Try it

1. Create `.github/workflows/hello.yml`.
2. Add the example workflow above.
3. Commit and push it to the repository's `main` branch.
4. Open **Actions** in GitHub and inspect the run.
5. Change the echo message and run it again.

## Troubleshooting checklist

- Is the YAML indentation consistent?
- Is the file under `.github/workflows/`?
- Does the event match the action you performed?
- Is the branch filter correct?
- Does every job define `runs-on`?
- Does every step contain a valid `run` or `uses` field?
- Are permissions sufficient but not broader than necessary?
- Did an action reference or shell command fail?

## Further reading

- [GitHub Actions workflows](https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows)
- [Workflow syntax reference](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [GitHub Actions security](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
