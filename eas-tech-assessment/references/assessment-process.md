# Assessment Process Reference

## The 6-Step Process

### Step 1: Clarify Context

Gather technical context (problem, requirements, constraints, stack, scale),
organizational context (team, skills, risk tolerance, timeline, budget), and
decision context (new vs replacement, expected lifetime, reversibility).

### Step 2: Define Evaluation Criteria

Establish weighted criteria based on context. Use three tiers:

- **Critical (40%)**: Must meet functional requirements, acceptable performance, team can learn in timeline
- **Important (40%)**: Good ecosystem/docs, reasonable operational complexity, acceptable TCO
- **Nice-to-have (20%)**: Excellent DX, strong community, cutting-edge features

### Step 3: Research Technologies

For each candidate:

- **Hard data**: Performance benchmarks (multiple sources), GitHub metrics, release cadence, CVEs, pricing
- **Soft data**: Community sentiment, production case studies, developer experience reports, expert comparisons

### Step 4: Structured Comparison

Create weighted comparison matrix. Score each dimension 1-5.
Replace qualitative with quantitative wherever possible.

### Step 5: Trade-off Analysis

- Identify clear winners
- Highlight context-sensitive trade-offs (gain X, lose Y)
- Quantify differences
- Flag reversibility risk

### Step 6: Provide Recommendation

1. Top recommendation + confidence level
2. Key reasons (3-5, context-specific)
3. Important caveats
4. Alternative options and when they win
5. Next steps (POC plan, validation milestones)

---

## Common Assessment Scenarios

### Database Selection — Key Dimensions

- Data model fit (structured, semi-structured, unstructured)
- Query patterns (OLTP, OLAP, mixed)
- Consistency requirements (ACID vs eventual)
- Scale requirements (vertical vs horizontal)
- Operational complexity
- Team expertise

### Frontend Framework — Key Dimensions

- Learning curve and team skills
- Performance (bundle size, runtime speed)
- Ecosystem (components, tooling)
- Enterprise readiness (TypeScript, testing)
- Long-term support
- Hiring pool

### Cloud Provider — Key Dimensions

- Service breadth and depth
- Pricing and cost predictability
- Geographic coverage
- Enterprise support and compliance certifications
- Existing organizational relationships
- Multi-cloud strategy

### API Style (REST / GraphQL / gRPC) — Key Dimensions

- Use case fit (public API, internal, real-time)
- Client diversity (web, mobile, IoT)
- Bandwidth constraints
- Type safety requirements
- Team familiarity

### Architecture Pattern (Monolith / Microservices / Modular Monolith) — Key Dimensions

- Team size and structure
- Deployment frequency needs
- Scale requirements
- Operational maturity
- Technology diversity needs
- System complexity

### Messaging / Event Streaming — Key Dimensions

- Throughput requirements
- Ordering guarantees (global, per-partition)
- Retention needs
- Consumer group / replay semantics
- Managed vs self-hosted
- Team operational capacity

### IaC Tools — Key Dimensions

- Multi-cloud support
- State management complexity
- Module ecosystem
- Testing capabilities
- Drift detection
- Team programming language familiarity
