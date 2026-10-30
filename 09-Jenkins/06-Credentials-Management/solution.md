# Solutions and Guidance: Jenkins Credentials Management

Use these as reference answers with dummy credentials only. Jenkins menu names and available types vary by version and plugins.

## Lab 1: Credential types

| Type | Example | Key concern |
|---|---|---|
| Secret text | API token | Do not echo or interpolate |
| Username/password | Registry login | Avoid process arguments and shell history |
| Secret file | Protected config | Avoid workspace exposure and artifacts |
| SSH private key | Git or SSH deployment | Protect temporary key and verify host identity |

## Lab 2: Create secret text
Create a dummy secret-text credential with ID `demo-api-token` and a descriptive purpose. Store it at the narrowest practical scope. The Jenkinsfile references the ID, never the value.

## Lab 3: Safe binding

```groovy
withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
    sh '''
        set +x
        : "${API_TOKEN:?API_TOKEN is required}"
        ./scripts/call-service.sh
    '''
}
```

The script should consume the variable without printing it. Masking is best-effort, not a security boundary.

## Lab 4: Username/password

```groovy
withCredentials([usernamePassword(
    credentialsId: 'demo-registry-login',
    usernameVariable: 'REGISTRY_USER',
    passwordVariable: 'REGISTRY_PASSWORD'
)]) {
    sh '''
        set +x
        ./scripts/registry-login.sh
    '''
}
```

Use a secure login mechanism and remove temporary auth files. Never archive authentication configuration.

## Lab 5: SSH private key

```groovy
withCredentials([sshUserPrivateKey(
    credentialsId: 'deploy-ssh-key',
    keyFileVariable: 'SSH_KEY_FILE',
    usernameVariable: 'SSH_USER'
)]) {
    sh '''
        set +x
        ssh -i "$SSH_KEY_FILE" \
          -o BatchMode=yes \
          -o StrictHostKeyChecking=yes \
          "$SSH_USER@staging.example.invalid" \
          'echo connection-check'
    '''
}
```

Replace the reserved hostname with a controlled lab host. Configure trusted host keys and do not disable verification.

## Lab 6: Secret file

```groovy
withCredentials([file(credentialsId: 'demo-config-file', variable: 'CONFIG_FILE')]) {
    sh '''
        set +x
        ./scripts/use-config.sh "$CONFIG_FILE"
    '''
}
```

Do not print or copy the file. Be careful with `dir` placement: a secret file bound from inside a workspace subdirectory may land in a browsable temporary workspace path.

## Lab 7: Scope
Prefer folder or item-level credentials for a token used by one project, where supported. Controller/global credentials may be available to many pipelines. Grant access only to the users and jobs that need it.

## Lab 8: Unsafe interpolation
Unsafe code interpolates `${API_TOKEN}` in Groovy before the shell runs. Safer approach:

```groovy
withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
    sh '''
        set +x
        ./scripts/call-service.sh
    '''
}
```

The script reads the token from the environment. Other leak paths include debug logs, process environments visible to same-account processes, workspace files, artifacts, crash dumps, and verbose client diagnostics.

## Lab 9: Rotation and revocation
1. Identify owner, purpose, scope, and dependent jobs.
2. Rotate the credential at the target service.
3. Update the Jenkins entry and run a safe validation.
4. Revoke the old value at the source service.
5. Check dependent jobs and remove copies from scripts, logs, and artifacts.
6. Record the change and next review date.

Changing the Jenkins entry does not automatically invalidate an old token at the external service.

## Lab 10: Exposure response
1. Stop or isolate the job if exposure may continue.
2. Revoke or rotate the credential if exposure is plausible.
3. Restrict access to logs and artifacts while preserving evidence under approved procedures.
4. Identify other jobs using the same credential.
5. Review audit records and the cause.
6. Fix unsafe logging and test with a dummy secret.
7. Document lessons learned.

Deleting a log line alone is not sufficient if the credential remains valid or has been copied.

## Lab 11: Agent isolation
Jobs running as the same OS user may be able to inspect environment variables or temporary files from concurrent builds. Do not run untrusted pull-request code on agents that handle deployment secrets. Use isolated or ephemeral agents and restrict job configuration permissions.

## Lab 12: Mini-project outline

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps { sh './build.sh' }
        }
        stage('Test') {
            steps { sh './test.sh' }
        }
        stage('Publish') {
            steps {
                withCredentials([string(credentialsId: 'artifact-publish-token', variable: 'PUBLISH_TOKEN')]) {
                    sh '''
                        set +x
                        ./scripts/publish.sh
                    '''
                }
            }
        }
    }
    post {
        always {
            echo 'Pipeline completed. Review result without exposing credentials.'
        }
    }
}
```

Ensure `publish.sh` consumes `PUBLISH_TOKEN` from the environment without logging it. Restrict the job to trusted branches and authorized users.

## Security checklist
- [ ] Secrets are stored in Jenkins Credentials, not source control.
- [ ] Scope is as narrow as possible.
- [ ] Only authorized people can create, update, or use credentials.
- [ ] Secret variables are not printed or interpolated into Groovy strings.
- [ ] Shell tracing and verbose output are disabled where appropriate.
- [ ] Untrusted jobs do not share privileged agents.
- [ ] Secret files are kept out of artifacts.
- [ ] Credentials have owners and rotation/revocation procedures.
- [ ] Logs, backups, and artifacts are protected.
- [ ] An exposure response plan exists.

## Official references
- [Jenkins Credentials](https://www.jenkins.io/doc/book/security/credentials/)
- [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- [Credentials Binding step reference](https://www.jenkins.io/doc/pipeline/steps/credentials-binding/)
