## Why

The repository's legal judgment and verification boundaries are distributed
across skills and contributor prose, while current-rule freshness and source
provenance have no complete public inventory. A new skill can therefore omit
those safeguards without failing validation. Issue #14 establishes one testable
governance capability so public skills remain human-directed, source-bounded
tools rather than autonomous legal advice.

## What Changes

**Repository governance**

- From: Judgment, source, permission, readiness, and tool-ownership boundaries
  are distributed and only partly reviewable.
- To: One public governance policy and pull-request checklist reserve user
  decisions, define protected gates, and require explicit review of any
  weakening.
- Reason: Contributors need one stable contract and reviewers need an explicit
  prompt.
- Impact: Non-breaking for skill users; new requirements for contributors.

**Rules freshness and provenance**

- From: Rules-dependent skills have no complete machine-checked freshness
  inventory.
- To: A registry classifies every public skill and records authoritative
  provenance and checked dates for bundled rule content or the runtime
  provenance contract.
- Reason: Current procedural propositions must be traceable and visibly dated.
- Impact: Validation fails for an unclassified or incomplete skill entry.

**Jurisdiction content**

- From: A jurisdiction overlay can mix source-gated workflow and current
  jurisdiction-specific propositions in its public SKILL file.
- To: Current jurisdiction-specific propositions live only in verified, sourced
  references; the SKILL surface routes to them without restating them.
- Reason: Local requirements change independently from general skill workflow.
- Impact: The Judge Scholer overlay is normalized without expanding its
  behavior.

## Capabilities

### New Capabilities

- `repository-skill-governance`: Reserve litigation judgment, expose rules
  freshness and provenance, protect legal gates through explicit review, and
  enforce the thin skill-wrapper repository boundary.

### Modified Capabilities

None.

## Impact

The change adds a root governance policy, one registry, one repository-specific
standard-library validator with tests, a pull-request checklist, validation
wiring, and a narrow Judge Scholer reference normalization. It adds no
dependency, rules fetcher, legal-advice engine, filing tool, branch-protection
setting, or mandatory Git Town workflow.
