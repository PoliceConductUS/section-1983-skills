# Retrospective

## Outcome

Issue #69 replaced a prescribed case-workspace onboarding path with one
product-independent folder-operations guide. The public entry point now begins
with fixed logical read-only roles, one explicit output folder, a declared
target and internet policy, trusted-host enforcement, and reproducible terminal
receipts without claiming that public-skill migration is complete.

## What worked

- A documentation RED that parsed the real JSON fixture and invoked the real
  validator prevented prose-only conformance claims.
- Bounded Markdown-section checks kept each of the six first-hour actions in its
  owning section instead of allowing distant prose to satisfy the flow.
- Fenced-decoy guards, repository-confined link resolution, and operation-unit
  checks made the public contract testable without prescribing caller folder
  names or a case-directory tree.
- Keeping `FOLDER_SCOPED_EXECUTION.md` and `SKILL_OUTPUT_PERSISTENCE.md` as
  canonical owners let the guide stay narrow while still making isolation and
  receipt requirements discoverable.
- The independent Task 2 review challenged semantic truthfulness, not merely
  word presence, and drove a determinate synthetic conformance operation.

## False-green test corrections

The initial RED could pass from unrelated sections, fenced decoys, and negated
or reversed safety language. Five review rounds corrected those weaknesses:

- validate the substituted fixture at the production boundary;
- bound each step at the next level-two heading;
- remove fenced blocks before prose assertions;
- require affirmative valid-manifest and absent-incomplete semantics;
- distinguish safe prohibitions from affirmative source, approval, mutation,
  validation, and filing-ready reversals; and
- catch bare affirmative instructions to run guessed, unconfigured, arbitrary,
  or any validation commands.

Two final matcher defects were corrected before GREEN: the operation-unit text
was lowercased while the expected `immutable QC report` phrase was not, and the
no-adapter pattern omitted the grammatical space after optional `is`.

## Staged rename history

Task 2 used `git mv CASE_WORKSPACE.md FOLDER_OPERATIONS.md` while the controller
was correcting the two defective RED matchers. The staged content-identical
rename was therefore recorded in `4bbd5ca`, the matcher-correction commit,
rather than the later documentation GREEN. The rewritten guide and README
remained unstaged until `6f66be1`. This history is unusual but preserves the
actual test-first boundary: the old content still failed the corrected RED, and
the public rewrite arrived only in GREEN.

## Original Task 2 review findings

The first GREEN incorrectly named an implemented public skill even though the
migration story had not run, described no determinate host behavior or exact
artifact, omitted complete logical input-to-immutable-output mappings from the
portable patterns, omitted discoverable shared-contract owner links, and made
shared hashes and manifests sound optional in README.

The correction added a new RED before public documentation changed. The final
guide names `synthetic-folder-audit`, defines its input-read-only target read,
no-network rule, exact `reports/example-inventory.json` output, canonical
publication, and `execution unavailable` result. It also completes every
portable mapping and makes logical input hashes and terminal run manifests
mandatory for folder-scoped operations while leaving extra packet controls
optional and separate.

## Misses and boundaries

- The first RED overfit phrasing in two places and required repeated review to
  distinguish prohibitions from contradictions. Mutation examples should have
  been designed with the original matcher.
- The first GREEN treated a plausible example as truthful without checking
  whether its named skill had actually migrated. A documentation fixture must
  not imply an executable seam that the repository does not yet provide.
- The first archive attempt exposed a delta-model error: a renamed requirement
  cannot be expressed only as `MODIFIED` under the new header. The CLI aborted
  without mutation; a failing archive probe then drove explicit `RENAMED`
  operations plus the full modifications before archival work resumed.
- The first archived guide still hard-coded a target path, redirected the
  logical input manifest to an ambient file, and named an inventory artifact
  without defining values that could be checked against the selected target.
  Final-review regression tests now substitute a caller-selected existing
  target, prohibit ambient manifest redirection, and require target-derived
  inventory fields plus terminal-receipt comparison.
- The first correction still treated validator stdout bytes as if they were the
  writer's canonical manifest bytes. A fresh re-review proved the two hashes
  differed. The final executable regression now publishes through a real
  `OutputRun` and binds the persisted artifact, inventory fingerprint, and
  terminal receipt fingerprint to one canonical serialization.
- This change does not implement a trusted host, universal runner, adapter,
  sandbox, synthetic operation executable, or migration of any installed skill.
  Live Issue #71 owns the implemented-skill migration.
- The ignored SDD evidence remains present for the controller and final
  independent reviewer. PR readiness is deliberately outside this archive-only
  task.

## Reusable lessons

Documentation conformance needs executable truth conditions. Parse examples,
call the real validator, resolve links inside the installation, isolate prose
from code fences, and mutation-test negations. When a guide demonstrates an
operation before the public skills migrate, use an explicitly synthetic,
determinate, fail-closed conformance operation rather than borrowing the name of
an implementation that does not yet honor the contract.
