## Why

Court-facing drafts currently lack one reusable lifecycle that validates every
assertion against original sources, detects omitted approved requirements, and
invalidates stale findings after material changes. Existing skills own useful
pieces, but their responsibilities are not joined by one semantic contract. This
change makes validation auditable without confusing citations, hashes, or
deterministic checks with evidentiary support or legal sufficiency.

## What Changes

**Shared post-draft validation**

- From: Drafting and review skills contain partial, sometimes duplicated review
  instructions.
- To: One independently installable skill owns the assertion-validation report,
  correction-loop handoff, freshness model, and stopping criteria.
- Reason: Every final candidate needs complete, source-substantive, reusable
  coverage under one contract.
- Impact: Non-breaking workflow addition for generated court-facing documents.

**Specialist coordination**

- From: Complaint, Monell, authority, adversarial, and Filing CI stages can run
  without a shared assertion ledger.
- To: Each stage contributes its bounded responsibility to the shared workflow
  while preserving read-only review and separate correction authority.
- Reason: Prevent gaps, stale passes, and responsibility collapse.
- Impact: Existing skills gain explicit routing and handoff requirements.

## Capabilities

### New Capabilities

- `post-draft-assertion-validation`: Complete semantic contract for validating
  and iterating generated court-facing documents.

### Modified Capabilities

- `drafting-section-1983-complaints`: Route complete complaint candidates and
  complaint requirements through the shared validation workflow.
- `drafting-section-1983-monell-claims`: Preserve canonical-owner integration
  and validate integrated Monell assertions and omissions.
- `verified-authority-audit`: Supply authority-specific findings to the shared
  report without becoming the whole-document owner.
- `adversarial-filing-review`: Keep defense attack downstream and distinct from
  assertion validation.
- `filing-ci-orchestration`: Contribute deterministic results without deciding
  substantive support or legal sufficiency.
- `repository-skill-governance`: Require one semantic owner and bounded
  references while preserving install-local QC safeguards.

## Impact

Adds one public skill package and behavioral evaluation corpus, updates six
existing skill contracts and routing metadata, and extends repository governance
and OpenSpec capabilities. It does not change any case repository, CaseGraph,
litigation decision, filed document, or general-purpose persistence tooling.
