# Risk and Governance

## Risk register — required fields
ID · Risk · Probability (H/M/L) · Impact (H/M/L) · **Owner** · **Early-warning trigger** · Mitigation (specific, actionable) · Contingency (if it happens anyway)

## Starter risks (tailor, drop the irrelevant)
| Risk | Typical trigger | Mitigation | Contingency |
|---|---|---|---|
| Hidden dependencies break cutover | Discovery < 90% coverage | Discovery tooling + owner interviews; move dependency groups together | Rollback runbook, keep on-prem warm |
| Data integrity loss | Reconciliation delta > 0 | CDC replication, checksum + business reconciliation, timed go/no-go | Rollback to source, replay |
| Downtime exceeds window | Rehearsal overruns | 2 dress rehearsals, blue-green/dark launch | Extend window with business sign-off |
| Skill gap | < 50% certified at Wave 1 start | Training plan, SI pairing, CCoE office hours | Slow wave pace, buy capacity |
| Egress / run-cost overrun | Month-3 bill > +15% vs model | Tagging, budgets, anomaly alerts, architecture review of chatty flows | Rightsize, move co-dependent apps together |
| Dual-running drags on | Wave slips > 1 month | Fixed decommission dates, exit criteria per wave | Re-baseline, escalate |
| Vendor lock-in | Heavy use of proprietary PaaS | Document exit path per tier-1 app, portability review | Exit plan execution |
| Performance regression | p95 > baseline +20% | Load test pre-cutover, observability baseline | Scale up, rollback |
| Change resistance | App owners refuse freeze; ops fear role loss | Early sponsorship, role evolution plan (ops → platform), visible quick wins | Exec escalation path |
| Security misconfiguration | Guardrail violations | Policy-as-code, CSPM, landing-zone only deployments | Quarantine + fix SLA |

Every major risk must have **both** a mitigation and an owner by name.

## Governance
- **CCoE** (small): platform lead, security, FinOps, architecture, migration factory lead. Mandate: standards, landing zone, guardrails, enablement, exceptions.
- **Decision rights**: who approves exceptions, who can stop a cutover, who owns the budget.
- **Cadence**: weekly migration stand-up, bi-weekly steering, monthly FinOps review.

## KPIs (with targets, not just names)
Migration velocity (apps/month) · % portfolio migrated vs plan · TCO variance vs model · incident rate post-cutover ·
unplanned downtime minutes · % resources tagged · % spend under commitment · on-prem decommissioned (racks/VMs/contracts) ·
% teams certified.

## Regulated-industry module (banks, insurers, public sector)
Load when the context mentions DORA, EBA, EIOPA, NIS2, supervisor, "critical or important functions".
Verify current text before citing articles; regulation evolves.
- **Overlay**: apps with CH ≤ 2 inherit the conditions in `scoring-and-decision-gates.md` §3b.
- **Mapping**: classify each app against critical/important functions; tier-1 apps need an explicit resilience design (multi-AZ, multi-region or tested exit).
- **Third-party ICT risk**: register of information for the cloud provider and subcontractors; concentration risk assessment (single provider, shared region).
- **Exit strategy**: documented and **tested** (stressed and non-stressed exit), with time estimates; portability for tier-1 data and workloads.
- **Contract**: audit/access rights, incident notification, data location, sub-outsourcing, termination assistance.
- **Data**: GDPR transfers and residency, encryption with customer-controlled keys where required.
- **Resilience testing**: DR and failover tests with evidence; TLPT applicability for the entity.
- **Supervisor notification**: check whether the move of a critical function requires prior notice.
- **Change resistance**: risk/compliance functions often need to be a *design partner* from Wave 0, not a gate at the end.
