---
name: validating-court-facing-assertions
description: >-
  Use when a generated complaint, amendment, motion, response, objection, brief,
  declaration, or other court-facing document needs an independent post-draft
  assertion and omission review against declared original sources before a
  correction loop or filing-readiness assessment.
---

# Validating Court-Facing Assertions

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `filing` contains the one generated court-facing document selected for
  validation.
- `record` contains the declared original factual sources and source
  documentation permitted for the review.
- `authorities` contains the declared authority sources and completed authority-
  audit material permitted for the review.
- `strategy` contains the current case controls that state approved claims,
  principal corrections, permitted source boundaries, and authorized treatment
  of unresolved issues.
- `prior-reports` optionally contains exact prior validation findings selected
  for a freshness and continued-applicability review.

There is one required target in `filing`. Internet is `disabled`. The validation
stage returns one proposed report and structured findings; only the trusted host
derives the canonical output-relative path and publishes it append-immutable.
Keep all extraction, staging, scratch, and temporary bytes beneath
`<output-folder>/temp/`.

Never search an ambient workspace, infer an undeclared source, modify an input,
or write directly to the output folder. This skill does not depend on CaseGraph
or require a graph, package, manifest, repository, or persistence layer. If a
declared source or control supplies a documentation route, preserve it as
optional provenance; its presence or absence does not prove substantive support.

## Required contract

Read
[the assertion-validation contract](references/assertion-validation-contract.md)
completely before reviewing any target. If the reference cannot be read, report
**assertion validation contract unavailable** and stop. Do not reconstruct or
replace it from another skill, prior report, case control, or conversation.

## Role and authority boundary

This skill owns the read-only semantic validation report. It does not draft or
revise the filing, decide litigation strategy, perform an adversarial attack,
run a deterministic checker, or publish output.

The complete workflow is:

1. an authorized drafting skill produces a complete candidate;
2. this skill identifies and validates every assertion and applicable
   requirement;
3. this skill returns its report without changing the candidate;
4. a separately authorized drafting or revision stage applies selected,
   source-supported corrections and creates a new version when versioning
   applies;
5. this skill revalidates every affected assertion and dependency and verifies
   the continued applicability of any reused finding; and
6. the workflow reconciles the complete final candidate and performs the final
   whole-document and rendered-file review.

Changed target text never authorizes this review stage to edit it back. A
general request to make a filing ready does not authorize a particular factual,
legal, strategic, or remedial choice.

## Perform the review

1. Bind the report to the exact target, declared source bytes, controls, prior
   findings, and methods actually used.
2. Inventory all text, including unchanged and inherited text, and split every
   compound sentence into separately assessable propositions.
3. Trace each factual proposition to an original source passage or recording
   observation. Test what that source actually establishes, including contrary
   context and limits.
4. Route every material legal proposition through `audit-authorities`. Consume
   its authority-specific findings; do not substitute a citation, route, or hash
   check for the authority audit.
5. Compare the complete candidate against current declared controls and every
   applicable drafting contract. Map each approved claim, material source fact,
   principal correction, and other applicable requirement to the target or
   report the omission.
6. Classify every assertion and coverage item using the shared contract. Do not
   collapse missing documentation, insufficient substantive support, and an
   authorized factual unknown.
7. Build the report and Mermaid summary from the assertion and coverage records'
   actual statuses and counts.
8. Apply the stopping criteria. Return precise unresolved issues and tradeoffs
   when evidence or a litigation-principal decision is required.

## Specialist coordination

- `section-1983-drafting` orchestrates the complete correction loop for
  generated Section 1983 filings.
- `drafting-section-1983-complaints` supplies the complete complaint candidate
  and its canonical requirements.
- `drafting-section-1983-rule-59e` supplies the complete Rule 59(e) candidate
  and its packet-specific requirements.
- `drafting-section-1983-monell-claims` supplies integrated Monell text only
  through the canonical complaint owner.
- `audit-authorities` supplies authority-specific findings.
- `adversarial-filing-review` remains a downstream independent defense attack
  after source validation.
- `filing-ci` supplies deterministic integrity and freshness signals only.

A deterministic check does not decide evidentiary support or legal sufficiency.
Passing deterministic output cannot close an assertion, authority, omission, or
litigation-decision finding.

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
