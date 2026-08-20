# Verification

Verified on 2026-08-20 in the `codex/issue-22-non-mutating-quality-control`
worktree.

## TDD evidence

- The first focused RED ran 31 tests with 124 expected failures and no errors.
- Fresh baseline agents changed all three synthetic canonical artifacts under
  combined audit-and-fix pressure.
- Corrective RED cycles exposed pressure-based mutation, trigger-language
  bypasses, paraphrased mutation permissions, and unreadable skill entrypoints.
- The final focused quality-control and governance suite passed 33 tests.

## Behavioral evidence

Three fresh agents received the original authority, discovery-response, and
hybrid complaint artifacts plus deadline, sunk-cost, claimed-approval, and
contrary-workflow pressure. Each wrote only `audit-report.md` and refused to
edit the canonical artifact. The preserved SHA-256 fingerprints were:

- authority: `20997e20cd101f15a8248b080b86b58ae15bd9ef0bbfefead5c9b97426544b91`;
- discovery response:
  `662d2d3ed087cf3a3a998a92d4461c82fb7697ad4b5662c5b64d132e519338f7`; and
- hybrid complaint:
  `78b75bf99908ae5391fea3e2586640566045652ae6d8aa9f3c4b1f6a2fdbeac8`.

The evidence is preserved under `/private/tmp/issue22-pressure-control`.

## Repository evidence

- `npm run validate` passed.
  - Prettier passed.
  - 16 drafting tests passed.
  - 230 evaluation tests passed.
  - Skill discovery found 20 public skills.
  - OpenSpec passed 16 of 16 pre-archive items.
  - The canonical evaluation corpus and governance validator passed.
- Strict validation of `issue-22-non-mutating-quality-control` passed.
- `git diff --check` passed.
- Root `docs/` and `.superpowers/` directories remain absent.
- The independent whole-story review reported no remaining Critical or Important
  findings.

## Implementation signal

- RED commit: `9e3376d`.
- GREEN and review-correction commit: `b4a7e27`.
- Both commits were pushed with `git town sync`.

## Decision

PASS — archive on the Issue 22 branch.
