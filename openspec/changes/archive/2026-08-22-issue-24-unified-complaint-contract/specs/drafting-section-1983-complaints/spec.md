## ADDED Requirements

### Requirement: Canonical complete complaint owner

The `drafting-section-1983-complaints` package SHALL be the only canonical owner
of the complete general Section 1983 complaint skeleton and detailed count
contract. It MUST provide both contracts through install-local references and
MUST require them for complaint drafting, revision, and audit.

#### Scenario: General complaint package is installed alone

- **WHEN** an agent receives only the `drafting-section-1983-complaints` package
  for a complaint task
- **THEN** the package supplies the ordered whole-document skeleton and the
  complete detailed count contract without relying on another skill package

#### Scenario: Canonical reference is unavailable

- **WHEN** either canonical complaint reference cannot be read
- **THEN** the package reports the complaint contract unavailable and does not
  invent or reconstruct the missing requirements

### Requirement: Ordered whole-document contract

The canonical complaint contract MUST define caption, optional introduction,
jurisdiction and venue, parties and capacities, chronological numbered facts,
separate counts, prayer for relief, jury demand, and signature block in that
order, subject only to a verified governing-court requirement.

#### Scenario: Agent constructs a complaint checklist

- **WHEN** an agent derives a complaint checklist from the canonical package
- **THEN** every required section appears once in canonical order and the
  introduction remains expressly optional

### Requirement: One detailed record per count tuple

The canonical complaint contract MUST require one count mapping for every
claim-defendant-capacity tuple. Each mapping SHALL identify the count,
constitutional source, defendant, capacity, challenged act, event stage,
governing standard and pinpoint, decisive-fact and incorporated paragraph
references, relevant-time knowledge, application, qualified-immunity material
when applicable, injury, relief, and result.

#### Scenario: One claim names two individual defendants

- **WHEN** the same legal claim is asserted against two individual defendants
- **THEN** the complaint contract requires two separately complete mappings
  rather than one collective count record

#### Scenario: Qualified immunity does not apply

- **WHEN** a count is against a defendant or capacity that cannot assert
  qualified immunity
- **THEN** the qualified-immunity fields are inapplicable without relaxing any
  other required count field

### Requirement: Umbrella routing without fallback

The `section-1983-drafting` package MUST route every complaint, amended
complaint, and amendment proffer to `drafting-section-1983-complaints`. It MUST
NOT maintain or use a competing general complaint skeleton or count contract.

#### Scenario: Umbrella is installed without the canonical owner

- **WHEN** a complaint task reaches the umbrella package but the canonical
  complaint package is unavailable
- **THEN** the umbrella reports the complaint contract unavailable and does not
  draft or audit from a local fallback

### Requirement: Specialization contains only deltas

The `drafting-false-arrest-complaints` package MUST load the canonical general
complaint package first and SHALL add only false-arrest-specific requirements.
It MUST NOT restate or replace the generic whole-document skeleton or detailed
general count contract.

#### Scenario: False-arrest stack is complete

- **WHEN** all three packages are installed for a false-arrest complaint
- **THEN** the general package supplies the one complete general contract and
  the false-arrest package supplies only its seizure, offense, actor,
  chronology, incorporated-material, and compression deltas

#### Scenario: General complaint owner is unavailable

- **WHEN** the false-arrest package is installed without the canonical general
  complaint package
- **THEN** it reports the complaint contract unavailable and does not promote
  its delta into a replacement general contract

### Requirement: Deterministic external-checker handoff

The canonical package SHALL publish one machine-readable contract identifying
the owner, version, ordered sections, count cardinality, required fields,
conditional qualified-immunity fields, mechanical checks, excluded judgments,
and stable finding shape. The package MUST NOT claim that this handoff executes
or replaces a configured checker.

#### Scenario: External checker reads the handoff

- **WHEN** a project-configured checker consumes the machine-readable contract
- **THEN** it can derive section/order, numbering, identifier, tuple,
  cross-reference, incorporation, and field-presence checks with stable finding
  identifiers and nonzero failure status

#### Scenario: Requested check requires legal judgment

- **WHEN** a requested check concerns fact truth, legal sufficiency, authority
  fit, material analogy, strategy, or filing readiness
- **THEN** the handoff identifies that question as excluded rather than
  representing it as deterministic

### Requirement: Install-local and behavioral verification

The repository MUST verify that each package's live local links remain confined
to that package and that realistic isolated compositions either supply the one
complete contract or fail closed. Instruction behavior MUST be pressure-tested
in fresh contexts before and after the change.

#### Scenario: Package is installed independently

- **WHEN** any affected package is copied without the repository root
- **THEN** every live local link resolves within that package and no dependency
  is represented by a broken cross-package file link

#### Scenario: Agent faces pressure to fill a missing contract

- **WHEN** deadline, authority, or sunk-cost pressure encourages an agent to
  draft from an incomplete or conflicting composition
- **THEN** the agent uses the canonical owner or reports the contract
  unavailable without inventing or silently reconciling requirements
