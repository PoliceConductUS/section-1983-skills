# Brainstorm: Defense-counsel litigation profiles

## Problem

The case-overlay lifecycle can identify actual attacks by litigation-alignment
group, but it intentionally does not research the professional behavior of
individual defense attorneys or counsel teams. Current-case attack records say
what counsel has asserted in this case. They do not establish who authored a
joint filing, which positions recur in comparable matters, how courts treated
those positions, or what bounded next move the public record supports expecting.

## Approved direction

- Create one public skill for evidence-coded defense-counsel overlays.
- Maintain reusable individual-attorney identity records separately from
  time-bounded counsel-team behavior records.
- Treat signer, named author, oral advocate, appearance counsel, and listed
  counsel as different attribution roles. A joint paper belongs to the counsel
  team unless a source supports individual authorship.
- Keep historical arguments, court treatment, current-case attacks, and
  forecasted next moves in separate canonical ledgers.
- Link counsel teams to issue-scoped litigation-alignment groups and effective
  date ranges. Do not treat a firm, caption, or appearance as permanent
  alignment.
- Permit calibrated forecasts of professional litigation moves only from a
  declared comparable corpus with denominator, missingness, supporting and
  contrary examples, posture, confidence, source IDs, and checked-through date.
- Keep the Judicial Reasoning Profile, controlling-law analysis, and counsel
  profile separate. Drafting may intersect them but may not merge their
  provenance or conclusions.
- Preserve a blind common-attack review with no counsel material. An actual-
  adversary review may receive only the relevant validated counsel-team slice;
  forecasts never suppress common attacks.
- Publish counsel-specific creation, reuse, refresh, rebuild, and supersession
  rules in `COUNSEL_OVERLAYS.md`. Keep shared inventory, precedence, manifest,
  and immutable-version rules in `OVERLAYS.md`.

## Options rejected

### One profile per law firm

Rejected because lawyers join, withdraw, substitute, divide responsibility, and
represent different litigation-alignment groups over time. The effective team
must be source-backed and date-bounded.

### Attribute every joint paper to every listed lawyer

Rejected because an appearance or signature block does not prove authorship.
Individual behavior requires a signer, named author, oral advocate, or another
approved source that directly supports the attribution.

### Treat recurring arguments as certain future conduct

Rejected because incomplete public dockets and changing posture make certainty
unsupportable. A forecast is a bounded professional prediction with explicit
denominator, missingness, contrary evidence, and confidence; it is never a case-
outcome prediction.

### Combine court treatment with counsel conduct

Rejected because a court's rejection or adoption is not counsel's statement.
Court treatment remains a separately attributable ledger linked to the exact
historical argument.

### Research personal traits

Rejected because family, politics, rumors, private life, irrelevant social
media, personality assessments, and protected traits are outside legitimate
litigation intelligence.

## Public surface

- New public skill: `building-defense-counsel-overlays`.
- New counsel-specific guide: `COUNSEL_OVERLAYS.md`.
- Install-local schemas for an immutable counsel research snapshot and defense-
  counsel overlay.
- One standard-library validator and generic synthetic fixtures.
- Modified filing-overlay manifest kinds and actual-adversary review slices in
  the existing litigation-alignment capability.
- Modified README, drafting router, general overlay guide, and governance
  registry.

## Boundaries

The skill does not incur PACER or other fees, browse during validation, conduct
personal investigations, infer private characteristics, decide estoppel, waiver,
concession, or strategy, predict a case outcome or judicial behavior, edit a
filing, or displace governing law and common-attack review.
