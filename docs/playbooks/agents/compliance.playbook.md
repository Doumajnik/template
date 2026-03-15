+++
id = "agents/compliance"
title = "Compliance Agent Rules"
agents = ["compliance"]
technologies = ["all"]
category = "rule"
tags = ["compliance"]
version = 4
+++

### Compliance Agent Rules

- Audit all dependency licenses for compatibility with the project's chosen license.
- Flag GPL-licensed dependencies in MIT/Apache projects — these are license conflicts.
- Verify GDPR compliance: user data has consent tracking, right to deletion, data export capability.
- Check for PII handling: personal data must be encrypted at rest and in transit.
- Verify data retention policies are implemented — data must be automatically purged after the retention period.
- Check cookie consent: track only after explicit consent, provide opt-out, document which cookies are used.
- Verify audit logging for sensitive operations: authentication, data access, permission changes.
- Check for proper data classification: public, internal, confidential, restricted.
- Verify access controls follow principle of least privilege — users/services get only the permissions they need.
- Produce a compliance report with: requirement, status (compliant/non-compliant), evidence, remediation steps.
- Flag any third-party data sharing that might require a Data Processing Agreement (DPA).
- Check that privacy policy and terms of service are accessible and up to date.
- Verify Data Protection Impact Assessments (DPIAs) are conducted before high-risk data processing activities begin.
- Check that a data breach notification process exists — authorities must be notified within 72 hours of awareness, and affected data subjects without undue delay.
- Require SPDX license identifiers (`SPDX-License-Identifier:`) in all source file headers for machine-readable license tracking and automated compliance scanning.
- Verify data processing records (GDPR Article 30) are maintained, up to date, and available for regulator inspection on request.
- Check that cross-border data transfers comply with adequacy decisions, Standard Contractual Clauses (SCCs), or Binding Corporate Rules — never transfer personal data to non-adequate jurisdictions without safeguards.
- Verify personal data is pseudonymized or anonymized wherever possible to minimize exposure in the event of a breach.
- Check that a Data Protection Officer (DPO) is appointed when required by the scale or sensitivity of data processing, and that the DPO has direct reporting access to senior management.
- Require DPIAs to document all six GDPR Article 35 elements: systematic description of processing, purpose and legitimate interest, necessity and proportionality assessment, risk assessment, planned safeguards, and evidence of DPO consultation.
- Conduct DPIAs before processing begins — start during the planning and design phase, not after implementation; the assessment must inform design decisions, not just rubber-stamp them.
- Require DPIA for any processing involving new technologies, systematic monitoring of public areas, large-scale profiling, children's data, or automated decisions with legal effects — when in doubt, conduct the DPIA anyway to minimize liability.
- Maintain a standardized DPIA template (based on ICO or supervisory authority guidance) in the project's compliance documentation for consistent risk assessment across all data processing activities.
- Implement a data breach response plan with defined roles: detection team, assessment lead, 72-hour authority notification timeline, data subject notification criteria, root cause analysis, and mandatory post-incident review process.
- Require signed Data Processing Agreements (DPAs) with all third-party processors before any data sharing begins — agreements must specify processing purpose, data categories, security measures, sub-processor rules, and audit rights.
- Implement granular consent management: separate consent per processing purpose, record consent timestamps and scope, provide easy withdrawal mechanisms, and re-obtain consent when processing purposes change.
