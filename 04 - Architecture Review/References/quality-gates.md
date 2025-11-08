# Quality Gates Reference

## Overview

Quality gates are checkpoint criteria that architecture must satisfy before progressing to the next phase. This document provides comprehensive gates for different review stages.

---

## Gate 1: Conceptual Architecture Review

**Timing**: After initial architecture vision, before detailed design

**Purpose**: Validate high-level approach and feasibility

### Exit Criteria

#### Business Alignment
- [ ] Architecture supports all critical business capabilities
- [ ] Solution aligns with business strategy and roadmap
- [ ] Value proposition is clearly articulated
- [ ] Success metrics defined and measurable
- [ ] Stakeholders identified and engaged

#### Technical Feasibility
- [ ] No obvious technical blockers identified
- [ ] Technology choices appropriate for problem domain
- [ ] Integration points with existing systems understood
- [ ] Performance targets appear achievable
- [ ] Security and compliance requirements identified

#### Organizational Readiness
- [ ] Team has or can acquire necessary skills
- [ ] Budget estimate within acceptable range (±30%)
- [ ] Timeline realistic for scope
- [ ] Change management implications understood
- [ ] Executive sponsorship confirmed

### Red Flags (Gate Cannot Pass)
- Critical business requirements cannot be met
- Fundamental technical approach is flawed
- Cost exceeds budget by >50%
- Team lacks skills with no training plan
- No executive sponsor

---

## Gate 2: Detailed Design Review

**Timing**: After detailed design, before implementation starts

**Purpose**: Validate architecture can be successfully implemented

### Exit Criteria

#### Functional Completeness
- [ ] All functional requirements mapped to components
- [ ] Component responsibilities clearly defined
- [ ] Interfaces and contracts specified
- [ ] Data flows documented for all use cases
- [ ] Edge cases and error scenarios addressed

#### Quality Attributes
- [ ] Performance targets quantified with acceptable ranges
- [ ] Scalability approach defined with capacity planning
- [ ] Security architecture documented (authn/authz model)
- [ ] Availability targets specified with SLA commitments
- [ ] Maintainability considerations incorporated
- [ ] Observability strategy defined (logs, metrics, traces)

#### Technology Stack
- [ ] All technology choices documented with rationale
- [ ] Technology maturity assessed and risks identified
- [ ] Licensing costs and implications understood
- [ ] Vendor lock-in risks evaluated
- [ ] Team training plan exists for new technologies
- [ ] Proof of concepts completed for high-risk choices

#### Architecture Patterns
- [ ] Patterns appropriately selected for context
- [ ] Pattern trade-offs understood and documented
- [ ] Patterns applied consistently across system
- [ ] Anti-patterns actively avoided
- [ ] Pattern variations justified

#### Data Architecture
- [ ] Data models defined and normalized
- [ ] Database choices justified (relational/NoSQL/cache)
- [ ] Data ownership boundaries clear
- [ ] Data consistency strategy defined (eventual/strong)
- [ ] Migration strategy exists for schema evolution
- [ ] Backup and disaster recovery approach specified
- [ ] Data privacy and compliance addressed (GDPR, HIPAA)

#### Integration & APIs
- [ ] API design follows standards (REST/GraphQL/gRPC)
- [ ] API versioning strategy defined
- [ ] Error handling approach consistent
- [ ] Timeout and retry policies specified
- [ ] Circuit breakers planned for external dependencies
- [ ] API documentation approach selected
- [ ] Backward compatibility strategy defined

#### Security Architecture
- [ ] Threat model completed
- [ ] Authentication mechanism selected and documented
- [ ] Authorization model defined (RBAC/ABAC)
- [ ] Sensitive data identified and protection planned
- [ ] Secrets management approach defined
- [ ] Audit logging requirements specified
- [ ] Security testing approach planned
- [ ] Compliance requirements mapped to controls

### Red Flags (Gate Cannot Pass)
- Functional gaps remain unresolved
- Quality attributes not quantified or unrealistic
- Critical technology choices unproven
- No data migration strategy for brownfield
- Security as afterthought (no threat model)
- APIs designed without versioning strategy

---

## Gate 3: Implementation Readiness Review

**Timing**: Before production implementation starts

**Purpose**: Ensure team is ready to build successfully

### Exit Criteria

#### Development Environment
- [ ] Development environments provisioned
- [ ] CI/CD pipeline scaffolding in place
- [ ] Code repositories created with branch strategy
- [ ] Development tools and IDEs configured
- [ ] Dependency management approach defined
- [ ] Code quality gates configured (linting, testing)

#### Architecture Documentation
- [ ] Architecture Decision Records (ADRs) created for key decisions
- [ ] C4 diagrams completed (Context, Container, Component)
- [ ] Deployment architecture documented
- [ ] Runbooks drafted for operational procedures
- [ ] API specifications published (OpenAPI/AsyncAPI)
- [ ] Data dictionary available

#### Team Readiness
- [ ] Team structure aligns with architecture (Conway's Law)
- [ ] Roles and responsibilities defined
- [ ] Training completed for new technologies
- [ ] Communication channels established
- [ ] Definition of Done agreed upon
- [ ] Code review process defined

#### Risk Management
- [ ] Risk register created and maintained
- [ ] High-priority risks have mitigation plans
- [ ] Technical spike results documented
- [ ] Dependency risks identified (external teams/vendors)
- [ ] Contingency plans for critical risks

#### Quality Assurance
- [ ] Test strategy defined (unit, integration, e2e)
- [ ] Test environments planned
- [ ] Performance test approach specified
- [ ] Security testing approach defined
- [ ] Test data strategy exists
- [ ] Acceptance criteria defined for features

### Red Flags (Gate Cannot Pass)
- No CI/CD pipeline plan
- Team untrained on critical technologies
- High-risk areas without spike/POC validation
- No testing strategy
- Architecture documentation incomplete

---

## Gate 4: Pre-Production Review

**Timing**: Before deploying to production

**Purpose**: Validate system is ready for real users

### Exit Criteria

#### Functional Validation
- [ ] All critical user journeys tested end-to-end
- [ ] Edge cases and error scenarios validated
- [ ] Data migration tested (if applicable)
- [ ] Integrations with external systems verified
- [ ] Rollback procedures tested
- [ ] Feature flags functional for controlled rollout

#### Performance & Scalability
- [ ] Load testing completed against peak traffic scenarios
- [ ] Performance targets met (p50, p95, p99 latency)
- [ ] Resource utilization acceptable (CPU, memory, network)
- [ ] Auto-scaling tested and validated
- [ ] Database performance acceptable under load
- [ ] Caching effectiveness validated

#### Security Validation
- [ ] Security testing completed (SAST, DAST)
- [ ] Penetration testing performed
- [ ] Vulnerability scan results acceptable
- [ ] Secrets properly managed (no hardcoded credentials)
- [ ] Authentication and authorization tested
- [ ] Audit logging functional and tested
- [ ] Compliance requirements validated

#### Operational Readiness
- [ ] Monitoring dashboards created for key metrics
- [ ] Alerting rules configured with appropriate thresholds
- [ ] Log aggregation functional
- [ ] Distributed tracing implemented (for microservices)
- [ ] Runbooks completed for common operations
- [ ] Incident response procedures documented
- [ ] On-call rotation and escalation defined
- [ ] Backup and restore procedures tested
- [ ] Disaster recovery plan validated

#### Deployment Readiness
- [ ] Production infrastructure provisioned
- [ ] Deployment automation functional and tested
- [ ] Blue-green or canary deployment strategy tested
- [ ] Database migration scripts tested
- [ ] Configuration management validated
- [ ] DNS and load balancer configured
- [ ] SSL certificates valid and renewed

#### Documentation
- [ ] User documentation completed
- [ ] API documentation published
- [ ] Operations manual available
- [ ] Troubleshooting guides created
- [ ] Architecture documentation updated
- [ ] Known limitations documented

#### Business Continuity
- [ ] Backup strategy implemented and tested
- [ ] Disaster recovery plan validated
- [ ] RTO/RPO targets achievable
- [ ] Data retention policies implemented
- [ ] Business continuity plan documented

### Red Flags (Gate Cannot Pass)
- Performance targets not met (p95 > SLA)
- Critical security vulnerabilities unresolved
- No monitoring or alerting configured
- Disaster recovery untested
- Deployment automation non-functional
- On-call coverage undefined

---

## Gate 5: Post-Launch Review

**Timing**: 2-4 weeks after production launch

**Purpose**: Validate production performance and identify improvements

### Exit Criteria

#### Production Stability
- [ ] System availability meets SLA (measured)
- [ ] Error rates within acceptable thresholds
- [ ] Performance targets consistently met
- [ ] No critical incidents in review period
- [ ] Auto-scaling performing as expected
- [ ] Resource utilization stable and predictable

#### Operational Effectiveness
- [ ] Monitoring provides adequate visibility
- [ ] Alerts are actionable (low false positive rate)
- [ ] Incident response times acceptable
- [ ] Runbooks proved effective during incidents
- [ ] Team comfortable operating the system
- [ ] On-call burden reasonable (<5 pages/week)

#### User Adoption
- [ ] User adoption tracking against projections
- [ ] User feedback collected and analyzed
- [ ] Critical user journeys performing well
- [ ] No usability blockers identified
- [ ] Support ticket volume manageable

#### Technical Debt Assessment
- [ ] Technical debt log created
- [ ] Priority issues identified for next iteration
- [ ] Shortcuts taken during delivery documented
- [ ] Improvement backlog prioritized
- [ ] Refactoring opportunities identified

#### Lessons Learned
- [ ] Retrospective conducted with team
- [ ] What went well documented
- [ ] What could improve documented
- [ ] Action items identified and assigned
- [ ] Knowledge transferred to operations team

### Red Flags (Immediate Action Required)
- SLA violations occurring
- Critical incidents recurring
- User adoption significantly below projections
- On-call burden unsustainable (>10 pages/week)
- Major architectural issues discovered in production

---

## Quality Metrics Reference

### Performance Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Response Time (p50) | <200ms | 200-500ms | >500ms |
| Response Time (p95) | <500ms | 500-1000ms | >1000ms |
| Response Time (p99) | <1000ms | 1000-2000ms | >2000ms |
| Error Rate | <0.1% | 0.1-1% | >1% |
| Availability | >99.9% | 99.5-99.9% | <99.5% |

### Security Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Critical Vulnerabilities | 0 | 0 | >0 |
| High Vulnerabilities | <5 | 5-10 | >10 |
| Unpatched Systems | 0 | 1-3 | >3 |
| Failed Login Attempts | <100/day | 100-1000/day | >1000/day |
| Security Incidents | 0 | 0 | >0 |

### Operational Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Deployment Frequency | Daily | Weekly | Monthly |
| Lead Time for Changes | <1 day | 1-7 days | >7 days |
| Mean Time to Recovery | <1 hour | 1-4 hours | >4 hours |
| Change Failure Rate | <5% | 5-15% | >15% |

---

## Gate Assessment Template

Use this template to document gate assessment results:

```markdown
# Quality Gate Assessment: [Gate Name]

**Date**: YYYY-MM-DD
**Reviewers**: [Names]
**System**: [System Name]
**Version**: [Version]

## Gate Status: [PASS / CONDITIONAL PASS / FAIL]

## Summary
[2-3 sentences on overall assessment]

## Criteria Assessment

### [Category 1]
**Status**: [PASS / FAIL]

Passed Criteria:
- [Criterion 1]: ✅ [Evidence]
- [Criterion 2]: ✅ [Evidence]

Failed Criteria:
- [Criterion X]: ❌ [Gap description]

### [Category 2]
[Repeat structure]

## Open Issues

| ID | Category | Description | Severity | Owner | Due Date |
|----|----------|-------------|----------|-------|----------|
| 1 | Security | No threat model | High | Alice | 2024-01-15 |
| 2 | Performance | Load test incomplete | Medium | Bob | 2024-01-20 |

## Conditions for Gate Passage

**Required Actions (Must Complete)**:
1. [Action 1] - [Owner] - [Deadline]
2. [Action 2] - [Owner] - [Deadline]

**Recommended Actions (Should Complete)**:
1. [Action 1] - [Owner] - [Deadline]

## Decision

**Recommendation**: [APPROVE / CONDITIONAL APPROVE / REJECT]

**Rationale**: [Why this decision]

**Next Review**: [Date, if conditional]

**Approvers**:
- [Name] - [Role] - [Signature/Date]
- [Name] - [Role] - [Signature/Date]
```

---

## Usage Guidelines

### When to Apply Gates

**Always Required**:
- New systems or major architecture changes
- Migration to new technology platforms
- Systems handling sensitive data
- High-traffic or mission-critical systems

**Optional/Lightweight**:
- Minor feature additions to stable systems
- Internal tools with limited user base
- Proof of concepts or experiments
- Team has high architectural maturity

### Tailoring Gates to Context

**For Startups/MVPs**:
- Focus on Gates 1, 2, and 4 (skip 3 for speed)
- Reduce criteria by 30-40%
- Prioritize user-facing quality over operational perfection
- Accept more technical debt with explicit tracking

**For Enterprise/Mission-Critical**:
- Apply all gates rigorously
- Add organization-specific criteria
- Require formal sign-offs at each gate
- Lower tolerance for risk and technical debt

**For Regulated Industries** (Finance, Healthcare):
- Add compliance-specific criteria at each gate
- Require audit trails for all decisions
- Include security and compliance team in reviews
- Maintain gate documentation for audits

---

## Related Resources

- `anti-patterns-catalog.md` - Common failures to avoid at each gate
- `quality-attributes-catalog.md` - Detailed quality attribute specifications
