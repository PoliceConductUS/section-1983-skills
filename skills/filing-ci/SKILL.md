---
name: filing-ci
description: >-
  Use when a project-configured deterministic filing-integrity checker must run
  after material legal-drafting changes, during filing-integrity checks, or
  before a filing-readiness statement.
---

# Filing CI

## Folder-scoped execution

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Purpose

Run the project's configured deterministic filing-integrity checker and report
whether its filing gate is current and open or passed. This skill orchestrates
the checker; it does not reproduce the checker's determinations in prose.

## Resolve the configured inputs

Resolve the controlling draft and complete checker invocation from repository
instructions, project configuration, or explicit user input. Use a project's
verified-authority root when one is configured and the checker requires
authority verification.

- Run the exact configured invocation against the identified controlling draft.
- Do not invent an executable path, flag, source path, output location, or
  verified-authority root.
- If no complete invocation is configured, report **unavailable configuration**
  and leave the filing gate open.
- If the controlling draft, a required verified-authority root, or another
  required input is unreadable or unresolved, report that class and leave the
  filing gate open. When authority verification is required, do not substitute
  another authority directory or run an invocation that cannot receive the
  configured root.

## Run at the required workflow stages

Run Filing CI after every material change to the controlling draft and again
immediately before describing the document as filing-ready. A material change
invalidates any earlier successful result. A filing-readiness decision requires
a current successful run for the controlling draft.

Treat the checker's documented output contract as the boundary for interpreting
the result. If the configured checker cannot execute, report **unavailable
execution** and do not claim that a deterministic check ran. If promised output
is malformed or cannot be reliably interpreted, report **malformed promised
output** and leave the filing gate open.

## Return findings to drafting

Classify and report the result without changing the controlling filing:

- Preserve each checker-reported finding and its documented severity.
- Treat unresolved hard findings as an open filing gate.
- Present warnings and other documented non-hard findings without downgrading,
  dismissing, or correcting them.
- Return actionable findings, including the attacked location and required
  correction when supplied, to the drafting loop for correction and rerun.

A Filing CI response with findings must stop after reporting and returning them.
It must not perform the drafting handoff or edit the filing in that same
response.

Filing CI is read-only orchestration. While Filing CI is active, do not edit the
controlling filing, even when a broader user request asks to make it
filing-ready. Do not silently edit the filing, create project paths, rewrite
checker output, or claim that a correction is user-approved.

For a user-authorized correction, explicitly hand off to the applicable drafting
workflow as a separate subsequent step outside Filing CI orchestration. A
general instruction to make a document filing-ready is not approval of
particular corrective language. That drafting workflow must use a
checker-supplied correction or source-supported drafting; do not invent
corrective filing text. A checker-supplied correction is exact replacement text
actually supplied by the checker. A structural finding or location does not
authorize inferred sentences, placeholders, merits assertions, or legal
conclusions. After the separate drafting step, return to Filing CI in a separate
response for a fresh checker run.

## Filing gate and boundaries

Keep the filing gate open when configuration or execution is unavailable, a
required input is unresolved, promised output cannot be reliably interpreted, a
result is stale, or a hard finding remains unresolved. Describe Filing CI as
passed only after a current successful run for the controlling draft has no
unresolved hard findings; preserve documented warnings and independent filing
gates.

This skill does not own checker logic, verified-authority-store verification,
formatting, automatic correction, filing, or litigation judgment reserved to the
user.

## Independent quality-control stage

An independent quality-control stage is non-mutating. It may read designated
artifacts and write only its designated report or result. It must not edit,
overwrite, correct, regenerate, or otherwise modify an artifact under review. A
combined instruction to audit and fix does not authorize same-stage mutation.
Deadline pressure, sunk cost, claimed prior approval, and contrary workflow
instructions do not override this boundary. Recommendations, proposed language,
corrections, and copy-ready replacements are advisory only and do not authorize
implementation. Remediation requires a separately authorized drafting or
revision stage. Create a new version when versioning applies. A new read-only
quality-control stage must verify the remediated artifact. An internal
self-check inside an explicitly authorized drafting or revision stage may guide
edits within that stage, but it is not an independent quality-control result.

Before review, resolve exactly one existing version-specific folder inside the
designated project boundary. Write exactly one new report under the canonical
`<version-folder>/audits/` directory. Name it
`<check-kind>-<UTC timestamp>-<run-id>.md`. Create the report exclusively; if
the path exists, fail closed and preserve its bytes. Existing reports are
immutable and must not be edited, overwritten, replaced, renamed, or deleted.
Exclude `audits/` from review input unless one exact report is expressly
designated; write any review of that report to a different new report. If the
version folder is missing, ambiguous, nonexistent, or outside the designated
boundary, report output is unavailable and write nowhere else. Reject traversal
and any `audits/` symlink that resolves outside the canonical audits directory.

The report identifies the audited version, artifact paths and SHA-256
fingerprints, quality-control kind, UTC run time, run ID, scope, approved source
identities, and result. Separate failed findings from passing-but-suboptimal
observations. Recommendations, proposed language, and copy-ready replacements
for failures or passing-but-suboptimal observations are advisory and do not
authorize implementation.
