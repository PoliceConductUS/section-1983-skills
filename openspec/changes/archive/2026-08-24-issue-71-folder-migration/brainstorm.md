# Brainstorm: migrate implemented skills to exact folder contracts

## Problem

Issues #64 and #65 provide a folder invocation validator and durable output
writer, and Issue #69 documents their product-independent use. Every public
skill now repeats a compact generic boundary, but none identifies its exact
roles, target policy, internet policy, or output mode. Several implemented
helpers still accept project/version paths or arbitrary positional paths, and
Filing CI still delegates to an externally configured command.

## Approaches considered

### Keep the generic prose boundary and infer roles from each request

Rejected. Inference cannot prove that an installed skill used the intended
folders, cannot distinguish a missing role from an undeclared path, and leaves
target and internet authority ambiguous.

### Add a universal runner that loads every skill contract

Rejected. The trusted host already owns enforcement, root validation, logical
input manifests, and output publication. A second runner would duplicate the
persistence boundary and couple skill packages to repository-local machinery.

### Let helpers import root-level validator and writer modules

Rejected. A single skill can be installed without repository-root files. Such an
import would make the package appear self-contained while failing when installed
alone.

### Ship one exact contract per skill and keep helpers pure

Selected. Every skill carries `references/folder-contract.json`. The trusted
host reads that contract, validates roots with the canonical root validator, and
publishes through `OutputRun`. Standalone helpers accept only declared
input-root plus canonical relative targets, or in-memory/standard-input data,
and return deterministic bytes or structured results. Helpers never select
output roots or write receipts.

## Boundaries

- All output modes are `append-immutable`.
- Legal analysis, drafting standards, source gates, human decisions, and
  non-mutation rules do not change.
- Historical archived OpenSpec changes and closed issue history remain intact.
- No CaseGraph bridge, optional graph adapter, universal runner, duplicated
  persistence manager, or general-purpose external checker is added.
- Git remains repository/release infrastructure only and is not a skill runtime
  dependency.
