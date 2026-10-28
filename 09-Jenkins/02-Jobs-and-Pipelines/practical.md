# Jenkins Jobs and Pipelines — Practical Exercises

Use a lab Jenkins controller and a non-production repository. Do not use real production credentials or deploy to production during these exercises.

## Lab 1: Create a Freestyle job

Tasks:
1. Create a Freestyle project named `freestyle-intro`.
2. Add a shell build step that prints a greeting, build number, and current directory.
3. Run the job twice.
4. Compare the console logs and build numbers.

**Deliverable:** Screenshot or notes showing two successful builds.

## Lab 2: Create a simple Pipeline

Tasks:
1. Create a Pipeline job named `pipeline-intro`.
2. Paste a Declarative Pipeline with `Build` and `Test` stages.
3. Use `echo` in each stage.
4. Run the Pipeline and inspect stage results.

**Deliverable:** A successful build log and a short explanation of each stage.

## Lab 3: Use shell commands safely

Tasks:
1. Add a stage that runs `pwd`, `whoami`, and `uname -a`.
2. Confirm the assigned agent is Linux.
3. If your agent is Windows, replace shell steps with appropriate Windows commands.
4. Explain why shell syntax is agent-specific.

**Deliverable:** Jenkinsfile and console output.

## Lab 4: Add environment variables

Tasks:
1. Define `APP_NAME` and `BUILD_LABEL` in the Pipeline `environment` block.
2. Print both non-sensitive values.
3. Add a stage-specific variable.
4. Explain the difference between pipeline-level and stage-level environment variables.

**Deliverable:** Updated Jenkinsfile.

## Lab 5: Add parameters

Tasks:
1. Add a choice parameter named `TARGET_ENV` with values `dev` and `staging`.
2. Add a boolean parameter named `RUN_LINT`.
3. Display the selected target.
4. Use a `when` expression to skip the lint stage when `RUN_LINT` is false.
5. Explain why parameters should be validated before they influence shell commands.

**Deliverable:** Parameterized Pipeline and results for both boolean values.

## Lab 6: Archive an artifact

Tasks:
1. Create a `dist/` directory in a build step.
2. Write a small text file into it.
3. Archive `dist/**` using `archiveArtifacts`.
4. Download or inspect the archived file from the build page.
5. Explain the difference between a workspace file and an archived artifact.

**Deliverable:** Pipeline and archived artifact.

## Lab 7: Configure Pipeline from SCM

Tasks:
1. Add a `Jenkinsfile` to the root of a test Git repository.
2. Commit and push it.
3. Create a Pipeline job configured as **Pipeline script from SCM**.
4. Configure repository URL, branch, and script path.
5. Run the job and verify it uses the committed file.
6. Change a harmless echo message, commit, and rebuild.

**Deliverable:** Repository commit IDs and successful build result.

## Lab 8: Use a credential safely

Tasks:
1. Create a dummy secret text credential in a lab Jenkins instance.
2. Reference it by credential ID with `withCredentials`.
3. Check only whether the value is present; do not print the value.
4. Confirm no secret is committed to source control.
5. Explain why credentials should be scoped to the smallest practical set of jobs.

**Deliverable:** Safe Jenkinsfile snippet and security note.

## Lab 9: Add post actions and timeout

Tasks:
1. Add `timestamps()` and a five-minute timeout.
2. Add `post` actions for `success`, `failure`, and `always`.
3. Make a temporary test step fail in a disposable branch.
4. Confirm the failure message appears.
5. Revert the intentional failure.

**Deliverable:** Build logs demonstrating success and failure handling.

## Lab 10: Troubleshoot a broken Pipeline

Start with this incorrect Jenkinsfile:

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Build started'
            }
        }
        stage('Test') {
            steps {
                sh 'test -f missing-file.txt'
            }
        }
    }
}
```

Tasks:
1. Run the Pipeline and locate the first failing step.
2. Explain why the test command fails.
3. Fix the issue by creating the expected test file or changing the test to check a file that exists.
4. Rerun and verify success.
5. Explain why changing the test to `true` without understanding the requirement would be a poor fix.

**Deliverable:** Root-cause note and corrected Jenkinsfile.

## Lab 11: Freestyle versus Pipeline comparison

Create one small job using each approach.

Compare:
- Where the configuration is stored.
- How changes are reviewed.
- How multiple stages are represented.
- How portable the definition is.
- Which approach you would choose for a team project and why.

**Deliverable:** A comparison table.

## Lab 12: Mini CI pipeline

Create a Pipeline with these stages:
1. Checkout (when using SCM configuration).
2. Build: create a harmless file in `dist/`.
3. Test: verify the file exists and is non-empty.
4. Archive: archive the file.
5. Post: print success or failure status.

Requirements:
- Use descriptive stage names.
- Use a timeout.
- Do not include secrets.
- Confirm the artifact is available from the build page.

**Deliverable:** A complete `Jenkinsfile` and a successful run.

## Assessment rubric

| Criterion | Points |
|---|---:|
| Freestyle and Pipeline job setup | 15 |
| Correct Declarative Pipeline syntax | 20 |
| Parameters and environment variables | 15 |
| Artifact and SCM integration | 20 |
| Troubleshooting and validation | 15 |
| Credential safety and documentation | 15 |
| **Total** | **100** |
