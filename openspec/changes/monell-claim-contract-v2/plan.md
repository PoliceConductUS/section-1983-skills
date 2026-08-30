# Monell Claim Contract Version 2 Implementation Plan

> **For agentic workers:** Use superpowers:subagent-driven-development to
> implement this plan task-by-task.

**Goal:** Ship strict typed individual-capacity, qualified-immunity, and Monell
complaint handoffs, two focused Monell skills, and a fail-closed read-only
on-disk CaseGraph assessment receipt that resolves every used authority pinpoint
to exact verified source text.

**Architecture:** `drafting-section-1983-complaints` owns the version-2 JSON
contract and a standard-library validator. A reasoned skill-layer adapter may
inspect supported CaseGraph YAML directly and read-only, while the validator
checks the resulting receipt, graph and pleading fingerprints, cited artifact
hashes, and exact text matches without invoking the CaseGraph CLI. Planning and
drafting remain separate skills; Filing CI reports structural validation and
graph assessment as distinct gates.

**Tech Stack:** Markdown Agent Skills, JSON contracts and fixtures, Python 3
standard library, `unittest`, OpenSpec, Prettier, skills CLI.

---

## Task 1: Freeze the strict contract behavior in failing tests

- [ ] **Step 1:** Add `evaluations/tests/test_monell_contract_v2.py` with a
      minimal valid version-2 handoff fixture builder.
- [ ] **Step 2:** Add RED cases for version 1, missing individual
      actor/time/causation fields, missing QI fields, merged Monell path types,
      and each path-specific omission.
- [ ] **Step 3:** Add RED cases for graph statuses, draft fingerprint mismatch,
      referenced-file hash mismatch, unresolved pinpoint, text mismatch, and
      ambiguous exact passage.
- [ ] **Step 4:** Run
      `python3 -m unittest evaluations.tests.test_monell_contract_v2 -v` and
      record the expected import/file failures.
- [ ] **Step 5:** Commit the RED tests with
      `test(monell): define strict v2 contract behavior` and push.

## Task 2: Implement the canonical version-2 contract and validator

- [ ] **Step 1:** Replace
      `skills/drafting-section-1983-complaints/references/complaint-structure-contract.json`
      with the version-2 vocabulary, required typed units, path-specific
      requirements, assessment states, and finding contract specified in
      `design.md`.
- [ ] **Step 2:** Add
      `skills/drafting-section-1983-complaints/scripts/validate_complaint_handoff.py`
      with `validate_handoff(data, base_dir=None, mode="drafting")` and a
      JSON-file CLI.
- [ ] **Step 3:** Implement stable findings for unsupported version, universal
      and conditional field absence, duplicate IDs, invalid path typing,
      cross-reference targets, assessment coverage, fingerprints, file hashes,
      and authority resolution.
- [ ] **Step 4:** Verify exact passage matching against the receipt's
      provenance-linked text file after only recorded deterministic
      normalization; reject missing, mismatched, or ambiguous matches.
- [ ] **Step 5:** Update
      `skills/drafting-section-1983-complaints/references/complaint-contract.md`
      and `skills/drafting-section-1983-complaints/SKILL.md` to require the
      validator and preserve legal-judgment boundaries.
- [ ] **Step 6:** Run the focused test module until green, then run the existing
      complaint contract and candor tests.
- [ ] **Step 7:** Commit with `feat(complaints): enforce claim contract v2` and
      push.

## Task 3: Add the Monell planning skill test-first

- [ ] **Step 1:** Add RED structure and behavior tests in
      `evaluations/tests/test_monell_claim_skills.py` for install-local
      references, separate path records, recommendation enums, contrary
      material, missing connections, temporal lanes, exact authority resolution,
      and plaintiff-reserved selection.
- [ ] **Step 2:** Create `skills/planning-section-1983-monell-claims/SKILL.md`,
      `agents/openai.yaml`, and focused references for the path inventory,
      recommendation record, CaseGraph assessment, and authority-resolution
      receipt.
- [ ] **Step 3:** Require direct read-only `config.yaml` and `<uid>/root.yaml`
      inspection when an explicit graph path is supplied; never search for or
      invoke a CLI.
- [ ] **Step 4:** Run the new behavior tests and `npx skills add . --list`;
      correct only observed failures.
- [ ] **Step 5:** Commit with `feat(monell): add claim planning skill` and push.

## Task 4: Add the Monell drafting skill test-first

- [ ] **Step 1:** Extend the RED behavior tests for approved-path-only drafting,
      path-specific typed deltas, information-and-belief bases, mechanism
      placement, temporal limitations, and no silent claim selection.
- [ ] **Step 2:** Create `skills/drafting-section-1983-monell-claims/SKILL.md`,
      `agents/openai.yaml`, and references for the approved planning handoff and
      complaint delta.
- [ ] **Step 3:** Route the delta back to the canonical complaint owner and
      require a version-2 validator rerun after integration.
- [ ] **Step 4:** Update `skills/drafting-section-1983-complaints/SKILL.md`,
      `references/claim-specific-contracts.md`, and `README.md` composition
      guidance.
- [ ] **Step 5:** Run the focused tests and skill discovery until green.
- [ ] **Step 6:** Commit with `feat(monell): add approved-path drafting skill`
      and push.

## Task 5: Integrate Filing CI modes and result separation

- [ ] **Step 1:** Add RED tests in `evaluations/tests/test_monell_filing_ci.py`
      for drafting versus filing mode and all assessment statuses.
- [ ] **Step 2:** Update `skills/filing-ci/SKILL.md` so drafting mode permits
      explicit unassessed states but filing mode requires current coverage of
      every included unit and leaves partial or unresolved authority components
      open.
- [ ] **Step 3:** Require output to preserve separate `structural_validation`
      and `casegraph_assessment` objects and prohibit an unqualified aggregate
      pass.
- [ ] **Step 4:** Run Filing CI and non-mutating quality-control tests until
      green.
- [ ] **Step 5:** Commit with
      `feat(filing-ci): enforce assessed claim contract v2` and push.

## Task 6: Complete metadata and corpus integration

- [ ] **Step 1:** Add both skills to `governance/rules-provenance.json` with
      their correct runtime-sourced or bundled-rules-dependent ownership.
- [ ] **Step 2:** Add synthetic evaluation fixtures demonstrating a passing
      separated Monell analysis and regressions for omnibus paths, post-event
      temporal leakage, and citation-string-only authority treatment.
- [ ] **Step 3:** Update `README.md` skill table, composition order, and
      complaint-checker boundary to describe the two-layer v2 system accurately.
- [ ] **Step 4:** Run `npm run format`, the focused test modules,
      `npm run evaluations:corpus`, and `npm run governance:validate`.
- [ ] **Step 5:** Commit with `test(monell): cover v2 skill integration` and
      push.

## Task 7: Verify and close the OpenSpec change

- [ ] **Step 1:** Run `npm run validate` from the worktree root and preserve its
      complete result.
- [ ] **Step 2:** Complete
      `openspec/changes/monell-claim-contract-v2/verification.md` with commands,
      outcomes, and exact implementation commit.
- [ ] **Step 3:** Complete
      `openspec/changes/monell-claim-contract-v2/retrospective.md`, check every
      completed item in `tasks.md`, and validate the change.
- [ ] **Step 4:** Archive the OpenSpec change on this branch using the
      repository's OpenSpec workflow, rerun `npm run validate`, commit with
      `docs(openspec): archive Monell contract v2`, and push.
