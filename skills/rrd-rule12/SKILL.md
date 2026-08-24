---
name: rrd-rule12
description:
  "Use when creating a response plan, checklist, or Response Requirements
  Document for a Rule 12 motion to dismiss in a Section 1983 case, including
  qualified immunity, Nieves retaliatory-arrest issues, record gating,
  incorporation by reference, or motion-attached BWC/video."
---

# SKILL.md — rrd-rule12

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `motion` contains the Rule 12 motion and its ordered arguments.
- `record` contains the operative pleading and approved pleading-stage record.
- `authorities` contains approved Rule 12 and claim-specific law.

Target is required in `motion`. Internet is `disabled`. Return the Rule 12 RRD
as a canonical output-relative path and deterministic bytes; only the trusted
host may publish it append-immutable. Report missing headings, pleading
material, record-gate facts, authority, or amendment information as a gap
without drafting the response brief.

Generate a **Response Requirements Document (RRD)** that functions as the
drafting blueprint for an opposition/response to a **Rule 12 motion to dismiss**
(especially **Rule 12(b)(6)**) in §1983 cases.

An RRD is **not** the brief. It is a checkable plan: what must be argued, what
facts must be treated as **plausible**, what authority must be cited, what the
**record gate** allows, and what materials (if any) can be referenced at this
stage.

This skill is designed to be run **once per motion**. If there are two motions
(e.g., **officers MTD** and **city MTD**), invoke it **twice** with each motion
declared separately and publish each returned artifact through its own output
run.

---

## The Job

1. Receive the motion arguments the user must respond to (or a summary)
2. Ask **3–5 essential** clarifying questions (lettered options)
3. Generate a structured **RRD** (Rule 12 optimized)
4. Return `rrd.yaml` bytes with a canonical output-relative path for trusted-
   host publication.
5. Be **idempotent**: when a prior RRD is expressly supplied in `record`, merge
   it without duplicating Response Units and return a new append-immutable
   artifact.

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

## Step 2 — Idempotence and deterministic identity

Before generating or updating an RRD, read
[references/deterministic-identifiers-and-merging.md](references/deterministic-identifiers-and-merging.md)
completely. Every repeatable object uses its prescribed SHA-256 fingerprint ID.
Merge by ID, preserve manual fields, and mark missing regenerated objects stale;
never duplicate or silently delete them.

## Output and YAML contract

Before producing `rrd.yaml`, read
[references/rrd-yaml-contract.md](references/rrd-yaml-contract.md) completely.
It owns the file layout, top-level and Response Unit schemas, amendment handoff,
false-arrest fields, conditional video map, and declared-role source metadata.
Do not substitute an incompatible schema.

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
- [ ] Returned with a canonical output-relative path for append-immutable
      trusted-host publication
- [ ] No internal tool artifacts in output
