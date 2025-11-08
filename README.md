# Enterprise Architecture System Prompts (EASP)

**Transform your LLM into your expert Enterprise Architect advisor** with professional agents covering architecture decisions, engineering metrics, technology roadmaps, and risk management.

---

## 🎯 What is EASP Content?

It is a collection of **expert AI Assistants** specifically designed for Enterprise Architects and engineering leaders. Each skill embeds proven methodologies and frameworks refined through real-world CTO experience.
As an Enterprise Architect, you face complex decisions, extensive documentation, and in-depth analyses daily. These system prompts are designed to:

- **Accelerate** the production of quality documentation
- **Standardize** decision-making processes and outputs
- **Improve** the consistency of your analyses
- **Free up time** for higher-value strategic activities

Think of it like having an experienced EA advisor available 24/7:

1. **Architecture Decision Record Generator** - Generates structured Architecture Decision Records following consolidated best practices.
2. **Architecture Documentation Generator** - Creates technical documentation (C4 Model, architectural views) from specifications or conversations.
3. **Technology Assessment** - Compares technologies, frameworks, and patterns with multi-dimensional analysis.
4. **Architectural review** - Reviews architectural designs, identifying risks, anti-patterns, and opportunities for improvement.
5. **Cloud Migration Strategy Planner** - Design a comprehensive, risk-mitigated strategy for migrating from on-premises to a target cloud environment.

TO DO LIST:

- **Architecture Documentation Generator**: to complete examples
- **Technology Assessment**: to complete example for framework comparison

## 📂 Repository Structure

Each use case has a dedicated folder with this organization:

```txt
use-case-name/
+-- References/         # Reference materials (templates, frameworks)
+-- Examples/           # Concrete examples of input/output
+-- SystemPrompt.md     # The ready-to-use prompt
```

---

## 🏗️ Architecture Decision Agent

**What it's for**: Make and document critical architectural decisions systematically

**When to use**:

- Evaluating technology choices (databases, frameworks, cloud providers)
- Planning major migrations or refactoring
- Documenting architectural decisions for team alignment
- Assessing and prioritizing technical debt

**What you get**:

- Architecture Decision Records (ADRs) following best practices
- Trade-off analysis with clear criteria and scoring
- Step-by-step migration plans with risk mitigation
- Technical debt assessment with prioritized remediation roadmap

**Covers**:

- Tech stack evaluation (build vs buy, database selection, cloud architecture)
- Architecture patterns (microservices, event-driven, serverless)
- Migration strategies (big bang, strangler fig, phased approach)
- Technical debt quantification and prioritization

---;

## 📐 Architecture Documentation Generator

**What it's for:** Generate comprehensive, stakeholder-specific documentation views (e.g., C4 Model, System Context, Technology Landscape) from raw architectural artifacts or fragmented information. This is the Documentation Multi-Tool.

**When to use:**

- Onboarding a new engineer or architect to a complex system.
- Preparing for a security audit or external review that requires specific views.
- Standardizing the "as-is" state of a legacy system before a modernization project.
- Communicating system boundaries and dependencies to a non-technical audience.

**What you get:**

- System Context Diagram (High-level boundary definition, following C4 model principles).
- Technology/Application Inventory (Categorized list of components, versions, and owners).
- Cross-Cutting Concerns Summary (How security, logging, and observability are implemented).
- Stakeholder-Specific Views (e.g., Security View, Operational Runbook, Business Capability Map).

**Covers:**

- Component and relationship mapping (dependencies).
- Technology lifecycle status (e.g., traffic light assessment).
- Data flows and information security boundaries.
- Alignment of systems to business capabilities.

---

💻 Technology Assessment & Comparison Agent

**What it's for:** Provide objective, multi-dimensional analysis to support informed technology and architecture decisions.

**When to use:**

- Comparing multiple technology alternatives (e.g., React vs Vue, SQL vs NoSQL).
- Evaluating new frameworks, patterns, or architectural approaches.
- Assessing technologies across critical dimensions like Technical Fit, Operational Burden, and Business Alignment.
- Calculating Total Cost of Ownership (TCO) and Cost-Benefit Analysis for a strategic technology choice.

**What you get:**

- Executive Summaries for management, highlighting key benefits and risks.
- Technical Deep Dives for architects, covering detailed analysis across six core dimensions.
- Structured Comparison Matrices with weighted scoring and quantified trade-offs.
- Actionable Recommendations with clear next steps (e.g., POC plans) and confidence levels.

**Covers:**

- Six Core Dimensions: Technical Fit, Maturity & Ecosystem, Operational Considerations, Developer Experience, Business Alignment, and Team & Organization.
- Assessment Frameworks: Technology Radar (Adopt/Trial/Hold), Risk-Value Matrix, and Decision Matrix (Weighted Scoring).
- Key Scenarios: Database Selection, Frontend Frameworks, Cloud Provider comparison, API Style (REST vs GraphQL), and Architecture Pattern comparison.

---

## 🏗️ Architectural Review

---

## ☁️ Cloud Migration Strategy Planner

**What it's for:** Design a comprehensive, risk-mitigated strategy for migrating existing applications and infrastructure from on-premises (or one cloud) to a target cloud environment (e.g., AWS, Azure, GCP).

**When to use:**

- Initiating a new corporate cloud adoption program.
- Planning the migration of a complex, legacy application portfolio.
- Defining the "6 Rs" (Rehost, Replatform, Refactor, etc.) strategy for applications.
- Estimating the effort, cost, and timeline for a large-scale migration wave.

**What you get:**

- Customized Migration Plan aligned with business priorities and constraints.
- Application Portfolio Assessment based on the 6 R's framework.
- Risk Profile and Mitigation Strategy specific to data, network, and application downtime.
- High-Level TCO Projection for the target cloud state.

**Covers:**

- Cloud Provider Selection Rationale (if not already chosen).
- Migration Strategy Definition (e.g., phased vs. large-scale).
- Target Architecture Design (Landing Zone, Network Topology, Security Baseline).
- Data Migration Techniques and Downtime minimization tactics.
- Organizational Change Management (Skills, Governance, and FinOps).

### Example Prompt Directive

When using the `SystemPrompt.md` for Technology Assessment, you must explicitly instruct the LLM to **adhere to this framework**.

> "Analyze Technology X based on the five dimensions in the `scoring-framework.md` provided. **Force your response to use a Score (1-10) and provide a concise justification for each dimension**, even if you need to simulate external research or make assumptions (which must be stated). Use the following weights: Technical Fit: 9, Operational Maturity: 6, Ecosystem & Viability: 7, Security & Compliance: 8, TCO: 5."

---

## 💡 How to use the prompts

### Option 1: Gemini Gems

1. Create a new Gem
2. Copy the content of SystemPrompt.md
3. Upload files from the References/ folder as a knowledge base
4. Save and interact with your personalized assistant

### Option 2: Claude Projects / ChatGPT Custom GPTs

1. Create a new project/GPT
2. Paste the system prompt into the instructions
3. Upload files from the References/ folder as a knowledge base
4. Use the Examples/ to test the behavior

### Option 3: API Integration

Use the prompts directly in your API calls:

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    system=open("use-case/SystemPrompt.md").read(),
    messages=[{"role": "user", "content": "..."}]
)
```

## 🔧 Customizations

The prompts are designed to be modular. You can:

- **Modify** the templates in `References/` to adapt them to your standards
- **Add** specific examples from your domain in `Examples/`
- **Extend** the system prompts with specific corporate constraints

## 📚 Best Practices

1. **Contextualize**: Always provide context about your project/organization
2. **Iterate**: The first outputs are drafts; refine them through dialogue
3. **Verify**: AIs are assistants; the final decision is always yours
4. **Document**: Save useful interactions as new examples

## 🤝 Contributing

Have you created a useful new use case? Do you want to improve an existing prompt?

1. Fork the repository
2. Create your branch (`git checkout -b feature/new-usecase`)
3. Commit your changes (`git commit -m 'Add: new use case'`)
4. Push to the branch (`git push origin feature/new-usecase`)
5. Open a Pull Request

## 📝 Licenses

MIT License - Free to use, modify and distributing these prompts.

## ✉️ Contacts

For questions, suggestions, or discussions:

- Open an Issue on GitHub
- Contribute with a Pull Request

---

**Note:** These prompts are support tools. The experience, judgment, and context knowledge of an Enterprise Architect remain irreplaceable.
