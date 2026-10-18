# Report Template — Cloud Migration Strategy

Use this structure for the final deliverable. Language = user's language. Remove sections the user didn't ask for
and say what's missing. Placeholders in [brackets]. Tag numbers `FACT` / `ESTIMATE` / `ASSUMPTION`.

---
# Cloud Migration Strategy: [Project / Portfolio]
**Date** · **Prepared for** [Steering Committee/CTO] · **Version** · **Data confidence** [H/M/L, % apps fully scored]

## 0. Executive Summary (one page)
- **Decision requested**: [what the committee must decide, by when]
- **Recommendation**: [Go / Go with conditions / No-Go] — [one sentence why, citing criteria]
- **Strategy**: [Phased / Strangler / Hybrid] from [source] to [target], driver: [measurable]
- **Headline numbers**: [apps by R] · 3-yr TCO base [X] / pessimistic [Y] · break-even [year] · duration [N months]
- **Top 3 risks** (with owners) · **Conditions to GO** · **Next 90 days**

## 1. Context and objectives
Business goals (financial / agility / resilience, each measurable) · Scope in/out · Constraints (regulatory, RTO/RPO, freeze periods, hard dates)

## 2. Assumptions and data gaps
| # | Assumption / gap | Impact if wrong | How to close | Owner |

## 3. Landing zone summary
Network · Identity · Security · Operations · Account model

## 4. Portfolio analysis
### 4.1 Strategy distribution
| R | # apps | % of compute (ESTIMATE) | Key rationale |
### 4.2 Application table
| App | Owner | Current env | BV/TT/CR/CH/TL | Fit score | R | Why this R, not [adjacent R] | Compliance conditions (CH ≤ 2) | Confidence | Effort (wks, ESTIMATE) |
### 4.3 Retain / Retire register
| App | Decision | Owner | Revisit date | Condition to change |

## 5. Migration plan
### 5.1 Waves
| Wave | Focus | Timeline | Apps (top 3 / count) | Entry criteria | Exit criteria | Business impact |
### 5.2 Data migration (per wave, critical stores)
Pattern · cutover window · validation · rollback
### 5.3 Dependencies and critical path

## 6. TCO and FinOps
| Category | Current (annual avg) | Target (annual avg) | Net | Tag |
One-off + dual-running costs · break-even · sensitivity (base vs pessimistic) · FinOps levers

## 7. Risks
| ID | Risk | P | I | Owner | Trigger | Mitigation | Contingency |
Organizational readiness: skills, culture, change resistance and how it's handled

## 8. Governance and KPIs
CCoE · decision rights · cadence · KPI table with targets

## 9. Go / No-Go assessment
| Criterion | Status (met / partial / not met) | Evidence |
(driver measurable · landing zone timeline · funding incl. dual-running · skills plan · risk owners · date buffer ≥ 20%)

## 10. Next steps (first 90 days)
1. [action · owner · date] — landing zone approval · CCoE · Wave 0/1 pilot · discovery completion
**This week**: [one concrete action]
