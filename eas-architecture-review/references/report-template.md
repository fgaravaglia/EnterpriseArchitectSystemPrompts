# Review Report Template

Use this template for the final deliverable. `examples/example-design-review.md` shows a fully worked, long-form instance of it.

Pick the size that fits the request:

- **Lite** (default for chat questions, quick opinions, single-topic reviews): sections 1-4 only, about one page.
- **Full** (formal design review, gate assessment, go/no-go): all sections.

Write the report in the language of the request. Keep the section labels below in English only if the requester's documents use English labels.

---

## 1. Verdict (always first)

```markdown
**Decision**: APPROVE | APPROVE WITH CONDITIONS | REVISE
**Review type / gate**: [Design review, Gate 2 | Production readiness, Gate 4 | ...]
**Confidence**: High | Medium | Low  (Low = major evidence missing; say what)
**One-paragraph rationale**: [the 2-3 facts that drove the decision]
```

## 2. Findings summary

```markdown
| Severity | Count | Headlines |
|----------|-------|-----------|
| P0 Critical | n | [short titles] |
| P1 High     | n | [...] |
| P2 Medium   | n | [...] |
| P3 Low      | n | [...] |
```

Also list **Strengths** (3-5 concrete, evidenced points). Strengths are part of the review: they tell the team what not to break.

## 3. Findings (one block per finding, ordered by severity)

```markdown
### F-<n>: <Short title>  [P0|P1|P2|P3]  [Dimension]

- **Evidence**: <where in the submitted material, or metric, or "not evidenced">
- **Why it matters**: <impact on a business or quality goal, in concrete terms>
- **Recommendation**: <specific action, not a principle>
- **Alternatives / trade-off**: <at least one alternative when the fix has a real cost>
- **Effort**: S | M | L  (~range)      **Owner (suggested)**: <role>
- **Confidence**: High | Medium | Low   **Assumption**: <if any>
```

Rules: one finding = one problem = one action. If evidence is missing, the finding is "not evidenced", and the recommendation is to produce the evidence.

## 4. Conditions and next step

```markdown
**Conditions to proceed** (each verifiable, with owner and date):
1. <condition> - <owner> - <date> - <how we will verify>

**Next concrete step (this week)**: <one action the team can start immediately>
```

---

## 5. Risk view (Full only)

```markdown
| Risk | Likelihood | Impact | Mitigation | Owner |
|------|-----------|--------|------------|-------|
```

Split into technical, delivery and operational risks. Include adoption risk (people, process, politics) when the recommendations require behavior change.

## 6. Dimension scorecard (Full only)

Use the categories of `review-checklist.md` (Summary Scoring table): Pass / Warning / Fail / N/A per dimension, plus the count of findings per severity.

## 7. Quality gate status (when a gate applies)

Use the Gate Assessment Template in `quality-gates.md` and reference finding IDs for every failed criterion.

## 8. Open questions and assumptions

List what you could not verify and what you assumed. Each item states the impact on the verdict if the assumption is wrong.

## 9. Follow-up (Full only)

Re-review date, what will be re-checked, and the trigger for an earlier review (e.g., "if the load test misses p95").

---

## Self-check before sending

- [ ] Verdict is on top and consistent with the findings (counts match everywhere)
- [ ] Every P0/P1 has evidence, impact, a specific action, effort and owner
- [ ] Severities follow the definitions in SKILL.md, not gut feeling
- [ ] Numbers and arithmetic checked (availability, capacity, cost)
- [ ] Strengths included; tone is constructive and specific
- [ ] Assumptions and missing evidence are visible, not buried
- [ ] Conditions are verifiable; there is a single next concrete step
