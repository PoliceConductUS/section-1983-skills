---
name: auditing-section-1983-privilege-logs
description: >-
  Use when a Section 1983 plaintiff needs to determine approved privilege-log
  requirements or audit a supplied privilege log.
---

# Auditing Section 1983 Privilege Logs

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `privilege-log` contains the supplied privilege-log entries.
- `served-discovery` contains the requests to which withholding relates.
- `authorities` contains the approved privilege rules, orders, and agreements.

Target is optional in `privilege-log`; without one, audit the supplied log set.
Internet is `disabled`. Return the entry-by-entry audit as a canonical
output-relative path and deterministic bytes; only the trusted host may publish
it append-immutable. Report missing log fields, request links, or authority as a
gap without inventing metadata or deciding privilege.

Determine source-bounded privilege-log requirements and audit supplied entries
without inventing metadata, exposing substance, or adjudicating privilege.

## Required inputs

Use approved rules, orders, agreements, timing provisions, served-request
relationships, supplied log entries, and approved source content. If no approved
source defines a disputed requirement, report a scoped authority gap.

## Portable coordination contract

Use approved source IDs for every supplied premise. Preserve each stable
`target_id` or served request ID. One map row represents one legal tuple:
`claim`, `defendant`, and `element`; it also records `factual_gap`,
`likely_custodian`, and `expected_native_source`. Values must be meaningful and
nonblank. Report null, empty, placeholder, collective, or unsupported values.

Apply bounded proportionality through a bounded time or date scope, bounded
actor or entity scope, bounded system or category scope, importance, supplied
burden information, and supported narrower alternatives. A `likely_custodian`
remains an expectation and is not established. An `expected_native_source`
remains an expectation and is not established.

Determine whether a source exists before stating its content. Unverified
existence or content stays unknown and receives an existence, identification, or
conditional request.

A material choice uses `PLAINTIFF DECISION REQUIRED`, states choices and
consequences, preserves the supplied material and position, and selects no
strategy.

## Requirements and audit

When no log has arrived, return a requirements checklist from supplied approved
sources without inventing entries, withheld material, or a deficiency.

The requirements matrix MUST include every field required by approved sources:
identifier, date, author, recipients, document type, nonprivileged subject,
asserted privilege or protection, stated basis, custodian, family or attachment
relationship, timing, and request relationship.

When a log exists, audit each log entry against the approved matrix. Identify
each missing field or missing metadata and preserve its stable request or target
relationship. Use only supplied entry facts. The skill must not substitute a
generic court rule for a missing source.

## Output and boundaries

Return Privilege-Log Requirements, an Entry Audit when a log exists, scoped
gaps, and Plaintiff Decisions. The skill must not invent a fact, field,
metadata, or entry; reveal privileged substance; or adjudicate privilege. It
must not declare waiver. It must not select clawback treatment, accept a
categorical log, choose a waiver theory, or decide whether to confer or move.

## Output provenance

Every returned artifact must identify the actual approved source identity and
checked date used.

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

The report identifies the logical input roles and hashes, selected target path
and SHA-256 fingerprint, quality-control kind, UTC run time, run ID, scope,
approved source identities, and result. Separate failed findings from
passing-but-suboptimal observations. Recommendations, proposed language, and
copy-ready replacements for failures or passing-but-suboptimal observations are
advisory and do not authorize implementation.
