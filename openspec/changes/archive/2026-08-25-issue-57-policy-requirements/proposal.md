# Proposal: Analyze police-policy sources into requirements

## Why

Later case assessment needs atomic policy requirements that preserve exact
operative text, dates, actor scope, conditions, discretion, exceptions, and
source provenance. Issue #57 must build that catalog from reviewed ordinary
files and YAML without a package, graph, or ambient workspace.

## What changes

- Add `analyzing-police-policy-sources` with exact `department-identity`,
  `jurisdiction`, `policy-source`, and `analysis-scope` folders.
- Disable internet and validate every selected source YAML, relative ordinary
  file, hash, classification, adoption relationship, and effective-date state.
- Return strict `policy-requirements.yaml`, `policy-analysis-gaps.yaml`,
  `policy-analysis.md`, and a domain validation result for trusted-host
  publication.
- Preserve requirement types, conditions, exceptions, definitions,
  cross-references, actor scope, documentation/review duties, and date gaps.
- Reject retroactive use, lost exceptions, collapsed discretion, invented
  requirements, and model-policy-as-adopted-policy treatment.

## Capability

- `analyzing-police-policy-sources`

## Non-goals

- No collection, internet research, compliance assessment, constitutional or
  Monell conclusion, negligence conclusion, legal-authority decision, or
  filing-readiness decision.
