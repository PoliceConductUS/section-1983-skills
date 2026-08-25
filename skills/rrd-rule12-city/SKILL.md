---
name: rrd-rule12-city
description:
  "Use when creating a response plan, checklist, or Response Requirements
  Document for a City or municipality's Rule 12(b)(6) motion in a Section 1983
  case, especially when Monell theories, pleading-stage record gating, and the
  movant's heading order control the response."
---

# SKILL.md — ~~rrd-rule12-city~~

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `motion` contains the municipality's Rule 12 motion and ordered arguments.
- `record` contains the operative pleading and approved Monell record.
- `authorities` contains approved Rule 12, constitutional, and Monell law.
- `municipal-profile` contains the four validated ordinary Issue #31 output
  files.

Read
[municipal profile consumption](references/municipal-profile-consumption.md)
before mapping the motion's attacks.

Target is required in `motion`. Internet is `disabled`. Return the city-motion
RRD as a canonical output-relative path and deterministic bytes; only the
trusted host may publish it append-immutable. Report missing motion headings,
Monell theory facts, record support, authority, or amendment information as a
gap without drafting the response brief.

Create a detailed **Response Requirements Document (RRD)** for a
**City/municipality Rule 12(b)(6) Motion to Dismiss** in a §1983 case (Monell).

An RRD is **not** the brief. It is the blueprint: what must be argued, what must
be plausibly alleged, what authority must be cited, and what the Rule 12
**record gate** permits.

## Non‑negotiables

1. **Preserve movant order:** The response’s **ARGUMENT** section MUST track the
   city’s motion headings **in the same order** (preferably verbatim).
2. **Monell element discipline:** Under each heading, organize substance by the
   **Monell element(s)** attacked (policy/custom, failure to
   train/supervise/discipline, deliberate indifference/notice, moving force
   causation, policymaker, etc.).
3. **Cross‑reference officers response:** Where appropriate, reference the
   officers response for the underlying constitutional violation; keep the city
   response focused on Monell.
4. **Rule 12 gate:** No extra-record facts; route gaps to amendment.

---

## The Job

1. Receive the motion headings and the Monell theories attacked
2. Ask **3–5 essential** clarifying questions (lettered options)
3. Generate a structured **RRD** that:
   - mirrors the motion’s heading order
   - breaks work into small Response Units (RUs)
   - maps each heading to Monell elements + required allegations
4. Return `rrd.yaml` bytes with a canonical output-relative path for trusted-
   host publication.
5. Be **idempotent** with deterministic IDs; merge a prior RRD only when it is
   expressly supplied in `record`, then return a new append-immutable artifact.

**Important:** Do **NOT** draft the final response brief. Only produce the RRD.

**Required companion skills:** Apply `drafting-section-1983-complaints` whenever
the RRD evaluates Monell pleading sufficiency, identifies an amendment, or
specifies an amendment proffer. Apply `drafting-false-arrest-complaints` when
the underlying violation turns on false arrest, probable cause, alternative
offenses, seizure timing, or incorporated arrest video. Run `audit-authorities`
before marking an authority-dependent unit ready.

Apply this skill as a municipal overlay on `rrd-rule12`. The base skill controls
canonical IDs, common field names, record-gate structure, amendment handoffs,
and the total of 3–5 clarifying questions. The fields below add Monell detail;
they do not create aliases for base fields.

Qualified immunity and its clearly-established-law prong are not municipal
defenses. Verify the underlying constitutional rule, but do not import the
individual defendant's prong-two burden into the City's Monell analysis.

---

## Rule 12 Guardrails (Do Not Violate)

- Treat well‑pleaded complaint facts as true; draw reasonable inferences for
  plaintiff.
- Do not resolve factual disputes.
- Record gate: complaint + complaint exhibits; judicial notice
  (existence/filing); incorporation-by-reference where proper.
- Do not use new facts to “fix” Monell gaps; mark **GAP** and route to
  amendment. Discovery-controlled details may refine a theory only when known
  pleaded facts already support its plausible municipal inference.

---

## Step 1 — City-Specific Clarifying Questions

Ask 3–5 questions total across this skill and `rrd-rule12`. Replace a base
question with a narrower question below when useful; do not ask both sets.

1. **Do you have the city motion’s headings/outline to preserve?**  
   A. Yes — I will paste the TOC/headings verbatim  
   B. Partial — I will paste what I have  
   C. No — build a best-effort outline from my summary

2. **Which Monell theory(ies) are you relying on (or want to preserve)?**  
   A. Policy (official policy / written policy)  
   B. Custom / widespread practice  
   C. Failure to train  
   D. Failure to supervise/discipline  
   E. Ratification / policymaker approval  
   F. Multiple (list)

3. **What is the record posture we must assume (Rule 12 gate)?**  
   A. Pleadings only (+ judicial notice where proper)  
   B. Pleadings + incorporated/central documents  
   C. Pleadings + response-attached exhibits (conversion risk)  
   D. Unsure → treat as A

4. **Do you want to cross-reference the officers response for the underlying
   violation?**  
   A. Yes — cross-reference; keep city brief focused on Monell elements  
   B. No — restate underlying violation analysis here  
   C. Mixed — restate briefly, then cross-reference

5. **Desired outcome**  
   A. Deny in full  
   B. Deny in part / narrow theories  
   C. Preserve leave to amend in the alternative  
   D. Other: [specify]

---

## Step 2 — Deterministic IDs + Idempotence (required, lightweight)

**RU fingerprint:** Use the canonical base recipe. For a City RU, set
`defendant_key` to the City, `event_stage` to the injury event stage, and
`challenged_conduct` to the identified municipal action or omission.

```
ru|<motion_key>|<claim_key>|<defendant_key>|<event_stage>|<challenged_conduct>|<movant_cluster_key>|<attacked_issue_key>
```

Normalize + `sha256` → first 10 hex chars uppercase → `RU-<HASH10>`.

Merge rules:

- update by `id`, preserve `user_notes`, `status`, and any `manual:*` subtree
- mark non-regenerated items as `stale`

---

## Step 3 — RRD Structure (city)

### 1) Matter Snapshot

- case caption / docket
- motion title/date
- due date
- record gate assumption

### 2) Motion Outline (Required)

Headings in order (verbatim if possible).

### 3) Response Outline Contract (Required)

ARGUMENT headings must mirror the motion outline in the same order and map to RU
IDs.

### 4) Monell Theory Map (Required)

A compact map of:

- theory (policy/custom/failure-to-train/etc.)
- required elements
- pleaded facts supporting each element (cite placeholders)
- the element-specific inference supported by those facts
- the requested result for that theory
- which already-plausible details remain within defendants' control
- gaps + amendment plan

### 5) Argument Map

For each movant heading:

- which Monell element(s) it targets
- what movant claims is missing
- what pleaded allegations satisfy plausibility
- counter-authority targets
- RU IDs

### 6) Response Units (RU)

Default RU granularity: **(movant heading) × (Monell element cluster)**.

Each RU must include:

```yaml
response_units:
  - id: "RU-XXXXXXXXXX"
    movant_heading_ordinal: "II.B"
    movant_heading: "II.B. ..."
    title: "Short name"
    attacked_claim: "<claim_key>"
    attacked_issue: "<element_cluster_key>"
    defendant: "<city_key>"
    event_stage: "<injury_event_stage>"
    challenged_conduct: "<identified municipal action or omission>"
    event_start: ""
    event_end: ""
    movants_ask: "dismiss|other"
    movant_argument_cluster: "<stable key>"
    monell_theory: "policy|custom|failure_to_train|failure_to_supervise|ratification|mixed"
    targeted_elements:
      - "policy_or_custom"
      - "deliberate_indifference"
      - "moving_force"
    record_gate:
      classification: "pleadings_only|judicial_notice|incorporation|conversion_risk"
      materials_relied_on:
        - material_type: "complaint|complaint_exhibit|judicial_notice|incorporated_document"
          source_id: ""
          cite: "Complaint ¶__"
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
        underlying_violation: []
        identified_municipal_path: []
        concrete_supporting_facts: []
        reasonable_municipal_inference: []
        attribution_and_notice: []
        particular_injury: []
        injury_event_stage: ""
        moving_force_mechanism: []
        information_and_belief_basis:
          known_facts: []
          controlled_information: []
          custodian: ""
          supported_inference: ""
        complaint_cites: []
      inference:
        text: ""
        element_supported: ""
        supported_alternative_inferences: []
      qualified_immunity:
        applies: false
        prong_1_application: []
        clearly_established_law:
          applicable: false
          status: "not_applicable"
      result:
        requested_sentence: ""
    movants_supporting_facts_to_neutralize: []
    counter_authority_required: []
    rebuttal_logic_required: []
    falsifiable_hypothesis: []
    exhibits_citations_needed: []
    requested_ruling: "Deny dismissal of Monell claim / theory ..."
    cross_references:
      underlying_violation:
        enabled: true|false
        reference: "" # path or anchor if provided
    status: "draft|ready|stale"
    user_notes: ""
```

Use the canonical `amendment_handoff[]` object from `rrd-rule12` for every
proposed cure, including its deterministic ID, proposed complaint version,
target section/count and paragraph placement, nonfutility explanation, and GAP
status. Set `defendant` to the City, identify the municipal theory in the claim
or defect fields, and use the particular injury's event stage. Anticipated
discovery cannot replace a presently missing plausible allegation.

### 7) Standards Library

- Monell baseline elements (policy/custom; deliberate indifference; moving
  force)
- failure-to-train/supervise standards
- pleading standards for Monell

### 8) Evidence & Exhibit Plan

Capture:

- what’s in the complaint
- which details remain within defendants' control after the complaint states a
  plausible basis
- judicial notice candidates (existence vs truth caution)

### 9) Risk Register

Common city risks:

- “single incident” problem
- conclusory policy/custom allegations
- policymaker identification gaps
- causation/moving-force gaps
- mitigation via amendment

### 10) Compliance & Packaging + Open Questions

---

## Output

- **Format:** YAML (`rrd.yaml`)
- **Publication:** canonical output-relative path through the trusted host
- **Filename:** `rrd.yaml`

---

## Checklist (must pass)

- [ ] Motion headings captured in order
- [ ] Response outline mirrors order and maps headings to RU IDs
- [ ] Monell theory map exists and is element-complete
- [ ] Each Monell theory separately maps verified elements, pleaded facts,
      element-specific inferences, and requested result
- [ ] Each theory separately states the identified path, concrete facts,
      municipal inference, attribution and notice, particular injury, injury
      event stage, and moving-force mechanism
- [ ] Information-and-belief allegations identify known facts, controlled
      information, custodian, and supported inference
- [ ] Each movant heading has at least one RU
- [ ] Record gate is explicit for each RU
- [ ] Deterministic IDs + idempotent merge behavior
- [ ] Every proposed amendment has a complete `amendment_handoff` entry
- [ ] Returned with a canonical output-relative path for append-immutable
      trusted-host publication
