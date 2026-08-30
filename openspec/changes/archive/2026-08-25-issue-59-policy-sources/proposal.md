# Proposal: Collect source-documented police-policy files

## Why

Policy analysis needs approved source bytes with explicit provenance, version,
classification, and coverage gaps. Issue #59 must acquire those materials
without a case-data package, root manifest, graph, repository, or ambient
workspace dependency.

## What changes

- Add one public `collecting-police-policy-sources` skill with exact
  `department-identity`, `jurisdiction`, `approved-source-system`, and
  `research-scope` input folders.
- Authorize internet only for the bounded collection invocation.
- Return ordinary source bytes, adjacent domain `SOURCE.yaml` records, a
  candidate index, and a gap register for trusted-host publication beneath one
  explicit output folder.
- Validate source classifications, provenance, checked dates, hashes, adoption
  uncertainty, review state, coverage gaps, and collector/analyzer separation.
- Keep every transient byte and process temporary location beneath
  `<output-folder>/temp/`.

## Capability

- `collecting-police-policy-sources`

## Non-goals

- No policy interpretation, semantic decomposition, compliance conclusion,
  liability conclusion, admissibility decision, filing-readiness decision, or
  same-invocation use by the analyzer.
- No package, manifest loader, FilingPacket, graph, CaseGraph, Git, repository,
  datastore, or ambient folder discovery.
