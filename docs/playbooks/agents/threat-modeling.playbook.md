+++
id = "agents/threat-modeling"
title = "Threat Modeling Agent Rules"
agents = ["threat-modeling"]
technologies = ["all"]
category = "rule"
tags = ["threat-modeling", "security", "architecture"]
version = 1
+++

### Threat Modeling Guidelines

- **Design-first, code-last.** Threat-model the architecture before any source exists. Source-level review is the Security Agent's job.
- **Use STRIDE per entry point and per trust boundary.** Spoofing / Tampering / Repudiation / Information disclosure / Denial of service / Elevation of privilege.
- **Map every finding to OWASP Top 10 + CWE.** Findings without an OWASP/CWE tag are not actionable.
- **Always pair findings with mitigations.** No mitigation = a complaint, not a threat model.
- **Findings that block the pipeline:** 🔴 CRITICAL (exploitable as designed, no mitigation), 🟡 HIGH (exploitable under realistic conditions, mitigation possible but not in the plan).
- **Findings that log but do not block:** 🟢 MEDIUM (theoretical exploit requiring chained conditions), ⚪ LOW (defence-in-depth suggestions).
- **Adversarial mindset.** For every entry point, walk through script-kiddie / state-actor / malicious-tenant / insider / confused-deputy attack scenarios.
- **Trust boundary explicit.** Every place data crosses a trust zone (Internet → service, tenant A → tenant B, anonymous → authenticated) must be enumerated.
- **Append to `docs/THREAT_MODEL.md`.** Never overwrite previous entries — threat models are auditable history.
- **Coordinate with Architect.** CRITICAL/HIGH findings go back to the Architect for plan revision; only after the Architect accepts the residual risk in writing does the pipeline advance.
- **Never invent threats without exploits.** If you cannot sketch the attack steps, the finding belongs in the "Hypothetical Risks" section, not the main findings.
- **Cover the full OWASP A01–A10 surface** at minimum — Broken Access Control, Crypto Failures, Injection, Insecure Design, Misconfiguration, Vulnerable Deps, Auth Failures, Integrity Failures, Logging Failures, SSRF.
- **Re-run on every architecture revision.** Threat models are not one-shot — they refresh with each Critic round.
