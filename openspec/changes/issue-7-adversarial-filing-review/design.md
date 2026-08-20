# Design: Independent Adversarial Filing Review

## Context

The repository supports seven federal filing families and has separate skills
for drafting, authority audit, response requirements, and deterministic Filing
CI. Issue #7 needs a fresh adversarial reviewer whose context is intentionally
narrower than the drafting context and whose output cannot mutate the filing.

## Goals

- Make reviewer independence an explicit, testable input boundary.
- Apply universal and document-family-specific defense and procedural attacks.
- Separate filing-critical, opposition, fact, discovery, and style findings.
- Return exact copy-ready corrections when a correction is supported and does
  not decide plaintiff strategy.
- Fail closed when a fresh context or an approved source is unavailable.

## Non-Goals

- Drafting or editing the canonical filing.
- Certifying authorities, predicting outcomes, or declaring filing readiness.
- Creating an RRD, a deterministic checker, or a replacement for Filing CI.
- Supporting filing families that the repository does not already support.

## Decisions

### Clean-room packet

The orchestrator resolves canonical draft bytes, a version and fingerprint, one
supported document family, and explicit approved sources. Each source entry
contains its stable ID, role, immutable content, and content fingerprint. Paths
and URLs are prohibited packet fields rather than resolvable reviewer inputs.
The `sha256` field is the lowercase hexadecimal SHA-256 digest of the exact
UTF-8 bytes of the corresponding `content` field.

A standard-library launcher validates the exact packet schema and fingerprints,
rejects extra fields, and starts a configured reviewer command in a new process
and empty working directory with conversation, session, thread, and stale
working-directory environment state removed. Its dispatch record exposes the
complete reviewer payload and enabled capabilities. The required capability set
is empty: filesystem, repository, browser, and conversation access are
forbidden. The orchestrator must verify the configured runtime can enforce that
set before dispatch. Otherwise it returns `independent review unavailable` and
does not start or simulate a review.

### Supported document families

The checklist owns complaint or amended complaint, motion-to-dismiss response,
summary-judgment response, leave to amend, extension motion, R&R objection, and
R&R response. An unsupported filing type is reported rather than mapped to the
nearest checklist. Those seven human-readable names are also the canonical
machine values for `document_family`; the launcher does not invent a second slug
vocabulary.

### Findings and corrections

The five required category headings always appear, including `None found` for an
empty category. Each finding contains a stable ID, exact attacked quote,
paragraph/page/heading location, approved source IDs, concrete attack,
consequence, and status.

When complete source-supported non-strategic language is available, a proposed
correction uses `Replace:` with the exact attacked text and `With:` with
complete copy-ready prose. Placeholders, invented facts, invented citations, and
silent edits are prohibited. A change that would retain, narrow, or omit a
claim, theory, fact, defense response, or requested relief becomes a separate
`PLAINTIFF DECISION REQUIRED` item with choices and consequences but no selected
outcome or proposed replacement.

### Composition

The reviewer may flag an apparent authority defect but does not certify the
authority; `audit-authorities` owns that gate. It does not create a response
blueprint owned by RRD skills, does not draft, and does not run or interpret
Filing CI. A later user-approved revision is a separate drafting workflow and
invalidates the prior review until the adversarial and Filing CI gates rerun.

## Risks / Trade-offs

- A prose skill cannot itself prove context isolation. The orchestrator contract
  and spied launcher tests make the dispatched payload and capability boundary
  visible and fail closed. Runtime sandbox enforcement remains a required
  configured precondition rather than an invented local sandbox.
- Exact quotes can be long. They are necessary to make corrections auditable and
  prevent replacement ambiguity.
- Five fixed categories create empty sections. Explicit `None found` prevents a
  missing category from masquerading as reviewed.
- Limiting document families leaves other filings unsupported, but avoids
  inventing checklists beyond the repository's existing drafting scope.

## Migration Plan

This is additive. Publish the new skill and README routing, run structural and
behavioral RED-GREEN tests, validate every skill and the canonical corpus, then
archive the OpenSpec change on the Issue #7 branch.

## Open Questions

None. The user approved the design and test-seam selection and requested
unattended execution.
