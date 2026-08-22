# Brainstorm: Judge-overlay execution receipts

## Classification

This is an architectural addition to the existing judge-overlay interface. It
does not create a new research method, but it adds a durable machine packet,
public receipt writer, and composition obligation shared by every assigned-
judge overlay.

## Approved direction

Add one generic standard-library receipt writer to the always-loaded
`section-1983-drafting` package. Assigned-judge skills provide a complete
execution packet after drafting. The writer verifies artifact fingerprints,
normalizes validation and anti-gaming failures to fail-closed outcomes, and
creates one immutable Markdown receipt under the audited version's `audits/`
directory. A completed receipt with an explicit no-change reason proves that the
overlay ran and degraded; absence of judge-specific prose does not.

## Rejected alternatives

- Filed judge-specific prose cannot prove execution because correct degradation
  may add none.
- A prose-only checklist cannot preserve hashes, versions, or immutable run
  identity.
- Storing the receipt in the filing or a shared project folder would violate the
  version-local quality-control contract.
- Revalidating or creating judge tendencies here would duplicate the canonical
  corpus and transfer-card owners.
