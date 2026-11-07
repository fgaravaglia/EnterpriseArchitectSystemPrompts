# Wave Planning

## Principles
1. **Group by dependency, not by R.** A rehost app chatty with a refactor app moves together or you pay latency/egress.
2. Build the **dependency graph** first (app→app, app→DB, shared services, batch/ETL, auth). Unknown dependencies are the #1 cause of failed cutovers; budget for discovery tooling and interviews.
3. **Wave 1 = learning wave**: low risk but production-like, includes at least one real workload, validates landing zone, tooling, runbooks and the cutover process. Not "all the dev/test".
4. Sequence inside a wave by Fit Score descending, then by lowest risk.
5. Respect **freeze periods** (year-end close, peak season, audit windows) and team capacity (max parallel cutovers).
6. Hard external dates (DC lease end) go backward from the date with ≥20% buffer.
7. **Decommission is part of the wave**: savings only exist when on-prem is switched off.

## Wave table (fields)
Wave · Focus · Apps (top + count) · Entry criteria · Exit criteria · Duration (ESTIMATE) · Dependencies · Risk level · Business impact

Typical shape (adapt, don't copy):
- Wave 0: landing zone, CCoE, tooling, pilot of 1-2 apps
- Wave 1: low-risk production-like (rehost/replatform), prove runbooks
- Wave 2: data core and shared services (DBs, ETL, identity-dependent apps)
- Wave 3: strategic refactors, Repurchase cutovers
- Wave N: Retain review + Retire/decommission

## Data migration patterns (pick per store)
| Pattern | Use when | Downtime | Watch out |
|---|---|---|---|
| Offline bulk (snapshot/transfer appliance) | Large cold data, relaxed window | Hours-days | Delta after snapshot |
| Continuous replication + cutover (CDC/DMS/native) | Critical DBs, small window | Minutes | Lag, schema drift, sequence/identity values |
| Dual-write / strangler | Refactor with progressive traffic shift | ~0 | Consistency, complexity |
| Re-point after Relocate | VMware-to-VMware services | Minutes | Licensing, network extension |

Every critical store needs: validation (row counts + checksums + business reconciliation), rollback
criteria (go/no-go checkpoint timed), and an owner on the night.

## Cutover checklist (short)
Freeze announced · backup verified · replication lag < threshold · rollback tested · DNS TTL lowered ·
comms plan · hypercare window defined · on-prem kept read-only for N days before decommission.
