




# TRINUS_EPIC_AUTOMATION.md — Trinus.com Automation Epic

**Executive Overview, Jira Traceability, and Agile Artifacts**


**Date:** 2026-01-02

---


Welcome, Vivek and Francis. This Epic is your executive and technical home for the Trinus.com End-to-End QA Automation initiative. It provides full traceability from business goals to delivered increments, and is designed for both IT leadership and engineering review. All content is now finalized and reflects the actual work, priorities, and Agile ceremonies completed by the team.


## Value for IT Directors, Scrum Teams & Stakeholders

- **Transparency:** All decisions and outcomes are traceable to Product Backlog Items, Feature Blocks, User Stories, and Sprint Goals, surfaced through taskprioritizer.py.
- **Empiricism:** The process is inspectable and adaptable, supporting continuous improvement.
- **Scalability:** The Scrum framework and documentation support future growth, audit, and cross-functional teams.
- **Demo-Readiness:** Each Increment is potentially shippable and ready for stakeholder review.

---
---

## About This Epic & Backlog Structure

This document is the single source of truth for the Trinus.com Automation Epic and its Feature Blocks. It serves as the Epic and Blocks backlog. All major areas of work are represented as Feature Blocks, each with mapped User Stories (US). The Epic Acceptance Criteria (AC) and Block descriptions are defined here.

**User Stories (US) and Acceptance Criteria (AC):**
- User Stories (US) are listed under each Feature Block for traceability.
- The detailed Acceptance Criteria (AC) for each US will be created and refined during Sprint Planning ceremonies (formerly called Triage). These ceremonies are documented in the corresponding Sprint Planning .md files, which will contain the prioritized Jira US tickets and their AC, as well as the team’s prioritization and consensus.
- This ensures that every US is traceable from Epic → Block → US → Sprint, and that all prioritization and refinement is captured in the right Agile artifact.

**How to Read This Epic:**
- Jira-style Epic, with traceability to all major deliverables and User Stories (US)
- Major Feature Blocks (delivery areas), each with mapped User Stories (US)
- Sprints, each referencing the US delivered and their Acceptance Criteria (AC)
- Index of ceremonies and artifacts (the .md files), which represent Agile process, not Jira items

**Note:** Margin bars visually mark Jira items (Epic, Feature Block, US) for clarity in GitHub/Markdown. “Feature Block” is used here for grouping; in strict Jira, these may be Epics or Components.

**Scrum Roles in this Epic:** Product Owner (PO), Scrum Master (SM), Developers (QA, Automation Engineer, etc.), Stakeholders (review/feedback)

**Mapping:**
- This document is the Epic and welcome page.
- Feature Blocks and User Stories are Jira-style items, visually marked for clarity.
- The .md files in this repo represent Agile ceremonies and artifacts (e.g., Planning, Retrospective), not Jira tickets themselves, but are referenced for traceability.

---

<div style="border-left: 4px solid #0052CC; padding-left: 1em; margin-bottom: 1em; background: #f6f8fa;">
<strong>Epic</strong> <br>
<strong>Epic Name:</strong> Trinus.com End-to-End Automation Epic  <br>
<strong>Epic Key:</strong> TRINUS-EPIC-001  <br>
<strong>Description:</strong> As a stakeholder, I want a fully automated, evidence-driven QA suite for Trinus.com, delivered incrementally through five Scrum sprints, so that I can ensure quality, traceability, and demo-readiness for all critical workflows.  <br>
<strong>Acceptance Criteria (AC):</strong>
<ul>
<li>The QA suite must automate all critical navigation and workflow scenarios for Trinus.com, with evidence captured for each run.</li>
<li>All automation must be reproducible, with per-run evidence folders and retention policies.</li>
<li>Each sprint must deliver a potentially shippable Increment, validated by Sprint Review and meeting the Definition of Done (DoD).</li>
<li>All work must be prioritized and traceable using taskprioritizer.py, with clear links from Epic AC to User Story (US) AC.</li>
<li>Demo artifacts and documentation must be available for director and stakeholder review at the end of each sprint.</li>
<li>Impediments (e.g., automation guards) must be documented, with spikes and POCs proposed as solutions.</li>
</ul>
<strong>Traceability:</strong> Each Block below is mapped to this Epic. User Stories (US) are mapped to Blocks and delivered by Sprints. See individual Sprint docs for US-level detail.<br>
<strong>Scrum Roles:</strong> Product Owner, Scrum Master, Developers, Stakeholders
</div>

---

## Major Delivery Blocks

<div style="border-left: 4px solid #36B37E; padding-left: 1em; margin-bottom: 1em; background: #f6f8fa;">
<strong>Block 1: Navigation Automation</strong> <br>
<strong>Block Key:</strong> TRINUS-BLOCK-001  <br>
<strong>User Stories:</strong>
<ul>
<li><strong>US-101:</strong> As a QA engineer, I want automated navigation for all main Trinus.com workflows so that I can validate user journeys.</li>
<li><strong>US-102:</strong> As a stakeholder, I want navigation tests to be reproducible and evidence-driven for auditability.</li>
</ul>
</div>
<div style="border-left: 4px solid #36B37E; padding-left: 1em; margin-bottom: 1em; background: #f6f8fa;">
<strong>Block 2: Evidence Management</strong> <br>
<strong>Block Key:</strong> TRINUS-BLOCK-002  <br>
<strong>User Stories:</strong>
<ul>
<li><strong>US-201:</strong> As a QA engineer, I want per-run evidence folders and retention logic so that test results are organized and traceable.</li>
<li><strong>US-202:</strong> As a stakeholder, I want evidence displayed in the UI for demo-readiness.</li>
</ul>
</div>
<div style="border-left: 4px solid #36B37E; padding-left: 1em; margin-bottom: 1em; background: #f6f8fa;">
<strong>Block 3: Prioritization & Traceability</strong> <br>
<strong>Block Key:</strong> TRINUS-BLOCK-003  <br>
<strong>User Stories:</strong>
<ul>
<li><strong>US-301:</strong> As a team member, I want all work prioritized and tracked using taskprioritizer.py so that delivery is transparent and auditable.</li>
</ul>
</div>
<div style="border-left: 4px solid #36B37E; padding-left: 1em; margin-bottom: 1em; background: #f6f8fa;">
<strong>Block 4: Demo-Readiness</strong> <br>
<strong>Block Key:</strong> TRINUS-BLOCK-004  <br>
<strong>User Stories:</strong>
<ul>
<li><strong>US-401:</strong> As a stakeholder, I want a stakeholder-ready UI and demo walkthroughs for each increment.</li>
</ul>
</div>
<div style="border-left: 4px solid #36B37E; padding-left: 1em; margin-bottom: 1em; background: #f6f8fa;">
<strong>Block 5: Impediment Handling</strong> <br>
<strong>Block Key:</strong> TRINUS-BLOCK-005  <br>
<strong>User Stories:</strong>
<ul>
<li><strong>US-501:</strong> As a QA engineer, I want automation guards and impediments documented for protected modules (e.g., Jobs module).</li>
<li><strong>US-502:</strong> As a team, I want spikes and POCs proposed for bypassing automation guards.</li>
</ul>
</div>

---

## Scrum Delivery Overview

**Sprint 1: Backlog Planning and Kickoff & Execution**<br>
• Established the Product Backlog and defined the MVP as a Selenium-based, reproducible test suite with evidence as Sprint Goal.<br>
• Backlog Planning and Kickoff: Selected PBIs, estimated effort, and clarified Acceptance Criteria.<br>
• Sprint Execution: Implemented foundational automation, evidence retention, and team alignment.<br>
• Sprint Review: Demonstrated Increment, validated DoD.<br>
• Sprint Retrospective: Identified improvements for backlog refinement and team collaboration.<br>
<strong>Sprint 1 Acceptance Criteria (AC):</strong><br>
• US-101, US-102 (Block 1): MVP navigation flows automated and reproducible.<br>
• US-201 (Block 2): Per-run evidence folders created and retained.<br>
• US-301 (Block 3): All work prioritized with taskprioritizer.py and traceable to Epic AC.<br>

**Sprint 2: Adaptation & Empirical Process**<br>
• Backlog Planning: Reprioritized backlog due to impediment (Job Filter module access blocked).<br>
• Sprint Execution: Pivoted to Navigation Test Cases (Nav TCs) for immediate value delivery.<br>
• Enhanced UI, evidence logic, and reporting; integrated AI-driven context and image display.<br>
• Sprint Review: Inspected Increment, gathered feedback.<br>
• Sprint Retrospective: Adapted Definition of Ready (DoR) and DoD for future sprints.<br>
<strong>Sprint 2 Acceptance Criteria (AC):</strong><br>
• US-101, US-102 (Block 1): Navigation Test Cases automated for all top nav/submenu pages.<br>
• US-201, US-202 (Block 2): Improved evidence logic, only latest run shown, Trinus isolated, evidence displayed in UI.<br>
• US-401 (Block 4): UI and evidence display improved for stakeholder review.<br>
• US-301 (Block 3): All work prioritized and traceable to Epic AC.<br>

**Sprint 3: Demo-Readiness & Stakeholder Engagement**<br>
• Backlog Planning: Focused on finalizing demo polish, unified evidence, and stakeholder-ready UI.<br>
• Sprint Execution: Addressed last-mile fixes, rehearsed demo, and prepared for Sprint Review.<br>
• Sprint Review: Presented Increment with YouTube walkthrough and application demo.<br>
• Sprint Retrospective: Captured lessons learned, updated team working agreements.<br>
<strong>Sprint 3 Acceptance Criteria (AC):</strong><br>
• US-401 (Block 4): Unified evidence display for all test types, stakeholder-ready UI.<br>
• US-101 (Block 1): Trinus Tour always runs first, visually prioritized.<br>
• US-301 (Block 3): All priorities set using taskprioritizer.py, traceable to Epic AC.<br>

**Sprint 4 (Planned): Scaling & Cross-Functional Value**<br>
• Backlog Planning: Apply Trinus Automation standards to Edwards Navigation Test Case.<br>
• Sprint Execution: Expand Increment scope, demonstrate cross-domain value.<br>
<strong>Sprint 4 Acceptance Criteria (AC):</strong><br>
• US-101 (Block 1): Standards applied to new domain (Edwards Navigation Test Case).<br>
• US-401 (Block 4): Increment scope expanded, cross-domain demo prepared.<br>
• US-301 (Block 3): All work prioritized and traceable to Epic AC.<br>

**Sprint 5 (Roadmap): Continuous Improvement & Spike for Trinus Jobs Module Automation Safeguards**<br>
• Backlog Planning: Revisit the Trinus Job module as an automation-guarded case-study and the overcoming impediments of automating a solution around it.<br>
• Sprint Execution: Document protections the module displays, initial attempted solutions during Sprint 1, and lessons learned.<br>
• Sprint Review: Create actionable items as possible solutions that came from the Spike for a possible POC on how the guard was bypassed and what stack was needed to solve the case.<br>
<strong>Sprint 5 Acceptance Criteria (AC):</strong><br>
• US-501 (Block 5): All automation guards and impediments documented for the Jobs module.<br>
• US-502 (Block 5): Actionable items and POC solutions proposed for bypassing automation guard.<br>
• US-301 (Block 3): All work prioritized and traceable to Epic AC.<br>

---

## Scrum Artifacts & Ceremonies Index

- [TRINUS_SPRINT1_PLANNING.md](TRINUS_SPRINT1_PLANNING.md) — Sprint 1 Planning: Product Backlog creation, Sprint Goal, and Acceptance Criteria
- [TRINUS_SPRINT1_RETRO.md](TRINUS_SPRINT1_RETRO.md) — Sprint 1 Retrospective: Inspect & adapt, team improvements
- [TRINUS_SPRINT2_PLANNING.md](TRINUS_SPRINT2_PLANNING.md) — Sprint 2 Planning: Backlog refinement, Sprint Goal, and pivot
- [TRINUS_SPRINT2_RETRO.md](TRINUS_SPRINT2_RETRO.md) — Sprint 2 Retrospective: Empirical process, DoR/DoD updates
- [TRINUS_SPRINT3_PLANNING.md](TRINUS_SPRINT3_PLANNING.md) — Sprint 3 Planning: Demo-readiness, stakeholder focus
- [TRINUS_SPRINT3_RETRO.md](TRINUS_SPRINT3_RETRO.md) — Sprint 3 Retrospective: Lessons learned, working agreements
- [SYMBOLIC_AGILE_TEAM_ROLES.md](SYMBOLIC_AGILE_TEAM_ROLES.md) — Scrum Team Roles: Product Owner, Scrum Master, Developers, and responsibilities

---

## Value for Scrum Teams & Stakeholders

- **Transparency:** All decisions and outcomes are traceable to Product Backlog Items, Blocks, User Stories, and Sprint Goals, surfaced through taskprioritizer.py.
- **Empiricism:** The process is inspectable and adaptable, supporting continuous improvement.
- **Scalability:** The Scrum framework and documentation support future growth, audit, and cross-functional teams.
- **Demo-Readiness:** Each Increment is potentially shippable and ready for stakeholder review.

---

_This is the Epic and master PBI for the Trinus Automation Scrum documentation. Begin here, then follow the index to explore each ceremony and artifact. All files are designed for clarity, traceability, and actionable insight, with the story of Agile transformation and continuous improvement (Kintsugi) woven throughout._


##########################
# === TRACEABILITY TABLES (NEW SECTION) ===
##########################

| AC ID           | Description                | Satisfied by US ID(s)        |
|-----------------|---------------------------|------------------------------|
| [AC-1](#AC-1)   | [Describe AC-1 here]      | [US-101](#US-101), [US-102](#US-102) |
| [AC-2](#AC-2)   | [Describe AC-2 here]      | [US-201](#US-201), [US-202](#US-202) |
| [AC-3](#AC-3)   | [Describe AC-3 here]      | [US-301](#US-301)            |
| [AC-4](#AC-4)   | [Describe AC-4 here]      | [US-401](#US-401)            |
| [AC-5](#AC-5)   | [Describe AC-5 here]      | [US-501](#US-501), [US-502](#US-502) |
| ...             | ...                       | ...                          |

| US ID           | Description                | Satisfies AC ID(s)           |
|-----------------|---------------------------|------------------------------|
| [US-101](#US-101) | [Describe US-101 here]   | [AC-1](#AC-1)                |
| [US-102](#US-102) | [Describe US-102 here]   | [AC-1](#AC-1)                |
| [US-201](#US-201) | [Describe US-201 here]   | [AC-2](#AC-2)                |
| [US-202](#US-202) | [Describe US-202 here]   | [AC-2](#AC-2)                |
| [US-301](#US-301) | [Describe US-301 here]   | [AC-3](#AC-3)                |
| [US-401](#US-401) | [Describe US-401 here]   | [AC-4](#AC-4)                |
| [US-501](#US-501) | [Describe US-501 here]   | [AC-5](#AC-5)                |
| [US-502](#US-502) | [Describe US-502 here]   | [AC-5](#AC-5)                |
| ...             | ...                       | ...                          |

#### Sprint-to-AC/US Mapping

Sprint 1:
	- Delivered US: [US-101](#US-101), [US-102](#US-102), [US-201](#US-201), [US-301](#US-301)
	- Satisfies AC: [AC-1](#AC-1), [AC-2](#AC-2), [AC-3](#AC-3)
Sprint 2:
	- Delivered US: [US-202](#US-202), [US-401](#US-401)
	- Satisfies AC: [AC-2](#AC-2), [AC-4](#AC-4)
Sprint 3:
	- Delivered US: [US-501](#US-501), [US-502](#US-502)
	- Satisfies AC: [AC-5](#AC-5)
...

#### User Story Acceptance Criteria Placeholders

[US-101](#US-101) Acceptance Criteria: See [TRINUS_SPRINT1_PLANNING.md#US-101-AC]
[US-102](#US-102) Acceptance Criteria: See [TRINUS_SPRINT1_PLANNING.md#US-102-AC]
[US-201](#US-201) Acceptance Criteria: See [TRINUS_SPRINT1_PLANNING.md#US-201-AC]
[US-202](#US-202) Acceptance Criteria: See [TRINUS_SPRINT2_PLANNING.md#US-202-AC]
[US-301](#US-301) Acceptance Criteria: See [TRINUS_SPRINT1_PLANNING.md#US-301-AC]
[US-401](#US-401) Acceptance Criteria: See [TRINUS_SPRINT2_PLANNING.md#US-401-AC]
[US-501](#US-501) Acceptance Criteria: See [TRINUS_SPRINT3_PLANNING.md#US-501-AC]
[US-502](#US-502) Acceptance Criteria: See [TRINUS_SPRINT3_PLANNING.md#US-502-AC]
...

##########################
# === END TRACEABILITY TABLES (NEW SECTION) ===
##########################
