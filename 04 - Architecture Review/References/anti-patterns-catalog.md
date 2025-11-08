# Architectural Anti-Patterns Catalog

A comprehensive catalog of common architectural anti-patterns, their symptoms, impacts, and remediation strategies. Use this as reference during architecture reviews to identify and address problematic patterns.

---

## What is an Anti-Pattern?

An **Input Validation**:
```java
@RestController
public class UserController {
    
    @PostMapping("/users")
    public User createUser(@Valid @RequestBody UserRequest request) {
        // @Valid triggers validation
    }
}

public class UserRequest {
    @NotNull(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be 2-100 characters")
    private String name;
    
    @Email(message = "Invalid email format")
    @NotNull
    private String email;
    
    @Min(value = 18, message = "Must be 18+")
    @Max(value = 120, message = "Age must be realistic")
    private Integer age;
    
    @Pattern(regexp = "^[A-Za-z0-9]+$", message = "Username: alphanumeric only")
    private String username;
}
```

**XSS Prevention**:
```javascript
// Bad: Direct innerHTML
element.innerHTML = userInput;  // Can execute scripts

// Good: Use textContent or escape
element.textContent = userInput;  // Safe, treats as text

// Good: Sanitize HTML
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);
```

**Prevention Checklist**:
- [ ] Validate all inputs (type, length, format, range)
- [ ] Use prepared statements (never string concatenation for SQL)
- [ ] Sanitize outputs (escape HTML, encode for JSON)
- [ ] Whitelist approach (allow known good, not block known bad)
- [ ] Rate limiting (prevent abuse)
- [ ] Content Security Policy headers

---

## Performance Anti-Patterns

### 13. Premature Optimization

**Description**: Optimizing code before there's evidence of a performance problem.

**Symptoms**:
- 🚩 Complex, hard-to-read code "for performance"
- 🚩 Micro-optimizations that provide negligible benefit
- 🚩 Avoiding database queries by keeping everything in memory
- 🚩 Custom data structures instead of standard library

**Example**:
```java
// Premature optimization: Complex bit manipulation
// To save 3 bytes of memory per object
public class User {
    // Packing age (7 bits), active (1 bit), role (3 bits) into one int
    private int packedData;
    
    public int getAge() {
        return (packedData >> 4) & 0x7F;
    }
    
    public void setAge(int age) {
        packedData = (packedData & ~(0x7F << 4)) | ((age & 0x7F) << 4);
    }
    // Saves 3 bytes, costs readability and maintainability
}

// vs Simple, clear code
public class User {
    private int age;  // Just use an int!
    private boolean active;
    private Role role;
}
```

**Impact**:
- Hard to maintain (complex code)
- Hard to debug (obscure bugs)
- Wasted effort (optimizing non-bottlenecks)
- Delayed delivery (time spent on wrong things)

**Famous Quote**:
> "Premature optimization is the root of all evil" - Donald Knuth

**How to Fix**:

**Step 1: Measure First**
```
Don't optimize based on assumptions
↓
Profile the application
↓
Identify actual bottlenecks (80/20 rule: 80% of time in 20% of code)
↓
Optimize the bottlenecks
↓
Measure again to validate improvement
```

**Step 2: Optimize Only When**:
- Performance testing shows a problem
- Problem is in critical path
- Problem significantly impacts users
- Simpler solutions don't work

**Step 3: Optimize Strategically**:
```
1. Algorithm complexity (O(n²) → O(n log n)) - biggest impact
2. Caching (avoid repeated work)
3. Database queries (N+1, indexing)
4. Network calls (batch, async)
5. Micro-optimizations (last resort)
```

**Prevention**:
- "Make it work, make it right, make it fast" - in that order
- Profile before optimizing
- Focus on algorithmic improvements, not micro-optimizations
- Keep code simple and readable by default

---

### 14. Caching Everything

**Description**: Over-eager caching without considering trade-offs.

**Symptoms**:
- 🚩 Everything cached "just in case"
- 🚩 Stale data (cache not invalidated)
- 🚩 Cache inconsistency (different caches showing different data)
- 🚩 Memory exhaustion (cache grows unbounded)
- 🚩 Complex cache invalidation logic

**Example**:
```java
// Over-caching
@Cacheable("users")  // Cached
public User getUser(String id) { }

@Cacheable("usersByEmail")  // Also cached
public User getUserByEmail(String email) { }

@Cacheable("userProfiles")  // Also cached
public UserProfile getProfile(String userId) { }

// Problem: User updates
// Need to invalidate: users, usersByEmail, userProfiles
// Easy to miss one → stale data
```

**Impact**:
- Stale data (users see old information)
- Memory issues (cache grows too large)
- Complexity (cache invalidation is hard)
- Debugging nightmares (which cache is stale?)

**How to Fix**:

**Cache Strategically**:
```
Cache when:
✅ Data is expensive to compute/fetch
✅ Data is read frequently (high read/write ratio)
✅ Staleness is acceptable (eventual consistency OK)
✅ Cache invalidation is straightforward

Don't cache when:
❌ Data changes frequently
❌ Staleness is not acceptable
❌ Simple to compute/fetch
❌ Cache invalidation is complex
```

**Cache Levels**:
```
1. HTTP cache (CDN, browser) - static assets, API responses
2. Application cache (Redis) - computed results, session data
3. Database query cache - query results
4. Database cache - hot data in memory

Start at top, add lower levels only if needed
```

**Proper Caching Example**:
```java
// Cache product catalog (changes infrequently)
@Cacheable(value = "products", key = "#id")
public Product getProduct(String id) {
    return productRepository.findById(id);
}

@CacheEvict(value = "products", key = "#product.id")
public Product updateProduct(Product product) {
    return productRepository.save(product);
}

// DON'T cache user session (changes frequently, security risk)
public UserSession getSession(String sessionId) {
    return sessionRepository.findById(sessionId);  // No cache
}
```

**Cache Configuration**:
```yaml
cache:
  products:
    ttl: 3600  # 1 hour (products don't change often)
    max-entries: 10000
  
  search-results:
    ttl: 300  # 5 minutes (search indexes update)
    max-entries: 1000
```

**Prevention**:
- Only cache when you have performance data showing need
- Set TTL (time-to-live) on all cache entries
- Set max size to prevent unbounded growth
- Document cache invalidation strategy
- Monitor cache hit rates (low hit rate = remove cache)

---

## Operational Anti-Patterns

### 15. No Observability

**Description**: Insufficient logging, monitoring, and tracing in production.

**Symptoms**:
- 🚩 "It's slow" - no metrics to prove/disprove
- 🚩 "It crashed" - no logs explaining why
- 🚩 MTTD (Mean Time To Detect) is hours/days
- 🚩 Debugging requires adding logs and redeploying
- 🚩 Can't trace requests across services

**Example**:
```java
// Insufficient observability
public void processOrder(Order order) {
    // No logging, no metrics, no tracing
    paymentService.process(order);
    inventoryService.reserve(order);
    fulfillmentService.ship(order);
    // If anything fails, no idea what or why
}
```

**Impact**:
- Slow incident response (can't diagnose issues)
- Poor customer experience (issues not detected)
- Guesswork debugging (no data)
- Repeat incidents (root cause unknown)

**How to Fix**:

**The Three Pillars of Observability**:

**1. Logging**:
```java
public void processOrder(Order order) {
    log.info("Processing order: orderId={}, userId={}, total={}", 
        order.getId(), order.getUserId(), order.getTotal());
    
    try {
        PaymentResult payment = paymentService.process(order);
        log.info("Payment processed: orderId={}, paymentId={}, status={}", 
            order.getId(), payment.getId(), payment.getStatus());
        
        inventoryService.reserve(order);
        log.info("Inventory reserved: orderId={}", order.getId());
        
        fulfillmentService.ship(order);
        log.info("Order shipped: orderId={}", order.getId());
        
    } catch (Exception e) {
        log.error("Order processing failed: orderId={}, error={}", 
            order.getId(), e.getMessage(), e);
        throw e;
    }
}
```

**2. Metrics**:
```java
@Timed(value = "orders.process", percentiles = {0.5, 0.95, 0.99})
public void processOrder(Order order) {
    orderCounter.increment();  // Total orders processed
    
    try {
        paymentService.process(order);
        successCounter.increment();  // Successful orders
    } catch (PaymentException e) {
        paymentFailureCounter.increment();  // Failed payments
        throw e;
    }
}

// Dashboards show:
// - Orders per second
// - Success rate
// - Latency (p50, p95, p99)
// - Error rate
```

**3. Distributed Tracing**:
```java
// Automatic with Spring Cloud Sleuth + Zipkin
public void processOrder(Order order) {
    // Trace ID automatically propagated across services
    // Can see full request path:
    // API Gateway (50ms) → Order Service (100ms) → Payment Service (200ms)
}
```

**Observability Stack**:
```
Logging: Structured logs → ELK/Loki → Kibana/Grafana
Metrics: Prometheus → Grafana dashboards
Tracing: Zipkin/Jaeger → distributed traces
APM: Datadog/New Relic → unified view
```

**What to Monitor**:

**Application Metrics**:
- Request rate (requests/second)
- Error rate (errors/second, %)
- Latency (p50, p95, p99)
- Saturation (resource utilization)

**Business Metrics**:
- Orders per hour
- Revenue per hour
- Conversion rate
- Active users

**Infrastructure Metrics**:
- CPU, memory, disk utilization
- Network bandwidth
- Database connections
- Queue depth

**Prevention**:
- Structured logging from day one
- Metrics for all critical operations
- Distributed tracing in microservices
- Dashboards for common queries
- Alerts for SLO violations

---

### 16. Manual Deployment

**Description**: Deploying software manually without automation.

**Symptoms**:
- 🚩 Deployment takes 4 hours
- 🚩 Deployment document is 50 steps
- 🚩 Deployments only done by one person who knows the steps
- 🚩 Deployments only on Friday nights (risky)
- 🚩 Different steps for dev/staging/production

**Example**:
```bash
# Manual deployment "runbook"
1. SSH to server
2. Stop application: systemctl stop app
3. Backup database: pg_dump ...
4. Copy new JAR from laptop: scp ...
5. Update config file: vi application.properties
6. Start application: systemctl start app
7. Test by clicking around
8. If broken, manually rollback (good luck!)
```

**Impact**:
- Slow deployments (hours instead of minutes)
- Error-prone (humans make mistakes)
- Fear of deployment (deploy rarely, big batches)
- Knowledge silos (only Bob knows how)
- Can't scale (one deployment at a time)

**How to Fix**:

**CI/CD Pipeline**:
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: ./gradlew test
      
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker image
        run: docker build -t app:${{ github.sha }} .
      - name: Push to registry
        run: docker push app:${{ github.sha }}
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/app \
            app=app:${{ github.sha }}
          kubectl rollout status deployment/app
      
      - name: Run smoke tests
        run: ./smoke-tests.sh
      
      - name: Rollback on failure
        if: failure()
        run: kubectl rollout undo deployment/app
```

**Benefits**:
- Fast (minutes, not hours)
- Consistent (same process every time)
- Auditable (Git log shows what was deployed when)
- Rollback easy (previous version saved)
- Can deploy many times per day

**Deployment Strategies**:

**Blue-Green**:
```
Blue (current) running with 100% traffic
↓
Deploy Green (new version)
↓
Test Green
↓
Switch traffic: Blue 0% → Green 100%
↓
Keep Blue for quick rollback
```

**Canary**:
```
Deploy new version to 5% of servers
↓
Monitor metrics (errors, latency)
↓
If good, increase to 25%
↓
If good, increase to 100%
↓
If bad at any point, rollback
```

**Rolling**:
```
10 servers total
↓
Update 2 servers (20%), keep 8 old (80%)
↓
Test, if OK, update next 2
↓
Repeat until all updated
```

**Prevention**:
- Automate from day one
- Treat infrastructure as code (Terraform, CloudFormation)
- Immutable infrastructure (Docker, Kubernetes)
- Deployment = Git push (GitOps)

---

## Testing Anti-Patterns

### 17. No Tests / Wrong Tests

**Description**: Either no automated tests, or tests that don't provide value.

**Symptoms**:
- 🚩 Zero or very low test coverage (<20%)
- 🚩 Tests that test getters/setters only
- 🚩 Tests that mock everything (testing mocks, not code)
- 🚩 Flaky tests (fail randomly)
- 🚩 Tests take 2 hours to run

**Example - Wrong Tests**:
```java
// Useless test - testing getters
@Test
public void testGetName() {
    User user = new User();
    user.setName("Alice");
    assertEquals("Alice", user.getName());  // Duh!
}

// Over-mocked test - not testing anything real
@Test
public void testProcessOrder() {
    PaymentService paymentService = mock(PaymentService.class);
    InventoryService inventoryService = mock(InventoryService.class);
    
    when(paymentService.process(any())).thenReturn(PaymentResult.success());
    when(inventoryService.reserve(any())).thenReturn(true);
    
    // Testing mocks, not actual business logic!
}
```

**Impact**:
- Bugs in production (no test coverage)
- False confidence (tests don't catch issues)
- Slow feedback (tests take forever)
- Ignored tests (flaky tests get disabled)

**How to Fix**:

**Testing Pyramid**:
```
         E2E (10%)
       /          \
      /            \
   Integration (30%)
    /              \
   /                \
  Unit Tests (60%)
```

**Unit Tests** (fast, many):
```java
@Test
public void shouldCalculateOrderTotal() {
    Order order = new Order();
    order.addItem(new OrderItem("SKU1", 2, Money.of(10.00)));  // $20
    order.addItem(new OrderItem("SKU2", 1, Money.of(15.00)));  // $15
    
    Money total = order.calculateTotal();
    
    assertEquals(Money.of(35.00), total);
}

// Tests business logic, not infrastructure
// No database, no network, no mocks
// Runs in milliseconds
```

**Integration Tests** (slower, fewer):
```java
@SpringBootTest
@AutoConfigureTestDatabase
public class OrderServiceIntegrationTest {
    
    @Autowired
    private OrderService orderService;
    
    @Test
    public void shouldProcessOrderEndToEnd() {
        Order order = createTestOrder();
        
        // Real database, real services (maybe mocked external APIs)
        OrderResult result = orderService.process(order);
        
        assertEquals(OrderStatus.COMPLETED, result.getStatus());
        
        // Verify in database
        Order saved = orderRepository.findById(result.getOrderId());
        assertNotNull(saved);
    }
}
```

**E2E Tests** (slowest, fewest):
```javascript
// Playwright/Cypress
test('user can complete checkout', async ({ page }) => {
  await page.goto('/products');
  await page.click('button:has-text("Add to Cart")');
  await page.click('a:has-text("Checkout")');
  
  await page.fill('#email', 'test@example.com');
  await page.fill('#card', '4242424242424242');
  await page.click('button:has-text("Place Order")');
  
  await expect(page.locator('.success')).toContainText('Order confirmed');
});
```

**Test Best Practices**:
- **AAA Pattern**: Arrange, Act, Assert
- **One assertion per test** (or closely related assertions)
- **Independent tests** (can run in any order)
- **Fast tests** (unit tests < 100ms, integration < 1s)
- **Descriptive names**: `shouldCalculateOrderTotalWithMultipleItems()`
- **Test behavior, not implementation**

**Prevention**:
- TDD (Test-Driven Development) - write tests first
- Require tests for all new code (PR reviews)
- CI fails if coverage drops
- Regular test suite maintenance (remove flaky tests)

---

## Summary: Anti-Pattern Detection

### Quick Checklist

During architecture review, look for these red flags:

**Distribution**:
- [ ] Microservices without clear bounded contexts?
- [ ] Shared database across services?
- [ ] Long synchronous call chains?
- [ ] No circuit breakers on external calls?

**Data**:
- [ ] N+1 query patterns?
- [ ] Anemic domain models?
- [ ] Database as integration point?
- [ ] No data ownership defined?

**Security**:
- [ ] Secrets in code or config files?
- [ ] No input validation?
- [ ] SQL injection vulnerabilities?
- [ ] No authentication/authorization?

**Performance**:
- [ ] Premature optimizations?
- [ ] Everything cached "just in case"?
- [ ] No performance testing?
- [ ] No query optimization?

**Operations**:
- [ ] No logging, metrics, or tracing?
- [ ] Manual deployment process?
- [ ] No monitoring or alerting?
- [ ] No disaster recovery plan?

**Testing**:
- [ ] No automated tests?
- [ ] Tests that don't provide value?
- [ ] Flaky test suite?
- [ ] Tests take hours to run?

---

## References

### Books
- *Software Architecture Patterns* - Mark Richards
- *Building Microservices* - Sam Newman
- *Domain-Driven Design* - Eric Evans
- *Release It!* - Michael Nygard
- *Refactoring* - Martin Fowler

### Online Resources
- [Microservices.io Patterns](https://microservices.io/patterns/)
- [Martin Fowler's Blog](https://martinfowler.com/)
- [Microsoft Architecture Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### Pattern Catalogs
- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/)
- [Cloud Design Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/)
- [Resilience Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/category/resiliency)

---

**End of Anti-Patterns Catalog**

Use this catalog during architecture reviews to quickly identify common problematic patterns and provide evidence-based recommendations for improvement.anti-pattern** is a common solution to a problem that appears beneficial at first but ultimately leads to negative consequences. Unlike bugs (which are mistakes), anti-patterns are often intentional decisions that seem reasonable but create problems over time.

**Key Characteristics**:
- Appears to be a good solution initially
- Becomes problematic as system evolves
- Has well-documented better alternatives
- Requires significant refactoring to fix

---

## Microservices & Distribution Anti-Patterns

### 1. Distributed Monolith

**Description**: Microservices architecture that retains all the coupling of a monolith while adding distributed system complexity.

**Symptoms**:
- 🚩 Services share the same database
- 🚩 All services must be deployed together (coordinated releases)
- 🚩 Changes ripple across multiple services
- 🚩 Synchronous calls everywhere (no async communication)
- 🚩 No independent scaling (scale all or nothing)
- 🚩 Service boundaries don't match business domains

**Example**:
```
UserService → Database
OrderService → Database  (same DB!)
PaymentService → Database

OrderService calls UserService synchronously
PaymentService calls OrderService synchronously
All deployed together or nothing works
```

**Impact**:
- All complexity of microservices (network, deployment, monitoring)
- None of the benefits (independence, scalability, resilience)
- Worse than a well-designed monolith
- High operational overhead with no gain

**Root Causes**:
- Decomposed by technical layers instead of business domains
- Skipped domain modeling and bounded contexts
- "Microservices first" without understanding why

**How to Fix**:

**Option 1: Proper Microservices**
1. Apply Domain-Driven Design (identify bounded contexts)
2. Database per service (own your data)
3. Async communication via events (message bus)
4. Independent deployment pipelines
5. Clear API contracts with versioning

**Option 2: Modular Monolith**
1. Consolidate into single deployable unit
2. Strong module boundaries (packages, namespaces)
3. Clear interfaces between modules
4. Share database but separate schemas
5. Much simpler to operate

**When to Choose**:
- Microservices: Team >15 people, clear domains, need independent scaling
- Modular Monolith: Team <15 people, domains unclear, simpler operations preferred

**Prevention**:
- Start with modular monolith
- Extract microservices when you have clear pain points
- Never start with microservices "because it's best practice"

---

### 2. Chatty APIs (N+1 Problem)

**Description**: Making many small API calls to accomplish a single task.

**Symptoms**:
- 🚩 Mobile app makes 10+ API calls to load one screen
- 🚩 Waterfall of sequential network requests
- 🚩 High latency despite fast individual services
- 🚩 API calls in loops (N+1 query pattern at API level)

**Example**:
```javascript
// Bad: Chatty API calls
async function loadDashboard() {
  const user = await fetch('/api/user');           // Call 1
  const profile = await fetch('/api/profile');     // Call 2
  const orders = await fetch('/api/orders');       // Call 3
  
  // For each order, fetch details
  for (let order of orders) {
    const details = await fetch(`/api/orders/${order.id}`);  // Call 4-N
  }
}
// Total: 3 + N calls, sequential waterfall
```

**Impact**:
- Poor user experience (slow page loads)
- Wasted bandwidth (HTTP overhead per request)
- Higher infrastructure costs (more requests to handle)
- Battery drain on mobile devices

**How to Fix**:

**Option 1: Backend for Frontend (BFF)**
```javascript
// API endpoint that aggregates
GET /api/dashboard
// Returns: { user, profile, orders: [{ ...details }] }

// Frontend makes 1 call instead of N
const dashboard = await fetch('/api/dashboard');
```

**Option 2: GraphQL**
```graphql
query Dashboard {
  user {
    name
    email
  }
  orders {
    id
    status
    items {
      name
      price
    }
  }
}
# Single request, flexible response
```

**Option 3: Batch API**
```javascript
POST /api/batch
{
  "requests": [
    { "method": "GET", "path": "/user" },
    { "method": "GET", "path": "/profile" },
    { "method": "GET", "path": "/orders" }
  ]
}
// Server processes in parallel, returns all results
```

**Prevention**:
- Design APIs for client use cases, not server architecture
- Consider GraphQL for flexible data fetching
- Implement batch endpoints for known multi-fetch patterns
- Monitor API call patterns from clients

---

### 3. God Service (Mega Service)

**Description**: A single service that does too many things, violating single responsibility principle.

**Symptoms**:
- 🚩 Service has 50+ API endpoints
- 🚩 100K+ lines of code in single repository
- 🚩 Multiple unrelated business capabilities (users, orders, products, payments all in one)
- 🚩 15+ database tables owned by one service
- 🚩 Deploys take 30+ minutes
- 🚩 Every team needs to touch this service

**Example**:
```
"api-service" handles:
- User management
- Order processing  
- Payment processing
- Inventory management
- Notifications
- Analytics
- Reporting
- ... everything
```

**Impact**:
- Bottleneck for all changes
- Hard to test (too many concerns)
- Hard to scale (one part needs more resources, scale all)
- Deploy risk high (any change affects everything)
- Team conflicts (everyone working in same codebase)
- Cognitive overload (no one understands it all)

**How to Fix**:

**Step 1: Domain Analysis**
- Identify bounded contexts (DDD)
- Map capabilities to business domains
- Find natural seams for decomposition

**Step 2: Strangler Fig Pattern**
```
Start: God Service (everything)
↓
Phase 1: Extract User Service (well-defined boundary)
- God Service still handles users internally
- New User Service for new features
- Gradually migrate
↓
Phase 2: Extract Order Service
↓
Phase 3: Extract Payment Service
↓
End: Multiple focused services, legacy god service retired
```

**Step 3: Implementation**
1. Create new service for one domain
2. Implement new features in new service
3. Proxy old endpoints to new service
4. Migrate data gradually
5. Retire old code when migration complete

**Warning**: Don't create "micro-god-services" - small services that are still doing too much. Focus on business domain cohesion.

**Prevention**:
- Define service boundaries based on business domains, not technical layers
- Regular architecture reviews to catch bloat early
- "Two pizza team" rule - if can't be fed by two pizzas, too big

---

### 4. Shared Database Anti-Pattern

**Description**: Multiple services directly accessing the same database, creating tight coupling.

**Symptoms**:
- 🚩 Service A directly queries Service B's database tables
- 🚩 Database schema changes break multiple services
- 🚩 Can't deploy services independently
- 🚩 No clear data ownership
- 🚩 Database becomes integration point

**Example**:
```
OrderService → Database ← PaymentService (both read/write same tables)
                 ↑
          UserService (also accessing same DB)
```

**Impact**:
- Tight coupling (can't change schema without coordinating all services)
- No encapsulation (business logic scattered across services)
- Transaction boundaries unclear
- Can't scale services independently
- Database becomes bottleneck

**How to Fix**:

**Option 1: Database per Service**
```
OrderService → Order DB (owns order data)
PaymentService → Payment DB (owns payment data)
UserService → User DB (owns user data)

Communication via:
- APIs (synchronous)
- Events (asynchronous)
- API Composition pattern
```

**Option 2: Schema per Service (same physical DB)**
```
Database
├── order_schema (OrderService only)
├── payment_schema (PaymentService only)
└── user_schema (UserService only)

Enforce with DB permissions
```

**Migration Strategy**:
1. **Audit**: Identify all cross-service queries
2. **Replace**: Implement API calls or event subscriptions
3. **Migrate**: Move tables to service-owned databases
4. **Enforce**: Database permissions prevent cross-service access

**Data Sharing Patterns**:

When services need each other's data:

**Pattern 1: API Composition**
```
GET /orders/123
OrderService:
  1. Get order from Order DB
  2. Call UserService API for user details
  3. Compose response
```

**Pattern 2: Event-Driven Materialized View**
```
UserService publishes UserUpdated event
→ OrderService subscribes and maintains local user cache
→ OrderService queries own cache (no runtime dependency)
```

**Pattern 3: Data Replication**
For read-only reference data, replicate to consuming services.

**Prevention**:
- Define data ownership upfront (which service owns what entity)
- Make cross-database queries impossible (network isolation)
- Code reviews flag any direct database access across boundaries

---

## Data & Persistence Anti-Patterns

### 5. N+1 Query Problem

**Description**: Executing one query to get a list, then N queries to get details for each item.

**Symptoms**:
- 🚩 Page load triggers 100+ database queries
- 🚩 Database connection pool exhausted
- 🚩 Slow performance that gets worse with more data
- 🚩 Database CPU at 100% for simple operations

**Example**:
```sql
-- Query 1: Get all orders
SELECT * FROM orders WHERE user_id = 123;  -- Returns 50 orders

-- Queries 2-51: For each order, get items
SELECT * FROM order_items WHERE order_id = 1;
SELECT * FROM order_items WHERE order_id = 2;
...
SELECT * FROM order_items WHERE order_id = 50;

-- Total: 51 queries for one page!
```

**Code Example**:
```javascript
// Bad: N+1 queries
const orders = await Order.findAll({ where: { userId: 123 } });  // 1 query

for (let order of orders) {
  order.items = await OrderItem.findAll({ where: { orderId: order.id } });  // N queries
}
```

**Impact**:
- Extremely poor performance (network roundtrips dominate)
- Database overload (queries scale with data size)
- Connection pool exhaustion
- Timeouts and failed requests

**How to Fix**:

**Option 1: Eager Loading (JOIN)**
```javascript
// Good: Single query with JOIN
const orders = await Order.findAll({
  where: { userId: 123 },
  include: [{ model: OrderItem }]  // ORM generates JOIN
});

// SQL: SELECT orders.*, order_items.* FROM orders
//      LEFT JOIN order_items ON orders.id = order_items.order_id
//      WHERE orders.user_id = 123
```

**Option 2: Batch Loading (IN clause)**
```javascript
// Good: 2 queries instead of N+1
const orders = await Order.findAll({ where: { userId: 123 } });  // 1 query
const orderIds = orders.map(o => o.id);

const items = await OrderItem.findAll({ 
  where: { orderId: { in: orderIds } }  // 1 query with IN clause
});

// Group items by order
const itemsByOrder = _.groupBy(items, 'orderId');
orders.forEach(order => {
  order.items = itemsByOrder[order.id] || [];
});
```

**Option 3: DataLoader Pattern**
```javascript
// For GraphQL or similar
const orderLoader = new DataLoader(async (orderIds) => {
  const items = await OrderItem.findAll({ 
    where: { orderId: { in: orderIds } } 
  });
  // Return items grouped by order ID
  return orderIds.map(id => items.filter(item => item.orderId === id));
});

// Automatically batches requests within same tick
const items1 = await orderLoader.load(order1.id);
const items2 = await orderLoader.load(order2.id);
// Single query for both: SELECT * FROM order_items WHERE order_id IN (1, 2)
```

**Prevention**:
- Enable query logging in development to spot N+1
- Use ORM query analysis tools
- Load testing with realistic data volumes
- Code review checklist: "Are we querying in a loop?"

---

### 6. Anemic Domain Model

**Description**: Domain objects are just data containers with no behavior; all logic is in services.

**Symptoms**:
- 🚩 Domain classes have only getters/setters
- 🚩 All business logic in service layer
- 🚩 Services manipulate domain objects like data structures
- 🚩 No encapsulation of business rules

**Example**:
```java
// Anemic: Just a data container
public class Order {
    private String id;
    private List<OrderItem> items;
    private Money total;
    
    // Only getters and setters, no behavior
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }
    public List<OrderItem> getItems() { return items; }
    public void setItems(List<OrderItem> items) { this.items = items; }
    public Money getTotal() { return total; }
    public void setTotal(Money total) { this.total = total; }
}

// Service has all the logic
public class OrderService {
    public void addItem(Order order, OrderItem item) {
        order.getItems().add(item);  // Direct manipulation
        
        // Business logic outside domain model
        Money subtotal = Money.ZERO;
        for (OrderItem i : order.getItems()) {
            subtotal = subtotal.add(i.getPrice().multiply(i.getQuantity()));
        }
        order.setTotal(subtotal);  // Setting total from outside
    }
}
```

**Impact**:
- Business logic scattered across services
- Duplicated logic (same calculation in multiple places)
- Easy to violate invariants (total doesn't match items)
- Hard to test (need to test services, not domain)
- Domain model doesn't express business concepts

**How to Fix**:

**Rich Domain Model**:
```java
// Rich: Domain object with behavior
public class Order {
    private final String id;
    private final List<OrderItem> items;
    private Money total;
    
    public Order(String id) {
        this.id = id;
        this.items = new ArrayList<>();
        this.total = Money.ZERO;
    }
    
    // Business logic in domain model
    public void addItem(OrderItem item) {
        items.add(item);
        recalculateTotal();  // Encapsulated
    }
    
    public void removeItem(OrderItem item) {
        items.remove(item);
        recalculateTotal();
    }
    
    private void recalculateTotal() {
        this.total = items.stream()
            .map(OrderItem::getSubtotal)
            .reduce(Money.ZERO, Money::add);
    }
    
    public boolean canBeCancelled() {
        // Business rule encapsulated
        return status != OrderStatus.SHIPPED && 
               status != OrderStatus.DELIVERED;
    }
    
    public void cancel() {
        if (!canBeCancelled()) {
            throw new OrderCannotBeCancelledException(
                "Order cannot be cancelled in status: " + status
            );
        }
        this.status = OrderStatus.CANCELLED;
    }
    
    // Expose total, but don't allow external setting
    public Money getTotal() { return total; }
    
    // No setTotal() - calculated internally only
}

// Service is thin - just coordination
public class OrderService {
    public void addItem(String orderId, OrderItem item) {
        Order order = orderRepository.findById(orderId);
        order.addItem(item);  // Domain handles logic
        orderRepository.save(order);
    }
}
```

**When Anemic is OK**:
- Simple CRUD applications with minimal business logic
- Data Transfer Objects (DTOs) - explicitly just data carriers
- Integration models - mapping external data

**Prevention**:
- Start with domain modeling (Event Storming, DDD)
- Ask "what can this object DO?" not "what data does it have?"
- Business rules should live in domain objects
- Services coordinate, domains encapsulate

---

### 7. Database as Integration Point

**Description**: Using database as the primary means of communication between systems/services.

**Symptoms**:
- 🚩 Multiple applications write to same tables
- 🚩 "Integration" via database triggers
- 🚩 Scheduled jobs poll database for changes
- 🚩 No API layer, direct database access

**Example**:
```
Legacy System → Database ← New Service (both writing)
                   ↑
            Batch Job (polling for changes)
                   ↑
            Reporting Tool (reading)
```

**Impact**:
- Tight coupling (schema changes break everything)
- No business logic encapsulation
- Difficult to add validation or workflows
- Performance issues (polling, locks, contention)
- Data corruption risk (concurrent writes)
- Can't easily migrate to new database

**How to Fix**:

**Option 1: API Layer**
```
Legacy System → API → Service → Database
New Service → API → Service → Database
Batch Job → API → Service → Database

API enforces:
- Validation
- Business rules
- Versioning
- Access control
```

**Option 2: Event-Driven**
```
Service writes to Database
       ↓
Publishes event to Message Bus
       ↓
Consumers: Legacy System, Batch Job, Reporting (subscribe)

Benefits:
- Decoupled (consumers don't know about each other)
- Asynchronous (no blocking)
- Auditable (event log)
```

**Migration Strategy**:
1. **Add API layer** over database (BFF pattern)
2. **Migrate consumers** one by one to use API
3. **Enforce API access** (remove direct DB access)
4. **Introduce events** for change notifications
5. **Database becomes implementation detail**

**Prevention**:
- Never expose database directly to external systems
- APIs are contracts, databases are implementation
- Use events for cross-system communication

---

## Integration & Communication Anti-Patterns

### 8. Synchronous Coupling (Call Chain of Death)

**Description**: Long chains of synchronous service calls where failure in any step fails the entire operation.

**Symptoms**:
- 🚩 Service A calls B calls C calls D (synchronous chain)
- 🚩 Timeout in D propagates all the way back to A
- 🚩 Latency compounds (A waits for B waits for C waits for D)
- 🚩 Cascading failures (D down = all down)

**Example**:
```
User Request → API Gateway → Order Service → Payment Service → Fraud Check Service
                                                                      ↓
                                                                Fraud DB (slow query)

Total latency: 50ms + 100ms + 200ms + 500ms = 850ms
If Fraud Service times out (30s), entire request times out
```

**Impact**:
- Poor user experience (high latency)
- Low availability (availability = product of all services)
  - If each service is 99.9% available: 0.999^4 = 99.6%
- Hard to debug (which service caused the slowdown?)
- Resource exhaustion (threads waiting on downstream)

**How to Fix**:

**Option 1: Asynchronous Processing**
```
User Request → API Gateway → Order Service
                                  ↓
                          Publish OrderCreated event
                                  ↓
                            Message Queue
                          ↙                ↘
              Payment Service          Fraud Service
                  ↓                         ↓
           Process async            Process async
```

**Benefits**:
- Fast user response (order accepted immediately)
- Resilient (services can be down temporarily, events queued)
- Scalable (services scale independently)

**Option 2: Circuit Breaker Pattern**
```java
@CircuitBreaker(name = "fraudCheck", fallbackMethod = "fraudCheckFallback")
public FraudResult checkFraud(Order order) {
    return fraudService.check(order);  // Might fail
}

public FraudResult fraudCheckFallback(Order order, Exception e) {
    // Graceful degradation
    return FraudResult.manual Review();  // Human review later
}
```

**Option 3: Timeout & Bulkhead**
```java
// Set aggressive timeouts
@Timeout(2000)  // 2 seconds max
public PaymentResult processPayment(Order order) {
    return paymentService.process(order);
}

// Bulkhead: limit concurrent calls
@Bulkhead(maxConcurrentCalls = 10)
public PaymentResult processPayment(Order order) {
    // Only 10 concurrent calls allowed
    // 11th call rejected immediately (fail fast)
}
```

**When Synchronous is OK**:
- Critical path with strong consistency requirements
- Low latency downstream services
- Simple request-response patterns
- Few hops (2-3 max)

**Prevention**:
- Default to async for cross-service communication
- Use sync only when truly needed (strong consistency, immediate response)
- Always add circuit breakers and timeouts for sync calls

---

### 9. Missing Circuit Breaker

**Description**: No protection when calling external services, leading to cascading failures.

**Symptoms**:
- 🚩 External service timeout (30s) blocks threads
- 🚩 Thread pool exhaustion (all threads waiting)
- 🚩 Entire service becomes unresponsive
- 🚩 Recovery takes long time even after external service recovers

**Example**:
```java
// No protection - dangerous!
public OrderResult createOrder(Order order) {
    // If payment gateway is slow/down, this blocks for 30s
    PaymentResult payment = paymentGateway.process(order);
    
    // Under load:
    // - 100 requests/sec
    // - Each waits 30s
    // - Need 3000 threads!
    // - Server crashes
}
```

**Impact**:
- Cascading failures (one slow service takes down whole system)
- Long recovery time (need to wait for all in-flight requests to timeout)
- Poor user experience (everything slow/failing)
- Resource exhaustion

**How to Fix**:

**Circuit Breaker Pattern** (Resilience4j):
```java
@CircuitBreaker(
    name = "payment",
    fallbackMethod = "paymentFallback"
)
public PaymentResult processPayment(Order order) {
    return paymentGateway.process(order);
}

public PaymentResult paymentFallback(Order order, Exception e) {
    // Circuit open - fail fast, don't wait
    log.error("Payment service unavailable, queueing order", e);
    
    // Queue for later processing
    paymentQueue.enqueue(order);
    
    // Return graceful response
    return PaymentResult.pending(order.getId());
}
```

**Circuit Breaker States**:
```
Closed (normal) →  [failures exceed threshold] → Open (failing fast)
       ↑                                              ↓
       ← [success] ← Half-Open (trying) ← [wait period expires]
```

**Configuration**:
```yaml
resilience4j.circuitbreaker:
  instances:
    payment:
      failure-rate-threshold: 50  # Open if >50% fail
      wait-duration-in-open-state: 30s  # Stay open 30s
      sliding-window-size: 10  # Look at last 10 calls
      minimum-number-of-calls: 5  # Need 5 calls before evaluating
```

**Additional Patterns**:

**Timeout**:
```java
@Timeout(value = 2000)  // Fail after 2 seconds
public PaymentResult processPayment(Order order) {
    return paymentGateway.process(order);
}
```

**Retry with Exponential Backoff**:
```java
@Retry(
    name = "payment",
    fallbackMethod = "paymentFallback"
)
// Retry config: 3 attempts, 1s, 2s, 4s delays
public PaymentResult processPayment(Order order) {
    return paymentGateway.process(order);
}
```

**Bulkhead** (isolate failures):
```java
@Bulkhead(
    name = "payment",
    type = Bulkhead.Type.THREADPOOL
)
// Separate thread pool for payment calls
// If payment exhausts its pool, doesn't affect other operations
```

**Prevention**:
- Add circuit breaker to ALL external service calls
- Set reasonable timeouts (2-5s for most calls)
- Implement fallback strategies
- Monitor circuit breaker states in production

---

### 10. Retry Storm

**Description**: Multiple failed requests retrying simultaneously, overwhelming the already-struggling service.

**Symptoms**:
- 🚩 Service recovers, immediately gets hit with 10,000 retried requests
- 🚩 Service goes down again from retry load
- 🚩 Cycle repeats (down → retry storm → down again)
- 🚩 Much longer recovery time than necessary

**Example**:
```
Service goes down at 10:00
↓
1000 requests fail, each retries immediately
↓
1000 retries hit service at 10:00.1
↓
Service overwhelmed by 1000 simultaneous requests
↓
Service stays down, cycle repeats
```

**Impact**:
- Prolonged outages (retry traffic prevents recovery)
- Wasted resources (retries on already-overloaded service)
- Cascading failures (retry storm can spread)

**How to Fix**:

**Option 1: Exponential Backoff with Jitter**
```javascript
// Bad: Immediate retry
for (let i = 0; i < 3; i++) {
  try {
    return await callService();
  } catch (e) {
    // All requests retry at same time - retry storm!
  }
}

// Good: Exponential backoff with jitter
async function callWithRetry(maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await callService();
    } catch (e) {
      if (i === maxRetries - 1) throw e;
      
      // Exponential backoff: 1s, 2s, 4s
      const baseDelay = Math.pow(2, i) * 1000;
      
      // Jitter: randomize to spread retries
      const jitter = Math.random() * 1000;
      const delay = baseDelay + jitter;
      
      await sleep(delay);
    }
  }
}
```

**Option 2: Circuit Breaker** (prevents retry storm)
```
Circuit opens after failures
↓
Retries fail fast (don't hit service)
↓
Service has time to recover
↓
Circuit half-opens, test request
↓
If success, circuit closes, traffic resumes gradually
```

**Option 3: Rate Limiting + Queue**
```
Failed requests go to queue
↓
Queue drains at controlled rate (100/sec)
↓
Service not overwhelmed
↓
Gradual recovery
```

**Retry Best Practices**:
1. **Exponential backoff**: 1s, 2s, 4s, 8s (doubling)
2. **Jitter**: Add randomness to spread requests
3. **Max retries**: Limit to 3-5 attempts
4. **Idempotency**: Ensure retries are safe
5. **Circuit breaker**: Fail fast when service is down
6. **Observability**: Monitor retry rates

**Prevention**:
- Never retry immediately without backoff
- Always add jitter to retry delays
- Use circuit breakers to stop retries when service is down
- Monitor retry metrics (% of requests that are retries)

---

## Security Anti-Patterns

### 11. Secrets in Code/Config

**Description**: Hardcoding credentials, API keys, or sensitive data in source code or configuration files.

**Symptoms**:
- 🚩 Database passwords in application.properties
- 🚩 API keys committed to Git
- 🚩 AWS credentials in Dockerfile
- 🚩 Encryption keys in code

**Example**:
```java
// NEVER do this!
public class DatabaseConfig {
    private static final String DB_URL = "postgresql://prod-db.company.com";
    private static final String DB_USER = "admin";
    private static final String DB_PASSWORD = "SuperSecret123!";  // 🚨
}
```

```yaml
# NEVER in config files
database:
  password: SuperSecret123!  # 🚨 Will be in Git history forever
```

**Impact**:
- Security breach (credentials exposed in Git)
- Can't rotate credentials (hardcoded everywhere)
- Compliance violations
- Credential sprawl (same password everywhere)

**How to Fix**:

**Option 1: Environment Variables**
```java
public class DatabaseConfig {
    private String dbPassword = System.getenv("DB_PASSWORD");
}
```

```bash
# Set in environment
export DB_PASSWORD="SuperSecret123!"
```

**Option 2: Secrets Management Service**
```java
// AWS Secrets Manager
public class DatabaseConfig {
    public String getDbPassword() {
        GetSecretValueRequest request = new GetSecretValueRequest()
            .withSecretId("prod/db/password");
        
        GetSecretValueResult result = secretsManager.getSecretValue(request);
        return result.getSecretString();
    }
}
```

**Option 3: Vault (HashiCorp)
```java
VaultOperations vault = vaultTemplate.opsForKeyValue("secret");
String password = vault.get("database/password").getData().get("value");
```

**Prevention**:
- Never commit secrets to Git
- Use `.gitignore` for local config files
- Pre-commit hooks to scan for secrets
- Use secrets management (Vault, AWS Secrets Manager, Azure Key Vault)
- Rotate secrets regularly
- Different secrets per environment

---

### 12. No Input Validation

**Description**: Accepting and processing untrusted input without validation or sanitization.

**Symptoms**:
- 🚩 SQL injection vulnerabilities
- 🚩 XSS (Cross-Site Scripting) attacks possible
- 🚩 No length limits (DoS via large inputs)
- 🚩 Type confusion (sending string where number expected)

**Example**:
```java
// Vulnerable to SQL injection
public User getUser(String userId) {
    String query = "SELECT * FROM users WHERE id = '" + userId + "'";
    //  User sends: userId = "1' OR '1'='1"
    // Query becomes: SELECT * FROM users WHERE id = '1' OR '1'='1'
    // Returns ALL users!
}
```

**Impact**:
- Data breaches (SQL injection, unauthorized access)
- Data corruption (invalid data stored)
- DoS (large inputs crash system)
- XSS attacks (stored scripts)

**How to Fix**:

**SQL Injection Prevention**:
```java
// Use prepared statements
public User getUser(String userId) {
    String query = "SELECT * FROM users WHERE id = ?";
    PreparedStatement stmt = connection.prepareStatement(query);
    stmt.setString(1, userId);  // Safely parameterized
    return stmt.executeQuery();
}

// OR use ORM
public User getUser(String userId) {
    return userRepository.findById(userId);  // ORM handles safety
}
```

**