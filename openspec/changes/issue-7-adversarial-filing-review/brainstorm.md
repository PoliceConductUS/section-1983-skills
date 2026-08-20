# Brainstorm: Independent Adversarial Filing Review

## Problem

The drafting skills own creation and revision, but a drafter should not certify
its own work. Section 1983 filings need a clean-room adversarial pass that sees
only the canonical filing and approved sources, applies document-specific
defense and procedural attacks, and returns findings without changing the filing
or making litigation choices reserved to the plaintiff.

## Constraints

- The reviewer receives no drafting history, redlines, strategy conclusions,
  prior review, checker output, or conversation/session state.
- The canonical draft remains byte-for-byte unchanged.
- Sources come only from an explicit user- or repository-approved allowlist.
- The skill must compose with drafting, authority audit, and Filing CI without
  duplicating or silently invoking their responsibilities.
- No `docs/` or `.superpowers/` directory may be created.
- The public skill contains no machine-specific path, provider dependency, or
  project-private fact.

## Approaches Considered

### 1. Add an adversarial section to each drafting skill

This would place document-specific attacks near their drafting rules, but the
same agent and context would still review its own conclusions. It also repeats
the clean-room and output contract across multiple skills.

### 2. Create one independent reviewer skill with a shared checklist reference

The orchestrator resolves a bounded review packet and starts a fresh reviewer
context that loads one public skill and one document-family checklist. The
reviewer returns a read-only structured report. This is the selected approach
because independence is explicit and the contract has one owner.

### 3. Build a deterministic review application

A program could enforce packet structure and output schema, but it cannot
perform the substantive adversarial analysis requested by this issue. That would
create a new tool rather than the narrow public skill in scope.

## Approved Design

Create `adversarial-filing-review` with:

- `SKILL.md` owning clean-room orchestration, output categories, correction
  rules, plaintiff-reserved decisions, and composition boundaries;
- `references/document-attack-checklists.md` owning universal attacks and the
  seven filing families already supported by this repository; and
- `agents/openai.yaml` for public discovery metadata; and
- a standard-library launcher that validates the exact packet, records the
  dispatched payload and enabled capabilities, and starts only a configured
  no-history reviewer command in an empty working directory.

The clean-room packet contains the immutable canonical draft content, its
version and fingerprint, one supported document family, and approved sources
with stable identifiers, roles, immutable content, and content fingerprints.
Paths and URLs may appear only as provenance metadata. The launcher requires an
empty reviewer capability set; filesystem, repository, browser, and conversation
access are forbidden. If the configured runtime cannot enforce those
restrictions or start a fresh reviewer, the orchestrator reports
`independent review unavailable` rather than simulating independence in the
drafting context.

The report keeps five finding categories separate: Fatal Defects, Credible
Opposition Arguments, Factual Disputes, Discovery Issues, and Style Complaints.
Each finding identifies the exact attacked text, location, source basis, attack,
and consequence. A non-strategic supported correction uses exact `Replace:` and
`With:` fields. A change that would retain, narrow, or omit a claim, theory,
fact, defense response, or requested relief is not a proposed correction; it is
a `PLAINTIFF DECISION REQUIRED` item that preserves the canonical text and
presents the choice without deciding it.

## Test Seams

1. A RED structural contract test requires the public skill, reference,
   discovery metadata, clean-room exclusions, five categories, correction
   fields, reserved-decision gate, and seven checklist families.
2. Launcher tests spy on the complete payload, environment, working directory,
   and declared capabilities and reject extra packet fields or forbidden tools.
3. Synthetic evaluation fixtures permanently reproduce history leakage,
   incomplete correction language, and reviewer-selected narrowing or omission.
4. Fresh reviewer scenarios prove fail-closed independence, all five category
   classifications, copy-ready correction output, and plaintiff-reserved
   choices.
5. The complete repository suite, canonical evaluation corpus, skill discovery,
   runtime validators, and OpenSpec validation remain green.
