## Design Summary

Issue #14 is an architectural governance change because it defines
repository-wide contracts for every public skill and for future contributions.
The narrow design is one public governance policy, one machine-readable
rules-provenance registry, one repository-specific validator, focused tests, and
a pull-request review checklist.

The policy reserves litigation judgment to the user, requires supported choices
and consequences without a selected strategy, confines jurisdiction-specific
legal propositions to verified references, protects existing verification,
source, permission, and filing-readiness gates, and routes general-purpose code
to its owning repository behind a thin skill wrapper.

The registry classifies every installed public skill as rules-independent,
runtime-sourced, or bundled-rules-dependent. Every entry has a review date. A
runtime-sourced entry identifies the approved source classes that the skill must
resolve and expose with a checked date when used. A bundled-rules-dependent
entry identifies authoritative source IDs whose URLs and checked dates live in
the same registry. The validator rejects missing skills, stale structural
omissions, unknown source IDs, malformed dates, non-authoritative source
records, and a rules-dependent entry without provenance.

The only current jurisdiction-specific package is the Judge Scholer overlay. Its
specific legal and procedural observations remain in or move to its sourced
reference, whose provenance and checked date are explicit. The public SKILL file
retains only the trigger, source-gated workflow, and non-strategic boundaries.

## Alternatives Considered

### Approach A: Policy prose only

- **Approach**: Add the governance rules to `CONTRIBUTING.md` and stop there.
- **Advantages**: Smallest file change and no validator maintenance.
- **Disadvantages**: Cannot detect an unclassified skill, missing freshness
  date, missing source provenance, or a weakened contribution checklist.
- **Why not chosen**: It does not make the acceptance criteria enforceable in
  the repository validation gate.

### Approach B: Central registry plus repository validator

- **Approach**: Add a public policy, a complete registry, focused validator
  tests, validation wiring, and an explicit pull-request review checklist.
- **Advantages**: One authoritative source of governance metadata, deterministic
  coverage of every public skill, minimal skill-package churn, and no new
  dependency.
- **Disadvantages**: Maintainers must update the registry when adding a skill or
  changing a rules source.
- **Why chosen**: It is the narrowest design that is both public and
  mechanically enforceable without turning governance into a general-purpose
  tool.

### Approach C: Duplicate provenance sections in every SKILL file

- **Approach**: Add a rules-freshness section and source list to all public
  skills.
- **Advantages**: Metadata appears beside each skill's instructions.
- **Disadvantages**: Repeats shared source URLs and dates across many packages,
  creates drift, and forces unrelated edits to rules-independent skills.
- **Why not chosen**: Duplication makes freshness weaker, not stronger. The
  central registry exposes the same information while the validator guarantees
  coverage.

## Agreed Approach

Use Approach B. Keep legal choices in public skill behavior, keep current-rule
metadata in one checked registry, keep jurisdiction-specific propositions in
sourced references, and make repository validation enforce the structure. The
policy and pull-request checklist describe the human explicit-review
requirement; the validator prevents those review prompts and the protected-gate
inventory from disappearing silently.

## Key Decisions

- Git Town remains an optional development convenience and is not part of the
  public governance contract.
- The registry covers every directory containing `skills/*/SKILL.md`; no
  manually maintained skill count is accepted.
- `runtime-sourced` means the skill must use project-approved rules or orders
  and expose their stable source identifiers or URLs and checked date in the
  returned artifact.
- `bundled-rules-dependent` means repository text supplies a procedural rule
  proposition and therefore requires authoritative registry sources with
  concrete checked dates.
- A source is provenance, not proof that every downstream legal proposition is
  correct; skills still apply the existing authority-verification gate.
- Explicit review is a human repository rule surfaced in the pull-request
  checklist; the repository does not invent a GitHub team, approval identity, or
  branch-protection setting.
- The validator is repository-specific standard-library code. General-purpose
  rules retrieval, citation verification, filing checks, and legal evidence
  tools remain in their owning repositories.

## Open Questions

None. The user authorized unattended backlog execution and approved the design
and public test-seam selection for this workstream.
