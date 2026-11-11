# Testcase Review – Quality Process Framework

Source: <https://synacor.atlassian.net/wiki/pages/viewpage.action?pageId=5877071887>

Page ID: 5877071887

Parent ID: 4943020087

Export notes:
- Some Confluence page references have no resolvable page ID/space key; titles were preserved.

---

## Purpose

This document defines the **Testcase Review Categories**, **Review Templates**, **Review Process**, and **Quality Metrics** to measure and improve the effectiveness of test case writing and review within the Zimbra Engineering Gated Delivery Process.

Aligned with:

-   Gated Process - Zimbra Engineering [Confluence page reference; URL unavailable]
    
-   QA Involvement Guidelines – Gated Delivery Process [Confluence page reference; URL unavailable]
    

* * *

## 1\. Testcase Review Categories

| # | Category Code | Category Name | Definition | Source Document | Action Required |
| --- | --- | --- | --- | --- | --- |
| 1 | **REQ-GAP** | Requirements Coverage Gap | Test case does not cover a functional requirement or acceptance criteria explicitly stated in the PRD (user stories, feature specs, acceptance criteria). | PRD / User stories | Update existing TC |
| 2 | **DESIGN-GAP** | Design Coverage Gap | Test case does not cover technical scenarios derived from HLD/LLD — API contracts, LDAP attribute usage, integration touchpoints, data flow, component interactions. | HLD / LLD / Implementation Tickets | Add new TC |
| 3 | **REG-GAP** | Regression Coverage Gap | An existing functionality that could be impacted by the change is not covered by any test case. | Existing test suite / change scope | Add new TC |
| 4 | **UNCLEAR** | Unclear Test Case | Test case steps, expected results, or preconditions are ambiguous, incomplete, or not reproducible as written. | — | Update existing TC |
| 5 | **REDUNDANT** | Redundant Test Case | Test case duplicates another TC or tests a scenario already sufficiently covered. | — | Remove TC |
| 6 | **MINOR** | Minor / Non-blocking Issue | Typo, formatting issue, wrong TCID reference, missing metadata (Priority, Type) — does not affect TC validity or executability. | — | Cosmetic fix — non-blocking |

**Key Rules:**

-   Categories 1–5 contribute to the **Rework Rate** metric
    
-   Category 6 (MINOR) is **excluded** from Rework Rate and must **not block approval**
    
-   A single TC can attract **multiple categories** — count each separately in the Summary comment
    
-   **DESIGN-GAP** is best identified by the **Developer/Architect** reviewer (HLD/LLD owner); **REQ-GAP** is best identified by the **QA Lead** (PRD mapper)
    

* * *

## 2\. Testcase Review Templates

Test case reviews must include **two structured Jira comments** — a Detailed comment and a Summary comment.

* * *

### 2.1 Detailed Review Comment

Posted by the Reviewer for each test case requiring a change.

```
🔍 REVIEW FEEDBACK
TCID#[X] | [CATEGORY CODE] | [Short Issue Title]
Issue   : [Describe what is wrong or missing]
Action  : [What the TC author needs to do]
Ref     : [PRD section / HLD section / LLD section if applicable]
TCID#[X] | [CATEGORY CODE] | [Short Issue Title]
Issue   : [Describe what is wrong or missing]
Action  : [What the TC author needs to do]
Ref     : [PRD section / HLD section / LLD section if applicable]
```

**Example:**

```
🔍 REVIEW FEEDBACK
TCID#3 | UNCLEAR | Incomplete test steps
Issue  : Test case steps do not include the exact API request headers 
         required to authenticate the EWS call.
Action : Add Authorization header and Content-Type to Step 2. 
         Include expected HTTP 200 response in Expected Result.
Ref    : LLD – Section 3.2 EWS Authentication Flow
TCID#7 | REQ-GAP | Shared mailbox scenario missing
Issue  : PRD acceptance criteria includes shared mailbox access but 
         no TC covers this scenario.
Action : Add new TC covering shared mailbox login via Outlook/EWS.
Ref    : PRD – AC-07 Shared Mailbox Access
```

* * *

### 2.2 Summary Review Comment

Posted by the Reviewer after completing the full review. One summary comment per reviewer.

```
📋 REVIEW SUMMARY
Reviewer        : [Name]
Review Date     : [DD-MMM-YYYY]
Testcases Reviewed = [X]
--- Changes Requested (counted in Rework Rate) ---
REQ-GAP    | Requirements Coverage Gap  (Update TCs) = [X]
DESIGN-GAP | Design Coverage Gap        (Add TCs)    = [X]
REG-GAP    | Regression Coverage Gap    (Add TCs)    = [X]
UNCLEAR    | Unclear Test Cases         (Update TCs) = [X]
REDUNDANT  | Redundant Test Cases       (Remove TCs) = [X]
Total Changes Requested = [X]
--- Non-blocking (NOT counted in Rework Rate) ---
MINOR      | Minor / Cosmetic Issues                 = [X]
--- Decision ---
[ ] ✅ APPROVED — No changes required / Only MINOR issues found
[ ] 🔄 CHANGES REQUIRED — Ticket to move back to In Progress
```

* * *

### 2.3 Approval Comment

When a Reviewer approves with no changes (or only MINOR issues):

```
✅ APPROVED
Reviewer    : [Name]
Review Date : [DD-MMM-YYYY]
Comments    : [Optional — e.g., "Test cases are comprehensive and aligned 
               with PRD and LLD. Minor typo in TCID#5 — non-blocking."]
```

> ⚠️ The transition to **Approved** requires **exactly 2 comments containing** `✅ APPROVED` from 2 different reviewers.

* * *

## 3\. Testcase Review Process

### 3.1 Reviewers

Each test case set must be reviewed by **3 reviewers**. Approval requires **any 2 of the 3**:

| Reviewer Role | Responsibility |
| --- | --- |
| **Peer QA** | Reviews TC structure, coverage completeness, step clarity, regression gaps |
| **QA Lead / QA Manager** | Reviews alignment with PRD/acceptance criteria, overall coverage quality |
| **Developer / Architect** | Reviews technical accuracy — API, LDAP, integration scenarios vs HLD/LLD |

* * *

### 3.2 Workflow States

```
In Progress → In Review → Approved
                  ↓ (changes required)
              In Progress  (Review Cycle Count + 1)
```

* * *

### 3.3 Process Steps

| Step | Who | Action |
| --- | --- | --- |
| 1 | **QA Author** | Writes test cases and attaches TC document to Jira ticket |
| 2 | **QA Author** | Transitions ticket: **In Progress → In Review** |
| 3 | **QA Author** | Tags all 3 reviewers in a comment to notify them |
| 4 | **Each Reviewer** | Posts **🔍 Detailed Feedback** comment (for TCs needing change) |
| 5 | **Each Reviewer** | Posts **📋 Summary** comment OR **✅ APPROVED** comment |
| 6a | **QA Lead / Dev** | If 2 approvals received → transitions ticket: **In Review → Approved** |
| 6b | **Any Reviewer** | If changes required → transitions ticket: **In Review → In Progress** |
| 7 | **QA Author** | Addresses all feedback, updates TCs |
| 8 | **QA Author** | Transitions ticket back: **In Progress → In Review** (new cycle begins) |
| 9 | — | Repeat Steps 4–6 until 2 approvals obtained |

* * *

### 3.4 Approval Rules

| Rule | Detail |
| --- | --- |
| ✅ **Approval threshold** | 2 out of 3 reviewers must post `✅ APPROVED` |
| ✅ **MINOR issues** | Do NOT block approval — reviewer still posts `✅ APPROVED` with MINOR note |
| 🔄 **Rework trigger** | Even 1 reviewer requesting changes (non-MINOR) moves ticket to **In Progress** — unless 2 approvals already exist |
| ⏱️ **Review TAT SLA** | Peer QA: ≤ 1 business day; QA Lead: ≤ 2 business days; Developer: ≤ 2 business days |

* * *

## 4\. Quality Metrics

### 4.1 Testcase Rework Rate

> Measures the quality of test cases written.

{Rework Rate} = {{REQ-GAP + DESIGN-GAP + REG-GAP + UNCLEAR + REDUNDANT}}/{{Total TCs Reviewed}}\*100

| Target | Value |
| --- | --- |
| ✅ Healthy | < 15% |
| ⚠️ Needs Attention | 15–30% |
| 🔴 Action Required | 30% |

* * *

### 4.2 Review Cycles for Approval

> Measures how many rework loops a ticket goes through before approval.

{Avg Review Cycles} = {{Review Cycle Count across all tickets}}/{Total tickets reviewed}}

| Target | Value |
| --- | --- |
| ✅ Ideal | ≤ 1 cycle |
| ⚠️ Acceptable | 2 cycles |
| 🔴 Action Required | 3+ cycles |

* * *

### 4.3 Review Turnaround Time (TAT)

> Measures the end-to-end time taken for a ticket to move from review initiation to final approval.

**TAT Definition (per ticket):**  
{TAT} = {Date ticket reached "Approved"} - {Date ticket first entered "In Review"}

> This is an **end-to-end measure** — it includes all rework cycles within. A ticket that goes through multiple In Review → In Progress → In Review loops will have a higher TAT.

**Average TAT (team):**  
{Avg TAT} = {{TAT of all tickets}}/{Total tickets reviewed}}

*Example: TATs of 1, 3, 2, 2, 2 days across 5 tickets → Avg TAT = (1+3+2+2+2) / 5 = **2 days***

* * *

**Targets:**

| Sub-metric | Target |
| --- | --- |
| **Per-Ticket TAT** | ≤ 3 business days |
| **Average TAT** | ≤ 2 business days |

* * *

**Jira Fields Used:**

| Field | Captured At |
| --- | --- |
| `Review Start Date` | Ticket first enters "In Review" |
| `Approval Date` | Ticket reaches "Approved" |
| `TAT` | `Approval Date` − `Review Start Date` |

* * *

## 4.4 Metric Summary

| # | Metric | Formula | Target |
| --- | --- | --- | --- |
| 1 | **Rework Rate** | (Changes Requested / Total TCs) × 100 | < 15% |
| 2 | **Review Cycles** | Avg count of In Review → In Progress transitions | ≤ 1 cycle |
| 3a | **Per-Ticket TAT** | `Approval Date` − `First Review Start Date` | ≤ 3 business days |
| 3b | **Average TAT** | Sum of all TATs / Total tickets reviewed | ≤ 2 business days |
