# Proposal: Make authority retrieval premise-aware

## Why

A retrieval system can return authentic but inapplicable authority when a query
contains a false premise, the wrong jurisdiction or rule version, or an
overbroad semantic match. Issue #79 requires collection to preserve a bounded
research frame, premise results, rejected candidates, and complete query
provenance without representing retrieval output as verified law.

## What changes

- Require one explicit retrieval frame per legal question.
- Record material query premises as verified, false, or unresolved, including
  corrections and gaps.
- Preserve source-system identity, provider or product identity when available,
  exact query, filters, execution metadata, result identity, and retrieval
  order.
- Preserve considered and rejected candidate sources with stable rejection
  reasons.
- Expand empty and incomplete result records with searched scope, known
  missingness, and coverage limits.
- Add synthetic passing/regression coverage for the Issue #79 failure taxonomy.

## Capability

- `collecting-legal-authority-sources`

## Non-goals

- No substantive authority verification, proposition audit, filing approval,
  provider mandate, litigation-strategy choice, or historical vendor benchmark.
