# Practical Exercises: Declarative Pipelines

Use a non-production Jenkins instance and a training repository. Do not use production credentials in these exercises.

## Lab 1: Build a basic pipeline

Create a Jenkinsfile with `Checkout`, `Build`, and `Test` stages.

**Tasks**
1. Use Declarative syntax.
2. Give each stage a meaningful name.
3. Add a top-level `post` section.
4. Run the job and inspect the Stage View or Pipeline view.

**Deliverable:** a committed Jenkinsfile.

## Lab 2: Add pipeline options

Configure a timeout, timestamps, build retention, and concurrency behavior.

**Questions**
- Why might `disableConcurrentBuilds()` be useful?
- When could it reduce throughput unnecessarily?
- Which options depend on plugins?

## Lab 3: Use parameters and environment variables

Add a choice parameter for `dev` or `staging`, plus a Boolean parameter for optional checks.

**Acceptance criteria**
- Parameter values are displayed in the build log without exposing secrets.
- Optional checks run only when enabled.
- You explain why a parameter cannot authorize a deployment by itself.

## Lab 4: Use `when`

Create a stage that runs only on `main` in a multibranch Pipeline.

**Tasks**
1. Test on `main`.
2. Test on a feature branch.
3. Document why the stage is skipped on the feature branch.
4. Describe a separate control that prevents unauthorized deployments.

## Lab 5: Use stage-level agents

Create separate validation stages for agents labeled `linux` and `windows`.

**Tasks**
- Run a platform-specific command on each agent.
- Explain why `agent none` can avoid holding an executor for the entire pipeline.
- Document what happens if no agent with a required label is available.

## Lab 6: Parallel execution

Run unit tests and API tests in parallel.

**Tasks**
1. Make sure the branches do not overwrite shared outputs.
2. Compare elapsed time with sequential execution.
3. Explain when parallel execution can make tests flaky.

## Lab 7: Matrix testing

Create a matrix over two runtime versions or two configuration values.

**Tasks**
- Define the axis and values.
- Ensure each cell really uses its intended runtime/configuration.
- Record which cells fail and why.

## Lab 8: Add approval before staging

Add an `input` step before a staging deployment.

**Tasks**
- Restrict the allowed submitters.
- Confirm that only authorized users can start the job.
- Explain why job permissions and credential scope remain necessary.

## Lab 9: Use credentials safely

Create a dummy Jenkins secret-text credential and bind it with `withCredentials`.

**Tasks**
- Pass the secret to a script through the environment.
- Never print the value.
- Inspect logs and workspace outputs for accidental exposure.
- Explain why masking alone is not a complete security control.

## Lab 10: Publish test reports

Configure the test tool to generate JUnit XML and publish it using `junit`.

**Tasks**
- Confirm test results are visible in Jenkins.
- Decide whether missing reports should fail the build.
- Identify the required plugin.

## Lab 11: Troubleshoot a pipeline

Investigate these scenarios and document the likely cause and next check:

1. Jenkins reports a Declarative syntax error.
2. A `when { branch 'main' }` stage is always skipped.
3. A matrix cell reports the wrong runtime version.
4. A parallel test stage fails intermittently.
5. The `junit` step is unknown.
6. The pipeline waits indefinitely for an agent or approval.

## Lab 12: Final mini-project

Build a Declarative Pipeline containing:

1. Checkout
2. Static validation
3. Parallel unit and API tests
4. Package creation
5. Artifact archival
6. Conditional staging stage
7. Approval and protected deployment controls
8. Post-build reporting and cleanup

**Deliverables**
- `Jenkinsfile`
- Short README listing tools, plugins, parameters, and assumptions
- Pipeline security checklist
- Evidence of a successful run and a deliberately failed test run
