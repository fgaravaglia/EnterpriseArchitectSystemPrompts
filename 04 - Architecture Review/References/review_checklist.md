# Architecture Review Checklist

A comprehensive, actionable checklist for conducting architecture reviews. Use this to ensure no critical aspect is overlooked during design reviews, implementation reviews, or production readiness assessments.

---

## How to Use This Checklist

### Review Types

**Design Review** (Pre-Implementation):
- Use ALL sections
- Focus on design decisions and trade-offs
- Flag issues before code is written

**Implementation Review** (Mid-Development):
- Use sections 1-8 (skip deployment/operations details)
- Focus on code quality and patterns
- Validate design is being followed

**Production Readiness Review** (Pre-Launch):
- Use ALL sections with extra focus on 6-9
- Focus on operational aspects
- Validate system is ready for production load

### Scoring

For each item, use this scale:
- ✅ **Pass**: Meets requirements, no issues
- ⚠️ **Warning**: Has issues but acceptable with mitigation
- 🚨 **Fail**: Critical issue, must be fixed
- N/A **Not Applicable**: Doesn't apply to this system

### Priority

When issues are found, assign priority:
- **P0 (Critical)**: Must fix before proceeding
- **P1 (High)**: Should fix before production
- **P2 (Medium)**: Fix in next iteration
- **P3 (Low)**: Nice to have, backlog

---

## 1. Functional Requirements

### 1.1 Requirements Coverage

- [ ] All functional requirements have been identified and documented
- [ ] Each requirement is mapped to one or more architectural components
- [ ] No requirements are orphaned (missing architectural support)
- [ ] Component responsibilities are clearly defined
- [ ] No component is doing too much (God component)

**Evidence**: Requirements traceability matrix, component responsibility document

**Common Issues**:
- 🚩 Vague requirements ("system should be fast")
- 🚩 Requirements without architectural home
- 🚩 Overlapping responsibilities between components

---

### 1.2 Use Case Coverage

- [ ] All critical user journeys are documented
- [ ] Each use case has a corresponding sequence diagram
- [ ] Happy path and error paths are both designed
- [ ] Edge cases are identified and handled
- [ ] Data flows support all use cases

**Test**: Walk through top 3 user journeys step-by-step

**Questions to Ask**:
- What happens if payment fails?
- What happens if user session expires mid-transaction?
- How does system handle duplicate requests?

---

### 1.3 Integration Points

- [ ] All external systems are identified
- [ ] Integration protocols are specified (REST, SOAP, gRPC, etc.)
- [ ] Data formats are defined (JSON, XML, Protobuf)
- [ ] Error handling for each integration is designed
- [ ] Timeout and retry policies are specified

**Red Flags**:
- 🚩 "We'll integrate with System X" (no details on how)
- 🚩 Missing error handling for external calls
- 🚩 No timeout values specified

---

## 2. Quality Attributes

### 2.1 Performance

#### Targets Defined

- [ ] Response time targets specified (p50, p95, p99)
- [ ] Throughput targets specified (requests/sec, transactions/sec)
- [ ] Resource utilization targets specified (CPU, memory, network)
- [ ] Targets are quantified (not "fast" or "performant")
- [ ] Targets are validated as achievable

**Example Good Targets**:
- API response time: p95 < 200ms, p99 < 500ms
- Throughput: 10,000 requests/second sustained
- Database queries: p95 < 50ms

#### Performance Architecture

- [ ] Caching strategy defined (what, where, TTL)
- [ ] Database indexing strategy documented
- [ ] Async processing used where appropriate
- [ ] No N+1 query patterns
- [ ] Connection pooling configured
- [ ] CDN used for static assets (if web application)

**Check For**:
- 🚩 No caching at all
- 🚩 Queries in loops (N+1 problem)
- 🚩 Synchronous processing for non-critical operations
- 🚩 Missing database indexes on query columns

#### Load Testing

- [ ] Load testing plan exists
- [ ] Load tests simulate realistic traffic patterns
- [ ] Load tests include peak load scenarios (2-10x normal)
- [ ] Performance benchmarks documented
- [ ] Bottlenecks identified and addressed

---

### 2.2 Scalability

#### Horizontal Scalability

- [ ] Services/components are stateless (or state is externalized)
- [ ] No server affinity required (any request can go to any instance)
- [ ] Shared state stored in cache/database (not local memory)
- [ ] Session data externalized (Redis, database)
- [ ] Auto-scaling policies defined

**Test**: Can you add more instances and handle more load linearly?

#### Vertical Scalability

- [ ] Resource limits understood (CPU, memory, disk, network)
- [ ] Instance size can be increased if needed
- [ ] No hard-coded limits that prevent scaling

#### Database Scalability

- [ ] Database can handle projected data volume (5 years out)
- [ ] Read replicas used for read-heavy workloads
- [ ] Database partitioning/sharding strategy exists (if needed)
- [ ] Connection pooling prevents connection exhaustion
- [ ] Indexes support projected query volume

**Red Flags**:
- 🚩 Stateful services (session data in memory)
- 🚩 Server affinity (sticky sessions)
- 🚩 No plan for database growth beyond 10x current size
- 🚩 Single database with no read replicas for read-heavy app

---

### 2.3 Availability & Reliability

#### High Availability

- [ ] Availability target specified (e.g., 99.95%)
- [ ] Single points of failure identified and mitigated
- [ ] Redundancy in place for critical components
- [ ] Health checks implemented for all services
- [ ] Automatic failover configured
- [ ] Multi-AZ or multi-region deployment (if required)

**Calculate Downtime**:
- 99.9% = 8.76 hours/year
- 99.95% = 4.38 hours/year
- 99.99% = 52.6 minutes/year

**Check**:
- [ ] Is calculated availability meeting target?
- [ ] Single component failure = system down? (If yes, 🚨)

#### Resilience Patterns

- [ ] Circuit breaker for external service calls
- [ ] Timeout policies on all network calls
- [ ] Retry policies with exponential backoff
- [ ] Bulkhead pattern to isolate failures
- [ ] Graceful degradation defined
- [ ] Fallback mechanisms implemented

**Test Each External Integration**:
- What happens if it times out?
- What happens if it returns errors?
- What happens if it's completely down?

#### Disaster Recovery

- [ ] RTO (Recovery Time Objective) defined
- [ ] RPO (Recovery Point Objective) defined
- [ ] Backup strategy documented (frequency, retention)
- [ ] Backup restoration tested
- [ ] Disaster recovery runbook exists
- [ ] Failover procedures documented and tested

**Questions**:
- Can you restore from backup in less than RTO?
- How much data would you lose? (Is it less than RPO?)
- When was the last DR test?

---

### 2.4 Security

#### Authentication & Authorization

- [ ] Authentication mechanism specified (OAuth, SAML, JWT, etc.)
- [ ] Authorization model defined (RBAC, ABAC, etc.)
- [ ] User roles and permissions documented
- [ ] MFA available for privileged accounts
- [ ] Session management strategy defined
- [ ] Password policy defined (if applicable)

**Check**:
- [ ] No hardcoded credentials in code/config
- [ ] Secrets stored in secrets manager (Vault, AWS Secrets Manager)
- [ ] API keys have appropriate scopes (least privilege)

#### Data Protection

- [ ] Sensitive data identified (PII, PCI, PHI)
- [ ] Data encrypted at rest (algorithm specified: AES-256, etc.)
- [ ] Data encrypted in transit (TLS 1.3 minimum)
- [ ] Data classification policy exists
- [ ] Data retention policy defined
- [ ] Data deletion/anonymization strategy (GDPR right to be forgotten)

**Red Flags**:
- 🚩 No encryption for sensitive data
- 🚩 TLS 1.0 or 1.1 (deprecated, insecure)
- 🚩 Credit card data stored (PCI DSS violation unless certified)
- 🚩 No data classification

#### Application Security

- [ ] Input validation on all user inputs
- [ ] Output encoding/escaping (XSS prevention)
- [ ] Parameterized queries (SQL injection prevention)
- [ ] CSRF protection implemented
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] Rate limiting to prevent abuse
- [ ] API authentication on all endpoints

**OWASP Top 10 Check**:
- [ ] Protection against injection attacks
- [ ] Broken authentication mitigated
- [ ] Sensitive data exposure prevented
- [ ] XXE (XML External Entities) prevented
- [ ] Broken access control mitigated
- [ ] Security misconfiguration avoided
- [ ] XSS (Cross-Site Scripting) prevented
- [ ] Insecure deserialization mitigated
- [ ] Components with known vulnerabilities avoided
- [ ] Insufficient logging & monitoring addressed

#### Compliance

- [ ] Compliance requirements identified (GDPR, HIPAA, PCI DSS, SOC 2)
- [ ] Compliance controls mapped to architecture
- [ ] Audit logging implemented (who did what when)
- [ ] Audit logs are immutable and tamper-proof
- [ ] Data residency requirements met (data stored in correct regions)
- [ ] Compliance certifications obtained (if required)

---

### 2.5 Maintainability

#### Code Organization

- [ ] Clear module/package structure
- [ ] Appropriate use of design patterns
- [ ] No god classes/components
- [ ] Low coupling between modules
- [ ] High cohesion within modules
- [ ] Dependency direction is correct (no circular dependencies)

**Metrics**:
- [ ] Cyclomatic complexity < 10 per method
- [ ] Class/module size reasonable (< 500 lines)
- [ ] Code duplication < 5%

#### Testing

- [ ] Unit test coverage > 80% for business logic
- [ ] Integration tests for critical paths
- [ ] E2E tests for key user journeys
- [ ] Test data management strategy
- [ ] Tests run in CI/CD pipeline
- [ ] Tests are reliable (not flaky)

**Test Pyramid Check**:
- Many unit tests (60%+)
- Some integration tests (30%)
- Few E2E tests (10%)

#### Documentation

- [ ] Architecture documentation exists and is current
- [ ] ADRs (Architecture Decision Records) for major decisions
- [ ] API documentation (OpenAPI/Swagger for REST)
- [ ] Code-level documentation for complex logic
- [ ] README with setup instructions
- [ ] Runbooks for operations

**Test**: Can a new team member onboard from documentation alone?

---

## 3. Technology Choices

### 3.1 Technology Selection

- [ ] Technology choices are justified (ADRs exist)
- [ ] Technologies are mature and production-ready
- [ ] Technologies match the use case (not resume-driven)
- [ ] Team has expertise or can acquire it in timeframe
- [ ] Operational complexity is manageable
- [ ] Vendor lock-in risks assessed
- [ ] Licensing costs understood and budgeted

**Questions for Each Technology**:
- Why this technology over alternatives?
- Does the team know it?
- Can we operate it in production?
- What if it's abandoned by maintainers?
- What's the total cost of ownership?

**Red Flags**:
- 🚩 Bleeding-edge tech (v0.x) for critical systems
- 🚩 No evaluation of alternatives
- 🚩 Technology choice not documented
- 🚩 Team has zero experience and tight timeline

---

### 3.2 Technology Stack Coherence

- [ ] Technologies are compatible with each other
- [ ] No conflicting dependencies or requirements
- [ ] Technology versions are specified
- [ ] All technologies actively maintained
- [ ] Upgrade path exists for all technologies

**Check**:
- Are we mixing incompatible versions? (Python 2 + Python 3)
- Are there known conflicts? (Library A and Library B don't work together)

---

## 4. Architecture Patterns

### 4.1 Pattern Selection

- [ ] Architectural patterns are explicitly named (Microservices, Layered, Event-Driven, etc.)
- [ ] Pattern choice is justified for context
- [ ] Patterns are applied consistently
- [ ] Pattern trade-offs are understood and acceptable
- [ ] No pattern over-engineering

**Check Each Pattern**:
- **Microservices**: Do you have team size and need for independence?
- **Event-Driven**: Do you need async communication and eventual consistency is OK?
- **CQRS**: Do you have complex read requirements different from write?
- **Saga**: Do you need distributed transactions across services?

**Red Flags**:
- 🚩 Microservices for 3-person team
- 🚩 CQRS for simple CRUD app
- 🚩 Event-driven for everything (including synchronous workflows)

---

### 4.2 Anti-Patterns

Check against common anti-patterns:

**Microservices Anti-Patterns**:
- [ ] No distributed monolith (services share database)
- [ ] No god service (service doing too much)
- [ ] No chatty APIs (too many round trips)
- [ ] Services have clear bounded contexts

**Data Anti-Patterns**:
- [ ] No N+1 query problem
- [ ] No anemic domain model (business logic in services, not domain)
- [ ] No database as integration point
- [ ] Clear data ownership per service

**Integration Anti-Patterns**:
- [ ] No long synchronous call chains (A→B→C→D)
- [ ] Circuit breakers for external calls
- [ ] No retry storms (exponential backoff + jitter)

**See**: `anti-patterns-catalog.md` for complete list

---

## 5. Data Architecture

### 5.1 Data Model

- [ ] Data model documented (ER diagrams, schema)
- [ ] Data model matches domain
- [ ] Normalization level is appropriate (usually 3NF)
- [ ] Denormalization is justified (performance optimization)
- [ ] No redundant data (without clear purpose)

---

### 5.2 Database Selection

- [ ] Database type matches use case (Relational, NoSQL, Cache, etc.)
- [ ] ACID requirements are met (or eventual consistency is acceptable)
- [ ] Database can handle projected scale
- [ ] Database choice is justified (ADR)

**Match Database to Use Case**:
- **Transactional data**: Relational (PostgreSQL, MySQL)
- **Document storage**: Document DB (MongoDB, DynamoDB)
- **Caching**: Redis, Memcached
- **Full-text search**: Elasticsearch
- **Time-series**: InfluxDB, TimescaleDB
- **Graph**: Neo4j

---

### 5.3 Data Ownership

- [ ] Each service owns its data (microservices)
- [ ] No shared database between services
- [ ] Clear which service is source of truth for each entity
- [ ] Data duplication is intentional (cached for performance)
- [ ] Data synchronization strategy defined (events, API calls)

**Test**: Draw data ownership boundaries. Any overlaps? 🚨

---

### 5.4 Data Management

- [ ] Migration strategy defined (schema changes, data migrations)
- [ ] Backup and restore procedures documented
- [ ] Data archival strategy (for old data)
- [ ] Data retention policy (how long to keep data)
- [ ] Data deletion strategy (GDPR compliance)

---

## 6. Integration & APIs

### 6.1 API Design

- [ ] API style chosen and justified (REST, GraphQL, gRPC)
- [ ] API contracts documented (OpenAPI, Protocol Buffers)
- [ ] Consistent naming conventions
- [ ] Proper HTTP status codes (REST)
- [ ] Pagination for list endpoints
- [ ] Filtering and sorting supported
- [ ] API versioning strategy defined

**REST Checklist**:
- [ ] Nouns for resources, not verbs (`/orders` not `/getOrders`)
- [ ] HTTP methods used correctly (GET, POST, PUT, PATCH, DELETE)
- [ ] 2xx for success, 4xx for client errors, 5xx for server errors
- [ ] Idempotent operations (PUT, DELETE)

---

### 6.2 API Versioning

- [ ] Versioning strategy defined (URL, header, content negotiation)
- [ ] Backward compatibility considered
- [ ] Deprecation policy documented
- [ ] Version upgrade path clear

**Example**:
- URL versioning: `/api/v1/orders`, `/api/v2/orders`
- Header versioning: `Accept: application/vnd.myapp.v2+json`

---

### 6.3 Error Handling

- [ ] Consistent error response format
- [ ] Error codes/types defined
- [ ] Error messages are helpful (not just "error")
- [ ] Sensitive information not leaked in errors
- [ ] Correlation IDs in errors (for tracing)

**Example Error Format**:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid order data",
    "details": [
      {"field": "email", "message": "Invalid email format"}
    ],
    "requestId": "abc-123-def"
  }
}
```

---

### 6.4 Communication Patterns

- [ ] Synchronous vs asynchronous usage is appropriate
- [ ] Timeout values specified for all sync calls
- [ ] Retry policies defined (exponential backoff)
- [ ] Circuit breaker pattern for external services
- [ ] Idempotency keys for critical operations

**Decision Matrix**:
| Use Case | Pattern |
|----------|---------|
| Need immediate response | Synchronous (REST, gRPC) |
| Fire-and-forget | Asynchronous (Message queue) |
| Multiple consumers | Pub/Sub (Kafka, SNS) |
| Workflow orchestration | Saga pattern |

---

## 7. Deployment & Operations

### 7.1 Deployment Strategy

- [ ] Deployment strategy defined (Blue-green, Canary, Rolling)
- [ ] Deployment is automated (CI/CD pipeline)
- [ ] Infrastructure as Code (Terraform, CloudFormation)
- [ ] Environment parity (dev, staging, production similar)
- [ ] Configuration externalized (12-factor app)
- [ ] Secrets management integrated

**Zero-Downtime Deployment**:
- [ ] Health checks prevent traffic to unhealthy instances
- [ ] Old version kept running during deployment
- [ ] Rollback is quick (<5 minutes)

---

### 7.2 Monitoring & Observability

#### Logging

- [ ] Centralized logging (ELK, Loki, CloudWatch)
- [ ] Structured logging (JSON format)
- [ ] Appropriate log levels (ERROR, WARN, INFO, DEBUG)
- [ ] Correlation IDs across services
- [ ] Log retention policy defined
- [ ] PII not logged

#### Metrics

- [ ] Application metrics collected (Prometheus, CloudWatch)
- [ ] Infrastructure metrics collected (CPU, memory, disk)
- [ ] Business metrics tracked (orders/hour, revenue, etc.)
- [ ] Dashboards created for common queries
- [ ] RED metrics for services (Rate, Errors, Duration)

**Key Metrics**:
- Request rate (requests/second)
- Error rate (errors/second, percentage)
- Latency (p50, p95, p99)
- Saturation (resource utilization)

#### Tracing

- [ ] Distributed tracing implemented (Jaeger, X-Ray, Zipkin)
- [ ] Trace context propagated across services
- [ ] Sampling configured (10% in prod, 100% in staging)
- [ ] Trace visualization available

#### Alerting

- [ ] Alerts defined for critical metrics
- [ ] Alert thresholds based on SLOs
- [ ] Alert fatigue avoided (not too many alerts)
- [ ] On-call rotation defined
- [ ] Runbooks for common alerts

---

### 7.3 Scaling Strategy

- [ ] Auto-scaling configured (horizontal pod autoscaling)
- [ ] Scaling triggers defined (CPU, memory, custom metrics)
- [ ] Scaling limits set (min/max instances)
- [ ] Load testing validates scaling behavior
- [ ] Cost implications of scaling understood

---

### 7.4 Operational Runbooks

- [ ] Runbooks exist for common operations
- [ ] Deployment procedures documented
- [ ] Rollback procedures documented
- [ ] Incident response procedures
- [ ] Disaster recovery procedures
- [ ] Database maintenance procedures (backups, migrations)

**Test**: Can someone not on the team deploy using the runbook?

---

## 8. Team & Organization

### 8.1 Team Structure

- [ ] Team size is appropriate for architecture complexity
- [ ] Team structure matches architecture (Conway's Law)
- [ ] Clear ownership of services/components
- [ ] Skills match technology choices
- [ ] Training plan for skill gaps

**Conway's Law**: Organizations design systems that mirror their communication structure.
- Microservices → Multiple small teams
- Monolith → Single team

---

### 8.2 Skills & Expertise

- [ ] Team has necessary technical skills
- [ ] Team has operational skills (or DevOps support)
- [ ] Knowledge is distributed (no single points of failure)
- [ ] Onboarding documentation for new team members
- [ ] Mentoring/pairing for knowledge transfer

**Red Flags**:
- 🚩 Only one person knows critical system
- 🚩 Team has zero experience with chosen tech stack
- 🚩 No plan to acquire necessary skills

---

### 8.3 Process & Practices

- [ ] Code review process defined and followed
- [ ] Definition of Done includes architecture review
- [ ] Regular architecture sync meetings
- [ ] ADRs created for significant decisions
- [ ] Post-mortems for incidents
- [ ] Continuous improvement culture

---

## 9. Cost & Budget

### 9.1 Cost Estimation

- [ ] Infrastructure costs estimated
- [ ] Licensing costs understood
- [ ] Operational costs estimated (24/7 on-call, monitoring tools)
- [ ] Development costs estimated
- [ ] Total Cost of Ownership (TCO) calculated

**TCO Formula**:
```
TCO = Infrastructure + Licenses + Development + Operations + Training + Migration
```

---

### 9.2 Cost Optimization

- [ ] Right-sizing of resources (not over-provisioned)
- [ ] Reserved instances for steady-state workload
- [ ] Auto-scaling to optimize costs
- [ ] Data storage lifecycle policies (archive old data)
- [ ] Cost monitoring and alerts configured

---

## 10. Risk Assessment

### 10.1 Technical Risks

- [ ] Technical risks identified
- [ ] Risk probability and impact assessed
- [ ] Mitigation strategies defined
- [ ] Risk owners assigned

**Common Technical Risks**:
- Third-party service dependency
- Data migration complexity
- Performance at scale
- Security vulnerabilities
- Technology maturity

---

### 10.2 Delivery Risks

- [ ] Timeline is realistic
- [ ] Dependencies identified
- [ ] Critical path identified
- [ ] Buffer time included for unknowns

---

### 10.3 Operational Risks

- [ ] Team capacity to operate assessed
- [ ] Operational complexity manageable
- [ ] Disaster scenarios planned for
- [ ] Incident response capability validated

---

## Summary Scoring

| Category | Pass | Warning | Fail | N/A |
|----------|------|---------|------|-----|
| 1. Functional Requirements | ___ | ___ | ___ | ___ |
| 2. Quality Attributes | ___ | ___ | ___ | ___ |
| 3. Technology Choices | ___ | ___ | ___ | ___ |
| 4. Architecture Patterns | ___ | ___ | ___ | ___ |
| 5. Data Architecture | ___ | ___ | ___ | ___ |
| 6. Integration & APIs | ___ | ___ | ___ | ___ |
| 7. Deployment & Operations | ___ | ___ | ___ | ___ |
| 8. Team & Organization | ___ | ___ | ___ | ___ |
| 9. Cost & Budget | ___ | ___ | ___ | ___ |
| 10. Risk Assessment | ___ | ___ | ___ | ___ |

**Overall Assessment**: 
- ✅ **Approve**: No critical issues
- ⚠️ **Approve with Conditions**: Some issues must be fixed
- 🚨 **Revise**: Too many critical issues, needs redesign

---

## Quick Reference: Top Issues to Look For

### Critical Issues (Always Check)

1. **Single Points of Failure** in critical path
2. **No Circuit Breakers** for external services
3. **Shared Database** between microservices
4. **Secrets in Code** or configuration files
5. **No Input Validation** (SQL injection, XSS risk)
6. **No Disaster Recovery** plan
7. **No Monitoring/Observability**
8. **Performance Targets** not validated
9. **N+1 Query Problem**
10. **Long Synchronous Call Chains**

---

**Checklist Version**: 1.0  
**Last Updated**: 2024-10-30  
**Maintained by**: Enterprise Architecture Team