# Issue #33 Judicial Reasoning Profiles Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans
> to implement this plan task-by-task.

**Goal:** Replace the embedded real-judge skill with one generic folder-native
builder for immutable Judicial Reasoning Profile packages.

**Architecture:** A self-contained public skill owns domain instructions,
schema, fixtures, and deterministic validation. Repository trusted-host code
continues to own the common package loader/publisher. Acquisition and
compilation are distinct invocation operations; profile data remains separate
from future static judicial-reviewer behavior.

**Tech stack:** Markdown skills, JSON Schema Draft 2020-12, Python standard
library, `unittest`, existing folder invocation and immutable package APIs.

## Global constraints

- No real-judge content, conclusion, skill, fixture, or generated instructions.
- No CaseGraph, Git, registry, launcher, role sweep, or persistent agent.
- All fixtures are fictional and public-safe.
- Every behavior change follows observed RED, minimal GREEN, and immediate push.
- Historical archived OpenSpec records remain immutable.

### Task 1: Exact skill package and fictional fixtures

**Files:**

- Create: `evaluations/tests/test_judicial_reasoning_profiles.py`
- Create: `skills/building-judicial-reasoning-profiles/SKILL.md`
- Create: `skills/building-judicial-reasoning-profiles/agents/openai.yaml`
- Create:
  `skills/building-judicial-reasoning-profiles/references/folder-contract.json`
- Create:
  `skills/building-judicial-reasoning-profiles/references/immutable-folder-package.md`
- Create:
  `skills/building-judicial-reasoning-profiles/references/judicial-reasoning-profile.schema.json`
- Create: `skills/building-judicial-reasoning-profiles/references/fixtures/*`

- [ ] Test the exact install-local surface, discovery metadata, folder roles,
      two operation modes, schema fields, and fictional package fixtures.
- [ ] Confirm RED because the generic package does not exist.
- [ ] Add the minimal generic public package and confirm structure tests GREEN.
- [ ] Commit and push RED and GREEN separately.

### Task 2: Install-local domain validator

**Files:**

- Create:
  `skills/building-judicial-reasoning-profiles/scripts/validate_judicial_profiles.py`
- Modify: `evaluations/tests/test_judicial_reasoning_profiles.py`

- [ ] Test valid complete and thin profiles; exact source classes; adoption,
      recommendation, and outcome attribution; copied comparison values;
      transfer eligibility; forbidden behavior fields and characterization;
      malformed bytes; and byte limits.
- [ ] Confirm RED for missing validator or behavior.
- [ ] Implement a deterministic standard-library validator that returns a
      canonical validated object and bounded stable errors without writes.
- [ ] Confirm focused tests GREEN in a copied isolated skill package.
- [ ] Commit and push RED and GREEN separately.

### Task 3: Trusted-host operation boundary

**Files:**

- Modify: `evaluations/tests/test_judicial_reasoning_profiles.py`
- Modify only if needed: `scripts/immutable_folder_package.py`

- [ ] Test installed-contract validation for internet-authorized acquisition and
      internet-disabled compilation, separate output packages, no same-run
      acquisition consumption, complete common-envelope publication, and input
      byte preservation.
- [ ] Confirm RED for the missing operation composition seam.
- [ ] Add only the minimal repository trusted-host composition required to call
      existing folder/package APIs; keep helpers output-root-free and read-only.
- [ ] Confirm package output reloads and input fingerprints remain unchanged.
- [ ] Commit and push RED and GREEN separately.

### Task 4: Embedded-profile removal and current migration

**Files:**

- Delete: `skills/drafting-for-judge-scholer/**`
- Modify: `README.md`, `JUDGE_OVERLAYS.md`, `GOVERNANCE.md`
- Modify: `skills/section-1983-drafting/SKILL.md`
- Modify: current tests and governance contracts that name the removed package
- Modify: active OpenSpec requirements that name the removed package

- [ ] Test that current public surfaces and discovered skills contain no real-
      judge dependency while archived history remains untouched.
- [ ] Migrate receipt runtime tests to a synthetic temporary generic static-role
      contract and keep receipt behavior unchanged.
- [ ] Update the approved folder-contract matrix and rules registry through
      discovered-skill validation.
- [ ] Commit and push RED and GREEN separately.

### Task 5: Verification and archive

**Files:**

- Create: `openspec/changes/issue-33-judicial-profiles/verify.md`
- Create: `openspec/changes/issue-33-judicial-profiles/retrospective.md`
- Modify: `openspec/changes/issue-33-judicial-profiles/tasks.md`

- [ ] Run focused tests, isolated package validation, Python compilation,
      `npm run validate`, and `git diff --check`.
- [ ] Review the complete stacked diff against live Issue #33 and correct every
      finding through RED/GREEN.
- [ ] Record evidence and archive with
      `npx openspec archive issue-33-judicial-profiles -y`.
- [ ] Re-run full validation, push the archive, require exact GitHub checks,
      mark ready, and leave both PR and issue open.
