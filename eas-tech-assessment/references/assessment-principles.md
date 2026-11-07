# Assessment Principles & Anti-Patterns

## The 6 Principles

### 1. Context is King

No technology is universally best. Always anchor recommendation to:

- Specific requirements
- Organizational constraints
- Team capabilities and timeline
- Risk tolerance
- Budget

**Wrong**: "PostgreSQL is the best database."  
**Right**: "Given your 3-engineer team with PostgreSQL experience, ACID requirements, and 6-month timeline, PostgreSQL is the best choice here."

### 2. Beware of Hype

Separate signal from noise. Red flags:

- "Revolutionary" or "game-changing" claims with no case studies
- "Replaces everything" positioning
- Overly aggressive advocates / resume-driven development
- No production case studies at comparable scale
- Project < 2 years old with no major adopters

### 3. Quantify When Possible

Replace qualitative claims with numbers:

- ❌ "Faster performance" → ✅ "50% lower p95 latency (200ms vs 400ms)"
- ❌ "Easier to learn" → ✅ "Team productive in 2 weeks vs 6 weeks"
- ❌ "Better ecosystem" → ✅ "15,000 npm packages vs 3,000"
- ❌ "More expensive" → ✅ "$4,200/month vs $1,800/month (3-year TCO: $50K gap)"

If you can't quantify, flag it explicitly as an estimate or uncertainty.

### 4. Total Cost of Ownership

Look beyond licensing:

```
TCO = Licensing + Infrastructure + Development + Operations + Training + Migration + Opportunity Cost
```

Most underestimated costs: training, migration, and operational overhead in year 1.

### 5. Reversibility Matters

Not all decisions are equal. The harder to reverse, the more rigor to apply.

- High reversibility: frontend library (days to change)
- Medium: backend framework (months)
- Low: database engine (quarters)
- Very low: cloud provider, core data platform (years)

**For low-reversibility decisions**: always recommend a time-boxed POC before final commitment.

### 6. Validate with POC

For significant, hard-to-reverse decisions:

1. Build small proof of concept (2-3 weeks max)
2. Test critical paths (the parts that could fail)
3. Measure key metrics against stated requirements
4. Get team feedback (they'll live with this daily)
5. Validate assumptions — POCs exist to find unknown unknowns

---

## Change Management Blind Spot

**Technically valid ≠ organizationally adoptable.**

Always flag when a technically superior choice is likely to face:

- High team resistance (unfamiliar paradigm, steep learning curve)
- Process disruption (changes CI/CD, deployment, monitoring)
- Cultural friction (e.g., moving from OOP to functional)
- Hiring challenges (small talent pool)

Recommend a change management strategy alongside technical recommendations for medium/high disruption changes.

---

## Common Assessment Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Popularity bias | Recommending the most-starred GitHub project | Check fit vs just fame |
| Recency bias | Favoring the newest option | Check production maturity |
| Survivorship bias | Only citing success stories | Research failure cases |
| Scope creep in assessment | Comparing 8+ technologies | Narrow to 3-4 serious candidates |
| Missing TCO | Comparing only licensing cost | Include full 3-year TCO |
| Ignoring team fit | Recommending a tech the team hates | Include DX + team feedback |
| Over-engineering | Recommending microservices for a 3-person startup | Match tech to current scale |

---

## Assessment Quality Checklist

A complete assessment delivers:

- [ ] Executive summary with recommendation and confidence
- [ ] Context recap (confirms understanding)
- [ ] Weighted comparison matrix
- [ ] Detailed analysis for top 2-3 choices
- [ ] Performance estimates with methodology
- [ ] 3-year TCO calculation
- [ ] Risk assessment for top recommendation
- [ ] Trade-off analysis (what you gain vs lose)
- [ ] Team impact (learning curve, productivity)
- [ ] Clear recommendation with conditions
- [ ] Confidence level with reasoning
- [ ] Actionable next steps / POC plan
- [ ] Decision triggers (what would change the recommendation)
