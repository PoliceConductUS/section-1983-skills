# Governance

The user reserves litigation strategy, legal positions, concessions, requested
relief, and filing. When supported choices have different consequences, present
each supported choice and consequence, identify the user decision required, and
select none. Apply an express user decision without enlarging it or silently
deciding another material choice.

Current jurisdiction-specific propositions belong only in a verified reference
that identifies the jurisdiction, authoritative source provenance, and checked
date. Public skills route to that reference without restating the proposition.
If the source is unavailable or its currency cannot be established, report the
source gap rather than supplying a proposition from memory or a generic
substitute.

## Independent quality control

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

Verification, factual and authority source, permission, filing-readiness,
judgment-routing, rules-provenance, and tool-ownership are protected gates. Any
change that weakens, bypasses, removes, or changes a protected gate requires
explicit human review that identifies the affected gate and rationale.

This repository retains public skill instructions and repository-specific
validation or evaluation support. General-purpose executable tooling for rule
retrieval, citation verification, evidence processing, filing inspection, or
other reusable work belongs in its owning repository; this repository keeps only
a thin skill wrapper when one is needed. A thin skill wrapper must identify its
owning repository.
