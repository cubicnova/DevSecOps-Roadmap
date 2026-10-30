# Jenkins Credentials Management

Jenkins Credentials stores authentication material so pipelines can reference credential IDs instead of hardcoding secrets. Credentials commonly provide access to source control, artifact registries, cloud services, deployment targets, and internal APIs.

## Learning objectives
- Identify common Jenkins credential types and scopes.
- Create credentials and reference them by ID.
- Bind secrets in Declarative Pipelines with `withCredentials`.
- Reduce secret exposure in logs, process arguments, workspaces, and agents.
- Apply least privilege, rotation, and access-review practices.

## Common credential types

| Type | Typical use |
|---|---|
| Secret text | API token or service token |
| Username with password | Registry, database, or service authentication |
| Secret file | Protected configuration or certificate bundle |
| SSH username with private key | Git over SSH or SSH-based deployment |
| Certificate | Certificate-based authentication |

Available types depend on installed plugins and Jenkins configuration.

## Scope and access
Credentials may be available at controller/global, folder, or item/job scope depending on configuration. Prefer the narrowest scope that works. Start with no access and grant only the users and jobs that require it. Restrict who can create, update, and consume credentials.

## Create and use a credential
1. Open **Manage Jenkins → Credentials** or the appropriate folder/job credential store.
2. Select the relevant store and domain.
3. Add the needed credential type and a descriptive ID, such as `demo-api-token`.
4. Reference the ID in a pipeline; never put the secret value in source control.
5. Test with dummy credentials and inspect logs and artifacts for exposure.

Menu labels vary by Jenkins version, permissions, and plugins.

## Example: secret text in Declarative Pipeline

Create a secret-text credential with ID `demo-api-token` first.

```groovy
pipeline {
    agent any
    stages {
        stage('Call Service') {
            steps {
                withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
                    sh '''
                        set +x
                        ./scripts/call-service.sh
                    '''
                }
            }
        }
    }
}
```

The script should read `API_TOKEN` from its environment. Do not echo the value or interpolate it into a Groovy double-quoted shell command.

## Security principles
1. Never hardcode secrets in Jenkinsfiles, repositories, images, or scripts.
2. Use service accounts and tokens with minimum required permissions.
3. Limit credential scope and restrict who can modify pipeline steps.
4. Avoid `echo`, shell tracing (`set -x`), debug dumps, and verbose output that could reveal secrets.
5. Prefer single-quoted Groovy shell strings so the shell expands secret environment variables.
6. Isolate jobs that handle secrets. Processes running under the same OS account may be able to inspect other processes' environments.
7. Keep secret files out of workspaces and artifacts.
8. Establish ownership, rotation, expiry, and revocation procedures.
9. Review access and audit credential usage.
10. Protect Jenkins controller data and recovery material.

Masking is a useful guardrail, not a guarantee. Anyone who can modify pipeline steps that receive a secret may be able to exfiltrate it.

## Troubleshooting
- **Credential ID not found:** check spelling, scope, domain, permissions, and type.
- **Binding step unavailable:** verify the Credentials Binding plugin.
- **Authentication fails:** check token expiry, permissions, endpoint, and expected format.
- **Secret appears in logs:** restrict access, rotate if exposure is plausible, and investigate.
- **Secret file appears in workspace:** review binding and `dir` placement; remove exposed copies and rotate affected secrets.

## Official documentation
- [Jenkins Credentials](https://www.jenkins.io/doc/book/security/credentials/)
- [Using credentials](https://www.jenkins.io/doc/book/using/using-credentials/)
- [Credentials Binding Plugin](https://www.jenkins.io/doc/pipeline/steps/credentials-binding/)
