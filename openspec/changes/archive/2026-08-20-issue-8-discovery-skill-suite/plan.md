# Implementation Plan: Section 1983 Discovery Skill Suite

**Goal:** Add five coordinated, separately tested public discovery skills with
traceable targets, bounded proportionality, no assumed evidence, and plaintiff-
reserved strategy.

**Architecture:** The existing `section-1983-drafting` skill routes the suite
and hosts a consolidated coordination reference. Five peer capabilities jointly
own the operative contract for written discovery, response audit,
meet-and-confer drafting, privilege-log requirements and audit, and deposition
outlines. Standard-library structural tests and five synthetic corpus fixtures
lock the public contracts before implementation.

**Tech stack:** Markdown public skills, OpenAI YAML discovery metadata, Python
standard-library tests, the existing evaluation harness, OpenSpec with the
superpowers bridge, and Git Town stacked worktrees.

## Task 1: Public decomposition RED

- Add a focused structural test that requires the five named new skill
  directories, `SKILL.md`, `agents/openai.yaml`, README, and
  `section-1983-drafting` routing without constraining unrelated present or
  future skill packages.
- Resolve every peer skill's Markdown links and require each relative target to
  remain inside that peer's directory so standalone installation cannot depend
  on a sibling skill.
- Require the same compact traceability literals and independent workflow
  boundary in every peer skill.
- Run before creating any peer skill and preserve the missing-file failures.

## Task 2: Cross-skill contract RED

- Require stable target or request IDs, claim, defendant, element, factual gap,
  likely custodian, expected native source, approved source IDs, bounded scope,
  proportionality, existence-first drafting, and `PLAINTIFF DECISION REQUIRED`.
- Require specific per-skill ownership and prohibit overlaps: assumed record
  content, silence-as-nonexistence, automatic waiver or sanctions, invented log
  facts, scripted testimony, and selected strategy.
- Keep tests semantic enough to permit clearer prose and harmless layout
  changes.

## Task 3: Synthetic regressions RED

- Add five Markdown fixtures targeting assumed-content written discovery,
  acceptance of a boilerplate objection without production status, selected
  narrowing in a meet-and-confer, automatic privilege waiver, and scripted
  expected deposition testimony.
- Prove complete, nonblank `target_id`, `claim`, `defendant`, `element`,
  `factual_gap`, `likely_custodian`, `expected_native_source`, approved source
  IDs, and bounded proportionality through structural assertions and fresh
  behavior, without imposing an unrequested JSON output format.
- Mutate cloned contracts with unrelated deterministic rules and prove generic
  failures cannot satisfy any behavior-specific expectation.

## Task 4: Implement shared coordination

- Add `references/discovery-coordination-contract.md` under the existing
  drafting skill with field definitions, proportionality, existence-versus-
  content, localization, source, strategy, and composition rules.
- Update the umbrella routing order and README without expanding the umbrella
  skill into discovery drafting or audit.

## Task 5: Implement five peer skills

- Add only `SKILL.md` and `agents/openai.yaml` for each peer skill unless a
  reviewed RED case proves a peer-specific reference is necessary.
- Keep each skill self-contained, repeat the compact shared contract, and give
  it exact inputs, ordered workflow, output sections, prohibited actions,
  strategy gates, and handoffs.
- Add no script, dependency, private fact, court-specific unsupported rule, or
  code comment.

## Task 6: Behavioral GREEN and review

- Run one fresh no-history agent per skill with a bounded synthetic packet and
  approved source IDs only.
- For each output, check traceability, non-assumption, proportionality,
  plaintiff-reserved decisions, and the peer skill's unique responsibility.
- Obtain an independent task review. Add a focused failing test before every
  accepted correction, implement the narrow fix, and rerun affected scenarios.

## Task 7: Verify and archive

- Run `npm run validate`, all runtime skill validators, strict OpenSpec
  validation, `git diff --check dd6a866..HEAD`, and forbidden-folder checks.
- Produce bridge verification and retrospective artifacts, obtain a fresh
  whole-change review, archive on the Issue #8 branch, replace generated durable
  purpose placeholders, rerun validation, commit, and run `git town sync` after
  every commit.
