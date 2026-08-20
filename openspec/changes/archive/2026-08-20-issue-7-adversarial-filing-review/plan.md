# Implementation Plan: Independent Adversarial Filing Review

## Task 1: Lock the Public Contract RED

Add a focused standard-library test that resolves the repository from its own
path and requires a valid public skill entrypoint, OpenAI discovery metadata,
README routing, the clean-room exclusions and fail-closed result, the five
category headings, exact correction fields, the plaintiff decision gate, and the
seven checklist families. Run the focused test before creating the skill and
record the genuine missing-file failures.

## Task 2: Lock the Launcher Contract RED

Add standard-library tests that spy on the complete payload sent to a fake
reviewer. Require only the canonical draft content/version/fingerprint,
supported document family, embedded source IDs/roles/content/fingerprints,
public skill/checklist content, and an empty capability set. Reject extra
fields, path-only sources, fingerprint mismatches, and forbidden capabilities.
Prove one fresh process, empty working directory, scrubbed context environment,
stable unavailable execution, bounded output, and no command on invalid input.

## Task 3: Add Synthetic Behavioral Regressions

Add three synthetic fixture directories to the canonical evaluation corpus:
history/control leakage, incomplete correction language, and reviewer-selected
narrowing or omission. Each fixture contains a bounded source manifest, passing
report, behavior-specific permanent regression, deterministic contract, and
stable rubric. Adversarially prove an unrelated generic failure cannot satisfy
each expected-finding subset.

## Task 4: Demonstrate the Missing Skill RED

Use a fresh subagent with only a synthetic canonical draft, approved source
packet, and request to load `adversarial-filing-review`. Record the unavailable-
skill response under `/private/tmp/adversarial-review-issue-7`. Do not add the
skill before the RED structural and public-seam evidence exists.

## Task 5: Implement the Minimal Skill

Add `skills/adversarial-filing-review/SKILL.md`, one self-contained document
attack checklist reference, `agents/openai.yaml`, and the standard-library
bounded-packet launcher. Update README discovery and composition text. Do not
add an external dependency, project path, comment, automatic edit, authority-
verification behavior, RRD behavior, or Filing CI substitute.

## Task 6: Prove Behavioral GREEN

Run fresh reviewers with only bounded synthetic packets for: unavailable fresh
context, all five category classifications, complete `Replace:`/`With:`
correction, and retain/narrow/omit choice. Compare the canonical draft hash
before and after each run. Require approved source IDs only. Dispatch a task
reviewer, add a RED test for every accepted behavioral defect, make the smallest
skill correction, and rerun the affected scenario in another fresh context.

## Task 7: Verify and Archive

Run `npm run validate`, all runtime skill validators, strict OpenSpec JSON
validation, `git diff --check 52a0a4d..HEAD`, and forbidden-folder checks.
Produce bridge verification and retrospective artifacts, obtain a fresh whole-
change review, archive on the Issue #7 branch, replace any generated durable-
purpose placeholder, check the archive task, rerun validation, commit, and run
`git town sync` after every commit.
