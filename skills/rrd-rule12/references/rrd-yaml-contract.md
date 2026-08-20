# RRD YAML Contract

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
