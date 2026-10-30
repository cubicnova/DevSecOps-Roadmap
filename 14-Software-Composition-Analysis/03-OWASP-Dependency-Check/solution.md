# Solutions and Instructor Guidance

Results vary by project, Dependency-Check release, analyzers, and vulnerability-data snapshot.

## Lab 1
Record the exact Dependency-Check and Java versions. Use a currently supported release and consult its release notes before upgrades. Current project guidance notes Java 11 minimum for 11+ and mandatory upgrade to 12.1.0+ due to NVD API compatibility changes; validate the latest status at lab time.

## Lab 2
A useful report includes project identifier, scan date, scanner version, data-source/update status, dependency evidence, CPE/CVE mapping, severity, and report format. If few dependencies are identified, verify the scan path, manifest/lockfile presence, required ecosystem tools, and analyzer support.

## Lab 3
The key should be injected at runtime from a secret store/environment variable. Do not store it in POM, YAML, shell history, or logs. A shared key can be rate-limited by concurrent builds; coordinate updates and cache data safely.

## Lab 4
Use a current plugin release and confirm its configuration parameters from that version's official documentation. A threshold such as CVSS 7.0 is an example policy only, not a universal security standard. Decide whether the build should fail based on severity, applicability, exposure, and exception workflow.

## Lab 5
A defensible false-positive decision documents:
- exact package coordinates and resolved version;
- evidence collected by the analyzer and CPE mapping;
- authoritative package/vendor identity evidence;
- why the CVE does not apply to this version/product;
- narrow suppression rule and review date;
- re-scan evidence.

Suppression must not become a substitute for remediation.

## Lab 6
Use least privilege, immutable action SHAs, protected secrets, safe cache strategy, artifact access controls, and explicit policy. Do not expose NVD credentials to untrusted fork code.

## Lab 7
For slow updates, check initial database population, network access, proxy, API key, and cache. For 403 errors, inspect key validity and concurrent requests. For migration problems, follow the official version-specific purge/migration instructions and back up relevant data first.

## Assessment rubric
- Correct installation and version awareness: 15%
- Reproducible scan and report interpretation: 20%
- Secure NVD key handling and cache design: 15%
- Evidence-based triage and narrow suppression: 20%
- Secure CI/CD integration: 20%
- Clear documentation: 10%
