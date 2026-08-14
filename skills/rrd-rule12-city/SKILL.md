---
name: rrd-rule12-city
description: "Use when creating a response plan, checklist, or Response Requirements Document for a City or municipality's Rule 12(b)(6) motion in a Section 1983 case, especially when Monell theories, pleading-stage record gating, and the movant's heading order control the response."
---

# SKILL.md — ~~rrd-rule12-city~~

Create a detailed **Response Requirements Document (RRD)** for a **City/municipality Rule 12(b)(6) Motion to Dismiss** in a §1983 case (Monell).

An RRD is **not** the brief. It is the blueprint: what must be argued, what must be plausibly alleged, what authority must be cited, and what the Rule 12 **record gate** permits.

## Non‑negotiables

1. **Preserve movant order:** The response’s **ARGUMENT** section MUST track the city’s motion headings **in the same order** (preferably verbatim).
2. **Monell element discipline:** Under each heading, organize substance by the **Monell element(s)** attacked (policy/custom, failure to train/supervise/discipline, deliberate indifference/notice, moving force causation, policymaker, etc.).
3. **Cross‑reference officers response:** Where appropriate, reference the officers response for the underlying constitutional violation; keep the city response focused on Monell.
4. **Rule 12 gate:** No extra-record facts; route gaps to amendment.

---

## The Job

1. Receive the motion headings and the Monell theories attacked
2. Ask **3–5 essential** clarifying questions (lettered options)
3. Generate a structured **RRD** that:
   - mirrors the motion’s heading order
   - breaks work into small Response Units (RUs)
   - maps each heading to Monell elements + required allegations
4. Save to `responses/<response-due-date>/<motion-folder>/rrd.yaml`
5. Be **idempotent** with deterministic IDs

**Important:** Do **NOT** draft the final response brief. Only produce the RRD.

**Required companion skill:** Apply `drafting-section-1983-complaints` whenever the RRD evaluates Monell pleading sufficiency, identifies an amendment, or specifies an amendment proffer. Each municipal theory must follow **Element → Facts → Inference → Result** and must remain separate from other municipal theories.

---

## Rule 12 Guardrails (Do Not Violate)

- Treat well‑pleaded complaint facts as true; draw reasonable inferences for plaintiff.
- Do not resolve factual disputes.
- Record gate: complaint + complaint exhibits; judicial notice (existence/filing); incorporation-by-reference where proper.
- Do not use new facts to “fix” Monell gaps; mark **GAP** and route to amendment.

---

## Step 1 — Clarifying Questions (ask 3–5 only)

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

4. **Do you want to cross-reference the officers response for the underlying violation?**  
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

**RU fingerprint (city):**

```
ru|<motion_folder>|<movant_heading>|<monell_theory_key>|<element_cluster_key>
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

ARGUMENT headings must mirror the motion outline in the same order and map to RU IDs.

### 4) Monell Theory Map (Required)

A compact map of:

- theory (policy/custom/failure-to-train/etc.)
- required elements
- pleaded facts supporting each element (cite placeholders)
- the element-specific inference supported by those facts
- the requested result for that theory
- what will be proven later (discovery)
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
    monell_theory: "policy|custom|failure_to_train|failure_to_supervise|ratification|mixed"
    targeted_elements:
      - "policy_or_custom"
      - "deliberate_indifference"
      - "moving_force"
    record_gate:
      posture: "pleadings_only|judicial_notice|incorporation|conversion_risk"
      materials:
        - cite: "Complaint ¶__"
          source: "complaint|complaint_exhibit|judicial_notice|incorporated_document"
    controlling_standard_required: []
    record_facts_required: []
    claim_pleading_contract:
      standard:
        elements: []
        verified_authority: []
      facts:
        underlying_violation: []
        policy_custom_or_practice: []
        policymaker_attribution: []
        notice_and_deliberate_indifference: []
        moving_force_and_injury: []
        complaint_cites: []
      inference:
        text: ""
        element_supported: ""
        supported_alternative_inferences: []
      result:
        requested_sentence: ""
    movant_framing_to_neutralize: []
    counter_authority_required: []
    rebuttal_logic_required: []
    done_test: []
    exhibits_citations_needed: []
    requested_ruling: "Deny dismissal of Monell claim / theory ..."
    cross_references:
      underlying_violation:
        enabled: true|false
        reference: "" # path or anchor if provided
    status: "draft|ready|stale"
    user_notes: ""
```

### 7) Standards Library

- Monell baseline elements (policy/custom; deliberate indifference; moving force)
- failure-to-train/supervise standards
- pleading standards for Monell

### 8) Evidence & Exhibit Plan

Capture:

- what’s in the complaint
- what will be proven in discovery
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
- **Location:** `responses/<response-due-date>/<motion-folder>/`
- **Filename:** `rrd.yaml`

---

## Checklist (must pass)

- [ ] Motion headings captured in order
- [ ] Response outline mirrors order and maps headings to RU IDs
- [ ] Monell theory map exists and is element-complete
- [ ] Each Monell theory separately maps verified elements, pleaded facts, element-specific inferences, and requested result
- [ ] Each theory addresses the underlying violation, municipal act or omission, policymaker attribution, required notice or deliberate indifference, moving force, and injury
- [ ] Each movant heading has at least one RU
- [ ] Record gate is explicit for each RU
- [ ] Deterministic IDs + idempotent merge behavior
- [ ] Saved to `responses/<due-date>/<motion-folder>/rrd.yaml`
