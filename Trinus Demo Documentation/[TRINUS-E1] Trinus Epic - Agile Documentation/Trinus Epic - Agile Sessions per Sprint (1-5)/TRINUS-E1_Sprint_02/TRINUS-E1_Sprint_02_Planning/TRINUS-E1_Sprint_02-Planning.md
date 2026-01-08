
# [TRINUS-E1] Sprint 2 Planning
## Voices Present
The following Agile roles participated in Sprint 2 Planning, ensuring all perspectives and responsibilities were represented:
- Product Owner (Stakeholder)
- Scrum Master (Facilitator)
- Quality Assurance Director (Director)
- Automation Engineer (Engineer)
- Developer (Engineer)
- Architect (Engineer)
- User Acceptance Tester (Stakeholder)
- Machine Learning Lead (Engineer)
- Security Lead (Director)
- Diego Alejandro (Project Lead, Organic Voice)

## Impediments & Adaptations
During Sprint 2, the team encountered a major impediment: access to the Job Filter module was blocked. In response, the team reprioritized the backlog and pivoted to focus on Navigation Test Cases (Nav TCs) for immediate value delivery. This adaptation ensured continued progress and value delivery despite constraints, in line with Agile empiricism and adaptability.

## Sprint 2 Reflection & Lessons Learned
- The team’s ability to quickly pivot and adapt to new constraints was critical to maintaining momentum and delivering value.
- Empirical decision-making and transparency supported effective backlog reprioritization.
- Enhancements to UI, evidence logic, and reporting increased stakeholder impact.
- Continuous improvement was reinforced through daily standups and retrospective feedback.


**Date:** 2026-01-07  
**Ceremony:** Sprint 2 Planning  
**Epic Reference:** [TRINUS-E1] Trinus.com Automation Epic  
**Journey Reference:** Agile_Journey_Rev1.md  
**Triage Reference:** TRINUS_SPRINT2_TRIAGE.md

---

## Jira-Style Traceability & Mapping
This Sprint Planning document is fully traceable to the Trinus.com Automation Epic (TRINUS-E1). All User Stories (US) are mapped to their respective Feature Blocks and Epic Acceptance Criteria (AC). This ensures every increment is director/stakeholder-ready and audit-compliant.

### Epic Summary
**Epic Name:** Trinus.com Automation Epic  
**Epic Key:** TRINUS-E1  
**Description:** Deliver a fully automated, evidence-driven QA suite for Trinus.com, incrementally through five Scrum sprints, covering all critical navigation, evidence, prioritization, demo, and impediment-handling workflows.  
**Acceptance Criteria (AC):**
- [AC-1] All critical Trinus.com workflows (login, navigation, subpages) are automated and demo-ready.
- [AC-2] Evidence is captured, organized, and displayed for every test run, with retention and auditability.
- [AC-3] Backlog, prioritization, and traceability are maintained from Epic to delivered increments using taskprioritizer.py and Jira mapping.
- [AC-4] Stakeholder-ready demos and UI polish are delivered for every increment, with video artifacts and executive review.
- [AC-5] All impediments (e.g., automation guards) are documented, with technical spikes and POCs proposed and reviewed.

### Sprint 2: Epic → Block → User Story Mapping
| User Story      | Block   | Epic AC Trace | Description |
|-----------------|---------|---------------|-------------|
| US-NAV-1.2      | NAV-1   | AC-1, AC-4    | Automate main menu and subpage navigation for all critical user journeys |
| US-EVD-2.2      | EVD-2   | AC-2, AC-4    | Display evidence (screenshots, logs) in the UI for demo-readiness and director review |
| US-PRI-3.2      | PRI-3   | AC-3, AC-4    | Maintain full traceability from Epic/Block/US to Sprint and demo artifacts |
| US-EVD-2.4      | EVD-2   | AC-2, AC-5    | (Spike) Research best practices for evidence retention and propose POC for audit integration |

---

## Executive Summary
Sprint 2 Planning is informed by validated priorities and lessons from Sprint 1 and the Sprint 2 Triage. The team adapts to constraints and focuses on delivering high-value increments, with all User Stories, Acceptance Criteria, and priorities traceable to the Epic (TRINUS-E1), Feature Blocks, and Agile Journey. This document sets the plan for execution, team agreements, and expected outcomes for Sprint 2. All User Stories were created, refined, and prioritized in this session, with explicit mapping to Epic and Block.

---


## Sprint 2 Goals & Deliverables
- Automate navigation for all main menu and subpages (**US-NAV-1.2**)
- Display evidence (screenshots, logs) in the UI for demo/stakeholder review (**US-EVD-2.2**)
- Ensure full traceability from Epic/Block/US to Sprint and demo artifacts (**US-PRI-3.2**)
- Research and propose POC for evidence retention and audit integration (**US-EVD-2.4**)

---

## User Stories & Acceptance Criteria

### US-NAV-1.2 (Block: NAV-1, AC-1, AC-4): Automate main menu and subpage navigation for all critical user journeys
- **AC:** All navigation flows are automated, reproducible, and demo-ready.
- **Dependencies:** Sprint 1 navigation foundation.
- **Owner:** Automation Engineer
- **Priority:** High

### US-EVD-2.2 (Block: EVD-2, AC-2, AC-4): Display evidence (screenshots, logs) in the UI for demo-readiness and director review
- **AC:** Evidence is accessible in the UI, supporting stakeholder review and demo.
- **Dependencies:** Evidence logic from Sprint 1.
- **Owner:** QA Director
- **Priority:** High

### US-PRI-3.2 (Block: PRI-3, AC-3, AC-4): Maintain full traceability from Epic/Block/US to Sprint and demo artifacts
- **AC:** All increments are mapped and tracked using taskprioritizer.py; traceability is documented.
- **Dependencies:** Epic and Sprint 1 traceability logic.
- **Owner:** Scrum Master
- **Priority:** Medium

### US-EVD-2.4 (Block: EVD-2, AC-2, AC-5) (Spike): Research best practices for evidence retention and propose POC for integrating evidence with external audit systems
- **AC:** Research completed; POC proposed and documented.
- **Dependencies:** Evidence retention logic from Sprint 1.
- **Owner:** Architect
- **Priority:** Medium

---

## Team Agreements & Working Practices
- **Empirical Planning:** Team will adapt the plan if new constraints or opportunities arise.
- **Transparency:** All work, decisions, and outcomes will be documented and traceable to the Epic and Journey.
- **Continuous Improvement:** Daily standups will focus on lessons learned and course correction.

---



## Next Steps
- Begin Sprint 2 execution as planned.
- Document all outcomes and lessons for the Sprint 2 Retrospective.
- Ensure all increments are demo-ready and traceable to the Epic (TRINUS-E1), Block, and User Story.

---

**References:**
- [TRINUS_AUTOMATION_EPIC.md]
- [Agile_Journey_Rev1.md]
- [TRINUS_SPRINT2_TRIAGE.md]

---

**Prepared for:** IT Directors, Product Owners, Stakeholders, and Engineering Teams

**Team Consensus & Final Vote:**
All Agile voices present reviewed and approved the Sprint 2 plan, outcomes, and adaptations. Consensus: **Unanimous**.

**Author:** Diego Alejandro
