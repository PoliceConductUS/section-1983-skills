---
name: rrd-rule12-officers
description: "Use when creating a response plan, checklist, or Response Requirements Document for an officers' Rule 12(b)(6) motion in a Section 1983 case, especially when qualified immunity requires claim-by-claim and officer-by-officer analysis in the movant's heading order."
---

# SKILL.md — rrd-rule12-officers

Create a detailed **Response Requirements Document (RRD)** for an **officers’ Rule 12(b)(6) Motion to Dismiss** in a §1983 case, where **qualified immunity** is commonly raised.

An RRD is **not** the brief. It is the blueprint: what must be argued, what facts must be treated as **plausible**, what authority must be cited, and what the **record gate** permits—so the final response brief is tight, checkable, and complete.

## Non‑negotiables

1. **Preserve movant order:** The response’s **ARGUMENT** section MUST track the movant’s headings **in the same order** (preferably verbatim).
2. **No lumping:** When qualified immunity (QI) is raised, analysis must be **per officer** (prong 1 + prong 2) for every claim/issue where the officer is a movant.
3. **Rule 12 record gate discipline:** Do not rely on extra-record facts unless clearly permissible or explicitly flagged as conversion risk.
4. **Video discipline:** Separate **authenticity** from **interpretation**; do not concede interpretation where competing inferences exist. Do **not** concede authenticity unless explicitly instructed — always check `STRATEGY.yaml` for case-specific authenticity posture. Defendants bear burden under FRE 901(a).

---

## The Job

1. Receive the movant’s arguments/headings and the claims/issues attacked
2. Ask **3–5 essential** clarifying questions (lettered options)
3. Generate a structured **RRD** that:
   - mirrors the motion’s heading order
   - breaks work into small, checkable “Response Units” (RUs)
   - forces officer-by-officer QI completion where needed
4. Save to `responses/<response-due-date>/<motion-folder>/rrd.yaml`
5. Be **idempotent**: re-running updates/merges without duplicating RUs

**Important:** Do **NOT** draft the final response brief. Only produce the RRD.

**Required companion skill:** Apply `drafting-section-1983-complaints` whenever the RRD evaluates complaint sufficiency, identifies an amendment, or specifies an amendment proffer. Each claim against each officer must follow **Element → Facts → Inference → Result**, with qualified immunity addressed officer by officer.

---

## Rule 12 Guardrails (Do Not Violate)

- Treat well‑pleaded complaint facts as true; draw reasonable inferences for the plaintiff.
- Do not resolve credibility disputes or competing inferences against plaintiff.
- Identify what the court may consider without conversion:
  - complaint + exhibits attached to complaint
  - judicial notice (typically existence/filing, not truth of disputed facts)
  - incorporation-by-reference / central documents (referenced + integral + authenticity not disputed)
- Motion-attached exhibits (video/BWC) defeat pleaded allegations only if they **blatantly contradict** them.
- If a needed fact is not safely in the Rule 12 record gate, mark it as a **GAP** and route to amendment or later proof.

---

## Step 1 — Clarifying Questions (ask 3–5 only)

Ask only what is needed to structure the RRD and properly gate the record.

### Required Questions (use this format)

1. **Do you have the motion’s headings/outline to preserve?**  
   A. Yes — I will paste the Table of Contents / headings verbatim  
   B. Partial — I will paste the headings I can, and you infer missing structure from the argument map I provide  
   C. No — build a best-effort outline from the motion summary I provide (higher risk)

2. **What is the record posture we must assume (Rule 12 gate)?**
   A. Pleadings only (+ judicial notice where proper)
   B. Pleadings + incorporated/central documents (authenticity not disputed)
   C. Pleadings + incorporated/central documents (authenticity IS disputed — challenge under FRE 901(a))
   D. Pleadings + response-attached exhibits (conversion risk acknowledged)
   E. Unsure → treat as A

3. **Is video/BWC in play for this motion?**  
   A. No  
   B. Yes — motion relies on it and court has access  
   C. Yes — motion relies on it but court access is unclear/disputed  
   D. Yes — we have it but the motion does not rely on it

4. **Which officers are moving, and is QI raised?**  
   A. One officer; QI raised  
   B. Multiple officers; QI raised  
   C. Officers moving; QI not raised  
   D. Unsure → assume QI raised and require officer-by-officer mapping

5. **Desired outcome**  
   A. Deny in full  
   B. Deny in part (identify which issues can be narrowed)  
   C. Preserve leave to amend in the alternative  
   D. Other: [specify]

User can reply like: `1A, 2A, 3B, 4B, 5C`.

---

## Step 2 — Deterministic IDs + Idempotence (lightweight but required)

This skill MUST be idempotent. It MUST also generate deterministic IDs so re-runs update existing work instead of duplicating it.

### Deterministic RU IDs

Each RU gets an ID derived from a stable fingerprint:

**Fingerprint (RU):**

```
ru|<motion_folder>|<movant_heading>|<claim_key>|<issue_key>|<officer_name_or_ALL>
```

Normalize each component: lowercase, trim, collapse spaces, strip punctuation except `-_/`.

Compute:

- `sha256(fingerprint)` → first 10 hex chars → uppercase
- RU ID format: `RU-<HASH10>`

### Merge behavior (on re-run)

If `rrd.yaml` exists:

- Match RUs by `id`
- If exists: update generated fields, preserve `user_notes`, `status`, and any `manual:*` fields
- If missing: append as new RU
- If old RU not regenerated: keep it, mark `status: stale` (do not delete)

---

## Step 3 — RRD Structure (officers)

The generated `rrd.yaml` MUST include these sections.

### 1) Matter Snapshot

- case caption / docket (as provided)
- motion title and filing date (if known)
- response due date
- record gate assumption

### 2) Motion Outline (Required)

A list capturing the movant’s headings **in order** (verbatim if provided).

```yaml
motion_outline:
  - ordinal: "I"
    heading: "..."
  - ordinal: "II.A"
    heading: "..."
```

### 3) Response Outline Contract (Required)

Explicitly states the rule:

- The response brief’s **ARGUMENT** section MUST reproduce `motion_outline[*].heading` in the same order.
- Each heading maps to one or more RU IDs.

```yaml
response_outline:
  - ordinal: "II.A"
    heading: "II.A. Probable Cause for ..."
    ru_ids: ["RU-...", "RU-..."]
```

### 4) Argument Map

A table-like mapping for each movant heading:

- targeted claim/element
- officers affected
- controlling standard
- key pleaded facts (cite placeholders)
- counter-authority targets
- video usage (if any)
- RU IDs that satisfy it

### 5) Claim × Officer Matrix (Required when QI is raised)

Prevents lumping by enforcing, per claim and per officer:

- alleged acts/omissions
- knowledge/observations (if relevant)
- timing/opportunity (if relevant)
- cite placeholders: complaint ¶ / exhibit page / BWC timestamp
- **GAP** flags + mitigation

### 6) Response Units (RU) — the core deliverable

Create one RU per:

- **(movant heading) × (claim/issue) × (officer)**

Only use `officer: ALL` if the issue is purely legal and genuinely identical.

Each RU MUST be checkable and must include:

```yaml
response_units:
  - id: "RU-XXXXXXXXXX"
    movant_heading_ordinal: "II.A"
    movant_heading: "II.A. ..."
    title: "Short name"
    attacked_claim: "<claim_key>"
    attacked_issue: "<issue_key>" # e.g., pc_public_intox, qi_prong1, qi_prong2
    officer: "Officer Name|ALL"
    movants_ask: "dismiss|grant_qi|other"
    record_gate:
      posture: "pleadings_only|judicial_notice|incorporation|conversion_risk"
      materials:
        - cite: "Complaint ¶__"
          source: "complaint|complaint_exhibit|motion_attachment|judicial_notice|incorporated_document"
      video:
        in_play: true|false
        court_has_access: true|false|null
        authenticity: "concede|contest|unknown"
        interpretation: "disputed|undisputed"
        key_timestamps: ["mm:ss", "mm:ss"]
    controlling_standard_required:
      - "Element/test checklist items to include in the brief"
    record_facts_required:
      - "F1: ... — cite: Complaint ¶__ / timestamp"
    claim_pleading_contract:
      standard:
        elements: []
        verified_authority: []
      facts:
        officer_specific_allegations: []
        complaint_cites: []
      inference:
        text: ""
        element_supported: ""
      qualified_immunity:
        prong_1_application: []
        prong_2_clearly_established_authority: []
      result:
        requested_sentence: ""
    movant_framing_to_neutralize:
      - "M1: ... — response constraint at Rule 12"
    counter_authority_required:
      - "Case: proposition"
    rebuttal_logic_required:
      - "Syllogism / logic chain"
      - "Backup framing"
    qualified_immunity_requirements:
      applies: true|false
      prong_1_violation_requirements: []
      prong_2_clearly_established_requirements: []
      officer_specific_application_required: true|false
    done_test:
      - "If H1 is true, movant loses — how verified"
      - "If H1 false, mitigation"
    exhibits_citations_needed:
      - "BWC mm:ss — purpose"
      - "Complaint ¶__"
    requested_ruling: "Deny dismissal of ...; deny QI at pleadings stage."
    status: "draft|ready|stale"
    user_notes: ""
```

### 7) Video / BWC Dispute Map (Conditional)

If video is in play, add a map that prevents accidental interpretation concessions.

```yaml
video_dispute_map:
  - id: "VDM-XXXXXXXXXX"
    movant_heading_ordinal: "II.A"
    issue: "..."
    timestamp: "mm:ss"
    plaintiff_allegation: "..."
    defense_video_claim: "..."
    classification: "blatantly_contradicts|ambiguous|supports_plaintiff|supports_defense"
    preserved_inference: "..."
    drafting_instruction: "Neutral description + plaintiff-favorable inference; do not concede interpretation."
```

### 8) Standards Library

Centralize reusable standards:

- Rule 12 plausibility + inference posture
- probable cause / arguable probable cause (as applicable)
- QI prong 1 / prong 2 framing guidance (pleadings stage)
- claim elements and verified authority for each attacked claim

### 9) Evidence & Exhibit Plan

Inventory of what exists and whether it is usable at Rule 12:

- complaint + exhibits
- incorporated documents
- judicial notice candidates (existence only unless undisputed)
- video/transcript availability and citation method (timestamps, transcript lines)

### 10) Risk Register

For each major risk:

- risk statement
- why it matters (dismissal/QI/waiver)
- mitigation
- trigger condition

### 11) Compliance & Packaging

Minimal checklist:

- response brief
- appendix/exhibits (if permitted)
- proposed order (if required)
- certificate of service

### 12) Open Questions

Remaining unknowns that block drafting.

---

## Output

- **Format:** YAML (`rrd.yaml`)
- **Location:** `responses/<response-due-date>/<motion-folder>/`
- **Filename:** `rrd.yaml`

---

## Checklist (must pass)

- [ ] Motion headings captured in `motion_outline` in correct order
- [ ] `response_outline` preserves the same order and maps headings to RU IDs
- [ ] Each movant heading has at least one RU
- [ ] If QI is raised, each relevant RU is officer-specific (no lumping)
- [ ] Each claim/officer RU states the elements, officer-specific facts, element-specific inference, and requested result
- [ ] Each individual-capacity RU separately completes QI prong one and prong two for that officer
- [ ] Record gate is explicitly stated for each RU
- [ ] Video authenticity vs interpretation is separated; interpretation not conceded where disputed
- [ ] Deterministic RU IDs + idempotent merge behavior
- [ ] Saved to `responses/<due-date>/<motion-folder>/rrd.yaml`
