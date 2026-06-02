# Output Format Templates

## Format 1: Executive Summary

**Use for**: C-level, management, non-technical stakeholders

```markdown
# Technology Assessment: [Technology Name]

## Recommendation
[Adopt / Trial / Hold] — Confidence: [High / Medium / Low]

## Executive Summary
[2-3 sentences: what it is, why this recommendation]

## Key Benefits
- [Benefit 1 with business impact, quantified]
- [Benefit 2 with business impact, quantified]
- [Benefit 3 with business impact, quantified]

## Key Risks
- [Risk 1] → Mitigation: [action]
- [Risk 2] → Mitigation: [action]

## Investment Required
- **Time**: [Timeline]
- **Cost**: [Budget estimate — include dev + infra + training]
- **Resources**: [Team requirements]

## Next Steps
1. [Concrete action 1 with owner and date]
2. [Concrete action 2]
```

---

## Format 2: Technical Deep Dive

**Use for**: Architects, senior engineers, technical decision makers

```markdown
# Technology Assessment: [Technology Name]

## Assessment Context
[Problem being solved, constraints, decision deadline]

## Evaluation Criteria (Weighted)
| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| [Dimension] | [%] | [Why this weight] |

## Comparison Matrix
| Criterion | Weight | [Tech A] | [Tech B] | [Tech C] | Winner |
|-----------|--------|----------|----------|----------|--------|
| [Dimension] | [%] | [Score + note] | ... | ... | [Best] |
| **Weighted Total** | 100% | **X.X/5** | **X.X/5** | **X.X/5** | |

## Detailed Analysis
### [Tech A]
- **Strengths**: ...
- **Weaknesses**: ...
- **Best for**: ...

## Performance Benchmarks
[Specific numbers, test methodology, source]

## TCO Analysis (3-year)
| Cost Type | Tech A | Tech B | Tech C |
|-----------|--------|--------|--------|
| Licensing | | | |
| Infrastructure (3yr) | | | |
| Development | | | |
| Training | | | |
| Migration | | | |
| **Total TCO** | | | |

## Trade-off Analysis
- **[Tech A] vs [Tech B]**: Gain [X], lose [Y], matters if [condition]
- ...

## Risk Assessment
| Risk | Tech A | Tech B | Mitigation |
|------|--------|--------|------------|

## Recommendation
[Detailed recommendation with reasoning tied to their specific context]

## Proof of Concept Plan
- **Duration**: [X weeks]
- **Success criteria**: [Measurable outcomes]
- **What to test**: [Critical paths]
- **Decision trigger**: [What would change the recommendation]

## References
[Benchmarks, case studies, documentation links]
```

---

## Format 3: Comparison Table (Quick Reference)

**Use for**: Decision meetings, Slack updates, rapid reference

```markdown
# Technology Comparison: [Tech A] vs [Tech B] vs [Tech C]

## Quick Summary
| Aspect | [Tech A] | [Tech B] | [Tech C] |
|--------|----------|----------|----------|
| **Recommendation** | ⭐ Primary | ✅ Alternative | ❌ Avoid |
| **Best For** | [Use case] | [Use case] | [Use case] |
| **Performance** | 🟢 Excellent | 🟡 Good | 🔴 Poor |
| **TCO (3yr)** | $XXK | $XXK | $XXK |
| **Learning Curve** | [Weeks] | [Weeks] | [Weeks] |
| **Hiring Pool** | Large | Medium | Small |

## Decision Guide
- **Choose [Tech A] if**: [Specific conditions]
- **Choose [Tech B] if**: [Specific conditions]  
- **Avoid [Tech C] because**: [Specific reasons]
```

---

## Format 4: POC Plan

**Use for**: Validating a recommendation before full commitment

```markdown
# POC Plan: [Technology Name]

## Objective
Validate [specific assumption] within [X weeks].

## Success Criteria
- [ ] [Measurable outcome 1, e.g., "p95 latency < 50ms under 1K req/sec load"]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

## Scope
**In scope**: [What we'll test]  
**Out of scope**: [What we won't test and why]

## Timeline
| Week | Activity | Owner |
|------|----------|-------|
| 1 | Setup + baseline | |
| 2 | Critical path testing | |
| 3 | Load testing + team feedback | |

## Resources Required
- [X] engineers for [Y] weeks
- Infrastructure: [estimate]

## Go / No-Go Criteria
**Go if**: All success criteria met + team confidence ≥ Medium  
**No-go if**: [Specific failure conditions]

## Decision Date
[Date when POC results reviewed and final decision made]
```
