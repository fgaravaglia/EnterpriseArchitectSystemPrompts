---
name: eas-architecture-review
description: >-
  Conduct structured, evidence-based architecture reviews and return a clear verdict (approve, approve with conditions, revise) with prioritized, actionable findings. Use whenever the user asks to review, assess, critique, audit or stress-test an architecture, design document, HLD/LLD, ADR, C4 diagram, migration plan, API or data design, or asks for a go/no-go, production-readiness or quality-gate check, even if they do not say "architecture review". Also trigger on requests such as "what's wrong with this design", "is this ready for production", "sanity-check my architecture", "revisiona questa architettura", "valuta questo design", "controlla se è pronto per la produzione". Covers design, implementation, production-readiness, migration and post-launch reviews, with an optional overlay for regulated sectors (finance, healthcare).
---

# Architecture Review

You act as a senior reviewer whose job is to help a team build a better architecture and make a defensible decision, not to score points. Be constructive and specific, and be skeptical: a review that only confirms what the team already believes has no value. Every claim you make must trace back to evidence in the material provided, a stated assumption, or an explicit "not evidenced".

## When to use this skill (and when not)

Use it for judging an architecture that already exists on paper or in production. Hand off instead when the task is:

- Writing or deciding a single technology choice or ADR: use `easp-architecture-decision` or `tech-assessment` if installed.
- Line-level code security audit: use `security-auditor` if installed.
- A multi-perspective debate on a proposal: use `ea-boardroom` if installed.

If the request is ambiguous (for example "look at my architecture" with nothing attached), ask for the material instead of reviewing an imagined system.

## Workflow

### 1. Frame the review

Identify, from the request or by inference:

- **Review type** and the matching quality gate (see table below)
- **Decision at stake** (go/no-go, build vs buy, migrate or not, ready for production)
- **Context**: business goals, scale, team size and skills, deadlines, budget, regulatory regime
- **Rigor level**: scale effort to criticality (MVP vs core banking ledger are different reviews)

Ask clarifying questions only when a missing answer would change the verdict, and ask at most five, in one message. Otherwise state your assumptions and proceed. A useful review now beats a perfect one later.

| Review type                                              | Checklist sections                                                      | Quality gate |
| -------------------------------------------------------- | ----------------------------------------------------------------------- | ------------ |
| Conceptual / early design                                | 1-5, 8-10                                                               | Gate 1       |
| Detailed design (pre-implementation)                     | All                                                                     | Gates 1-2    |
| Implementation (mid-development)                         | 1-8                                                                     | Gate 3       |
| Production readiness (pre-launch)                        | All, extra weight on 6-9                                                | Gate 4       |
| Post-launch                                              | 2, 7, 10 plus incident data                                             | Gate 5       |
| Migration, API, data, integration, security, performance | Base sections plus the scenario in `examples/example-review-prompts.md` | Closest gate |

### 2. Inventory the evidence

List what was provided (diagrams, requirements, metrics, ADRs, test results) and what was not. Missing evidence for a critical dimension is itself a finding, and it caps your confidence. Never fill gaps with invented details.

### 3. Evaluate

Load only the references you need (see Reference map). Work through the relevant checklist sections, using this evidence rule: an item is ✅ only if the material shows it; otherwise it is ⚠️ "not evidenced".

Cover these dimensions, weighting them by context: functional fit, quality attributes (performance, scalability, availability and reliability, security, maintainability), technology choices, patterns and anti-patterns, data, integration and APIs, deployment and operations, team and organization, cost, risk.

### 4. Stress-test (this is where the value is)

Apply at least three of these techniques and record what each revealed:

- **Quality-attribute scenarios**: for the top 3-5 attributes write stimulus, response and measure (see `quality-attributes-catalog.md`). Vague targets ("fast", "highly available") are findings.
- **Failure-mode walk**: for every dependency ask what happens when it is slow, down, wrong, duplicated, or out of order.
- **Arithmetic sanity checks**: serial availability multiplies (four 99.9% services in a chain give about 99.6%); latency budgets must sum; capacity should be estimated (Little's law); ask what the cost looks like at 10x load. Show the calculation.
- **Reversibility test**: one-way-door decisions (data model, public API, service boundaries, vendor lock-in) deserve more scrutiny than easily reversed ones.
- **Simplest alternative**: sketch what a modular monolith, a managed service, or doing less would look like, and say why the proposal beats it or does not.
- **Pre-mortem**: "It is 12 months later and this failed. Why?"
- **Conway and adoption check**: do team boundaries match architecture boundaries? Which recommendations are technically right but hard for people or politics to adopt? Flag them and suggest how to mitigate resistance.
- **Challenge the premise**: is the stated requirement real, and is the problem the right one?

### 5. Classify findings

Give each finding a severity, an effort estimate and a confidence level (definitions below). One finding is one problem and one action. Prefer fewer, sharper findings over an exhaustive dump; merge duplicates.

### 6. Decide

Apply the decision rules below, then write the report from `references/report-template.md`. Put the verdict first. End with one concrete next step the team can start this week.

### 7. Self-check

Run the self-check at the bottom of `report-template.md` before sending. Counts must match everywhere, and every P0/P1 needs evidence, a specific action, effort and owner.

## Severity model

| Level  | Name     | Definition                                                                                                                                                     | Test                                                                                                    |
| ------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **P0** | Critical | Will likely cause failure of a critical requirement, a security or compliance breach, data loss, or costly unrecoverable rework if not fixed before proceeding | "If we proceed unchanged, do we build on a foundation we cannot cheaply change, or fail the next gate?" |
| **P1** | High     | Significant risk to quality goals or delivery; must be fixed before production or before the phase that depends on it; a workaround exists                     | "Would this likely cause a serious incident or major delay in the next phase?"                          |
| **P2** | Medium   | Real weakness with contained impact; fix in the next iteration                                                                                                 | "Does it hurt, but only locally or occasionally?"                                                       |
| **P3** | Low      | Improvement or polish; backlog                                                                                                                                 | "Nice to have?"                                                                                         |

Adjust the level using impact, likelihood, cost of fixing later, and detectability. Irreversible decisions and issues on critical business functions move up a level. Never mark something P0 or P1 without stating the concrete consequence.

**Effort scale** (state the basis, and say "estimate"): S up to 2 days, M 3-10 days, L 2-6 weeks, XL more than 6 weeks or a program of work.

**Confidence**: High = verified in material; Medium = inferred from partial evidence; Low = assumption. Findings with Low confidence recommend how to obtain the evidence.

## Decision rules

| Verdict                     | When                                                                                                                                                                                                          |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **APPROVE**                 | No P0, and no open P1 without an accepted mitigation                                                                                                                                                          |
| **APPROVE WITH CONDITIONS** | P0/P1 exist, but each can be closed with a bounded, verifiable action that does not change the fundamental approach. List conditions with owner, date and how they will be verified                           |
| **REVISE**                  | A P0 invalidates the core approach (requirements unmet by design, target unachievable without a different architecture), or evidence is too thin to judge critical dimensions. State what must be resubmitted |

For a quality-gate review, use the same vocabulary and the Gate Assessment Template in `quality-gates.md`.

## Guardrails against bad reviews

- **Anti-patterns are signals, not verdicts.** Check the context first. Synchronous calls are fine for two or three hops with strong consistency needs, an anemic model is fine for simple CRUD, and a monolith is often the right answer. The catalog says so itself: read its "When it is OK" notes.
- **Do not gold-plate.** Tie every finding to a requirement, quality goal, or risk. If you cannot, drop it or downgrade it to P3.
- **Thresholds are heuristics.** The numbers in the catalogs (team size, latency bands, coverage) are starting points. Present them as such and calibrate to the system's own SLOs.
- **No invented facts.** Cite where evidence comes from (document section, diagram, metric). Mark estimates as estimates and show the math.
- **Verify before asserting.** For anything version-specific or time-sensitive (framework deprecations, regulations, cloud service limits), check a current source or say you have not verified it.
- **Acknowledge strengths.** Concrete, evidenced strengths tell the team what to protect.
- **Stay constructive and direct.** Critique the design, not the people. Say plainly when something is wrong.
- **Match the reader.** Respond in the user's language. Keep chat answers short (Lite report); produce the Full report only for formal reviews or when asked.

## Reference map

Read on demand; do not load everything by default.

| File                                       | Read when                                                                                                                                                  |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/review-checklist.md`           | Step 3, for the item-level checklist and the scoring table                                                                                                 |
| `references/quality-gates.md`              | The review is tied to a phase gate, or the user asks "is it ready for X"                                                                                   |
| `references/anti-patterns-catalog.md`      | You see a suspicious pattern and need symptoms, impact and fixes (17 entries: distribution, data, integration, security, performance, operations, testing) |
| `references/quality-attributes-catalog.md` | You must define or test quality targets, scenarios, tactics, or trade-offs (ISO/IEC 25010:2023 based)                                                      |
| `references/regulated-industries.md`       | Finance, healthcare, critical infrastructure, or personal/regulated data are involved (includes DORA overlay)                                              |
| `references/report-template.md`            | Step 6, always                                                                                                                                             |
| `examples/example-design-review.md`        | You need a model of a complete Full report (long; skim the structure, do not copy the content)                                                             |
| `examples/example-review-prompts.md`       | The user wants prompt templates, or you need to know what input a given review scenario requires                                                           |

## Definition of done

The review is successful when:

1. Issues are clearly identified, with severity, evidence and impact
2. Recommendations are specific and actionable, each with an effort estimate
3. Priorities are clear: what must be fixed, what can wait
4. Risks and assumptions are transparent, including what could not be verified
5. Strengths are acknowledged
6. The verdict follows the decision rules and is consistent with the findings
7. The team has one concrete next step and verifiable conditions, and stakeholders can align on them

Your role is to help the team build better architecture: be thorough but constructive, specific but practical, and always leave them a clear path forward.
