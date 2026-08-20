## Context

The public JSON schemas document shape and controlled values. The custom
validator adds stable findings and semantic rules that a general schema engine
would not provide. Both are intentional, but their shared structural contract
needs a direct CI seam.

## Goals / Non-Goals

**Goals:**

- Fail CI when a mapped schema required-field set differs from its validator
  constant.
- Fail CI when a mapped schema enum differs from its validator constant.
- Produce mismatch messages that name the contract and values present on only
  one side.
- Preserve the current validator CLI and corpus behavior exactly.

**Non-Goals:**

- Prove semantic validator coverage through static analysis.
- Interpret arbitrary JSON Schema documents.
- Replace behavioral fixture or CLI tests.
- Add new corpus fields, values, findings, or runtime validation behavior.

## Decisions

### Explicit structural mappings

The test imports the validator module and loads both public schemas. Explicit
maps pair schema object paths with required-field tuples and schema enum paths
with allowed-value constants. An explicit map makes a new public contract node
require a conscious test update and avoids unreliable Python source scanning.

### Validator constants are the comparison seam

Required fields already use named tuples. Every schema-controlled enum will use
a named validator set, including values currently written inline at call sites.
Production code continues to pass those sets to the same validation helper.

### Behavioral tests remain authoritative

The guard checks equality of shared structural vocabulary only. Existing CLI
tests continue to prove type checks, authorship rules, references, completeness,
denominator semantics, transfer-card strength, findings, and fixture outcomes.

## Risks / Trade-offs

- **[A schema node is not added to the explicit map]** → The alignment test also
  inventories all schema `required` and enum nodes and fails if the mapped paths
  do not equal that inventory.
- **[The mapping itself becomes hard to diagnose]** → Failure messages identify
  the path and schema-only or validator-only values.
- **[Refactoring inline sets changes behavior]** → Preserve every literal and
  run the full Rule 59 CLI suite plus repository validation.

## Migration Plan

1. Add a RED alignment test that requires named constants for every public
   controlled enum.
2. Extract the missing validator constants and reuse them at existing call
   sites.
3. Run focused and full validation, archive this OpenSpec change, and sync the
   child branch.

## Open Questions

None.
