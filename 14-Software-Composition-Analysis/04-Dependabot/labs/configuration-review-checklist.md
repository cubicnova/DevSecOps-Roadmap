# Dependabot Configuration Review Checklist

- [ ] File is `.github/dependabot.yml` on the default branch
- [ ] `version: 2` is present
- [ ] Every ecosystem identifier is supported
- [ ] Each directory contains the relevant manifest
- [ ] Monorepo directories are complete and accurate
- [ ] Schedule is appropriate
- [ ] PR limit will not block urgent work
- [ ] Groups are ordered and scoped intentionally
- [ ] Ignore rules have rationale and review dates
- [ ] Cooldown is understood to apply to version updates, not security updates
- [ ] Private registry credentials use secrets and least privilege
- [ ] Security updates and alerts are enabled in repository settings
- [ ] Update PRs require appropriate tests and review
