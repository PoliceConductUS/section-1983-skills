# Filing CI Review-Correction Plan

**Goal:** Close the final-review evidence and durable-specification gaps without
expanding the public skill.

**Architecture:** Keep the executable skill unchanged if all missing behavioral
scenarios pass. Express the two demonstrated edit-loop safeguards as a modified
durable OpenSpec requirement. Keep synthetic fixtures and reports under
`/private/tmp`.

## Task 1: Complete Public-Seam Evidence

1. Create synthetic projects for missing configuration, unavailable required
   verified-authority root, non-hard warning, and current success.
2. Dispatch one independent fresh-context agent per project with only the public
   skill, project configuration, and pressured user request.
3. Record whether the agent ran or refused the configured command, preserved
   finding classes, avoided draft edits and invented configuration, and made the
   correct gate decision.
4. Change the public skill only if an observable behavior fails, then rerun only
   the affected case.

## Task 2: Correct the Durable Contract

1. Modify the read-only requirement to require a finding-bearing response to
   stop before drafting.
2. Require any approved correction to occur in a separate later drafting
   workflow and reject general make-ready language as specific-text approval.
3. Define checker-supplied replacement text as exact text and prohibit inferred
   substantive language from structural findings.
4. Require a fresh later Filing CI run after a material drafting correction.
5. Replace the generated durable purpose placeholder after archive.

## Task 3: Verify and Finish

1. Validate OpenSpec while the corrective change is active.
2. Run `npm run validate`, runtime validation for every skill,
   `git diff --check`, and the forbidden-folder checks.
3. Produce `verify.md` and `retrospective.md` with the four new run reports as
   evidence.
4. Archive on `codex/issue-1-filing-ci`, replace the durable purpose
   placeholder, rerun validation, commit, and run `git town sync`.
5. Request a fresh read-only review against parent commit `5f271d2`.
