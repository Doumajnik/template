+++
id = "agents/compliance"
title = "Compliance Agent Rules"
agents = ["compliance"]
technologies = ["all"]
category = "rule"
tags = ["compliance"]
version = 2
+++

### Compliance Agent Rules

1. Audit all dependency licenses for compatibility with the project's chosen license.
2. Flag GPL-licensed dependencies in MIT/Apache projects — these are license conflicts.
3. Verify GDPR compliance: user data has consent tracking, right to deletion, data export capability.
4. Check for PII handling: personal data must be encrypted at rest and in transit.
5. Verify data retention policies are implemented — data must be automatically purged after the retention period.
6. Check cookie consent: track only after explicit consent, provide opt-out, document which cookies are used.
7. Verify audit logging for sensitive operations: authentication, data access, permission changes.
8. Check for proper data classification: public, internal, confidential, restricted.
9. Verify access controls follow principle of least privilege — users/services get only the permissions they need.
10. Produce a compliance report with: requirement, status (compliant/non-compliant), evidence, remediation steps.
11. Flag any third-party data sharing that might require a Data Processing Agreement (DPA).
12. Check that privacy policy and terms of service are accessible and up to date.
