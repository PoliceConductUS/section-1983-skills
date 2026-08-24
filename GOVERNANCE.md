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

Verification, factual and authority source, permission, filing-readiness,
judgment-routing, rules-provenance, tool-ownership, folder scope, recursive
input non-mutation, output confinement, and declared internet policy are
protected gates. Any change that weakens, bypasses, removes, or changes a
protected gate requires explicit human review that identifies the affected gate
and rationale.

A contribution that broadens input mutation, output placement, undeclared path
access, or internet authority must identify the affected protected gate and
rationale and request explicit human review before acceptance. The canonical
folder-execution protocol is
[FOLDER_SCOPED_EXECUTION.md](FOLDER_SCOPED_EXECUTION.md).

Every public skill links to an install-local folder contract that fixes its
ordered input roles, target policy, internet policy, and append-immutable output
mode. Repository validation compares each contract with the approved skill
matrix. Composing skills does not combine their contracts or enlarge either
skill's filesystem or network authority.

This repository retains public skill instructions and repository-specific
validation or evaluation support. General-purpose executable tooling for rule
retrieval, citation verification, evidence processing, filing inspection, or
other reusable work belongs in its owning repository; this repository keeps only
a thin skill wrapper when one is needed. A thin skill wrapper must identify its
owning repository.
