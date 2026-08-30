---
name: filing-ci
description: >-
  Use when an installed deterministic filing-integrity checker must run after
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

- `filing-source` contains the filing selected for a mechanical check.
- `filing-index` contains the selected filing's domain YAML source record.
- `record-reference` contains selected record bytes and `SOURCE.yaml` records.
- `exhibit` contains selected exhibit bytes and `SOURCE.yaml` records.
- `docket-to-appendix` contains the selected mapping bytes and domain YAML.
- `verified-authority` contains selected authority bytes and `SOURCE.yaml`
  records.

Target is required in `filing-source`. Internet is `disabled`. Return checker
content and structured findings; only the trusted host derives the canonical
output-relative path and publishes the report append-immutable. Report an
unavailable checker, filing, authority source, or current result as a gap and
keep the filing gate open.

## Purpose

Run a checker registered inside this installed skill directory and report
whether its filing gate is current and open or passed. This skill orchestrates
the checker; it does not reproduce the checker's determinations in prose.

## Resolve declared inputs and installed checker

Use the required target in the declared `filing-source` role and only the five
other declared roles listed above. The trusted host validates selected domain
YAML, relative paths, hashes, dates, and ordinary source bytes before invoking
`scripts/run_filing_ci.py`. The installed Section 1983 complaint checker ID is
`section-1983-complaint-v2`.

- Dispatch only the exact registered installed checker ID.
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
the result. If the installed checker cannot execute, report **unavailable
execution** and do not claim that a deterministic check ran. If promised output
is malformed or cannot be reliably interpreted, report **malformed promised
output** and leave the filing gate open.

## Complaint contract version 2

For a Section 1983 complaint handoff, also run the canonical install-local
`drafting-section-1983-complaints/scripts/validate_complaint_handoff.py` against
contract version 2. Version 1 is unsupported. Preserve the validator's
`structural_validation`, `casegraph_assessment`, and `filing_gate` result layers
separately. Do not collapse them into an unqualified overall pass.

Drafting mode may continue when structural validation passes and the graph
status is explicitly `not_run_missing`, `not_run_invalid`,
`not_run_incompatible`, or `not_run_stale`. It must report that legal assessment
did not complete. A `partial` assessment reports the components assessed and
every missing connection; it is not a completed merits result.

Filing mode requires a current `completed` assessment covering every included
claim unit and the current document fingerprint. Each authority proposition used
by the assessment must resolve to the verified opinion artifact and hash, cited
pinpoint, and exact matching passage in a provenance-linked text representation.
A `partial`, `not_run_missing`, `not_run_invalid`, `not_run_incompatible`, or
`not_run_stale` status leaves the filing gate open. Missing, ambiguous, or
nonmatching authority text also leaves the filing gate open for every dependent
component.

The canonical validator verifies the receipt, referenced-file hashes, and exact
text match. It does not independently decide fact truth, authority quality,
legal sufficiency, or litigation strategy. Preserve the reasoned assessment's
component findings without recasting them as deterministic checker conclusions.

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

Keep the filing gate open when the installed checker or execution is
unavailable, a required input is unresolved, promised output cannot be reliably
interpreted, a result is stale, or a hard finding remains unresolved. Describe
Filing CI as passed only after a current successful run for the controlling
draft has no unresolved hard findings; preserve documented warnings and
independent filing gates.

This skill owns only its registered deterministic checker logic. It does not own
verified-authority-store verification, formatting, automatic correction, filing,
or litigation judgment reserved to the user.

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
trusted host may publish the report through the shared output boundary. The
trusted host accepts quality-control publication only from an invocation bound
to the installed skill's target policy and approved target roles; it rejects an
unbound invocation or a target outside those approved roles.

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
does not include sibling or older reports. The canonical quality-control
metadata envelope identifies a generated report even when the report directory
itself is a declared input root. A quality-control run ID must be a canonical
lowercase UUIDv4; weak, malformed, or reused identities fail closed before
publication.

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
