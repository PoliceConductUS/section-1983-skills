# Trusted Adversarial Review Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `subagent-driven-development`
> when explicitly authorized or `executing-plans` for inline execution. Follow
> `test-driven-development`, `writing-skills`, and the OpenSpec/Superpowers
> bridge. Commit and run `git town sync` after every commit.

**Goal:** Make the existing clean-room adversarial review executable through a
trusted stateless runtime while preserving immutable reviewed artifacts and
version-specific audit reports.

**Architecture:** Keep exact packet validation as the single reviewer-input
gate. Add a standard-library Responses transport that constructs a no-tools,
no-storage, no-session request, validates a strict categorized response, and
passes it to a separate exclusive report writer. The arbitrary command seam
remains available only as an untrusted compatibility boundary and cannot be made
independent by a Boolean assertion.

**Tech Stack:** Python 3 standard library, `unittest`, OpenSpec
superpowers-bridge, existing synthetic evaluation harness.

**Spec:**
`openspec/changes/issue-28-adversarial-review-runtime/specs/adversarial-filing-review/spec.md`

## Global constraints

- The reviewer receives only the validated embedded packet and bounded public
  instructions.
- No tools, storage, conversation, previous-response identity, filesystem,
  repository, browser, or shell capability reaches the reviewer.
- The reviewed artifact and every existing audit remain byte-identical.
- Only one new report under the resolved version's `audits/` directory may be
  written.
- Python standard library only; no dependency or workflow change.
- No root `docs/` or `.superpowers/` directory and no case-specific fixture.
- No PR or issue closure.

## Task 1: Trusted provider request RED

**Files:**

- Modify: `evaluations/tests/test_adversarial_review_launcher.py`
- Create only if separation improves the public seam:
  `evaluations/tests/test_adversarial_review_runtime.py`

**Interfaces:**

- Consumes: existing `valid_packet()` fixture and public launcher module.
- Produces: failing expectations for
  `run_trusted_review(packet, model, api_key, timeout_seconds=60, transport=None)`
  and the CLI trusted-runtime mode.

- [ ] Add a literal spy transport test that names the break: any request with a
      nonempty tool set, tool selection other than `none`, `store` other than
      false, conversation/session continuation field, content outside the
      validated packet, or missing strict response schema must fail.
- [ ] Add a preflight sentinel proving invalid packets and absent explicit model
      or credentials prevent transport execution.
- [ ] Add direct and CLI tests for timeout, HTTP failure, oversized/invalid
      UTF-8 bodies, malformed JSON, missing output text, and response-schema
      failure.
- [ ] Run the focused module and record RED caused only by the missing trusted
      entry point and behavior.
- [ ] Commit with `test: expose unavailable trusted review runtime`, then run
      `git town sync`.

## Task 2: Categorized response RED

**Files:**

- Modify: the focused runtime test module from Task 1.
- Add generic synthetic fixture files only if the existing harness needs a new
  behavior pressure case.

**Interfaces:**

- Consumes: provider output-text object.
- Produces: failing expectations for
  `validate_review_response(response, approved_source_ids)` and
  `render_review_markdown(response, receipt)`.

- [ ] Define one hand-written valid response containing all five exact category
      keys, one source-backed finding, one complete `Replace`/`With` correction,
      and one unselected plaintiff decision.
- [ ] Add table-driven mutations for a missing category, extra category, empty
      finding field, duplicate finding ID, unknown source ID, partial
      correction, selected plaintiff option, category duplication, and invalid
      string bytes.
- [ ] Assert empty arrays render `None found` and unavailable execution renders
      no successful category decisions.
- [ ] Run the focused tests and record genuine RED.
- [ ] Commit with `test: define trusted review response protocol`, then sync.

## Task 3: Immutable report RED

**Files:**

- Modify: the focused runtime test module.

**Interfaces:**

- Consumes: validated packet, categorized response, project boundary, version
  folder, audited artifact, explicit model, injected UTC time/run ID.
- Produces: failing expectations for `write_review_report(...)` and the
  end-to-end trusted CLI.

- [ ] Create temporary synthetic project/version/artifact trees and assert the
      artifact hash is checked before transport.
- [ ] Assert a successful run changes exactly one path beneath `audits/`, uses
      the canonical filename, records the bounded receipt, and preserves all
      artifact/existing-report hashes.
- [ ] Add traversal, outside-boundary, ambiguous/missing version, escaping
      audits-symlink, existing-name collision, and artifact-mismatch cases.
- [ ] Add unavailable-provider end-to-end behavior: nonzero exit, exactly one
      honest unavailable report when output is resolvable, no `PASS` label, no
      synthesized categories, and no credential value.
- [ ] Run focused RED, formatting, compile, and diff checks; review the complete
      RED suite and correct any false-green or implementation-coupled
      assertions.
- [ ] Commit with `test: require immutable adversarial review reports`, then
      sync.

## Task 4: Minimal trusted runtime GREEN

**Files:**

- Modify: `skills/adversarial-filing-review/scripts/launch_review.py`
- Create if responsibility separation is needed:
  `skills/adversarial-filing-review/scripts/openai_runtime.py`
- Create if responsibility separation is needed:
  `skills/adversarial-filing-review/scripts/review_report.py`

**Interfaces:**

- Produces the public functions named in Tasks 1–3 and a CLI that reads the
  packet from UTF-8 JSON stdin.

- [ ] Implement strict input validation before any transport or filesystem
      write.
- [ ] Construct the minimal official Responses request with explicit model,
      bounded instructions/input, strict JSON schema, empty tools, tool choice
      `none`, storage false, and no conversation/previous-response fields.
- [ ] Implement bounded HTTPS transport, strict UTF-8/JSON extraction, and
      stable provider failure classes without logging the API key.
- [ ] Implement exact categorized response validation and Markdown rendering.
- [ ] Implement canonical path resolution, exact artifact verification,
      exclusive report creation, and machine-readable CLI results.
- [ ] Make a bare caller Boolean insufficient to execute a trusted custom
      command.
- [ ] Run all focused tests until GREEN, then the full evaluation suite.
- [ ] Commit with `feat: run trusted isolated adversarial reviews`, then sync.

## Task 5: Public skill behavior GREEN

**Files:**

- Modify: `skills/adversarial-filing-review/SKILL.md`
- Modify: `README.md`
- Modify: `skills/adversarial-filing-review/agents/openai.yaml` only if
  discovery must mention the executable path.
- Modify or add synthetic fixtures only when the recorded RED pressure requires
  it.

**Interfaces:**

- Consumes: the trusted CLI from Task 4.
- Produces: install-local instructions that run the trusted mode without a
  caller assertion and preserve the immutable QC boundary.

- [ ] Run fresh no-guidance/control pressure scenarios against the current skill
      and retain exact failures.
- [ ] Update only the instructions needed to select the trusted runtime, supply
      an explicit model/packet/output boundary, interpret unavailable results,
      and keep custom commands untrusted without a proved adapter.
- [ ] Run the same pressure scenarios with the revised skill; verify a valid
      runtime produces a five-category report and failure remains fail closed.
- [ ] Run quick skill validation, discovery, focused tests, corpus, governance,
      `npm run validate`, forbidden-folder search, comment search, and diff
      checks.
- [ ] Commit with `docs: route adversarial review through trusted runtime`, then
      sync.

## Task 6: Whole-story review and archive

**Files:**

- Modify: implementation/tests only for accepted review corrections.
- Create: `openspec/changes/issue-28-adversarial-review-runtime/verify.md`
- Create:
  `openspec/changes/issue-28-adversarial-review-runtime/retrospective.md`
- Archive into:
  `openspec/changes/archive/2026-08-22-issue-28-adversarial-review-runtime/`
- Modify durable spec: `openspec/specs/adversarial-filing-review/spec.md`

**Interfaces:**

- Produces: an independently complete Issue 28 branch ready to parent Issue 29.

- [ ] Review request construction, response parsing, path confinement, immutable
      output, credential/error handling, and tests for false greens.
- [ ] Correct accepted Critical or Important findings through new failing tests,
      rerun review once, and record final evidence.
- [ ] Complete tasks, verification, and retrospective without placeholders.
- [ ] Archive with the repository-local OpenSpec CLI; replace any generated
      durable-spec placeholder and run strict/all validation.
- [ ] Run final full validation and verify local/origin parity, clean status,
      Issue 28 remains open, and no PR exists.
- [ ] Commit with `docs: archive trusted adversarial review runtime`, then sync.
