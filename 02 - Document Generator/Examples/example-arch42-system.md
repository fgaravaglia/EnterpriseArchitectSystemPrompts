**Appointment Service** (Example microservice decomposition):

```
┌───────────────────────────────────────────────────────┐
│          Appointment Service (Whitebox)               │
│                                                       │
│  ┌─────────────────────────────────────────────┐     │
│  │          API Layer                          │     │
│  │  ┌────────────────┐  ┌────────────────┐    │     │
│  │  │AppointmentCtrlr│  │AvailabilityCtrl│    │     │
│  │  │(REST endpoints)│  │(REST endpoints) │    │     │
│  │  └────────┬───────┘  └────────┬───────┘    │     │
│  └───────────┼──────────────────┼─────────────┘     │
│              │                  │                    │
│  ┌───────────▼──────────────────▼─────────────┐     │
│  │       Application Service Layer            │     │
│  │  ┌────────────────────────────────────┐    │     │
│  │  │  AppointmentApplicationService     │    │     │
│  │  │  - BookAppointment()               │    │     │
│  │  │  - CancelAppointment()             │    │     │
│  │  │  - GetAvailableSlots()             │    │     │
│  │  └────────┬───────────────────────────┘    │     │
│  └───────────┼────────────────────────────────┘     │
│              │                                       │
│  ┌───────────▼────────────────────────────────┐     │
│  │         Domain Layer                       │     │
│  │  ┌──────────────┐  ┌──────────────────┐   │     │
│  │  │ Appointment  │  │AppointmentPolicy │   │     │
│  │  │  (Aggregate) │  │ (Domain Service) │   │     │
│  │  │              │  │                  │   │     │
│  │  │ - patientId  │  │ - ValidateSlot() │   │     │
│  │  │ - providerId │  │ - CheckConflict()│   │     │
│  │  │ - datetime   │  │                  │   │     │
│  │  │ - status     │  └──────────────────┘   │     │
│  │  │ - Cancel()   │                         │     │
│  │  └──────────────┘                         │     │
│  └───────────┬────────────────────────────────┘     │
│              │                                       │
│  ┌───────────▼────────────────────────────────┐     │
│  │      Infrastructure Layer                  │     │
│  │  ┌──────────────┐  ┌──────────────────┐   │     │
│  │  │Appointment   │  │  Centricity      │   │     │
│  │  │Repository    │  │  Client          │   │     │
│  │  │(SQL DB)      │  │  (SOAP API)      │   │     │
│  │  └──────────────┘  └──────────────────┘   │     │
│  │  ┌──────────────────────────────────┐     │     │
│  │  │  Service Bus Publisher           │     │     │
│  │  │  (Appointment events)            │     │     │
│  │  └──────────────────────────────────┘     │     │
│  └────────────────────────────────────────────┘     │
└───────────────────────────────────────────────────────┘
```

**Responsibilities**:

| Component | Responsibility |
|-----------|----------------|
| **API Layer** | REST endpoints, request validation, DTOs |
| **Application Service** | Use case orchestration, transaction boundaries |
| **Domain Layer** | Business rules, domain entities, invariants |
| **Infrastructure Layer** | Database access, external API clients, messaging |

### 5.3 Level 3: Component Details

**Appointment Aggregate (Domain Model)**:

```csharp
public class Appointment : AggregateRoot
{
    public Guid Id { get; private set; }
    public Guid PatientId { get; private set; }
    public Guid ProviderId { get; private set; }
    public DateTime ScheduledDateTime { get; private set; }
    public AppointmentType Type { get; private set; }
    public AppointmentStatus Status { get; private set; }
    public string CancellationReason { get; private set; }
    public DateTime CreatedAt { get; private set; }
    
    // Domain Events
    private List<DomainEvent> _domainEvents = new();
    public IReadOnlyList<DomainEvent> DomainEvents => _domainEvents;
    
    // Factory Method
    public static Appointment Schedule(
        Guid patientId, 
        Guid providerId, 
        DateTime scheduledTime,
        AppointmentType type)
    {
        // Business rule: Cannot book in the past
        if (scheduledTime <= DateTime.UtcNow)
            throw new InvalidOperationException("Cannot book past appointments");
        
        // Business rule: Must be during business hours
        if (scheduledTime.Hour < 8 || scheduledTime.Hour > 17)
            throw new InvalidOperationException("Outside business hours");
        
        var appointment = new Appointment
        {
            Id = Guid.NewGuid(),
            PatientId = patientId,
            ProviderId = providerId,
            ScheduledDateTime = scheduledTime,
            Type = type,
            Status = AppointmentStatus.Scheduled,
            CreatedAt = DateTime.UtcNow
        };
        
        appointment.AddDomainEvent(new AppointmentScheduledEvent(appointment.Id));
        return appointment;
    }
    
    // Domain Behavior
    public void Cancel(string reason)
    {
        // Business rule: Cannot cancel completed appointments
        if (Status == AppointmentStatus.Completed)
            throw new InvalidOperationException("Cannot cancel completed appointment");
        
        // Business rule: Cannot cancel less than 24h before
        if (ScheduledDateTime.Subtract(DateTime.UtcNow).TotalHours < 24)
            throw new InvalidOperationException("Must cancel 24h in advance");
        
        Status = AppointmentStatus.Cancelled;
        CancellationReason = reason;
        AddDomainEvent(new AppointmentCancelledEvent(Id, reason));
    }
    
    public void MarkCompleted()
    {
        if (Status != AppointmentStatus.Scheduled)
            throw new InvalidOperationException("Only scheduled appointments can be completed");
        
        Status = AppointmentStatus.Completed;
        AddDomainEvent(new AppointmentCompletedEvent(Id));
    }
    
    private void AddDomainEvent(DomainEvent @event)
    {
        _domainEvents.Add(@event);
    }
}
```

---

## 6. Runtime View

### 6.1 Scenario: Patient Books Appointment

**Actors**: Patient, Portal System, Centricity Scheduling System

**Preconditions**: Patient is authenticated and has selected a provider

**Flow**:

```
┌────────┐   ┌────────┐   ┌───────────┐   ┌────────────┐   ┌────────────┐
│Patient │   │Web App │   │API Gateway│   │Appointment │   │Centricity  │
│        │   │        │   │           │   │  Service   │   │  System    │
└───┬────┘   └───┬────┘   └─────┬─────┘   └─────┬──────┘   └─────┬──────┘
    │            │              │               │                 │
    │ 1. Select  │              │               │                 │
    │  Provider  │              │               │                 │
    │───────────>│              │               │                 │
    │            │              │               │                 │
    │            │ 2. GET       │               │                 │
    │            │ /available   │               │                 │
    │            │ -slots       │               │                 │
    │            │─────────────>│               │                 │
    │            │              │ 3. Validate   │                 │
    │            │              │    Token      │                 │
    │            │              │───────┐       │                 │
    │            │              │       │       │                 │
    │            │              │<──────┘       │                 │
    │            │              │               │                 │
    │            │              │ 4. Forward    │                 │
    │            │              │    Request    │                 │
    │            │              │──────────────>│                 │
    │            │              │               │                 │
    │            │              │               │ 5. Check Cache  │
    │            │              │               │────────┐        │
    │            │              │               │        │        │
    │            │              │               │<───────┘        │
    │            │              │               │   Cache Miss    │
    │            │              │               │                 │
    │            │              │               │ 6. SOAP Call    │
    │            │              │               │  GetSchedule()  │
    │            │              │               │────────────────>│
    │            │              │               │                 │
    │            │              │               │  7. Available   │
    │            │              │               │     Slots       │
    │            │              │               │<────────────────│
    │            │              │               │                 │
    │            │              │               │ 8. Cache Slots  │
    │            │              │               │────────┐        │
    │            │              │               │        │        │
    │            │              │               │<───────┘        │
    │            │              │               │   (5 min TTL)   │
    │            │              │               │                 │
    │            │              │ 9. Return     │                 │
    │            │              │    Slots      │                 │
    │            │              │<──────────────│                 │
    │            │              │               │                 │
    │            │ 10. Available│               │                 │
    │            │     Slots    │               │                 │
    │            │<─────────────│               │                 │
    │            │              │               │                 │
    │ 11. Display│              │               │                 │
    │    Slots   │              │               │                 │
    │<───────────│              │               │                 │
    │            │              │               │                 │
    │ 12. Select │              │               │                 │
    │     Slot   │              │               │                 │
    │───────────>│              │               │                 │
    │            │              │               │                 │
    │            │ 13. POST     │               │                 │
    │            │ /appointments│               │                 │
    │            │─────────────>│               │                 │
    │            │              │               │                 │
    │            │              │ 14. Forward   │                 │
    │            │              │──────────────>│                 │
    │            │              │               │                 │
    │            │              │               │ 15. Begin TX    │
    │            │              │               │────────┐        │
    │            │              │               │        │        │
    │            │              │               │ 16. Create      │
    │            │              │               │ Appointment     │
    │            │              │               │ (Domain Model)  │
    │            │              │               │────────┐        │
    │            │              │               │        │        │
    │            │              │               │<───────┘        │
    │            │              │               │                 │
    │            │              │               │ 17. Save to DB  │
    │            │              │               │────────┐        │
    │            │              │               │        │        │
    │            │              │               │<───────┘        │
    │            │              │               │                 │
    │            │              │               │ 18. SOAP Call   │
    │            │              │               │ CreateAppt()    │
    │            │              │               │────────────────>│
    │            │              │               │                 │
    │            │              │               │ 19. Confirmation│
    │            │              │               │<────────────────│
    │            │              │               │                 │
    │            │              │               │ 20. Publish     │
    │            │              │               │ AppointmentBooked│
    │            │              │               │ Event           │
    │            │              │               │────────┐        │
    │            │              │               │        │        │
    │            │              │               │<───────┘        │
    │            │              │               │                 │
    │            │              │               │ 21. Commit TX   │
    │            │              │               │<───────┘        │
    │            │              │               │                 │
    │            │              │ 22. Return    │                 │
    │            │              │    201        │                 │
    │            │              │<──────────────│                 │
    │            │              │               │                 │
    │            │ 23. Appt     │               │                 │
    │            │  Confirmed   │               │                 │
    │            │<─────────────│               │                 │
    │            │              │               │                 │
    │ 24. Show   │              │               │                 │
    │ Confirmation│             │               │                 │
    │<───────────│              │               │                 │
```

**Async Processing** (After step 20):

```
Service Bus receives AppointmentBookedEvent:

┌────────────────┐        ┌────────────────┐        ┌─────────────┐
│ Notification   │        │   EHR Sync     │        │  Analytics  │
│   Service      │        │   Service      │        │   Service   │
└───────┬────────┘        └───────┬────────┘        └──────┬──────┘
        │                         │                        │
        │ Consumes Event          │ Consumes Event         │ Consumes Event
        │                         │                        │
        │ Send Email              │ POST to Epic FHIR      │ Track Metric
        │ Confirmation            │ /Appointment           │ "appointment_booked"
        │                         │                        │
```

**Performance Characteristics**:

- **Response Time**: p95 = 1.8 seconds
  - Cache lookup: 50ms
  - Database write: 200ms
  - Centricity SOAP call: 1.2s (bottleneck)
  - Event publishing: 100ms
- **Throughput**: 50 bookings/minute
- **Error Rate**: 0.5% (mostly Centricity timeouts)

### 6.2 Scenario: View Medical Records (with EHR Integration)

**Flow**:

```
Patient → Web App → API Gateway → Medical Records Service → Epic EHR
                                        ↓
                                   Redis Cache
                                   (5 min TTL)
```

**Sequence**:

1. Patient clicks "Medical Records" tab
2. Web App: GET `/api/v1/medical-records?patientId={id}`
3. API Gateway: Validates JWT token, checks rate limit
4. Medical Records Service: Checks Redis cache for patient records
5. **Cache Hit** (80% of requests):
   - Return cached data (< 100ms total)
6. **Cache Miss** (20% of requests):
   - Query Epic FHIR API: `GET /Patient/{id}/Observation` (lab results)
   - Query Epic FHIR API: `GET /Patient/{id}/DocumentReference` (visit notes)
   - Query Epic FHIR API: `GET /Patient/{id}/MedicationRequest` (prescriptions)
   - Aggregate results (parallel calls via Task.WhenAll)
   - Store in Redis cache (5 min TTL)
   - Return to client (2-3 seconds total)

**Circuit Breaker Logic**:

```csharp
// Polly configuration
var circuitBreakerPolicy = Policy
    .HandleResult<HttpResponseMessage>(r => !r.IsSuccessStatusCode)
    .Or<TimeoutException>()
    .CircuitBreakerAsync(
        handledEventsAllowedBeforeBreaking: 5,
        durationOfBreak: TimeSpan.FromMinutes(1),
        onBreak: (result, duration) => {
            // Alert on-call team
            logger.LogError("Circuit breaker opened for Epic EHR");
            alertService.SendAlert("Epic EHR unavailable");
        },
        onReset: () => {
            logger.LogInformation("Circuit breaker closed for Epic EHR");
        });
```

**Fallback Strategy** (if Epic unavailable):

- Return cached data (even if stale > 5 min)
- Show banner: "Medical records may not be up-to-date. Last updated: {timestamp}"
- Log incident for follow-up

---

## 7. Deployment View

### 7.1 Infrastructure Overview

**Azure Resources** (Primary Region: East US):

```
┌──────────────────────────────────────────────────────────────┐
│                    Azure Subscription                         │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐     │
│  │         Resource Group: PatientPortal-Prod          │     │
│  │                                                      │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │      Azure Kubernetes Service (AKS)       │     │     │
│  │  │  ┌──────────────────────────────────────┐ │     │     │
│  │  │  │  Node Pool: system (3 nodes)         │ │     │     │
│  │  │  │  - VM Size: Standard_D4s_v3          │ │     │     │
│  │  │  │  - OS: Ubuntu 22.04                  │ │     │     │
│  │  │  └──────────────────────────────────────┘ │     │     │
│  │  │  ┌──────────────────────────────────────┐ │     │     │
│  │  │  │  Node Pool: apps (5 nodes)           │ │     │     │
│  │  │  │  - VM Size: Standard_D8s_v3          │ │     │     │
│  │  │  │  - Autoscale: 3-10 nodes             │ │     │     │
│  │  │  └──────────────────────────────────────┘ │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                      │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │   Azure SQL Database (PaaS)               │     │     │
│  │  │  - Tier: Business Critical                │     │     │
│  │  │  - vCores: 8                              │     │     │
│  │  │  - Storage: 1 TB                          │     │     │
│  │  │  - Zone Redundant: Yes                    │     │     │
│  │  │  - Geo-Replication: West US (secondary)   │     │     │
│  │  │                                            │     │     │
│  │  │  Databases:                                │     │     │
│  │  │  - AppointmentDB                          │     │     │
│  │  │  - MedicalRecordsDB                       │     │     │
│  │  │  - MessagingDB                            │     │     │
│  │  │  - PrescriptionDB                         │     │     │
│  │  │  - BillingDB                              │     │     │
│  │  │  - PatientDB                              │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                      │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │   Azure Cache for Redis                   │     │     │
│  │  │  - Tier: Premium P2 (6 GB)                │     │     │
│  │  │  - Zone Redundant: Yes                    │     │     │
│  │  │  - Data Persistence: RDB + AOF            │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                      │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │   Azure Service Bus (Premium)             │     │     │
│  │  │  - Namespace: patientportal-sb            │     │     │
│  │  │  - Queues:                                │     │     │
│  │  │    - appointment-events                   │     │     │
│  │  │    - notification-requests                │     │     │
│  │  │    - ehr-sync                             │     │     │
│  │  │  - Topics:                                │     │     │
│  │  │    - domain-events (with subscriptions)   │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                      │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │   Azure API Management                    │     │     │
│  │  │  - Tier: Premium                          │     │     │
│  │  │  - Gateway URL: api.patientportal.health  │     │     │
│  │  │  - Portal URL: developer.patientportal... │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                      │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │   Azure Application Insights              │     │     │
│  │  │  - Instrumentation for all services       │     │     │
│  │  │  - Distributed tracing                    │     │     │
│  │  │  - Custom metrics & dashboards            │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                      │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │   Azure Log Analytics                     │     │     │
│  │  │  - Centralized logging                    │     │     │
│  │  │  - HIPAA-compliant retention (7 years)    │     │     │
│  │  │  - KQL queries & alerts                   │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                      │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │   Azure Key Vault                         │     │     │
│  │  │  - Secrets: DB conn strings, API keys     │     │     │
│  │  │  - Certificates: TLS certs, client certs  │     │     │
│  │  │  - Soft-delete: 90 days                   │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  │                                                      │     │
│  │  ┌────────────────────────────────────────────┐     │     │
│  │  │   Azure Storage Account                   │     │     │
│  │  │  - Blob: Medical images, documents        │     │     │
│  │  │  - Encryption: Microsoft-managed keys     │     │     │
│  │  │  - Geo-redundant (GRS)                    │     │     │
│  │  └────────────────────────────────────────────┘     │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                               │
│  ┌─────────────────────────────────────────────────────┐     │
│  │   Networking                                        │     │
│  │  - Virtual Network (VNet): 10.0.0.0/16             │     │
│  │  - Subnets:                                        │     │
│  │    - AKS: 10.0.1.0/24                              │     │
│  │    - SQL: 10.0.2.0/24 (Private Endpoint)           │     │
│  │    - Redis: 10.0.3.0/24 (Private Endpoint)         │     │
│  │  - NSG: Network Security Groups per subnet         │     │
│  │  - Azure Firewall: Outbound traffic control        │     │
│  └─────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

### 7.2 Kubernetes Deployment

**Namespace Structure**:

```
- patient-portal-prod
  ├── appointment-service (3 replicas)
  ├── medical-records-service (4 replicas)
  ├── messaging-service (3 replicas)
  ├── prescription-service (2 replicas)
  ├── billing-service (2 replicas)
  ├── patient-service (3 replicas)
  └── notification-service (2 replicas)
```

**Example Deployment YAML** (Appointment Service):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: appointment-service
  namespace: patient-portal-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: appointment-service
  template:
    metadata:
      labels:
        app: appointment-service
        version: v3.0
    spec:
      containers:
      - name: appointment-service
        image: acr.azurecr.io/appointment-service:3.0.124
        ports:
        - containerPort: 8080
        env:
        - name: ASPNETCORE_ENVIRONMENT
          value: "Production"
        - name: ConnectionStrings__AppointmentDB
          valueFrom:
            secretKeyRef:
              name: db-secrets
              key: appointment-db-conn
        - name: Redis__ConnectionString
          valueFrom:
            secretKeyRef:
              name: redis-secret
              key: connection-string
        - name: APPLICATIONINSIGHTS_CONNECTION_STRING
          valueFrom:
            secretKeyRef:
              name: appinsights-secret
              key: connection-string
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8080
          initialDelaySeconds: 15
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: appointment-service
              topologyKey: topology.kubernetes.io/zone
---
apiVersion: v1
kind: Service
metadata:
  name: appointment-service
  namespace: patient-portal-prod
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
  selector:
    app: appointment-service
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: appointment-service-hpa
  namespace: patient-portal-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: appointment-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### 7.3 Disaster Recovery Setup

**Multi-Region Architecture**:

```
Primary Region (East US)              Secondary Region (West US)
┌──────────────────────┐              ┌──────────────────────┐
│ AKS Cluster (Active) │              │ AKS Cluster (Standby)│
│ - All services       │              │ - All services       │
│ - Handles 100%       │              │ - Handles 0%         │
└──────────┬───────────┘              └──────────┬───────────┘
           │                                     │
           ▼                                     ▼
┌──────────────────────┐              ┌──────────────────────┐
│ SQL (Primary)        │──Geo Repl──>│ SQL (Secondary)      │
│ - Read-Write         │ Async 30s   │ - Read-Only          │
└──────────────────────┘              └──────────────────────┘
           │                                     │
           ▼                                     ▼
┌──────────────────────┐              ┌──────────────────────┐
│ Redis (Primary)      │              │ Redis (Secondary)    │
│ - Active             │              │ - Passive Replica    │
└──────────────────────┘              └──────────────────────┘

       Azure Traffic Manager (Global Load Balancer)
                Priority Routing:
                1. East US (Priority 1)
                2. West US (Priority 2 - failover)
```

**Failover Procedure**:

1. **Detection** (Automated):
   - Azure Traffic Manager health probes detect primary region failure
   - Alert sent to on-call team via PagerDuty

2. **Decision** (Manual Approval Required):
   - On-call engineer assesses situation
   - Incident Commander approves failover
   - Estimated decision time: 15 minutes

3. **Failover** (Semi-Automated):
   - Traffic Manager routes to West US
   - SQL failover group promotes secondary to primary (5 minutes)
   - Redis promoted to active
   - AKS services in West US start handling traffic
   - Total failover time: 30 minutes

4. **Validation**:
   - Smoke tests run automatically
   - On-call verifies critical workflows
   - Communication to stakeholders

**RTO/RPO Targets**:

- **RTO** (Recovery Time Objective): 1 hour
- **RPO** (Recovery Point Objective): 5 minutes (based on SQL geo-replication lag)

**Data Loss Scenarios**:

- Transactions committed in last 5 minutes in East US may be lost
- In-flight Redis cache data lost (acceptable - non-critical data)
- Service Bus messages replicated via namespace pairing (no loss)

---

## 8. Cross-cutting Concepts

### 8.1 Security

#### Authentication & Authorization

**Patient Authentication**:

```
Flow: OAuth 2.0 Authorization Code Flow + PKCE

1. User → Web App: Click "Login"
2. Web App → Azure AD B2C: Redirect to login page
3. Azure AD B2C → User: Show username/password form
4. User → Azure AD B2C: Enter credentials
5. Azure AD B2C: Validate credentials, send MFA code (SMS/authenticator)
6. User → Azure AD B2C: Enter MFA code
7. Azure AD B2C → Web App: Return authorization code
8. Web App → Azure AD B2C: Exchange code for tokens (+ PKCE verifier)
9. Azure AD B2C → Web App: Return access token, refresh token, ID token
10. Web App: Store tokens in secure httpOnly cookie
11. Web App → API Gateway: Request with Bearer token
12. API Gateway: Validate token signature, expiry, claims
13. API Gateway → Microservices: Forward request with validated JWT
```

**Token Structure** (JWT Claims):

```json
{
  "sub": "patient-12345",
  "email": "john.doe@email.com",
  "given_name": "John",
  "family_name": "Doe",
  "tfp": "B2C_1A_signup_signin_mfa",
  "roles": ["Patient"],
  "patientId": "550e8400-e29b-41d4-a716-446655440000",
  "facilityId": "facility-001",
  "iat": 1699459200,
  "exp": 1699462800,
  "nbf": 1699459200,
  "iss": "https://healthcare.b2clogin.com/...",
  "aud": "api://patient-portal"
}
```

**Authorization Model** (Role-Based Access Control):

| Role | Permissions |
|------|-------------|
| **Patient** | View own records, book appointments, send messages, pay bills |
| **Provider** | View assigned patients, respond to messages, update clinical notes |
| **Nurse** | View assigned patients, triage messages, schedule appointments |
| **Admin** | User management, system configuration, audit logs |
| **Billing** | View all billing records, process payments, generate reports |

**Authorization Enforcement**:

```csharp
[Authorize(Roles = "Patient")]
[HttpGet("api/v1/appointments")]
public async Task<IActionResult> GetAppointments()
{
    var patientId = User.FindFirst("patientId")?.Value;
    
    // Ensure patient can only access their own appointments
    var appointments = await _appointmentService
        .GetAppointmentsForPatient(Guid.Parse(patientId));
    
    return Ok(appointments);
}

[Authorize(Roles = "Provider,Nurse")]
[HttpGet("api/v1/patients/{patientId}/records")]
public async Task<IActionResult> GetPatientRecords(Guid patientId)
{
    // Verify provider has access to this patient
    var userId = User.FindFirst("sub")?.Value;
    if (!await _authorizationService.CanAccessPatient(userId, patientId))
    {
        return Forbid();
    }
    
    var records = await _medicalRecordsService.GetRecords(patientId);
    return Ok(records);
}
```

#### Data Protection

**Encryption at Rest**:

- **SQL Database**: Transparent Data Encryption (TDE) enabled
- **Blob Storage**: Azure Storage Service Encryption (SSE) with Microsoft-managed keys
- **Backups**: Encrypted with same key as source data
- **Sensitive Fields**: Additional application-level encryption for SSN, credit cards

**Encryption in Transit**:

- **External**: TLS 1.3 only (TLS 1.2 minimum for legacy clients)
- **Internal**: TLS 1.2 between services (Azure CNI network policy)
- **Certificate Management**: Azure Key Vault with auto-renewal

**Data Masking**:

```csharp
public class Patient
{
    public Guid Id { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    
    [PersonalData]
    [DataMasking(MaskType = MaskType.SSN)]
    public string SocialSecurityNumber { get; set; }  // Stored: encrypted, Logged: XXX-XX-1234
    
    [PersonalData]
    [DataMasking(MaskType = MaskType.DateOfBirth)]
    public DateTime DateOfBirth { get; set; }  // Logged: XXXX-XX-15
    
    [PersonalData]
    public string Email { get; set; }  // Logged: j***@email.com
}
```

#### Audit Logging

**HIPAA Audit Requirements**:

- Log all PHI access (read, write, delete)
- Include user ID, timestamp, action, resource, outcome
- Retain logs for 7 years
- Tamper-proof storage

**Audit Log Entry**:

```json
{
  "timestamp": "2024-11-08T14:32:45.123Z",
  "eventType": "PHI_ACCESS",
  "userId": "provider-789",
  "userName": "Dr. Sarah Chen",
  "patientId": "patient-12345",
  "action": "VIEW_LAB_RESULTS",
  "resource": "/api/v1/medical-records/lab-results/result-456",
  "outcome": "SUCCESS",
  "ipAddress": "10.0.2.45",
  "userAgent": "Mozilla/5.0...",
  "facilityId": "facility-001",
  "correlationId": "req-abc-123"
}
```

**Audit Log Queries** (Azure Log Analytics KQL):

```kusto
// All PHI access by a specific provider in last 30 days
AuditLogs
| where timestamp > ago(30d)
| where userId == "provider-789"
| where eventType == "PHI_ACCESS"
| project timestamp, patientId, action, outcome

// Suspicious activity: Multiple failed access attempts
AuditLogs
| where timestamp > ago(1h)
| where eventType == "PHI_ACCESS"
| where outcome == "FAILURE"
| summarize FailureCount = count() by userId, patientId
| where FailureCount > 5
| order by FailureCount desc
```

### 8.2 Error Handling

**Error Response Format** (RFC 7807 Problem Details):

```json
{
  "type": "https://api.patientportal.health/problems/appointment-conflict",
  "title": "Appointment Slot No Longer Available",
  "status": 409,
  "detail": "The selected time slot was booked by another patient. Please choose a different slot.",
  "instance": "/api/v1/appointments",
  "traceId": "00-abc123-def456-01",
  "errors": {
    "ScheduledDateTime": ["The selected slot is no longer available"]
  }
}
```

**Exception Handling Strategy**:

```csharp
public class GlobalExceptionHandler : IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext, 
        Exception exception, 
        CancellationToken cancellationToken)
    {
        var problemDetails = exception switch
        {
            ValidationException validationEx => new ValidationProblemDetails
            {
                Status = 400,
                Title = "Validation Error",
                Detail = validationEx.Message,
                Errors = validationEx.Errors.ToDictionary()
            },
            
            NotFoundException notFoundEx => new ProblemDetails
            {
                Status = 404,
                Title = "Resource Not Found",
                Detail = notFoundEx.Message
            },
            
            UnauthorizedAccessException unauthorizedEx => new ProblemDetails
            {
                Status = 403,
                Title = "Access Denied",
                Detail = "You do not have permission to access this resource"
            },
            
            ExternalServiceException externalEx => new ProblemDetails
            {
                Status = 503,
                Title = "External Service Unavailable",
                Detail = "We're experiencing issues connecting to an external system. Please try again later.",
                Extensions = { ["retryAfter"] = "60" }
            },
            
            _ => new ProblemDetails
            {
                Status = 500,
                Title = "Internal Server Error",
                Detail = "An unexpected error occurred. Our team has been notified."
            }
        };
        
        // Add trace ID for correlation
        problemDetails.Extensions["traceId"] = Activity.Current?.TraceId.ToString();
        
        // Log exception (PHI-safe logging - no sensitive data)
        _logger.LogError(exception, 
            "Exception occurred: {ExceptionType}", 
            exception.GetType().Name);
        
        // Return problem details
        httpContext.Response.StatusCode = problemDetails.Status ?? 500;
        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);
        
        return true;
    }
}
```

**Retry Policies** (Polly):

```csharp
// Retry policy for transient errors
var retryPolicy = Policy
    .Handle<HttpRequestException>()
    .Or<TimeoutException>()
    .WaitAndRetryAsync(
        retryCount: 3,
        sleepDurationProvider: retryAttempt => 
            TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
        onRetry: (exception, timeSpan, retryCount, context) =>
        {
            _logger.LogWarning(
                "Retry {RetryCount} after {Delay}s due to {Exception}",
                retryCount, timeSpan.TotalSeconds, exception.GetType().Name);
        });

// Circuit breaker for Epic EHR
var circuitBreaker = Policy
    .Handle<HttpRequestException>()
    .CircuitBreakerAsync(
        exceptionsAllowedBeforeBreaking: 5,
        durationOfBreak: TimeSpan.FromMinutes(1),
        onBreak: (exception, duration) =>
        {
            _logger.LogError("Circuit breaker opened for Epic EHR");
            _alertService.SendAlert(AlertLevel.Critical, "Epic EHR unavailable");
        },
        onReset: () =>
        {
            _logger.LogInformation("Circuit breaker closed for Epic EHR");
        });

// Combined policy
var combinedPolicy = Policy.WrapAsync(retryPolicy, circuitBreaker);
```

### 8.3 Logging & Observability

**Structured Logging** (Serilog):

```csharp
public class AppointmentService
{
    private readonly ILogger<AppointmentService> _logger;
    
    public async Task<Appointment> BookAppointment(BookAppointmentRequest request)
    {
        using var _ = _logger.BeginScope(new Dictionary<string, object>
        {
            ["PatientId"] = request.PatientId,
            ["ProviderId"] = request.ProviderId,
            ["ScheduledDateTime"] = request.ScheduledDateTime
        });
        
        _logger.LogInformation(
            "Booking appointment for patient {PatientId} with provider {ProviderId}",
            request.PatientId, request.ProviderId);
        
        try
        {
            var appointment = await _repository.CreateAsync(request);
            
            _logger.LogInformation(
                "Appointment {AppointmentId} booked successfully",
                appointment.Id);
            
            return appointment;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed to book appointment for patient {PatientId}",
                request.PatientId);
            throw;
        }
    }
}
```

**Log Output** (JSON format for Azure Log Analytics):

```json
{
  "timestamp": "2024-11-08T14:32:45.123Z",
  "level": "Information",
  "messageTemplate": "Appointment {AppointmentId} booked successfully",
  "message": "Appointment 550e8400-e29b-41d4-a716-446655440000 booked successfully",
  "properties": {
    "AppointmentId": "550e8400-e29b-41d4-a716-446655440000",
    "PatientId": "patient-12345",
    "ProviderId": "provider-789",
    "ScheduledDateTime": "2024-11-15T10:00:00Z",
    "SourceContext": "AppointmentService",
    "MachineName": "aks-node-01",
    "ProcessId": 12345,
    "ThreadId": 42
  },
  "traceId": "00-abc123-def456-01",
  "spanId": "def456"
}
```

**Distributed Tracing** (Application Insights):

```csharp
// Automatic instrumentation via Application Insights SDK
// Manual span creation for custom operations

public async Task<MedicalRecords> GetRecords(Guid patientId)
{
    using var activity = _activitySource.StartActivity("GetMedicalRecords");
    activity?.SetTag("patientId", patientId);
    
    // Check cache
    using (var cacheActivity = _activitySource.StartActivity("CheckCache"))
    {
        var cached = await _cache.GetAsync<MedicalRecords>(patientId.ToString());
        if (cached != null)
        {
            cacheActivity?.SetTag("cache.hit", true);
            return cached;
        }
        cacheActivity?.SetTag("cache.hit", false);
    }
    
    // Fetch from Epic EHR
    using (var ehrActivity = _activitySource.StartActivity("FetchFromEpicEHR"))
    {
        ehrActivity?.SetTag("ehr.system", "Epic");
        var records = await _epicClient.GetPatientRecords(patientId);
        ehrActivity?.SetTag("ehr.record_count", records.Count);
        
        // Cache for 5 minutes
        await _cache.SetAsync(patientId.ToString(), records, TimeSpan.FromMinutes(5));
        
        return records;
    }
}
```

**Metrics** (Prometheus-style, exposed via Application Insights):

```csharp
public class AppointmentMetrics
{
    private readonly Counter _appointmentsBookedCounter;
    private readonly Histogram _bookingDurationHistogram;
    private readonly Gauge _activeAppointmentsGauge;
    
    public AppointmentMetrics(IMeterFactory meterFactory)
    {
        var meter = meterFactory.Create("AppointmentService");
        
        _appointmentsBookedCounter = meter.CreateCounter<long>(
            "appointments_booked_total",
            description: "Total number of appointments booked");
        
        _bookingDurationHistogram = meter.CreateHistogram<double>(
            "appointment_booking_duration_seconds",
            unit: "s",
            description: "Duration of appointment booking operation");
        
        _activeAppointmentsGauge = meter.CreateObservableGauge<int>(
            "active_appointments_count",
            observeValue: () => GetActiveAppointmentsCount(),
            description: "Current number of active appointments");
    }
    
    public void RecordAppointmentBooked(string appointmentType)
    {
        _appointmentsBookedCounter.Add(1, 
            new KeyValuePair<string, object>("type", appointmentType));
    }
    
    public void RecordBookingDuration(double durationSeconds, bool success)
    {
        _bookingDurationHistogram.Record(durationSeconds,
            new KeyValuePair<string, object>("success", success));
    }
}
```

**Dashboards** (Azure Monitor):

- **Service Health Dashboard**: Error rate, latency (p50/p95/p99), throughput per service
- **Infrastructure Dashboard**: CPU, memory, disk, network per node
- **Business Metrics Dashboard**: Appointments booked/hour, patients registered/day, revenue
- **External Dependencies**: Epic EHR response time, Centricity availability, Stripe transaction success rate

**Alerting Rules**:

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| High Error Rate | Error rate > 5% for 5 min | Critical | Page on-call |
| Slow Response Time | p95 > 5s for 10 min | High | Slack + Email |
| Epic EHR Down | Circuit breaker open | Critical | Page on-call |
| Database CPU High | CPU > 80% for 15 min | High | Email DBA team |
| Low Appointment Slots | Available slots < 100 | Medium | Email operations |

### 8.4 Data Consistency

**Consistency Strategies per Bounded Context**:

| Context | Strategy | Rationale |
|---------|----------|-----------|
| **Appointments** | Strong Consistency | Critical for preventing double-booking |
| **Medical Records** | Eventual Consistency (5 min) | Historical data, acceptable delay |
| **Messaging** | Strong Consistency | Messages must not be lost or duplicated |
| **Billing** | Strong Consistency | Financial data requires accuracy |
| **Notifications** | Eventual Consistency | Non-critical, can tolerate delay |

**Saga Pattern Example** (Appointment Cancellation):

```csharp
public class AppointmentCancellationSaga
{
    private readonly IAppointmentRepository _appointmentRepo;
    private readonly ICentricityClient _centricityClient;
    private readonly IServiceBusPublisher _publisher;
    private readonly ILogger<AppointmentCancellationSaga> _logger;
    
    public async Task<SagaResult> CancelAppointment(Guid appointmentId, string reason)
    {
        var saga = new Saga(appointmentId);
        
        try
        {
            // Step 1: Mark appointment as cancelling
            await _appointmentRepo.UpdateStatus(appointmentId, AppointmentStatus.Cancelling);
            saga.RecordStep("MarkCancelling", StepStatus.Completed);
            
            // Step 2: Cancel in Centricity scheduling system
            try
            {
                await _centricityClient.CancelAppointment(appointmentId);
                saga.RecordStep("CancelInCentricity", StepStatus.Completed);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to cancel in Centricity");
                saga.RecordStep("CancelInCentricity", StepStatus.Failed);
                
                // Compensate: Revert appointment status
                await _appointmentRepo.UpdateStatus(appointmentId, AppointmentStatus.Scheduled);
                saga.RecordStep("RevertStatus", StepStatus.Completed);
                
                return SagaResult.Failure("Failed to cancel in scheduling system");
            }
            
            // Step 3: Update appointment to cancelled
            await _appointmentRepo.UpdateStatus(appointmentId, AppointmentStatus.Cancelled, reason);
            saga.RecordStep("MarkCancelled", StepStatus.Completed);
            
            // Step 4: Publish event for notifications
            await _publisher.PublishAsync(new AppointmentCancelledEvent
            {
                AppointmentId = appointmentId,
                CancellationReason = reason,
                CancelledAt = DateTime.UtcNow
            });
            saga.RecordStep("PublishEvent", StepStatus.Completed);
            
            await _sagaRepository.SaveAsync(saga);
            return SagaResult.Success();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Saga failed for appointment {AppointmentId}", appointmentId);
            await _sagaRepository.SaveAsync(saga);
            throw;
        }
    }
}
```

**Idempotency Implementation**:

```csharp
public class IdempotentAppointmentService
{
    private readonly IDistributedCache _cache;
    private readonly IAppointmentService _appointmentService;
    
    public async Task<Appointment> BookAppointment(BookAppointmentRequest request)
    {
        var idempotencyKey = request.IdempotencyKey;
        var cacheKey = $"appointment:idempotency:{idempotencyKey}";
        
        // Check if already processed
        var cached = await _cache.GetStringAsync(cacheKey);
        if (cached != null)
        {
            return JsonSerializer.Deserialize<Appointment>(cached);
        }
        
        // Process request
        var appointment = await _appointmentService.BookAppointment(request);
        
        // Cache result for 24 hours
        await _cache.SetStringAsync(
            cacheKey, 
            JsonSerializer.Serialize(appointment),
            new DistributedCacheEntryOptions 
            { 
                AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(24) 
            });
        
        return appointment;
    }
}
```

### 8.5 Testing Strategy

**Test Pyramid**:

```
        /\
       /  \  E2E Tests (5%)
      /────\  - Critical user journeys
     /      \  - Full system integration
    /────────\  Integration Tests (25%)
   /          \ - API tests with real DB
  /────────────\ - Service integration tests
 /              \ Unit Tests (70%)
/────────────────\ - Domain logic
                   - Business rules
                   - Service layer
```

**Unit Test Example**:

```csharp
public class AppointmentTests
{
    [Fact]
    public void Schedule_WithValidData_CreatesAppointment()
    {
        // Arrange
        var patientId = Guid.NewGuid();
        var providerId = Guid.NewGuid();
        var scheduledTime = DateTime.UtcNow.AddDays(7).AddHours(10); // 7 days from now, 10 AM
        
        // Act
        var appointment = Appointment.Schedule(
            patientId, 
            providerId, 
            scheduledTime, 
            AppointmentType.OfficeVisit);
        
        // Assert
        Assert.NotNull(appointment);
        Assert.Equal(AppointmentStatus.Scheduled, appointment.Status);
        Assert.Single(appointment.DomainEvents);
        Assert.IsType<AppointmentScheduledEvent>(appointment.DomainEvents[0]);
    }
    
    [Fact]
    public void Schedule_WithPastDateTime_ThrowsException()
    {
        // Arrange
        var patientId = Guid.NewGuid();
        var providerId = Guid.NewGuid();
        var pastTime = DateTime.UtcNow.AddDays(-1);
        
        // Act & Assert
        var exception = Assert.Throws<InvalidOperationException>(() =>
            Appointment.Schedule(patientId, providerId, pastTime, AppointmentType.OfficeVisit));
        
        Assert.Equal("Cannot book past appointments", exception.Message);
    }
    
    [Fact]
    public void Cancel_WhenScheduled_UpdatesStatusAndPublishesEvent()
    {
        // Arrange
        var appointment = Appointment.Schedule(
            Guid.NewGuid(), 
            Guid.NewGuid(), 
            DateTime.UtcNow.AddDays(7), 
            AppointmentType.OfficeVisit);
        appointment.DomainEvents.Clear(); // Clear scheduled event
        
        // Act
        appointment.Cancel("Patient requested cancellation");
        
        // Assert
        Assert.Equal(AppointmentStatus.Cancelled, appointment.Status);
        Assert.Equal("Patient requested cancellation", appointment.CancellationReason);
        Assert.Single(appointment.DomainEvents);
        Assert.IsType<AppointmentCancelledEvent>(appointment.DomainEvents[0]);
    }
}
```

**Integration Test Example** (with Testcontainers):

```csharp
public class AppointmentServiceIntegrationTests : IAsyncLifetime
{
    private readonly IContainer _sqlContainer;
    private readonly IContainer _redisContainer;
    private AppointmentService _sut;
    
    public AppointmentServiceIntegrationTests()
    {
        _sqlContainer = new MsSqlBuilder()
            .WithImage("mcr.microsoft.com/mssql/server:2022-latest")
            .Build();
        
        _redisContainer = new RedisBuilder()
            .WithImage("redis:7-alpine")
            .Build();
    }
    
    public async Task InitializeAsync()
    {
        await _sqlContainer.StartAsync();
        await _redisContainer.StartAsync();
        
        // Setup test data
        var connectionString = _sqlContainer.GetConnectionString();
        await SeedDatabase(connectionString);
        
        // Initialize SUT
        _sut = new AppointmentService(
            new AppointmentRepository(connectionString),
            new RedisCacheService(_redisContainer.GetConnectionString()),
            new Mock<ICentricityClient>().Object);
    }
    
    [Fact]
    public async Task BookAppointment_WithAvailableSlot_PersistsToDatabase()
    {
        // Arrange
        var request = new BookAppointmentRequest
        {
            PatientId = Guid.NewGuid(),
            ProviderId = Guid.Parse("provider-123"),
            ScheduledDateTime = DateTime.UtcNow.AddDays(7),
            Type = AppointmentType.OfficeVisit
        };
        
        // Act
        var appointment = await _sut.BookAppointment(request);
        
        // Assert
        Assert.NotNull(appointment);
        
        // Verify persisted
        var retrieved = await _sut.GetAppointment(appointment.Id);
        Assert.Equal(appointment.Id, retrieved.Id);
        Assert.Equal(AppointmentStatus.Scheduled, retrieved.Status);
    }
    
    public async Task DisposeAsync()
    {
        await _sqlContainer.DisposeAsync();
        await _redisContainer.DisposeAsync();
    }
}
```

**E2E Test Example** (Playwright):

```csharp
[TestFixture]
public class AppointmentBookingE2ETests
{
    private IPlaywright _playwright;
    private IBrowser _browser;
    
    [SetUp]
    public async Task Setup()
    {
        _playwright = await Playwright.CreateAsync();
        _browser = await _playwright.Chromium.LaunchAsync(new() 
        { 
            Headless = true 
        });
    }
    
    [Test]
    public async Task Patient_CanBookAppointment_EndToEnd()
    {
        // Arrange
        var page = await _browser.NewPageAsync();
        await page.GotoAsync("https://staging.patientportal.health");
        
        // Act - Login
        await page.ClickAsync("text=Login");
        await page.FillAsync("input[name='email']", "testpatient@example.com");
        await page.FillAsync("input[name='password']", "Test@1234");
        await page.ClickAsync("button[type='submit']");
        
        // Wait for MFA code (in test env, use test MFA code)
        await page.FillAsync("input[name='mfaCode']", "123456");
        await page.ClickAsync("button:text('Verify')");
        
        // Navigate to appointments
        await page.ClickAsync("text=Appointments");
        await page.ClickAsync("text=Book New Appointment");
        
        // Select provider
        await page.SelectOptionAsync("select[name='provider']", "Dr. Sarah Chen");
        
        // Select date
        await page.ClickAsync("input[name='date']");
        var nextWeek = DateTime.Now.AddDays(7).ToString("MM/dd/yyyy");
        await page.FillAsync("input[name='date']", nextWeek);
        
        // Select time slot
        await page.ClickAsync("button:text('10:00 AM')");
        
        // Confirm booking
        await page.ClickAsync("button:text('Confirm Appointment')");
        
        // Assert - Confirmation shown
        await Expect(page.Locator("text=Appointment Confirmed")).ToBeVisibleAsync();
        await Expect(page.Locator("text=Dr. Sarah Chen")).ToBeVisibleAsync();
        await Expect(page.Locator($"text={nextWeek}")).ToBeVisibleAsync();
    }
    
    [TearDown]
    public async Task Teardown()
    {
        await _browser.CloseAsync();
        _playwright.Dispose();
    }
}
```

---

## 9. Architecture Decisions

### ADR-001: Microservices Architecture

**Status**: Accepted  
**Date**: 2023-06-15  
**Deciders**: Architecture Team, CTO

**Context**:
Need to support 500K patients with 9-month delivery timeline and 15-person team distributed across 3 locations.

**Decision**:
Adopt microservices architecture with services aligned to bounded contexts (Appointments, Medical Records, Messaging, etc.).

**Rationale**:

- Independent deployment enables parallel team work
- Services can scale independently based on load
- Failure isolation prevents cascading failures
- Technology diversity possible (though we'll standardize on .NET initially)
- Aligns with Conway's Law (team structure)

**Consequences**:

- ✅ Teams can work independently
- ✅ Can deploy individual services without full system deployment
- ❌ Increased operational complexity (monitoring 6+ services)
- ❌ Distributed system challenges (eventual consistency, network latency)
- ❌ Need service mesh or API gateway

**Alternatives Considered**:

- **Modular Monolith**: Simpler but single deployment unit limits team independence
- **Serverless**: Considered but cold start latency unacceptable for healthcare

---

### ADR-002: Azure as Cloud Provider

**Status**: Accepted  
**Date**: 2023-06-20  
**Deciders**: CTO, Infrastructure Team

**Context**:
Need HIPAA-compliant cloud infrastructure with strong healthcare integrations.

**Decision**:
Use Microsoft Azure as exclusive cloud provider.

**Rationale**:

- Existing enterprise agreement with Microsoft (cost savings)
- Azure Health Data Services for HL7 FHIR support
- Strong compliance certifications (HIPAA, HITRUST)
- Integration with Epic EHR (Epic on Azure program)
- Team familiarity with Azure AD

**Consequences**:

- ✅ Leverage existing Azure expertise
- ✅ Integrated FHIR services
- ✅ Cost savings via EA
- ❌ Vendor lock-in to Azure
- ❌ Must use Azure-specific services (limits portability)

**Alternatives Considered**:

- **AWS**: More mature but no existing EA, less healthcare focus
- **GCP**: Strong healthcare AI but smallest market share, least team familiarity

---

### ADR-003: HL7 FHIR R4 for EHR Integration

**Status**: Accepted  
**Date**: 2023-07-01  
**Deciders**: Integration Architect, Clinical Informatics

**Context**:
Must integrate with Epic EHR for medical records access per 21st Century Cures Act.

**Decision**:
Use HL7 FHIR R4 standard for all EHR integrations.

**Rationale**:

- Federal mandate (21st Century Cures Act)# Architecture Documentation - Healthcare Patient Portal

**arc42 Template Version 8.1**

## Document Information

**System Name**: Healthcare Patient Portal  
**Version**: 3.0  
**Date**: 2024-11-08  
**Status**: Approved  
**Classification**: Confidential - HIPAA Protected

**Authors**:

- Lead Architect: Sarah Chen (<sarah.chen@healthcare.com>)
- Security Architect: Michael Rodriguez (<michael.rodriguez@healthcare.com>)
- Solutions Architect: David Kim (<david.kim@healthcare.com>)

---

## Table of Contents

1. [Introduction and Goals](#1-introduction-and-goals)
2. [Architecture Constraints](#2-architecture-constraints)
3. [System Scope and Context](#3-system-scope-and-context)
4. [Solution Strategy](#4-solution-strategy)
5. [Building Block View](#5-building-block-view)
6. [Runtime View](#6-runtime-view)
7. [Deployment View](#7-deployment-view)
8. [Cross-cutting Concepts](#8-cross-cutting-concepts)
9. [Architecture Decisions](#9-architecture-decisions)
10. [Quality Requirements](#10-quality-requirements)
11. [Risks and Technical Debt](#11-risks-and-technical-debt)
12. [Glossary](#12-glossary)

---

## 1. Introduction and Goals

### 1.1 Requirements Overview

#### Business Context

The Healthcare Patient Portal is a comprehensive digital platform enabling patients to access their medical records, schedule appointments, communicate with healthcare providers, manage prescriptions, and view billing information. The system serves 500,000 active patients across 50 medical facilities.

#### Key Business Drivers

1. **Patient Engagement**: Increase patient engagement from 45% to 75% within 2 years
2. **Operational Efficiency**: Reduce administrative workload by 30% through self-service
3. **Care Quality**: Improve medication adherence by 25% through reminders and tracking
4. **Regulatory Compliance**: Maintain HIPAA, HITECH, and state healthcare regulations compliance
5. **Revenue Protection**: Ensure 99.9% uptime for appointment booking (revenue-critical)

#### Essential Features

**Patient Self-Service**:

- View complete medical history (lab results, imaging, visit notes)
- Schedule, reschedule, and cancel appointments online
- Request prescription refills and view medication history
- Secure messaging with healthcare providers
- Pay bills online and view insurance claims

**Clinical Integration**:

- Bi-directional sync with Electronic Health Record (EHR) system
- Real-time appointment availability from scheduling system
- Integration with pharmacy systems for e-prescribing
- Lab results auto-published when ready

**Administrative Functions**:

- Patient registration and demographic updates
- Insurance information management
- Consent and form management
- Appointment reminders via email/SMS

### 1.2 Quality Goals

| Priority | Quality Goal | Scenario | Target Metric |
|----------|-------------|----------|---------------|
| 1 | **Security & Privacy** | Patient PHI protected from unauthorized access | Zero data breaches, 100% HIPAA compliance |
| 2 | **Availability** | System available for appointment booking 24/7 | 99.9% uptime (< 45 min/month downtime) |
| 3 | **Performance** | Fast response times for critical workflows | p95 < 2 seconds for appointment search |
| 4 | **Usability** | Accessible to elderly and disabled patients | WCAG 2.1 AA compliance, < 5 support calls/1000 users |
| 5 | **Interoperability** | Seamless integration with EHR systems | HL7 FHIR R4 compliant, < 5 min sync delay |
| 6 | **Maintainability** | Easy to add new features without regression | Deploy weekly, < 0.1% defect rate |

### 1.3 Stakeholders

| Role | Expectations | Contact |
|------|--------------|---------|
| **Patients** | Easy access to health info, schedule appointments, secure communication | <patients@feedback.com> |
| **Physicians** | Reduce admin burden, secure messaging, view patient-entered data | <medical.staff@healthcare.com> |
| **Nurses** | Manage appointments, triage messages, update patient records | <nursing.staff@healthcare.com> |
| **Billing Department** | Online payment processing, reduced phone inquiries | <billing@healthcare.com> |
| **IT Operations** | Reliable system, easy monitoring, quick incident resolution | <it.ops@healthcare.com> |
| **CISO** | HIPAA compliance, data security, audit trails | <security@healthcare.com> |
| **Legal/Compliance** | Regulatory compliance, patient consent management | <legal@healthcare.com> |
| **Executive Leadership** | ROI, patient satisfaction scores, market differentiation | <executive@healthcare.com> |

---

## 2. Architecture Constraints

### 2.1 Technical Constraints

| Constraint | Description | Rationale |
|------------|-------------|-----------|
| **TC-1: FHIR R4 Compliance** | All clinical data exchange must use HL7 FHIR R4 standard | Federal regulation (21st Century Cures Act) |
| **TC-2: EHR Integration** | Must integrate with Epic EHR system via APIs | Epic is existing EHR across all facilities |
| **TC-3: Azure Cloud Only** | Must run on Microsoft Azure (no AWS/GCP) | Enterprise agreement and existing Azure investment |
| **TC-4: .NET Technology Stack** | Backend must use .NET 8 and C# | IT department standardization |
| **TC-5: SQL Server Database** | Primary database must be SQL Server | Existing DBA expertise and license agreements |
| **TC-6: Active Directory** | Use Azure AD for authentication | Enterprise SSO requirement |
| **TC-7: Two-Factor Authentication** | MFA required for all user logins | HIPAA security requirements |

### 2.2 Organizational Constraints

| Constraint | Description | Impact |
|------------|-------------|--------|
| **OC-1: Team Size** | 15 developers, 3 QA, 2 DevOps, 1 UX designer | Limits architectural complexity |
| **OC-2: Budget** | $3M development, $500K/year operations | Rules out expensive commercial products |
| **OC-3: Timeline** | Must launch MVP in 9 months | Requires phased delivery approach |
| **OC-4: Distributed Team** | Team across 3 locations (Seattle, Chicago, Bangalore) | Requires clear contracts, async communication |
| **OC-5: On-Call Support** | 24/7 support required with 15-minute response for P1 | Needs robust monitoring and alerting |
| **OC-6: HIPAA Training** | All team members must complete annual HIPAA training | Mandatory compliance requirement |

### 2.3 Legal and Regulatory Constraints

| Constraint | Description | Implementation |
|------------|-------------|----------------|
| **LC-1: HIPAA Privacy Rule** | Protect patient PHI from unauthorized disclosure | Role-based access, encryption, audit logs |
| **LC-2: HIPAA Security Rule** | Technical safeguards for ePHI | Encryption at rest/transit, access controls, risk analysis |
| **LC-3: HITECH Act** | Breach notification within 60 days | Automated breach detection and notification system |
| **LC-4: 21st Century Cures Act** | Patients must access records within 24 hours | Real-time sync with EHR, no blocking |
| **LC-5: State Regulations** | Comply with 50 state healthcare regulations | Legal review for each state, configurable consent workflows |
| **LC-6: ADA Compliance** | Website accessible to disabled users | WCAG 2.1 AA compliance, screen reader support |
| **LC-7: PCI DSS** | Protect payment card data | Tokenization, no card storage, annual audit |

### 2.4 Conventions

**Documentation Standards**:

- Architecture decisions recorded in ADR format (Michael Nygard template)
- C4 model for architecture diagrams (Context, Container, Component)
- OpenAPI 3.0 for REST API specifications
- All documentation in Markdown, version controlled in Git

**Coding Standards**:

- C# coding conventions per Microsoft guidelines
- Code reviews required for all changes (2 approvers)
- 80% unit test coverage minimum
- SonarQube quality gates enforced in CI/CD

**Naming Conventions**:

- REST endpoints: `/api/v{version}/{resource}` (e.g., `/api/v1/appointments`)
- Database tables: PascalCase (e.g., `Appointments`, `Patients`)
- Microservices: `{domain}-service` (e.g., `appointment-service`)

---

## 3. System Scope and Context

### 3.1 Business Context

```
                    ┌─────────────────────────────────────┐
                    │   Healthcare Patient Portal         │
                    │                                     │
                    │  - Medical Records Access           │
   ┌────────────┐   │  - Appointment Scheduling          │
   │  Patients  │◄──┤  - Secure Messaging                │
   │            │   │  - Prescription Refills            │
   └────────────┘   │  - Bill Payment                    │
                    └──────┬──────┬──────┬──────┬────────┘
                           │      │      │      │
          ┌────────────────┘      │      │      └─────────────┐
          │                       │      │                    │
          ▼                       ▼      ▼                    ▼
   ┌────────────┐        ┌─────────────────┐       ┌──────────────┐
   │   Epic     │        │   Scheduling    │       │   Pharmacy   │
   │    EHR     │        │     System      │       │    System    │
   │            │        │   (Centricity)  │       │   (Surescripts)│
   └────────────┘        └─────────────────┘       └──────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │    Billing      │
                        │    System       │
                        │   (Cerner)      │
                        └─────────────────┘
```

#### External Entities

**Patients** (Primary Users)

- **Interaction**: Web browser, iOS/Android apps
- **Data Provided**: Demographics, appointment requests, messages, payment info
- **Data Received**: Medical records, lab results, appointments, bills, messages
- **Frequency**: 200K daily active users, 500K monthly active users

**Healthcare Providers** (Secondary Users)

- **Interaction**: Same portal, provider view
- **Data Provided**: Clinical notes, responses to messages
- **Data Received**: Patient messages, appointment schedules
- **Frequency**: 5,000 providers, 50% daily usage

**Epic EHR System** (Critical Integration)

- **Interaction**: HL7 FHIR R4 REST APIs
- **Data Provided**: Patient demographics, medical history, lab results, visit notes
- **Data Received**: Patient-entered data (symptoms, medications), appointment confirmations
- **Frequency**: Real-time sync, 10K API calls/hour

**Scheduling System (Centricity)** (Critical Integration)

- **Interaction**: SOAP Web Services
- **Data Provided**: Provider schedules, appointment slots, appointment status
- **Data Received**: New appointments, cancellations, reschedules
- **Frequency**: Real-time, 2K appointments/day

**Pharmacy System (Surescripts)** (Important Integration)

- **Interaction**: NCPDP SCRIPT standard via REST API
- **Data Provided**: Medication history, fill status
- **Data Received**: Refill requests, new prescriptions (via provider)
- **Frequency**: 500 requests/day

**Billing System (Cerner)** (Important Integration)

- **Interaction**: HL7 v2 messages via Integration Engine
- **Data Provided**: Patient statements, insurance claims, payment status
- **Data Received**: Online payments
- **Frequency**: 1K payments/day, 5K statement views/day

**Payment Gateway (Stripe)** (Critical for Revenue)

- **Interaction**: REST API
- **Data Provided**: Payment status, transaction IDs
- **Data Received**: Payment details (tokenized)
- **Frequency**: 1K payments/day

**Notification Services**

- **Twilio** (SMS): Appointment reminders, 2FA codes - 10K SMS/day
- **SendGrid** (Email): Notifications, appointment confirmations - 50K emails/day

### 3.2 Technical Context

```
┌──────────────────────────────────────────────────────────────┐
│                      Patient Portal System                    │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐         │
│  │   Web App   │  │  iOS App    │  │ Android App  │         │
│  │  (React)    │  │  (Swift)    │  │  (Kotlin)    │         │
│  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘         │
│         │                │                 │                 │
│         └────────────────┴─────────────────┘                 │
│                          │                                   │
│                          ▼                                   │
│              ┌───────────────────────┐                       │
│              │    API Gateway        │                       │
│              │ (Azure API Management)│                       │
│              └───────────┬───────────┘                       │
│                          │                                   │
│         ┌────────────────┼────────────────┐                 │
│         │                │                │                 │
│         ▼                ▼                ▼                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Appointment │  │  Medical    │  │  Messaging  │         │
│  │  Service    │  │   Records   │  │  Service    │         │
│  │ (ASP.NET)   │  │  Service    │  │ (ASP.NET)   │         │
│  └─────┬───────┘  └─────┬───────┘  └─────┬───────┘         │
│        │                │                 │                 │
└────────┼────────────────┼─────────────────┼─────────────────┘
         │                │                 │
         ▼                ▼                 ▼
┌──────────────────────────────────────────────────────────────┐
│                    External Systems                           │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐         │
│  │   Epic EHR  │  │ Centricity  │  │  Surescripts │         │
│  │   (FHIR)    │  │   (SOAP)    │  │    (REST)    │         │
│  └─────────────┘  └─────────────┘  └──────────────┘         │
│                                                               │
│  Protocol: HTTPS/REST               Protocol: SOAP/WS        │
│  Format: JSON (FHIR R4)             Format: XML              │
│  Auth: OAuth 2.0 + Client Cert     Auth: SAML 2.0           │
└──────────────────────────────────────────────────────────────┘
```

#### Technical Interfaces

**TI-1: Patient Web/Mobile → API Gateway**

- **Protocol**: HTTPS/REST
- **Format**: JSON
- **Authentication**: OAuth 2.0 (Authorization Code Flow) + Azure AD
- **Security**: TLS 1.3, rate limiting (100 req/min per user), CSRF tokens
- **Error Handling**: RFC 7807 Problem Details format

**TI-2: API Gateway → Microservices**

- **Protocol**: HTTP/2
- **Format**: JSON
- **Authentication**: JWT tokens (validated by each service)
- **Service Discovery**: Azure Service Discovery
- **Load Balancing**: Azure Application Gateway

**TI-3: Microservices → Epic EHR**

- **Protocol**: HTTPS/REST
- **Format**: JSON (HL7 FHIR R4)
- **Authentication**: OAuth 2.0 + Mutual TLS (client certificates)
- **Rate Limit**: 1000 req/hour per facility
- **Retry Policy**: Exponential backoff, max 3 retries
- **Circuit Breaker**: Open after 5 consecutive failures
- **Resources Used**:
  - `Patient`: Demographics, identifiers
  - `Observation`: Lab results, vitals
  - `MedicationRequest`: Prescriptions
  - `Appointment`: Scheduled visits
  - `DocumentReference`: Clinical notes

**TI-4: Microservices → Centricity Scheduling**

- **Protocol**: HTTPS/SOAP 1.2
- **Format**: XML
- **Authentication**: SAML 2.0 bearer tokens
- **Timeout**: 30 seconds
- **Operations Used**:
  - `GetProviderSchedule`: Fetch available slots
  - `CreateAppointment`: Book appointment
  - `CancelAppointment`: Cancel existing appointment
  - `GetAppointmentDetails`: Fetch appointment info

**TI-5: Microservices → Surescripts Pharmacy**

- **Protocol**: HTTPS/REST
- **Format**: XML (NCPDP SCRIPT 2017071)
- **Authentication**: API Key + IP whitelisting
- **Encryption**: Message-level encryption for PHI
- **Operations**:
  - `MedicationHistory`: Fetch patient med history
  - `RefillRequest`: Submit refill request

**TI-6: Microservices → Stripe Payment**

- **Protocol**: HTTPS/REST
- **Format**: JSON
- **Authentication**: Bearer token (secret key)
- **PCI Compliance**: Tokenization (no card storage)
- **Webhook**: Payment status updates via webhook

---

## 4. Solution Strategy

### 4.1 Technology Decisions

| Decision | Technology | Rationale |
|----------|-----------|-----------|
| **Architecture Style** | Microservices | Independent deployment, scalability per service, team autonomy |
| **Backend Framework** | ASP.NET Core 8 | Enterprise constraint, async/await, cross-platform, high performance |
| **Frontend Framework** | React 18 with TypeScript | Component reusability, strong typing, large ecosystem |
| **Mobile Apps** | Native (Swift/Kotlin) | Best UX, access native APIs (biometrics, notifications) |
| **API Gateway** | Azure API Management | Rate limiting, OAuth integration, Azure native |
| **Database** | Azure SQL Database | Enterprise constraint, ACID transactions, JSON support |
| **Caching** | Azure Redis Cache | Reduce EHR API calls, improve response times |
| **Message Queue** | Azure Service Bus | Async processing, guaranteed delivery, dead-letter queues |
| **Identity** | Azure AD B2C | Patient self-registration, MFA, SSO with providers |
| **Monitoring** | Azure Application Insights | Azure native, distributed tracing, alerting |
| **Logging** | Azure Log Analytics | Centralized logging, KQL queries, HIPAA-compliant retention |

### 4.2 Top-Level Decomposition

**Domain-Driven Design Approach**: System decomposed into bounded contexts aligned with business capabilities.

```
┌─────────────────────────────────────────────────────────────┐
│                  Healthcare Patient Portal                   │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Appointment  │  │   Medical    │  │   Messaging  │      │
│  │   Context    │  │   Records    │  │   Context    │      │
│  │              │  │   Context    │  │              │      │
│  │ - Booking    │  │ - Lab Results│  │ - Inbox      │      │
│  │ - Scheduling │  │ - Visit Notes│  │ - Compose    │      │
│  │ - Reminders  │  │ - Imaging    │  │ - Threads    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Prescription │  │   Billing    │  │   Patient    │      │
│  │   Context    │  │   Context    │  │   Context    │      │
│  │              │  │              │  │              │      │
│  │ - Medications│  │ - Statements │  │ - Profile    │      │
│  │ - Refills    │  │ - Payments   │  │ - Consent    │      │
│  │ - History    │  │ - Insurance  │  │ - Preferences│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Achieving Quality Goals

#### QG-1: Security & Privacy (Priority 1)

**Measures**:

- **Encryption**: TLS 1.3 in transit, AES-256 at rest (Azure Storage Service Encryption)
- **Authentication**: Azure AD B2C with MFA mandatory (SMS or authenticator app)
- **Authorization**: Role-based access control (RBAC) + patient data isolation
- **Audit Logging**: All PHI access logged with user ID, timestamp, action
- **Data Masking**: SSN masked (show last 4 digits), DOB masked in logs
- **Breach Detection**: Azure Security Center monitors for anomalies
- **Penetration Testing**: Annual third-party pen test
- **Compliance**: HIPAA Security Risk Analysis completed annually

**Validation**: Zero breaches in 3 years of production ✅

#### QG-2: Availability (Priority 2)

**Measures**:

- **Multi-Region**: Active-passive across 2 Azure regions (primary: East US, secondary: West US)
- **Database**: Azure SQL with geo-replication and automatic failover groups
- **Redundancy**: Each microservice has min 3 instances across availability zones
- **Health Checks**: Kubernetes liveness/readiness probes
- **Circuit Breakers**: Polly library for fault tolerance (EHR, scheduling system)
- **Graceful Degradation**: Cache last 24h of data, show cached if EHR unavailable
- **Monitoring**: 24/7 on-call, PagerDuty alerts for P1 issues

**Validation**: 99.94% uptime last 12 months ✅

#### QG-3: Performance (Priority 3)

**Measures**:

- **Caching**: Redis caches EHR data (lab results, medications) with 5-minute TTL
- **Database Optimization**: Indexes on query patterns, read replicas for reporting
- **CDN**: Azure CDN for static assets (images, CSS, JS)
- **Async Processing**: Azure Service Bus for non-critical tasks (email notifications)
- **Query Optimization**: Entity Framework compiled queries
- **Connection Pooling**: ADO.NET connection pooling (max 100 connections)
- **Lazy Loading**: Load medical records on-demand, not upfront

**Validation**: Appointment search p95 = 1.8s (target: < 2s) ✅

#### QG-4: Usability (Priority 4)

**Measures**:

- **WCAG 2.1 AA**: Keyboard navigation, screen reader support, color contrast ratios
- **User Testing**: Quarterly usability testing with 20 patients (diverse ages, abilities)
- **Simplified UI**: Max 3 clicks to book appointment, clear error messages
- **Help Center**: Contextual help, video tutorials, chatbot for common questions
- **Multilingual**: English, Spanish support (60% of patient base)

**Validation**: Support calls: 3.2 per 1000 users (target: < 5) ✅

#### QG-5: Interoperability (Priority 5)

**Measures**:

- **FHIR Compliance**: HL7 FHIR R4 for all EHR communication
- **SMART on FHIR**: Support SMART app launch for third-party integrations
- **API Documentation**: OpenAPI specs published, developer portal
- **Standardized Codes**: SNOMED CT for conditions, LOINC for lab tests, RxNorm for meds
- **Sync Frequency**: Real-time for critical data, 15-minute batch for reports

**Validation**: EHR sync delay p95 = 3 minutes (target: < 5 min) ✅

### 4.4 Organizational Decisions

**Team Structure** (Conway's Law Applied):

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Appointments Team│  │  Records Team    │  │  Messaging Team  │
│  (3 developers)  │  │  (4 developers)  │  │  (3 developers)  │
│                  │  │                  │  │                  │
│ - Appointment    │  │ - Medical Records│  │ - Messaging      │
│   Service        │  │   Service        │  │   Service        │
│ - Scheduling     │  │ - Lab Results    │  │ - Notifications  │
│   Integration    │  │ - EHR Integration│  │                  │
└──────────────────┘  └──────────────────┘  └──────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ Pharmacy Team    │  │  Billing Team    │  │  Platform Team   │
│  (2 developers)  │  │  (2 developers)  │  │  (3 developers)  │
│                  │  │                  │  │                  │
│ - Prescription   │  │ - Billing Service│  │ - Shared libs    │
│   Service        │  │ - Payment Gateway│  │ - CI/CD pipeline │
│ - Surescripts    │  │ - Cerner         │  │ - Monitoring     │
│   Integration    │  │   Integration    │  │ - Infrastructure │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

**Development Workflow**:

- **Sprint Length**: 2 weeks
- **Deployment Frequency**: Weekly to production (Thursday deployments)
- **Code Review**: Required, 2 approvers minimum
- **Testing**: Unit (developers), integration (QA), UAT (product owners + clinicians)
- **On-Call Rotation**: 1-week rotation per team

---

## 5. Building Block View

### 5.1 Level 1: System Context

**Whitebox Overall System**:

```
┌─────────────────────────────────────────────────────────────┐
│          Healthcare Patient Portal (Whitebox)                │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │         Frontend Layer (User Interface)            │     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────┐  │     │
│  │  │  Web App    │  │  iOS App    │  │ Android  │  │     │
│  │  │  (React)    │  │  (Swift)    │  │  (Kotlin)│  │     │
│  │  └─────────────┘  └─────────────┘  └──────────┘  │     │
│  └────────────┬───────────────────────────────────────┘     │
│               │ HTTPS/REST                                  │
│  ┌────────────▼───────────────────────────────────────┐     │
│  │            API Gateway Layer                       │     │
│  │     (Azure API Management)                         │     │
│  │  - Authentication & Authorization                  │     │
│  │  - Rate Limiting                                   │     │
│  │  - Request Routing                                 │     │
│  └────────────┬───────────────────────────────────────┘     │
│               │ HTTP/2                                      │
│  ┌────────────▼───────────────────────────────────────┐     │
│  │         Application Services Layer                 │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐  ┌─────┐ │     │
│  │  │Appointmt │ │ Records  │ │Messaging │..│Other│ │     │
│  │  │ Service  │ │ Service  │ │ Service  │  │ ... │ │     │
│  │  └──────────┘ └──────────┘ └──────────┘  └─────┘ │     │
│  └────────────┬───────────────────────────────────────┘     │
│               │ SQL/Redis/ServiceBus                        │
│  ┌────────────▼───────────────────────────────────────┐     │
│  │           Data & Integration Layer                 │     │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │     │
│  │  │  SQL DB  │ │  Redis   │ │  Service Bus     │   │     │
│  │  │(Per Svc) │ │  Cache   │ │  (Async Queue)   │   │     │
│  │  └──────────┘ └──────────┘ └──────────────────┘   │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
         │                │                │
         ▼                ▼                ▼
   ┌─────────┐     ┌──────────┐    ┌──────────┐
   │  Epic   │     │Centricity│    │Surescripts│
   │  EHR    │     │Scheduling│    │ Pharmacy │
   └─────────┘     └──────────┘    └──────────┘
```

**Contained Building Blocks**:

| Name | Responsibility |
|------|----------------|
| **Frontend Layer** | User interface for patients and providers |
| **API Gateway** | Authentication, rate limiting, routing |
| **Application Services** | Business logic, domain models, orchestration |
| **Data & Integration** | Persistence, caching, async messaging |

**Important Interfaces**:

| Interface | Description |
|-----------|-------------|
| **Frontend ↔ API Gateway** | HTTPS/REST with OAuth 2.0 tokens |
| **API Gateway ↔ Services** | HTTP/2 with JWT validation |
| **Services ↔ External Systems** | FHIR/REST, SOAP, HL7 v2 |

### 5.2 Level 2: Application Services (Whitebox)

**Appointment Service** (Example microservice decomposition):

```
┌───────────────────────────────────────────────────────┐
│          Appointment Service (Whitebox)               │
│                                                       │
│  ┌─────────────────────────────────────────────┐     │
│  │          API Layer                          │     │
│  │  ┌────────────────┐  ┌──
