# ordinary-filing-folders Specification

## Purpose

Define filing work over caller-declared recursive read-only folders, ordinary
files, explicit role-relative targets, one exact output folder, and its
output-local temporary subtree without a shared persistence abstraction.

## Requirements

### Requirement: Filing work uses ordinary declared folders

Filing-related skills MUST consume only caller-declared recursive read-only
input folders and ordinary files. They MUST NOT require a FilingPacket,
folder-wide manifest, generic index, loader, publisher, registry, graph,
repository, datastore, ambient workspace, or replacement folder object.

#### Scenario: A prior draft is revised

- **WHEN** a caller requests revision of a prior generated draft
- **THEN** the caller supplies that prior output folder as a declared read-only
  input to a new invocation
- **AND** the skill leaves every input byte unchanged

### Requirement: Targets are explicit

A task that targets one filing file MUST identify its declared input role and
folder-relative path. A whole-folder task MUST expressly identify the ordinary
files in scope rather than infer membership from a root manifest.

#### Scenario: A single response is audited

- **WHEN** the caller selects one response file for audit
- **THEN** the skill resolves only the declared role-relative target
- **AND** no folder membership file is required

### Requirement: Durable output uses the exact output folder

An invocation that writes durable output MUST receive exactly one
caller-selected full absolute output folder and MUST write generated files
directly beneath it. Missing output information MUST stop the invocation before
substantive or filesystem work.

#### Scenario: A proposed filing is generated

- **WHEN** the caller supplies the exact output folder
- **THEN** the proposed ordinary files are written directly beneath that folder
- **AND** no intermediate persistence namespace is created

### Requirement: Temporary work is output-local

The invocation MUST keep every cache, download, extraction, staging file,
process working directory, `TMPDIR`, `TMP`, `TEMP`, and other temporary byte
beneath `<output-folder>/temp/`.

#### Scenario: A filing source requires extraction

- **WHEN** an authorized invocation extracts or stages source material
- **THEN** all temporary paths are descendants of `<output-folder>/temp/`
- **AND** no other temporary directory is used
