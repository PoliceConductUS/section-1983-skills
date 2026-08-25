# Tasks

## 1. Design and stack

- [x] 1.1 Define authority separation, package compatibility, process isolation,
      output/temp confinement, and adversarial-review migration.
- [x] 1.2 Push the OpenSpec design and open a draft PR stacked on Issue #33.

## 2. Static role and launch-request validation

- [ ] 2.1 RED-test exact operation, profile, target, context, task, internet,
      freshness, fingerprint, and public-reference contracts.
- [ ] 2.2 Implement and GREEN deterministic pre-dispatch binding without process
      or output-root authority in domain helpers.

## 3. Fresh isolated process boundary

- [ ] 3.1 RED-test fresh-process attestation, empty run-scoped temp cwd,
      scrubbed environment/session state, no commands from untrusted data,
      timeout, exit, UTF-8, JSON, and stream bounds.
- [ ] 3.2 Implement and GREEN the trusted adapter protocol and bounded launcher.

## 4. Advisory output and immutability

- [ ] 4.1 RED-test role-specific output validation, output confinement, stable
      failures, and unchanged profile, target, context, and public references.
- [ ] 4.2 Implement and GREEN proposed-artifact return through the shared output
      boundary with all transient work under `<output-folder>/temp`.

## 5. Adversarial-review migration

- [ ] 5.1 RED-test the existing five categories, independence, read-only target,
      plaintiff decisions, and provider failures through the shared launcher.
- [ ] 5.2 Migrate the public adversarial reviewer without weakening its current
      domain validator or adding an arbitrary command surface.

## 6. Verification and archive

- [ ] 6.1 Run focused tests, install-local skill validation, full repository
      validation, and fresh whole-story review.
- [ ] 6.2 Record verification and retrospective evidence and archive OpenSpec.
- [ ] 6.3 Push the verified archive and mark the PR ready while leaving the PR
      and issue open.
