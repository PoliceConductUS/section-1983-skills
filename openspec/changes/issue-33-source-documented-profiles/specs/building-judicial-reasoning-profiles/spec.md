## MODIFIED Requirements

### Requirement: Acquisition and compilation are separate invocations

The builder MUST expose separate acquisition and compilation operations.
Acquisition MUST require expressly authorized internet and MUST write ordinary
source bytes plus domain `SOURCE.yaml` provenance directly beneath the explicit
output folder. Compilation MUST disable internet, MUST use only files from its
declared read-only inputs, and MUST write `judicial-profile.json`,
`judicial-profile-sources.yaml`, and `validation-receipt.json` directly beneath
a different explicit output folder. Every temporary file MUST remain beneath
`<output-folder>/temp/`. Neither operation may create or consume a package
manifest, package identity, package loader, graph, or CaseGraph object.

#### Scenario: Newly acquired source becomes eligible for compilation

- **WHEN** acquisition writes public-source bytes and matching `SOURCE.yaml`
  provenance into its explicit output folder
- **THEN** compilation may use those bytes only in a later invocation that
  declares the acquisition folder as recursive read-only `approved-sources`

## ADDED Requirements

### Requirement: Profile source references preserve folder provenance

The compiled profile MUST retain each source ID and MUST emit a domain YAML
source index mapping that ID to the declared input role, folder-relative
`SOURCE.yaml`, referenced artifact path, SHA-256, applicable dates,
classification, validation state, limitations, and gaps. Missing, malformed,
escaping, mismatched, or stale required source records MUST stop compilation
before semantic work.

#### Scenario: Profile source hash does not match

- **WHEN** a source index entry's SHA-256 does not match the referenced bytes in
  its declared read-only input folder
- **THEN** compilation fails and emits no profile
