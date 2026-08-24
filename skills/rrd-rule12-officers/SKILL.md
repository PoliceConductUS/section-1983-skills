---
name: rrd-rule12-officers
description:
  "Use when creating a response plan, checklist, or Response Requirements
  Document for an officers' Rule 12(b)(6) motion in a Section 1983 case,
  especially when qualified immunity requires claim-by-claim and
  officer-by-officer analysis in the movant's heading order."
---

# SKILL.md — rrd-rule12-officers

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `motion` contains the officers' Rule 12 motion and ordered arguments.
- `record` contains the operative pleading and approved officer-specific record.
- `authorities` contains approved Rule 12, claim, and qualified-immunity law.

Target is required in `motion`. Internet is `disabled`. Return the officer-
motion RRD as a canonical output-relative path and deterministic bytes; only the
trusted host may publish it append-immutable. Report missing headings,
officer-act facts, record support, authority, or amendment information as a gap
without drafting the response brief.

Create a detailed **Response Requirements Document (RRD)** for an **officers’
Rule 12(b)(6) Motion to Dismiss** in a §1983 case, where **qualified immunity**
is commonly raised.

An RRD is **not** the brief. It is the blueprint: what must be argued, what
facts must be treated as **plausible**, what authority must be cited, and what
the **record gate** permits—so the final response brief is tight, checkable, and
complete.

## Non‑negotiables

1. **Preserve movant order:** The response’s **ARGUMENT** section MUST track the
   movant’s headings **in the same order** (preferably verbatim).
2. **No lumping:** When qualified immunity (QI) is raised, analysis must be
   **per officer** (prong 1 + prong 2) for every claim/issue where the officer
   is a movant.
3. **Rule 12 record gate discipline:** Do not rely on extra-record facts unless
   clearly permissible or explicitly flagged as conversion risk.
4. **Video discipline:** Separate **authenticity** from **interpretation**; do
   not concede interpretation where competing inferences exist. Do **not**
   concede authenticity unless explicitly instructed — always check
   `STRATEGY.yaml` for case-specific authenticity posture. Defendants bear
   burden under FRE 901(a).

---

## The Job

1. Receive the movant’s arguments/headings and the claims/issues attacked
2. Ask **3–5 essential** clarifying questions (lettered options)
3. Generate a structured **RRD** that:
   - mirrors the motion’s heading order
   - breaks work into small, checkable “Response Units” (RUs)
   - forces officer-by-officer QI completion where needed
4. Return `rrd.yaml` bytes with a canonical output-relative path for trusted-
   host publication.
5. Be **idempotent**: merge without duplicating RUs only when a prior RRD is
   expressly supplied in `record`, then return a new append-immutable artifact.

**Important:** Do **NOT** draft the final response brief. Only produce the RRD.

**Required companion skills:** Apply `drafting-section-1983-complaints` whenever
the RRD evaluates complaint sufficiency, identifies an amendment, or specifies
an amendment proffer. Also apply `drafting-false-arrest-complaints` when
probable cause, arguable probable cause, alternative offenses, seizure timing,
later alleged resistance, or incorporated arrest video is material. Run
`audit-authorities` before marking a qualified-immunity or authority-dependent
unit ready.

Apply this skill as an officers-specific overlay on `rrd-rule12`. The base skill
controls canonical IDs, common field names, record-gate structure, amendment
handoffs, and the total of 3–5 clarifying questions. The fields below add
officer and qualified-immunity detail; they do not create aliases for base
fields.

---

## Rule 12 Guardrails (Do Not Violate)

- Treat well‑pleaded complaint facts as true; draw reasonable inferences for the
  plaintiff.
- Do not resolve credibility disputes or competing inferences against plaintiff.
- Identify what the court may consider without conversion:
  - complaint + exhibits attached to complaint
  - judicial notice (typically existence/filing, not truth of disputed facts)
  - incorporation-by-reference / central documents (referenced + integral +
    authenticity not disputed)
- Motion-attached exhibits (video/BWC) defeat pleaded allegations only if they
  **blatantly contradict** them.
- If a needed fact is not safely in the Rule 12 record gate, mark it as a
  **GAP** and route to amendment or later proof.

---

## Step 1 — Officers-Specific Clarifying Questions

Ask 3–5 questions total across this skill and `rrd-rule12`. Replace a base
question with a narrower question below when useful; do not ask both sets.

### Required Questions (use this format)

1. **Do you have the motion’s headings/outline to preserve?**  
   A. Yes — I will paste the Table of Contents / headings verbatim  
   B. Partial — I will paste the headings I can, and you infer missing structure
   from the argument map I provide  
   C. No — build a best-effort outline from the motion summary I provide (higher
   risk)

2. **What is the record posture we must assume (Rule 12 gate)?** A. Pleadings
   only (+ judicial notice where proper) B. Pleadings + incorporated/central
   documents (authenticity not disputed) C. Pleadings + incorporated/central
   documents (authenticity IS disputed — challenge under FRE 901(a)) D.
   Pleadings + response-attached exhibits (conversion risk acknowledged) E.
   Unsure → treat as A

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

This skill MUST be idempotent. It MUST also generate deterministic IDs so
re-runs update existing work instead of duplicating it.

### Deterministic RU IDs

Each RU gets an ID derived from a stable fingerprint:

**Fingerprint (RU):**

```
ru|<motion_key>|<claim_key>|<defendant_key>|<event_stage>|<challenged_conduct>|<movant_cluster_key>|<attacked_issue_key>
```

Normalize each component: lowercase, trim, collapse spaces, strip punctuation
except `-_/`.

Compute:

- `sha256(fingerprint)` → first 10 hex chars → uppercase
- RU ID format: `RU-<HASH10>`

### Merge behavior (on re-run)

If `rrd.yaml` exists:

- Match RUs by `id`
- If exists: update generated fields, preserve `user_notes`, `status`, and any
  `manual:*` fields
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

- The response brief’s **ARGUMENT** section MUST reproduce
  `motion_outline[*].heading` in the same order.
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

Only use `defendant: ALL` if the issue is purely legal and genuinely identical.

Each RU MUST be checkable and must include:

```yaml
response_units:
  - id: "RU-XXXXXXXXXX"
    movant_heading_ordinal: "II.A"
    movant_heading: "II.A. ..."
    title: "Short name"
    attacked_claim: "<claim_key>"
    attacked_issue: "<issue_key>" # e.g., pc_public_intox, qi_prong1, qi_prong2
    defendant: "Officer Name|ALL"
    event_stage: "encounter|arrest_decision|seizure|force|continued_custody|report|prosecution|other"
    challenged_conduct: ""
    event_start: ""
    event_end: ""
    movants_ask: "dismiss|grant_qi|other"
    movant_argument_cluster: "<stable key>"
    record_gate:
      classification: "pleadings_only|judicial_notice|incorporation|conversion_risk"
      materials_relied_on:
        - material_type: "complaint|complaint_exhibit|motion_attachment|judicial_notice|incorporated_document"
          source_id: ""
          cite: "Complaint ¶__"
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
        defendant_specific_allegations: []
        complaint_cites: []
      inference:
        text: ""
        element_supported: ""
      qualified_immunity:
        applies: true|false
        prong_1_application: []
        clearly_established_law:
          applicable: true|false
          event_date: ""
          precise_right_or_rule: ""
          authorities:
            - citation: ""
              identity_status: "verified|gap"
              court_and_publication_status: ""
              decision_date: ""
              pre_event: true|false|null
              holding_classification: "holding|alternative_holding|implicit_holding|dicta|non_holding|appellate_fact|persuasive_only"
              procedural_posture: ""
              pinpoint: ""
              later_history: ""
              rule_of_orderliness: ""
              material_similarities: []
              material_differences: []
              fair_warning_explanation: ""
              audit_status: "verified|needs_narrowing|filing_critical_gap"
          material_similarities: []
          material_differences: []
          fair_warning_explanation: ""
          orderliness_and_later_history: ""
          status: "verified|needs_narrowing|filing_critical_gap|not_applicable"
      result:
        requested_sentence: ""
    movants_supporting_facts_to_neutralize:
      - "M1: ... — response constraint at Rule 12"
    counter_authority_required:
      - "Case: proposition"
    rebuttal_logic_required:
      - "Syllogism / logic chain"
      - "Backup framing"
    qualified_immunity_requirements:
      applies: true|false
      prong_1_violation_requirements: []
      clearly_established_law_complete: true|false
      officer_specific_application_required: true|false
    falsifiable_hypothesis:
      - "If H1 is true, movant loses — how verified"
      - "If H1 false, mitigation"
    exhibits_citations_needed:
      - "BWC mm:ss — purpose"
      - "Complaint ¶__"
    requested_ruling: "Deny dismissal of ...; deny QI at pleadings stage."
    status: "draft|ready|stale"
    user_notes: ""
```

For a false-arrest unit, use the canonical linked `seizure_point` and
`suspected_offenses[].offense_elements[]` schema in `rrd-rule12`. Complete the
contemporaneous, negating, later-only, actual-probable-cause, and
arguable-probable-cause fields for each offense element.

Use the canonical `amendment_handoff[]` object from `rrd-rule12` for every
proposed cure, including its deterministic ID, proposed complaint version,
target section/count and paragraph placement, clearly-established-law cure,
nonfutility explanation, and GAP status. Set `defendant` to the individual
officer. A brief assertion or anticipated discovery cannot cure a missing
complaint allegation.

### 7) Video / BWC Dispute Map (Conditional)

If video is in play, add a map that prevents accidental interpretation
concessions.

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
    drafting_instruction:
      "Neutral description + plaintiff-favorable inference; do not concede
      interpretation."
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
- video/transcript availability and citation method (timestamps, transcript
  lines)

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
- **Publication:** canonical output-relative path through the trusted host
- **Filename:** `rrd.yaml`

---

## Checklist (must pass)

- [ ] Motion headings captured in `motion_outline` in correct order
- [ ] `response_outline` preserves the same order and maps headings to RU IDs
- [ ] Each movant heading has at least one RU
- [ ] If QI is raised, each relevant RU is officer-specific (no lumping)
- [ ] Each claim/officer RU states the elements, officer-specific facts,
      element-specific inference, and requested result
- [ ] Each individual-capacity RU separately completes QI prong one and prong
      two for that officer
- [ ] Each prong-two analysis contains the complete clearly-established-law
      object and is not `ready` with a filing-critical GAP
- [ ] Each RU identifies event stage and challenged conduct; false-arrest units
      include the arrest-decision fields
- [ ] Record gate is explicitly stated for each RU
- [ ] Video authenticity vs interpretation is separated; interpretation not
      conceded where disputed
- [ ] Deterministic RU IDs + idempotent merge behavior
- [ ] Every proposed amendment has a complete `amendment_handoff` entry
- [ ] Returned with a canonical output-relative path for append-immutable
      trusted-host publication
