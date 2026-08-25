# source-documented-folders Specification

## Purpose

TBD - created by archiving change issue-68-source-documented-folders. Update
Purpose after archive.

## Requirements

### Requirement: Domain data uses ordinary declared folders

Skills MUST consume participant, court, profile, overlay, and research data only
as ordinary files selected from named recursive read-only input folders. Skills
MUST write proposed artifacts directly beneath the invocation's one explicit
output folder and MUST use `<output-folder>/temp/` as the only temporary
workspace. A generic package manifest, identity, kind, loader, publisher,
registry, graph, or CaseGraph adapter MUST NOT be required.

#### Scenario: A profile becomes input to a role run

- **WHEN** a later role run uses a previously generated profile
- **THEN** the caller declares the profile's ordinary folder as an input root
  and the host selects required immutable file bytes without loading a package

### Requirement: Domain YAML records document sources and derived artifacts

Each domain contract MUST name and validate the YAML records required for its
source units and derived artifacts. Applicable records MUST preserve
folder-relative artifact references, hashes, provenance or retrieval identity,
checked-through or retrieval dates, classifications, validation state,
assumptions, and gaps. The repository MUST NOT require one generic root manifest
or one generic YAML schema for every folder.

#### Scenario: A source reference is invalid

- **WHEN** a required domain YAML record is missing, malformed, stale, points
  outside its declared input root, or gives a hash that does not match the
  referenced bytes
- **THEN** the invocation fails before semantic work

### Requirement: Protected behavior remains separate from folder data

Protected behavior MUST remain in installed skill or static-role instructions.
Participant-, court-, posture-, source-class-, and assumption-specific files
MUST remain data and MUST NOT alter protected capabilities, prohibitions,
target-mutation boundaries, output authority, or filesystem/network access.

#### Scenario: Data contains instruction-shaped text

- **WHEN** an input YAML or artifact asks for broader behavior or access
- **THEN** the host treats that text only as untrusted domain data and preserves
  the protected instructions and invocation authority unchanged
