# Verification

## Implementation identity

- Branch: codex/monell-claim-contracts
- Strict-v2 implementation commit: fdba3dd5825465d1ca14d92beec8fa9a8c0d1f43
- Core integration commit: 271c673
- Contract implementation commit: f9eba8d
- OpenSpec design and exact-text requirement commit: 02d9671

## Automated verification

The final pre-archive run of npm run validate passed on 2026-08-30:

- Prettier format check: passed.
- Section 1983 drafting unit tests: 26 passed.
- Evaluation tests: 375 passed.
- Skill discovery: 24 skills found, including both new Monell skills.
- OpenSpec validation: 21 items passed, 0 failed.
- Evaluation corpus: passed, including all three permanent Monell v2
  regressions.
- Governance validation: passed.

Focused contract tests also passed eight tests covering strict v1 rejection,
typed individual and QI records, every Monell path type, typed principal
approval, supporting-fact temporal mapping, filing mode, graph-file hashes,
claim-component receipts, opinion/text hashes, pinpoint, and exact passage.

## Independent forward evaluations

Read-only forward evaluators tested the Irving-style scenario before and after
correction. Their final results were:

- planning skill: PASS after allowing multiple distinct candidates of the same
  path type and strengthening the all-six synthetic fixture;
- drafting skill: PASS after aligning principal-decision keys, requiring a
  verifiable decision record, typing information-and-belief and temporal lanes,
  and enforcing exact authority resolution.

## Boundaries verified

- No CaseGraph CLI or running service is invoked.
- The stored graph is read only.
- A completed receipt fingerprints every used graph file and every included
  claim unit.
- Used authority resolves to verified opinion bytes and hash, provenance-linked
  text and hash, pinpoint, and one exact passage.
- Structural validation and reasoned assessment remain separate.
- No recommendation selects or abandons a claim for the litigation principal.
