# Verification

## Branch and scope

- Branch: `codex/issue-66-filing-packets`.
- Stacked base: `codex/issue-67-qc-output` at
  `0c3791ef2d0c8ca1ba4894846b4038acd20f0c56`.
- Pre-archive reviewed HEAD: `073d634021c56b9c786f0fe92b30d843752698b0`.
- Pre-archive range: 10 commits; 41 files; 1,275 insertions.
- Live Issue #66 and draft PR #77 remain open. The PR stays draft through
  archival and exact-head verification.
- The implementation uses only declared folders and the existing trusted-host
  output writer. It adds no CaseGraph or electronic-filing dependency.

## Acceptance-criteria review

- `filing-packet.json` fixes stable IDs, deterministic order, independent kinds
  and roles, canonical relative paths, exact sizes, SHA-256 values, and source
  and input-manifest provenance.
- Runtime validation requires exactly one `main`, expressly authorized other
  roles, regular canonical manifest/member paths, confined matching files, and
  unique IDs and paths.
- Publication requires an invocation bound to one installed skill contract and
  creates one complete append-immutable packet beneath the explicit output root
  without changing source or context inputs.
- Whole-packet and exact-member targeting are distinct. Mechanical readiness
  requires each configured gate to pass and cover every packet member without
  deciding legal quality, strategy, filing authorization, or electronic filing.
- Complaint, motion-with-amended-complaint, response, and multi-exhibit fixtures
  exercise order, kind/role separation, hashes, confinement, provenance, target
  selection, and gate coverage.
- Each current filing skill covered by this story retains an install-local
  FilingPacket contract, including `drafting-for-judge-scholer`.

## TDD and review trace

- `81cafaf` established the initial FilingPacket RED; `0b0a32a` supplied the
  initial GREEN; `f633c1d` made the shared contract install-local.
- Fresh review found four Important gaps: external and in-root symlink aliases,
  generic rather than installed-contract-bound publication, boolean-version and
  schema/runtime path drift, and the omitted Scholer package contract.
- `235cdc3` recorded the four-gap RED. `2fd80d9` rejected aliases and unbound
  publication, aligned schema versions, and completed current-skill coverage.
- A fresh path-language comparison found an unbounded `IndexError` for `.` and
  newline disagreement between the schema and POSIX runtime. `22f1a77` recorded
  the RED and `073d634` supplied the final GREEN.
- The final whole-story review compared the implementation and documentation to
  the live Issue #66 body and found no remaining Critical, Important, or Minor
  issue.

## Fresh pre-archive evidence

- `python3 -m unittest evaluations.tests.test_filing_packets` passed 8 tests.
- `python3 -m py_compile scripts/filing_packet.py evaluations/tests/test_filing_packets.py`
  passed.
- `npm run validate` passed formatting, 27 drafting tests, 503 evaluation tests,
  discovery of 22 skills, all 24 active OpenSpec items, corpus evaluation, and
  governance validation.
- `git diff --check` passed, and the tracked worktree was clean and synchronized
  with origin at the reviewed HEAD.

## Decision

PASS for archive. Final readiness requires the archived durable specifications,
fresh repository validation, a pushed archive commit, and exact remote/check
verification. PR #77 and Issue #66 remain open under the close-on-merge policy.

## Archive verification

The repository-local OpenSpec CLI archived this change as
`2026-08-25-issue-66-filing-packets`. It created the durable
`filing-packet-lifecycle` specification with four requirements and added the
public FilingPacket package-boundary requirement to
`repository-skill-governance`.

- `npm run validate` passed formatting, 27 drafting tests, 503 evaluation tests,
  discovery of 22 skills, all 24 durable OpenSpec specifications, corpus
  evaluation, and governance validation.
- `git diff --check` passed after archival and durable-spec formatting.

The archive commit, exact remote parity, GitHub validation, and draft-to-ready
transition remain pending at this checkpoint. PR #77 and Issue #66 remain open.
