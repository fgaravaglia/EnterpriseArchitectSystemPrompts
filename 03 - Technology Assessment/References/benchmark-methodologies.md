# Benchmark Methodologies for Technology Assessment

A comprehensive guide to properly benchmarking technologies for objective comparison. Poor benchmarks lead to wrong decisions - this guide ensures your benchmarks are meaningful, reproducible, and actionable.

---

## Core Principles

### 1. Representative Workloads
Benchmark what you'll actually do in production, not toy examples.

❌ **Bad**: "SELECT * FROM users LIMIT 100"  
✅ **Good**: "SELECT u.*, COUNT(o.id) FROM users u LEFT JOIN orders o WHERE u.region = 'US' GROUP BY u.id"

### 2. Realistic Data
Use production-scale data with realistic distributions.

❌ **Bad**: 1000 rows of sequential IDs  
✅ **Good**: 10M rows with production-like distribution (hotspots, skew)

### 3. Environment Parity
Test in conditions similar to production.

❌ **Bad**: Localhost with 8GB RAM  
✅ **Good**: AWS instance matching production spec with network latency

### 4. Statistical Rigor
Measure multiple times, report distributions (not just averages).

❌ **Bad**: "It took 50ms"  
✅ **Good**: "p50: 45ms, p95: 78ms, p99: 125ms (n=10,000 requests)"

### 5. Isolate Variables
Change one thing at a time to understand cause and effect.

❌ **Bad**: Compare PostgreSQL on bare metal vs MongoDB in Docker  
✅ **Good**: Both in Docker with same resource limits, or both on bare metal

---

## Benchmark Types

### 1. Microbenchmarks (Component Level)

**Purpose**: Measure specific capabilities in isolation

**Examples**:
- Database: Single query latency
- API: HTTP request/response time
- Framework: Component render time
- Algorithm: Sort performance on N elements

**When to Use**:
- Understanding specific bottlenecks
- Validating vendor claims
- Comparing narrow functionality

**Limitations**:
- Doesn't represent real usage
- Easy to optimize for the benchmark
- May not reflect system integration

**Example: Database Read Latency**
```bash
# PostgreSQL
pgbench -c 10 -j 2 -t 10000 -S mydb

# MongoDB
mongoperf <<EOF
{
  nThreads: 10,
  fileSizeMB: 1000,
  r: true
}
EOF
```

---

### 2. Macrobenchmarks (System Level)

**Purpose**: Measure realistic end-to-end workflows

**Examples**:
- E-commerce: Full checkout flow (browse → cart → payment → confirmation)
- API: Complete CRUD operations sequence
- Web app: User journey with multiple interactions

**When to Use**:
- Validating system-level performance
- Understanding integration overhead
- Estimating real user experience

**Example: E-commerce Checkout Flow**
```javascript
// Using k6 load testing
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function() {
  // Browse products
  let browse = http.get('https://api.example.com/products?category=electronics');
  check(browse, { 'browse status 200': (r) => r.status === 200 });
  
  // Add to cart
  let cart = http.post('https://api.example.com/cart', JSON.stringify({
    productId: '12345',
    quantity: 1
  }));
  check(cart, { 'cart status 200': (r) => r.status === 200 });
  
  // Checkout
  let checkout = http.post('https://api.example.com/checkout', JSON.stringify({
    paymentMethod: 'credit_card'
  }));
  check(checkout, { 'checkout status 200': (r) => r.status === 200 });
  
  sleep(1);
}
```

---

### 3. Load Testing (Capacity)

**Purpose**: Determine system limits and behavior under stress

**Metrics**:
- Maximum throughput (requests/sec)
- Latency degradation under load
- Error rate at various loads
- Resource utilization (CPU, memory, network)

**Load Patterns**:
1. **Constant Load**: Steady rate for sustained period
2. **Ramp Up**: Gradually increase load
3. **Spike**: Sudden traffic increase
4. **Step**: Incremental increases with plateaus

**Example: Ramp-Up Load Test**
```yaml
# k6 configuration
export let options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 200 },  // Ramp to 200 users
    { duration: '5m', target: 200 },  // Stay at 200
    { duration: '2m', target: 500 },  // Ramp to 500
    { duration: '5m', target: 500 },  // Stay at 500
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500'], // 95% requests under 500ms
    'http_req_failed': ['rate<0.01'],   // Error rate under 1%
  }
};
```

---

### 4. Stress Testing (Breaking Point)

**Purpose**: Find system limits and failure modes

**Goals**:
- Identify maximum capacity
- Understand failure behavior
- Test recovery mechanisms
- Validate error handling

**Method**:
1. Start with expected load
2. Incrementally increase until failure
3. Document breaking point and failure mode
4. Test recovery (how does it come back?)

**Example Failure Modes**:
- Gradual degradation (latency increases)
- Sudden collapse (service stops responding)
- Cascading failures (one component fails → others follow)
- Memory exhaustion (OOM kills)
- Database connection pool exhaustion

---

### 5. Soak Testing (Endurance)

**Purpose**: Validate stability over extended periods

**Duration**: Hours to days (typically 24-72 hours)

**What to Monitor**:
- Memory leaks (gradual memory increase)
- Connection leaks (growing connection count)
- Disk space (log files, temp files)
- Performance degradation over time
- Resource exhaustion

**Example: 24-Hour Soak Test**
```bash
# Run constant load for 24 hours
k6 run --duration 24h --vus 50 soak-test.js

# Monitor during test
watch -n 60 'docker stats'
watch -n 60 'df -h'
watch -n 60 'ss -s'  # Socket statistics
```

---

## Database Benchmarking

### Common Database Workloads

#### 1. OLTP (Online Transaction Processing)
**Characteristics**: Many small read/write transactions

**TPC-C Benchmark**:
- Order entry simulation
- Mix of reads and writes
- ACID transaction requirements
- Industry standard

**Tool**: [Sysbench](https://github.com/akopytov/sysbench)

```bash
# Prepare data
sysbench oltp_read_write \
  --mysql-host=localhost \
  --mysql-user=test \
  --mysql-password=test \
  --mysql-db=sbtest \
  --tables=10 \
  --table-size=1000000 \
  prepare

# Run benchmark
sysbench oltp_read_write \
  --mysql-host=localhost \
  --mysql-user=test \
  --mysql-password=test \
  --mysql-db=sbtest \
  --tables=10 \
  --table-size=1000000 \
  --threads=64 \
  --time=300 \
  --report-interval=10 \
  run
```

#### 2. OLAP (Online Analytical Processing)
**Characteristics**: Complex queries, large data scans

**TPC-H Benchmark**:
- Business intelligence queries
- Aggregations, joins, sorting
- Decision support workload

**Queries to Test**:
- Full table scans with aggregation
- Multi-table joins (3+ tables)
- Subqueries and CTEs
- Window functions
- GROUP BY with HAVING

#### 3. Mixed Workload
**Real-world**: Combination of OLTP and OLAP

**Ratio Example**:
- 70% simple reads (key lookups)
- 20% writes (inserts, updates)
- 10% complex queries (analytics)

### Database-Specific Benchmarks

#### PostgreSQL
**pgbench**: Built-in benchmark tool

```bash
# Initialize test database
pgbench -i -s 100 testdb  # Scale factor 100

# Read-only test
pgbench -c 10 -j 2 -T 60 -S testdb

# Read-write test
pgbench -c 10 -j 2 -T 60 testdb

# Custom script
pgbench -c 10 -j 2 -T 60 -f custom_queries.sql testdb
```

**Key Metrics**:
- TPS (transactions per second)
- Latency (average, p95, p99)
- Connection time
- Deadlocks

#### MongoDB
**YCSB** (Yahoo! Cloud Serving Benchmark)

```bash
# Load data
./bin/ycsb load mongodb -s \
  -P workloads/workloada \
  -p mongodb.url=mongodb://localhost:27017/ycsb

# Run workload A (50% reads, 50% updates)
./bin/ycsb run mongodb -s \
  -P workloads/workloada \
  -p mongodb.url=mongodb://localhost:27017/ycsb \
  -threads 16
```

**Workload Types**:
- **Workload A**: Update heavy (50% reads, 50% updates)
- **Workload B**: Read heavy (95% reads, 5% updates)
- **Workload C**: Read only
- **Workload D**: Read latest (95% reads, 5% inserts)
- **Workload E**: Scan heavy (95% scans, 5% inserts)
- **Workload F**: Read-modify-write

#### Redis
**redis-benchmark**: Built-in tool

```bash
# Basic benchmark
redis-benchmark -h localhost -p 6379 -n 100000

# Specific commands
redis-benchmark -t set,get -n 100000 -q

# Pipeline testing
redis-benchmark -t set,get -n 100000 -P 16

# Specific key size
redis-benchmark -t set -n 100000 -d 1024  # 1KB values
```

---

## API Benchmarking

### REST API Testing

**Tools**:
- **k6**: Modern load testing (JavaScript)
- **Apache JMeter**: Java-based, GUI available
- **Gatling**: Scala-based, developer-friendly
- **wrk**: Lightweight, C-based
- **hey**: Simple Go-based tool

#### k6 Example (Recommended)

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export let options = {
  stages: [
    { duration: '1m', target: 50 },
    { duration: '3m', target: 50 },
    { duration: '1m', target: 100 },
    { duration: '3m', target: 100 },
    { duration: '1m', target: 0 },
  ],
  thresholds: {
    'http_req_duration': ['p(95)<500', 'p(99)<1000'],
    'errors': ['rate<0.1'],
  },
};

export default function() {
  // Test multiple endpoints
  let responses = http.batch([
    ['GET', 'https://api.example.com/users/123'],
    ['GET', 'https://api.example.com/products?limit=20'],
    ['POST', 'https://api.example.com/orders', JSON.stringify({
      productId: '456',
      quantity: 2
    }), { headers: { 'Content-Type': 'application/json' }}],
  ]);

  responses.forEach(response => {
    const success = check(response, {
      'status is 200': (r) => r.status === 200,
      'response time OK': (r) => r.timings.duration < 500,
    });
    
    errorRate.add(!success);
  });

  sleep(1);
}
```

#### wrk for Quick Tests

```bash
# Simple GET test
wrk -t4 -c100 -d30s https://api.example.com/users

# POST with body
wrk -t4 -c100 -d30s -s post.lua https://api.example.com/orders

# post.lua
wrk.method = "POST"
wrk.body = '{"productId": "123", "quantity": 2}'
wrk.headers["Content-Type"] = "application/json"
```

### GraphQL API Testing

**Challenges**:
- Query complexity varies
- N+1 query problem
- Resolver performance

**Strategy**:
1. Test individual queries (simple → complex)
2. Test typical query combinations
3. Test nested queries at various depths
4. Measure query complexity vs performance

**Example**:
```javascript
// k6 GraphQL test
import http from 'k6/http';

const query = `
  query GetUserWithOrders($userId: ID!) {
    user(id: $userId) {
      id
      name
      orders(last: 10) {
        edges {
          node {
            id
            total
            items {
              id
              name
              price
            }
          }
        }
      }
    }
  }
`;

export default function() {
  const response = http.post('https://api.example.com/graphql', JSON.stringify({
    query: query,
    variables: { userId: '123' }
  }), {
    headers: { 'Content-Type': 'application/json' }
  });
  
  check(response, {
    'is status 200': (r) => r.status === 200,
    'no errors': (r) => !JSON.parse(r.body).errors,
  });
}
```

---

## Frontend Framework Benchmarking

### Metrics to Measure

1. **Initial Load Time**: Time to interactive (TTI)
2. **Bundle Size**: JavaScript size transferred
3. **Runtime Performance**: Component render time
4. **Memory Usage**: Heap size over time
5. **Build Time**: Development and production builds

### Tools

#### Lighthouse (Chrome)
```bash
# CLI usage
lighthouse https://example.com --output html --output-path report.html

# Key metrics
# - First Contentful Paint (FCP)
# - Largest Contentful Paint (LCP)
# - Time to Interactive (TTI)
# - Total Blocking Time (TBT)
# - Cumulative Layout Shift (CLS)
```

#### WebPageTest
- Real browser testing
- Multiple locations
- Filmstrip view
- Waterfall analysis

**URL**: https://www.webpagetest.org/

#### Bundlephobia
Check npm package sizes: https://bundlephobia.com/

#### Chrome DevTools Performance

```javascript
// React example - measure component render
import { Profiler } from 'react';

function onRenderCallback(
  id, phase, actualDuration, baseDuration, startTime, commitTime
) {
  console.log(`${id}'s ${phase} phase:`);
  console.log(`Actual time: ${actualDuration}ms`);
  console.log(`Base time: ${baseDuration}ms`);
}

<Profiler id="MyComponent" onRender={onRenderCallback}>
  <MyComponent />
</Profiler>
```

### JavaScript Benchmark Example

```javascript
// Benchmark component render performance
import { render } from '@testing-library/react';
import { performance } from 'perf_hooks';

function benchmarkRender(Component, iterations = 1000) {
  const times = [];
  
  for (let i = 0; i < iterations; i++) {
    const start = performance.now();
    const { unmount } = render(<Component />);
    const end = performance.now();
    
    times.push(end - start);
    unmount();
  }
  
  times.sort((a, b) => a - b);
  
  return {
    mean: times.reduce((a, b) => a + b) / times.length,
    p50: times[Math.floor(times.length * 0.5)],
    p95: times[Math.floor(times.length * 0.95)],
    p99: times[Math.floor(times.length * 0.99)],
    min: times[0],
    max: times[times.length - 1]
  };
}

const results = benchmarkRender(MyComponent);
console.log(`Mean: ${results.mean.toFixed(2)}ms`);
console.log(`p95: ${results.p95.toFixed(2)}ms`);
```

---

## Cloud Provider Benchmarking

### Compute Performance

**Methodology**:
1. Provision identical VM specs across providers
2. Run CPU-intensive benchmark (e.g., Geekbench, sysbench)
3. Run memory bandwidth test
4. Run disk I/O test
5. Compare results normalized by cost

**Example: CPU Benchmark**
```bash
# Sysbench CPU test
sysbench cpu --cpu-max-prime=20000 --threads=4 run

# Measure
# - Events per second
# - Latency (min, avg, max)
# - Compare across providers
```

### Network Performance

**Metrics**:
- Bandwidth (Gbps)
- Latency (ms)
- Packet loss (%)
- Jitter (ms)

**Tools**:
- **iperf3**: Network bandwidth
- **ping**: Latency
- **mtr**: Network diagnostics

**Example: Cross-Region Latency**
```bash
# Setup iperf3 server on VM1
iperf3 -s

# Run client on VM2
iperf3 -c <server-ip> -t 60 -i 10

# Measure latency
ping -c 100 <server-ip>

# Results to compare
# - Throughput (Mbits/sec)
# - Latency (ms)
# - Retransmits
```

### Storage Performance

**Tests**:
1. Sequential read/write
2. Random read/write (4K blocks)
3. Mixed workload (70% read, 30% write)
4. IOPS (I/O operations per second)

**Tool: fio (Flexible I/O Tester)**

```bash
# Random read test
fio --name=random-read \
    --ioengine=libaio \
    --iodepth=16 \
    --rw=randread \
    --bs=4k \
    --direct=1 \
    --size=1G \
    --numjobs=4 \
    --runtime=60 \
    --group_reporting

# Sequential write test
fio --name=seq-write \
    --ioengine=libaio \
    --iodepth=16 \
    --rw=write \
    --bs=1M \
    --direct=1 \
    --size=1G \
    --numjobs=1 \
    --runtime=60 \
    --group_reporting
```

---

## Common Pitfalls & How to Avoid Them

### Pitfall 1: Cold Start vs Warm Cache

**Problem**: First request much slower than subsequent

**Solution**: 
- Warm up system before measuring
- Run 1000 requests, then start measuring
- Report both cold and warm performance separately

```javascript
// Correct approach
async function benchmark() {
  // Warmup
  for (let i = 0; i < 1000; i++) {
    await makeRequest();
  }
  
  // Actual measurement
  const times = [];
  for (let i = 0; i < 10000; i++) {
    const start = Date.now();
    await makeRequest();
    times.push(Date.now() - start);
  }
  
  return calculateStats(times);
}
```

### Pitfall 2: Coordinated Omission

**Problem**: Not accounting for requests that couldn't start due to system being saturated

**Example**:
- System can handle 100 req/s
- You send 200 req/s
- 100 requests wait in queue
- You only measure the 100 that completed (selection bias!)

**Solution**: Use proper load testing tools (k6, Gatling) that account for this

### Pitfall 3: Reporting Only Averages

**Problem**: Averages hide outliers and distribution

**Solution**: Always report percentiles

```
❌ Bad: "Average latency: 50ms"
   (Could be 49ms for 99% and 5000ms for 1%)

✅ Good: 
   - p50: 45ms (median)
   - p95: 78ms
   - p99: 125ms
   - p99.9: 450ms
   - max: 2500ms
```

### Pitfall 4: Insufficient Sample Size

**Problem**: Too few measurements = unreliable results

**Solution**:
- Minimum 1,000 samples for meaningful percentiles
- 10,000+ for p99, p99.9
- Run test multiple times, check consistency

### Pitfall 5: Benchmarking on Developer Laptop

**Problem**: Not representative of production

**Solution**:
- Use environment matching production specs
- Account for network latency (localhost has none)
- Consider noisy neighbors (cloud VMs)
- Test during different times of day

### Pitfall 6: Not Controlling Variables

**Problem**: Comparing apples to oranges

**Example Issues**:
- Different hardware specs
- Different data volumes
- Different network conditions
- Different configurations

**Solution**: Change ONE variable at a time

### Pitfall 7: Vendor Benchmarks

**Problem**: Vendor-provided benchmarks often optimized for the benchmark, not real use

**Solution**:
- Always run your own benchmarks
- Use your actual workload
- Be skeptical of marketing claims
- Look for independent third-party benchmarks

### Pitfall 8: Ignoring Resource Utilization

**Problem**: Fast performance but at 100% CPU = will not scale

**Solution**: Monitor during benchmarks
```bash
# CPU, Memory, Disk I/O
top
htop
iostat -x 5

# Network
iftop
nethogs

# All-in-one
dstat --time --cpu --mem --net --disk 5
```

---

## Benchmark Reporting Template

### Executive Summary

```markdown
## Benchmark Results: [Technology A] vs [Technology B]

**Winner**: [Technology A] for [specific use case]

**Key Findings**:
- Technology A is 35% faster at p95 latency (120ms vs 185ms)
- Technology B handles 2x throughput (10K req/s vs 5K req/s)
- Technology A uses 40% less memory (2GB vs 3.3GB)

**Recommendation**: [Technology A] for our latency-sensitive use case

**Confidence**: High (benchmarked on production-like environment)
```

### Detailed Results

```markdown
## Methodology

**Environment**:
- AWS EC2 c5.2xlarge (8 vCPU, 16GB RAM)
- Same instance type for both technologies
- Same region (us-east-1)
- Tested on [date]

**Workload**:
- Mixed: 70% reads, 20% writes, 10% complex queries
- Dataset: 10M records, 50GB total
- Duration: 30 minutes per test
- Concurrent users: 100

**Tools**: k6 (load testing), Prometheus (metrics), Grafana (visualization)

## Results

### Latency (ms)

| Metric | Tech A | Tech B | Winner |
|--------|--------|--------|--------|
| p50 | 45 | 52 | Tech A (-13%) |
| p95 | 120 | 185 | Tech A (-35%) |
| p99 | 280 | 520 | Tech A (-46%) |
| p99.9 | 890 | 1,250 | Tech A (-29%) |

### Throughput

| Metric | Tech A | Tech B | Winner |
|--------|--------|--------|--------|
| Max RPS | 5,200 | 10,400 | Tech B (+100%) |
| Sustained RPS | 4,800 | 9,200 | Tech B (+92%) |

### Resource Usage (at 5K RPS)

| Metric | Tech A | Tech B | Winner |
|--------|--------|--------|--------|
| CPU % | 65% | 72% | Tech A |
| Memory GB | 2.1 | 3.3 | Tech A (-36%) |
| Disk I/O MB/s | 45 | 38 | Tech B |
| Network MB/s | 120 | 115 | Tech B |

### Error Rate

| Load Level | Tech A | Tech B |
|------------|--------|--------|
| 1K RPS | 0.01% | 0.01% |
| 5K RPS | 0.05% | 0.03% |
| 10K RPS | 2.3% | 0.15% |
| 15K RPS | 15% | 1.8% |

## Analysis

**Tech A Strengths**:
- Superior latency at all percentiles
- Lower resource usage (better cost efficiency)
- Simpler configuration

**Tech A Weaknesses**:
- Lower maximum throughput
- Errors increase sharply above 10K RPS

**Tech B Strengths**:
- 2x throughput capacity
- Maintains low error rate at high load
- Scales more predictably

**Tech B Weaknesses**:
- Higher latency, especially at tail (p99)
- Uses more memory
- More complex configuration

## Recommendation

For our use case (latency-sensitive, 5K RPS sustained load):
**Technology A** is recommended.

**Rationale**:
- Our SLA is p95 < 150ms (Tech A: 120ms ✅, Tech B: 185ms ❌)
- Current load is 3K RPS, projection is 8K RPS in 2 years (Tech A can handle)
- Lower resource usage = 30% cost savings
- Team has Tech A expertise

**When Tech B would be better**:
- If throughput requirements exceed 10K RPS
- If tail latency (p99) is less critical than throughput
- If we need to handle traffic spikes > 15K RPS

## Appendix

[Include]:
- Raw data (CSV)
- Grafana screenshots
- Configuration files used
- Reproduction steps
```

---

## Continuous Benchmarking

### Why Continuous?

- Detect performance regressions early
- Track improvements over time
- Validate optimization efforts
- Prevent performance debt

### Setup

**1. Automated Benchmarks in CI**
```yaml
# GitHub Actions example
name: Performance Benchmark

on:
  pull_request:
    branches: [ main ]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run benchmarks
        run: npm run benchmark
      
      - name: Store benchmark result
        uses: benchmark-action/github-action-benchmark@v1
        with:
          tool: 'benchmarkjs'
          output-file-path: output.txt
          
      - name: Comment PR with results
        uses: actions/github-script@v5
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'Performance impact: [results here]'
            })
```

**2. Performance Budgets**
```json
// performance-budget.json
{
  "latency_p95_ms": 200,
  "throughput_rps": 5000,
  "memory_mb": 2048,
  "error_rate_percent": 0.1
}
```

**3. Fail CI if Budget Exceeded**
```javascript
// check-performance.js
const results = require('./benchmark-results.json');
const budget = require('./performance-budget.json');

if (results.latency_p95 > budget.latency_p95_ms) {
  console.error(`p95 latency ${results.latency_p95}ms exceeds budget ${budget.latency_p95_ms}ms`);
  process.exit(1);
}
```

---

## References & Tools

### Load Testing Tools
- [k6](https://k6.io/) - Modern, developer-friendly
- [Apache JMeter](https://jmeter.apache.org/) - Feature-rich, GUI
- [Gatling](https://gatling.io/) - Scala-based, excellent reports
- [Locust](https://locust.io/) - Python-based, distributed
- [wrk](https://github.com/wg/wrk) - Lightweight, fast

### Database Benchmarks
- [Sysbench](https://github.com/akopytov/sysbench) - Multi-threaded benchmark
- [YCSB](https://github.com/brianfrankcooper/YCSB) - NoSQL benchmark
- [pgbench](https://www.postgresql.org/docs/current/pgbench.html) - PostgreSQL
- [redis-benchmark](https://redis.io/topics/benchmarks) - Redis

### Web Performance
- [Lighthouse](https://developers.google.com/web/tools/lighthouse) - Chrome DevTools
- [WebPageTest](https://www.webpagetest.org/) - Real browser testing
- [Speedcurve](https://speedcurve.com/) - Continuous monitoring

### System Benchmarks
- [Geekbench](https://www.geekbench.com/) - Cross-platform CPU/GPU
- [fio](https://fio.readthedocs.io/) - Flexible I/O tester
- [iperf3](https://iperf.fr/) - Network bandwidth

### Methodology References
- [How NOT to Measure Latency](https://www.youtube.com/watch?v=lJ8ydIuPFeU) - Gil Tene
- [Coordinated Omission](http://highscalability.com/blog/2015/10/5/your-load-generator-is-probably-lying-to-you-take-the-red-p.html)
- [Performance Testing Guidance](https://docs.microsoft.com/en-us/azure/architecture/antipatterns/no-caching/)

---

## Quick Reference Checklist

Before running benchmarks:
- [ ] Define clear goals and metrics
- [ ] Use production-like environment
- [ ] Prepare realistic data (scale and distribution)
- [ ] Warm up system before measuring
- [ ] Control all variables except what you're testing
- [ ] Run multiple times for statistical significance
- [ ] Monitor resource utilization during test

When analyzing results:
- [ ] Report percentiles (p50, p95, p99), not just averages
- [ ] Include sample size (n=X)
- [ ] Document methodology and environment
- [ ] Show error bars / confidence intervals
- [ ] Compare against baseline or previous results
- [ ] Consider cost per unit of performance

When reporting:
- [ ] Executive summary for decision makers
- [ ] Detailed data for engineers
- [ ] Clear winner with context ("for our use case")
- [ ] Acknowledge limitations and caveats
- [ ] Provide reproduction steps