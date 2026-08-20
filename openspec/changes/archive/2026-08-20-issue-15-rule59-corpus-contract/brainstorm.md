## Design Summary

Issue #15 extends the existing `studying-rule-59e-decisions` reference with a
canonical, public, machine-checkable transfer format. The skill keeps its
evidence-led research workflow, but a corpus that will be published or
transferred must export one JSON object validated by a skill-specific
standard-library command.

The canonical corpus contains a versioned study manifest, a declared denominator
and its limits, decision records, a retrieval-gap log, and neutral transfer
cards. Each decision record separately encodes court and case identity, assigned
judge, authorship roles, procedural posture, asserted grounds, requested relief,
proposed material, reasoning independence, disposition, sources, missing
documents, and appellate history.

Decision type is explicit and validated against reasoning independence. A
recommendation cannot masquerade as a final decision; an adoption-only order
cannot be credited with the recommendation's reasoning; and an independently
reasoned final decision must identify its reasoning author. Missing records
remain visible in both the record and study-level gap log.

Transfer cards are neutral evidence transfers, not drafting instructions or
predictions. They carry the proposition, defined universe, numerator,
denominator, date range, supporting and disconfirming row IDs, evidence level,
missingness, permitted use, prohibited inference, and checked-through date. The
validator rejects a tendency or success-rate card unless the declared universe
is complete and the relevant unresolved missingness count is zero.

## Alternatives Considered

### Approach A: Expand only the Markdown field table

- **Approach**: Add the missing fields and warnings to the current corpus
  contract.
- **Advantages**: Smallest change and remains format-neutral.
- **Disadvantages**: Cannot deterministically detect missing fields, authorship
  conflation, invalid controlled values, or an unsupported rate/tendency claim.
- **Why not chosen**: Acceptance requires validation fixtures and a published
  schema, not only prose guidance.

### Approach B: Canonical JSON schemas plus a skill-specific validator

- **Approach**: Publish a corpus schema and transfer-card schema, validate
  canonical JSON with standard-library code, and check in synthetic pass/fail
  fixtures.
- **Advantages**: Portable, install-local, testable, and narrow enough to remain
  part of the public skill package.
- **Disadvantages**: Researchers using CSV, YAML, or a database must export
  canonical JSON before validation.
- **Why chosen**: It is the smallest machine-checkable public contract that
  covers the complete Issue #15 acceptance criteria without a dependency.

### Approach C: General multi-format corpus framework

- **Approach**: Build a reusable schema engine for JSON, CSV, YAML, and
  databases.
- **Advantages**: Broad reuse across future legal research corpora.
- **Disadvantages**: General-purpose parsing, migration, and schema tooling
  exceeds this skill repository's ownership boundary.
- **Why not chosen**: That tool belongs in a legal-evidence tooling repository
  behind a thin skill wrapper, not in this issue.

## Agreed Approach

Use Approach B. Keep research judgment and legal verification in the existing
skill; add only the canonical publication contract and deterministic validation
needed to make the evidence transfer reproducible. Preserve the existing
Markdown contract as the human-readable field and coding guide, with direct
links to both machine schemas and the validator command.

## Key Decisions

- Canonical publication format is JSON; other working formats may be used only
  if they can export an equivalent validated JSON artifact.
- One parent record represents one motion-disposition pair. Recommendations,
  adoption orders, amended orders, and appellate events remain linked stages,
  not extra motions.
- `decision_type` distinguishes `recommendation`, `adoption-only-order`,
  `independently-reasoned-final-decision`, `consent-final-decision`, and
  `outcome-only-order`.
- Authorship consistency is a semantic validator rule rather than a prose
  convention.
- A denominator has a defined universe, candidate count, coded-pair count,
  research-question-complete count, status, and explicit limits.
- Incomplete or convenience samples may support examples or a documented
  cluster, but never a tendency or success-rate claim.
- Fixtures use fictional courts, judges, cases, and documents and contain no
  private case material.
- The validator implements only this public contract; it is not a general JSON
  Schema engine or legal authority checker.

## Open Questions

None. The user authorized unattended backlog execution and approved the design
and public test-seam selection for this workstream.
