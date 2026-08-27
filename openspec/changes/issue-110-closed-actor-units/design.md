## Context

The canonical complaint contract already owns tuple cardinality and requires
decisive facts, incorporated paragraphs, relevant-time knowledge, application,
injury, and qualified-immunity fields. The false-arrest delta already separates
seizure stages, officers, material offenses, and later facts. The observed gap
is that an agent can point to a factual range and state a conclusion without
placing the decisive factual bridge inside the actor unit.

## Goals / Non-Goals

**Goals:**

- Make each claim–Defendant–challenged-act unit functionally complete in filed
  complaint prose.
- Require actor-specific incorporation when acts, stages, or knowledge differ.
- Keep later facts out of an earlier knowledge set while permitting an expressly
  stated later function.
- State the false-arrest actor recipe in one place without duplicating the
  general complaint skeleton.
- Preserve a paired synthetic behavior fixture and independent rubric.

**Non-Goals:**

- No new QI skill or doctrine owner.
- No fixed paragraph count or mandatory repetition.
- No case-specific names, paragraph numbers, or packet-control changes.
- No deterministic judgment about fact truth, legal sufficiency, authority fit,
  causation sufficiency, probable cause, QI, strategy, or filing readiness.
- No change to the rule that only actually raised alternative offenses require
  treatment.

## Decisions

### A positive closed-unit recipe

Each actor unit will directly contain its incorporated factual paragraphs,
challenged act and time, then-known decisive facts, disputed element,
fact-to-element application, later-only fact boundary, personal causal role,
injury, and both QI-prong applications when QI applies. This is a functional
shape, not a demand for one paragraph per field.

### Complaint and brief have different jobs

The complaint owns the concise decisive bridge. A supporting brief may expand
authority comparisons and competing record interpretations. It cannot be the
only place where the facts are applied to the actor, element, causation, or QI
prongs.

### False-arrest closure is officer and seizure-stage specific

Every challenged officer's unit will identify the seizure or continued-seizure
point, suspected and actually raised alternative offenses, facts known at that
point, missing or disputed elements, probable and arguable probable cause,
later-fact exclusions, causal stage, injury, and conduct-specific fair warning
and QI results.

### Semantic fixture with a narrow deterministic tripwire

The failing candidate will reproduce multiple actor headings, omnibus
incorporation, the sentence “the relevant facts are pleaded in paragraphs X–Y,”
and bare QI conclusions. The passing candidate will directly close each actor
unit. A narrow banned-pattern finding preserves the demonstrated shortcut.
Rubric criteria own the semantic questions; deterministic success is never
described as proof of legal sufficiency or actor-unit closure.

## Risks / Trade-offs

- **Guidance causes needless repetition** → Define functional closure and allow
  compact prose rather than fixed paragraph cardinality.
- **Later facts disappear entirely** → Permit them when their later function is
  stated and they are excluded from the earlier knowledge set.
- **Fixture appears to prove semantics mechanically** → Limit the deterministic
  rule to the explicit shortcut and state rubric ownership in the fixture and
  durable specification.
- **False-arrest delta duplicates the general owner** → State only the offense-,
  seizure-, and officer-specific additions.

## Migration Plan

1. Add RED contract and fixture tests against the current installed references.
2. Preserve a fresh-context baseline showing the shortcut before guidance
   changes.
3. Add the minimal closed-unit language to the three approved references.
4. Add the paired fixture and independent semantic rubric.
5. Run the same pressure task with the corrected references, focused tests,
   strict OpenSpec validation, and full repository validation.

Rollback is the reversal of this stacked branch; PR #109 remains unchanged.

## Open Questions

None.
