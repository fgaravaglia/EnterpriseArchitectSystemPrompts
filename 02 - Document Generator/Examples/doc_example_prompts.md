# Example Prompts - Documentation Generator Use Cases

This file contains real-world examples of how to interact with the Documentation Generator to get high-quality architectural documentation.

---

## Scenario 1: Creating C4 Documentation from Scratch

### User Prompt

```
I need to document a new microservices-based e-commerce platform. Here's what we have:

- React frontend (SPA) hosted on Cloudflare
- Node.js API Gateway that routes requests
- Three backend services: 
  - Product Service (Go, manages product catalog)
  - Order Service (Java Spring Boot, handles orders)
  - User Service (Node.js, manages authentication and user profiles)
- PostgreSQL databases (one per service)
- Redis for caching and sessions
- RabbitMQ for async communication between services
- Stripe for payments (external)
- SendGrid for emails (external)

Users are customers who shop and admins who manage inventory.

Can you create comprehensive C4 documentation with Context, Container, and Component views?
```

### Expected Output Structure

The assistant should produce:
1. **System Context Diagram** showing users (Customer, Admin) and external systems (Stripe, SendGrid)
2. **Container Diagram** showing all internal containers (Frontend, API Gateway, 3 services, databases, Redis, RabbitMQ)
3. **Component Diagrams** for at least 1-2 key services (e.g., Order Service showing controllers, services, repositories)
4. Text descriptions for each diagram
5. Technology rationale section
6. Deployment considerations

---

## Scenario 2: Updating Existing Documentation

### User Prompt

```
We have existing architecture documentation (C4 model) for our payment processing system.

Changes we made:
- Added a new Fraud Detection Service (Python, scikit-learn)
- Moved from synchronous REST calls to event-driven with Kafka
- Introduced API Gateway (Kong) in front of all services
- Migrated from MySQL to PostgreSQL

Please update the Container and Component diagrams to reflect these changes. 
Also add a section explaining the migration rationale and new data flow patterns.
```

### Expected Behavior

The assistant should:
1. Ask for the existing documentation or work from description
2. Identify what changed at each C4 level
3. Update Container diagram with new components (Fraud Service, Kafka, Kong)
4. Update relationships to show event-driven flow
5. Add new Component diagram for Fraud Detection Service
6. Create a "Changes and Rationale" section
7. Update technology stack documentation
8. Suggest creating an ADR for the migration

---

## Scenario 3: Documentation from Meeting Notes

### User Prompt

```
I have notes from our architecture design meeting. Can you help structure this into proper documentation?

Meeting Notes:
"We discussed the new analytics platform. Marketing needs real-time dashboards. 
Data comes from our main app database (Postgres, has customer data and events).
We decided to use Kafka to stream events. There's a consumer service that will 
process events and store aggregated data in ClickHouse for fast queries.
Grafana will be the dashboard tool. We also need to export data to S3 for 
long-term storage and ML training. The ML team will use SageMaker.
Security team wants all data encrypted at rest and in transit.
We have 6 months and a team of 4 developers."

Please create a complete architecture document using C4 model.
```

### Expected Behavior

The assistant should:
1. Extract structured information from unstructured notes
2. Identify all components: Source (PostgreSQL), Stream (Kafka), Processor (Consumer Service), Storage (ClickHouse, S3), Visualization (Grafana), ML (SageMaker)
3. Create Context diagram showing the analytics platform and its users
4. Create Container diagram with all identified containers
5. Add sections for:
   - Quality attributes (real-time, security requirements)
   - Constraints (timeline, team size)
   - Technology choices rationale
   - Implementation roadmap suggestion
6. Flag missing information (e.g., "What language for Consumer Service?")

---

## Scenario 4: Reverse Engineering Documentation from Code

### User Prompt

```
I have a codebase but no documentation. Here's the structure:

```
src/
├── api/
│   ├── controllers/
│   │   ├── AuthController.ts
│   │   ├── ProductController.ts
│   │   └── OrderController.ts
│   ├── services/
│   │   ├── AuthService.ts
│   │   ├── ProductService.ts
│   │   ├── OrderService.ts
│   │   └── PaymentService.ts
│   ├── repositories/
│   │   ├── UserRepository.ts
│   │   ├── ProductRepository.ts
│   │   └── OrderRepository.ts
│   └── middleware/
│       ├── authentication.ts
│       └── validation.ts
├── database/
│   └── connection.ts (connects to PostgreSQL)
├── cache/
│   └── redis-client.ts
└── external/
    ├── stripe-client.ts
    └── sendgrid-client.ts
```

Technologies: Node.js, TypeScript, Express, PostgreSQL, Redis

Can you create Component and Container diagrams from this structure?
```

### Expected Behavior

The assistant should:
1. Identify the container as a Node.js API application
2. Map code structure to components:
   - Controllers → API Layer components
   - Services → Business Logic components
   - Repositories → Data Access components
   - Middleware → Cross-cutting concerns
3. Identify external integrations (Stripe, SendGrid)
4. Identify infrastructure (PostgreSQL, Redis)
5. Create Component diagram showing layered architecture
6. Create Container diagram showing API + Database + Cache + External services
7. Infer typical data flows (Controller → Service → Repository → Database)
8. Suggest adding Context diagram with business context

---

## Scenario 5: Migration Architecture Documentation

### User Prompt

```
We're migrating from a monolithic .NET application to microservices. 

Current state:
- ASP.NET MVC monolith (C#)
- SQL Server database
- All features in one codebase
- Deployed on Windows Server

Target state:
- Microservices (Java Spring Boot and Node.js)
- Domain-driven design with bounded contexts
- Kubernetes deployment
- PostgreSQL for most services, MongoDB for one
- Event-driven communication with Kafka

Migration strategy:
- Strangler Fig pattern
- 18-month timeline
- Three phases: Phase 1 extract User/Auth, Phase 2 extract Orders, Phase 3 extract Products

Create documentation showing:
1. Current architecture
2. Target architecture  
3. Migration path with interim states
```

### Expected Behavior

The assistant should create:
1. **Current State Documentation**:
   - Container diagram of monolith
   - Component diagram showing main modules

2. **Target State Documentation**:
   - Complete C4 documentation of microservices architecture
   - Multiple Container diagrams for target state

3. **Migration Path**:
   - Phase diagrams showing interim architectures
   - Hybrid state documentation (monolith + extracted services)
   - Integration patterns during migration (API Gateway, Anti-Corruption Layer)

4. **Additional sections**:
   - Risk assessment per phase
   - Rollback strategies
   - Data migration approach
   - Testing strategy

---

## Scenario 6: Domain-Specific Documentation

### User Prompt

```
I need to document our healthcare platform architecture for a HIPAA compliance audit.

System overview:
- Patient portal (React)
- Provider portal (Angular)
- FHIR API (Java) for interoperability
- EHR integration service
- Appointment scheduling service
- Billing service
- All services use PostgreSQL
- HL7 messages via Mirth Connect
- AWS deployment with encryption everywhere

Compliance requirements:
- All PHI encrypted at rest and in transit
- Audit logging for all data access
- Role-based access control
- Data retention policies
- Business Associate Agreements with vendors

Focus on security architecture and compliance controls in the documentation.
```

### Expected Behavior

The assistant should:
1. Create standard C4 diagrams (Context, Container, Component)
2. Add specialized views:
   - **Security Architecture View**: showing encryption, auth flows, network segmentation
   - **Compliance View**: mapping components to HIPAA requirements
   - **Data Flow View**: showing PHI data paths with security controls
3. Documentation sections:
   - Security controls per component
   - Audit logging strategy
   - Access control model
   - Encryption details (at rest, in transit, key management)
   - Third-party integrations and BAAs
   - Incident response procedures
4. Annotate diagrams with security zones/boundaries
5. Create compliance matrix (Component → HIPAA requirement mapping)

---

## Scenario 7: Quick Documentation for Proof of Concept

### User Prompt

```
We built a quick POC for a real-time chat application. Need to document it fast for a stakeholder presentation tomorrow.

What we have:
- React Native mobile app
- Socket.io server (Node.js)
- MongoDB for message persistence
- Redis for presence (who's online)
- AWS S3 for file/image uploads
- Push notifications via Firebase

Key features:
- 1-to-1 and group chats
- Real-time typing indicators
- Message history
- File sharing
- Presence status

Just need high-level architecture diagram and brief description. Keep it simple for non-technical stakeholders.
```

### Expected Behavior

The assistant should:
1. Create a simplified Context diagram (users + system)
2. Create a Container diagram (focus on visual clarity over detail)
3. Use simple, business-friendly language
4. Include brief bullet points highlighting:
   - Real-time capabilities (Socket.io)
   - Scalability aspects (Redis, MongoDB)
   - Mobile-first design
   - File handling
5. Add a simple flow diagram: User sends message → Server → Real-time delivery → Storage
6. Keep total documentation under 2 pages
7. Use visual emphasis over text

---

## Scenario 8: Multi-System Ecosystem Documentation

### User Prompt

```
I need to document our entire e-commerce ecosystem, not just one system.

Systems:
1. Customer-facing website (main e-commerce)
2. Mobile app (iOS + Android)
3. Admin portal for operations
4. Warehouse Management System (WMS) - legacy, can't change
5. ERP system (SAP) - for finance
6. Marketing platform (in-house)
7. Analytics platform
8. Customer support system (Zendesk)

Integration points:
- Orders flow from website/app to WMS
- Inventory syncs between WMS and e-commerce
- Financial data goes to SAP
- Customer data syncs to marketing and analytics
- Support tickets link to orders

Need documentation that shows how everything connects.
```

### Expected Behavior

The assistant should:
1. Create a **System Landscape diagram** showing all 8 systems
2. Create **System Context diagrams** for each system showing its specific integrations
3. Create an **Integration View** showing:
   - Integration patterns (sync/async, protocols)
   - Data flows between systems
   - Integration middleware if any
4. Documentation sections:
   - System catalog (brief description of each)
   - Integration matrix (which systems talk to which)
   - Data ownership (which system is source of truth for what)
   - Integration technologies (REST, message queues, file transfer, etc.)
5. Recommend breaking down into separate detailed docs per system
6. Identify integration risks (especially with legacy WMS)

---

## Scenario 9: Documentation with Quality Attribute Focus

### User Prompt

```
Document our video streaming platform with strong focus on performance and scalability.

Architecture:
- CDN (Cloudflare) for content delivery
- Origin servers (Nginx)
- Transcoding service (FFmpeg cluster)
- Metadata API (Go)
- PostgreSQL for metadata
- S3 for video storage
- Elasticsearch for search
- Redis for rate limiting and caching

Requirements:
- Must handle 100K concurrent viewers
- 99.99% availability
- < 2s video start time
- Global audience (Europe, US, Asia)
- DDoS protection

Document with emphasis on how architecture achieves these quality attributes.
```

### Expected Behavior

The assistant should:
1. Create standard C4 diagrams
2. Annotate diagrams with performance characteristics:
   - CDN: "Reduces latency to <50ms"
   - Redis: "Cache hit rate >95%"
   - Transcoding: "Horizontal scaling for burst capacity"
3. Add **Quality Attribute Scenarios** section:
   - Performance scenario: user clicks play → video starts in <2s
   - Scalability scenario: traffic spike from 10K to 100K users
   - Availability scenario: origin server failure
4. Create specialized views:
   - **Deployment View** showing global distribution
   - **Scalability View** showing autoscaling groups
   - **Resilience View** showing redundancy and failover
5. Documentation sections for each quality attribute:
   - How performance is achieved
   - Scaling strategies
   - Availability tactics (redundancy, health checks, failover)
   - Security measures (DDoS protection, rate limiting)

---

## Scenario 10: API-First Documentation

### User Prompt

```
We're designing a new API platform using API-first approach. 
Need architecture documentation that emphasizes the API design.

Platform:
- RESTful API (OpenAPI 3.0 spec)
- GraphQL API (for mobile apps)
- Webhook system for events
- API Gateway (Kong) with rate limiting, auth
- Multiple backend services
- API documentation portal (developer.company.com)

Key aspects:
- Versioning strategy (URL-based)
- Authentication (OAuth 2.0 + API keys)
- Rate limiting (tier-based)
- Developer experience is priority
- Will be public API used by partners

Focus on API architecture and governance.
```

### Expected Behavior

The assistant should:
1. Create Container diagram showing API layer architecture
2. Create Component diagram of API Gateway showing:
   - Auth plugin
   - Rate limiting plugin
   - Routing logic
   - Analytics/logging
3. Add specialized sections:
   - **API Design Principles** (RESTful, GraphQL decisions)
   - **Versioning Strategy** with examples
   - **Authentication & Authorization** flows
   - **Rate Limiting Tiers** (Free, Pro, Enterprise)
   - **Developer Onboarding** flow
4. Create sequence diagrams for:
   - OAuth 2.0 flow
   - Typical API call with auth
   - Webhook delivery
5. Include API governance:
   - Design review process
   - Breaking changes policy
   - Deprecation strategy
   - SLA commitments

---

## Tips for Effective Prompts

### DO provide:
✅ **Purpose/goal** of the system
✅ **Technologies used** (be specific)
✅ **Key requirements** (performance, security, etc.)
✅ **Constraints** (budget, timeline, team)
✅ **Audience** for the documentation
✅ **Existing context** if updating docs

### DON'T:
❌ Be vague about technologies ("a database" vs "PostgreSQL 15")
❌ Forget to mention external systems and integrations
❌ Skip quality requirements
❌ Assume the assistant knows your business domain

### Follow-up Questions to Expect

The assistant may ask:
- "Who is the primary audience for this documentation?"
- "What's the most critical quality attribute? (performance/security/cost)"
- "Are there any constraints I should be aware of?"
- "What level of detail do you need? (high-level vs detailed)"
- "Should I include deployment/infrastructure details?"
- "Are there any compliance requirements?"

### Iterating on Generated Documentation

After initial generation, refine with prompts like:
- "Add more detail to the security aspects"
- "Simplify this for executive audience"
- "Add a deployment diagram showing AWS infrastructure"
- "Include a migration section from current to target state"
- "Add sequence diagrams for the main user flows"
- "Create a separate component diagram for the API Gateway"