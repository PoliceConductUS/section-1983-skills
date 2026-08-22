# Design

## Context

Issue 24 established one canonical complaint owner and one false-arrest delta.
This change adds semantic drafting duties without changing that ownership or the
bounded JSON checker handoff.

## Decisions

### Filed-text no-concession boundary

The general complaint package repeats the operative no-concession minimum needed
for standalone use. A filed complaint may qualify what a source proves, state a
fact as disputed or unresolved, plead supported alternatives, and use a
procedurally necessary conditional. It must not describe its own claim, element,
fair-warning path, or immunity position as weak, likely to fail, likely barred,
contested in the adverse sense, or probably subject to qualified immunity.

Risk and strength assessment belongs in versioned strategy or an internal audit.
Moving the assessment does not permit concealment of contrary evidence or
authority; the filed text remains accurate and the authority audit remains
independent.

### Bounded fair-warning unit

The complaint ordinarily uses one verified lead binding pre-event authority for
each distinct fair-warning proposition. Another complaint-level authority is
permitted only when the draft identifies its separate job, such as a distinct
governing proposition or necessary precedential link. The full comparison, later
history, competing cases, and string cite stay in the internal matrix or brief.
The boundary is functional rather than a universal numeric maximum.

### Canonical tuple checklist and authority-audit boundary

One checklist in the complaint contract owns the field names for every
claim–defendant–challenged-act tuple. Its universal layer joins decisive facts,
the defendant's relevant-time knowledge, and the resulting element-specific
application. Its conditional qualified-immunity layer joins event date and
stage, conduct-specific right, verified binding pre-event authority,
authority-audit status, factual similarities and differences, defendant-
specific fair warning, rule-of-orderliness and later-history review status, and
separate prong results.

The complaint package owns only that interface and its fail-closed completion
rule. `audit-authorities` continues to own case identity, publication and
binding-status verification, precedential force, pinpoints, later history,
rule-of-orderliness analysis, and approval procedure. Missing or unverified
qualified-immunity fields create an internal filing-critical GAP and block
filing-ready status; they do not authorize a filed adverse merits assessment.
The existing non-executable JSON handoff mirrors the checklist's tuple
cardinality and machine field names so the human and mechanical interfaces do
not drift; it does not implement the authority audit.

### Purpose-based pruning

The completion audit consumes the filed draft's own uncertainty labels. Each
retained paragraph must name at least one permitted job: required element,
actually raised defense premise, chronology needed to understand a material
event, or preservation/source limitation required for candor. If it serves none,
remove it from filed text or move it to the internal chronology. The audit does
not delete uncertainty merely because it is inconvenient.

### Alternative-offense and record uncertainty

The false-arrest delta operates only for an offense already in the arrest-time
matrix. When an incorporated recording leaves a fact unresolved and that fact is
material to an element, the count must identify the dispute without admitting
the fact, map it to the element, and either state the supported element-level
reason the unresolved fact does not supply probable or arguable probable cause
or log a filing-critical GAP for strategy decision. The skill does not invent
offenses or select a concession.

## Verification

- Deterministic structure and mutation tests inspect the independently installed
  general and false-arrest packages.
- Four generic synthetic fixtures each isolate one prohibited behavior and prove
  unrelated-rule discrimination.
- Fresh-context agents execute the four scenarios against the revised packages;
  accepted output must preserve factual candor, avoid adverse merits
  self-assessment, keep authority bounded, prune nonfunctional uncertainty, and
  fail closed on unresolved offense effects.
- Mutation tests require the canonical tuple fields and prove that incomplete
  authority-audit status fails closed without copying the detailed audit
  procedure into the complaint package.

## Risks

- A no-concession rule could be read as permission to hide adverse material.
  Pair it with express candor and authority-preservation language.
- A citation budget could become an arbitrary hard cap. Require separate jobs,
  not a universal number of citations.
- Pruning could remove necessary context. Preserve chronology and source-limit
  functions expressly.
- Alternative-offense analysis could proliferate defenses. Keep the existing
  actual-offense trigger unchanged.
