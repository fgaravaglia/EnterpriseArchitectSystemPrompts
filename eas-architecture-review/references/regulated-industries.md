
# Regulated Industries Overlay

Optional module. Load it when the system sits in a regulated sector (banking and payments, insurance, healthcare, critical infrastructure) or handles regulated data. It does **not** replace the base checklist and gates: it adds criteria and questions on top of them.

> **Reliability warning**: regulations and their technical standards change (delegated acts, guidelines, national transpositions). Treat everything below as a review prompt, not as legal advice. When a finding depends on the exact wording or a deadline, say so and recommend confirmation with Compliance / Legal instead of asserting it.

## Contents

1. How to use this overlay
2. EU financial sector: DORA
3. Other frameworks to check for applicability
4. Overlay criteria per quality gate
5. Review questions (fast probes)
6. Regulatory findings: how to grade them

---

## 1. How to use this overlay

1. Establish **which regimes apply** (sector, entity type, data types, geography, criticality of the service). If unknown, list it as an open question and continue with assumptions stated.
2. Map the system's **critical or important functions** and the ICT assets that support them. Most regulatory expectations attach to these.
3. Add the criteria of section 4 to the gates you are applying.
4. Grade regulatory gaps with section 6 (a regulatory gap is not automatically P0, but a gap on a critical function usually is at least P1).
5. Distinguish **architecture concerns** (what the review can judge) from **legal interpretation** (what it cannot). Hand off the latter.

## 2. EU financial sector: DORA

Digital Operational Resilience Act, Regulation (EU) 2022/2554, applicable since 17 January 2025, for most EU financial entities (banks, payment and e-money institutions, insurers, investment firms, crypto-asset service providers and others) and, through an oversight framework, for designated critical ICT third-party providers. Its five areas map cleanly to architecture review questions:

| DORA area | What an architecture review should probe |
| ----------- | ------------------------------------------ |
| **ICT risk management** (governance, asset inventory, protection, detection, response and recovery, backup, learning) | Is there an inventory of the components supporting each critical function? Are RTO/RPO defined per function and *demonstrated* by tests? Are single points of failure, dependencies and data flows documented? Is change management controlled and auditable? |
| **ICT incident management and reporting** | Can the system detect, classify and time-stamp incidents quickly enough to feed staged regulatory notifications (initial, intermediate, final)? Do logs, correlation IDs and runbooks support root-cause analysis? Who decides that an incident is "major"? |
| **Digital operational resilience testing** | Is there a testing programme beyond functional tests: vulnerability scanning, scenario-based failover tests, restore tests, and, for entities in scope, threat-led penetration testing (TLPT, at least every three years)? Is the architecture testable in a production-like environment? |
| **ICT third-party risk** | Is every ICT provider (cloud, SaaS, data, network) in the register of information? Do contracts contain the required provisions (audit and access rights, incident support, data location, termination and exit)? Is there a **documented, tested exit strategy** and an assessment of concentration risk (same provider or region behind several critical functions)? |
| **Information sharing** | Are threat-intelligence inputs and outputs (feeds, sharing arrangements) considered in the design of monitoring? |

Typical architecture-level findings under DORA:

- Critical function depends on a single cloud region or single provider with no tested exit or fallback.
- Backup exists but restore was never tested against the stated RTO/RPO.
- No end-to-end tracing, so incident classification and timelines cannot be evidenced.
- Third-party components (SaaS, libraries, APIs) missing from the inventory or the register.
- Manual, unaudited production changes.

## 3. Other frameworks to check for applicability

| Framework | Check when | Architecture hooks |
| ----------- | ------------ | -------------------- |
| **GDPR** (Reg. (EU) 2016/679) | Personal data of people in the EU | Data classification, minimization, retention and erasure across *all* copies (caches, analytics, backups), DPIA for high-risk processing, breach detection supporting the 72h notification duty, cross-border transfer mechanism |
| **NIS2** (Directive (EU) 2022/2555) | Essential or important entities outside the financial sector (financial entities under DORA are covered by DORA as the more specific regime) | Risk-management measures, supply-chain security, incident reporting |
| **PSD2 / payment rules** | Payment services in the EU | Strong customer authentication, secure APIs, fraud monitoring; check the status of successor legislation |
| **PCI DSS** (currently v4.0.x) | Card data stored, processed or transmitted | Scope minimization (tokenization), network segmentation, key management, logging |
| **EBA guidelines** (ICT and security risk, outsourcing) and national supervisory expectations | Banks and payment institutions | Check with Compliance which guidelines remain in force alongside DORA and any national add-ons |
| **EU AI Act** (Reg. (EU) 2024/1689) | AI systems placed on the EU market or used in it | Risk classification, human oversight, logging, data governance; verify current application dates |
| **HIPAA / sector health rules** | US health data | Access controls, audit trails, encryption, business associate agreements |

## 4. Overlay criteria per quality gate

**Gate 1 - Conceptual**

- [ ] Applicable regimes identified and owners named (Compliance, DPO, CISO)
- [ ] Critical or important functions identified, with impact tolerance and RTO/RPO targets
- [ ] Third-party and cloud strategy consistent with concentration and exit expectations

**Gate 2 - Detailed design**

- [ ] Data classification applied to every store, queue and cache; residency and encryption decisions recorded
- [ ] Resilience design matches criticality (multi-AZ or multi-region where the RTO demands it; no hidden single points of failure)
- [ ] Logging and audit design captures who did what and when, tamper-evident, with retention aligned to obligations
- [ ] Exit strategy and portability considered for each critical third-party dependency (data export, API abstraction, contractual termination assistance)
- [ ] Segregation of duties and least privilege designed for production access, including emergency access

**Gate 3 - Implementation readiness**

- [ ] Register of information inputs (provider, service, criticality, data, location) prepared for new third-party services
- [ ] Testing plan includes restore tests, failover scenarios and security testing proportional to criticality
- [ ] Change management path (approvals, evidence, rollback) defined for production

**Gate 4 - Pre-production**

- [ ] Restore and failover exercised against stated RTO/RPO, with results recorded
- [ ] Incident detection and classification runbook tested, including the regulatory notification path and owners
- [ ] Security testing completed at the depth required (penetration test; TLPT where applicable)
- [ ] Third-party contracts and SLAs confirmed by Legal and Procurement before go-live

**Gate 5 - Post-launch**

- [ ] Real incidents (if any) were classified and reported within required timelines
- [ ] Resilience test findings tracked to closure; register of information updated

## 5. Review questions (fast probes)

1. Which customer-facing or regulated function fails if this component is down, and how long can it be down?
2. When was the last *successful restore* from backup, and what RTO did it actually achieve?
3. If our main cloud or SaaS provider disappeared for 30 days, what would we do, and has anyone tried it?
4. Can we reconstruct, from logs alone, who changed what in production last Tuesday?
5. Where does personal or regulated data live outside the primary database (caches, logs, exports, analytics, backups, vendor systems)?
6. Which provider contracts have audit, access and exit clauses, and who has read them?
7. Who is authorized to declare an incident "major", and how fast can they know?

## 6. Regulatory findings: how to grade them

| Situation | Suggested severity |
| ----------- | -------------------- |
| Mandatory control absent on a critical function, no compensating control | P0 |
| Mandatory control present on paper but untested (restore, failover, exit) on a critical function | P1 |
| Gap on a non-critical function, or documentation gap with the control operating | P2 |
| Improvement beyond the requirement | P3 |

Always state the **evidence** and the **assumption** behind the grading, and name who must confirm the regulatory interpretation.

---

**Overlay Version**: 1.0
