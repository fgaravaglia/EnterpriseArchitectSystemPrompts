# Example Assessment Prompts - Technology Comparison Scenarios

This file contains ready-to-use prompts for common technology assessment scenarios. Copy, customize with your specific context, and use with the Technology Assessment system prompt.

---

## How to Use These Prompts

1. **Copy the base prompt** for your scenario
2. **Customize the context** with your specific details:
   - Team size and skills
   - Current tech stack
   - Budget constraints
   - Timeline requirements
   - Scale requirements
3. **Add specific requirements** unique to your situation
4. **Run the assessment** with the Technology Assessment system prompt
5. **Follow up** with clarifying questions as needed

---

## Database Selection Scenarios

### Scenario 1: Primary Database for New Application

```
I need help selecting a database for a new e-commerce application.

CONTEXT:
- Application: E-commerce platform (product catalog, orders, customers)
- Expected scale: 500K products, 20K orders/day initially, 100K orders/day in 2 years
- Team: 5 backend engineers (3 know PostgreSQL, 2 know MySQL, 0 know NoSQL)
- Budget: Max $4K/month for database infrastructure
- Timeline: Launch in 6 months
- Deployment: AWS cloud

REQUIREMENTS:
Functional:
- Strong consistency for orders and payments (ACID required)
- Complex queries (joins, aggregations) for analytics
- Full-text search for product catalog
- Flexible schema for product attributes (variants, custom fields)

Non-functional:
- Read latency p95 < 50ms
- Write latency p95 < 100ms
- 99.95% availability
- GDPR compliant
- PCI DSS Level 1 for payment data

CONSTRAINTS:
- Must be production-ready (no beta/experimental)
- Team must be productive within 1 month
- Must support our compliance requirements

CANDIDATES TO EVALUATE:
1. PostgreSQL 15 (AWS RDS)
2. MongoDB 7 (Atlas)
3. MySQL 8 (AWS RDS)
4. Amazon DynamoDB

Please provide:
1. Detailed comparison matrix across all key dimensions
2. Benchmark performance estimates for our workload
3. 3-year TCO calculation
4. Clear recommendation with confidence level
5. Risk assessment for top 2 choices
6. Next steps (POC plan if needed)
```

### Scenario 2: Migration from Existing Database

```
We're considering migrating from MySQL to a different database for better performance and features.

CURRENT SITUATION:
- Database: MySQL 5.7 (on-premise, single instance)
- Data: 50M records across 30 tables
- Traffic: 5K queries/sec peak, mostly reads (80/20 split)
- Pain points:
  - Slow full-text search (impacting user experience)
  - JSON support is limited (we store product attributes in JSON)
  - Hitting vertical scaling limits (96GB RAM instance maxed out)
  - No automatic failover (manual process takes 30+ minutes)

REQUIREMENTS:
- Better full-text search performance
- Rich JSON/document support
- Horizontal scaling capability
- High availability with automatic failover
- Minimal application changes (ideally)

CONSTRAINTS:
- Budget: Current cost is $2K/month, max increase 50% ($3K/month)
- Timeline: Must complete migration within 4 months
- Downtime: Max 4 hours for cutover
- Team: 3 DBAs familiar with MySQL, limited time for training

CANDIDATES:
1. PostgreSQL (for better JSON and full-text search)
2. MongoDB (for native document model and scaling)
3. MySQL 8.0 with optimizations (incremental improvement)
4. Aurora MySQL (AWS managed, better performance)

Please assess:
1. Migration complexity for each option
2. Performance improvement estimates
3. Feature comparison for our pain points
4. Migration cost (effort + downtime)
5. Operational complexity change
6. Recommendation with migration strategy
```

### Scenario 3: Analytical Database Selection

```
We need to select a database for our analytics and reporting workload.

USE CASE:
- Purpose: Business intelligence, reporting, data warehouse
- Data sources: Operational PostgreSQL database (10M records), API logs, event streams
- Users: 50 business analysts running ad-hoc queries
- Update frequency: Hourly ETL from operational systems

QUERY PATTERNS:
- Large aggregations across millions of rows
- Complex joins (5-10 tables)
- Time-series analysis
- Rarely update data (append-only mostly)

SCALE:
- Data volume: 500GB now, growing 50GB/month
- Query concurrency: 20-30 simultaneous queries
- Acceptable query latency: Seconds to minutes (not milliseconds)

CANDIDATES:
1. PostgreSQL with columnar extension (Citus or TimescaleDB)
2. ClickHouse (columnar OLAP database)
3. Snowflake (cloud data warehouse)
4. Amazon Redshift

Evaluate on:
- Query performance for OLAP workloads
- Cost (including data storage growth)
- Ease of ETL integration
- SQL compatibility (analysts know SQL)
- Operational overhead
```

---

## Frontend Framework Selection

### Scenario 4: Framework for New Web Application

```
We're starting a new customer-facing web application and need to choose a frontend framework.

APPLICATION:
- Type: SaaS dashboard (B2B product)
- Complexity: High (real-time data, charts, complex forms)
- Users: Desktop primarily (90%), mobile secondary
- Expected traffic: 10K daily active users initially

TEAM:
- Size: 4 frontend engineers, 3 backend engineers
- Current skills: 2 engineers know React, 1 knows Vue, 1 knows vanilla JS
- Hiring: Planning to hire 2 more frontend engineers in 6 months

REQUIREMENTS:
Technical:
- TypeScript support (must have)
- Component reusability
- State management for complex data
- Real-time updates (WebSocket integration)
- Good testing support
- SEO not critical (behind login)

Business:
- Fast time to market (launch in 5 months)
- Long-term maintainability (10+ year product lifecycle)
- Low hiring friction (easy to find developers)

CANDIDATES:
1. React 18 (current team knowledge)
2. Vue 3 (some team knowledge)
3. Svelte (smaller bundle, better performance)
4. Angular (enterprise-focused)
5. Solid.js (React-like but faster)

Assess on:
- Learning curve given team skills
- Development velocity
- Performance (bundle size, runtime speed)
- Ecosystem maturity
- Hiring pool availability
- Long-term viability
```

### Scenario 5: Migration from Legacy Framework

```
We have a large application in AngularJS (Angular 1.x) that needs modernization.

CURRENT STATE:
- Framework: AngularJS 1.6
- Codebase: 200K lines of code, 500+ components
- Age: 7 years old
- Technical debt: High (patterns outdated, hard to test)
- Performance: Slow (complex two-way binding)

BUSINESS DRIVERS:
- AngularJS end of life (security risk)
- Hiring difficulty (few developers know AngularJS)
- Feature velocity declined (takes 2x longer than 2 years ago)
- User complaints about performance

CONSTRAINTS:
- Cannot rewrite from scratch (too risky, business won't accept downtime)
- Must migrate incrementally (strangler fig pattern)
- Budget: $500K over 18 months (5 engineers full-time)
- Must maintain feature delivery during migration

MIGRATION OPTIONS:
1. Angular (natural upgrade path, but still learning curve)
2. React (most popular, large talent pool)
3. Vue (gentler learning curve, good for incremental migration)
4. Svelte (modern, but smaller ecosystem)

Evaluate:
- Incremental migration feasibility (can we run both side-by-side?)
- Migration effort estimation
- Performance improvement expected
- Team retraining requirements
- Risk assessment
- Recommended migration strategy with phases
```

---

## Cloud Provider Selection

### Scenario 6: Primary Cloud Provider Choice

```
We're a startup moving from on-premise to cloud and need to select our primary cloud provider.

COMPANY:
- Stage: Series A startup, 30 employees
- Revenue: $2M ARR, growing 200% YoY
- Product: B2B SaaS platform
- Technical team: 10 engineers

CURRENT:
- Hosting: Co-located servers (expensive, limited scalability)
- Monthly cost: $15K/month

REQUIREMENTS:
Infrastructure:
- Compute: Kubernetes for microservices (8 services currently)
- Database: Managed PostgreSQL, Redis
- Object storage: 500GB media files, growing 100GB/month
- CDN: Global delivery (US, Europe, Asia)
- Monitoring: Metrics, logs, tracing

Scale:
- Current: 5K daily active users
- Projected: 50K DAU in 12 months
- Need to scale quickly during customer launches

Compliance:
- SOC 2 Type II (required by enterprise customers)
- GDPR (European customers)

CANDIDATES:
1. AWS (most mature, largest service catalog)
2. Azure (good for enterprises, .NET friendly)
3. GCP (strong in data/ML, good pricing)

Budget: Target $10K/month initially, accept up to $20K for right choice

Evaluate:
- Service offerings for our needs
- Pricing comparison (estimate monthly cost)
- Learning curve (team has minimal cloud experience)
- Support options
- Compliance certifications
- Multi-region deployment capability
- Lock-in risk
```

### Scenario 7: Multi-Cloud Strategy

```
We're on AWS currently but considering multi-cloud strategy.

CURRENT SITUATION:
- Primary: AWS (100% of workloads)
- Spend: $80K/month
- Dependency: Deep AWS integration (RDS, ElastiCache, CloudWatch, etc.)

DRIVERS FOR MULTI-CLOUD:
- Vendor lock-in concerns (AWS increases pricing 15% annually)
- Negotiating leverage (want better pricing)
- Reliability (single cloud provider risk)
- Compliance (some customers require multi-cloud)

CONCERNS:
- Complexity (managing multiple clouds)
- Cost (duplicated infrastructure, tooling)
- Team expertise (engineers know AWS deeply)

OPTIONS:
1. Stay single-cloud AWS (optimize costs instead)
2. Add Azure for specific workloads (hybrid)
3. Add GCP for specific workloads (hybrid)
4. Full multi-cloud with abstraction layer (Terraform, Kubernetes)

CONSTRAINTS:
- Cannot migrate everything (too disruptive)
- Must maintain current SLA (99.95%)
- Team bandwidth limited (3 platform engineers)

Assess:
- True benefits vs complexity for our scale
- Which workloads good candidates for multi-cloud
- Cost analysis (including operational overhead)
- Risk assessment
- Phased approach if recommended
```

---

## Architecture Pattern Selection

### Scenario 8: Microservices vs Modular Monolith

```
We're designing a new platform and debating architecture approach.

PROJECT:
- Product: Order management system for e-commerce
- Scope: Order processing, inventory, payments, fulfillment
- Timeline: 12 months to launch
- Expected scale: 10K orders/day initially, 100K in 2 years

TEAM:
- Size: 8 backend engineers, 2 frontend engineers
- Structure: Single team currently, may split into 2 teams in 6 months
- Experience: Built monoliths before, limited microservices experience
- Location: Co-located (same office)

CURRENT THINKING:
Some engineers advocate for microservices for "scalability and team autonomy."
Others prefer starting with modular monolith for "simplicity and faster delivery."

REQUIREMENTS:
- Independent deployment of order processing (critical path)
- Different scaling needs (inventory checks 10x more frequent than orders)
- May need to replace payment provider in future
- Analytics team wants to query order data without impacting operations

NON-FUNCTIONAL:
- Availability: 99.95%
- Latency: p95 < 200ms for order creation
- Must handle 2x traffic spikes during promotions

OPTIONS:
1. Microservices from day one (separate services for orders, inventory, payments, fulfillment)
2. Modular monolith (clean boundaries, but single deployment)
3. Hybrid (monolith with extracted services for specific needs)
4. Monolith now, migrate to microservices later (evolutionary architecture)

Evaluate:
- Complexity vs team capability
- Time to market impact
- Operational overhead
- Testing complexity
- Cost implications
- When does microservices complexity pay off for our scale
- Recommendation with reasoning
```

### Scenario 9: Event-Driven vs Request-Response

```
We need to decide on integration pattern for service communication.

CONTEXT:
- Architecture: Microservices (12 services)
- Current: Synchronous REST APIs between services
- Pain points:
  - Cascading failures (one service down affects many)
  - Tight coupling (changes require coordinated deployments)
  - Performance issues (sequential calls add latency)

EXAMPLE FLOW:
Order created → Inventory reserved → Payment processed → Fulfillment triggered → Notification sent

Current: Synchronous chain (takes 2-3 seconds, error-prone)

OPTIONS:
1. Keep synchronous REST (add circuit breakers, retries)
2. Event-driven with message queue (RabbitMQ or Kafka)
3. Hybrid (sync for critical path, async for non-critical)

REQUIREMENTS:
- Reduce cascading failures
- Improve resilience
- Acceptable eventual consistency for some operations
- Must maintain strong consistency for payments

CONCERNS:
- Event-driven complexity (debugging, monitoring)
- Team learning curve (no experience with message brokers)
- Operational overhead (managing Kafka/RabbitMQ)

Evaluate:
- Trade-offs for our specific use case
- Which communication patterns for which interactions
- Message broker comparison (Kafka vs RabbitMQ vs AWS SQS)
- Migration strategy from current state
- Complexity increase justified by benefits?
```

---

## API Style Selection

### Scenario 10: REST vs GraphQL vs gRPC

```
We're building a new API platform and need to choose API style.

USE CASES:
1. Mobile app (iOS, Android) - consumer-facing
2. Web dashboard - internal users
3. Partner integrations - external companies
4. Internal microservice communication

CURRENT:
- RESTful APIs (15 endpoints)
- Over-fetching problem (mobile gets too much data, wastes bandwidth)
- Under-fetching problem (mobile needs 3-4 calls for one screen)
- No strong typing (errors caught at runtime)

REQUIREMENTS BY USE CASE:

Mobile app:
- Minimize bandwidth (users on cellular)
- Minimize round trips (latency sensitive)
- Flexible queries (different screens need different data)

Web dashboard:
- Rich queries (filters, sorting, pagination)
- Real-time updates (WebSocket-like)

Partner integrations:
- Stable contracts (versioning important)
- Good documentation
- Wide language support

Internal services:
- High performance (low latency)
- Type safety
- Efficient serialization

CANDIDATES:
1. REST (status quo, well understood)
2. GraphQL (solves over/under-fetching, flexible)
3. gRPC (performance, type safety, but less adoption)
4. Hybrid (different styles for different use cases)

TEAM:
- 6 backend engineers (all know REST, none know GraphQL or gRPC)
- 3 mobile engineers (interested in GraphQL)

Evaluate:
- Which API style for which use case
- Learning curve and team productivity impact
- Performance comparison
- Tooling and ecosystem
- Client library support
- Versioning strategy
- Migration path from current REST APIs
```

---

## CI/CD Tool Selection

### Scenario 11: CI/CD Platform Choice

```
We're moving from Jenkins to a modern CI/CD platform.

CURRENT SITUATION:
- Tool: Jenkins (self-hosted, 5 years old)
- Jobs: 200+ pipelines
- Pain points:
  - Maintenance burden (plugins break, upgrades scary)
  - Slow builds (1 hour for full test suite)
  - Limited cloud integration
  - UI outdated
  - Groovy DSL hard to maintain

REQUIREMENTS:
- Support for microservices (12 services, independent deployments)
- Multiple environments (dev, staging, production)
- GitHub integration (code is on GitHub)
- Docker build and push
- Kubernetes deployment
- Secrets management
- PR checks (test, lint, security scan)

SCALE:
- 15 engineers pushing code daily
- 50+ deployments per day
- 10K+ builds per month

CANDIDATES:
1. GitHub Actions (native GitHub integration)
2. GitLab CI (considering moving from GitHub to GitLab)
3. CircleCI (cloud-native, fast)
4. Jenkins X (modern Jenkins for Kubernetes)
5. AWS CodePipeline (AWS-native)

CONSTRAINTS:
- Budget: Current Jenkins costs $2K/month (infrastructure), willing to pay up to $5K/month
- Migration: Must be completed in 3 months
- Cannot have downtime during migration

Evaluate:
- Ease of migration from Jenkins
- Build performance
- Cost comparison
- GitHub integration quality
- Kubernetes deployment support
- Secret management
- Learning curve
- Vendor lock-in risk
```

---

## Monitoring & Observability

### Scenario 12: Observability Platform Selection

```
We need an observability platform for our microservices architecture.

CONTEXT:
- Architecture: 15 microservices on Kubernetes (AWS EKS)
- Current: CloudWatch (basic), application logs to files
- Problems:
  - Hard to trace requests across services
  - No unified view of metrics
  - Log aggregation is manual
  - Cannot debug production issues quickly (MTTR > 2 hours)

REQUIREMENTS:
Metrics:
- Application metrics (latency, throughput, errors)
- Infrastructure metrics (CPU, memory, network)
- Business metrics (orders/min, revenue)
- Alerting on SLOs

Logging:
- Centralized log aggregation
- Full-text search
- Structured logging support
- Retention: 30 days

Tracing:
- Distributed tracing across microservices
- Request correlation
- Performance profiling

SCALE:
- 15 services
- 100 req/sec currently, 1000 req/sec in 12 months
- 50GB logs per day

TEAM:
- 2 SREs
- 10 engineers (need to access for debugging)

CANDIDATES:
1. Datadog (popular, comprehensive, expensive)
2. New Relic (APM focused)
3. Grafana Stack (Prometheus + Loki + Tempo, open source)
4. AWS native (CloudWatch + X-Ray, cheaper but limited)
5. Elastic Stack (ELK, familiar to team)

BUDGET:
- Current: $500/month (CloudWatch)
- Willing to invest: Up to $3K/month for right solution

Evaluate:
- Feature completeness
- Ease of integration (K8s, AWS)
- Cost at our scale (and projected scale)
- Learning curve
- Alerting capabilities
- Query performance
- Vendor lock-in
```

---

## Message Broker Selection

### Scenario 13: Message Broker for Event-Driven Architecture

```
We're adopting event-driven architecture and need to select a message broker.

ARCHITECTURE:
- Current: Synchronous REST between services
- Target: Event-driven with async messaging
- Services: 12 microservices
- Events: Order lifecycle, inventory updates, notifications

EVENT CHARACTERISTICS:
- Volume: 10K events/day currently, 100K in 12 months
- Patterns: Pub/sub (one event, multiple consumers)
- Ordering: Required for order events, not required for notifications
- Retention: 7 days for replay/debugging
- Delivery: At-least-once acceptable (idempotent consumers)

USE CASES:
1. Order processing (critical, low latency)
2. Inventory sync (high volume, less critical)
3. User notifications (fire-and-forget)
4. Analytics events (batch processing)

TEAM:
- 8 engineers (no Kafka experience, some RabbitMQ experience)
- 1 platform engineer (will manage broker)

REQUIREMENTS:
- Reliability (99.9% availability)
- Observability (message tracking, dead letter queues)
- Multi-tenancy (different services don't interfere)
- Schema evolution (events change over time)

CANDIDATES:
1. Apache Kafka (industry standard, complex)
2. RabbitMQ (simpler, team has experience)
3. AWS SQS/SNS (managed, cloud-native)
4. AWS MSK (managed Kafka)
5. Azure Service Bus (if we move to Azure)

CONSTRAINTS:
- Budget: Max $2K/month for infrastructure
- Operations: Limited ops bandwidth, prefer managed
- Deployment: AWS preferred

Evaluate:
- Operational complexity
- Performance for our volume
- Cost comparison (managed vs self-hosted)
- Feature fit for our patterns
- Team learning curve
- Vendor lock-in risk (cloud-native vs portable)
```

---

## Testing Framework Selection

### Scenario 14: E2E Testing Framework

```
We need to select an end-to-end testing framework for our web application.

APPLICATION:
- Type: SaaS web application (React frontend, REST API backend)
- Complexity: Complex forms, multi-step workflows
- Critical paths: User signup, subscription checkout, dashboard interactions

CURRENT STATE:
- Testing: Manual QA (2 QA engineers)
- Coverage: ~30% of features tested manually before release
- Pain: Regression bugs slip through, release cycle slow (1 week)

GOALS:
- Automate critical user journeys
- Run on every PR and before deploy
- Catch regressions early
- Reduce QA time by 50%

REQUIREMENTS:
Technical:
- Test modern web app (SPA with dynamic content)
- Cross-browser (Chrome, Safari, Firefox)
- Run in CI/CD (GitHub Actions)
- Parallel execution (fast feedback)
- Debugging support (screenshots, videos on failure)

Team:
- 6 engineers will write tests
- 2 QA engineers will maintain test suite
- Mixed JavaScript skill levels

CANDIDATES:
1. Cypress (popular, developer-friendly)
2. Playwright (faster, better cross-browser)
3. Selenium (old but stable)
4. TestCafe (no WebDriver needed)

CONSTRAINTS:
- Must integrate with GitHub Actions
- Budget: Prefer open source, can pay for cloud service if compelling
- Timeline: Need basic test suite running in 1 month

Evaluate:
- Ease of writing tests (developer productivity)
- Test stability (flaky tests are worse than no tests)
- Speed (feedback time)
- Debugging experience
- CI/CD integration
- Cross-browser support
- Learning curve
- Community and ecosystem
```

---

## Infrastructure as Code

### Scenario 15: IaC Tool Selection

```
We're adopting Infrastructure as Code and need to choose a tool.

CURRENT STATE:
- Infrastructure: AWS (10+ services)
- Provisioning: Manual via AWS Console (error-prone, slow)
- Environments: Dev, staging, production (often drift out of sync)
- Team: 3 platform engineers, 8 application engineers

GOALS:
- Reproducible infrastructure
- Version controlled (infrastructure in Git)
- Review process (PR for infra changes)
- Consistent environments
- Self-service for developers

INFRASTRUCTURE:
- Compute: EKS (Kubernetes), EC2 instances
- Data: RDS (PostgreSQL), ElastiCache (Redis)
- Networking: VPC, subnets, security groups, load balancers
- Storage: S3 buckets
- Other: CloudFront, Route53, IAM roles

REQUIREMENTS:
- AWS support (primary cloud)
- May need multi-cloud support in 2 years (Azure or GCP)
- State management (must be robust)
- Module reusability (don't repeat common patterns)
- Testing support (validate before apply)

TEAM SKILLS:
- Strong in scripting (Python, Bash)
- Some know Terraform
- No experience with Pulumi or CDK

CANDIDATES:
1. Terraform (de facto standard, HCL)
2. AWS CloudFormation (AWS-native, YAML/JSON)
3. Pulumi (real programming languages)
4. AWS CDK (CloudFormation with code)
5. Ansible (also does config management)

Evaluate:
- Learning curve
- Multi-cloud support (for future)
- State management complexity
- Module ecosystem
- Testing capabilities
- Drift detection
- Team productivity
- Vendor lock-in risk
```

---

## Data Store Selection

### Scenario 16: Caching Solution

```
We need to add caching to our application for performance.

CURRENT PERFORMANCE:
- Database: PostgreSQL (read-heavy, 80% reads)
- Latency: p95 = 300ms (too slow)
- Bottleneck: Repeated queries for same data
- Traffic: 5K requests/sec peak

USE CASES:
1. Session storage (user sessions, JWT tokens)
2. API response caching (product catalog, user profiles)
3. Rate limiting (API throttling)
4. Real-time data (online users, live notifications)

REQUIREMENTS:
- Latency: Sub-millisecond reads
- Availability: 99.9% (can tolerate cache misses)
- Scale: 100M keys, 50GB data
- TTL support (keys expire after N seconds)
- Pub/sub (for real-time features)

CACHE PATTERNS:
- Cache-aside (application manages)
- Write-through (optional, for some data)
- Cache invalidation (on updates)

CANDIDATES:
1. Redis (most popular, rich features)
2. Memcached (simpler, pure cache)
3. Amazon ElastiCache (managed Redis/Memcached)
4. DragonflyDB (Redis-compatible, faster)

TEAM:
- 6 backend engineers
- Familiar with Redis from previous jobs
- Prefer managed solution (limited ops capacity)

CONSTRAINTS:
- AWS deployment preferred
- Budget: Max $1K/month
- Setup time: Need in production in 2 weeks

Evaluate:
- Feature fit for use cases
- Performance at our scale
- Persistence needs (vs pure cache)
- Managed vs self-hosted
- Cost comparison
- Operational complexity
- Redis compatibility (if switching from Redis later)
```

---

## Tips for Getting Better Assessments

### Provide More Context
The more detail you provide, the better the assessment:
- ✅ "Team of 5 with 3 knowing PostgreSQL" 
- ❌ "Small team"

- ✅ "Budget: $3K/month infrastructure"
- ❌ "Limited budget"

- ✅ "Launch in 6 months, 4 months for decision + setup"
- ❌ "Soon"

### Specify Constraints
Clear constraints help eliminate options:
- Must be GDPR compliant
- Team has max 2 weeks for training
- No beta/experimental technologies
- Must support Windows (if relevant)

### Define Success Criteria
What does a good outcome look like?
- "Reduce API latency from 300ms to <100ms"
- "Deploy 10x per day instead of weekly"
- "Reduce cloud cost by 30%"

### Ask Follow-up Questions
After initial assessment, dig deeper:
- "What's the migration complexity from X to Y?"
- "Can you detail the TCO calculation?"
- "What are the top 3 risks with option A?"
- "How would we validate this with a POC?"

### Request Specific Outputs
Tell the AI what format you need:
- "Provide a comparison matrix"
- "Include a 3-year TCO calculation"
- "Create an executive summary for leadership"
- "Give me a POC plan to validate the top choice"

### Challenge the Assessment
Don't accept blindly, probe the reasoning:
- "Why did you score performance as 4/5 instead of 5/5?"
- "Your TCO seems low, did you include training costs?"
- "What if our scale is 10x higher than stated?"
- "The team learning curve seems optimistic, can you revise?"

---

## Common Follow-up Prompts

After receiving an initial assessment:

### Dig Deeper on Recommendation
```
You recommended [Technology A]. Can you elaborate on:
1. Specific migration steps from our current [Technology B]
2. Detailed POC plan to validate your recommendation (2 weeks)
3. What could go wrong and how to mitigate
4. When should we re-evaluate this decision (what would change your mind)
```

### Challenge the Analysis
```
I'm concerned about [specific aspect, e.g., cost/learning curve/performance]. 
Can you:
1. Provide more detail on your [cost/learning/performance] assessment
2. Compare this to the alternative [Technology C] on this dimension specifically
3. Show me the math/data behind your conclusion
4. Suggest how to validate this concern with testing
```

### Request Different Format
```
Can you reformat this assessment as:
1. Executive summary (1 page, for leadership)
2. Technical deep dive (for engineers)
3. Risk assessment matrix (for architecture review board)
4. Decision tree (if X then Y, else Z)
```

### Explore Alternatives
```
You recommended [Technology A] but I'm also interested in [Technology D] which you didn't consider. Can you:
1. Add it to the comparison
2. Explain why it wasn't initially included
3. Under what conditions would it be the better choice
```

### Plan Next Steps
```
Based on your recommendation of [Technology A], create:
1. 2-week POC plan with success criteria
2. Full migration timeline if POC succeeds
3. Training plan for the team
4. Risk mitigation plan for top 3 risks
5. Checklist for making final decision
```

---

## Assessment Output Checklist

A complete assessment should include:

- [ ] **Executive Summary** (recommendation, confidence, key points)
- [ ] **Context Recap** (confirms understanding of your situation)
- [ ] **Comparison Matrix** (all candidates across all dimensions)
- [ ] **Detailed Analysis** (deep dive on top 2-3 choices)
- [ ] **Performance Estimates** (with methodology)
- [ ] **Cost Analysis** (3-year TCO preferred)
- [ ] **Risk Assessment** (for top recommendation)
- [ ] **Trade-off Analysis** (what you gain vs what you lose)
- [ ] **Team Impact** (learning curve, productivity)
- [ ] **Recommendation** (clear winner with conditions)
- [ ] **Confidence Level** (high/medium/low with reasoning)
- [ ] **Next Steps** (actionable items, POC plan)
- [ ] **Decision Triggers** (when to re-evaluate)

If any of these are missing, ask for them!