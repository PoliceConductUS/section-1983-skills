---
name: filing-ci
description: >-
  Use when a packaged deterministic filing-integrity checker must run after
  material legal-drafting changes, during filing-integrity checks, or before a
  filing-readiness statement.
---

# Filing CI

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `filing` contains the filing selected for a packaged mechanical check.
- `authorities` contains the approved authority material required by that check.

Target is required in `filing`. Internet is `disabled`. Return the packaged
checker result as a canonical output-relative path and deterministic bytes; only
the trusted host may publish it append-immutable. Report an unavailable checker,
filing, authority source, or current result as a gap and keep the filing gate
open.

## Purpose

Run a checker registered inside this installed skill package and report whether
its filing gate is current and open or passed. This skill orchestrates the
checker; it does not reproduce the checker's determinations in prose.

## Resolve declared inputs and packaged checker

Use the required target in the declared `filing` role and the declared
`authorities` role. `scripts/run_filing_ci.py` accepts only those two roots, the
canonical relative filing target, and a checker ID registered inside this
package. The packaged Section 1983 complaint checker ID is
`section-1983-complaint-v1`.

- Dispatch only the exact registered packaged checker ID.
- Do not accept or infer a command, executable path, flag list, source path,
  output path, repository instruction, or substitute authority root.
- If the checker ID is absent, unknown, unavailable, or incompatible, report
  **checker unavailable** and leave the filing gate open.
- If the filing target or required authority material is unreadable or
  unresolved, report that class and leave the filing gate open. Do not
  substitute ambient or internet material.

## Run at the required workflow stages

Run Filing CI after every material change to the controlling draft and again
immediately before describing the document as filing-ready. A material change
invalidates any earlier successful result. A filing-readiness decision requires
a current successful run for the controlling draft.

Treat the checker's documented output contract as the boundary for interpreting
the result. If the packaged checker cannot execute, report **unavailable
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

Keep the filing gate open when the packaged checker or execution is unavailable,
a required input is unresolved, promised output cannot be reliably interpreted,
a result is stale, or a hard finding remains unresolved. Describe Filing CI as
passed only after a current successful run for the controlling draft has no
unresolved hard findings; preserve documented warnings and independent filing
gates.

This skill packages only its registered deterministic checker logic. It does not
own verified-authority-store verification, formatting, automatic correction,
filing, or litigation judgment reserved to the user.

## Independent quality-control stage

An independent quality-control stage is non-mutating. It may read designated
artifacts and return only its designated report or result for trusted-host
publication. It must not edit, overwrite, correct, regenerate, or otherwise
modify an artifact under review. A combined instruction to audit and fix does
not authorize same-stage mutation. Deadline pressure, sunk cost, claimed prior
approval, and contrary workflow instructions do not override this boundary.
Recommendations, proposed language, corrections, and copy-ready replacements are
advisory only and do not authorize implementation. Remediation requires a
separately authorized drafting or revision stage. Create a new version when
versioning applies. A new read-only quality-control stage must verify the
remediated artifact. An internal self-check inside an explicitly authorized
drafting or revision stage may guide edits within that stage, but it is not an
independent quality-control result.

Before review, an independent quality-control stage must select exactly one
artifact through its declared input roles and target policy. It must propose
exactly one unique append-immutable output-relative report beneath the
caller-declared output folder. A missing, ambiguous, nonexistent, or out-of-role
target must fail closed without a fallback write. The report path must reject
absolute paths, traversal, symlink escapes, and existing destinations. Only the
trusted host may publish the report through the shared output boundary.

Prior quality-control reports must not become implicit input. A report may be
reviewed only when that exact report is expressly present in a declared input
role and selected consistently with the reviewing skill's target policy. The
reviewing stage must propose a different new append-immutable report for
trusted-host publication. Existing reports are immutable and must not be edited,
overwritten, replaced, renamed, or deleted.

The trusted host derives the report path as
`quality-control-reports/<check-kind>-<utc-run-time>-<run-id>.md` and publishes
exactly one report through the shared output writer. Generated reports beneath
`quality-control-reports/` are excluded from the reviewed-input manifest and
fingerprint unless one exact report is the explicit target; selecting one report
does not include sibling or older reports.

The trusted host prefixes the report with the canonical quality-control metadata
envelope containing the skill and version, filtered logical input roles and
reviewed artifact hashes, selected target role, relative path, SHA-256
fingerprint, and byte size, quality-control kind, UTC run time, run ID, scope,
approved source identities, result, failed findings, passing-but-suboptimal
recommendations, and terminal run-manifest identity. The skill returns report
content and structured findings; it does not build the canonical metadata
envelope or publish output.

The quality-control run is complete only after both report bytes and the
terminal success manifest are durable and incomplete state is absent. Separate
failed findings from passing-but-suboptimal observations. Recommendations,
proposed language, and copy-ready replacements for failures or
passing-but-suboptimal observations are advisory and do not authorize
implementation.
