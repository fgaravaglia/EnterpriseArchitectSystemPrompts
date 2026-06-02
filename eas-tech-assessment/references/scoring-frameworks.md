# Scoring & Decision Frameworks

## Scoring Scale

- 🟢 5/5 Excellent — exceeds requirements significantly
- 🟡 4/5 Good — meets requirements well
- 🟠 3/5 Adequate — meets minimum requirements
- 🔴 2/5 Poor — barely meets or has significant gaps
- ⛔ 1/5 Unacceptable — does not meet requirements
- N/A — not applicable to this assessment

---

## Framework 1: Technology Radar

Classify into quadrants:

- **Adopt**: High confidence, ready for production use
- **Trial**: Worth exploring, POC recommended before committing
- **Assess**: Interesting, monitor developments, not ready to use
- **Hold**: Avoid for new projects, plan phase-out if already using

For each technology provide: current position, movement direction (↑↓→), reasoning, last assessment date.

---

## Framework 2: Risk-Value Matrix

```
High Value │  ⚠️ Calculated Risk   │  ⭐ Sweet Spot
           │  (validate with POC)  │  (Recommended)
           │──────────────────────│──────────────────
Low Value  │  ❌ Avoid             │  ✅ Safe Conservative
           │                      │
           └──────────────────────┴──────────────────
                High Risk              Low Risk
```

Use this to position each candidate visually. Ideal recommendation: Sweet Spot quadrant.

---

## Framework 3: Weighted Decision Matrix

```
Total Score = Σ(Criterion Weight × Technology Score)

Example:
  Performance (30%): Tech A = 4/5 → 0.30 × 4 = 1.20
  Maturity (25%):    Tech A = 5/5 → 0.25 × 5 = 1.25
  Cost (20%):        Tech A = 3/5 → 0.20 × 3 = 0.60
  DX (15%):          Tech A = 4/5 → 0.15 × 4 = 0.60
  Team Fit (10%):    Tech A = 2/5 → 0.10 × 2 = 0.20

  Total = 3.85/5
```

Show the matrix explicitly in every multi-technology comparison.

---

## Framework 4: Cost-Benefit Analysis

**Costs to always include**:

- Licensing fees (annual)
- Infrastructure (monthly × 36 months = 3-year TCO)
- Development time (engineer-hours × blended hourly rate)
- Training (courses + time away from delivery)
- Migration effort (if replacing existing system)
- Operational overhead (monitoring, maintenance, on-call)

**Benefits to quantify**:

- Faster time to market (business value of earlier delivery)
- Performance improvements (conversion, SLA compliance)
- Cost savings vs alternatives
- Risk reduction (quantified)
- Developer productivity gains

**Formula**:

```
ROI = (Total Benefits - Total Costs) / Total Costs × 100%
```

---

## Reversibility Guide

| Decision Type | Reversibility | Recommended Investment |
|--------------|--------------|----------------------|
| UI component library | Very High (days) | Light assessment |
| Frontend framework | High (weeks) | Standard assessment |
| Backend framework | Medium (months) | Standard + POC |
| Message broker | Medium-Low (months+) | Full assessment + POC |
| Database | Low (quarters) | Full assessment + POC + pilot |
| Cloud provider | Very Low (years) | Full assessment + pilot + exec sign-off |
| Core data platform | Very Low (years) | Full assessment + pilot + exec sign-off |

**Rule**: The lower the reversibility, the more time and rigor to invest in assessment.
