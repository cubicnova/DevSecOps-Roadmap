# Practical Exercises: Jenkins RBAC and Authorization

Use a test Jenkins instance. Do not experiment with controller security changes on a production system without a tested recovery plan.

## Lab 1: Authentication vs authorization
Explain the difference between authentication and authorization. Give one Jenkins example of each and describe how an LDAP/Active Directory security realm relates to authorization.

## Lab 2: Inventory permissions
List users/groups, jobs, folders, agents, credentials, and sensitive controller operations in your lab. Identify which resources need restricted access.

## Lab 3: Design roles
Design roles for administrators, developers, release managers, auditors, and agent operators. For each role, list required capabilities and permissions that should be excluded.

## Lab 4: Build a permission matrix
Create a matrix with roles as rows and permissions as columns. Include read, build, configure, delete, credential use/management, agent management, and controller administration where available. Justify each grant.

## Lab 5: Explore Matrix-based Security
In a test instance with the Matrix Authorization Strategy plugin, configure a small set of permissions for test identities. Test read/build access and confirm that ungranted actions are denied.

## Lab 6: Explore Role-based Authorization Strategy
If installed, create global and item roles for a development folder and a release job. Assign roles to test users/groups. Document plugin and version prerequisites.

## Lab 7: Test item-role regular expressions
Create a role pattern for a team folder and test it against intended and unintended job names. Include cases for similarly named folders and production jobs. Record which items match.

## Lab 8: Review permission inheritance
Compare global, parent-folder, and item-level grants. Determine whether permissions are inherited, additive, or overridden according to the chosen strategy. Explain why a local restriction may not remove a broader inherited grant.

## Lab 9: Test least privilege
Log in as a developer, release manager, and auditor using separate test accounts. Verify allowed and denied actions. Do not use an administrator account to infer what a limited user can do.

## Lab 10: Analyze a privilege escalation path
A developer can configure a job that has access to a deployment token. Explain how changing the job definition could expose or misuse the token. Propose mitigations involving job configuration permissions, credential scope, branch trust, and agent isolation.

## Lab 11: Change and recovery plan
Write a change plan for adjusting Jenkins authorization. Include a backup/recovery path, test identities, pre-change permission export or documentation, validation steps, rollback criteria, and a named approver role.

## Lab 12: Final mini-project
Implement a least-privilege access design in a disposable Jenkins environment.

**Deliverables**
- Role and permission matrix
- Screenshot or text record of the configured authorization strategy
- Access test results for allowed and denied actions
- Item-role pattern tests, if applicable
- Recovery/rollback plan
- Security review identifying residual risks
