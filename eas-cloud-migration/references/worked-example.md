# Worked Example (illustrative — fictional data)

**Prompt**: "Mid-size insurer, 2 DCs on VMware, 120 apps, going to Azure. DC lease ends in 20 months.
Goal: exit DCs without losing the Solvency reporting calendar. Budget ~€6M. EU data only."

## Step 1 — What the skill asks (one message)
1. Is the lease end date contractual or negotiable (extension cost)?
2. Any app tied to specific hardware or a vendor that doesn't certify Azure?
3. Which regions are allowed (EU only? two EU regions for DR)?
4. Current annual DC + licence cost, if you can share it, so I can build the baseline.
5. Can you share the inventory? Template attached.

(User answers 1-3, can't share costs → proceed with a labelled estimate structure.)

## Step 3 — Excerpt of the output table
Driver = `dc_exit_speed`. Scores BV/TT/CR/CH/TL.

| App | Scores | Fit | R | Why this R, not the adjacent | Conf. |
|---|---|---|---|---|---|
| Claims Core | 5/2/2/3/5 | 61 | **Relocate → Refactor (phase 2)** | Hard 20-month date: refactor first would miss it. Relocate to Azure VMware Solution now, refactor from month 12 (break-even ESTIMATE ~3.5 yrs). Not Rehost: licences tied to the hypervisor. | M |
| Intranet Wiki | 2/4/3/5/3 | 61 | **Repurchase** | SaaS fit 90%, commodity. Not Retire: still used by 400 staff. | H |
| Actuarial Batch | 4/3/4/4/4 | 70 | **Replatform** | Move jobs to a managed scheduler/DB; Rehost would keep a DBA-heavy setup. Not Refactor: no positive case yet (revisit in 12 months). | M |
| Customer Portal | 4/3/3/2/5 | 58 | **Replatform** + compliance overlay | Managed app platform + DB gives operational relief. Not Refactor: no positive case yet. CH = 2 → conditions: risk sign-off before entry, tested exit plan, resilience design, ICT provider assessment, **not in Wave 1**. | M |
| Policy Ledger | 5/1/1/1/5 | 40 | **Retain** | Vendor doesn't support cloud (gate 2). Revisit in 6 months with the vendor's roadmap; exit-DC plan needs a small colo for this one — flagged as a plan risk. | H |
| Legacy Reporting | 2/3/3/5/1 | 49 | **Retire** | Duplicate of the new BI stack (gate 1). Saves one wave slot. | H |

## Step 4 — Waves (excerpt)
| Wave | Focus | Timeline (ESTIMATE) | Why |
|---|---|---|---|
| 0 | Landing zone, CCoE, discovery | M1-M3 | Gates everything; identity + network first |
| 1 | 12 low-risk production-like apps incl. Intranet Wiki, one reporting app | M3-M6 | Proves runbooks with real users, avoids "all dev/test" false confidence |
| 2 | Data core: Actuarial Batch, shared DBs, ETL | M6-M12 | Dependency group moved together to avoid cross-DC latency |
| 3 | Claims Core Relocate, then refactor roadmap | M12-M16 | Must avoid the Solvency reporting freeze (M10-M11) — scheduling choice goes to steering |
| 4 | Decommission + Retain review | M14-M20 | Savings need switched-off racks |

## Step 5 — What the self-critique caught
- First draft said GO. Criteria check: no skills plan, dual-running not funded → **Go with conditions**.
- Assumption that breaks the plan: lease end date can't move. Named in section 2.
- Politically hard: the 3-person ops team sees Relocate/Replatform as role loss → role-evolution plan (ops → platform) added to risks.

## Final line of the response
"This week: ask procurement what a 6-month lease extension would cost — it's the cheapest insurance against your biggest assumption."
