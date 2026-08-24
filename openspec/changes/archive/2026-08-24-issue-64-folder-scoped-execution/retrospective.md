# Retrospective

## Outcome

Issue #64 replaces the pending CaseGraph-coupled execution assumption with one
folder-native contract: named absolute read-only inputs, one absolute writable
output, explicit internet authority, and trusted-host isolation. The public
skills remain independently installable and carry the same compact boundary.

## Evidence

- Pre-archive range: `1e163cd..c10aa89` (8 commits; 40 files; +1,732 / -12).
- Tasks before archive: 12 of 12 checked.
- External dependencies: none.
- Focused result: 14 folder-invocation tests and 37 governance tests passed.
- Full result: 26 drafting tests and 373 evaluation tests passed; 22 skills
  discovered; governance and corpus checks passed.
- OpenSpec state before archive: 21 of 21 items valid.
- Implementation work used four task-sized RED/GREEN dispatches with independent
  reviews and two review-correction rounds for the conformance helper.

Commit chain:

```text
d78dcac docs: plan folder-scoped execution contract
e8bf04e test: define folder invocation boundary
c332450 test: strengthen folder invocation red coverage
b00a168 feat: establish folder-scoped invocation contract
d3345ce fix: bound folder invocation path errors
b256917 fix: align folder invocation path schema
e5b5109 test: protect folder-scoped skill execution
c10aa89 docs: apply folder boundary to public skills
```

## What worked

- Separating schema/runtime conformance from host enforcement made the public
  contract testable without claiming that prompt text is a sandbox.
- Literal manifest fixtures exposed machine-path leakage and preserved stable
  role/path/size/SHA-256 output across relocated roots.
- Review mutations found two real boundary drifts: NUL-containing root errors
  could escape bounded diagnostics, and schema/runtime handling of backslashes
  differed. Both were corrected test-first.
- One compact contract in each `SKILL.md` preserves the boundary when a skill is
  installed alone, while one canonical owner document avoids copying the full
  protocol 22 times.

## Misses and surprises

- The pushed Task 1 RED commit made GitHub Actions report the expected missing
  conformance module before the GREEN commit arrived. The draft PR was behaving
  as a TDD stack, but the isolated CI report looked like an accidental import
  failure without commit context.
- Prettier includes ignored `.superpowers` coordination artifacts. That makes
  the aggregate validation command temporarily red even when every tracked file
  is formatted; the controller must remove the scratch workspace before final
  validation.

## Plan deviations

- Task 2 needed two narrow review-correction commits for bounded NUL-path errors
  and schema/runtime backslash agreement. Both followed new failing tests.
- The Task 5 worker left PR #72 draft despite the plan's final state-transition
  wording because the controller reserved that action until after independent
  whole-branch review. No product behavior changed.

## Boundaries preserved

- The conformance helper is repository validation and host-integration support,
  not a general persistence product or OS sandbox.
- `max_seconds` and `max_input_bytes` are validated declarations returned to the
  trusted host; the helper does not pretend to enforce time, mount, process, or
  network capabilities.
- Output writing, collision policy, atomic persistence, and receipts remain for
  later stories.

## Reusable lessons

- A public isolation contract should distinguish declarative conformance from
  capabilities only the launcher can establish.
- If every RED commit must be pushed, draft-PR CI may intentionally be red;
  commit-specific TDD context should accompany status interpretation.
- Ignored coordination artifacts should be removed before the final aggregate
  formatting gate when repository globs do not honor `.gitignore`.
