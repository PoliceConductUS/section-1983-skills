# Proposal: Collect source-documented legal-authority files

## Why

Authority audits need reusable source material, but collection must not imply
that an opinion, citation, proposition, treatment, or fair-warning use has been
verified. Issue #60 needs a bounded authorized collector that preserves ordinary
source bytes, provenance, classifications, candidate identities, and gaps for a
later independent audit.

## What changes

- Add `collecting-legal-authority-sources` with exact `legal-question`,
  `jurisdiction`, `court-hierarchy`, `relevant-date`, `seed-authority`, and
  `approved-source-system` folders.
- Authorize internet only for bounded collection under the caller's source,
  access, date, and cost limits.
- Return ordinary retrieved files, adjacent strict domain source YAML, a
  candidate index, and a gap register for trusted-host publication.
- Preserve source type, exact query and result provenance, decision-date
  evidence or gap, proposed citation identity, limitations, and duplicates.
- Keep authority verification exclusively in a later `audit-authorities`
  invocation.

## Capability

- `collecting-legal-authority-sources`

## Non-goals

- No package, graph, authority audit, legal-strategy decision, claim selection,
  filing language, or assertion that an empty search proves no authority exists.
