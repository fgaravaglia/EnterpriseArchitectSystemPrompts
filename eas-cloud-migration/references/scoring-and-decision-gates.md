# Scoring and Decision Gates

## Contents
1. Criteria and anchored rubric
2. Score formula
3. Ordered decision gates (this decides the R)
4. Flags required as input
5. Known flaws of the original template (fixed here)

## 1. Criteria and anchored rubric

All criteria are oriented so that **5 = favourable for cloud**. (The original mixed directions:
"Technical Complexity 5 = easy", "Compliance Burden 5 = low". Renamed to remove the inversion.)

| Code | Criterion | Weight | 1 (bad) | 3 (medium) | 5 (good) |
|---|---|---|---|---|---|
| BV | Business Value | 5 | Obsolete / few users | Important, replaceable | Critical, differentiating |
| TT | Technical Tractability (code/architecture quality) | 4 | Undocumented monolith, no tests, unsupported stack | Modular monolith, some tests | Modular/microservices, CI/CD, tests |
| CR | Cloud Readiness (runtime/infra dependencies) | 3 | Special hardware, licence tied to host, stateful local disks | Containerizable with effort | Stateless, 12-factor, containerized |
| CH | Compliance Headroom | 5 | Hard residency/regulatory block, unique audit needs | Standard controls, mappable | Public data, standard controls |
| TL | Target Lifespan | 3 | < 1 year | 2-3 years | > 5 years |

Score unknown as `?` — do not guess. Report the share of unknown cells as data-confidence.

## 2. Score formula

`Fit Score (0-100) = (Σ(score × weight) − Σweight) / (4 × Σweight) × 100`   (weights sum = 20)

Meaning: **how attractive the app is for investment in cloud modernization**. Use it to **rank and
sequence** apps inside a wave. It does not choose the R.

## 3. Ordered decision gates (first match wins)

| # | Gate | Condition | R |
|---|---|---|---|
| 1 | Redundant / unused | `usage = none` OR `duplicate_of` set | **Retire** |
| 2 | Hard block | CH = 1 OR `hw_dependency` OR `vendor_unsupported_in_cloud` | **Retain** (set revisit date + owner) |
| 3 | Near end of life | TL ≤ 2 and BV ≤ 3 | **Retain** until EoL, then Retire |
| 4 | SaaS fit | `saas_fit_pct` ≥ 80 AND BV ≤ 4 (commodity) | **Repurchase** |
| 5 | Fast DC exit on VMware | `source = vmware` AND `driver = dc_exit_speed` AND CR ≤ 2 | **Relocate** (optional 7th R) |
| 6 | Strategic modernization | BV ≥ 4 AND TL ≥ 4 AND (TT ≤ 3 OR CR ≤ 3) AND `refactor_case = positive` | **Refactor** |
| 7 | Managed-service gain | CR 2-4 AND BV ≥ 3 AND managed alternative exists | **Replatform** |
| 8 | Default | everything else | **Rehost** |

Notes
- Gate 3: an app with TL ≤ 2 but BV 5 is **not** Retire — it's critical but short-lived: Rehost or Retain.
- Gate 6 requires a positive business case (TCO break-even < 3 years or a velocity target). No case → Replatform.
- Gate 4 inverts the original rule ("Repurchase if BV > 4"): you replace *commodity* software, not crown jewels.
- Gate 5 beats gate 6 on purpose: with a hard DC-exit date, a strategic app is **Relocated now and Refactored in a later phase** (two-step). Record the planned second step.
- Always state the **adjacent R** you rejected and why.

## 3b. Compliance overlay (applies on top of the R)

Gate 2 only catches the hard block (CH = 1). Apps with **CH ≤ 2** (default; configurable via
`--ch-threshold`, set it from your own risk policy) keep the R chosen by the gates but get
**mandatory conditions**. It is an overlay, not a new R, because the migration path is the same
while the entry requirements change.

| Condition | Why |
|---|---|
| Compliance/risk sign-off before wave entry | Risk is a design partner, not an end-of-line gate |
| Tested exit plan (stressed and non-stressed) | Required for critical/important functions in regulated sectors |
| Resilience design (tier-1: multi-AZ / multi-region) | Availability must be demonstrated, not assumed |
| Not in Wave 1 | Wave 1 is the learning wave; don't learn on regulated workloads |
| ICT provider risk assessment + register entry (Repurchase, Replatform, Refactor) | New provider or managed service = new third-party dependency |

If the conditions can't be met in the time available, downgrade to **Retain** and record the revisit date.
Check your regulator's current requirements before citing specific obligations.

## 4. Flags required as input (add to inventory)
`usage`, `duplicate_of`, `hw_dependency`, `vendor_unsupported_in_cloud`, `saas_fit_pct`, `managed_alternative` (yes/no),
`refactor_case` (positive/negative/unknown), `source` (vmware/physical/other), `dependencies`.

## 5. Flaws of the original template (for transparency)
- Source credit: the "6 R's" are AWS's expansion of Gartner's 2010 5 Rs; Relocate came later (7 Rs).
- "Calculated Score" was never defined; weights existed but no formula.
- Refactor rule required CR > 3 (already cloud-ready), which argues *against* refactoring;
  its own example (Core Billing 5/2/1 → Refactor) failed the rule.
- Replatform rule `CR > 2 AND CR < 4` excluded CR = 4, yet its example (4/3/4) used it.
- Rules overlapped with no priority; no Retain rule; Retire on `TL < 2` wrongly retired critical apps.
- Compliance (weight 5) influenced no rule — now it triggers Retain (gate 2).
