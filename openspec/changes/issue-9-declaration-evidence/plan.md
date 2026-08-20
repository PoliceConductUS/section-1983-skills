# Implementation Plan: Section 1983 Declarations and Evidence

**Goal:** Add one source-bounded public skill for factual human declarations and
exhibit-foundation preparation, with correct Section 1746 language and explicit
human declarant approval before execution.

**Architecture:** A self-contained peer skill classifies every proposed
statement before drafting, prepares one-proposition factual paragraphs and an
exhibit map, and keeps execution blocked until the human declarant approves
every retained exact statement. Existing README, umbrella, and summary-judgment
references route the capability. Standard-library structural tests and five
synthetic fixtures lock the public contract.

**Tech stack:** Markdown public skills, OpenAI YAML metadata, Python standard-
library tests, the existing evaluation harness, OpenSpec with the superpowers
bridge, and Git Town stacked worktrees.

## Task 1: Structure RED

- Add `evaluations/tests/test_declaration_evidence_skill_structure.py` before
  creating the public package.
- Require exact frontmatter name, nonblank discovery metadata, README route,
  umbrella route, and summary-judgment handoff.
- Require both statutory forms, actual-location selection, blank human date and
  signature, classification labels, statement-specific knowledge and competency,
  exhibit prompts, approval choices, and execution prohibition.
- Keep assertions semantic except for stable public labels and statutory text.

## Task 2: Synthetic behavior RED

- Add five fixture directories targeting discovery expectation as personal
  knowledge, derived analysis retained anywhere in the declaration,
  attributed-record content as firsthand knowledge, unsupported exhibit
  foundation, and execution before human approval. Make the execution fixture
  also reject a form selected from residence, venue, or custody instead of
  actual execution location and an edit that retains stale approval.
- Give every fixture bounded generic sources, stable citation IDs, a substantive
  passing candidate, one behavior-specific permanent regression, and a stable
  judgment rubric.
- Add `evaluations/tests/test_declaration_evidence_skill_fixtures.py` to require
  exact target skill, clean passing candidate, exact regression finding and
  location, and unrelated-rule discrimination.
- Run focused RED before any production skill exists and preserve exact output
  under `/private/tmp/declaration-evidence-issue-9`.

## Task 3: Minimal GREEN

- Add only `skills/drafting-section-1983-declarations-and-evidence/SKILL.md` and
  `agents/openai.yaml`.
- Implement required inputs, classification ledger, numbered draft declaration,
  source-bounded exhibit map, excluded material, and approval/execution status.
- Update README, `section-1983-drafting`, and its summary-judgment response
  reference with narrow composition routes.
- Add no script, dependency, private fact, unsupported evidentiary conclusion,
  or code comment.

## Task 4: Review corrections

- Obtain an independent task review against the active spec and public RED
  suite.
- For every accepted finding, first add a focused failing public test, then make
  the smallest production correction and rerun the affected suite.

## Task 5: Behavioral GREEN

- Run fresh no-history scenarios with bounded synthetic inputs for domestic and
  foreign execution, all proposition classes, missing exhibit foundation, and
  one pending approval. Compare the selected execution block with the complete
  applicable statutory form and record the result in `verify.md`.
- Preserve exact outputs outside the repository and verify no personal-
  knowledge laundering, invented foundation, selected strategy, execution, or
  admissibility claim.

## Task 6: Verify and archive

- Run `npm run validate`, all runtime skill validators, strict OpenSpec
  validation, `git diff --check 4f56696..HEAD`, and forbidden-folder checks.
- Produce bridge verification and retrospective artifacts, obtain a fresh
  whole-change review, archive on the Issue #9 branch, replace the generated
  durable purpose placeholder, rerun validation, commit, and run `git town sync`
  after every commit.
