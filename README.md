# Enterprise Architecture System (EAS)

**Accelerating Digital Strategy Through Automated Intelligence:** Traditional Enterprise Architecture is often perceived as a bottleneck. EAS is an open-source framework designed to transform Large Language Models (LLMs) into expert architectural assistants capable of orchestrating complex decisions, technical documentation, and risk analysis in a fraction of the standard time.

## Strategic Value Proposition

In a technological landscape moving at the speed of AI, consistency in decision-making is the only sustainable competitive advantage. EAS applies proven methodologies (C4 Model, 6R Framework, ADR) to:

- Reduce by 70% the time spent on repetitive technical documentation.
- Standardize Decision-Making by eliminating cognitive biases in technology selection.
- Mitigate Structural Risk by identifying anti-patterns before they evolve into legacy technical debt

---

## 🎯 Framework Architecture: The 5 Core Pillars

EAS is a collection of **expert AI Assistants** specifically designed for Enterprise Architects and engineering leaders. Each skill embeds proven methodologies and frameworks refined through real-world CTO experience.
Each agent in this repository is engineered to handle a critical phase of the architecture lifecycle. They are designed to:

- **Accelerate** the production of quality documentation
- **Standardize** decision-making processes and outputs
- **Improve** the consistency of your analyses
- **Free up time** for higher-value strategic activities

Think of it like having an experienced EA advisor available 24/7:

| Skill                            | Strategic Function            | Business Impact               |
|----------------------------------|-------------------------------|-------------------------------|
| **Architecture Decision Skill**  | Systematic decision logging.  | Improves traceability by reducing drafting time through pre-validated templates.  |
| **Documentation Generation**     | C4 Model & Context views.     | Accelerates onboarding by 40% synthesizing fragmented info into coherent diagrams.|
| **Technology Assessment**        | Multi-dimensional analysis.   | Optimizes TCO ensuring business alignment via weighted scoring matrices.          |
| **Architectural Review**         | System & Microservices audit. | Lowers refactoring costs identifying "God Services" before they hit production.   |
| **Cloud Migration Planner**      | 6 Rs Migration Strategy.      | Minimizes migration risk defining roadmaps based on criticality and impact analysis. |

---

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

## 💻 Technology Assessment & Comparison Agent

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

**What it's for:** Conduct comprehensive, structured reviews of existing or proposed architectures to identify risks, anti-patterns, and improvement opportunities before issues reach production.

**When to use:**

- Reviewing greenfield system designs before development starts.
- Validating microservices architectures for distributed monolith symptoms or improper boundaries.
- Assessing production readiness before launch (go/no-go decisions).
- Evaluating legacy systems for modernization opportunities.
- Conducting security architecture reviews and threat validation.
- Performing post-launch architecture health checks.

**What you get:**

- Executive Summaries for leadership with Red/Yellow/Green status and critical issues prioritized.
- Detailed Technical Reviews for architects and developers with findings across 9 dimensions and specific remediation plans.
- Prioritized Issue Lists with severity classification (Critical/High/Medium/Low) and effort estimates.
- Actionable Recommendations with code examples, alternatives, and clear next steps with ownership.

**Covers:**

- Multi-Dimensions analysis
- Quality Gates: Five progressive checkpoints from Conceptual Design through Post-Launch Review.
- Anti-Pattern Detection: Distributed Monolith, God Services, Chatty APIs, Shared Mutable State, and 20+ common architectural smells.
- Key Scenarios: New system design, Microservices evaluation, Cloud migration, API design, Security review, Legacy modernization, Performance optimization.

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

## 💡 Deployment & Integration

EAS is LLM-agnostic and designed to work with Gemini, Claude, ChatGpt, and other herness tools.

### 📂 Repository Structure

Each use case has a dedicated folder with this organization:

```txt
use-case-name/
+-- references/         # Methodological standards and templates (the Agent's specialized knowledge).
+-- examples/           # Real-world input/output scenarios to ensure consistency and quality.
+-- SKILL.md            # The core behavioral logic to be injected into your LLM.
```

### Integration Options

- Personalized Assistants: Use the prompts to create dedicated "Gems" (Gemini), "Projects" (Claude), or "Custom GPTs" (OpenAI).
- API Integration: Inject the system prompts directly into your automated CI/CD or documentation pipelines.

## 📚 Validation & Safety (The Expert View)

AI is a high-speed accelerator, not a replacement for professional judgment. To ensure architectural integrity:

- Context is King: Always provide specific corporate constraints (budget, stack, compliance).
- Audit the Output: Treat every AI-generated artifact as an "Advanced Draft" requiring senior sign-off.
- Security First: Ensure no sensitive production credentials or PII are shared during the prompting process.

## 📝 Licenses & Contributing

Released under the MIT License. This framework is a living asset. Contributions regarding new architectural patterns (e.g., FinOps, AI Governance, Event-Driven Design) are encouraged via Pull Request.
Have you created a useful new use case? Do you want to improve an existing prompt?

1. Fork the repository
2. Create your branch (`git checkout -b feature/new-usecase`)
3. Commit your changes (`git commit -m 'Add: new use case'`)
4. Push to the branch (`git push origin feature/new-usecase`)
5. Open a Pull Request

**Connect & Explore:** For deep dives into modern digital architectures and IT strategy, visit [Modern Digital Architectures.](https://francescogaravaglia.substack.com/)

Maintained by Francesco Garavaglia - Transforming IT into a growth engine.

## ✉️ Contacts

For questions, suggestions, or discussions:

- Open an Issue on GitHub
- Contribute with a Pull Request

---

**Note:** These prompts are support tools. The experience, judgment, and context knowledge of an Enterprise Architect remain irreplaceable.
