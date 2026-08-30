# analyzing-police-policy-sources Specification

## Purpose

Define an offline folder-native skill that decomposes approved adopted-policy
ordinary files into source-bounded atomic requirements and explicit gaps without
deciding conduct, compliance, or legal liability.

## Requirements

### Requirement: Analysis uses exact declared folders

The installed skill MUST accept exactly the recursive read-only
`department-identity`, `jurisdiction`, `policy-source`, and `analysis-scope`
roles, no target, disabled internet, and one explicit output folder. Temporary
work MUST remain under `<output-folder>/temp/`.

#### Scenario: Complete offline analysis is supplied

- **WHEN** the trusted host validates the exact roles and enforceable isolation
- **THEN** analysis uses only the selected ordinary files and YAML within those
  folders

### Requirement: Selected source bytes are strictly bound

The analyzer MUST validate each selected source YAML, adjacent ordinary file,
relative path, SHA-256, classification, adoption relationship, review state, and
effective-date state before decomposition.

#### Scenario: Selected policy hash changed

- **WHEN** the ordinary file no longer matches its documented SHA-256
- **THEN** analysis fails before producing a requirement

### Requirement: Atomic requirements preserve operative limits

Each requirement MUST preserve its quotation, pinpoint, actor, trigger,
mandatory/prohibited/permitted/discretionary type, action, conditions,
exceptions, definitions, dependencies, cross-references, documentation or review
duty, effective interval or date gap, source path/hash, and unresolved gaps.

#### Scenario: Conditional requirement is decomposed

- **WHEN** operative language applies only after a stated trigger and subject to
  an exception
- **THEN** the trigger and exception remain attached to the same atomic record

### Requirement: Source classification controls catalog use

The analyzer MUST NOT represent model, accreditation, training, statutory,
regulatory, collective-bargaining, form, guidance, or comparison material as
department policy without adopted-policy classification and documented adoption.

#### Scenario: Model policy lacks adoption evidence

- **WHEN** selected material is classified `model_policy` with uncertain
  adoption
- **THEN** it produces a source gap or bounded comparison note and no
  department-policy requirement

### Requirement: Catalog output remains non-liability analysis

The analyzer MUST return deterministic requirement YAML, gap YAML, analysis
Markdown, and domain validation bytes for trusted-host publication. It MUST NOT
decide policy compliance, constitutional or Monell liability, negligence,
admissibility, legal authority, or filing readiness.

#### Scenario: Catalog validates

- **WHEN** every proposed requirement and gap passes the domain contract
- **THEN** the trusted host may publish the artifacts without treating them as a
  compliance or liability conclusion
