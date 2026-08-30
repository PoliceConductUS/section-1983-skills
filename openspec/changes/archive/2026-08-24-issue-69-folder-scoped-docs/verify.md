# Verification

## Branch and scope

- Branch: `codex/issue-69-folder-docs`.
- Stacked base: `codex/issue-65-output-writer` at
  `55cabd3c408f692ace3394bf0f3d602ed70554d1`.
- Pre-archive reviewed HEAD: `08e15a9f5f3d496386b992316709a63cb177d301`.
- Live PR #74 was open and draft at that exact HEAD, with the expected stacked
  base, before archival work began.
- The change is documentation and contract evidence only. It adds no runner,
  adapter, skill implementation, workspace template, or case-management runtime.

## RED and GREEN history

- Planning: `8d8a718` (`docs: plan folder-scoped operations guide`).
- Initial RED: `d8a3906` (`test: define folder operations documentation`) ran 16
  focused tests with 34 expected assertion failures and no errors.
- RED review corrections: `06b63f2`, `8a77f5d`, `af564ed`, and `7517462`
  successively closed real-validator, bounded-section, fenced-decoy,
  affirmative-terminal, safety-negation, and configured-validation false-green
  paths. The final reviewed RED ran 21 tests with 57 expected assertion failures
  and no errors.
- Matcher correction and staged rename: `4bbd5ca` corrected the lowercased
  `immutable QC report` comparison and no-adapter grammar. Because Task 2 had
  already staged `git mv`, that test-only commit also records the
  content-identical `CASE_WORKSPACE.md` to `FOLDER_OPERATIONS.md` rename.
- Initial GREEN: `6f66be1` (`docs: explain folder-scoped skill operations`) ran
  21 focused tests and 447 evaluations successfully.
- Independent review RED: `3942c76` (`test: expose folder guide contract gaps`)
  ran 24 tests with 21 expected assertion failures and no errors. It exposed an
  unmigrated public-skill fixture, an indeterminate host operation, incomplete
  portable role/output semantics, missing shared-owner links, and optional
  shared receipt language.
- Corrected GREEN: `08e15a9` (`docs: complete folder operations contract`) ran
  24 focused tests and 450 evaluations successfully. It uses the determinate
  synthetic conformance operation, exact artifact, fail-closed unavailable
  result, complete portable mappings, canonical owner links, and mandatory
  logical input hashes and run manifests.
- Archive RED exposed unsupported delta operations: the renamed requirement
  headers were marked only as `MODIFIED`, so the repository-local CLI correctly
  aborted without changing files because those headers did not exist in the
  durable specification. Commit `66f57d9` records the correction using three
  supported `RENAMED` operations, full `MODIFIED` content, and one `ADDED`
  product-independent requirement. Strict change validation passed before the
  archive was retried.

## Whole-story review

The current public guide and README were reviewed against the complete change,
the approved test suite, Git history, Task 1 and Task 2 reports, and every
ignored review package. An initial review accepted the documented boundary. A
fresh final review then found three Important documentation-verification gaps:
the fixture hard-coded a target that ordinary selected folders would not
contain, the validator example redirected its logical manifest to an ambient
working-directory file, and the synthetic inventory had no target-derived
semantic content contract. It also found that the archive checklist combined
completed archive work with controller-owned final readiness work.

- README links exactly once to the install-local guide while retaining the thin
  complaint-checker and Filing CI boundaries.
- The six first-hour sections are ordered, locally complete, and reuse stable
  `record` and `authorities` roles plus one explicit output root.
- The corrected canonical fixture passes the real invocation validator after
  caller-root and caller-selected existing-target substitution; the test no
  longer creates the guide's hard-coded target behind the reader's back.
- A direct link check resolved all 11 repository-relative links in README and
  the guide inside the repository.
- The five portable operation units each state their logical input, immutable
  output, and install-local skill owner. The invocation/isolation and
  output/receipt owners are each linked exactly once.

## Synthetic-operation truthfulness

`synthetic-folder-audit` is deliberately a named host-conformance operation, not
an installed public skill or repository runner. Current-code search finds the
identifier only in the guide, its OpenSpec contract, and its documentation test.
The guide requires an input-read-only read of the declared target, no network,
and publication of `reports/example-inventory.json` through the canonical output
protocol. It now defines the inventory's schema version, target role and path,
target byte size and SHA-256, and logical input-manifest SHA-256. Validation
output stays in trusted-host memory until the host publishes the logical input
manifest beneath the explicit output root through the same canonical protocol.
If the trusted host cannot provide that exact operation, the documented result
is `execution unavailable` and execution stops.

## Final review correction RED and GREEN

- `6315892` (`test: expose folder guide verification gaps`) ran 26 focused tests
  with 11 intended assertion failures and no errors.
- `40d807b` (`docs: make folder guide outputs verifiable`) made all 26 focused
  tests and all 452 evaluation tests pass.
- `npx openspec validate case-workspace-start-guide --strict` passed.
- `npx openspec validate --all --strict` passed 22 items and failed 0.
- `git diff --check` passed.

The final independent re-review and controller-owned scratch removal, fresh
repository-wide validation, and PR readiness remain pending at this evidence
checkpoint.

The re-review at `49ec3d7` found one further Important interoperability gap:
validator stdout bytes and the writer's canonical input-manifest fingerprint
used different JSON serializations. The guide could therefore instruct a host to
persist bytes whose SHA-256 did not match the receipt.

- `89bce81` (`test: bind guide manifest bytes to receipt`) added an executable
  writer integration test and failed on the missing canonical-byte instruction.
- `79e9b02` (`docs: bind persisted manifests to writer receipts`) requires the
  host to parse validator stdout into an object, serialize the same object with
  the writer's canonical compact UTF-8 sorted-key JSON encoding, and publish
  those exact bytes.
- The integration test now publishes the manifest and inventory through a real
  `OutputRun`, completes the run, and proves equality among the manifest
  artifact SHA-256, inventory `input_manifest_sha256`, and terminal receipt
  `input_manifest_sha256`.
- Focused documentation and writer integration tests passed 27 tests; full
  evaluation discovery passed 453 tests; strict OpenSpec passed 22 items and
  failed 0; tracked formatting and `git diff --check` passed.

Final independent approval and controller-owned cleanup, repository-wide
validation, and PR readiness remain pending at this evidence checkpoint.

## Final approval and controller verification

The independent reviewer approved exact head `710a197` with no Critical,
Important, or Minor finding. Independent execution confirmed equality among the
persisted logical-manifest file SHA-256, its terminal artifact-record SHA-256,
the inventory `input_manifest_sha256`, and the terminal receipt
`input_manifest_sha256`. The live draft PR was open and green at that exact
head, and Issue #69 remained open.

The controller then consumed and removed only the retained ignored
`.superpowers/sdd/plan/` review scratch. With no ignored review files remaining,
a fresh `npm run validate` passed formatting, 26 drafting tests, 453 evaluation
tests, 22 discovered skills, 22 OpenSpec items, corpus evaluation, and
governance validation. The tracked tree remained clean before this final
evidence update.

PR readiness follows only after this evidence commit is pushed and its exact
head is freshly verified. The PR and Issue #69 remain open under the requested
close-on-merge policy.

## Issue #71 boundary

Live Issue #71 remained open during verification and continues to own migration
of implemented public skills, durable specifications, governance, fixtures, and
executable seams to fixed recursive read-only roles and one output folder. This
guide says that not every installed skill is already folder-native and does not
claim that migration. No Issue #71 implementation is included here.

## Public terminology and privacy

- The current-public search across `README.md` and `FOLDER_OPERATIONS.md` for
  CaseGraph, CaseHome, ResourceHandle, resource UID, graph traversal, JSONL,
  Git-backed history, and Git history commands returned no matches.
- The private-marker search across the guide and active change for user home
  paths, the private docket fragment, party and municipality names, username,
  and ECF-number markers returned no matches.
- Examples use only generic synthetic roots, roles, target material, and output.

## Pre-archive commands

- `python3 -m unittest evaluations.tests.test_folder_operations_guide -v` — 24
  tests passed.
- `python3 -m unittest discover -s evaluations/tests -p 'test_*.py'` — 450 tests
  passed.
- Repository-relative Markdown link check — 11 links checked, all resolved.
- `git diff --check 55cabd3..08e15a9` — passed.

## Archive verification

The repository-local OpenSpec CLI archived this change into
`openspec/changes/archive/2026-08-24-issue-69-folder-scoped-docs/` and merged
the approved delta into the durable `case-workspace-start-guide` specification.
The stale placeholder Purpose was replaced with a concrete folder-operations
purpose.

- `npx openspec validate case-workspace-start-guide --strict` — valid.
- `npx openspec validate --all --strict` — 22 passed and 0 failed.
- Focused documentation tests — 24 passed.
- Full evaluation discovery — 450 passed.
- Repository-relative Markdown link check — 11 links checked, all resolved.
- `npm run governance:validate` — passed.
- Tracked formatting and `git diff --check` — passed.
- `npm run validate` — passed formatting, 26 drafting tests, 450 evaluations, 22
  discovered skills, 22 OpenSpec items, corpus evaluation, and governance.

The ignored SDD scratch was temporarily isolated for repository-wide formatting
and restored with an identical SHA-256 inventory. The controller retains it for
final independent review and owns PR readiness; Issue #69 and PR #74 remain
open.
