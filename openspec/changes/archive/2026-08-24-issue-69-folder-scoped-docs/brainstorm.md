# Brainstorm: folder-scoped operations documentation

## Problem

The current first-hour guide organizes useful artifact roles under an example
case-workspace tree, while README still names a particular external checker.
That presentation obscures the actual portable boundary: a trusted host grants
recursive read-only access to fixed logical input roles, one output folder,
optional target selection, and a declared internet policy.

## Approaches considered

### Keep the case-workspace guide and add another folder guide

Rejected. Two first-hour guides would leave competing entry points and retain a
case-directory mental model that the new contract does not require.

### Rewrite the existing file without renaming it

Rejected. The old filename would continue to advertise workspace setup rather
than an invocation that can use already-existing folders anywhere the trusted
host authorizes.

### Replace it with one folder-operations guide

Selected. Rename the guide to `FOLDER_OPERATIONS.md`, link it from README, and
make the ordered synthetic flow exercise the checked-in invocation validator and
output-receipt protocol. Keep source classification, protected decisions,
immutable inputs, gaps, and filing-readiness cautions as role semantics rather
than a prescribed directory tree.

## Boundaries

- Documentation does not create a sandbox, agent runner, workspace template,
  adapter, or case-management integration.
- Issue #71 owns migration of each implemented skill's executable/input-output
  seam; this story must not claim that migration is already complete.
- The examples remain synthetic and use caller-selected folders rather than a
  real case, judge, lawyer, municipality, filing, or machine path.
- Historical archived OpenSpec changes remain untouched.
