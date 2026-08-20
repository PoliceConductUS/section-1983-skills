---
name: rrd-rule12
description:
  "Use when creating a response plan, checklist, or Response Requirements
  Document for a Rule 12 motion to dismiss in a Section 1983 case, including
  qualified immunity, Nieves retaliatory-arrest issues, record gating,
  incorporation by reference, or motion-attached BWC/video."
---

# SKILL.md — rrd-rule12

Generate a **Response Requirements Document (RRD)** that functions as the
drafting blueprint for an opposition/response to a **Rule 12 motion to dismiss**
(especially **Rule 12(b)(6)**) in §1983 cases.

An RRD is **not** the brief. It is a checkable plan: what must be argued, what
facts must be treated as **plausible**, what authority must be cited, what the
**record gate** allows, and what materials (if any) can be referenced at this
stage.

This skill is designed to be run **once per motion**. If there are two motions
(e.g., **officers MTD** and **city MTD**), run it **twice** and write to two
separate folders.

---

## The Job

1. Receive the motion arguments the user must respond to (or a summary)
2. Ask **3–5 essential** clarifying questions (lettered options)
3. Generate a structured **RRD** (Rule 12 optimized)
4. Save to the response path required by the repository; if none is defined,
   default to `responses/<response-due-date>/<motion-folder>/rrd.yaml`
5. Be **idempotent**: re-running the skill updates/merges the existing
   `rrd.yaml` without duplicating Response Units.

**Important:** Do **NOT** draft the final response brief. Only produce the RRD.

**Required companion skills:** Apply `drafting-section-1983-complaints` whenever
the RRD evaluates whether a § 1983 claim is plausibly pleaded, identifies an
amendment, or specifies an amendment proffer. Also apply
`drafting-false-arrest-complaints` when probable cause, arguable probable cause,
alternative offenses, seizure timing, later alleged resistance, or incorporated
arrest video is material. Run `audit-authorities` before marking an
authority-dependent unit ready.

Use `rrd-rule12-officers` for an individual-officer motion and `rrd-rule12-city`
for a municipal motion. This skill owns canonical identifiers, common field
names, the 3–5-question total, and shared guardrails. A specialization may add
fields and replace a base question with a narrower one; it may not create
aliases, require an additional question set, or remove record, amendment,
event-stage, or authority requirements.

---

## Rule 12 Guardrails (Do Not Violate)

- **Pleadings-first:** Treat the complaint’s well-pleaded facts as true and draw
  reasonable inferences for the nonmovant.
- **No fact finding:** Do not resolve credibility disputes or competing
  inferences against the plaintiff.
- **Record gate:** Identify what the court may consider without conversion:
  - complaint + attached exhibits
  - judicially noticeable materials (usually existence/filing, not truth of
    disputed facts)
  - documents incorporated-by-reference / central-to-claim _if referenced and
    authenticity is not disputed_
- **Exhibit discipline:** If the motion attaches evidence (e.g., BWC/video),
  separate:
  - **Authenticity** (do **not** concede unless explicitly instructed — check
    STRATEGY.yaml and case-specific instructions; Defendants bear burden under
    FRE 901(a))
  - **Interpretation** (do **not** concede if competing inferences exist)
  - Video defeats allegations only when it **blatantly contradicts** them.
  - Always check `STRATEGY.yaml` for case-specific authenticity posture before
    defaulting.
- **Defendant specificity:** For individuals and qualified immunity:
  requirements must be **per claim, per defendant** (no lumping).
- **No new facts:** Do not rely on new facts outside the record gate. If a fact
  is missing, mark a **gap** and route it to amendment or later proof.

---

## Step 1 — Clarifying Questions (3–5 only)

Ask only what is necessary to correctly gate the record, pick standards, and
structure the RRD.

### Required Questions (use these exact shapes)

1. **Which motion is this RRD for?** A. Officers MTD (individual defendants)  
   B. City/municipality MTD  
   C. Other: [specify]

2. **What is the procedural vehicle and stage?** A. Rule 12(b)(6)  
   B. Rule 12(b)(1)  
   C. Mixed 12(b)(1)/(6)  
   D. Rule 56 (summary judgment)  
   E. Other: [specify]

3. **What "record gate" should we assume for drafting?** A. Pleadings only (+
   judicial notice where proper) B. Pleadings + incorporated/central documents
   (authenticity not disputed) C. Pleadings + incorporated/central documents
   (authenticity IS disputed — challenge under FRE 901(a)) D. Pleadings +
   response-attached exhibits (conversion risk acknowledged) E. Unsure → treat
   as **A** (most conservative)

4. **Is video/BWC in play for this motion?** A. No  
   B. Yes — motion relies on it and court has access  
   C. Yes — motion relies on it but court access is unclear / disputed  
   D. Yes — we have it but the motion did not attach it

5. **What is the desired outcome?** A. Deny in full  
   B. Deny in part (identify which claims can be narrowed)  
   C. Preserve leave to amend in the alternative  
   D. Procedural ruling (strike/convert/not convert/other)

Allow the user to reply like: `1A, 2A, 3A, 4B, 5C`.

---

## Step 2 — Idempotence + Deterministic IDs (Required)

### Why this matters

If this skill is re-run after edits or after the movant files a reply, you need
the generator to **update** rather than create duplicates. That requires
**stable, deterministic IDs**.

### Deterministic ID Rules (MUST)

All generated objects that can repeat across runs MUST have a deterministic `id`
based on a **fingerprint hash**.

Objects that MUST have deterministic IDs:

- `response_units[]`
- `strategic_arguments_library.arguments[]`
- `argument_map[]` items (if you keep them as discrete objects)
- `video_dispute_map[]` items (when present)
- `risk_register[]` items (optional but recommended)
- `amendment_handoff[]`

### Fingerprint

A fingerprint is a _stable_ string derived from the essence of the thing, then
hashed.

**Normalization rules:**

- lowercase
- trim whitespace
- collapse internal whitespace to a single space
- remove punctuation that does not affect meaning (keep slashes, hyphens)
- do **not** include ordering/sequence numbers
- do **not** include timestamps like “generated_at”

**Hash rule:**

- `sha256(fingerprint)` → take the first 10 hex chars → uppercase
- Use that as an ID suffix.

### ID formats

- Response Units: `RU-<HASH10>`
- Strategic arguments: `SA-<HASH10>`
- Video dispute map items: `VDM-<HASH10>`
- Risks: `RISK-<HASH10>`
- Argument map entries: `AM-<HASH10>`
- Amendment handoffs: `AH-<HASH10>`

### Fingerprint recipes (canonical)

These are the default recipes; if the user supplies claim IDs from a `claims/`
folder, prefer those keys.

**Response Unit fingerprint:**

```
ru|<motion_key>|<claim_key>|<defendant_key>|<event_stage>|<challenged_conduct>|<movant_cluster_key>|<attacked_issue_key>
```

**Strategic argument fingerprint:**

```
sa|<motion_key>|<legal_theory_key>|<proposition_normalized>
```

**Video dispute map fingerprint:**

```
vdm|<motion_key>|<issue_key>|<timestamp>|<plaintiff_allegation_normalized>|<defense_claim_normalized>
```

**Risk fingerprint:**

```
risk|<motion_key>|<risk_key>|<risk_statement_normalized>
```

**Argument map fingerprint:**

```
am|<motion_key>|<movant_heading_normalized>|<targeted_claim_key>|<defense_type_key>
```

**Amendment handoff fingerprint:**

```
ah|<motion_key>|<motion_or_ruling_premise>|<claim_key>|<defendant_key>|<event_stage>|<exact_defect_normalized>
```

### Merge rules (idempotent updates)

When `rrd.yaml` already exists, the generator MUST:

1. Parse existing YAML.
2. Build an index by `id` for all deterministic objects.
3. For each newly generated object:
   - If `id` exists → **update** machine-managed fields; preserve user notes.
   - If `id` does not exist → **append**.
4. For objects present in the old file but not regenerated:
   - Keep them, but mark with `status: stale` (do not delete automatically).

Apply these same update-by-ID and stale-item rules to `amendment_handoff[]`; do
not duplicate a cure when its deterministic ID already exists.

**User-preserved fields** (never overwrite on a regenerated object if present):

- `user_notes`
- `status` (unless it is missing; default to `draft`)
- `worklog`
- `owner`
- any field under a `manual:` subtree (reserved)

The generated transition from an item no longer produced to `status: stale` is
the sole exception to status preservation. If the item is produced again,
restore its last non-stale user status when recorded; otherwise use the schema
default.

---

## Output: File Layout

- **Format:** YAML (`rrd.yaml`)
- **Location:** use the repository-defined response path; default to
  `responses/<response-due-date>/<motion-folder>/rrd.yaml`
- **Filename:** fixed `rrd.yaml`

Example:

```
responses/
└── 2026-01-29/
    ├── officers-mtd/
    │   ├── SOURCE.yaml
    │   └── rrd.yaml
    └── city-mtd/
        ├── SOURCE.yaml
        └── rrd.yaml
```

Create or update source metadata only when the repository's source schema
requires it. `rrd.yaml` should reference repository source IDs when available.

---

## Required YAML Contract (rrd.yaml)

### Top-level fields (required)

```yaml
meta:
  rrd_version: "1.1"
  generated_at_utc: "YYYY-MM-DDTHH:MM:SSZ"
  motion_key: "officers-mtd|city-mtd|<custom>"
  response_due_date: "YYYY-MM-DD"
  id_strategy: "sha256-fingerprint-10"
matter_snapshot:
  case_name: ""
  case_number: ""
  court: ""
  motion_being_responded_to: ""
  response_posture: "oppose|partial|support"
  record_gate_assumption: "pleadings_only|incorporation|includes_response_exhibits"
response_objectives: []
argument_map: [] # optional but recommended
strategic_arguments_library:
  notes: ""
  arguments: []
response_units: []
standards_library: {}
evidence_exhibit_plan: {}
risk_register: []
compliance_packaging: {}
amendment_handoff: []
open_questions: []
```

### Response Unit contract (required)

Each `response_units[]` entry MUST include:

```yaml
- id: "RU-XXXXXXXXXX"
  title: ""
  attacked_claim: "" # claim_key preferred
  attacked_issue: "" # e.g., "qi_prong_1", "arguable_pc", "monell_policy"
  defendant: "" # defendant_key or "ALL" for purely legal items
  event_stage: "" # encounter|arrest_decision|seizure|force|continued_custody|report|prosecution|other
  challenged_conduct: ""
  event_start: ""
  event_end: ""
  movants_ask: "" # dismiss / grant QI / etc.
  movant_argument_cluster: "" # stable key, not a sequence number
  record_gate:
    classification: "pleadings_only|judicial_notice|incorporation|conversion_risk"
    materials_relied_on:
      - material_type: "complaint|complaint_exhibit|motion_attachment|judicial_notice|incorporated_document"
        source_id: "" # points to SOURCE.yaml entry when applicable
        cite: "" # complaint ¶, exhibit page, docket cite, timestamp, etc.
    video:
      in_play: true|false
      court_has_access: true|false|null
      authenticity: "concede|contest|unknown"
      interpretation: "disputed|undisputed"
  controlling_standard_required: []
  record_facts_required: []
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
            court_and_publication_status: ""
            decision_date: ""
            pre_event: true|false|null
            holding_classification: "holding|alternative_holding|implicit_holding|dicta|non_holding|appellate_fact|persuasive_only"
            pinpoint: ""
            identity_status: "verified|gap"
            procedural_posture: ""
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
  movants_supporting_facts_to_neutralize: []
  counter_authority_required: []
  rebuttal_logic_required: []
  falsifiable_hypothesis: []
  exhibits_citations_needed: []
  requested_ruling: ""
  status: "draft|ready|stale"
  user_notes: "" # preserved on regen
```

For a false-arrest unit, use this linked offense-and-element schema so a later
fact cannot silently support an earlier arrest decision:

```yaml
seizure_point: ""
suspected_offenses:
  - offense_key: ""
    offense: ""
    legal_source: ""
    offense_elements:
      - element_key: ""
        element: ""
        facts_known_then: []
        negating_facts: []
        later_only_facts: []
        probable_cause_conclusions: []
        arguable_probable_cause_conclusions: []
```

Use this contract for every proposed amendment:

```yaml
amendment_handoff:
  - id: "AH-XXXXXXXXXX" # hash motion|premise|claim|defendant|event_stage|defect
    motion_or_ruling_premise: ""
    claim: ""
    defendant: ""
    event_stage: ""
    exact_defect: []
    proposed_factual_cure: []
    source_or_supported_inference: []
    proposed_complaint_version:
      "next numbered version or repository-defined version"
    target_complaint_section_or_count: []
    target_paragraphs: []
    clearly_established_law_cure:
      applicable: true|false
      cure: {} # use {} only when applicable is false
    nonfutility_explanation: ""
    status: "draft|supported|needs_narrowing|filing_critical_gap|stale"
```

A brief assertion or anticipated discovery cannot cure a missing complaint
allegation.

### Video dispute map (conditional)

If video/BWC is in play, include:

```yaml
video_dispute_map:
  - id: "VDM-XXXXXXXXXX"
    issue: ""
    plaintiff_allegation: ""
    complaint_cite: ""
    defense_video_claim: ""
    timestamp: "mm:ss"
    classification: "blatantly_contradicts|ambiguous|supports_plaintiff|supports_defense"
    preserved_inference: ""
    drafting_instruction: ""
    user_notes: ""
```

---

## Step 3 — RRD Sections (content requirements)

Generate the RRD with these sections (compatible with your existing pattern),
but now enforce the YAML contract above.

### 1) Matter Snapshot

- include `motion_key` and `record_gate_assumption` explicitly

### 2) Response Objectives

Specific, checkable outcomes (deny/dismiss/leave to amend).

### 3) Argument Map

Map each movant heading/argument to:

- targeted claim/element
- defendants affected
- controlling standard
- record gate constraints
- key pleaded facts
- counter-authority
- core rebuttal
- risk + mitigation

### 4) Claim × Defendant Matrix (Required for officers; recommended for city)

For each claim, list each moving defendant and the pleaded linkage. Mark gaps.

### 5) Response Units (RU) — the main body

Default granularity: **(claim, defendant, argument cluster)**. Only use
`defendant: ALL` for pure-legal arguments with identical application.

Every RU must include:

- record gate (and video stance if relevant)
- controlling standard
- defendant-specific facts required as plausible
- a complete claim-pleading contract: **Element → Facts → Inference → Result**
- movant framing to neutralize
- counter-authority
- rebuttal logic
- falsifiable “done test”
- exhibits/citations needed
- requested ruling sentence

### 6) Standards Library

Reusable standards you expect to cite. If retaliatory arrest is attacked,
include:

- Nieves framework
- Nieves exception requirements and “objective evidence”
- two-path plan (no PC vs exception even if PC)

### 7) Evidence & Exhibit Plan

Inventory what exists and whether it is proper at Rule 12; explicitly flag
conversion risk.

### 8) Risk Register

Dismissal/QI/waiver risks + triggers + mitigations.

### 9) Compliance & Packaging

Brief components checklist (you can ignore page count for planning, but still
record it if known).

### 10) Open Questions

Unknowns that block drafting.

---

## Step 4 — Source metadata (when repository-required)

If the repository requires `SOURCE.yaml` and it is missing, create it under that
repository's schema. A minimal fallback is:

```yaml
meta:
  source_version: "1.0"
  created_at_utc: "YYYY-MM-DDTHH:MM:SSZ"
sources:
  - id: "SRC-<HASH10>"
    type: "complaint|motion|order|video|docket|exhibit|other"
    title: ""
    location: "" # file path, docket entry, or URL (if public)
    notes: ""
```

`rrd.yaml` should reference these by `source_id` whenever possible.

---

## Generator Checklist (must pass)

Before saving:

- [ ] Asked only 3–5 clarifying questions with lettered options
- [ ] Deterministic IDs generated for RUs (and other objects as applicable)
- [ ] Existing `rrd.yaml` merged idempotently (no duplicates)
- [ ] Claim × Defendant matrix present (especially for officer motion)
- [ ] Every claim-focused RU states the elements, defendant-specific facts,
      element-specific inference, and requested result
- [ ] Every individual-capacity RU addresses both qualified-immunity prongs
      separately for each defendant
- [ ] Every prong-two analysis contains the complete clearly-established-law
      object and is not `ready` with a filing-critical GAP
- [ ] Every RU identifies the event stage and challenged conduct; false-arrest
      units contain the arrest-decision fields
- [ ] Every RU includes record gate + standard + facts + authority + logic +
      done test + requested ruling
- [ ] If video is in play, included `video_dispute_map` and did not concede
      interpretation
- [ ] Judicial notice used for existence/filing only unless undisputed
- [ ] Gaps are explicitly labeled with mitigation (amendment / later proof)
- [ ] Every proposed amendment has a complete `amendment_handoff` entry
- [ ] Saved to the repository-defined response path, or the documented default
      when none exists
- [ ] No internal tool artifacts in output
