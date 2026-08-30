# Verification

## Branch and scope

- Branch: `codex/issue-64-folder-boundary`
- Parent: `main` at `1e163cd`
- Pre-archive reviewed HEAD: `c10aa89`
- Commit range: `1e163cd..c10aa89` (8 commits; 40 files; +1,732 / -12)
- Issue #64 and draft PR #72 remain open. The controller owns the final
  draft-to-ready transition after independent whole-branch review.
- No CaseGraph, CaseHome, Git, MCP, resource-URI, virtual-filesystem, bridge,
  output-writer, persistence-manager, or external runtime dependency was added.

## Whole-story review

The review checked schema/runtime agreement, strict envelope shapes, canonical
root containment, target and child traversal, file and directory symlink
handling, directory-cycle rejection, deterministic logical manifests, bounded
CLI diagnostics, truthful host-enforcement language, and all 22 public skill
packages. The first self-review found no defect. Independent whole-branch review
then proved two Important false-green classes: runtime child paths normalized
raw syntax that the schema rejected, and parser or manifest recursion exhaustion
could escape the bounded-error contract. Focused RED tests now cover both, and
the narrow corrections preserve the existing public error codes and normal
manifest behavior.

The validator proves only invocation conformance, confined resolution, target
selection, and logical fingerprints. It does not claim to enforce read-only
mounts, undeclared-path denial, runtime limits, or network policy; those remain
trusted-host responsibilities.

## Fresh verification evidence

- `python3 -m unittest evaluations.tests.test_folder_scoped_execution -v` — 17
  tests passed.
- `python3 -m unittest evaluations.tests.test_repository_governance -v` — 37
  tests passed.
- `python3 -m unittest discover -s evaluations/tests -p 'test_*.py'` — 376 tests
  passed.
- `npm run test:unit` — 26 drafting tests and 376 evaluation tests passed.
- `npm run skills:list` — discovered 22 public skills.
- `npm run openspec:validate` — 21 of 21 items passed before archive.
- `npm run evaluations:corpus` — passed and reproduced the tracked corpus
  reports without a diff.
- `npm run governance:validate` — passed.
- `git ls-files '*.json' '*.md' '*.yml' '*.yaml' | xargs npx prettier --check` —
  every tracked JSON, Markdown, and YAML file passed formatting.
- `git diff --check origin/main...HEAD` — passed.
- Forbidden dependency search — only explicit OpenSpec non-dependency language
  and a pre-existing MCP authority reference were found; no new dependency or
  runtime import exists.
- Standard-library import review — the new helper imports only Python standard
  library modules.
- Origin parity before archive — local and origin were both at `c10aa89`.

`npm run validate` reached formatting and stopped only because Prettier scans
the intentionally ignored `.superpowers/sdd/plan/` coordination files. Those
files are not product content and are retained temporarily so the controller can
consume this report and run the independent whole-branch review. Every tracked
validation stage was then run directly and passed. The controller will remove
that ignored workspace and rerun the exact aggregate gate before the
ready-for-review transition.

## TDD and review trace

- Task 1 recorded the missing-module RED for the invocation seam and then
  strengthened canonical-root, shape, and path cases.
- Task 2 supplied the standard-library GREEN implementation. Review-driven RED
  tests closed NUL-path diagnostic leakage and schema/runtime backslash drift.
- Task 3 recorded governance RED across every public skill.
- Task 4 added the protected governance gate and the compact four-sentence
  install-local contract to all 22 public skills. Independent task review was
  clean.
- Final independent review added RED coverage for raw dot, empty, trailing,
  drive-prefixed, and NUL child-path segments across target/input/output APIs.
  The shared helper now rejects them consistently with the schema while
  preserving valid POSIX newline names.
- The same review reproduced unbounded `RecursionError` behavior in the CLI JSON
  parser and deep manifest traversal. Both now return stable bounded errors with
  no stderr traceback or installation-path leakage.

## Archive verification

The repository-local OpenSpec CLI archived this change as
`2026-08-24-issue-64-folder-scoped-execution`, created the durable
`folder-scoped-skill-execution` specification, and updated the durable
`repository-skill-governance` specification. The generated placeholder Purpose
was replaced with the concrete capability statement above. Post-archive
durable-spec and repository validation results are recorded in the Task 5
report.

## Decision

PASS for archive and independent whole-branch review. The branch is
implementation-complete; the controller retains the ignored-workspace cleanup,
fresh aggregate validation, push/parity confirmation, and PR state transition.
