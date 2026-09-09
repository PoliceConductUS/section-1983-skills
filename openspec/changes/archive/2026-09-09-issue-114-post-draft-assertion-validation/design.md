## Context

The repository separates authorized drafting from independent quality control.
Independent QC already preserves target bytes and produces append-immutable
reports, but no single contract requires full proposition coverage, original-
source substantiation, omission mapping, dependency-aware freshness, correction
handoff, and final rendered review for every generated court-facing document.

The new behavior must work with ordinary declared input folders and one explicit
output folder. It must not depend on CaseGraph, modify a case repository, take a
litigation decision, or make deterministic tooling sound like a legal reviewer.

## Goals / Non-Goals

**Goals:**

- Establish one semantic owner for post-draft assertion validation.
- Review one explicit target read-only and cover inherited and unchanged text.
- Trace atomic propositions to original passages or recording observations.
- Distinguish facts, inferences, authority propositions, and unresolved issues.
- Detect omissions against declared case controls and document-specific
  requirements.
- Invalidate only affected findings and dependencies after changes, then
  reconcile complete final-candidate coverage.
- Coordinate drafting, authority audit, adversarial review, and Filing CI
  without collapsing their authority boundaries.

**Non-Goals:**

- Editing the target during independent review.
- Selecting, weakening, retaining, or dropping a claim or theory.
- Treating pleading support as trial proof.
- Adding a CaseGraph dependency or interpreting a missing CaseGraph route as
  missing substantive support.
- Building a deterministic engine that decides factual support, legal
  sufficiency, or filing readiness.
- Modifying case-specific controls or stable private reports in place.

## Decisions

### Dedicated semantic owner

Add `skills/validating-court-facing-assertions/`. Its `SKILL.md` owns the stage
sequence, role boundaries, and stop conditions. A detailed install-local
reference owns the report schema, status taxonomy, freshness rules, omission
coverage, and Mermaid construction. Other skills name and load this owner; they
do not reproduce the detailed semantic contract.

### Folder and target contract

The validation skill reads declared recursive read-only `filing`, `record`,
`authorities`, `strategy`, and optional `prior-reports` folders. It requires one
ordinary target in `filing`. Internet is denied by the validation skill itself;
authority research or updating occurs only through `audit-authorities` under
that skill's declared policy. All temporary work is confined to
`<output-folder>/temp/`. The validation skill returns report bytes and
structured findings; only the trusted host publishes the immutable receipt.

### Assertion and evidence model

Every sentence is decomposed into independently assessable propositions. Each
assertion record contains identity, exact text and location, classification,
optional supplied documentation route, original source passage or recording
observation, pinpoint, contrary context, inference reasoning, one or more
independently applicable results, and corrective action. Substantive review
separately tests actor, conduct, time, duration, attribution, knowledge,
causation, quotation accuracy, and degree of certainty.

A document drafted by either side may document its own filing text, an
attributed party position, or a procedural act. It is never independent support
for an underlying event or quoted words. Plaintiff memory is an eligible
independent source only when recorded in a separate identified source document;
the validation report attributes it as the Plaintiff's memory claim and does not
upgrade it to adjudicated fact.

The report has distinct sections and counts for supported assertions, supported
inferences, contradictions, overstatements, insufficient sources, missing
documentation links, unchecked assertions, omissions, and unresolved factual
questions. The Mermaid summary is generated from those actual counts and cannot
substitute for the assertion records.

### Authority specialization

`audit-authorities` remains the authority specialist. For each legal
proposition, it supplies actual holding, pinpoint, controlling status, posture,
relevant later treatment, factual fit, and application. The shared validator
keeps pre-event clearly established law, defendant knowledge, municipal notice,
and Rule 15(c) lawsuit notice in separate uses.

### Omission coverage

The validator reads only declared case controls and applicable skill contracts.
It maps approved claims, material source facts, principal corrections, and other
applicable requirements to exact draft locations or records an omission. An
authorized unknown is recorded with its authorized treatment and is not a
drafting defect merely because it remains unknown.

### Freshness and iteration

The report is bound to the reviewed target hash. Each finding is separately
bound to its assertion text, supporting source hashes, controlling authority
identity and state, reasoning premises, and applicable control versions. A
change invalidates each affected finding and every dependent finding; a target
hash change alone does not invalidate an unrelated finding. Unaffected findings
may be carried forward only after verifying their bindings remain applicable.
Final validation reconciles every assertion and applicable requirement in the
complete candidate and includes a rendered-file review.

### Report persistence

Each independent invocation still produces one append-immutable receipt under
the existing trusted-host QC publication contract. A case controller may keep a
stable private current report in Git by consuming a prior report as declared
input and publishing proposed replacement bytes in its own separately authorized
workflow. The public validation skill never overwrites an input or edits case
controls. Independent receipts are preserved.

When an exact prior report is supplied, the next proposed report reuses its
existing issue register and stable issue identities. It explicitly updates or
closes those entries and adds genuinely new findings instead of creating a
parallel register that obscures unresolved history.

### Specialist handoffs

- The umbrella drafting skill orchestrates the loop.
- Complaint drafting supplies the complete complaint and requirements inventory.
- Monell drafting validates only after its deltas are integrated by the
  canonical complaint owner.
- Authority auditing supplies authority findings.
- Adversarial review attacks a validation-complete candidate afterward and may
  send defects back to a separate correction and revalidation loop.
- Filing CI contributes deterministic integrity findings and freshness inputs
  through the optional `deterministic-results` role; it cannot close semantic
  findings.
- Rule 59(e) invokes validation once for each generated court-facing document,
  then reconciles the complete packet without violating the one-target rule.
- Declaration drafting routes each complete generated declaration through the
  same one-target validation loop.

## Risks / Trade-offs

- **Risk: Cross-skill owner unavailable.** → Consumers fail with
  `assertion validation contract unavailable` instead of reconstructing it.
- **Risk: Reports become enormous.** → Require atomic completeness but allow
  stable IDs, tables, and reuse of still-applicable findings.
- **Risk: Stale findings are reused casually.** → Bind each finding to exact
  hashes, control versions, and premises and require final coverage
  reconciliation.
- **Risk: Missing documentation route is confused with no source support.** →
  Keep separate statuses.
- **Risk: Deterministic fixtures overclaim semantic proof.** → Describe tests as
  contract and behavior pressure checks only.

## Migration Plan

Add the new skill and integration references in one release. Existing drafting
outputs remain valid historical artifacts, but they cannot be described as
passing the new workflow without a fresh report. Rollback removes the new skill
and references without changing case files or report receipts.

## Open Questions

None.
