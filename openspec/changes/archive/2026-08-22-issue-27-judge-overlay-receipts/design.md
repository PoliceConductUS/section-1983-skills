# Design

## Context

The judge-overlay method already validates neutral transfer cards, degrades
unsupported conclusions to no drafting change, and prohibits judge gaming. The
repository also requires independent quality-control reports to be read-only,
immutable, exclusive, and version-local. Issue 27 joins those contracts with an
execution receipt; it does not alter either evidence standard.

## Goals / Non-Goals

**Goals:**

- Prove which overlay and evidence inputs were used for one filing version.
- Distinguish completed no-change degradation from no execution.
- Fail closed on every required invalid or unavailable input.
- Preserve the filing and prior audit reports byte-for-byte.
- Keep every report inside the audited version's canonical `audits/` directory.

**Non-Goals:**

- Researching, validating, or inventing judge tendencies.
- Editing the filing or implementing report recommendations.
- Predicting outcomes, exploiting preferences, manipulating assignment, or
  altering facts, law, or adverse authority.
- Replacing the canonical corpus, transfer-card, authority, or Filing CI gates.

## Decisions

### One complete execution packet

Publish `judge-overlay-execution.schema.json` in the generic drafting package.
The exact Draft 2020-12 packet contains:

- schema version, audited version ID, scope, and approved source IDs;
- relative artifact paths and expected SHA-256 fingerprints;
- overlay skill, version, fingerprint, checked date, and validation status;
- corpus ID, version, fingerprint, checked date, and validation status;
- official court-conduct source IDs, checked dates, and validation statuses;
- neutral transfer-card IDs, validation statuses, and used flags;
- the exact required anti-gaming check IDs and Boolean pass results; and
- requested execution status, drafting changes with supporting transfer-card
  IDs, a no-change reason, or a stable failure class.

Validation statuses are `passed`, `missing`, `stale`, `failed`, or
`unavailable`. The writer accepts only exact keys, stable IDs, UTC/ISO dates,
lowercase SHA-256 values, unique arrays, and strings without leading or trailing
whitespace. It rejects path fields outside the artifact records.

### Artifact and output preflight

The public API receives a project boundary, one existing version folder, the
packet, and injectable UTC time/run ID for deterministic tests. The CLI receives
the boundary and version folder as argv and the packet on standard input.

Before creating output, resolve the project and version canonically; require the
version inside the project; reject artifact traversal, absolute paths, missing
files, directories, and every artifact under `audits/`; and compute each actual
fingerprint. A mismatch becomes `artifact-fingerprint-mismatch` and may be
recorded only inside a valid version-local receipt. The script never writes to
an artifact.

Resolve or create only `<version-folder>/audits/`. Reject a symlink or canonical
escape. Create `judge-overlay-execution-<UTC compact timestamp>-<run-id>.md`
exclusively. A collision fails before any write and preserves the existing
report.

### Outcome normalization

A completed run may have either:

1. one or more drafting changes, each supported by a used, passing transfer
   card; or
2. no changes and one nonempty bounded reason, rendered exactly as
   `no judge-specific drafting change`.

The second result proves execution and degradation. An absent receipt proves
nothing about execution.

Any nonpassing overlay, corpus, required court-conduct input, or used transfer
card; missing required anti-gaming check; failed anti-gaming check; fingerprint
mismatch; unsupported change; or requested failed status normalizes to
`failed-closed`. The receipt records one stable failure class, no drafting
changes, and never labels the result passed.

### Exact anti-gaming checks

Every packet contains each of these IDs exactly once with `passed: true` for a
completed result:

- `assignment-manipulation`;
- `preference-exploitation`;
- `desired-outcome-tailoring`;
- `adverse-authority-concealment`;
- `record-distortion`;
- `court-personalization`;
- `outcome-or-behavior-prediction`; and
- `unsupported-judge-conclusion`.

A missing, duplicate, unknown, or failed check is fail-closed. These checks
record that the existing prohibited-inference gate ran; they do not create a new
natural-language judge profiler.

### Receipt content and non-mutation

The Markdown receipt identifies the audited version path and ID, artifact paths
and expected/actual fingerprints, quality-control kind, UTC run time, run ID,
scope, approved sources, overlay and corpus identities/versions/check dates/
validation, official conduct inputs, qualifying neutral cards used, every anti-
gaming check, normalized outcome, bounded reason or failure class, and supported
drafting changes.

The receipt states that recommendations are advisory and require separately
authorized remediation in a new version followed by a fresh read-only audit. The
stage writes no recommendation unless one is already present in the packet;
Issue 27 adds no recommendation field. Prior reports are excluded from artifact
inputs and remain immutable.

## Testing

- Structural tests require the install-local schema/script and exact guide,
  router, assigned-judge, and reference routes.
- API and CLI tests use temporary generic version folders and literal SHA-256
  values. They fingerprint every preexisting file before and after execution.
- A completed change run and completed no-change run write the exact receipt; an
  uninvoked overlay writes nothing.
- Table-driven semantic failures cover every nonpassing validation status,
  missing/failed/unknown/duplicate anti-gaming checks, unsupported changes, and
  fingerprint mismatch.
- Path tests cover missing/out-of-bound versions, absolute/traversing/audits
  artifacts, audits symlink escape, and report collision.
- Mutation tests reject every prohibited behavior while preserving neutral
  no-change language and the filed artifact bytes.

## Risks / Trade-offs

The receipt proves what the composing run declared and what the writer verified;
it does not independently rerun the judge corpus validator. Fingerprint and
status preservation keeps that boundary visible. Requiring exact check IDs is
less flexible than free prose but makes anti-gaming execution auditable. A
failed output preflight cannot write a receipt; the CLI returns a stable bounded
error and writes nowhere else.
