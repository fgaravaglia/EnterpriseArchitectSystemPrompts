# Quality Attributes Catalog

A comprehensive catalog of software quality attributes based on ISO/IEC 25010 standard, with practical metrics, scenarios, and architectural tactics for each attribute. Use this as reference when documenting quality requirements and architectural decisions.

---

## Understanding Quality Attributes

### What Are Quality Attributes?

**Quality attributes** (also called non-functional requirements or "-ilities") define HOW WELL a system performs its functions, not WHAT functions it performs.

**Examples**:
- ❌ Functional: "System must process customer orders"
- ✅ Quality: "System must process 10K orders/second with p95 latency < 200ms"

### Why Document Them?

Quality attributes:
- **Drive architectural decisions** (performance needs influence technology choices)
- **Enable trade-off analysis** (security vs usability, performance vs maintainability)
- **Provide measurable targets** (99.95% availability vs "highly available")
- **Guide testing strategy** (what to test beyond functional correctness)
- **Justify costs** (why we need that expensive database or monitoring tool)

### ISO/IEC 25010 Quality Model

The international standard organizes quality into 8 main characteristics:

1. **Functional Suitability** - Does it do what it's supposed to do?
2. **Performance Efficiency** - How well does it use resources?
3. **Compatibility** - Does it work with other systems?
4. **Usability** - How easy is it to use?
5. **Reliability** - How dependable is it?
6. **Security** - How well is it protected?
7. **Maintainability** - How easy is it to change?
8. **Portability** - How easy is it to move to different environments?

---

## 1. Performance Efficiency

### Definition
The performance relative to the amount of resources used under stated conditions.

### Sub-Characteristics

#### 1.1 Time Behavior (Responsiveness)
**Concern**: How fast does the system respond?

**Metrics**:
- **Latency**: Time from request to response
  - p50 (median): 50% of requests faster than X ms
  - p95: 95% of requests faster than X ms
  - p99: 99% of requests faster than X ms
  - p99.9: 99.9% of requests faster than X ms
- **Throughput**: Requests/transactions per second
- **Response time**: End-to-end time including processing and network

**Typical Targets**:
- Web pages: < 2 seconds for full page load
- API calls: < 100ms p95 for read operations
- Database queries: < 50ms p95 for simple queries
- Real-time systems: < 10ms p95

**Quality Scenario Example**:
```
Scenario: User searches for product
Source: Customer using mobile app
Stimulus: Enters search query and submits
Environment: Normal load, 1000 concurrent users
Response: Search results displayed
Measure: p95 latency < 500ms, p99 < 1000ms
```

**Architectural Tactics**:
- Caching (Redis, CDN)
- Database indexing
- Async processing (message queues)
- Load balancing
- Connection pooling
- Query optimization
- Content compression

---

#### 1.2 Resource Utilization
**Concern**: How efficiently does the system use CPU, memory, storage, network?

**Metrics**:
- **CPU utilization**: Percentage of CPU capacity used (target: < 70% sustained)
- **Memory usage**: Heap size, memory leaks over time
- **Disk I/O**: IOPS, throughput (MB/s)
- **Network bandwidth**: Data transferred per second
- **Cost per transaction**: Cloud infrastructure cost divided by transactions

**Typical Targets**:
- CPU: < 70% under normal load (headroom for spikes)
- Memory: < 80% with no growth trend (no leaks)
- Database connections: < 80% of pool size
- Network: < 50% of available bandwidth

**Quality Scenario Example**:
```
Scenario: System handles peak load
Source: 10,000 concurrent users
Stimulus: Normal mix of operations
Environment: Production with autoscaling
Response: System scales horizontally
Measure: CPU < 70%, memory < 80%, no resource exhaustion
```

**Architectural Tactics**:
- Horizontal scaling (add more servers)
- Vertical scaling (bigger servers)
- Resource pooling (connection pools, thread pools)
- Efficient algorithms and data structures
- Lazy loading
- Pagination
- Resource monitoring and alerting

---

#### 1.3 Capacity (Scalability)
**Concern**: What is the maximum load the system can handle?

**Metrics**:
- **Maximum concurrent users**: How many simultaneous users?
- **Maximum throughput**: Requests per second at peak
- **Data volume capacity**: Records, files, or data size supported
- **Scaling factor**: How much more load with X% more resources?
- **Time to scale**: How long to provision additional capacity?

**Typical Targets**:
- Handle 10x normal load during peak events
- Scale from 1K to 100K users within 5 minutes (auto-scaling)
- Support 100M records with < 10% performance degradation
- Linear scaling: 2x resources = 2x capacity (ideal)

**Quality Scenario Example**:
```
Scenario: Black Friday traffic spike
Source: Marketing campaign drives 10x normal traffic
Stimulus: Sudden increase from 5K to 50K concurrent users
Environment: Production with autoscaling enabled
Response: System scales out automatically
Measure: Maintain p95 latency < 500ms, no errors, scale-up time < 3 minutes
```

**Architectural Tactics**:
- Horizontal scaling (stateless services)
- Database sharding
- Caching layers (reduce database load)
- CDN (distribute content globally)
- Auto-scaling policies
- Load testing and capacity planning
- Queue-based load leveling

---

## 2. Reliability

### Definition
The degree to which a system performs specified functions under specified conditions for a specified period.

### Sub-Characteristics

#### 2.1 Availability
**Concern**: What percentage of time is the system operational?

**Metrics**:
- **Uptime percentage**: (Total time - Downtime) / Total time × 100
- **Downtime per year**: How many hours/minutes unavailable
- **MTBF** (Mean Time Between Failures): Average time between failures
- **MTTR** (Mean Time To Repair): Average time to restore service

**Common SLA Tiers**:
| Availability | Downtime/Year | Downtime/Month | Downtime/Week | Use Case |
|--------------|---------------|----------------|---------------|----------|
| 90% | 36.5 days | 3 days | 16.8 hours | Development |
| 95% | 18.25 days | 1.5 days | 8.4 hours | Internal tools |
| 99% ("two nines") | 3.65 days | 7.2 hours | 1.68 hours | Basic service |
| 99.9% ("three nines") | 8.76 hours | 43.2 minutes | 10.1 minutes | Standard SaaS |
| 99.95% | 4.38 hours | 21.6 minutes | 5 minutes | High availability |
| 99.99% ("four nines") | 52.6 minutes | 4.32 minutes | 1.01 minutes | Mission critical |
| 99.999% ("five nines") | 5.26 minutes | 25.9 seconds | 6.05 seconds | Ultra critical |

**Quality Scenario Example**:
```
Scenario: Database primary fails
Source: Hardware failure in primary database server
Stimulus: Primary becomes unresponsive
Environment: Production with Multi-AZ setup
Response: Automatic failover to standby
Measure: Downtime < 30 seconds, zero data loss, 99.95% annual uptime maintained
```

**Architectural Tactics**:
- Redundancy (active-active, active-passive)
- Health checks and monitoring
- Automatic failover
- Multi-region deployment
- Graceful degradation
- Circuit breakers
- Retry mechanisms with exponential backoff

---

#### 2.2 Fault Tolerance
**Concern**: How does the system behave when components fail?

**Metrics**:
- **Recovery time**: Time to restore functionality after failure
- **Data loss**: Amount of data lost during failure (RPO - Recovery Point Objective)
- **Blast radius**: Percentage of users affected by a single failure
- **Error rate during degradation**: Errors while operating in degraded mode

**Typical Targets**:
- RTO (Recovery Time Objective): < 1 hour
- RPO (Recovery Point Objective): < 15 minutes of data
- Partial degradation preferred over complete outage
- Isolate failures (1 component failure ≠ system failure)

**Quality Scenario Example**:
```
Scenario: Payment service unavailable
Source: Payment service crashes
Stimulus: Order checkout attempted
Environment: Production with circuit breaker
Response: Circuit breaker opens, order queued for later processing
Measure: User notified gracefully, order saved, retry succeeds when service recovers
```

**Architectural Tactics**:
- Circuit breaker pattern
- Bulkhead pattern (isolation)
- Timeout and retry policies
- Fallback mechanisms
- Compensation transactions
- Health checks
- Chaos engineering (test failure modes)

---

#### 2.3 Recoverability
**Concern**: How quickly can the system recover from failures?

**Metrics**:
- **RTO** (Recovery Time Objective): Max acceptable downtime
- **RPO** (Recovery Point Objective): Max acceptable data loss
- **Backup frequency**: How often are backups taken?
- **Restore time**: How long does full restore take?
- **Data integrity**: Percentage of data recovered correctly

**Typical Targets**:
- Critical systems: RTO < 1 hour, RPO < 15 minutes
- Standard systems: RTO < 4 hours, RPO < 1 hour
- Non-critical: RTO < 24 hours, RPO < 24 hours

**Quality Scenario Example**:
```
Scenario: Disaster recovery test
Source: Operations team initiates DR failover
Stimulus: Entire primary region goes offline
Environment: DR region with replicated data
Response: Failover to DR region
Measure: RTO 30 minutes, RPO 5 minutes, all services functional
```

**Architectural Tactics**:
- Database replication (sync/async)
- Backup automation
- Point-in-time recovery
- Disaster recovery (DR) site
- Regular DR drills
- Immutable infrastructure
- Blue-green deployments

---

## 3. Security

### Definition
The degree to which a system protects information and data so that unauthorized persons or systems cannot read or modify them.

### Sub-Characteristics

#### 3.1 Confidentiality
**Concern**: Is data protected from unauthorized access?

**Metrics**:
- **Encryption coverage**: % of data encrypted at rest and in transit
- **Access control violations**: Failed authorization attempts
- **Data leak incidents**: Unauthorized data exposure events
- **Secrets management**: Hardcoded secrets found (should be 0)

**Typical Targets**:
- 100% of sensitive data encrypted at rest (AES-256)
- 100% of data in transit encrypted (TLS 1.3)
- Zero hardcoded credentials
- All access logged for audit

**Quality Scenario Example**:
```
Scenario: Attacker intercepts network traffic
Source: External attacker
Stimulus: Attempts to read data in transit
Environment: Production with TLS enabled
Response: All traffic encrypted
Measure: Zero sensitive data readable, TLS 1.3 enforced, perfect forward secrecy
```

**Architectural Tactics**:
- Encryption at rest (database, storage)
- Encryption in transit (TLS/HTTPS)
- Secrets management (Vault, AWS Secrets Manager)
- Key rotation policies
- Data masking/tokenization
- VPN for internal communication
- Zero-trust architecture

---

#### 3.2 Integrity
**Concern**: Is data protected from unauthorized modification?

**Metrics**:
- **Checksum verification**: Data integrity checks performed
- **Audit log coverage**: % of changes logged
- **Tampering detection**: Unauthorized modification attempts detected
- **Input validation coverage**: % of inputs validated

**Typical Targets**:
- 100% of critical operations logged
- Input validation on all user inputs
- Digital signatures for critical transactions
- Immutable audit logs

**Quality Scenario Example**:
```
Scenario: Malicious input submitted
Source: Attacker submits SQL injection attempt
Stimulus: Crafted input in search field
Environment: Production with input validation
Response: Input rejected, attack logged
Measure: Attack blocked, no data modified, security team alerted
```

**Architectural Tactics**:
- Input validation and sanitization
- Prepared statements (prevent SQL injection)
- Digital signatures
- Checksums and hashing
- Audit logging (write-once, immutable)
- CSRF protection
- Content Security Policy (CSP)

---

#### 3.3 Authentication & Authorization
**Concern**: Are users who they claim to be, and can they do what they're attempting?

**Metrics**:
- **Failed login attempts**: Brute force attempt detection
- **MFA adoption rate**: % of users with 2FA enabled
- **Session management**: Session hijacking attempts
- **Privilege escalation attempts**: Unauthorized access attempts

**Typical Targets**:
- MFA required for admin access (100%)
- MFA encouraged for all users (>80% adoption)
- Password complexity enforced
- Session timeout: 30 minutes idle
- JWT token expiry: 1 hour

**Quality Scenario Example**:
```
Scenario: User attempts unauthorized action
Source: Authenticated user
Stimulus: Attempts to delete another user's data
Environment: Production with RBAC enabled
Response: Action denied, audit logged
Measure: Authorization check passes, action blocked, incident logged
```

**Architectural Tactics**:
- Multi-factor authentication (MFA)
- OAuth 2.0 / OpenID Connect
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- JWT with short expiry
- API keys with scopes
- Principle of least privilege

---

#### 3.4 Non-Repudiation
**Concern**: Can users deny performing an action?

**Metrics**:
- **Audit log completeness**: % of actions logged
- **Digital signature usage**: Critical transactions signed
- **Log integrity**: Logs protected from tampering

**Quality Scenario Example**:
```
Scenario: Dispute over transaction
Source: User claims they didn't make a payment
Stimulus: Dispute filed
Environment: Production with audit logging
Response: Audit trail retrieved
Measure: Complete log of user actions, digital signature verified, dispute resolved
```

**Architectural Tactics**:
- Comprehensive audit logging
- Digital signatures
- Timestamping
- Immutable log storage
- Log aggregation and retention

---

#### 3.5 Accountability
**Concern**: Can actions be traced to specific users?

**Metrics**:
- **User action tracking**: % of operations attributed to users
- **Log retention**: How long are logs kept?
- **Audit trail completeness**: All security events logged

**Quality Scenario Example**:
```
Scenario: Security incident investigation
Source: Security team
Stimulus: Investigates suspicious activity
Environment: Production with centralized logging
Response: Complete audit trail available
Measure: All actions traced to specific users, timestamps accurate, chain of custody maintained
```

**Architectural Tactics**:
- User ID in all logs
- Correlation IDs across services
- Centralized log aggregation
- SIEM integration
- Compliance-aligned retention policies

---

## 4. Maintainability

### Definition
The degree of effectiveness and efficiency with which the system can be modified.

### Sub-Characteristics

#### 4.1 Modularity
**Concern**: Is the system composed of discrete components?

**Metrics**:
- **Cyclomatic complexity**: Code complexity per module (target: < 10)
- **Coupling**: Dependencies between modules (aim: low)
- **Cohesion**: Relatedness within modules (aim: high)
- **Module size**: Lines of code per module (target: < 500)

**Typical Targets**:
- Average method complexity < 10
- Max method complexity < 20
- Clear module boundaries (well-defined interfaces)
- Minimal cross-module dependencies

**Quality Scenario Example**:
```
Scenario: Change payment provider
Source: Developer
Stimulus: Replace Stripe with PayPal
Environment: Development
Response: Change isolated to payment module
Measure: < 100 lines changed, no other modules affected, tests pass
```

**Architectural Tactics**:
- Layered architecture
- Microservices (bounded contexts)
- Interface segregation
- Dependency inversion
- Hexagonal architecture
- Domain-Driven Design

---

#### 4.2 Reusability
**Concern**: Can components be used in multiple contexts?

**Metrics**:
- **Code duplication**: Percentage of duplicated code (target: < 5%)
- **Library usage**: Reused components vs custom code
- **API consistency**: Common patterns across APIs

**Quality Scenario Example**:
```
Scenario: Reuse authentication in new service
Source: Developer building new microservice
Stimulus: Needs authentication
Environment: Development
Response: Import authentication library
Measure: Zero authentication code written, < 1 hour integration time
```

**Architectural Tactics**:
- Shared libraries
- Design patterns
- Component libraries (UI)
- API standards
- Service mesh (common concerns)

---

#### 4.3 Analyzability
**Concern**: How easy is it to diagnose problems and understand the system?

**Metrics**:
- **Code coverage**: % of code covered by tests (target: > 80%)
- **Documentation completeness**: APIs documented, architecture docs exist
- **Logging coverage**: % of important operations logged
- **Mean Time To Diagnose (MTTD)**: Time to identify root cause

**Typical Targets**:
- 80%+ unit test coverage
- All public APIs documented
- All errors logged with context
- Architecture documentation exists and is current

**Quality Scenario Example**:
```
Scenario: Production incident
Source: Operations team
Stimulus: Users report errors
Environment: Production with logging/monitoring
Response: Root cause identified via logs
Measure: MTTD < 15 minutes, logs provide sufficient context
```

**Architectural Tactics**:
- Structured logging
- Distributed tracing
- Metrics and dashboards
- Code documentation
- Architecture documentation (ADRs, diagrams)
- Static code analysis

---

#### 4.4 Modifiability
**Concern**: How easy is it to make changes?

**Metrics**:
- **Change lead time**: Time from code commit to production
- **Lines changed per feature**: Smaller is better
- **Blast radius**: Components affected by average change
- **Failed deployment rate**: % of deployments that fail

**Typical Targets**:
- Deploy to production in < 1 hour
- Average feature requires changing 1-2 modules
- Failed deployment rate < 5%
- Rollback time < 5 minutes

**Quality Scenario Example**:
```
Scenario: Add new field to user profile
Source: Developer
Stimulus: Business requests new user attribute
Environment: Development
Response: Change implemented
Measure: < 4 hours development, < 20 files changed, tests pass, deploy in < 1 hour
```

**Architectural Tactics**:
- Loose coupling
- Configuration over code
- Feature flags
- Automated testing
- CI/CD pipelines
- Blue-green deployments

---

#### 4.5 Testability
**Concern**: How easy is it to test the system?

**Metrics**:
- **Test coverage**: % of code/paths tested
- **Test execution time**: How long test suite runs
- **Test flakiness**: % of tests that fail intermittently
- **Test to code ratio**: Test lines vs code lines (1:1 or higher is good)

**Typical Targets**:
- Unit test coverage > 80%
- Integration test coverage > 60%
- Test suite runs in < 10 minutes
- Flaky test rate < 1%

**Quality Scenario Example**:
```
Scenario: Developer adds new feature
Source: Developer
Stimulus: Writes new code
Environment: Development with CI/CD
Response: Automated tests run
Measure: Tests complete in < 5 minutes, coverage remains > 80%, all pass
```

**Architectural Tactics**:
- Dependency injection
- Mocking and stubbing
- Test data builders
- Contract testing
- Test automation
- Test environments (staging, QA)

---

## 5. Usability

### Definition
The degree to which a product can be used by specified users to achieve specified goals with effectiveness, efficiency, and satisfaction.

### Sub-Characteristics

#### 5.1 Learnability
**Concern**: How easy is it for users to learn the system?

**Metrics**:
- **Time to first success**: Minutes until new user completes core task
- **Training time required**: Hours of training needed
- **Help documentation usage**: % of users accessing help
- **Error rate during learning**: Errors made by new users

**Typical Targets**:
- New user completes key task in < 5 minutes (no training)
- 80% of users don't need help documentation
- Onboarding completion rate > 90%

**Quality Scenario Example**:
```
Scenario: New user signs up
Source: First-time user
Stimulus: Accesses application
Environment: Production with onboarding flow
Response: Guided through key features
Measure: Completes onboarding in < 10 minutes, error-free
```

**Architectural Tactics**:
- Progressive disclosure
- Onboarding flows
- In-app tutorials
- Contextual help
- Consistent UI patterns
- Clear error messages

---

#### 5.2 Operability
**Concern**: How easy is the system to operate and control?

**Metrics**:
- **Task completion rate**: % of users completing intended tasks
- **Error rate**: Errors per user session
- **Time on task**: Minutes to complete common operations
- **Clicks to goal**: Number of clicks to accomplish task

**Typical Targets**:
- Task completion rate > 95%
- < 3 clicks to complete common actions
- Error rate < 5% of interactions
- Key tasks completable in < 2 minutes

**Quality Scenario Example**:
```
Scenario: User creates new order
Source: Regular user
Stimulus: Wants to place order
Environment: Production on desktop
Response: Navigates through order flow
Measure: 3 steps, < 1 minute, 98% completion rate
```

**Architectural Tactics**:
- Intuitive navigation
- Keyboard shortcuts
- Bulk operations
- Undo/redo functionality
- Auto-save
- Smart defaults

---

#### 5.3 Accessibility
**Concern**: Can users with disabilities use the system?

**Metrics**:
- **WCAG compliance level**: A, AA, or AAA
- **Screen reader compatibility**: % of content accessible
- **Keyboard navigation**: All functions keyboard-accessible
- **Color contrast ratio**: Meets WCAG standards (4.5:1 minimum)

**Typical Targets**:
- WCAG 2.1 Level AA compliance
- 100% keyboard navigable
- Screen reader compatible
- Color contrast ratios meet standards

**Quality Scenario Example**:
```
Scenario: Visually impaired user navigates site
Source: User with screen reader
Stimulus: Accesses application
Environment: Production with ARIA labels
Response: Screen reader reads all content
Measure: All functions accessible, WCAG AA compliant
```

**Architectural Tactics**:
- Semantic HTML
- ARIA labels
- Keyboard navigation support
- Color contrast compliance
- Alt text for images
- Captions for videos
- Accessibility testing

---

## 6. Compatibility

### Definition
The degree to which a system can exchange information with other systems and perform its required functions while sharing hardware or software environment.

### Sub-Characteristics

#### 6.1 Interoperability
**Concern**: Can the system exchange data and operate with other systems?

**Metrics**:
- **API compatibility**: % of API endpoints following standards
- **Integration success rate**: Successful integrations vs attempts
- **Data format support**: Number of formats supported (JSON, XML, CSV, etc.)
- **Protocol support**: HTTP/REST, gRPC, GraphQL, SOAP, etc.

**Quality Scenario Example**:
```
Scenario: Third-party integration
Source: Partner company
Stimulus: Wants to integrate via API
Environment: Production API
Response: API documentation accessed
Measure: Integration completed in < 1 day, no custom development needed
```

**Architectural Tactics**:
- RESTful API design
- Standard data formats (JSON, Protobuf)
- API versioning
- Webhooks for notifications
- Well-documented APIs (OpenAPI/Swagger)
- SDKs in multiple languages

---

#### 6.2 Co-existence
**Concern**: Can the system coexist with other systems in shared environment?

**Metrics**:
- **Resource isolation**: Degree of resource sharing with other systems
- **Deployment conflicts**: Conflicts during deployment
- **Port conflicts**: Network port collisions

**Quality Scenario Example**:
```
Scenario: Deploy alongside legacy system
Source: Operations team
Stimulus: Deploys new version
Environment: Shared infrastructure with legacy app
Response: Both systems operate
Measure: No resource conflicts, no interference, both systems maintain SLA
```

**Architectural Tactics**:
- Containerization (Docker)
- Namespace isolation
- Service mesh
- API Gateway (routing)
- Feature toggles

---

## 7. Portability

### Definition
The ease with which a system can be transferred from one environment to another.

### Sub-Characteristics

#### 7.1 Adaptability
**Concern**: How easily can the system be adapted to different environments?

**Metrics**:
- **Configuration externalization**: % of config externalized
- **Environment parity**: Differences between dev/staging/prod
- **Platform dependencies**: Hardcoded platform-specific code

**Quality Scenario Example**:
```
Scenario: Deploy to new region
Source: Operations team
Stimulus: Launches in new AWS region
Environment: Fresh AWS region
Response: System deployed via IaC
Measure: < 1 hour deployment, all configuration externalized, zero code changes
```

**Architectural Tactics**:
- 12-factor app principles
- Environment variables for config
- Infrastructure as Code (Terraform)
- Cloud-agnostic design (where possible)
- Containerization

---

#### 7.2 Installability
**Concern**: How easy is the system to install?

**Metrics**:
- **Installation time**: Minutes to install from scratch
- **Installation steps**: Number of manual steps
- **Failure rate**: Failed installations vs successful
- **Rollback time**: Time to rollback failed installation

**Quality Scenario Example**:
```
Scenario: Fresh installation
Source: New customer
Stimulus: Wants to self-host
Environment: Customer infrastructure
Response: Follows installation guide
Measure: < 30 minutes installation, automated, no manual config
```

**Architectural Tactics**:
- One-click installers
- Docker Compose for local dev
- Helm charts for Kubernetes
- Automated provisioning scripts
- Health checks post-installation

---

#### 7.3 Replaceability
**Concern**: How easy is it to replace this system with another?

**Metrics**:
- **Data export completeness**: % of data exportable
- **Migration tools availability**: Tools to move to alternative
- **Vendor lock-in score**: Proprietary dependencies vs open standards

**Quality Scenario Example**:
```
Scenario: Migrate to competitor
Source: Customer
Stimulus: Wants to change vendors
Environment: Production
Response: Export all data
Measure: Complete data export, standard format, < 1 day migration
```

**Architectural Tactics**:
- Standard data formats
- Export functionality
- API-first design
- Avoid vendor-specific features
- Open source where possible

---

## Quality Attribute Scenarios Template

Use this template to document quality attribute requirements:

```markdown
### [Quality Attribute] Scenario: [Name]

**Quality Attribute**: [Performance/Security/Reliability/etc.]
**Sub-characteristic**: [Specific sub-characteristic]

**Source**: [Who initiates? User, system, admin, attacker, etc.]
**Stimulus**: [What happens? User action, failure, attack, etc.]
**Artifact**: [What part of system? Component, service, database, etc.]
**Environment**: [Conditions? Normal load, peak load, under attack, etc.]
**Response**: [What should system do?]
**Response Measure**: [How to measure? Specific metric and target]

**Rationale**: [Why is this important?]
**Priority**: [Critical/High/Medium/Low]
**Related Scenarios**: [Links to related scenarios]
```

**Example**:
```markdown
### Performance Scenario: Product Search Under Load

**Quality Attribute**: Performance Efficiency
**Sub-characteristic**: Time Behavior (Latency)

**Source**: Customer using mobile app
**Stimulus**: Enters search query "wireless headphones"
**Artifact**: Search service and database
**Environment**: Peak traffic (10,000 concurrent users)
**Response**: Search results returned and displayed
**Response Measure**: p95 latency < 500ms, p99 < 1000ms

**Rationale**: Fast search is critical for user experience and conversion rate. Studies show 100ms delay reduces conversion by 1%.
**Priority**: Critical
**Related Scenarios**: "Database Query Performance", "CDN Cache Hit Rate"
```

---

## Quality Attributes vs Architectural Decisions

### How Quality Attributes Drive Architecture

| Quality Attribute | Influences | Example Decision |
|------------------|------------|------------------|
| **High Availability** | Deployment | Multi-AZ database, redundant load balancers |
| **Performance** | Caching | Redis caching layer, CDN |
| **Scalability** | Architecture | Microservices, stateless services, horizontal scaling |
| **Security** | Network | Zero-trust network, VPN, WAF |
| **Maintainability** | Structure | Modular monolith, clear boundaries |
| **Testability** | Dependencies | Dependency injection, mocking |
| **Portability** | Technology | Containers, cloud-agnostic design |

### Trade-off Analysis

Quality attributes often conflict. Document trade-offs explicitly:

**Example: Performance vs Security**
- More security checks = slower response time
- Decision: Implement caching for authenticated users, accept 50ms latency increase for auth check

**Example: Availability vs Cost**
- Multi-region = higher availability but 2x infrastructure cost
- Decision: Single region with Multi-AZ for 99.95% availability at 30% cost increase

**Example: Flexibility vs Performance**
- Generic abstraction = easier to swap but slower
- Decision: Direct database access for critical path, abstraction for non-critical

---

## Measuring Quality Attributes

### Establishing Baselines
1. Measure current state (before improvements)
2. Set target (desired state)
3. Measure after changes
4. Compare and iterate

### Example Measurement Plan

**Performance Baseline**:
```
Current State (measured via APM):
- p50: 120ms
- p95: 450ms
- p99: 1200ms

Target (based on user research):
- p50: < 100ms
- p95: < 300ms
- p99: < 800ms

Measurement Method:
- Production APM (Datadog)
- Sampled: 100% of requests
- Measured: After authentication before response

Review Cadence: Weekly
```

---

## References & Standards

### Standards
- **ISO/IEC 25010**: Systems and software Quality Requirements and Evaluation (SQuaRE)
- **ISO/IEC 25012**: Data quality model
- **WCAG 2.1**: Web Content Accessibility Guidelines

### Books
- *Software Architecture in Practice* (Bass, Clements, Kazman) - Definitive guide to quality attributes
- *Designing Data-Intensive Applications* (Martin Kleppmann) - Performance, reliability, scalability
- *Release It!* (Michael Nygard) - Reliability patterns

### Tools
- **Performance**: k6, JMeter, Gatling
- **Security**: OWASP ZAP, SonarQube, Snyk
- **Accessibility**: axe DevTools, WAVE, Lighthouse
- **Code Quality**: SonarQube, CodeClimate, ESLint

---

## Quick Reference: Quality Attributes Checklist

When documenting architecture, ensure you've addressed:

**Performance**:
- [ ] Latency targets defined (p50, p95, p99)
- [ ] Throughput requirements specified
- [ ] Resource utilization limits set
- [ ] Scalability targets defined

**Reliability**:
- [ ] Availability SLA specified (99.X%)
- [ ] RTO and RPO defined
- [ ] Fault tolerance mechanisms identified
- [ ] Recovery procedures documented

**Security**:
- [ ] Authentication mechanism specified
- [ ] Authorization model defined (RBAC, ABAC)
- [ ] Encryption requirements (at rest, in transit)
- [ ] Audit logging scope defined
- [ ] Compliance requirements identified

**Maintainability**:
- [ ] Code quality standards set
- [ ] Testing strategy defined (unit, integration, e2e)
- [ ] Documentation requirements specified
- [ ] Deployment process documented

**Usability**:
- [ ] Key user tasks identified
- [ ] Success metrics defined (completion rate, time on task)
- [ ] Accessibility requirements specified
- [ ] User feedback mechanism exists

**Compatibility**:
- [ ] Integration points identified
- [ ] API standards specified
- [ ] Data format standards defined

**Portability**:
- [ ] Configuration externalization complete
- [ ] Environment parity maintained
- [ ] Deployment automation exists

---

## Prioritizing Quality Attributes

Not all quality attributes are equally important. Use this framework to prioritize:

### Priority Matrix

| Priority | Definition | Allocation |
|----------|------------|------------|
| **Critical** | System fails without this | 40% of effort |
| **High** | Significant value, manageable risk | 35% of effort |
| **Medium** | Nice to have, adds value | 20% of effort |
| **Low** | Future consideration | 5% of effort |

### Prioritization Questions

**For each quality attribute, ask**:
1. **Business impact**: What's the cost of not meeting this? (revenue loss, reputation damage)
2. **User impact**: How many users affected? How severely?
3. **Risk**: What's the likelihood and impact of failure?
4. **Cost**: How expensive is it to achieve?
5. **Time**: How long will it take?

### Example Prioritization

**E-commerce Platform**:

**Critical** (Must Have):
- Availability: 99.95% (lost revenue during downtime)
- Security: PCI DSS compliance (legal requirement)
- Performance: < 2s page load (high bounce rate otherwise)

**High** (Should Have):
- Scalability: Handle 10x traffic spikes (seasonal events)
- Maintainability: Deploy 10x/day (competitive advantage)

**Medium** (Nice to Have):
- Accessibility: WCAG AA (expands market)
- Portability: Multi-cloud (risk mitigation)

**Low** (Future):
- Internationalization: Support 20+ languages (not needed yet)

---

## Quality Attribute Tactics Catalog

### Performance Tactics

**Reduce Resource Demand**:
- Reduce computational complexity (better algorithms)
- Reduce data volume (compression, pagination)
- Cache expensive computations
- Lazy loading (load on demand)

**Manage Resources**:
- Increase available resources (scale up/out)
- Introduce concurrency (parallel processing)
- Use resource pooling (connection pools)
- Schedule resources (prioritize critical tasks)

**Bound Queue Sizes**:
- Limit queue length (prevent memory exhaustion)
- Drop low-priority requests (graceful degradation)

---

### Availability Tactics

**Detect Faults**:
- Heartbeat/ping (periodic health checks)
- Monitoring (metrics, logs, traces)
- Exception detection (error handling)

**Recover from Faults**:
- Active redundancy (hot standby)
- Passive redundancy (cold standby)
- Spare (dynamically provision)
- Rollback (revert to last known good state)
- Retry (transient fault recovery)

**Prevent Faults**:
- Removal from service (isolate failing component)
- Transactions (ACID guarantees)
- Predictive model (ML for failure prediction)
- Exception prevention (input validation)
- Increase competence set (design for known failures)

---

### Security Tactics

**Resist Attacks**:
- Authenticate users (verify identity)
- Authorize users (verify permissions)
- Maintain data confidentiality (encryption)
- Maintain integrity (checksums, signatures)
- Limit exposure (minimize attack surface)
- Limit access (principle of least privilege)

**Detect Attacks**:
- Intrusion detection (anomaly detection)
- Service monitoring (unusual patterns)

**Recover from Attacks**:
- Audit trail (forensics)
- Restore (backups, snapshots)

**React to Attacks**:
- Revoke access (block attacker)
- Lock computer (rate limiting, account lockout)
- Inform actors (alerting, notifications)

---

### Modifiability Tactics

**Reduce Coupling**:
- Encapsulate (hide implementation)
- Use intermediary (adapter, proxy)
- Restrict dependencies (dependency rules)
- Refactor (improve design)
- Abstract common services (DRY principle)

**Increase Cohesion**:
- Increase semantic coherence (related things together)
- Anticipate expected changes (design for flexibility)
- Generalize module (parameterize, configure)

**Defer Binding**:
- Runtime registration (plugin architecture)
- Configuration files (externalize config)
- Polymorphism (interface-based design)
- Component replacement (hot-swap)
- Adherence to protocols (standard interfaces)

---

### Testability Tactics

**Control and Observe System State**:
- Specialized interfaces (test APIs)
- Record/playback (capture interactions)
- Localize state storage (easier to inspect)
- Abstract data sources (mock dependencies)
- Sandbox (isolated test environment)
- Executable assertions (self-testing code)

**Limit Complexity**:
- Limit structural complexity (low cyclomatic complexity)
- Limit nondeterminism (predictable behavior)

---

## Quality Attribute Utility Tree

A utility tree helps prioritize quality attribute scenarios. Create one for your project:

```
System Quality
│
├── Performance (High Priority)
│   ├── Latency (H, H) - Search results in < 500ms
│   ├── Throughput (H, M) - Handle 10K req/s
│   └── Resource Usage (M, L) - CPU < 70%
│
├── Availability (Critical)
│   ├── Uptime (H, H) - 99.95% availability
│   ├── Recovery (H, M) - MTTR < 30 minutes
│   └── Degradation (M, M) - Graceful degradation
│
├── Security (Critical)
│   ├── Authentication (H, H) - MFA for all users
│   ├── Authorization (H, H) - RBAC enforced
│   └── Encryption (H, M) - All data encrypted
│
├── Modifiability (High)
│   ├── Change (H, M) - New feature in < 2 weeks
│   └── Deploy (M, L) - Deploy in < 1 hour
│
└── Usability (Medium)
    ├── Learnability (M, M) - Onboard in < 10 min
    └── Efficiency (M, L) - Complete task in < 5 clicks

Legend: (Business Priority, Technical Difficulty)
H = High, M = Medium, L = Low
```

---

## Anti-Patterns in Quality Attributes

### Anti-Pattern 1: Vague Requirements
❌ **Bad**: "System should be fast"  
✅ **Good**: "Product search should return results with p95 latency < 500ms under load of 10K concurrent users"

### Anti-Pattern 2: Ignoring Trade-offs
❌ **Bad**: "We need maximum performance, security, and flexibility"  
✅ **Good**: "We prioritize security (Critical), accept 50ms latency increase, sacrifice some flexibility for security"

### Anti-Pattern 3: Not Measuring
❌ **Bad**: Assume performance is good based on "feels fast"  
✅ **Good**: Continuously monitor p50/p95/p99 latency in production via APM

### Anti-Pattern 4: Gold Plating
❌ **Bad**: "We need 99.999% availability for internal admin tool"  
✅ **Good**: "99.9% is adequate for admin tool (4.3 minutes downtime/month acceptable)"

### Anti-Pattern 5: No Stakeholder Buy-in
❌ **Bad**: Architects define all quality attributes in isolation  
✅ **Good**: Workshop with business, product, and engineering to agree on priorities

### Anti-Pattern 6: Unchanging Requirements
❌ **Bad**: Define quality attributes once at project start, never revisit  
✅ **Good**: Review quality attributes quarterly, adjust based on learnings

---

## Quality Attributes in Different Contexts

### Startup (Early Stage)
**Priorities**:
1. **Time to Market** (Modifiability) - Ship fast
2. **Performance** - Good enough, not perfect
3. **Security** - Basic security, comply with regulations
4. **Availability** - 99.9% acceptable

**Rationale**: Speed to market is existential. Over-engineering is waste.

### Enterprise (Mature)
**Priorities**:
1. **Security** - Zero breaches, compliance critical
2. **Availability** - 99.95%+ required
3. **Maintainability** - Long-term sustainability
4. **Performance** - Consistent, predictable

**Rationale**: Reputation and compliance are critical. Have resources for quality.

### Consumer Internet (Scale)
**Priorities**:
1. **Performance** - Sub-second response times
2. **Scalability** - Handle 100M+ users
3. **Availability** - 99.99%+ required
4. **Cost Efficiency** - Margins are thin

**Rationale**: User experience drives growth. Scale is the challenge.

### Safety-Critical (Medical, Aviation)
**Priorities**:
1. **Reliability** - No failures acceptable
2. **Safety** - Human life depends on it
3. **Traceability** - Complete audit trail
4. **Compliance** - FDA, FAA regulations

**Rationale**: Human safety overrides all other concerns.

---

## Documentation Templates

### Quality Attribute Requirement Template

```markdown
## [Quality Attribute] Requirements

### Overview
[Why this quality attribute matters for the system]

### Current State
[Baseline measurements if system exists]
- Metric 1: [Current value]
- Metric 2: [Current value]

### Target State
[Desired future state]
- Metric 1: [Target value, timeline]
- Metric 2: [Target value, timeline]

### Scenarios

#### Scenario 1: [Name]
- **Source**: [Who/what initiates]
- **Stimulus**: [What happens]
- **Response**: [Expected behavior]
- **Measure**: [Success criteria]
- **Priority**: [Critical/High/Medium/Low]

#### Scenario 2: [Name]
[Same structure]

### Architectural Tactics
[How architecture supports this quality attribute]
- Tactic 1: [Description]
- Tactic 2: [Description]

### Validation
[How will we verify this is achieved?]
- Test approach: [Load testing, security audit, etc.]
- Tools: [Specific tools used]
- Frequency: [Continuous, weekly, quarterly]

### Risks
[What could prevent us from achieving this?]
- Risk 1: [Description + mitigation]
- Risk 2: [Description + mitigation]

### Cost
[Estimated cost to achieve this quality attribute]
- Development: [Engineer-months]
- Infrastructure: [Monthly cost]
- Tools/Licenses: [One-time + recurring]

### Dependencies
[What else must be true?]
- Technical: [Other systems, tools]
- Organizational: [Team skills, processes]
```

---

### Quality Attribute Trade-off Template

```markdown
## Trade-off Analysis: [QA1] vs [QA2]

### Conflict
[Describe how these quality attributes conflict]

**Example**: Increasing security (more checks) decreases performance (slower response)

### Options

#### Option A: Favor [QA1]
**Approach**: [How we'd optimize for QA1]  
**Impact on QA1**: [Improvement amount]  
**Impact on QA2**: [Degradation amount]  
**Cost**: [Effort, resources]

#### Option B: Favor [QA2]
**Approach**: [How we'd optimize for QA2]  
**Impact on QA1**: [Degradation amount]  
**Impact on QA2**: [Improvement amount]  
**Cost**: [Effort, resources]

#### Option C: Balance
**Approach**: [Compromise approach]  
**Impact on QA1**: [Partial improvement]  
**Impact on QA2**: [Partial improvement]  
**Cost**: [Effort, resources]

### Recommendation
**Choice**: [Option A/B/C]  
**Rationale**: [Why this choice?]  
**Stakeholders**: [Who agreed?]  
**Conditions**: [Under what assumptions?]  
**Review**: [When to re-evaluate?]
```

---

## Summary: Key Takeaways

### Essential Practices

1. **Make quality attributes explicit** - Don't assume, document
2. **Make them measurable** - Use specific metrics, not adjectives
3. **Prioritize ruthlessly** - Not everything can be critical
4. **Consider trade-offs** - Acknowledge what you sacrifice
5. **Measure continuously** - Monitor in production, don't guess
6. **Review regularly** - Priorities change as system and business evolve

### Common Mistakes to Avoid

- ❌ Vague requirements ("fast", "secure", "scalable")
- ❌ No measurements or baselines
- ❌ Ignoring trade-offs
- ❌ Everything is "critical"
- ❌ Define once, never revisit
- ❌ No stakeholder alignment

### Quality Attributes Drive

- Architecture decisions (patterns, technologies)
- Infrastructure choices (cloud, database, caching)
- Development practices (testing, deployment)
- Operational processes (monitoring, on-call)
- Team structure (who owns what)
- Budget allocation (where to invest)

---

## Appendix: ISO 25010 Full Model

```
Quality in Use
├── Effectiveness
├── Efficiency  
├── Satisfaction
│   ├── Usefulness
│   ├── Trust
│   ├── Pleasure
│   └── Comfort
├── Freedom from Risk
│   ├── Economic Risk Mitigation
│   ├── Health and Safety Risk Mitigation
│   └── Environmental Risk Mitigation
└── Context Coverage
    ├── Context Completeness
    └── Flexibility

Product Quality
├── Functional Suitability
│   ├── Functional Completeness
│   ├── Functional Correctness
│   └── Functional Appropriateness
├── Performance Efficiency
│   ├── Time Behavior
│   ├── Resource Utilization
│   └── Capacity
├── Compatibility
│   ├── Co-existence
│   └── Interoperability
├── Usability
│   ├── Appropriateness Recognizability
│   ├── Learnability
│   ├── Operability
│   ├── User Error Protection
│   ├── User Interface Aesthetics
│   └── Accessibility
├── Reliability
│   ├── Maturity
│   ├── Availability
│   ├── Fault Tolerance
│   └── Recoverability
├── Security
│   ├── Confidentiality
│   ├── Integrity
│   ├── Non-repudiation
│   ├── Accountability
│   └── Authenticity
├── Maintainability
│   ├── Modularity
│   ├── Reusability
│   ├── Analyzability
│   ├── Modifiability
│   └── Testability
└── Portability
    ├── Adaptability
    ├── Installability
    └── Replaceability
```

---

**End of Quality Attributes Catalog**

Use this catalog as a reference when:
- Writing architectural documentation
- Creating ADRs
- Defining system requirements
- Evaluating technology choices
- Conducting architecture reviews
- Planning testing strategies
- Setting SLAs and monitoring alerts