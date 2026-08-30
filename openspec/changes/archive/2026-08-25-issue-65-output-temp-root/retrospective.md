# Retrospective

## What changed

The first Issue #65 implementation correctly kept staging somewhere beneath the
output root, but combined transient staging with durable run receipts under
`.skill-runs/<run-id>/staging/`. The clarified contract gives temporary work an
explicit, predictable boundary: `<output-folder>/temp/`.

## What worked

- Returning the still-open PR to draft kept its readiness signal honest.
- A small RED pair isolated the visible contract change before the staging move.
- Reusing the existing directory-handle and hard-link publication path preserved
  atomicity and failure semantics.
- The full preexisting writer suite exposed every assertion that still assumed
  staging belonged to the receipt directory.

## Follow-through

Downstream branches must be restacked on this corrected Issue #65 head. Their
guidance must use the same `temp/` namespace, and Issue #68 must treat the
caller-selected output folder itself as the produced profile or artifact folder
rather than adding a registry-like intermediate namespace.
