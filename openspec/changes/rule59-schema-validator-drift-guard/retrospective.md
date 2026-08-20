# Retrospective

## What worked

- Testing exact schema-to-validator equality exposed the missing comparison
  seams without changing runtime behavior.
- Inventorying schema nodes separately prevents a future required or enum node
  from being silently omitted from the explicit mappings.
- Keeping semantic rules in the existing CLI suite preserved a clear boundary
  between structural drift and behavioral correctness.

## What changed during implementation

The initial test used tuple segments for every schema path. The GREEN refactor
compressed those mappings into readable dotted paths while retaining complete
inventory and one-sided mismatch diagnostics.

## Future rule

When a Rule 59 schema adds or changes a required field or enum, update the
validator constant and the explicit mapping in the same change. When semantic
behavior changes, add or update a real CLI fixture test instead of expanding the
structural guard.
