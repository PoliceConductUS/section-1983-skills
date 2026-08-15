---
name: rrd
description: "Generate a Response Requirements Document (RRD) for opposing (or supporting) a specific claim/argument in a legal motion. Use when planning a motion response, building a claim-by-claim checklist, or when asked to create an RRD. Triggers on: create an rrd, write rrd for, respond to this motion, opposition plan, response checklist, requirements for response, claim-by-claim response, 12(b)(6) response plan, qualified immunity response plan."
---

# RRD Generator

Create detailed **Response Requirements Documents (RRDs)** that are clear, actionable, and suitable for drafting a motion response **claim-by-claim**.

An RRD is **not** the brief. It is the blueprint: what must be argued, proved, cited, and attached so the final response is tight, checkable, and complete.

## Routing rule

Use this generic skill for non-Rule-12 response planning. For a Section 1983 Rule 12 motion, use `rrd-rule12` and then `rrd-rule12-officers` or `rrd-rule12-city` as applicable. If the plan evaluates a complaint or amendment, load `drafting-section-1983-complaints`; add `drafting-false-arrest-complaints` when probable cause, alternative offenses, seizure timing, or arrest video is material. Run `audit-authorities` before marking any authority-dependent unit ready.

---

## The Job

1. Receive the motion claim/argument (or set of arguments) the user must respond to
2. Ask 3–5 essential clarifying questions (with lettered options)
3. Generate a structured RRD based on answers
4. Save to `responses/<response-due-date>/<motion-folder>/rrd.yaml`

**Important:** Do **NOT** draft the final response brief. Only produce the RRD.

---

## Step 1: Clarifying Questions

Ask only critical questions where the prompt is ambiguous. Focus on:

- **Posture & Court:** What court/jurisdiction and what motion type?
- **Targets:** Which specific claims/arguments are being attacked?
- **Record:** What evidence/record exists and what is admissible at this stage?
- **Relief & Outcomes:** What exact ruling are we asking for (deny/strike/partial deny/etc.)?
- **Constraints:** Deadlines, page limits, local rules, required sections.

```

### Format Questions Like This

1. What is the procedural posture / motion type?
   A. Rule 12(b)(6) (failure to state a claim)
   B. Rule 12(b)(1) (jurisdiction)
   C. Summary judgment (Rule 56)
   D. Qualified immunity (12(b)(6) or summary judgment)
   E. Other: [please specify]

2. What is the court/jurisdiction?
   A. Federal (U.S. District Court) — specify circuit
   B. State trial court — specify state
   C. State appellate court — specify state
   D. Other: [please specify]

3. What “record” can we rely on in this response?
   A. Pleadings only (complaint + exhibits + judicially noticeable materials)
   B. Pleadings + attachments to the response (declarations/exhibits)
   C. Full discovery record (depo, interrogatories, admissions)
   D. Mixed/unsure — treat conservatively

4. What is the desired outcome?
   A. Deny motion in full
   B. Deny in part / narrow issues
   C. Preserve leave to amend / request amendment window
   D. Procedural win (strike, sanctions, or convert/not convert)

This lets users reply with “1A, 2A, 3A, 4B” for quick iteration.

```

## Step 2: RRD Structure

Generate the RRD with these sections.

### 1. Matter Snapshot

- Case name / caption (as provided)
- Motion being responded to
- Filing deadline (if provided)
- Response posture (oppose/support/partial)
- Standard of review posture (pleadings-only vs evidentiary record)

### 2. Response Objectives

Bulleted list of **specific outcomes**:

- Deny dismissal of Claim X
- Preserve Claim Y under alternative theory Z
- Prevent conversion to Rule 56 (if relevant)
- Preserve issues for appeal / avoid waiver

### 3. Argument Map

A table-like outline mapping:

- **Movant Heading / Argument**
- **Targeted Claim/Element**
- **Controlling Standard**
- **Key Facts (with citation placeholders)**
- **Counter-Authority**
- **Core Rebuttal Logic**
- **What Would Defeat Us (risk)**
- **What Defeats Them (falsifiable hypothesis/test)**

### 4. Response Units (RU) — Claim-by-Claim Requirements

For each attacked claim/argument, create a “Response Unit” that is small and checkable.

**Format:**

```markdown
## RU-001: [Movant Argument Heading or Short Name]

**Attacked Claim/Issue:** [e.g., First Amendment retaliation; PI probable cause; Qualified immunity prong 1/2]

**Movant’s Ask:** [dismiss / grant QI / strike / convert / etc.]

**Controlling Standard (Required):**

- [ ] Quote or accurately paraphrase the controlling test elements
- [ ] Identify burden allocation (who must show what)
- [ ] Identify what the court must accept as true at this stage (if pleadings)

**Record Facts We Must Establish (Required):**

- [ ] Fact F1: [statement] — cite: [BWC timestamp / exhibit / complaint ¶]
- [ ] Fact F2: [statement] — cite: [...]
- [ ] Fact F3: [statement] — cite: [...]

**Movant’s “Supporting Facts” to Neutralize (Required):**

- [ ] Alleged fact M1: [their framing] — response: [why disputed/irrelevant/conclusory]
- [ ] Alleged fact M2: [...]

**Counter-Authority (Required):**

- [ ] Case/Rule A: [proposition] — why it controls here
- [ ] Case/Rule B: [proposition] — why it distinguishes movant’s cases

**Rebuttal Logic (Required):**

- [ ] Syllogism: If [standard element], then [result], because [facts + authority]
- [ ] Alternative framing (backup): [narrower argument that still wins]

**Falsifiable Hypothesis / “Done Test” (Required):**

- [ ] If **H1** is true, movant’s argument fails: [precise statement]
- [ ] How we would verify H1: [cite / exhibit / declaration / judicial notice]
- [ ] If **H1** is false, mitigation: [amendment / alternative claim / concession]

**Exhibits & Citations Needed (Required):**

- [ ] Exhibit E1: [name] — purpose: [what it proves]
- [ ] Exhibit E2: [...]
- [ ] Citation list: [complaint ¶ / docket entry / transcript page / timestamp]

**Requested Ruling (Required):**

- [ ] Deny / deny-in-part / preserve leave to amend / other: [exact language]
```

**Important:**

- Every checklist item must be **verifiable**.
- Prefer “cite X at Y” over “show the court.”
- If a fact cannot be sourced, mark it as a **gap** and specify how it will be filled.

### 5. Standards Library (Reusable)

Centralize the controlling standards likely needed:

- Pleading standards (Twombly/Iqbal equivalents, if applicable)
- Qualified immunity framework (if applicable): clearly established + violation prongs
- Probable cause / arguable probable cause (if applicable)
- Elements of each substantive claim (e.g., retaliation, false arrest, municipal liability)

Each entry should include:

- The test elements
- Burden
- What facts matter most
- Common defense pivots and how to counter them

### 6. Evidence & Exhibit Plan

- Exhibit inventory (what you have, what you need)
- Authentication plan (declaration, stipulation, self-authenticating, judicial notice)
- “Stage gate” note: what can be used at this procedural posture

### 7. Risk Register (What Could Sink Us)

For each major risk:

- Risk statement
- Why it matters
- Mitigation (alternate theory, amendment, narrowing, concessions)
- “Trigger condition” (what would make the risk real)

### 8. Compliance & Packaging

- Page limits, formatting, required sections (if provided)
- Required certifications (meet-and-confer, word count, etc.)
- Filing components checklist:
  - Response brief
  - Appendix/exhibits
  - Proposed order (if required)
  - Notice of hearing (if required)
  - Certificate of service

### 9. Open Questions

Anything still unknown that blocks drafting:

- Missing transcript? Missing exhibit? Unclear motion scope?
- Conflicting dates?
- Need to confirm standard-of-review?

---

## Writing for Non-Specialists (and Future You)

The RRD reader may be a junior attorney, paralegal, or AI agent. Therefore:

- Be explicit and unambiguous
- Define legal jargon the first time it appears
- Use numbered requirements for easy cross-reference
- Use short “Response Units” so each argument can be drafted and checked independently
- Use falsifiable tests so you know when you’re truly “done”

---

## Output

- **Format:** YAML (`rrd.yaml`)
- **Location:** `responses/<response-due-date>/<motion-folder>/`
- **Filename:** `rrd.yaml` (fixed)

Where:

- `<response-due-date>` is the court-ordered due date for the response (YYYY-MM-DD)
- `<motion-folder>` matches the motion folder name (e.g., `city-mtd`, `officers-mtd`)

Example output folder layout:

```text
responses/
└── 2026-01-29/
    ├── city-mtd/
    │   ├── SOURCE.yaml
    │   └── rrd.yaml
    └── officers-mtd/
        ├── SOURCE.yaml
        └── rrd.yaml
```

Each response folder should already contain `SOURCE.yaml`; if it does not, create it following the project `SOURCE.yaml` spec.

---

## Example RRD (Mini)

```markdown
# RRD: Opposition to Motion to Dismiss (Rule 12(b)(6))

## Matter Snapshot

- Motion: Defendant’s Rule 12(b)(6) Motion to Dismiss
- Posture: Pleadings-only
- Desired outcome: Deny in full; alternatively preserve leave to amend as to Count IV

## Response Objectives

- Keep Count I (First Amendment retaliation) alive past 12(b)(6)
- Defeat qualified immunity at pleadings stage by alleging violation + clearly established law
- Prevent movant from reframing disputed facts as “undisputed”

## RU-001: “No Constitutional Violation” (Retaliation)

**Attacked Claim/Issue:** First Amendment retaliation

**Controlling Standard (Required):**

- [ ] Identify elements: protected activity + adverse action + causal connection (retaliatory motive)
- [ ] Note pleading posture: factual allegations taken as true; plausible inference standard

**Record Facts We Must Establish (Required):**

- [ ] F1: Plaintiff engaged in protected recording/criticism — cite: Complaint ¶\_\_
- [ ] F2: Arrest occurred shortly after protected activity — cite: Complaint ¶\_\_ / timeline
- [ ] F3: Officer statements support retaliatory motive — cite: BWC timestamp **:**

**Counter-Authority (Required):**

- [ ] Case A: Retaliatory arrest analysis post-Nieves (and exceptions if applicable)
- [ ] Case B: Clearly established principle that arrest in retaliation for protected speech is unlawful absent objective PC (as framed for this circuit)

**Falsifiable Hypothesis / “Done Test” (Required):**

- [ ] H1: If the record shows officer announced intent to “find justification,” then plausible retaliatory motive is adequately pled.
- [ ] Verification: BWC clip at **:** + transcript excerpt.
- [ ] If false: pivot to alternative theory (e.g., lack of PC / unlawful seizure) + preserve amendment.

**Requested Ruling (Required):**

- [ ] Deny dismissal of Count I; deny qualified immunity at this stage.
```

---

## Checklist

Before saving the RRD:

- [ ] Asked clarifying questions with lettered options (only where needed)
- [ ] Built Response Units for each distinct movant argument / attacked element
- [ ] Each RU contains: controlling standard, record facts, counter-authority, rebuttal logic, falsifiable hypothesis, exhibits needed, requested ruling
- [ ] Risks and mitigations are stated plainly
- [ ] Packaging/compliance checklist is included
- [ ] Saved to `responses/<response-due-date>/<motion-folder>/rrd.yaml`
