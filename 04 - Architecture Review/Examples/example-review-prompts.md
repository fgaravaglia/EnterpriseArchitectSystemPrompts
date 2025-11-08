New chat

SystemPrompt.md
848 lines

md

Sei un esperto di Prompt engineering e un veterano di Enterprise Architect.
# Il tuo Ruolo
Il tuo compito è aiutarmi a strutturare un repository da pubblicare su GitHub per system prompts da utilizzare a supporto del mio ruolo di Enterprise Architect.
# Comportamento
Per ogni use case chiesto dall'utente:
1)  **Struttura del Repository:** Guida l'utente nella definizione della struttura ideale del repository GitHub, focalizzandoti su chiarezza, scalabilità e facilità d'uso per gli 'Enterprise System Prompts'.
2)  **Analisi dei Casi Esempio:** Utilizza il caso 'Architecture Decision Record Generator' come modello per spiegare la struttura di ciascun use case nel repository:
    a) Spiega la funzione e il contenuto atteso del file 'SystemPrompt.md' (il prompt LLM generato).
    b) Spiega l'utilità e il formato del file 'adr-template.md' (esempio di output/template di supporto per le decisioni architettoniche).
    c) Spiega l'utilità e il formato del file 'trade-off-matrix.md' (template per la valutazione sistematica delle opzioni).
3)  **Generazione di Nuovi Use Cases:** Quando richiesto un nuovo use case (es. 'Cloud Migration Strategy Generator'), collabora con l'utente per definire la struttura del prompt, l'output atteso e i template di supporto necessari, mantenendo la coerenza con la struttura 'Architecture Decision Record Generator'.
4)  **Consulenza su Prompt Engineering:** Fornisci best practices di prompt engineering specifiche per il contesto di Enterprise Architecture (es. come definire il 'target audience', 'constraints', e 'output format' all'interno del prompt).
# Tono
- Utilizza un tono professionale, autorevole e collaborativo, tipico di un consulente esperto e di un architetto di alto livello. 
- Rispondi in Ingelse e genera solo markdown in inglese. 
- Mantieni le risposte concise e focalizzate sull'obiettivo.

Show more
Repository Structure Analysis & Guidance
Ottima iniziativa! Creare un repository di system prompts per Enterprise Architecture è un asset strategico. Analizziamo insieme come strutturarlo al meglio.

Current State Assessment
Il tuo repository ha già un'ottima base con l'"Architecture Review Assistant". Questo sarà il nostro modello di riferimento. La struttura attuale dimostra:

Organizzazione chiara per use case
Documentazione completa del prompt stesso
Template di supporto per output strutturati
Pattern replicabili per nuovi casi d'uso
Recommended Repository Structure
enterprise-architecture-prompts/
│
├── README.md                          # Overview e quick start
├── CONTRIBUTING.md                    # Guidelines per contributi
├── LICENSE                            # Licenza (MIT consigliata)
│
├── use-cases/                         # Cartella principale use cases
│   │
│   ├── architecture-review/           # Caso esistente
│   │   ├── SystemPrompt.md           # Il prompt LLM
│   │   ├── README.md                 # Guida uso specifico
│   │   └── templates/                # Template output
│   │       ├── executive-summary.md
│   │       └── detailed-review.md
│   │
│   ├── architecture-decision-records/ # Nuovo caso
│   │   ├── SystemPrompt.md
│   │   ├── README.md
│   │   └── templates/
│   │       ├── adr-template.md
│   │       └── trade-off-matrix.md
│   │
│   └── [altri-use-cases]/
│
├── references/                        # Materiale di supporto condiviso
│   ├── quality-attributes-catalog.md
│   ├── anti-patterns-catalog.md
│   └── architecture-patterns.md
│
└── examples/                          # Esempi completi end-to-end
    ├── architecture-review-example.md
    └── adr-example.md
Anatomy of a Use Case: Architecture Decision Record Generator
Usiamo questo come pattern per tutti i futuri use cases.

1. SystemPrompt.md Structure
Purpose: Questo è il cuore del use case - il prompt da fornire all'LLM.

Key Components:

markdown
# System Prompt: [Use Case Name]

## Your Role
[Define clearly WHO the assistant is and WHAT they do]

## Core Responsibilities
[List 3-5 specific tasks the assistant performs]

## Process/Methodology
[Step-by-step approach the assistant should follow]

## Output Format
[Exact structure of the expected deliverable]

## Quality Criteria
[What makes a good vs bad output]

## Common Pitfalls to Avoid
[Anti-patterns specific to this use case]

## References & Best Practices
[Links to relevant materials in /references]
Why This Works:

Clear scope: L'LLM sa esattamente cosa fare
Structured approach: Riduce variabilità dell'output
Quality gates: Built-in quality control
Reusable: Template applicabile ad altri use cases
2. Template Files (e.g., adr-template.md)
Purpose: Fornisce struttura standardizzata per l'output dell'LLM.

Content Example (ADR Template):

markdown
# ADR-XXX: [Decision Title]

**Date**: YYYY-MM-DD
**Status**: [Proposed | Accepted | Superseded | Deprecated]
**Deciders**: [List of people involved]
**Technical Story**: [Ticket/Issue reference]

## Context and Problem Statement
[What situation triggered this decision? 
What problem are we trying to solve?]

## Decision Drivers
* [Driver 1]
* [Driver 2]
* [Driver n]

## Considered Options
1. [Option 1]
2. [Option 2]
3. [Option n]

## Decision Outcome
**Chosen option**: "[option X]"

**Rationale**: [Why we chose this]

### Positive Consequences
* [e.g., improvement of quality attribute X]

### Negative Consequences
* [e.g., compromising quality attribute Y]

## Pros and Cons of the Options

### [Option 1]
* **Good**, because [argument a]
* **Bad**, because [argument b]

[Repeat for each option]

## Links
* [Related ADRs]
* [External references]
Why This Template:

Consistency: Tutte le ADR hanno la stessa struttura
Traceability: Context e rationale sempre documentati
Decision trail: Status tracking per evoluzioni future
3. Supporting Template: trade-off-matrix.md
Purpose: Strumento di valutazione sistematica per comparare opzioni.

Content Example:

markdown
# Trade-off Analysis Matrix

## Options Under Consideration
- **Option A**: [Brief description]
- **Option B**: [Brief description]
- **Option C**: [Brief description]

## Evaluation Criteria

| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| **Functional Fit** | 25% | 8/10 | 6/10 | 9/10 |
| **Performance** | 20% | 7/10 | 9/10 | 6/10 |
| **Cost** | 15% | 6/10 | 4/10 | 8/10 |
| **Team Expertise** | 15% | 9/10 | 5/10 | 7/10 |
| **Time to Market** | 15% | 8/10 | 6/10 | 7/10 |
| **Maintainability** | 10% | 7/10 | 8/10 | 6/10 |
| **TOTAL** | 100% | **7.5** | **6.6** | **7.4** |

## Detailed Analysis

### Option A: [Name]
**Strengths**:
- [Strength 1]
- [Strength 2]

**Weaknesses**:
- [Weakness 1]

**Risks**:
- [Risk 1]

[Repeat for B and C]

## Recommendation
[Based on analysis, which option and why]
Why This Template:

Objective comparison: Quantifica elementi qualitativi
Weighted criteria: Riflette priorità business
Transparent rationale: Decision facilmente difendibile
Prompt Engineering Best Practices for EA Context
1. Define Clear Boundaries
markdown
❌ Don't: "Help architects make decisions"
✅ Do: "Generate Architecture Decision Records following 
      the Michael Nygard template, evaluating 2-5 options 
      against specified quality attributes"
2. Specify Target Audience
markdown
## Target Audience
This prompt generates content for:
- **Primary**: Enterprise Architects reviewing decisions
- **Secondary**: Development teams implementing solutions
- **Tertiary**: Stakeholders approving budget/timeline

**Adjust tone and detail accordingly**.
3. Include Context Requirements
markdown
## Required Context
Before generating output, the assistant MUST gather:
1. Business problem being solved
2. Key constraints (budget, timeline, team skills)
3. Quality attribute priorities (performance, security, etc.)
4. Current architecture state (greenfield vs brownfield)

**If context is missing, the assistant should ASK before proceeding**.
4. Define Output Format Explicitly
markdown
## Output Format
The assistant produces:
1. **Primary artifact**: ADR in Markdown (1500-2500 words)
2. **Supporting artifact**: Trade-off matrix (table format)
3. **Optional**: Architecture diagrams (C4 model Level 2-3)

**File naming convention**: 
- ADR-YYYY-MM-DD-short-title.md
- tradeoff-YYYY-MM-DD-short-title.md
5. Build in Quality Gates
markdown
## Quality Checklist
Before finalizing output, verify:
- [ ] All considered options have pros/cons documented
- [ ] Decision rationale references business drivers
- [ ] Trade-offs are explicitly stated
- [ ] Risks are identified with mitigation strategies
- [ ] Next steps are actionable and assigned

**If any item fails, revise before presenting**.
Next Steps
Immediate Actions:

Crea la struttura cartelle proposta
Migra "Architecture Review Assistant" nella nuova struttura
Aggiungi README.md principale con navigation
Quick Wins (nuovi use cases da aggiungere):

Cloud Migration Strategy Generator
System Integration Pattern Selector
Non-Functional Requirements Analyzer
Legacy Modernization Assessor
Vuoi che iniziamo con uno di questi nuovi use cases? Posso guidarti step-by-step nella creazione del SystemPrompt.md e dei template correlati.

ti ho fornito il system ptompt che ho scritto per il caso d'use Architecture review. ora devo generare i file oer completare il repoository. ti chiedo ora di generare il file quality-gates.md delle referenze.
il file che devi generare deve essere esclusivamente in formato md, usa gli artifact

quality-gates.md
Code 
Ecco il file quality-gates.md completo per le tue referenze.

Struttura del documento
Ho organizzato il contenuto in 5 gate progressivi che mappano il ciclo di vita architetturale:

Conceptual Architecture Review - Validazione iniziale dell'idea
Detailed Design Review - Design completo prima dell'implementazione
Implementation Readiness - Pronto per iniziare a costruire
Pre-Production Review - Pronto per il deploy in produzione
Post-Launch Review - Validazione dopo il rilascio
Caratteristiche chiave
Per ogni gate troverai:

Exit criteria specifici e misurabili
Red flags che bloccano il passaggio
Categorie logiche (business, technical, operational)
Sezioni di supporto:

Quality Metrics Reference - Soglie numeriche concrete (p50, p95, p99)
Gate Assessment Template - Template per documentare il risultato della review
Usage Guidelines - Come adattare i gate al tuo contesto (startup vs enterprise)
Il documento è pronto per essere utilizzato sia come checklist durante le review, sia come riferimento per stabilire gli standard di qualità nel tuo team.

Vuoi che generi ora un altro file delle referenze (es. anti-patterns-catalog.md o quality-attributes-catalog.md)?

ora genera il file md per example-review-prompts.md

example-review-prompts.md
Code 


Session limit reached ∙ resets 10:00 PM
Upgrade





# Example Review Prompts

## Overview

This document provides ready-to-use prompts for different architecture review scenarios. Each prompt is designed to work with the Architecture Review Assistant system prompt and produces specific, actionable outputs.

---

## Table of Contents

1. [New System Design Review](#new-system-design-review)
2. [Microservices Architecture Review](#microservices-architecture-review)
3. [Cloud Migration Assessment](#cloud-migration-assessment)
4. [API Design Review](#api-design-review)
5. [Security Architecture Review](#security-architecture-review)
6. [Legacy System Modernization](#legacy-system-modernization)
7. [Production Readiness Review](#production-readiness-review)
8. [Performance Optimization Review](#performance-optimization-review)
9. [Data Architecture Review](#data-architecture-review)
10. [Integration Architecture Review](#integration-architecture-review)

---

## 1. New System Design Review

### Scenario
Reviewing a proposed architecture for a greenfield system before development starts.

### Prompt Template

```
I need an architecture review for a new system we're about to build.

## System Context
**System Name**: [e.g., Customer Order Management System]
**Purpose**: [e.g., Handle online orders from web and mobile apps]
**Users**: [e.g., 100K daily active users, peak 500 orders/minute]

## Business Requirements
- [Requirement 1: e.g., Process orders in real-time]
- [Requirement 2: e.g., Support multiple payment providers]
- [Requirement 3: e.g., Generate invoices and send notifications]

## Quality Requirements
- **Performance**: [e.g., Order processing < 2 seconds p95]
- **Availability**: [e.g., 99.9% uptime]
- **Scalability**: [e.g., Handle 3x current traffic within 6 months]
- **Security**: [e.g., PCI DSS compliant for payment data]

## Proposed Architecture

### High-Level Design
[Describe architecture style: e.g., microservices, event-driven, layered]

### Key Components
1. **[Component 1]**: [Description and responsibility]
2. **[Component 2]**: [Description and responsibility]
3. **[Component 3]**: [Description and responsibility]

### Technology Stack
- **Frontend**: [e.g., React, Next.js]
- **Backend**: [e.g., Node.js, Java Spring Boot]
- **Database**: [e.g., PostgreSQL, MongoDB]
- **Message Queue**: [e.g., RabbitMQ, Kafka]
- **Cache**: [e.g., Redis]
- **Cloud Provider**: [e.g., AWS, Azure, GCP]

### Data Flow
[Describe how data flows through the system for key use cases]

## Team Context
- **Team Size**: [e.g., 8 developers, 2 QA, 1 DevOps]
- **Experience**: [e.g., Strong in Java, new to Kafka]
- **Timeline**: [e.g., 6 months to MVP]
- **Budget**: [e.g., $500K including cloud costs]

## Specific Concerns
1. [e.g., Worried about handling payment gateway failures]
2. [e.g., Unsure if we need microservices or monolith is enough]
3. [e.g., Concerned about database scalability]

Please provide a comprehensive architecture review focusing on risks, potential issues, and specific recommendations.
```

### Expected Output
- Executive summary with overall assessment
- Detailed findings across all 9 review dimensions
- Prioritized list of issues (Critical, High, Medium, Low)
- Specific recommendations with effort estimates
- Risk assessment and mitigation strategies

---

## 2. Microservices Architecture Review

### Scenario
Evaluating an existing or proposed microservices architecture for issues like distributed monolith, chatty services, or improper boundaries.

### Prompt Template

```
Review our microservices architecture for potential issues and improvements.

## System Overview
**System**: [e.g., E-commerce Platform]
**Number of Services**: [e.g., 15 microservices]
**Traffic**: [e.g., 1M requests/day]
**Team Structure**: [e.g., 3 teams, 6 developers each]

## Service Inventory

### Service 1: [Service Name]
- **Responsibility**: [What it does]
- **Technology**: [e.g., Node.js, PostgreSQL]
- **Dependencies**: [Which services it calls]
- **Database**: [Shared or dedicated]
- **API Endpoints**: [Number and type: REST/gRPC]
- **Team Ownership**: [Which team owns it]

### Service 2: [Service Name]
[Repeat structure]

[Continue for all services]

## Integration Patterns
- **Service-to-service communication**: [e.g., Synchronous REST calls]
- **Event bus**: [e.g., Kafka with 20 topics]
- **API Gateway**: [e.g., Kong, AWS API Gateway]
- **Service mesh**: [e.g., Istio, Linkerd, or none]

## Current Pain Points
1. [e.g., Deployments require coordinating 5 services]
2. [e.g., One service change breaks 3 others]
3. [e.g., Service A calls Service B calls Service C (deep call chains)]
4. [e.g., Database shared between 3 services]

## Specific Questions
- Are our service boundaries correct?
- Do we have a distributed monolith?
- Is our communication pattern appropriate?
- Should some services be consolidated?

Please identify anti-patterns, assess service granularity, and recommend improvements.
```

### Expected Output
- Service boundary analysis
- Identification of distributed monolith symptoms
- Communication pattern assessment
- Data ownership evaluation
- Specific consolidation or decomposition recommendations
- Refactoring roadmap with priorities

---

## 3. Cloud Migration Assessment

### Scenario
Planning to migrate an on-premises system to the cloud and need to evaluate the proposed migration strategy.

### Prompt Template

```
Review our cloud migration strategy and architecture.

## Current State (On-Premises)

### Application Architecture
- **Type**: [e.g., 3-tier monolithic application]
- **Technology**: [e.g., Java 8, Oracle DB, Apache HTTP Server]
- **Deployment**: [e.g., Physical servers in corporate datacenter]
- **Traffic**: [e.g., 50K daily users, 200 req/sec peak]
- **Data Volume**: [e.g., 2TB database, 500GB files]

### Infrastructure
- **Servers**: [e.g., 8 application servers, 2 database servers]
- **Load Balancer**: [e.g., F5 hardware load balancer]
- **Storage**: [e.g., SAN storage]
- **Backup**: [e.g., Nightly tape backups]

### Current Issues
- [e.g., Cannot scale quickly for seasonal peaks]
- [e.g., Disaster recovery takes 4+ hours]
- [e.g., Hardware refresh costs $500K every 3 years]

## Proposed Target State (Cloud)

### Migration Strategy
- **Approach**: [e.g., Lift-and-shift, Re-platform, Re-architect]
- **Cloud Provider**: [e.g., AWS]
- **Timeline**: [e.g., 9 months]
- **Budget**: [e.g., $300K migration cost, $50K/month operational]

### Target Architecture
- **Compute**: [e.g., ECS containers, EC2 instances]
- **Database**: [e.g., RDS PostgreSQL, Aurora]
- **Storage**: [e.g., S3 for files, EBS for volumes]
- **Network**: [e.g., VPC, CloudFront CDN]
- **Security**: [e.g., IAM, Security Groups, WAF]

### Migration Phases
1. **Phase 1**: [e.g., Migrate database to RDS - 2 months]
2. **Phase 2**: [e.g., Containerize applications - 3 months]
3. **Phase 3**: [e.g., Migrate to ECS - 2 months]
4. **Phase 4**: [e.g., Decommission on-prem - 2 months]

## Constraints
- **Downtime tolerance**: [e.g., Max 4 hours for cutover]
- **Budget limit**: [e.g., Cannot exceed $400K total]
- **Compliance**: [e.g., Must maintain SOC2, HIPAA]
- **Team skills**: [e.g., Team has zero AWS experience]

## Specific Concerns
1. [e.g., Risk of data loss during migration]
2. [e.g., Cloud costs spiraling out of control]
3. [e.g., Performance degradation after migration]

Evaluate the migration strategy, identify risks, and recommend improvements or alternatives.
```

### Expected Output
- Migration strategy assessment
- Risk analysis for each phase
- Cost optimization recommendations
- Performance implications
- Security and compliance validation
- Rollback strategy evaluation
- Team readiness assessment

---

## 4. API Design Review

### Scenario
Reviewing API design before implementation to ensure it's well-structured, scalable, and maintainable.

### Prompt Template

```
Review our API design for a new service.

## API Overview
**Service**: [e.g., Product Catalog API]
**Type**: [e.g., RESTful API, GraphQL, gRPC]
**Consumers**: [e.g., Web app, mobile apps, partner integrations]
**Expected Load**: [e.g., 10K requests/minute peak]

## API Specification

### Authentication & Authorization
- **Auth Method**: [e.g., OAuth 2.0, JWT, API Keys]
- **Authorization Model**: [e.g., RBAC with roles: admin, user, partner]

### Endpoints

#### Endpoint 1: Get Product List
```
GET /api/v1/products
Query Parameters:
  - category: string (optional)
  - page: integer (default: 1)
  - limit: integer (default: 20, max: 100)
  
Response 200:
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "price": number,
      "category": "string"
    }
  ],
  "pagination": {
    "page": number,
    "totalPages": number,
    "totalItems": number
  }
}
```

#### Endpoint 2: Get Product Details
```
GET /api/v1/products/{productId}

Response 200:
{
  "id": "string",
  "name": "string",
  "description": "string",
  "price": number,
  "inventory": number,
  "category": "string",
  "images": ["string"],
  "specifications": {}
}

Response 404:
{
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product not found"
  }
}
```

[Continue for all endpoints]

### Error Handling
- **HTTP Status Codes**: [List which codes are used and when]
- **Error Response Format**: [Show structure]
- **Error Codes**: [List custom error codes]

### Versioning Strategy
- [e.g., URI versioning: /api/v1/, /api/v2/]
- [Deprecation policy: e.g., Support N-1 versions for 6 months]

### Rate Limiting
- [e.g., 1000 requests/hour per API key]
- [Headers: X-RateLimit-Limit, X-RateLimit-Remaining]

### Caching
- [e.g., Cache-Control headers for product data: 5 minutes]
- [ETag support for conditional requests]

## Specific Questions
- Are our endpoints RESTful or have we deviated?
- Is pagination approach scalable?
- Should we use GraphQL instead of REST?
- Is error handling comprehensive?
- Do we need webhooks for real-time updates?

Review for REST best practices, scalability, security, and developer experience.
```

### Expected Output
- RESTful design compliance assessment
- Endpoint structure evaluation
- Versioning strategy review
- Error handling completeness
- Security posture analysis
- Performance and scalability considerations
- Developer experience feedback
- Specific improvement recommendations

---

## 5. Security Architecture Review

### Scenario
Comprehensive security review before production launch or after a security audit finding.

### Prompt Template

```
Conduct a security architecture review for our system.

## System Overview
**Application**: [e.g., Healthcare Patient Portal]
**Sensitivity**: [e.g., Handles PHI data (HIPAA-regulated)]
**Users**: [e.g., 50K patients, 500 healthcare providers]
**Deployment**: [e.g., AWS multi-region]

## Current Security Architecture

### Authentication
- **User Authentication**: [e.g., Email/password + MFA via SMS]
- **Session Management**: [e.g., JWT tokens, 1-hour expiry]
- **Password Policy**: [e.g., Min 12 chars, complexity requirements]
- **SSO Support**: [e.g., SAML 2.0 for healthcare provider orgs]

### Authorization
- **Model**: [e.g., RBAC with 4 roles: Patient, Provider, Admin, Auditor]
- **Permissions**: [Describe key permissions]
- **Enforcement**: [e.g., Application layer + database row-level security]

### Data Protection

#### Encryption at Rest
- **Database**: [e.g., PostgreSQL with TDE enabled]
- **File Storage**: [e.g., S3 with SSE-KMS]
- **Backups**: [e.g., Encrypted with customer-managed keys]

#### Encryption in Transit
- **External**: [e.g., TLS 1.3, certificate from LetsEncrypt]
- **Internal**: [e.g., TLS between microservices]
- **API**: [e.g., HTTPS only, HSTS enabled]

### Secrets Management
- [e.g., AWS Secrets Manager for DB credentials, API keys]
- [Rotation policy: e.g., Every 90 days]

### Network Security
- **Perimeter**: [e.g., AWS WAF rules, DDoS protection via Shield]
- **Segmentation**: [e.g., VPC with public/private subnets]
- **Firewalls**: [e.g., Security groups, NACLs]
- **Bastion Host**: [e.g., For administrative access]

### Application Security
- **Input Validation**: [e.g., Server-side validation for all inputs]
- **SQL Injection Prevention**: [e.g., Parameterized queries only]
- **XSS Prevention**: [e.g., Content Security Policy, output encoding]
- **CSRF Protection**: [e.g., Anti-CSRF tokens]
- **Dependency Scanning**: [e.g., Snyk for vulnerability detection]

### Audit & Logging
- **Authentication Events**: [e.g., Logged to CloudWatch]
- **Data Access**: [e.g., All PHI access logged with user ID, timestamp]
- **Changes**: [e.g., Audit trail for data modifications]
- **Retention**: [e.g., 7 years for compliance]

### Compliance
- **Regulations**: [e.g., HIPAA, GDPR]
- **Certifications**: [e.g., SOC 2 Type II]
- **Audits**: [e.g., Annual penetration test, quarterly vulnerability scans]

## Recent Security Testing

### Penetration Test Results
- **Date**: [e.g., 3 months ago]
- **Critical Findings**: [e.g., None]
- **High Findings**: [e.g., 2 - both remediated]
- **Medium Findings**: [e.g., 5 - 3 remediated, 2 in progress]

### Known Issues
1. [e.g., MFA only via SMS, not TOTP apps]
2. [e.g., No automated security headers testing in CI/CD]
3. [e.g., Logs stored in same region as production data]

## Threat Model
- **Assets**: [e.g., Patient health records, provider credentials]
- **Threats**: [e.g., Data breach, ransomware, insider threat]
- **Attack Vectors**: [e.g., Compromised credentials, SQL injection, XSS]

## Specific Concerns
1. [e.g., Are we HIPAA compliant?]
2. [e.g., Is our encryption approach sufficient?]
3. [e.g., Should we implement additional DLP controls?]

Perform comprehensive security review and identify gaps or risks.
```

### Expected Output
- Security posture assessment across all layers
- Compliance gap analysis
- Threat model validation
- Critical vulnerability identification
- Defense-in-depth evaluation
- Specific security recommendations prioritized by risk
- Remediation roadmap

---

## 6. Legacy System Modernization

### Scenario
Assessing options for modernizing a legacy system and reviewing the proposed approach.

### Prompt Template

```
Review our legacy system modernization strategy.

## Current Legacy System

### Overview
- **System Name**: [e.g., Order Management System]
- **Age**: [e.g., 15 years old]
- **Technology**: [e.g., Java 6, Oracle 10g, JSP]
- **Architecture**: [e.g., Monolithic 3-tier]
- **LOC**: [e.g., 500K lines of code]
- **Documentation**: [e.g., Minimal, outdated]

### Business Impact
- **Revenue**: [e.g., Processes $50M orders/year]
- **Users**: [e.g., 200 internal users, 10K customers]
- **Criticality**: [e.g., Business stops if system is down]

### Current Problems
1. [e.g., Cannot deploy without 4-hour downtime]
2. [e.g., Adding features takes 3-6 months]
3. [e.g., Frequent production issues due to technical debt]
4. [e.g., Hard to find developers with legacy skills]
5. [e.g., Cannot integrate with modern systems easily]

### Technical Debt
- [e.g., No automated tests, manual regression testing takes 2 weeks]
- [e.g., Database has 500 tables with unclear relationships]
- [e.g., Business logic scattered across DB stored procedures and Java code]
- [e.g., No API layer, direct database access from UI]

## Proposed Modernization Strategy

### Approach
- **Strategy**: [e.g., Strangler Fig Pattern - incrementally replace]
- **Duration**: [e.g., 18-24 months]
- **Budget**: [e.g., $2M]

### Target Architecture
- **Style**: [e.g., Microservices with event-driven communication]
- **Technology**: [e.g., Spring Boot, PostgreSQL, Kafka, React]
- **Deployment**: [e.g., Kubernetes on AWS EKS]

### Migration Phases

#### Phase 1: API Layer (Months 1-3)
- Build API façade in front of legacy system
- Expose core functionality as REST APIs
- Continue using legacy UI and database

#### Phase 2: Extract Order Processing (Months 4-9)
- Build new Order Service
- Dual-write to both old and new systems
- Gradually route traffic to new service
- Decommission old order module

#### Phase 3: Extract Customer Management (Months 10-15)
[Describe]

#### Phase 4: Extract Inventory (Months 16-21)
[Describe]

#### Phase 5: Decommission Legacy (Months 22-24)
[Describe]

### Data Migration Strategy
- [e.g., ETL pipelines to sync data between old and new]
- [e.g., Event-driven CDC (Change Data Capture) for real-time sync]
- [e.g., One-time bulk migration for reference data]

### Risk Mitigation
- [e.g., Feature flags to route traffic between old and new]
- [e.g., Comprehensive test suite before each cutover]
- [e.g., Rollback plan for each phase]

## Team & Organization
- **Current Team**: [e.g., 5 developers maintaining legacy]
- **Modernization Team**: [e.g., 10 developers for new development]
- **Training Needs**: [e.g., Team needs Kubernetes, microservices training]

## Constraints
- **Zero Downtime Required**: [Business cannot tolerate outages]
- **Must Support Legacy for 2 Years**: [Some customers on old version]
- **Budget Ceiling**: [Cannot exceed $2.5M]

## Specific Questions
- Is strangler fig the right approach?
- Should we consider a full rewrite instead?
- Are our phases too aggressive?
- How do we handle data consistency during migration?

Evaluate the modernization strategy, identify risks, and provide recommendations.
```

### Expected Output
- Modernization approach assessment
- Risk analysis for each phase
- Data migration strategy evaluation
- Technical debt prioritization
- Team readiness assessment
- Cost-benefit analysis
- Alternative strategies consideration
- Detailed recommendations for improvement

---

## 7. Production Readiness Review

### Scenario
Final review before production launch to ensure operational readiness.

### Prompt Template

```
Conduct a production readiness review for our system launching in 2 weeks.

## System Overview
**System**: [e.g., Payment Processing Service]
**Launch Date**: [e.g., December 1, 2024]
**Expected Load**: [e.g., 500 transactions/minute initially, 2K at peak]
**Criticality**: [e.g., High - revenue impacting]

## Functional Testing

### Test Coverage
- **Unit Tests**: [e.g., 85% coverage]
- **Integration Tests**: [e.g., Critical paths covered]
- **E2E Tests**: [e.g., 20 scenarios automated]
- **UAT**: [e.g., Completed, 3 minor issues open]

### Test Results
- **Pass Rate**: [e.g., 98% (2 known bugs, low priority)]
- **Critical User Journeys**: [e.g., All passing]
- **Edge Cases**: [e.g., 15/20 tested]

## Performance Testing

### Load Test Results
```
Test Scenario: Peak Load (2000 req/min)
Duration: 30 minutes
Results:
  - Throughput: 2100 req/min (✅ Above target)
  - Response Time p50: 180ms (✅ Target <200ms)
  - Response Time p95: 450ms (✅ Target <500ms)
  - Response Time p99: 850ms (✅ Target <1000ms)
  - Error Rate: 0.02% (✅ Target <0.1%)
  - CPU Utilization: 65% average (✅ Acceptable)
  - Memory Utilization: 70% average (✅ Acceptable)
```

### Stress Test
- **Max Throughput**: [e.g., 3500 req/min before degradation]
- **Breaking Point**: [e.g., 4200 req/min - OOM errors]
- **Recovery**: [e.g., Auto-recovers in 2 minutes after load reduction]

### Scalability Test
- [e.g., Horizontal scaling tested: 2 → 6 instances, linear performance]

## Security Testing

### Security Scan Results
- **SAST**: [e.g., Clean - no issues]
- **DAST**: [e.g., 2 medium findings - both remediated]
- **Dependency Scan**: [e.g., 5 low-severity vulnerabilities - acceptable]
- **Penetration Test**: [e.g., Scheduled for next week]

### Security Checklist
- [✅] All secrets in Secrets Manager
- [✅] TLS 1.3 for all endpoints
- [✅] Input validation on all API calls
- [✅] SQL injection prevention verified
- [❌] MFA for admin users (in progress)

## Infrastructure

### Production Environment
- **Cloud Provider**: [e.g., AWS us-east-1]
- **Compute**: [e.g., ECS Fargate, 4 tasks initially, auto-scale to 12]
- **Database**: [e.g., RDS PostgreSQL, db.r5.2xlarge, Multi-AZ]
- **Cache**: [e.g., ElastiCache Redis, cache.r5.large]
- **Load Balancer**: [e.g., Application Load Balancer]

### Disaster Recovery
- **Backup**: [e.g., Automated daily backups, 30-day retention]
- **RTO**: [e.g., 4 hours]
- **RPO**: [e.g., 1 hour]
- **DR Test**: [e.g., Not yet conducted - planned for this week]

## Observability

### Monitoring
- **Metrics**: [e.g., CloudWatch dashboards for latency, error rate, throughput]
- **Logs**: [e.g., Centralized in CloudWatch Logs]
- **Tracing**: [e.g., AWS X-Ray for distributed tracing]
- **Dashboards**: [e.g., 2 dashboards - operations and business metrics]

### Alerting
```
Alerts Configured:
1. High Error Rate (>1%) - Severity: Critical - Notify: PagerDuty
2. High Latency (p95 >1s) - Severity: High - Notify: Slack + Email
3. Low Throughput (<100 req/min) - Severity: Medium - Notify: Slack
4. Database CPU >80% - Severity: High - Notify: PagerDuty
5. Failed Deployment - Severity: Critical - Notify: PagerDuty
```

### Runbooks
- [✅] Deployment runbook
- [✅] Rollback procedure
- [✅] Common issues troubleshooting
- [❌] Disaster recovery runbook (in progress)

## Deployment

### CI/CD Pipeline
- **Build**: [e.g., GitHub Actions - 5 minutes]
- **Tests**: [e.g., Automated - unit, integration, smoke tests]
- **Deploy**: [e.g., Blue-green deployment via ECS]
- **Rollback**: [e.g., Automated rollback on health check failure]

### Deployment Strategy
- **Launch Plan**: [e.g., Canary - 10% → 50% → 100% over 4 hours]
- **Feature Flags**: [e.g., LaunchDarkly for gradual rollout]
- **Rollback Time**: [e.g., <5 minutes]

## Operational Readiness

### On-Call
- **Rotation**: [e.g., 3 engineers, 1-week rotation]
- **Escalation**: [e.g., Level 1 → Level 2 → CTO]
- **Response Time SLA**: [e.g., Critical: 15 min, High: 1 hour]

### Documentation
- [✅] Architecture documentation
- [✅] API documentation (OpenAPI spec)
- [✅] Operations manual
- [❌] User documentation (in progress)

### Team Readiness
- [✅] Team trained on new system
- [✅] On-call rotation staffed
- [❌] Post-launch support plan (needs definition)

## Open Issues

| ID | Description | Severity | Status | Owner | Due |
|----|-------------|----------|--------|-------|-----|
| 1 | MFA for admin users | Medium | In Progress | Alice | Nov 25 |
| 2 | DR runbook incomplete | High | In Progress | Bob | Nov 28 |
| 3 | User docs not ready | Low | In Progress | Carol | Dec 5 |
| 4 | Pen test not completed | High | Scheduled | Security | Nov 30 |

## Specific Concerns
1. [e.g., Are we ready to launch with pen test incomplete?]
2. [e.g., Is our on-call team adequately trained?]
3. [e.g., Should we do a smaller canary (5%) first?]

Evaluate production readiness and provide go/no-go recommendation.
```

### Expected Output
- Go/No-Go recommendation with clear rationale
- Production readiness checklist assessment
- Critical blockers identification
- Risk assessment for launch
- Contingency plans evaluation
- Post-launch monitoring plan
- Specific actions before launch

---

## 8. Performance Optimization Review

### Scenario
System experiencing performance issues in production; need to identify bottlenecks and optimization opportunities.

### Prompt Template

```
Review our system for performance optimization opportunities.

## Current Performance Issues

### Symptoms
1. [e.g., API response time p95 is 3.5s, target is 500ms]
2. [e.g., Database CPU at 95% during peak hours]
3. [e.g., Users complaining about slow page loads]
4. [e.g., Timeout errors occurring 5% of the time]

### Performance Metrics

#### Current State
```
Metric                  | Current | Target | Status
------------------------|---------|--------|--------
Throughput             | 800/min | 1000/min | ❌
Response Time (p50)    | 1.2s    | 200ms  | ❌
Response Time (p95)    | 3.5s    | 500ms  | ❌
Response Time (p99)    | 8.2s    | 1000ms | ❌
Error Rate             | 5%      | <0.1%  | ❌
Database Connections   | 90/100  | <80    | ⚠️
Cache Hit Rate         | 45%     | >80%   | ❌
```

## System Architecture

### Current Architecture
- **Frontend**: [e.g., React SPA]
- **API Layer**: [e.g., Node.js Express, 4 instances]
- **Application Logic**: [e.g., Java Spring Boot, 6 instances]
- **Database**: [e.g., PostgreSQL, single instance db.m5.xlarge]
- **Cache**: [e.g., Redis, single node cache.t3.small]

### Key Endpoints

#### Slow Endpoint 1: GET /api/products
- **Current p95**: [e.g., 4.2s]
- **Volume**: [e.g., 400 req/min]
- **Operations**: 
  - Query products table (800K rows)
  - Join with categories, reviews, inventory
  - Calculate average ratings
  - No pagination limit

#### Slow Endpoint 2: POST /api/orders
- **Current p95**: [e.g., 2.8s]
- **Volume**: [e.g., 200 req/min]
- **Operations**:
  - Validate order data
  - Check inventory (5 sequential DB queries)
  - Call payment gateway (external, 1.5s average)
  - Send order confirmation email (synchronous)
  - Update inventory (row locking)

### Database Analysis

#### Query Performance
```sql
-- Slow Query 1: Product Search
SELECT p.*, c.name as category, AVG(r.rating) as avg_rating
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
LEFT JOIN reviews r ON r.product_id = p.id
WHERE p.active = true
GROUP BY p.id, c.name;

Execution Time: 3.2s
Rows Scanned: 800K
Rows Returned: 5K
```

#### Missing Indexes
- [e.g., No index on products.active]
- [e.g., No composite index on (category_id, active)]

#### N+1 Query Problems
- [e.g., Order endpoint makes 1 query for order, then 1 query per item]

### Caching Strategy
- **Current**: [e.g., Cache only user sessions]
- **Cache Hit Rate**: [e.g., 45%]
- **TTL**: [e.g., 5 minutes]
- **Not Cached**: [e.g., Product data, category lists, inventory status]

### External Dependencies
- **Payment Gateway**: [e.g., Average 1.5s, p95 2.8s, no timeout/circuit breaker]
- **Email Service**: [e.g., Synchronous call, 800ms average]
- **Inventory Service**: [e.g., 5 serial calls, 200ms each = 1s total]

## Profiling Data

### Application Profiling
```
Top Time Consumers (Order Endpoint):
1. Payment gateway call: 52% (1.5s)
2. Email sending: 18% (800ms)
3. Database queries: 20% (600ms)
4. Business logic: 
