## Why

The Rule 59(e) study skill already describes an evidence ledger and denominator
gates, but its format-neutral prose cannot deterministically detect missing
fields, authorship conflation, or unsupported tendency and success-rate claims.
Issue #15 publishes a canonical public schema and validator so corpora and
neutral transfer cards are reproducible without exposing private case materials.

## What Changes

**Canonical publication contract**

- From: CSV, YAML, or database rows follow a prose field table.
- To: Published or transferred corpora export one versioned canonical JSON
  object under a public schema.
- Reason: One portable seam permits deterministic validation.
- Impact: Existing working formats need a canonical JSON export before
  validation.

**Authorship and reasoning stages**

- From: Controlled values exist, but stage combinations are not mechanically
  checked.
- To: Recommendations, adoption-only orders, independently reasoned final
  decisions, consent decisions, and outcome-only orders have consistent required
  authorship fields.
- Reason: Adoption must not be misreported as independent judicial reasoning.
- Impact: Invalid stage/author combinations fail validation.

**Denominator and transfer limits**

- From: Finding cards warn against unsupported claims in prose.
- To: Neutral transfer cards and corpus denominators are separately schematized,
  and incomplete corpora cannot validate a tendency or success-rate card.
- Reason: Missing documents and convenience samples must remain visible
  downstream.
- Impact: Stronger claims require a complete declared universe and zero
  unresolved relevant missingness.

## Capabilities

### New Capabilities

- `studying-rule-59e-decisions`: Publish and validate a source-bounded Rule 59
  decision corpus, authorship coding, denominator limits, gap log, and neutral
  transfer cards.

### Modified Capabilities

None.

## Impact

The change updates one existing public skill and reference, adds two JSON
schemas, one skill-specific standard-library validator, generic synthetic
validation fixtures, and focused tests. It adds no dependency, docket retriever,
database, private corpus, legal truth certification, filing action, prediction,
or general-purpose schema framework.
