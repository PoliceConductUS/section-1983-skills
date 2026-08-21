# Verification

Verified on 2026-08-21 in the `codex/issue-23-immutable-version-audit-reports`
worktree.

## TDD evidence

- The focused pre-implementation governance suite ran 34 methods with 66
  expected report-contract failures. After explicit traversal, symlink, live
  description, and negative-control coverage was added, the bounded RED set ran
  7 methods with 78 expected failures.
- The final focused governance suite passed 35 tests.
- The existing non-mutation and focused governance suites passed 38 tests
  together.

## Behavioral evidence

The RED pressure run showed three distinct failures: an authority agent
attempted to overwrite the prior report, a discovery agent wrote outside the
audited version folder, and a hybrid review agent wrote beside the filing.

Three fresh GREEN agents received the same conflicting instructions. Each wrote
one new uniquely named report under the audited version's `audits/` directory.
The authority run preserved the requested overwrite target, the discovery run
refused the external shared path, and the hybrid run refused beside-filing
output and same-stage remediation.

The canonical artifact and prior-report SHA-256 fingerprints remained:

- authority: `f39006684d48585626148794f037670103b56ddd8430e0d01d3bace4b691a018`
  and `e2573471784c2fd8e5dc9bbdfbb8e275275844ad21e056a27cc0c554a3f060b7`;
- discovery: `b557972a1571120b77727433af906a1a842be8234e7a6219150e76de2d74dd68`
  and `29f8115ef8fb35d2e7f57ef9ae3100c75230f49d5525ae415530d5a69d196259`;
- hybrid: `b1c75258ebfca577d57dae851e07124fceb441a5626f30ea24c1286e69f2a7e1` and
  `c15390fc19fd8af8212c74415b478a192db9c136bd940807422b5fe03797f107`.

## Repository evidence

- `npm run validate` passed.
  - Prettier passed.
  - 16 drafting tests passed.
  - 235 evaluation tests passed.
  - Skill discovery found 20 public skills.
  - OpenSpec passed 16 of 16 pre-archive items.
  - The canonical corpus and governance validator passed.
- All nine changed skill packages passed `quick_validate.py`.
- Strict validation of `issue-23-immutable-version-audit-reports` passed.
- `git diff --check` passed.
- The independent whole-story review reported no Critical, Important, or Minor
  findings.

## Implementation signal

- RED commit: `b27be36`.
- GREEN commit: `dec6673`.
- Both commits were pushed with `git town sync`.

## Decision

PASS — archive on the Issue 23 branch.
