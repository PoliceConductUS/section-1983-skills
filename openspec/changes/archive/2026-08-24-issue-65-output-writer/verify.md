# Verification

## Branch and scope

- Branch: `codex/issue-65-output-writer`
- Parent: `codex/issue-64-folder-boundary` at `28d0754`
- Pre-archive reviewed HEAD: `7b19d80`
- Commit range: `28d0754..7b19d80` (16 commits; 14 files; +3,364 / -0)
- Issue #65 and draft PR #73 remain open. The controller owns the final
  ignored-workspace cleanup, independent whole-branch review, and draft-to-ready
  transition.
- No CaseGraph, CaseHome, Git, MCP, graph, resource-URI, persistence-manager, or
  external runtime dependency was added.

## Whole-story review

The review checked stable output-root and run-directory authority, post-start
path replacement, descendant symlink swaps, canonical relative paths, hard-link
alias classification, create-exclusive publication, durable staging cleanup,
partial artifact and receipt failures, terminal sealing, descriptor closure,
retry honesty, canonical manifests, internet provenance, schema/runtime
agreement, and bounded diagnostics.

Three independent Task 4 correction rounds identified ten Important findings and
one Minor documentation defect. New failing tests first proved every accepted
behavior gap. The narrow GREEN corrections now seal every possibly visible
terminal receipt, preserve authoritative incomplete state, close stable
directory handles, derive internet use from durable and incomplete artifacts,
validate skill versions and source URLs before mutation, sync every staging
unlink, preserve primary bounded failures, and seal successfully linked receipt
names even when another actor removes them before a later sync failure. Scoped
re-review accepted each correction round with no remaining Critical or Important
finding.

The writer remains a standard-library repository helper bound to Issue #64's
validated invocation. It does not grant ambient path authority or claim to
provide the trusted host's filesystem or network sandbox.

## Fresh pre-archive verification evidence

- `python3 -m py_compile scripts/skill_output_writer.py scripts/validate_folder_invocation.py evaluations/tests/test_skill_output_writer.py evaluations/tests/test_folder_scoped_execution.py`
  — passed.
- `python3 -m unittest evaluations.tests.test_skill_output_writer evaluations.tests.test_folder_scoped_execution -v`
  — 74 tests passed.
- `python3 -m unittest discover -s evaluations/tests -p 'test_*.py'` — 433 tests
  passed.
- `npx openspec validate issue-65-output-writer --strict` — passed.
- `npm run openspec:validate` — 22 of 22 items passed before archive.
- `npm run governance:validate` — passed.
- `git ls-files '*.json' '*.md' '*.yml' '*.yaml' | xargs npx prettier --check` —
  every tracked JSON, Markdown, and YAML file passed formatting.
- `git diff --check 28d0754..HEAD` — passed.
- Forbidden dependency search found only the proposal and brainstorm's explicit
  CaseGraph non-dependency statements; production, schema, protocol, and tests
  contain no forbidden runtime import or dependency.
- Origin parity before archive — local and origin both resolved to `7b19d80`.

The ignored `.superpowers/sdd/plan/` coordination workspace is intentionally
retained for the controller and final independent reviewer. Repository-wide
Prettier includes ignored files, so the aggregate gate is run with that exact
workspace temporarily isolated and restored unchanged. The controller will
remove it only after consuming the reports.

## TDD and review trace

- Task 1 recorded the expected missing-writer RED and then strengthened stable
  root, run-ID, path, input-preservation, and failure-confinement coverage.
- Task 2 supplied the atomic writer GREEN. Review-driven RED tests added
  case-folded namespace protection, honest post-link failure state, bounded
  recursive input indexing, bounded modes, and input-symlink alias
  classification.
- Task 3 recorded receipt RED for incomplete, terminal, retry, canonical,
  internet, and bounded-failure behavior. Three review refinements closed
  false-success windows and required durable incomplete-state recovery.
- Task 4 supplied receipt, schema, and protocol GREEN. Three additional
  test-first review rounds closed terminal visibility, cleanup durability,
  validation, descriptor, and linked-receipt race defects.

## Archive verification

The repository-local OpenSpec CLI archived this change as
`2026-08-24-issue-65-output-writer`, created the durable
`explicit-skill-output-persistence` specification, and updated the durable
`folder-scoped-skill-execution` specification. The generated placeholder Purpose
was replaced with the concrete capability statement above.

Post-archive evidence:

- `npx openspec validate explicit-skill-output-persistence --strict` — passed.
- `npx openspec validate folder-scoped-skill-execution --strict` — passed.
- `npx openspec validate --all --strict` — all 22 durable specifications passed.
- `npm run validate` — formatting passed; 26 drafting tests and 433 evaluation
  tests passed; 22 skills were discovered; all 22 OpenSpec items, the evaluation
  corpus, and governance validation passed.
- `git diff --check` — passed after archive.

For the aggregate command, the ignored SDD coordination directory was moved to
one fixed temporary path and restored immediately after the command completed.
It remains byte-for-byte available for the controller's report consumption and
independent review.

## Decision

PASS for OpenSpec archive. PR #73 remains draft until the controller completes
its independent whole-branch review and final state checks.

## Post-archive independent-review correction

The controller's later independent whole-branch review found four Important
defects not covered by the pre-archive scoped reviews:

1. a caught prepublication write failure did not prevent a later success
   receipt;
2. an unlink operation that removed `incomplete.json` and then reported failure
   could leave a visible manifest without the authoritative incomplete marker;
3. the value returned by `write()` shared nested provenance state with the
   eventual receipt; and
4. runtime retrieval-time parsing accepted alternate ISO 8601 forms outside the
   receipt schema's RFC 3339 contract.

The correction was performed without unarchiving the change. RED commit
`06c2292` proved all four defects while the prior 74-test focused baseline
remained green. The narrow correction adds sticky completion-ineligible state
after an artifact attempt begins, restores and re-syncs incomplete state on any
terminal cleanup error, recursively detaches returned artifact records, and
accepts only `YYYY-MM-DDTHH:MM:SS[.fraction]Z` or the equivalent `+00:00` input
before normalizing it to `Z`. The durable and archived specifications were
updated together.

Fresh post-correction evidence:

- `python3 -m unittest evaluations.tests.test_skill_output_writer evaluations.tests.test_folder_scoped_execution -v`
  — 76 tests passed.
- `python3 -m unittest discover -s evaluations/tests -p 'test_*.py'` — 435 tests
  passed.
- `npx openspec validate explicit-skill-output-persistence --strict` — passed.
- `npx openspec validate --all --strict` — all 22 durable specifications passed.
- `npm run validate` with the ignored SDD coordination directory temporarily
  isolated and restored unchanged — formatting passed; 26 drafting tests and 435
  evaluation tests passed; 22 skills were discovered; all 22 OpenSpec items, the
  evaluation corpus, and governance validation passed.
- `git diff --check` — passed.

The archive remains valid, but this post-archive correction supersedes the
earlier statement that no Important findings remained. PR #73 and Issue #65
remain open, and the PR remains draft pending correction re-review and final
controller checks.
