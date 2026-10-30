# Baseline Policy Notes

This folder is intended for reviewed, version-controlled DAST policy documentation.

## Baseline profile
- Passive checks only.
- Bounded crawl duration and scope.
- No destructive routes.
- Reports stored as restricted CI artifacts.
- No secrets committed to the repository.

## Active profile
Maintain a separate policy for explicitly approved isolated environments. Record enabled rules, threshold, strength, time limits, concurrency, exclusions, and approval.

## Change control
For every policy change, record:
- Rule ID/category and old/new state.
- Reason for enabling, disabling, or changing a rule.
- Expected impact on coverage and noise.
- Reviewer and date.
- Date for revalidation.

Do not add blanket suppressions without evidence and an owner. Revalidate policy behavior after scanner/add-on upgrades.
