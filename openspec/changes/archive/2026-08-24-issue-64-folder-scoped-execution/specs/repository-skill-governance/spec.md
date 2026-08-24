## ADDED Requirements

### Requirement: Independently installable folder boundary

Every public `SKILL.md` MUST carry a compact folder-scoped execution contract
that treats only caller-declared input folders as available and recursively
read-only, permits writes only beneath the caller-declared output folder,
permits internet use only when the skill expressly authorizes it, and stops
before reading case material when the host cannot enforce those boundaries. The
full protocol SHALL remain in the repository's canonical execution owner and
MUST NOT be copied in full into every skill.

#### Scenario: Skill is installed alone

- **WHEN** an agent loads one public skill without repository-root governance
  files
- **THEN** that skill still preserves the compact input, output, internet, and
  host-enforcement boundary

### Requirement: Deterministic folder-contract validation

Repository governance validation MUST inspect every public `SKILL.md` and fail
with a stable skill-specific finding when the compact folder-scoped contract is
missing or semantically inverted. The validator MUST NOT claim to prove host
isolation or subjective agent behavior.

#### Scenario: Public skill omits the compact contract

- **WHEN** a public skill lacks or inverts a required folder-scoped boundary
- **THEN** repository validation exits nonzero and identifies that skill

### Requirement: Protected folder-execution gate

The repository MUST protect folder scope, recursive input non-mutation, output
confinement, and declared internet policy as contribution gates. A contribution
that weakens or bypasses one of those gates SHALL identify the affected gate and
rationale and request explicit human review.

#### Scenario: Contribution changes filesystem authority

- **WHEN** a contribution broadens input mutation, output placement, undeclared
  path access, or internet authority
- **THEN** the pull request identifies the protected change for explicit human
  review before acceptance
