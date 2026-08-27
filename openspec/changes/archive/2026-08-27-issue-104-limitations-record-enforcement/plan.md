# Limitations Record Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve the complete defendant-identity and diligence timeline and
enforce one structurally valid limitations record for every affected intended
individual at the installed complaint-checker seam.

**Architecture:** Add a required `limitations_gate` object and JSON Schema to
the existing complaint mechanical handoff. Native validators in the canonical
complaint checker and independently installed Filing CI derive affected
defendants and enforce shape, cardinality, sources, dates, and fail-closed
status while retaining all legal conclusions as excluded judgments.

**Tech Stack:** Markdown agent skills, OpenSpec, JSON Schema, Python `unittest`,
native Python JSON validation, YAML pressure fixtures.

**Spec:**
`openspec/changes/issue-104-limitations-record-enforcement/specs/drafting-section-1983-complaints/spec.md`

## Global Constraints

- No universal numeric definition of “near limitations.”
- No deterministic decision about fact truth, legal sufficiency, authority fit,
  relation back, tolling, mistake, notice or service sufficiency, strategy,
  requested relief, or filing readiness.
- No CaseGraph, graph, repository, package, persistence, network, or ambient
  filesystem dependency.
- Original input folders remain recursively read-only; outputs and temporary
  work retain the existing folder-scoped boundary.
- No change to false-arrest seizure timing, actor causation, or
  arresting-officer defendant ordering.

---

### Task 1: RED installed-checker contract

**Files:**

- Modify: `evaluations/tests/test_installed_filing_checks.py`
- Create: `evaluations/unknown-defendant-limitations/v2/records.json`

**Interfaces:**

- Consumes: complaint JSON handoffs with intended-individual trigger entries and
  candidate limitations records.
- Produces: literal stable check IDs for missing gate, missing affected record,
  malformed event, unresolved entry, schema drift, and prohibited legal-judgment
  expansion.

- [ ] Add literal valid and invalid handoff fixtures and tests that invoke both
      real installed checkers.
- [ ] Run `python3 -m unittest evaluations.tests.test_installed_filing_checks`
      and confirm failure because Issue #102 has no limitations schema or
      validator.
- [ ] Commit and push the RED public-seam evidence.

### Task 2: RED skill pressure

**Files:**

- Create: `evaluations/unknown-defendant-limitations/v2/pressure-scenarios.yaml`
- Modify: `openspec/changes/issue-104-limitations-record-enforcement/verify.md`

**Interfaces:**

- Consumes: fresh contexts containing deadline pressure, unresolved intended
  defendants, distinct source dates, incomplete authority, and a demand to file.
- Produces: exact outputs scored for gate activation, date separation,
  defendant-specific gaps, authority completeness, and filing-ready refusal.

- [ ] Define pressure prompts without stating the expected response.
- [ ] Run the prompts against an isolated copy of the Issue #102 skill and
      preserve exact baseline outputs and scores.
- [ ] Identify the observable baseline failures before editing guidance.

### Task 3: Canonical schema and complaint checker

**Files:**

- Create:
  `skills/drafting-section-1983-complaints/references/limitations-record.schema.json`
- Modify:
  `skills/drafting-section-1983-complaints/references/complaint-structure-contract.json`
- Modify: `skills/drafting-section-1983-complaints/scripts/check_complaint.py`

**Interfaces:**

- Consumes: `limitations_gate` with intended-individual entries, records, gaps,
  and `clear|blocked` status.
- Produces: deterministic hard findings using declared contract check IDs.

- [ ] Add the JSON Schema matching the approved record sections and enums.
- [ ] Add the limitations check IDs to the mechanical contract without removing
      any excluded legal judgment.
- [ ] Implement trigger derivation, unique-ID and record-cardinality checks,
      required structure, ISO-date and source-reference checks, and unresolved
      fail-closed checks.
- [ ] Run the focused installed-checker tests and confirm the canonical checker
      reaches GREEN.
- [ ] Commit and push the canonical checker implementation.

### Task 4: Filing CI installed alignment

**Files:**

- Create: `skills/filing-ci/references/limitations-record.schema.json`
- Modify: `skills/filing-ci/references/complaint-checker-contract.json`
- Modify: `skills/filing-ci/scripts/run_filing_ci.py`
- Modify: `evaluations/tests/test_installed_filing_checks.py`

**Interfaces:**

- Consumes: the same complaint handoff and independently installed schema.
- Produces: the same limitations finding classes without importing the complaint
  skill or repository code.

- [ ] Copy the exact canonical schema and contract into Filing CI.
- [ ] Implement aligned native validation and preserve the Filing CI read-only
      result contract.
- [ ] Run the shared literal fixtures through both installed checkers and
      confirm GREEN and byte-equal schema alignment.
- [ ] Commit and push the Filing CI alignment.

### Task 5: Minimal corrected guidance

**Files:**

- Modify:
  `skills/drafting-section-1983-complaints/references/complaint-contract.md`
- Modify:
  `skills/drafting-section-1983-complaints/references/completion-audit.md`
- Modify: `skills/drafting-section-1983-complaints/SKILL.md`
- Modify: `evaluations/unknown-defendant-limitations/v1/scenarios.yaml`
- Modify: `evaluations/tests/test_unknown_defendant_limitations_gate.py`

**Interfaces:**

- Consumes: the approved trigger and record distinctions proved missing by the
  baseline pressure runs.
- Produces: guidance that requires the schema-backed handoff and preserves legal
  judgment for independent audit.

- [ ] Replace the ambiguous field and narrow trigger with the approved positive
      record recipe.
- [ ] Update completion and skill routing to require the handoff check and its
      fail-closed result.
- [ ] Update synthetic records to the corrected field model and exercise the
      real validator rather than adding new source-text assertions.
- [ ] Run focused evaluations and confirm GREEN.
- [ ] Commit and push the minimal guidance.

### Task 6: Pressure GREEN and completion

**Files:**

- Modify: `openspec/changes/issue-104-limitations-record-enforcement/tasks.md`
- Create: `openspec/changes/issue-104-limitations-record-enforcement/verify.md`
- Create:
  `openspec/changes/issue-104-limitations-record-enforcement/retrospective.md`

**Interfaces:**

- Consumes: the exact RED prompts, corrected installed skill, completed tests,
  and exact Git state.
- Produces: scored behavioral evidence, archived durable specs, and a freshly
  verified stacked PR.

- [ ] Run the exact pressure prompts against the corrected isolated skill and
      preserve outputs and scores.
- [ ] Mutate one trigger predicate and one unresolved-state branch; confirm the
      focused tests fail, restore, and confirm GREEN.
- [ ] Run focused neighboring tests, strict change validation, and
      `npm run validate`.
- [ ] Complete verification and retrospective artifacts, archive the change, run
      post-archive validation, commit, and push.
- [ ] Verify the exact remote head and GitHub checks, mark the PR ready, and
      leave PR #103, PR #104's implementation PR, Issue #102, and Issue #104
      open.
