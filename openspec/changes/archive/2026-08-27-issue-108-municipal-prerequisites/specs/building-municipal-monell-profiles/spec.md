## ADDED Requirements

### Requirement: Prerequisite resolution is separate from profile compilation

The installed municipal-profile skill MUST expose a prerequisite-resolution
operation separately from its existing compilation operation. Resolution MUST
return a deterministic plan without opening an input or output folder, while
compilation MUST retain exactly its existing seven recursive read-only roles,
disabled internet, and profile artifacts. The operations MUST NOT combine their
folder roles or network authority.

#### Scenario: Profile catalog and assessment are absent

- **WHEN** prerequisite resolution receives no valid policy catalog or policy
  assessment
- **THEN** it returns an actionable next-stage plan without attempting profile
  compilation or broadening the compilation invocation

### Requirement: Policy prerequisites route through owning installed skills

The resolver MUST route an absent catalog through
`collecting-police-policy-sources` when approved sources are unavailable and
through `analyzing-police-policy-sources` when independently approved sources
are available. It MUST route an absent assessment through
`assessing-police-policy-compliance` only after a valid catalog exists.
Collection output MUST stop at independent review and MUST NOT approve itself or
automatically become policy-analysis input.

#### Scenario: Collection returns candidate policy material

- **WHEN** candidate sources have been collected but no independent
  `approved_for_analysis` review exists
- **THEN** the resolver returns `review-required` and does not route analysis

#### Scenario: Approved policy sources are available

- **WHEN** every analysis role and a fresh analysis output folder are ready
- **THEN** the resolver returns `ready-for-analysis` with the analyzer's exact
  roles, disabled internet, and required postconditions

#### Scenario: Valid catalog exists but assessment is absent

- **WHEN** every assessment role and a fresh assessment output folder are ready
- **THEN** the resolver returns `ready-for-assessment` with the assessor's exact
  roles, disabled internet, and required postconditions

### Requirement: Every stage preserves folder and authorization boundaries

Every collection, analysis, assessment, and profile stage MUST be a new trusted-
host invocation of its owning installed skill with that skill's exact declared
roles, network policy, and one caller-supplied full absolute output folder. Each
stage MUST keep temporary work beneath its own `<output-folder>/temp/`. A stage
output MUST become a later input only through a new invocation that explicitly
declares the published output folder as recursive read-only input. Network or
fee authority MUST NOT transfer between stages.

#### Scenario: Collection is otherwise ready but lacks internet authority

- **WHEN** every collection role and output folder are ready but bounded
  internet authorization is absent
- **THEN** the resolver returns `authorization-required` and does not launch or
  emulate collection

#### Scenario: Next stage lacks an output folder

- **WHEN** every semantic input is ready but no fresh full absolute output
  folder was supplied for the next invocation
- **THEN** the resolver returns `input-required` and identifies the missing
  output-folder precondition

### Requirement: Stage postconditions fail closed without erasing gaps

Before continuation, the resolver MUST require the expected four ordinary
analysis or assessment artifacts, a successful terminal receipt, a passing
domain validation result, and matching input fingerprints. Invalid, stale,
incomplete, or mismatched mechanical postconditions MUST return
`blocked-invalid` and require a fresh output folder. A structurally valid result
MUST remain eligible for continuation when it preserves substantive gaps,
uncertain applicability, or indeterminate assessment findings.

#### Scenario: Valid assessment preserves indeterminate findings

- **WHEN** the assessment validator passes, fingerprints match, and its ordinary
  artifacts preserve unresolved substantive gaps
- **THEN** prerequisite resolution treats the assessment as valid rather than
  requiring invented certainty

#### Scenario: Catalog claims validity without matching fingerprints

- **WHEN** a supplied catalog lacks any required postcondition or its input
  fingerprints do not match
- **THEN** the resolver returns `blocked-invalid` and does not use or overwrite
  that catalog

### Requirement: Prerequisite plans are deterministic and actionable

The resolver MUST return `municipal-profile-prerequisites.yaml` and
`municipal-profile-prerequisites.md` under its explicit output folder. The plan
MUST contain the workflow version, one current status, next installed skill,
exact required and missing roles, internet mode, output-folder readiness,
ordered blocking reasons, and ordered postconditions. Status MUST be one of
`input-required`, `authorization-required`, `review-required`,
`ready-for-collection`, `ready-for-analysis`, `ready-for-assessment`,
`ready-for-profile`, or `blocked-invalid`.

#### Scenario: Every profile prerequisite is valid and declared

- **WHEN** the valid catalog and assessment folders plus every other existing
  compilation role and a fresh profile output folder are ready
- **THEN** the resolver returns `ready-for-profile` and identifies the unchanged
  offline municipal-profile compilation invocation

#### Scenario: Unrelated profile input is absent

- **WHEN** policy prerequisites are valid but municipality, department, source,
  case-record, or verified-authority input is missing
- **THEN** the resolver returns `input-required` with the exact missing role and
  does not acquire, infer, or fabricate it
