# Cloud Migration: 6R Assessment Matrix Template

## Purpose

This template provides a systematic framework for evaluating applications and workloads within an existing portfolio to determine the optimal cloud migration strategy, aligning with business objectives, risk appetite, and cost constraints. The analysis is based on Gartner's "6 R's" migration strategies.

## 1. The 6 R's Definition

| Strategy | Description | Typical Effort/Cost | Risk Profile | Target Application Profile |
| :--- | :--- | :--- | :--- | :--- |
| **1. Rehost (Lift and Shift)** | Moving an application exactly as it is (VMs, OS) from on-prem to cloud infrastructure (IaaS). | LOW effort, LOW initial cost | LOW technical risk, HIGH operational debt | Legacy applications with short lifespan, or high volume portfolios needing speed. |
| **2. Replatform (Lift, Tinker, and Shift)** | Moving an application while making minor, cloud-optimizing changes (e.g., replacing a self-managed database with a cloud-managed service like RDS). | MEDIUM effort, MEDIUM cost | MEDIUM risk (testing is critical) | Applications needing immediate operational relief or taking advantage of managed services. |
| **3. Refactor (Rearchitect)** | Modifying the application's code and architecture to fully leverage cloud-native features (e.g., breaking a monolith into microservices, adopting Serverless). | HIGH effort, HIGH cost | HIGH complexity, LOW long-term TCO | Strategic applications with a long lifespan and high demands for scalability, velocity, or resilience. |
| **4. Repurchase (Drop and Shop)** | Moving to a different product, typically switching from a self-hosted solution to a SaaS offering (e.g., replacing an on-prem CRM with Salesforce). | LOW effort, HIGH vendor lock-in risk | LOW technical risk, HIGH data migration risk | Applications where a COTS/SaaS solution meets 80%+ of requirements. |
| **5. Retain (Do Nothing)** | Keeping the application in the current environment (e.g., on-prem) because it is too complex, too costly to move, or recently upgraded. | ZERO effort, HIGH sunk cost | HIGH technical debt, LOW immediate cost | Applications with regulatory dependencies, specialized hardware, or low business value. |
| **6. Retire (Decommission)** | Shutting down applications that are no longer needed or are redundant after analysis. | NEGATIVE cost (savings generated) | LOW risk | Applications with low or zero usage, or duplicate functionality. |

## 2. Application Assessment Criteria and Scoring

For each application in the portfolio, assign a score (1-5) based on the criteria below. The calculated total score will inform the recommended "R" strategy.

| Criterion | Score (1-5) | Description (5 = High/Good, 1 = Low/Bad) | Weight (1-5) | Justification/Notes |
| :--- | :--- | :--- | :--- | :--- |
| **Business Value (BV)** | [1-5] | Value derived from this application (5=Critical, 1=Low/Obsolete). | **5** | |
| **Technical Complexity (TC)** | [1-5] | Difficulty of codebase/infrastructure (5=Modern/Easy, 1=Legacy/Monolithic). | **4** | |
| **Cloud Readiness (CR)** | [1-5] | Alignment with cloud standards (e.g., stateless, containerized). | **3** | |
| **Compliance/Regulatory Burden (CB)** | [1-5] | Sensitivity of data, specific compliance needs (5=Low/Standard, 1=High/Unique). | **5** | |
| **Target Lifespan (TL)** | [1-5] | Expected remaining life of the application (5= >5 years, 1= <1 year). | **3** | |
| **Total Weight** | - | - | **[Sum Weights]** | |

## 3. Migration Strategy Calculation Matrix

Use the Application Assessment Scores (BV, TC, CR, CB, TL) to drive the recommended R. This calculation should be customized based on enterprise priorities.

| R Strategy | Input Score Focus | Calculation Logic (Example) | Recommended Profile |
| :--- | :--- | :--- | :--- |
| **Rehost** | High BV, Low CR, Short TL | **IF** (TC < 3 **AND** TL < 3) **OR** (CR < 2 **AND** BV > 3) | Quick moves for short-term value. |
| **Replatform**| High BV, Medium CR, Medium TL | **IF** (CR > 2 **AND** CR < 4) **AND** (BV > 3) | Balanced approach; quick wins with some optimization. |
| **Refactor** | High BV, Long TL, Low TC tolerance | **IF** (BV = 5 **AND** TL = 5) **AND** (CR > 3) | Strategic investment in modernizing core assets. |
| **Repurchase**| Low TC, Medium CR, High BV | **IF** (TC < 3 **AND** BV > 4) **AND** SaaS alternative exists | Replacement is better than fixing or moving. |
| **Retire** | Low BV, Low TL | **IF** (BV < 2 **OR** TL < 2) | Decommissioning is the most financially sensible move. |

## 4. Application Portfolio Assessment Table (Output Structure)

This table should be the final output populated by the LLM after analyzing the input application data.

| Application Name | Business Owner | Current Environment | Assessment (BV/TC/CR) | Calculated Score | Recommended R | Migration Rationale | Estimated Effort (Wks) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Core Billing System | Finance | On-prem Data Center | 5 / 2 / 1 | [Score] | Refactor | Strategic asset requiring modernization for global scale. | 52 Wks |
| Internal Wiki | IT Ops | Single VM | 2 / 4 / 3 | [Score] | Repurchase | Low business value; move to a standard SaaS documentation tool. | 4 Wks |
| Legacy ETL Engine | Data Team | Private Cloud (vSphere) | 4 / 3 / 4 | [Score] | Replatform | Use a cloud-native ETL service (e.g., AWS Glue) to reduce operational cost. | 24 Wks |

---

With this template, you now have a repeatable, quantifiable methodology for your Cloud Migration Strategy.

The final component for this use case is the primary deliverable: the **Cloud Migration Strategy Report**. Would you like me to generate the template for the `cloud-migration-report.md` next?