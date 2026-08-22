# Rule 59 Decision Corpus Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish and validate a canonical Rule 59 decision corpus, authorship
coding, denominator limits, retrieval gaps, and neutral transfer cards.

**Architecture:** The existing public skill remains the research workflow and
its Markdown reference remains the coding guide. Two install-local JSON schemas
define the canonical publication objects, while one standard-library script
enforces shape and cross-field invariants against synthetic fixtures.

**Tech Stack:** Markdown, JSON Schema Draft 2020-12 documents, Python 3 standard
library, `unittest`, OpenSpec 1.3.1.

**Spec:**
`openspec/changes/issue-15-rule59-corpus-contract/specs/studying-rule-59e-decisions/spec.md`

## Global Constraints

- One parent record represents one motion-disposition pair.
- Recommendations, adoption-only orders, and independently reasoned final
  decisions remain distinct.
- Incomplete or convenience samples cannot produce tendency or success-rate
  cards.
- Transfer cards are neutral and select no litigation strategy.
- Fixtures are fictional and contain no private case material or machine paths.
- The validator is skill-specific, standard-library-only, offline, and
  traceback-free.
- Do not create root `docs` or `.superpowers` directories.
- Add no code comments; use self-documenting names.
- Commit and run `git town sync` after every commit.

---

### Task 1: RED schemas, CLI, and fixture contract

**Files:**

- Create: `evaluations/tests/test_rule59_corpus_contract.py`

**Interfaces:**

- Consumes: future schemas under
  `skills/studying-rule-59e-decisions/references/`, future fixtures under
  `references/fixtures/`, and future CLI
  `python3 skills/studying-rule-59e-decisions/scripts/validate_corpus.py <corpus.json>`.
- Produces: public-seam tests with stable literal expectations.

- [ ] **Step 1: Capture the no-new-schema behavior baseline**

  In a fresh context, give a worker the current public skill and a bounded
  fictional motion/recommendation/adoption packet. Ask it to produce the
  canonical publication artifact and run the public validator. Preserve the
  output under `/private/tmp/issue-15-rule59-corpus/`; record that the
  schemas/validator do not yet exist and do not change the repository.

- [ ] **Step 2: Add schema coverage tests**

  Assert the canonical schema requires the study manifest, denominator, decision
  records, retrieval gaps, and transfer cards and publicly defines all
  issue-required decision fields and controlled stage values. Assert the
  transfer-card schema requires neutral evidence, source, denominator,
  missingness, and use-limit fields. Compare independently listed required
  literals rather than mirroring schema builders.

- [ ] **Step 3: Add real CLI and fixture tests**

  Execute the future CLI against temporary JSON and every checked-in fixture.
  Require stable findings for malformed input, missing required fields,
  duplicate IDs, broken row references, `authorship-stage-inconsistent`,
  `missing-gap-entry`, `incomplete-tendency`, and `incomplete-success-rate`.
  Require valid complete and incomplete-example fixtures to exit zero.

- [ ] **Step 4: Verify RED, commit, and sync**

  Run:

  ```bash
  python3 -m unittest evaluations.tests.test_rule59_corpus_contract -v
  python3 -m py_compile evaluations/tests/test_rule59_corpus_contract.py
  git diff --check
  ```

  Expected: genuine failures because schemas, fixtures, and CLI are absent.
  Commit only the test file as `test: define Rule 59 corpus contract`, then run
  `git town sync`.

### Task 2: GREEN schemas, validator, and public skill route

**Files:**

- Modify: `skills/studying-rule-59e-decisions/SKILL.md`
- Modify: `skills/studying-rule-59e-decisions/references/corpus-contract.md`
- Create:
  `skills/studying-rule-59e-decisions/references/decision-corpus.schema.json`
- Create:
  `skills/studying-rule-59e-decisions/references/transfer-card.schema.json`
- Create: `skills/studying-rule-59e-decisions/scripts/validate_corpus.py`
- Create:
  `skills/studying-rule-59e-decisions/references/fixtures/valid-complete.json`
- Create:
  `skills/studying-rule-59e-decisions/references/fixtures/valid-incomplete-example.json`
- Create:
  `skills/studying-rule-59e-decisions/references/fixtures/invalid-incomplete-tendency.json`
- Create:
  `skills/studying-rule-59e-decisions/references/fixtures/invalid-authorship-stage.json`

**Interfaces:**

- Consumes: one filesystem path to a canonical JSON corpus.
- Produces: `validate_corpus(corpus: object) -> list[str]`; CLI exit zero with
  `corpus validation passed`, or exit one with one stable line-oriented finding
  per violation.

- [ ] **Step 1: Publish both schemas**

  Use Draft 2020-12 metadata and `additionalProperties: false` at canonical
  object boundaries. Define exact required fields, enums, arrays, integer
  minima, ISO-date patterns, and stable IDs. Make the embedded transfer-card
  definition match the separately published transfer-card schema.

- [ ] **Step 2: Implement vertical validator slices**

  Make one RED test GREEN at a time: malformed JSON/types; required structure;
  controlled values; duplicate IDs; row references; authorship-stage
  consistency; missing-document gap linkage; incomplete tendency; incomplete
  success rate. Catch file, Unicode, JSON, and malformed type failures without
  traceback.

- [ ] **Step 3: Add exactly four synthetic fixtures**

  Use fictional `Example District`, fictional judges/cases, synthetic source
  IDs, and no external paths. The complete fixture contains recommendation,
  adoption-only, and independently reasoned final records. The incomplete valid
  fixture transfers only an example. Each invalid fixture isolates its named
  semantic failure.

- [ ] **Step 4: Update the public route and coding guide**

  Require canonical export and validator success before publication or transfer.
  Retain working-format flexibility, evidence hierarchy, no-selection rules,
  missingness, and authority-verification boundaries. Rename the finding-card
  section to neutral transfer card and make its fields match the schema.

- [ ] **Step 5: Verify GREEN, commit, and sync**

  Run the focused module, all 150 existing evaluations, public skill quick
  validation, `python3 -m compileall` for the new script, targeted Prettier,
  corpus validator over all fixtures, `npm run validate`, and
  diff/forbidden-folder/comment checks. Commit as
  `feat: publish Rule 59 corpus contract`, then run `git town sync`.

### Task 3: Fresh behavior, whole review, verification, and archive

**Files:**

- Modify: `openspec/changes/issue-15-rule59-corpus-contract/tasks.md`
- Create: `openspec/changes/issue-15-rule59-corpus-contract/verify.md`
- Create: `openspec/changes/issue-15-rule59-corpus-contract/retrospective.md`
- Archive through OpenSpec only after review is clean.

**Interfaces:**

- Consumes: complete Issue #15 branch diff, public skill package, and synthetic
  packet.
- Produces: one fresh canonical behavior artifact that passes the public
  validator and a durable archived `studying-rule-59e-decisions` spec.

- [ ] **Step 1: Run a fresh public behavior scenario**

  Give a new worker only the public skill and a bounded fictional packet
  containing a recommendation, adoption order, independently reasoned final
  decision, missing motion, and incomplete denominator. Require canonical JSON
  and neutral example-only transfer; validate the artifact with the public CLI
  and preserve output/hash under `/private/tmp/issue-15-rule59-corpus/`.

- [ ] **Step 2: Run complete verification**

  Run focused and full tests, `npm run validate`, all public skill validators,
  `npx openspec validate --all --json`, fixture matrix, compile, format, diff,
  root forbidden-folder checks, private-path scan, and worktree/origin equality.

- [ ] **Step 3: Review the whole branch**

  Check every durable requirement, schema/validator alignment, fixture
  isolation, authorship consistency, incomplete-sample prohibition, neutral
  transfer behavior, no general-tool creep, and no private material. Correct
  every Critical or Important finding test-first and rerun affected gates.

- [ ] **Step 4: Verify, archive, commit, and sync**

  Complete bridge verify and retrospective artifacts, archive
  `issue-15-rule59-corpus-contract`, rerun full validation, commit the
  evidence/archive changes, and run `git town sync` after each commit.
