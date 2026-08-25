# collecting-police-policy-sources Specification

## ADDED Requirements

### Requirement: Collection uses exact declared folders

The installed skill MUST accept exactly the recursive read-only
`department-identity`, `jurisdiction`, `approved-source-system`, and
`research-scope` input roles, no target, authorized internet, and one explicit
output folder. It MUST require all temporary work beneath
`<output-folder>/temp/` and MUST NOT require a package, graph, repository, or
ambient workspace.

#### Scenario: Complete bounded collection is supplied

- **WHEN** the trusted host supplies the exact roles, authorized internet, one
  output folder, and enforceable isolation
- **THEN** the skill may perform only the bounded source collection

### Requirement: Every acquired file has strict source documentation

Every proposed ordinary source file MUST have one adjacent domain `SOURCE.yaml`
record that binds its relative path and SHA-256 to provenance, query coverage,
dates, result identity, classification, adoption relationship, review state,
retrieval result, effective-date evidence or gap, limitations, and duplicate
relationships.

#### Scenario: Retrieved bytes changed after documentation

- **WHEN** the documented SHA-256 differs from the proposed ordinary bytes
- **THEN** validation fails and neither file is eligible for publication

### Requirement: Classification remains source bounded

The collector MUST distinguish adopted policy, statute, regulation,
collective-bargaining material, accreditation material, model policy, training
material, form, guidance, and comparison material. It MUST NOT turn a proposed
classification or adoption relationship into policy meaning or compliance.

#### Scenario: Model policy is discovered

- **WHEN** a source is a model policy without adoption evidence
- **THEN** it remains classified as model policy with an uncertain or rejected
  adoption relationship and cannot be represented as department policy

### Requirement: Coverage gaps remain visible

The collector MUST record empty, incomplete, inaccessible, paid, ambiguous, and
out-of-scope searches as bounded gaps. Those gaps MUST NOT establish absence of
a policy or version.

#### Scenario: Search returns no result

- **WHEN** one bounded source-system query returns no result
- **THEN** the gap record preserves the exact query, filters, source system,
  checked date, and coverage limitation without asserting nonexistence

### Requirement: Collection and analysis are separate invocations

The collection skill MUST return only output-relative source, YAML, index, and
gap artifact plans to the trusted host. It MUST NOT analyze newly acquired
material under Issue #57 during the same invocation. A later caller MAY declare
the reviewed output folder as a new read-only input.

#### Scenario: Collection completes successfully

- **WHEN** the trusted host durably publishes the proposed collection files
- **THEN** those files remain collection output until a later invocation
  expressly supplies them as reviewed input
