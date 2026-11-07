# TCO and FinOps

## Rule: no false precision
Provide **base and pessimistic** cases, mark every input as `FACT` (user-supplied), `ESTIMATE` or
`ASSUMPTION`. If the user gave no cost baseline, produce the **structure with ranges** and ask for the inputs.

## Current-state baseline (what people forget)
Hardware depreciation/refresh · DC space, power, cooling · network/WAN · licences (OS, DB, hypervisor,
**Windows/SQL/Oracle BYOL rules in cloud**) · support contracts · staff time (not just FTE headcount) ·
DR site · backup · security tooling.

## Target-state lines
Compute · storage · network/**egress** · managed services · licences · support plan · observability ·
security tooling · landing zone overhead · training · **CCoE team**.

## One-off and transitional costs
Migration tooling · partner/SI effort · refactor engineering · **dual-running** (on-prem + cloud during waves) ·
data transfer · contract exit/early termination · testing · hypercare.

## Formula (per year, then 3-year sum)
`TCO_cloud(y) = run(y) + one_off(y) + dual_running(y)`
`Net(y) = TCO_onprem(y) − TCO_cloud(y)`
`Break-even = first year where cumulative Net ≥ 0`
`ROI % = cumulative Net(3y) / cumulative one_off`

Present: table by category, break-even year, sensitivity (±20% usage, +egress, slower migration pace).

## Honest caveat
Rehost-heavy portfolios often **raise** run cost in year 1-2 versus a depreciated on-prem baseline.
If the driver is cost and the plan is mostly Rehost, say so explicitly and show where savings come from
(rightsizing, commitment discounts, decommissioning, avoided refresh).

## FinOps levers
Rightsizing post-migration (60-90 days) · Savings Plans/Reserved/CUDs once usage is stable ·
non-prod schedules (auto-shutdown) · storage tiering · tagging + showback/chargeback ·
budget alerts and anomaly detection · egress review · licence optimization.

## Refactor justification template
Cost of refactor (one-off) · run-cost delta per year · velocity/resilience benefit (quantified or stated) ·
break-even year · what happens if we don't (maintenance cost, risk).
