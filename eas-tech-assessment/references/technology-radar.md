# Technology Radar Framework

A comprehensive guide to using the Technology Radar approach for assessing and tracking technology adoption decisions. Based on the Thoughtworks Technology Radar methodology, adapted for Enterprise Architects.

---

## What is a Technology Radar?

A **Technology Radar** is a visual tool and framework for tracking technology decisions, trends, and recommendations within an organization. It helps:

- **Communicate** technology strategy to stakeholders
- **Track** technology adoption over time
- **Standardize** decision-making across teams
- **Reduce risk** by classifying maturity levels
- **Enable innovation** while maintaining stability

### Origin

Created by [Thoughtworks](https://www.thoughtworks.com/radar) in 2010, published bi-annually. Companies like Zalando, Spotify, and AOE have adopted and customized it for internal use.

---

## Radar Structure

The Technology Radar has **two dimensions**:

### Dimension 1: Rings (Maturity/Recommendation)

From inner to outer ring:

#### 1. ADOPT 🟢
**Meaning**: "We recommend this technology for production use"

**Characteristics**:
- Proven in production at our organization
- Well understood by multiple teams
- Stable and mature
- Strong support and documentation
- Low risk for new projects

**Examples**:
- PostgreSQL (database)
- Kubernetes (orchestration)
- React (frontend framework)
- TypeScript (language)

**When to place here**:
- Multiple successful production deployments
- Team expertise is widespread
- No major concerns or blockers

#### 2. TRIAL 🟡
**Meaning**: "Worth pursuing. Enterprises should try in a project that can handle the risk"

**Characteristics**:
- Shows promise, worth experimenting
- POC or pilot projects underway
- Some risk, but manageable
- Learning curve acceptable
- Not yet proven at scale in our context

**Examples**:
- GraphQL (if you're REST-heavy)
- Deno (if you're Node.js-heavy)
- Terraform CDK (if using Terraform)
- Tailwind CSS (if using traditional CSS)

**When to place here**:
- Technology addresses real pain point
- Initial POC shows promise
- 1-2 teams experimenting
- Waiting for production validation

#### 3. ASSESS 🟠
**Meaning**: "Worth exploring with the goal of understanding how it will affect your enterprise"

**Characteristics**:
- Interesting but unproven
- Research and exploration phase
- May be too new or immature
- Potential game-changer, or may be hype
- No commitment yet

**Examples**:
- WebAssembly for frontend
- Rust for backend services
- Micro-frontends architecture
- Server-driven UI patterns

**When to place here**:
- Emerging technology or pattern
- Solving problems you don't have yet (but might)
- Industry buzz, want to understand reality
- Spike/research phase only

#### 4. HOLD ⛔
**Meaning**: "Proceed with caution. Not recommended for new projects"

**Characteristics**:
- Declining or obsolete
- Better alternatives exist
- Phase out from existing systems
- Don't start new work with this
- Legacy/maintenance mode

**Examples**:
- AngularJS (superseded by Angular)
- jQuery (for new projects)
- MongoDB 2.x (old version)
- Monolithic architecture (in certain contexts)

**When to place here**:
- Technology is being phased out
- Better alternatives available
- Known issues or limitations
- Keep for existing systems, no new adoption

---

### Dimension 2: Quadrants (Technology Categories)

#### 1. Techniques
**Definition**: Processes, methodologies, approaches, practices

**Examples**:
- Adopt: Trunk-based development, Infrastructure as Code
- Trial: Chaos engineering, Contract testing
- Assess: Micro-frontends, Event storming
- Hold: Long-lived feature branches, Manual deployment

**Subcategories**:
- Development practices (TDD, pair programming)
- Architecture patterns (microservices, event sourcing)
- DevOps practices (GitOps, continuous delivery)
- Agile methodologies (Scrum, Kanban)

#### 2. Tools
**Definition**: Software tools, applications, utilities

**Examples**:
- Adopt: Docker, GitHub Actions, Datadog
- Trial: Deno, K6, Playwright
- Assess: Bun, WASM runtimes
- Hold: Jenkins (migrating to GitHub Actions)

**Subcategories**:
- Development tools (IDEs, linters, debuggers)
- DevOps tools (CI/CD, monitoring, logging)
- Testing tools (unit, integration, e2e)
- Productivity tools (project management, documentation)

#### 3. Platforms
**Definition**: Infrastructure, operating systems, cloud platforms, frameworks

**Examples**:
- Adopt: AWS, Kubernetes, PostgreSQL
- Trial: Cloudflare Workers, Supabase
- Assess: Deno Deploy, Edge computing platforms
- Hold: On-premise data centers

**Subcategories**:
- Cloud providers (AWS, Azure, GCP)
- Databases (SQL, NoSQL, NewSQL)
- Message brokers (Kafka, RabbitMQ)
- Orchestration (Kubernetes, ECS, Nomad)

#### 4. Languages & Frameworks
**Definition**: Programming languages, frameworks, libraries

**Examples**:
- Adopt: TypeScript, React, Spring Boot
- Trial: Svelte, FastAPI, Go for services
- Assess: Rust, Solid.js, Fresh
- Hold: PHP 5.x, AngularJS, jQuery

**Subcategories**:
- Programming languages (JavaScript, Python, Java, Go)
- Frontend frameworks (React, Vue, Angular, Svelte)
- Backend frameworks (Spring, Express, FastAPI, Rails)
- Libraries (Lodash, Axios, date-fns)

---

## Visual Representation

### Classic Radar Visualization

```
                    TECHNIQUES
                        │
                   ASSESS│TRIAL
                    ╱    │    ╲
              HOLD ●     │     ● ADOPT
                    ╲    │    ╱
       TOOLS ──────────────────────── LANGUAGES
                    ╱    │    ╲
              HOLD ●     │     ● ADOPT
                    ╲    │    ╱
                   ASSESS│TRIAL
                        │
                   PLATFORMS
```

### Alternative: Quadrant Grid

```
┌─────────────────────┬─────────────────────┐
│    TECHNIQUES       │    TOOLS            │
│                     │                     │
│ 🟢 ADOPT:           │ 🟢 ADOPT:           │
│ • Trunk-based dev   │ • Docker            │
│ • IaC               │ • GitHub Actions    │
│                     │                     │
│ 🟡 TRIAL:           │ 🟡 TRIAL:           │
│ • Chaos eng         │ • K6                │
│                     │                     │
├─────────────────────┼─────────────────────┤
│    PLATFORMS        │ LANGUAGES/FRAMEWORKS│
│                     │                     │
│ 🟢 ADOPT:           │ 🟢 ADOPT:           │
│ • AWS               │ • TypeScript        │
│ • Kubernetes        │ • React             │
│                     │                     │
│ 🟡 TRIAL:           │ 🟡 TRIAL:           │
│ • Cloudflare        │ • Svelte            │
│                     │                     │
└─────────────────────┴─────────────────────┘
```

---

## Creating Your Organization's Radar

### Step 1: Inventory Current Technologies

**Method**: Survey teams and projects

**Template**:
```markdown
## Current Technology Inventory

### In Production
- PostgreSQL (5 projects)
- MongoDB (2 projects)
- MySQL (3 legacy projects)

### In Pilot/POC
- GraphQL (1 project)
- Svelte (1 project)

### Under Evaluation
- Rust for backend
- Edge computing
```

### Step 2: Classify Each Technology

**Decision Tree**:

```
Is it proven in production in our org?
├─ YES → Multiple teams using it?
│         ├─ YES → ADOPT 🟢
│         └─ NO → TRIAL 🟡
│
└─ NO → Do we have active POC/pilot?
          ├─ YES → TRIAL 🟡
          └─ NO → Do we plan to explore it?
                    ├─ YES → ASSESS 🟠
                    └─ NO → Should we avoid it?
                              ├─ YES → HOLD ⛔
                              └─ NO → Not on radar
```

### Step 3: Define Entry Criteria

**ADOPT Criteria**:
- [ ] 3+ production deployments
- [ ] Positive team feedback (80%+ satisfaction)
- [ ] Documented best practices exist
- [ ] Training materials available
- [ ] Support process established
- [ ] No major blockers or concerns

**TRIAL Criteria**:
- [ ] Addresses real pain point
- [ ] 1+ successful POC completed
- [ ] Risk assessment completed
- [ ] Learning path defined
- [ ] 1-2 teams committed to trying it
- [ ] Success criteria defined

**ASSESS Criteria**:
- [ ] Relevant to our domain/problems
- [ ] Spike/research completed
- [ ] Industry adoption exists
- [ ] Technical feasibility assessed
- [ ] No immediate need, but future potential

**HOLD Criteria**:
- [ ] Being phased out
- [ ] Better alternative exists (specify)
- [ ] Known significant issues
- [ ] No new projects should use it
- [ ] Migration plan for existing usage

### Step 4: Movement Rules

**Moving INTO the Radar** (Off → Assess):
- Technology becomes relevant to our problems
- Industry adoption warrants investigation
- Team expresses interest with justification

**Moving INWARD** (Assess → Trial → Adopt):
- Assess → Trial: Successful spike, team ready to pilot
- Trial → Adopt: Successful production deployment, team expertise grown

**Moving OUTWARD** (Adopt → Trial → Assess → Hold):
- Significant issues discovered
- Better alternative emerges
- Strategic direction changes
- Technology becomes obsolete

**Moving OFF the Radar** (Hold → Off):
- No remaining usage in organization
- Complete migration accomplished
- No longer relevant

### Step 5: Update Cadence

**Recommended**: Quarterly updates with annual comprehensive review

**Quarterly** (lightweight):
- Add new technologies entering ASSESS
- Move technologies between rings based on progress
- Update descriptions for changed items
- Remove technologies that left the radar

**Annual** (comprehensive):
- Complete inventory review
- Validate all classifications
- Gather team feedback via survey
- Strategic alignment check
- Publish updated radar with blog post

---

## Technology Radar Entry Template

For each technology on the radar, document:

```markdown
### [Technology Name]

**Ring**: [Adopt | Trial | Assess | Hold]  
**Quadrant**: [Techniques | Tools | Platforms | Languages & Frameworks]  
**Status**: [New | Moved In | Moved Out | No Change]

#### Description
[1-2 sentences: What is it?]

#### Rationale
[Why this ring? What's the recommendation?]

#### Context
- **Use Cases**: [Where does it fit?]
- **Alternatives**: [What else was considered?]
- **Team Experience**: [Who has used it?]

#### Adoption Status
- **Projects Using**: [List or count]
- **Success Stories**: [Brief examples]
- **Challenges**: [Known issues]

#### Next Steps
- [What should teams do with this info?]

#### Last Updated
[Date and by whom]

---

**Example:**

### GraphQL

**Ring**: Trial 🟡  
**Quadrant**: Languages & Frameworks  
**Status**: Moved In (from Assess)

#### Description
GraphQL is a query language for APIs that allows clients to request exactly the data they need, reducing over-fetching and under-fetching.

#### Rationale
We're placing GraphQL in TRIAL after successful POC in the Mobile team. It addresses real pain points with our REST APIs (multiple round trips, over-fetching). However, we need more production validation before recommending broadly.

#### Context
- **Use Cases**: Mobile apps needing flexible queries, BFF (Backend for Frontend) pattern
- **Alternatives**: REST (current standard), gRPC (evaluated, better for service-to-service)
- **Team Experience**: Mobile team (6 months), 1 backend engineer trained

#### Adoption Status
- **Projects Using**: Mobile app (production), Admin portal (POC starting)
- **Success Stories**: Mobile app reduced API calls by 40%, improved loading time by 30%
- **Challenges**: Schema design requires careful planning, caching strategy different from REST

#### Next Steps
- Teams with mobile clients should evaluate GraphQL for BFF layer
- Backend team creating GraphQL best practices guide (due Q2)
- Monitoring performance in production for 6 months before ADOPT consideration

#### Last Updated
2024-10-30 by Enterprise Architecture Team
```

---

## Assessment Process for New Technologies

### 1. Initial Request

**Who can request**: Any team member  
**Process**: Submit technology proposal

**Template**:
```markdown
## Technology Proposal: [Name]

**Proposed by**: [Name, Team]  
**Date**: [YYYY-MM-DD]

### Problem Statement
[What problem does this solve?]

### Technology Overview
[Brief description of the technology]

### Why Now?
[Why is this relevant now?]

### Alternatives Considered
[What else did you evaluate?]

### Proposed Ring
[Assess | Trial | Adopt] and why

### Initial Assessment
- [ ] Technical feasibility researched
- [ ] Cost implications understood
- [ ] Team capacity available
- [ ] Aligns with tech strategy

### Next Steps
[What do you propose we do?]
```

### 2. Architecture Review

**Who**: Enterprise Architecture team  
**Duration**: 1-2 weeks

**Review Checklist**:
- [ ] Strategic alignment validated
- [ ] Technical feasibility confirmed
- [ ] Cost/benefit analysis completed
- [ ] Risk assessment done
- [ ] Team readiness evaluated
- [ ] Alternative options reviewed

**Outputs**:
- Recommendation (Accept, Modify, Reject)
- Proposed ring placement
- Conditions/requirements
- Next steps

### 3. Approval & Placement

**Lightweight** (for Assess):
- Architecture team approval sufficient
- Add to radar immediately
- Notify organization via Slack/email

**Heavyweight** (for Trial/Adopt):
- Requires Architecture Review Board approval
- POC/pilot results required
- Training plan needed
- Support model defined

### 4. Monitoring & Graduation

**Metrics to Track**:
- Number of teams using
- Production deployments
- Team satisfaction (surveys)
- Success/failure stories
- Support burden

**Graduation Criteria**:
Assess → Trial:
- [ ] Spike completed successfully
- [ ] Team ready to pilot
- [ ] Success criteria defined

Trial → Adopt:
- [ ] 3+ production deployments
- [ ] Positive team feedback (>80%)
- [ ] Best practices documented
- [ ] Training available
- [ ] No major blockers

---

## Common Patterns & Antipatterns

### ✅ Good Patterns

#### 1. Start Small
Begin with ASSESS, validate through TRIAL before ADOPT.

**Example**: Don't jump React → Svelte → ADOPT. Do: React (ADOPT) → Svelte (ASSESS) → POC → Svelte (TRIAL) → validate → Svelte (ADOPT)

#### 2. Evidence-Based Movement
Move technologies based on concrete outcomes, not hype.

**Example**: GraphQL moved to TRIAL after measuring 40% reduction in API calls, not because it's trendy.

#### 3. Clear Exit Criteria
Define what success looks like before starting.

**Example**: "Svelte moves to ADOPT when: 3 production apps, <2 weeks training time, team satisfaction >80%"

#### 4. Diverse Quadrants
Balance innovation across all quadrants (techniques, tools, platforms, languages).

**Example**: Don't just focus on languages. Also assess techniques (mob programming) and tools (Playwright).

#### 5. Hold Doesn't Mean Forbidden
HOLD = "don't start new work," not "stop all use immediately."

**Example**: AngularJS in HOLD - maintain existing apps, but new projects use Angular or React.

---

### ❌ Antipatterns

#### 1. Resume-Driven Decisions
Adding tech because engineers want to learn it, not because it solves problems.

**Example**: "Let's use Rust because it's cool" vs "Let's assess Rust for our performance-critical service where GC pauses are an issue"

#### 2. Too Many in ADOPT
If everything is ADOPT, nothing is. ADOPT should be your stable, recommended core.

**Rule of thumb**: 
- ADOPT: 30-40% of radar
- TRIAL: 30-40%
- ASSESS: 20-30%
- HOLD: 10-20%

#### 3. Skipping Rings
Going directly from ASSESS to ADOPT without TRIAL validation.

**Problem**: Bypasses learning and validation phase. High risk.

#### 4. Never Moving to HOLD
Accumulating technologies without deprecating old ones.

**Result**: Technology sprawl, maintenance burden, confusion.

**Fix**: Actively move outdated tech to HOLD and eventually off the radar.

#### 5. Radar as Dictatorship
"This is the law, comply or else."

**Better**: Radar as guidance. Teams can make different choices with justification and architecture approval.

#### 6. Static Radar
Creating radar once and never updating it.

**Fix**: Quarterly reviews minimum. Radar should be living document.

---

## Integration with ADRs

**Relationship**: Technology Radar complements Architecture Decision Records (ADRs)

### When Technology Enters TRIAL or ADOPT
→ Create ADR documenting the decision

**ADR should reference**:
- Radar entry for the technology
- Assessment that led to placement
- Alternatives considered
- Success criteria for progression

**Example**:
```markdown
# ADR-042: Adopt GraphQL for Mobile BFF

## Status
Accepted

## Context
GraphQL has been in TRIAL for 6 months after successful POC. 
See Technology Radar Q3 2024.

[Rest of ADR...]

## Decision
Move GraphQL to ADOPT ring for mobile BFF use cases.

## Consequences
Teams building mobile APIs should default to GraphQL.
See updated Technology Radar entry for guidance.
```

### When Technology Moves to HOLD
→ Create ADR documenting deprecation

---

## Communicating the Radar

### Internal Communication

#### 1. Radar Publication
**Format**: Interactive website + PDF + blog post

**Tools**:
- [Thoughtworks Radar Builder](https://www.thoughtworks.com/radar/byor)
- [Zalando Tech Radar](https://github.com/zalando/tech-radar)
- [AOE Tech Radar](https://github.com/AOEpeople/aoe_technology_radar)

#### 2. Quarterly Newsletter
**Content**:
- What's new this quarter
- Technologies that moved (highlight with explanations)
- Success stories
- Upcoming assessments

#### 3. Brown Bag Sessions
**Format**: Lunch & learn presentations

**Topics**:
- "What's new in the Tech Radar"
- "Deep dive: Technology X (now in TRIAL)"
- "Lessons learned from HOLD technologies"

#### 4. Slack/Teams Channel
**Purpose**: Ongoing discussion

**Activities**:
- Announcement of radar updates
- Questions about placements
- Technology proposals
- Experience sharing

### External Communication

#### For Candidates/Recruiting
**Message**: "We use modern, proven technologies and actively evaluate emerging trends"

**Show**:
- ADOPT ring (our core stack)
- TRIAL ring (we're forward-thinking)
- Process (we're thoughtful about decisions)

#### For Partners/Vendors
**Message**: "These are our technology standards"

**Use**:
- Align vendor proposals with our radar
- Vendors know what we use (better proposals)
- Integration compatibility

---

## Example: Complete Radar Entry Set

### Techniques Quadrant

#### ADOPT 🟢
**Trunk-Based Development**
- All teams use trunk-based development with short-lived feature branches (<2 days)
- CI/CD pipeline enforces this with automated checks
- 95% developer satisfaction

**Infrastructure as Code**
- All infrastructure defined in Terraform
- 100+ modules in internal library
- Change review process established

**Continuous Deployment**
- All services deploy to production multiple times per day
- Automated rollback on failures
- MTTR < 10 minutes

#### TRIAL 🟡
**Chaos Engineering**
- Platform team running monthly chaos experiments
- 2 teams have adopted for their services
- Waiting for tooling standardization before broad adoption

**Contract Testing**
- API teams experimenting with Pact
- Early results positive (reduced integration test failures by 40%)
- Need to validate across more service pairs

#### ASSESS 🟠
**Micro-Frontends**
- Research spike completed
- Potential solution for our monolithic frontend
- Concerns about complexity and bundle size

**Event Storming**
- DDD team attended workshop
- Considering for next greenfield project
- Need internal facilitator training

#### HOLD ⛔
**Long-Lived Feature Branches**
- Legacy practice from pre-CI/CD era
- All teams migrated to trunk-based development
- No longer acceptable for new projects

---

### Tools Quadrant

#### ADOPT 🟢
**Docker**
- Standard for all containerized applications
- 100% of new services use Docker
- Internal base images maintained

**GitHub Actions**
- CI/CD platform for all repositories
- 200+ workflows in production
- Migration from Jenkins complete

**Datadog**
- Observability platform (metrics, logs, traces)
- All services instrumented
- Incident response playbooks reference Datadog

#### TRIAL 🟡
**K6**
- Load testing tool
- 3 teams using successfully
- Evaluating vs current JMeter usage
- Training materials in development

**Playwright**
- E2E testing framework
- Faster and more reliable than Cypress
- 2 teams migrated, 4 more planning
- Will move to ADOPT after 6-month validation

#### ASSESS 🟠
**Bun**
- Alternative JavaScript runtime
- Spike showed 3x faster CI builds
- Compatibility concerns need investigation
- Monitoring for production readiness

#### HOLD ⛔
**Jenkins**
- Legacy CI/CD platform
- All pipelines migrated to GitHub Actions
- Final instances being decommissioned Q1 2025
- No new usage allowed

---

### Platforms Quadrant

#### ADOPT 🟢
**AWS**
- Primary cloud provider
- 95% of workloads run on AWS
- Deep expertise across organization
- Multi-region setup established

**Kubernetes**
- Container orchestration platform
- All new services deploy to EKS
- Internal platform team provides support
- Best practices documented

**PostgreSQL**
- Default relational database
- Proven at scale (10M+ records)
- DBA team available for support
- RDS for managed deployment

#### TRIAL 🟡
**Cloudflare Workers**
- Edge computing platform
- CDN team running pilot for edge functions
- Evaluating cold start vs Lambda
- Cost comparison in progress

**Supabase**
- Backend-as-a-Service
- 1 internal tool using successfully
- Evaluating for rapid prototyping use cases
- Not for customer-facing apps yet

#### ASSESS 🟠
**Deno Deploy**
- Edge runtime for TypeScript
- Spike showed good performance
- Unclear if needed vs Cloudflare Workers
- Monitoring ecosystem maturity

#### HOLD ⛔
**MongoDB 3.x**
- Outdated version with known issues
- All instances upgraded to 5.x or 6.x
- No new 3.x deployments allowed

---

### Languages & Frameworks Quadrant

#### ADOPT 🟢
**TypeScript**
- Default for all JavaScript/Node.js projects
- Reduces runtime errors by 40%
- Strong typing improves collaboration
- Excellent IDE support

**React 18**
- Frontend framework standard
- Component library built on React
- 15 production applications
- Internal training program established

**Spring Boot (Java)**
- Backend framework for JVM services
- Mature ecosystem and libraries
- Team expertise is deep
- Proven at scale

#### TRIAL 🟡
**Svelte**
- Alternative frontend framework
- 1 production app (positive feedback)
- Smaller bundle size vs React (40% reduction)
- Evaluating for future projects
- Training 2 more teams Q4

**FastAPI (Python)**
- Modern Python web framework
- Data team using for ML services
- Better performance than Flask
- Async support out of box
- Will expand usage to more Python services

#### ASSESS 🟠
**Rust**
- Systems programming language
- Spike for performance-critical service showed promise
- Learning curve is steep (3-4 weeks)
- Evaluating where performance justifies complexity

**Solid.js**
- Reactive UI framework
- Extremely fast (benchmarks impressive)
- Small ecosystem concerns
- Monitoring for production use cases

#### HOLD ⛔
**AngularJS** (Angular 1.x)
- Superseded by Angular (2+) and React
- 3 legacy apps remaining (migration planned)
- No new development allowed
- Final migration target: Q2 2025

**jQuery**
- Legacy library no longer needed
- Modern browsers have native equivalents
- All new code uses vanilla JS or framework
- Acceptable only in legacy maintenance

---

## Radar Metrics & Health

### Metrics to Track

**Overall Health**:
- Total technologies on radar
- Distribution across rings (should match guidelines)
- Average time in TRIAL before ADOPT or removal
- Number of movements per quarter

**Adoption Metrics**:
- % teams using ADOPT technologies
- % projects using non-radar technologies (should be low)
- Time to adopt new technology (ASSESS → ADOPT)

**Engagement Metrics**:
- Technology proposals submitted per quarter
- Survey response rate
- Radar page views
- Slack channel activity

### Red Flags

🚩 **Too many technologies** (>100 entries)
- **Problem**: Overwhelming, hard to maintain
- **Fix**: Consolidate, remove obsolete entries

🚩 **Everything in ADOPT** (>60% in ADOPT)
- **Problem**: Not evolving, stagnant
- **Fix**: Actively assess new technologies

🚩 **Nothing in HOLD** (0% in HOLD)
- **Problem**: Not deprecating old tech
- **Fix**: Audit old technologies, move outdated ones to HOLD

🚩 **Technologies stuck in TRIAL** (>1 year)
- **Problem**: No path forward or backward
- **Fix**: Either commit to ADOPT or move to HOLD

🚩 **Low engagement** (<5 proposals per quarter for 100+ engineers)
- **Problem**: Radar not seen as relevant
- **Fix**: Better communication, success stories, incentivize participation

---

## Tools for Building Your Radar

### Open Source Tools

1. **Thoughtworks Build Your Own Radar**
   - URL: https://www.thoughtworks.com/radar/byor
   - Input: CSV file
   - Output: Interactive HTML radar
   - Pros: Official, well-designed
   - Cons: Limited customization

2. **Zalando Tech Radar**
   - GitHub: https://github.com/zalando/tech-radar
   - Tech: JavaScript, D3.js
   - Pros: Highly customizable, open source
   - Cons: Requires hosting

3. **AOE Tech Radar**
   - GitHub: https://github.com/AOEpeople/aoe_technology_radar
   - Tech: JavaScript, Static site
   - Pros: Beautiful UI, versioning support
   - Cons: More complex setup

### Commercial Tools

1. **Miro / Mural**
   - Collaborative whiteboard
   - Good for workshop facilitation
   - Manual maintenance

2. **Confluence / Notion**
   - Wiki-based radar
   - Easy to update
   - Less visual than radar tools

### DIY Approach

**Simple Spreadsheet**:
```
| Technology | Quadrant | Ring | Status | Last Updated | Owner |
|-----------|----------|------|--------|--------------|-------|
| React     | Languages| Adopt| No change| 2024-10-30  | Frontend Team |
| GraphQL   | Languages| Trial| Moved In | 2024-10-30  | API Team |
```

**Notion Database**:
- Create database with properties: Ring, Quadrant, Status, Description
- Filter views by ring or quadrant
- Easy to maintain, search, and share

---

## Getting Started Checklist

### Week 1: Foundation
- [ ] Review this guide and Thoughtworks examples
- [ ] Decide on quadrant categories (use standard or customize)
- [ ] Define ring criteria for your organization
- [ ] Choose radar visualization tool

### Week 2: Initial Content
- [ ] Inventory current technologies (survey teams)
- [ ] Classify initial set (20-40 technologies)
- [ ] Write descriptions for each
- [ ] Get Architecture team alignment

### Week 3: Process
- [ ] Define proposal process
- [ ] Set update cadence (quarterly recommended)
- [ ] Establish approval workflow
- [ ] Create communication plan

### Week 4: Launch
- [ ] Publish initial radar
- [ ] Announce to organization
- [ ] Host intro session/workshop
- [ ] Gather feedback

### Ongoing
- [ ] Quarterly reviews and updates
- [ ] Track metrics
- [ ] Celebrate successes (technologies moving to ADOPT)
- [ ] Continuously improve process

---

## References

- [Thoughtworks Technology Radar](https://www.thoughtworks.com/radar)
- [Zalando Tech Radar](https://opensource.zalando.com/tech-radar/)
- [Spotify Technology Radar](https://engineering.atspotify.com/2020/06/improving-spotifys-technology-radar/)
- [Build Your Own Technology Radar (Neal Ford)](https://www.thoughtworks.com/insights/articles/build-your-own-technology-radar)
- [AOE Tech Radar Documentation](https://www.aoe.com/tech-radar/)