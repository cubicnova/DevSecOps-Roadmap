# Jenkins Credentials Management Examples

Use dummy credentials in a test Jenkins instance. Create the IDs shown before running each example.

## Example 1: Secret text
Credential type: **Secret text**; ID: `demo-api-token`.

```groovy
pipeline {
    agent any
    stages {
        stage('Use API Token') {
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

The script reads the token from its environment. Do not print it or interpolate it into a Groovy double-quoted command.

## Example 2: Username and password
Credential ID: `demo-registry-login`.

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

Use a tool-supported login mechanism that avoids shell history, process arguments, and logs. Remove temporary auth configuration afterwards.

## Example 3: SSH private key
Credential type: **SSH Username with private key**; ID: `deploy-ssh-key`.

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

Replace the reserved example hostname with an approved lab host and configure trusted host keys. Do not disable host-key checking.

## Example 4: Secret file
Credential type: **Secret file**; ID: `demo-config-file`.

```groovy
withCredentials([file(credentialsId: 'demo-config-file', variable: 'CONFIG_FILE')]) {
    sh '''
        set +x
        ./scripts/use-config.sh "$CONFIG_FILE"
    '''
}
```

Do not print the file contents, copy it into the artifact, or place it in a browsable workspace path. Follow the Credentials Binding documentation for safe placement.

## Example 5: Username/password in one variable

```groovy
withCredentials([usernameColonPassword(
    credentialsId: 'demo-registry-login',
    variable: 'REGISTRY_AUTH'
)]) {
    sh '''
        set +x
        ./scripts/publish-artifact.sh
    '''
}
```

Use this only if the tool expects the `username:password` format. Treat the combined variable as sensitive.

## Example 6: Declarative environment binding

```groovy
pipeline {
    agent any
    environment {
        API_TOKEN = credentials('demo-api-token')
    }
    stages {
        stage('Authenticated Task') {
            steps {
                sh '''
                    set +x
                    ./scripts/call-service.sh
                '''
            }
        }
    }
}
```

Use the correct credential type and confirm supported binding behavior. A stage-scoped binding can reduce exposure compared with making a secret available to every stage.

## Example 7: Scope credentials to publishing

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh './build.sh'
            }
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
}
```

Restrict the publish job to trusted branches and authorized users.

## Example 8: Unsafe interpolation — do not use

```groovy
// UNSAFE: do not use
withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
    sh "curl -H 'Authorization: Bearer ${API_TOKEN}' https://service.example.invalid"
}
```

Groovy interpolates the secret before the shell runs. Prefer a single-quoted Groovy string and let the shell expand `$API_TOKEN` internally.

## Example 9: Placeholder script

`./scripts/call-service.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
set +x
: "${API_TOKEN:?API_TOKEN must be provided}"
# Use the token with an approved client or SDK.
# Do not print the token or enable verbose request logging.
./bin/service-client health-check
```

Adapt the placeholder command to your tool and configure that tool to consume the environment variable safely.

## Pre-run checklist
- [ ] Credential ID exists and has the expected type.
- [ ] Scope is as narrow as practical.
- [ ] Job and agent are trusted to handle the secret.
- [ ] No command echoes the secret.
- [ ] No Groovy interpolation of secret variables.
- [ ] Secret files are not copied into artifacts.
- [ ] Token permissions and rotation owner are documented.
