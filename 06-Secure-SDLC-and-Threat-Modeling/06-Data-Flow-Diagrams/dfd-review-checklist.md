# DFD Security Review Checklist

## Scope and ownership
- [ ] Diagram title, owner, version, and review date are recorded.
- [ ] The modeled feature and system boundary are explicit.
- [ ] The diagram is at a useful level of detail.
- [ ] Assumptions, exclusions, and unresolved questions are documented.

## Elements
- [ ] External entities are shown and named.
- [ ] Processes that transform or route data are shown.
- [ ] Data stores, including relevant queues, logs, files, and backups, are shown.
- [ ] Every important data flow has an arrow and direction.
- [ ] Flow IDs are unique and stable.
- [ ] The notation is consistent and explained where needed.

## Flow labels
- [ ] Purpose and data types are described.
- [ ] Protocols and encryption in transit are identified.
- [ ] Sensitive data classification is recorded.
- [ ] Authentication and authorization expectations are noted.
- [ ] Validation, encoding, and integrity checks are considered.
- [ ] Error, retry, and asynchronous paths are included where relevant.

## Trust boundaries
- [ ] Public/private and third-party boundaries are explicit.
- [ ] Service-to-service and privilege boundaries are considered.
- [ ] Data crossing boundaries is treated according to its trust level.
- [ ] Administrative and privileged flows are represented.
- [ ] Data residency or privacy constraints are noted when applicable.

## Security and privacy
- [ ] Threats are linked to specific elements or flows.
- [ ] STRIDE or another appropriate method has been applied where useful.
- [ ] Data minimization and retention are considered.
- [ ] Secrets, credentials, and tokens are not exposed in logs or diagrams.
- [ ] Stores have access-control, backup, and deletion considerations.
- [ ] Monitoring and audit requirements are identified.
- [ ] Third-party assumptions and dependencies are recorded.

## Maintenance
- [ ] Diagram matches the current architecture.
- [ ] Review findings have owners and due dates.
- [ ] Material architecture changes trigger an update.
- [ ] Diagram source is stored where the team can maintain it.
