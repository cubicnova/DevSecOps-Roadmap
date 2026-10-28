# Jenkins Agents and Executors — Practical Exercises

Use a lab controller and machines you are authorized to administer. Avoid exposing agent ports or granting privileged access to untrusted builds.

## Lab 1: Understand the node model

Tasks:
1. Open **Manage Jenkins → Nodes**.
2. Identify the built-in node and any configured agents.
3. Record node name, labels, online/offline state, and executor count.
4. Explain the difference between a node, agent, and executor.

**Deliverable:** A node inventory table.

## Lab 2: Configure a permanent agent

Tasks:
1. Prepare a second lab VM or host with a supported Java runtime and required build tools.
2. Create a restricted service account for Jenkins builds.
3. In Jenkins, create a permanent node with a unique name and remote root directory.
4. Assign labels such as `linux` and `python`.
5. Configure a supported connection method, such as SSH or an inbound agent, following the current UI instructions.
6. Connect the agent and confirm it is online.

**Deliverable:** Agent configuration summary without passwords, tokens, or private keys.

## Lab 3: Run a Pipeline on a labelled agent

Create a Pipeline that uses `agent { label 'linux' }` and prints hostname, username, and OS details.

Tasks:
1. Run the Pipeline.
2. Confirm the commands executed on the agent, not the controller.
3. Change the label to a label that does not exist in the lab.
4. Observe the queue behavior, then restore a valid label.

**Deliverable:** Jenkinsfile and notes explaining label scheduling.

## Lab 4: Configure multiple labels

Tasks:
1. Add two labels to an agent, such as `linux` and `python`.
2. Run a Pipeline with `label 'linux && python'`.
3. Change the expression to require a nonexistent label.
4. Explain why the job remains queued or cannot be scheduled.

**Deliverable:** Two runs with the outcomes explained.

## Lab 5: Run stages on different agents

If you have both Linux and Windows agents, use `agent none` and stage-level agents to run one stage on each OS.

Tasks:
1. Add a Linux stage using `sh`.
2. Add a Windows stage using `bat`.
3. Verify the node assigned to each stage.
4. If only one OS is available, document the missing prerequisite and complete the Linux-only variation.

**Deliverable:** Jenkinsfile and stage results.

## Lab 6: Executor and queue experiment

Tasks:
1. Record the executor count for an agent.
2. Create a harmless Pipeline step that sleeps for a short period (for example, `sleep 20` in a shell step).
3. Start several builds close together.
4. Observe which builds run and which remain queued.
5. Repeat after changing the executor count in the lab.
6. Compare results and discuss CPU/RAM constraints.

**Deliverable:** A short experiment table. Restore a sensible executor count afterward.

## Lab 7: Diagnose an offline agent

Scenario: A job requiring `linux` is queued because its agent is offline.

Tasks:
1. Open the node's status and log.
2. Check host availability and network connectivity.
3. Verify the configured connection method and credentials.
4. Check the agent Java/runtime and recent host resource issues.
5. Restore the connection and rerun the job.

**Deliverable:** Root cause and validation evidence.

## Lab 8: Diagnose a missing tool

Scenario: A Pipeline fails with `python3: not found` on an agent that has the `python` label.

Tasks:
1. Check the actual agent selected.
2. Run `command -v python3` and inspect PATH in the job environment.
3. Confirm whether Python is installed for the agent's OS and service account.
4. Install/configure the tool or correct the label.
5. Re-run the Pipeline.

**Deliverable:** Root-cause note and corrected agent setup.

## Lab 9: Security and isolation review

Tasks:
1. Check whether the built-in controller node runs jobs.
2. Review agent service account privileges.
3. Identify which jobs can use sensitive deployment labels.
4. Review Docker access and workspace sharing risks.
5. Propose an isolation approach for untrusted pull requests.

**Deliverable:** Five findings and recommended mitigations.

## Lab 10: Capacity plan

Scenario: Ten builds frequently queue. The current setup has one agent with two executors, and each build is CPU- and memory-intensive.

Tasks:
1. Explain why increasing executors may worsen contention.
2. Gather approximate CPU, RAM, disk I/O, and build-duration data.
3. Propose a capacity change, such as another agent or lower concurrency.
4. Explain how labels can direct workloads to appropriate hardware.
5. Define metrics to monitor after the change.

**Deliverable:** A one-page capacity proposal.

## Lab 11: Restrict deployment work

Tasks:
1. Create or identify a `test-deploy` label on a lab-only agent.
2. Configure a Pipeline stage to use that label.
3. Explain why label assignment must be paired with Jenkins authorization, restricted credentials, and target-environment protections.
4. Confirm that the deployment step cannot accidentally run on a generic agent.

**Deliverable:** Jenkinsfile and security explanation.

## Lab 12: Final agent acceptance test

Check each item:

- [ ] Agent is online
- [ ] Node name and labels are documented
- [ ] Required Java/runtime is supported
- [ ] Build tools are available to the service account
- [ ] Pipeline selects the expected agent
- [ ] Executor count is justified by workload
- [ ] Controller is not used for normal builds where practical
- [ ] Service account has least privilege
- [ ] Sensitive workloads are isolated
- [ ] Offline and queue troubleshooting steps are documented

**Deliverable:** Completed checklist and unresolved issues.

## Assessment rubric

| Criterion | Points |
|---|---:|
| Node/agent/executor concepts | 15 |
| Agent setup and connection | 20 |
| Labels and Pipeline scheduling | 20 |
| Executor/capacity analysis | 15 |
| Troubleshooting | 15 |
| Security and isolation | 15 |
| **Total** | **100** |
