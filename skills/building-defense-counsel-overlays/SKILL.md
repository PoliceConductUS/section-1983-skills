---
name: building-defense-counsel-overlays
description: >-
  Use when a Section 1983 case needs source-backed defense-attorney identity,
  counsel-team litigation behavior, court-treatment history, or a calibrated
  forecast of a defense team's likely next professional litigation move.
---

# Building Defense-Counsel Overlays

## Folder-scoped execution

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Purpose

Build an immutable professional litigation profile from one approved public-
source snapshot. Keep identity, team behavior, court treatment, current attacks,
and forecasts separately attributable. The profile informs an actual-adversary
review; it does not decide law, strategy, outcome, or filing readiness.

Every returned artifact must identify the actual approved source identity and
checked date used.

## Load the contracts

Read these install-local contracts completely:

- [references/counsel-research-snapshot.schema.json](references/counsel-research-snapshot.schema.json)
- [references/defense-counsel-overlay.schema.json](references/defense-counsel-overlay.schema.json)

Use only one existing snapshot that passed its approved project preflight. Do
not browse, open an unlisted path or URL, silently refresh a source, or incur a
PACER or other fee. Missing public content and unavailable paid content are
scoped gaps unless the user separately authorizes retrieval.

## Separate identity from behavior

An identity record may contain verified professional name, bar status, firm
affiliations, appearances, represented parties, dates, roles, and sources. It
contains no litigation behavior.

Build a counsel team per matter, effective date range, represented party, and
litigation-alignment group. Appearance, withdrawal, substitution, or changed
alignment produces a new immutable team version.

Distinguish signer, named author, oral advocate, appearance counsel, listed
counsel, and counsel team. Appearance or listing proves neither authorship nor
individual behavior. Attribute a joint filing to the counsel team unless an
approved source directly identifies an individual signer, named author, or oral
advocate.

## Preserve four evidence layers

Keep historical counsel arguments, judicial treatment, current-case attacks, and
forecasted next moves in separate ledgers. Historical arguments preserve exact
source, location, quotation, posture, party, group, claim, challenged act,
defense, qualified-immunity prong, requested relief, attribution, and date.

A court's recommendation, adoption, rejection, modification, reversal, or other
treatment remains the court's record linked to the historical argument. It is
not counsel conduct. A current attack remains the canonical attack ID from the
litigation-alignment overlay; do not copy or relabel its text.

## Calibrate patterns and forecasts

A pattern or professional next-move forecast requires a declared comparable
corpus, selection method, denominator, coded count, unresolved and unavailable
missingness, posture, supporting examples, contrary examples, confidence, source
IDs, checked-through date, and limits. Every cited record must belong to that
corpus.

An incomplete corpus supports bounded examples and gaps only. It cannot support
`often`, `usually`, a loss rate, a recurring pattern, or a forecast. A forecast
uses low, moderate, or high confidence and may say a team `may` make a defined
professional move. It must not say counsel will, always, or never act, predict a
case outcome or judicial behavior, or turn a forecast into an actual attack.

Cross-case differences remain sourced comparisons. They do not establish waiver,
concession, estoppel, misconduct, or bad faith without a separate verified legal
analysis.

## Compose review inputs

A blind common-attack review receives no attorney identity, counsel team,
historical behavior, court treatment, pattern, forecast, or counsel source. An
actual-adversary review receives only the validated current team and
professional history relevant to the target group, claim, defendants, challenged
acts, posture, and effective date.

Keep the Judicial Reasoning Profile, defense-counsel profile, controlling law,
and litigation-alignment attack slice separate. A forecast must not suppress,
replace, remove, or displace any common attack or the independent blind review.

## Validate and version

Run:

```bash
python3 scripts/validate_counsel_overlays.py SNAPSHOT_JSON OVERLAY_JSON \
  --filing-manifest FILING_MANIFEST_JSON
```

Pin counsel identity and counsel team as separate overlay kinds in the filing-
version manifest. A stale, mismatched, or failing pin produces no specialized
drafting change.

Create a new immutable version after appearance, withdrawal, substitution,
changed team alignment, a new signed filing or oral argument, verified identity
or status change, new court treatment, material public evidence, corrected
attribution, or an explicit user scope change. Preserve superseded versions. A
user override may change scope; it cannot rewrite provenance, attribution,
checked dates, history, forecasts, or prior versions.

## Boundaries

Exclude family, politics, private life, protected traits, rumors, personality
assessments, irrelevant social media, threats, deception, harassment, and
instructions to manipulate an adversary or judge.

This skill does not edit, revise, modify, overwrite, correct, or regenerate a
filing or artifact. Recommendations remain advisory. Remediation requires a
separately authorized drafting stage, a new version when applicable, and a new
read-only quality check.
