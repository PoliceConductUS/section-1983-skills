# Verification

## Branch and scope

- Branch: `codex/issue-24-unified-complaint-contract`
- Parent: `codex/issue-23-immutable-version-audit-reports`
- Pre-archive reviewed HEAD: `bc608ac9658f7c83f02ff6dcca93b5937a48bc5d`
- Origin parity before archive: local and origin both at
  `bc608ac9658f7c83f02ff6dcca93b5937a48bc5d`
- Commits: RED `1c84458`, RED seam correction `3f3bb80`, canonical owner
  `a107ac9`, full GREEN `96f6486`, review correction `bc608ac`
- No executable checker, dependency, workflow, root `docs/`, or `.superpowers/`
  directory was added. CaseGraph issue 18 remains the executable-checker owner.

## Structural contract

- `drafting-section-1983-complaints` is the only package containing
  `complaint-structure-contract.json`.
- Its Markdown contract owns the ordered skeleton and the sixteen machine field
  identifiers while preserving Element as the first of five count functions.
- The umbrella complaint entry routes and fails closed without a fallback.
- The false-arrest package contains an install-local specialization delta and no
  generic skeleton, complete generic field list, general qualified-immunity
  matrix, or general Monell contract.
- Live local links were resolved in isolated copies of all three packages.

## Behavioral pressure

- Umbrella-only: **complaint contract unavailable**; the agent named the missing
  owner and both missing references without reconstruction. Output SHA-256:
  `8cdb677067f37f4d19a584d4b9f641fb6a60c3638394eadf30c57bc9ed82a6f5`.
- General-only: one complete canonical contract and stable bounded mechanical
  handoff. Preserved verdict SHA-256:
  `dac72c5094960707ff2cfdca21e1414269aac159908592d73913931c1a64e4c9`.
- Full false-arrest stack: one general owner, routing without fallback,
  universal governance without competing ownership, and specialization-only
  complaint-construction deltas. Preserved verdict SHA-256:
  `a082a4f98fb3bc8d2f316a230a3cdb0042e66ec65b13afab0bf82970b4b1319a`.

The first GREEN runs found and drove tests for three real inconsistencies:
Element as a mistaken seventeenth machine field, the umbrella reference index
calling the complaint route a skeleton, and an obsolete four-function count
sequence. Corrected fresh contexts found no remaining contract gap within the
approved mechanical scope.

## Mutation evidence

The focused suite rejects:

- removal of a required section;
- permission to draft, revise, or audit while the canonical contract is
  unavailable, even when a separate non-invention sentence remains;
- a second machine-contract owner;
- one canonical backticked machine field added to the false-arrest delta;
- a complete generic field list in the delta;
- a local-link traversal or symlink escape;
- a legal judgment moved from exclusions into deterministic checks;
- human/JSON field drift; and
- a competing count-function sequence.

## Review

The whole-story reviewer found two Important test gaps: the narrow fail-closed
inversion and single-field delta regression. Commit `bc608ac` added both
mutation guards. The one required scoped re-review was CLEAN and confirmed the
exact mutations now fail without banning legitimate false-arrest prose or
universal governance.

## Commands

- `python3 -m unittest evaluations.tests.test_complaint_contract_composition -v`
  — 12 passed after the review correction.
- `python3 -m py_compile evaluations/tests/test_complaint_contract_composition.py`
  — passed.
- `npm run validate` — passed before archive: formatting; 16 drafting tests; 245
  evaluation tests; 20 discovered skills; 16 OpenSpec items; corpus evaluation;
  governance.
- `openspec validate issue-24-unified-complaint-contract --strict` — passed.
- `quick_validate.py` — passed for the umbrella, general complaint, and
  false-arrest packages.
- `git diff --check` — passed.

## Remote state

Live GitHub Issue 24 was verified OPEN. Its acceptance criteria match this
change and expressly require no PR and no issue closure.
`gh pr list --head codex/issue-24-unified-complaint-contract --state all`
returned an empty list.

## Archive verification

OpenSpec archived the change as
`2026-08-22-issue-24-unified-complaint-contract`. The generated durable purpose
was replaced with the approved capability purpose rather than leaving a TBD.
After archive, `npm run validate` passed formatting, 16 drafting tests, 247
evaluation tests, 20 discovered skills, 16 durable OpenSpec specifications,
corpus evaluation, and governance. The focused 12-test composition suite and
`git diff --check` also passed.
