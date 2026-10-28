# Practical Exercises: Jenkins Credentials Management

Use a test Jenkins instance and dummy credentials only. Do not use production tokens, passwords, private keys, or configuration files.

## Lab 1: Explore credential types
Identify available types and compare secret text, username/password, secret file, and SSH private key. Record any plugin prerequisites.

## Lab 2: Create secret text
Create a dummy secret-text credential with ID `demo-api-token`. Add a description, choose the narrowest scope, and reference the ID without placing the value in source control.

## Lab 3: Bind a secret safely
Use `withCredentials` to bind `demo-api-token` to `API_TOKEN`.
- Disable shell tracing where relevant.
- Do not print the secret.
- Limit the binding block to the required steps.
- Fail clearly if the credential is missing.

## Lab 4: Username and password
Create `demo-registry-login`. Bind username and password separately, pass them to a lab script, avoid revealing the password in process arguments or shell history, and remove temporary auth files.

## Lab 5: SSH private key
Create a lab-only SSH credential. Bind the key to a temporary file, connect only to a controlled host, configure trusted host keys, and verify the key is not copied into artifacts.

## Lab 6: Secret file
Create a dummy secret-file credential. Use it without printing its contents. Review workspace and temporary-file locations, and explain why a workspace subdirectory can be risky.

## Lab 7: Credential scope
Compare controller/global, folder, and job/item scope where available. Recommend a scope for a staging-only token and explain why broad access increases risk.

## Lab 8: Detect unsafe interpolation
Review the code:

```groovy
withCredentials([string(credentialsId: 'demo-api-token', variable: 'API_TOKEN')]) {
    sh "curl -H 'Authorization: Bearer ${API_TOKEN}' https://service.example.invalid"
}
```

Explain the risk, rewrite it using a single-quoted Groovy string, and identify two other possible secret leak paths.

## Lab 9: Rotation and revocation
Using a dummy value, document the owner and dependent jobs, replace the value, test, invalidate the old value at the source service, and write a recovery procedure.

## Lab 10: Exposure incident response
Assume a build log exposes a credential. List containment actions, rotation/revocation decisions, log/artifact access restrictions, affected-job discovery, and prevention steps.

## Lab 11: Agent isolation
Determine whether trusted and untrusted jobs share an OS account or agent. Explain risks from environment variables and temporary files, and recommend isolation or ephemeral agents.

## Lab 12: Final mini-project
Build a pipeline that builds and tests without credentials, publishes using a scoped dummy token, cleans temporary authentication data, and reports results without exposing secrets.

**Deliverables:** `Jenkinsfile`, credential type/ID/scope/owner notes, security checklist, and evidence that logs and artifacts contain no secret.
