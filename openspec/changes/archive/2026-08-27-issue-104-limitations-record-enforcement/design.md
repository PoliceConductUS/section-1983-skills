## Context

Issue #102 added a limitations gate to the canonical complaint guidance. The
installed complaint checker still validates only sections, paragraph links, and
count structure. A handoff can therefore pass without any limitations record.
The checker and Filing CI are independently installable, folder-scoped skills,
so each must ship the same machine-readable contract without importing
repository-local code.

## Goals / Non-Goals

**Goals:**

- Trigger on every unresolved intended individual defendant without treating an
  unidentified non-defendant as affected.
- Preserve distinct identity and diligence events with source references.
- Separate notice, service, Rule 4(m), record control, actor attribution, and
  authority-route application.
- Enforce one structurally complete record per affected defendant at both
  installed checker seams.
- Fail closed on missing, malformed, or unresolved material.
- Pressure-test the skill under realistic filing pressure.

**Non-Goals:**

- No legal conclusion about limitations, relation back, tolling, mistake,
  notice, service, authority fit, or requested relief.
- No fixed definition of “near limitations.”
- No automatic correction or same-stage mutation.
- No change to false-arrest seizure analysis, actor causation, defendant
  ordering, folder boundaries, or persistence.

## Decisions

### One required limitations-gate handoff object

Every complaint JSON mechanical handoff will contain `limitations_gate`, even
when it has no affected defendants. Its `intended_individuals` entries declare a
stable defendant ID, name or role, identity status, amendment action, deadline
status, and whether the record, court, opponent, or caller raised a covered
risk.

The checker derives an affected defendant when the entry is intended as a
defendant and any of these observable predicates is true:

1. identity status is `unnamed`, `role-only`, `misnamed`, or
   `named-not-serviceable`;
2. a covered risk is raised; or
3. the amendment action is `added`, `identified`, or `substituted` and the
   deadline status is `passed` or `unresolved`.

This avoids natural-language inference and a universal day-count threshold.

### One native schema-aligned validator per installed checker

The canonical complaint skill will ship a JSON Schema for `limitations_gate` and
native Python validation in `check_complaint.py`. Filing CI will ship an exact
copy of the schema and aligned native validation because it must run when
installed alone. Repository tests will compare the contracts and exercise both
implementations against the same literal fixtures.

Native validation avoids a new runtime dependency. It checks only types,
required fields, enumerations, ISO dates, source-reference arrays, unique IDs,
per-defendant cardinality, and the rule that unresolved material requires a
declared filing-critical gap and blocked status. A supported record may state
that notice, service, tolling, or concealment was not found; the validator does
not convert that supported fact into a merits conclusion.

### Required defendant-specific sections

Each affected record will contain:

- accrual and limitations deadline facts;
- original Doe or role description and same-transaction analysis;
- separate identity events for first availability, first possession, objective
  ascertainability with basis, and actual identification with source and method;
- separate pre-limitations, post-filing/pre-identification, and
  post-identification/pre-service diligence histories;
- record-control and withholding provenance with separate municipal, custodian,
  and individual attribution;
- Rule 15(c)(1)(C) notice facts;
- service status, attempts, method, date, and proof;
- Rule 4(m) deadline, extension status, good-cause facts, discretionary facts,
  and requested relief;
- authority-route records for limitations, Rule 15(c)(1)(A), Rule 15(c)(1)(C),
  Rule 4(m), tolling, and concealment;
- mistake-versus-lack-of-knowledge classification, defendant-specific
  concealment/tolling facts, fallback claims, and severable relief; and
- explicit filing-critical gaps and overall `clear` or `blocked` status.

Every analytical or factual section carries a structural completion status and
source references. The schema permits a supported “none found” conclusion; only
missing, malformed, or `unresolved` sections are mechanically fatal.

### Behavioral verification

Pressure inputs will withhold the desired answer while combining deadline
pressure, multiple Does, conflicting identity dates, incomplete authority, and
an instruction to file immediately. The baseline uses the Issue #102 skill and
records omissions. The same inputs run against the corrected installed skill and
are scored for the observable gate, separate dates, defendant cardinality, and
refusal to claim filing-ready status with unresolved material. Exact inputs and
scored outputs belong in `verify.md` rather than case files.

## Risks / Trade-offs

- **Aligned installed copies drift** → Compare schema bytes and run identical
  fixtures through both checkers.
- **A structured field appears to decide the merits** → Validate completion and
  sources only; retain legal sufficiency and authority fit in
  `excluded_judgments`.
- **An unidentified witness activates the gate** → Derive affected entries only
  from declared intended individual defendants.
- **A supported adverse fact is mistaken for an unresolved field** → Permit a
  complete sourced “none found” analysis without treating it as malformed.
- **Agent guidance passes text checks but fails under pressure** → Preserve
  fresh-context baseline and corrected pressure runs with scored behavior.

## Migration Plan

1. Add RED public-seam tests and baseline pressure evidence against the Issue
   #102 head.
2. Add the schema and native complaint-checker validation.
3. Align Filing CI's installed copy and validator.
4. Update the canonical guidance and completion audit.
5. Run corrected pressure scenarios, focused tests, mutation checks, strict
   OpenSpec validation, and full repository validation.

Rollback is the reversal of this stacked branch; PR #103 remains unchanged.

## Open Questions

None.
