# Practical Exercises: Jenkinsfile

Perform these exercises in a test Jenkins instance and a non-production repository. Do not use production credentials in training jobs.

## Lab 1: Create your first Jenkinsfile

Write a Declarative Pipeline with `Build`, `Test`, and `Package` stages.

**Tasks**
1. Add an `agent` directive.
2. Give each stage a descriptive name.
3. Add a `post` section that always reports completion.

**Deliverable:** a root-level `Jenkinsfile`.

## Lab 2: Add real validation commands

Use a small Python repository.

**Tasks**
- Check the Python version.
- Run `python3 -m compileall -q .`.
- Run `python3 -m unittest discover -s tests`.
- Confirm a failing test causes the pipeline to fail.

## Lab 3: Add parameters

Create a `TARGET_ENV` choice parameter with `dev` and `staging` values.

**Tasks**
1. Display the selected environment.
2. Add a Boolean parameter for an optional quality check.
3. Explain why parameters alone must not authorize production deployment.

## Lab 4: Use `when`

Add a stage that runs only for the `main` branch in a multibranch Pipeline.

**Questions**
- What happens when the condition is false?
- What must be true about the Jenkins job type for the branch condition to work as expected?

## Lab 5: Handle test reports

Configure the test stage to produce JUnit XML reports and publish them with the `junit` step.

**Tasks**
- Confirm reports appear in the Jenkins build.
- Decide whether missing reports should fail the pipeline.
- Document the plugin prerequisite.

## Lab 6: Use Jenkins Credentials

Create a dummy secret credential in a lab Jenkins instance.

**Tasks**
1. Bind it using `withCredentials`.
2. Pass it to a script through an environment variable.
3. Do not print the secret.
4. Explain why Groovy interpolation of a secret in a double-quoted shell command is risky.

## Lab 7: Add timeouts and concurrency protection

Add a global timeout and `disableConcurrentBuilds()`.

**Tasks**
- Run a deliberately slow command in a test branch.
- Observe timeout behavior.
- Explain when concurrent builds should be allowed instead.

## Lab 8: Create a staging gate

Create a staging deployment stage that runs only on the intended branch and requires appropriate approval or job-level access controls.

**Deliverable:** Jenkinsfile excerpt plus a description of Jenkins authorization and credential scope.

## Lab 9: Declarative vs Scripted

Rewrite a small two-stage pipeline in Scripted syntax.

**Tasks**
- Compare readability.
- Identify a case where Groovy control flow could be useful.
- Explain why Declarative is a good default for conventional pipelines.

## Lab 10: Diagnose failures

For each case, identify a likely cause and a debugging step:

1. Jenkins reports a syntax error before any stage runs.
2. `sh` fails because a command is missing.
3. Tests fail locally but pass in Jenkins.
4. The `junit` step is unknown.
5. A branch-specific stage never runs.
6. A build hangs indefinitely.

## Lab 11: Pipeline security review

Review a Jenkinsfile for:
- Hardcoded credentials
- Secret interpolation in shell strings
- Overly broad deployment access
- Untrusted code running on a privileged agent
- Unnecessary plugins or permissions
- Missing timeout and cleanup behavior

**Deliverable:** a risk register with finding, impact, and remediation.

## Lab 12: Final mini-project

Create a pipeline with these stages:

1. Checkout
2. Static validation
3. Unit tests
4. Package
5. Archive artifact
6. Optional staging deployment
7. Post-build reporting and cleanup

**Acceptance criteria**
- Pipeline is committed to source control.
- Required tests block packaging or deployment when they fail.
- Artifact paths are explicit.
- Secrets are stored in Jenkins Credentials.
- Deployment is restricted to the intended branch and authorized users.
- README notes required tools and plugins.
