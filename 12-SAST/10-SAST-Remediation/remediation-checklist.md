# SAST Remediation Checklist

- [ ] Read the finding and query help.
- [ ] Confirm affected branch, file, and code path.
- [ ] Trace source, transformations, and sink.
- [ ] Identify the root cause and trust boundary.
- [ ] Assess exploitability, impact, and priority.
- [ ] Select a context-appropriate secure control.
- [ ] Fix all relevant paths, not only the highlighted line.
- [ ] Add regression tests for the original weakness.
- [ ] Run unit and integration tests.
- [ ] Run SAST again using the relevant configuration.
- [ ] Review the diff for regressions and side effects.
- [ ] Document residual risk and exceptions.
- [ ] Confirm alert status on the intended branch.
