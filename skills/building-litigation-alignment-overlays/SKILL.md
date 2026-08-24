---
name: building-litigation-alignment-overlays
description: >-
  Use when a Section 1983 case needs docket-derived litigation-alignment groups,
  actual adversary attack profiles, plaintiff-response coverage, judicial
  treatment, independent review jobs, or filing-version overlay pins.
---

# Building Litigation-Alignment Overlays

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Purpose

Transform one approved immutable docket snapshot into a source-backed, versioned
case overlay. Preserve who said what. The output informs later drafting and
independent review; it does not decide truth, strategy, outcome, or filing
readiness.

Every returned overlay artifact must identify the actual approved source
identity and checked date used.

## Load the contracts

Read these install-local contracts completely:

- [references/docket-snapshot.schema.json](references/docket-snapshot.schema.json)
- [references/litigation-alignment-overlay.schema.json](references/litigation-alignment-overlay.schema.json)
- [references/filing-overlay-manifest.schema.json](references/filing-overlay-manifest.schema.json)

Use only one existing snapshot that passed its approved project preflight. Do
not browse, open an unlisted path or URL, silently refresh the docket, or add a
source from conversation history. If the snapshot is missing, stale, ambiguous,
or invalid, report the scoped gap and stop overlay generation.

## Derive litigation-alignment groups

Preserve every individual defendant. Build groups per issue, not per caption,
law firm, or filing. Compare capacity, challenged act, relevant-time knowledge
position, qualified-immunity position, requested relief, and every other
material defense. Split defendants when any dimension diverges.

Keep a municipality separate from individual-capacity defendants unless the
approved record establishes alignment for that particular issue. Joint
representation or a joint filing is evidence to inspect, not proof of complete
alignment.

Keep generated groups immutable. Record a user addition, exclusion, or
regrouping as an explicit override with its instruction ID, affected defendants,
generated groups, effective groups, and rationale. Never erase the generated
profile or its provenance.

## Build three canonical ledgers

Keep these ledgers separate and fingerprint each one:

1. `adversary_attacks` contains only adversary positions and adversary-prefixed
   statuses.
2. `plaintiff_responses` contains only plaintiff coverage and plaintiff-prefixed
   states.
3. `judicial_treatments` contains only treatment attributed to the actual
   magistrate judge, district judge, or appellate court.

Every attack identifies its exact source, docket entry, page, heading,
quotation, date, group, claim, defendants, challenged act, element or defense,
qualified-immunity prong when applicable, requested disposition, and current
adversary status.

An adoption, rejection, or modification links to the recommendation it treats.
It does not convert the magistrate judge's reasoning into district-judge
reasoning. Record independent reasoning only when the supplied judicial source
contains it. Missing documents, uncertain grouping, uncertain authorship, and
unresolved treatment remain scoped gaps.

## Derive without conflating

The issue matrix links canonical record IDs and the exact union of their source
IDs. Do not copy position text into the matrix. Silence is not agreement,
non-opposition, withdrawal, rejection, or adoption. With no approved response or
treatment record, use the explicit unavailable state.

## Plan independent reviews

For every target artifact and effective group with an available actual profile,
create two distinct fresh jobs:

- `blind-common-attack` receives the target and common checklist but no
  adversary attack ID, source, content, or prior review; and
- `actual-adversary` receives only the attacks and sources matching that group,
  claim, defendants, and challenged acts.

Treat a leave motion and proposed amended complaint as separate targets. They
require four jobs per group. When no responsive filing exists, mark
`actual-adversary-unavailable`, create two fresh blind common-attack jobs per
group, and do not invent an actual attack.

Dispatch each job through `adversarial-filing-review` only after the overlay and
review plan validate. The blind reviewer never receives an overlay slice. The
actual reviewer receives only its validated slice.

## Pin and validate

Run:

```bash
python3 scripts/validate_overlays.py SNAPSHOT_JSON OVERLAY_JSON \
  --filing-manifest FILING_MANIFEST_JSON
```

The filing-version manifest pins every consumed overlay by kind, ID, version,
SHA-256, checked-through date, validator result, and source snapshot. A stale,
mismatched, or failing overlay produces no specialized drafting change.

Create a new immutable overlay version after a material docket, party,
alignment, attack, response, judicial-treatment, assignment, official-rule, or
user-override event. Preserve superseded versions. Never overwrite an overlay,
snapshot, manifest, source, target artifact, or filing.

## Boundaries

This skill does not research or profile an attorney or counsel. It does not
edit, revise, or modify a filing or artifact. It does not predict outcomes,
infer personality, recommend gaming, select a litigation position, or verify
legal authority. Recommendations are advisory and remediation requires a
separately authorized drafting stage and a new version when applicable.

Use `building-defense-counsel-overlays` as a separate stage when approved public
research should supply professional attorney identity or counsel-team behavior.
The litigation-alignment overlay continues to own current attacks and filing-
version composition; it does not absorb counsel history or forecasts.
