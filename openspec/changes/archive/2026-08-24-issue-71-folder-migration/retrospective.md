# Retrospective

## Outcome

Issue #71 migrates the already implemented public skill surface from implicit
project, repository, version-folder, configured-checker, and CaseGraph-shaped
runtime assumptions to exact install-local folder contracts. Each of the 22
skills now declares fixed ordered read-only roles, target policy, internet
policy, and append-immutable output semantics. Packaged helpers consume only
declared roots and canonical targets or bounded in-memory data, while the
trusted host alone owns output publication.

## What worked

- One checked-in contract per independently installable skill made filesystem
  and network authority reviewable without a case-management product.
- Isolated-package tests prevented accidental reliance on repository-root
  scripts and proved the packaged helpers remained distributable.
- Host test doubles proved deterministic helper bytes can be published through
  the shared append-immutable output protocol without giving helpers an output
  root.
- Preserving the existing legal fixtures throughout the migration separated
  runtime-boundary corrections from litigation judgment and legal semantics.
- Focused independent review caught both residual direct-persistence prose and
  the difference between publishing a contract and enforcing it.

## Misses and corrections

- The first current-guidance test checked role and policy phrases but did not
  execute contract-to-envelope conformance. An installed contract is not an
  authority boundary until the host validates the selected envelope against it.
  The final matrix copies and exercises every skill package.
- The generic RRD, Rule 12 RRD, and Rule 59 study retained old write/save verbs
  after their new folder sections were added. Regression patterns now reject
  those active direct-write instructions.
- The quality-control boilerplate said a stage could “write” its report even
  though the explicit-output contract assigned publication to the host. The
  canonical governance sentence, validator fixtures, and all affected skills now
  say the stage returns a result for trusted-host publication.
- GitHub Actions exposed an import ambiguity that macOS did not: the root
  `scripts` directory was a namespace package and could lose to an installed
  package with the same name. A minimal `scripts/__init__.py` makes ownership
  deterministic without changing helper behavior.
- One full validation attempt classified a 50-millisecond synthetic malformed
  response as a timeout under load. The exact test passed immediately in
  isolation and the fresh complete validation passed without a code change.

## Reusable lessons

Contract documents, prose, and schema validation are complementary but not
substitutes for runtime enforcement. A folder-scoped host must load the selected
installed package's contract and reject authority drift before touching case
material. Migration searches should also test positive write verbs, not only
product names and obsolete path fragments. Finally, direct-write ownership must
use one canonical sentence across governance, generated skill boilerplate, and
mutation tests so a future wording change cannot reopen the persistence seam.

## Boundaries retained

This change does not add a universal runner, CaseGraph adapter, bridge, graph
resource model, external general-purpose checker, or case-directory convention.
It does not rewrite archived OpenSpec history or closed issue history. It does
not change approved legal analysis, source gates, non-mutation requirements, or
plaintiff-reserved decisions.
