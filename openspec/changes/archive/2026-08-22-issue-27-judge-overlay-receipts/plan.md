# Judge-Overlay Execution Receipts Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans
> to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for
> tracking.

**Goal:** Record every applicable judge-overlay composition run in one immutable
version-local receipt, including honest no-change degradation and fail-closed
input failures.

**Architecture:** Add one exact JSON packet schema and one standard-library
receipt writer to the generic drafting package. The writer validates and hashes
only designated artifacts, normalizes semantic failures, and exclusively writes
one Markdown report below the canonical audits directory. Existing judge guides
and overlays require the receipt after composition.

**Tech Stack:** Python standard library, Draft 2020-12 JSON Schema, `unittest`,
Markdown, OpenSpec.

**Spec:** `openspec/changes/issue-27-judge-overlay-receipts/design.md`

## Global Constraints

- Add no new tendency, authority conclusion, dependency, or filing edit.
- Preserve artifacts and prior reports byte-for-byte.
- Write only one new receipt under the audited version's `audits/` directory.
- Keep missing/stale/invalid/unavailable results fail-closed and non-passing.
- Use no root `docs/`, `.superpowers/`, private data, or code comments.
- Commit and run `git town sync` after every commit.

---

### Task 1: Schema, structure, and runtime RED

**Files:**

- Create: `evaluations/tests/test_judge_overlay_receipt_structure.py`
- Create: `evaluations/tests/test_judge_overlay_receipt_runtime.py`

**Interfaces:**

- Consumes: absent
  `skills/section-1983-drafting/references/judge-overlay-execution.schema.json`
  and `scripts/judge_overlay_receipt.py`.
- Produces: failing tests for `validate_packet(packet)` and
  `execute_receipt(packet, project_boundary, version_folder, now, run_id)` plus
  the public stdin CLI.

- [ ] Add structural tests for schema/script/routes and exact ownership.
- [ ] Add complete synthetic packet builders and literal receipt expectations.
- [ ] Add valid-change, valid-no-change, nonexecution, validation-status,
      anti-gaming, unsupported-change, artifact-fingerprint, confinement,
      collision, and immutability tests.
- [ ] Confirm RED is caused only by absent Issue 27 behavior; commit and sync.

### Task 2: Minimal GREEN

**Files:**

- Create:
  `skills/section-1983-drafting/references/judge-overlay-execution.schema.json`
- Create: `skills/section-1983-drafting/scripts/judge_overlay_receipt.py`
- Modify: `skills/section-1983-drafting/SKILL.md`
- Modify: `skills/drafting-for-judge-scholer/SKILL.md`
- Modify: `JUDGE_OVERLAYS.md`

**Interfaces:**

- Consumes: Task 1 public contract.
- Produces: exact packet validation, normalized result, immutable Markdown
  receipt, public CLI, and required composition guidance.

- [ ] Publish the exact Draft 2020-12 packet schema.
- [ ] Implement fail-fast value/link validation and result normalization.
- [ ] Implement canonical input resolution, fingerprinting, audits confinement,
      exclusive report creation, Markdown rendering, and bounded JSON CLI.
- [ ] Add only the required guide and skill routes.
- [ ] Run focused GREEN, commit, and sync.

### Task 3: Pressure, review, and archive

**Files:**

- Modify: tests and production only after an accepted finding becomes RED.
- Create: `openspec/changes/issue-27-judge-overlay-receipts/verify.md`
- Create: `openspec/changes/issue-27-judge-overlay-receipts/retrospective.md`

**Interfaces:**

- Consumes: complete Issue 27 story.
- Produces: reviewed, archived durable `judge-overlay-execution` and modified
  `judge-overlay-authoring` capabilities.

- [ ] Pressure malformed types, status combinations, check/card linkage, path
      races, collisions, report text, output bounds, and artifact bytes.
- [ ] Run focused, full, formatting, OpenSpec, corpus, governance, compilation,
      forbidden-folder, private-marker, code-comment, and diff checks.
- [ ] Complete verification and retrospective records, archive, replace any
      generated Purpose placeholder, validate both durable specs, commit, sync,
      and prove clean origin parity with Issue 27 open and no PR.
