# implemented-skill-folder-migration Specification

## Purpose

TBD - created by archiving change issue-71-folder-migration. Update Purpose
after archive.

## Requirements

### Requirement: Every public skill carries an exact folder contract

Every public skill MUST link to a schema-valid install-local folder contract
with exactly its approved ordered role set, target policy and target roles,
internet policy, and `append-immutable` output mode:

| Skill                                             | Ordered input roles                                                         | Target policy and roles                       | Internet   |
| ------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------- | ---------- |
| `adversarial-filing-review`                       | `filing`, `approved-sources`                                                | required in `filing`                          | authorized |
| `audit-authorities`                               | `filing`, `authorities`                                                     | required in `filing`                          | authorized |
| `auditing-section-1983-discovery-responses`       | `served-discovery`, `responses`, `production`, `authorities`                | required in `served-discovery` or `responses` | disabled   |
| `auditing-section-1983-privilege-logs`            | `privilege-log`, `served-discovery`, `authorities`                          | required in `privilege-log`                   | disabled   |
| `building-defense-counsel-overlays`               | `research-snapshot`, `case-record`                                          | required in `research-snapshot`               | disabled   |
| `building-judicial-reasoning-profiles`            | `judge-identity`, `court-scope`, `approved-sources`, `verified-authorities` | none                                          | authorized |
| `building-litigation-alignment-overlays`          | `docket-snapshot`, `filing`                                                 | required in `docket-snapshot`                 | disabled   |
| `drafting-false-arrest-complaints`                | `record`, `authorities`, `filing`                                           | optional in `filing`                          | disabled   |
| `drafting-section-1983-complaints`                | `record`, `authorities`, `filing`                                           | optional in `filing`                          | disabled   |
| `drafting-section-1983-declarations-and-evidence` | `record`, `authorities`                                                     | optional in `record`                          | disabled   |
| `drafting-section-1983-deposition-outlines`       | `record`, `authorities`, `discovery`                                        | optional in `record`                          | disabled   |
| `drafting-section-1983-meet-and-confer`           | `discovery-audit`, `served-discovery`, `authorities`, `conference-record`   | required in `discovery-audit`                 | disabled   |
| `drafting-section-1983-rule-59e`                  | `record`, `authorities`, `filing`                                           | optional in `filing`                          | disabled   |
| `drafting-section-1983-written-discovery`         | `record`, `authorities`, `claim-map`                                        | optional in `claim-map`                       | disabled   |
| `filing-ci`                                       | `filing`, `authorities`                                                     | required in `filing`                          | disabled   |
| `horan-bad-words`                                 | `filing`                                                                    | required in `filing`                          | disabled   |
| `rrd`                                             | `motion`, `record`, `authorities`                                           | required in `motion`                          | disabled   |
| `rrd-rule12`                                      | `motion`, `record`, `authorities`                                           | required in `motion`                          | disabled   |
| `rrd-rule12-city`                                 | `motion`, `record`, `authorities`                                           | required in `motion`                          | disabled   |
| `rrd-rule12-officers`                             | `motion`, `record`, `authorities`                                           | required in `motion`                          | disabled   |
| `section-1983-drafting`                           | `record`, `authorities`, `strategy`, `filing`                               | optional in `filing`                          | authorized |
| `studying-rule-59e-decisions`                     | `decisions`, `authorities`                                                  | optional in `decisions`                       | authorized |

The contract object MUST contain no additional fields. Every role listed by the
contract MUST appear exactly once and in order in the invocation. A required
target MUST be present in an allowed target role; an optional target MAY be
omitted for non-targeted behavior but MUST use an allowed role when present; a
`none` target policy MUST reject a target. A composed workflow MUST validate
each skill independently and MUST NOT union role, target, internet, or output
authority across skills.

#### Scenario: A quality-control-only skill omits its primary target

- **WHEN** a discovery-response or privilege-log audit invocation omits its
  required primary target
- **THEN** installed-skill validation reports `contract-target` before reading
  case material or publishing a report

### Requirement: Trusted host owns roots and persistence

The trusted host SHALL own absolute-root validation, logical input-manifest
construction, filesystem and network enforcement, and every call that starts,
writes, completes, or fails an output run. A skill or packaged helper MUST NOT
receive an output-root path, create a receipt, instantiate a persistence
manager, import repository-root validator or writer modules, or select an
alternate output location. The repository MUST NOT add a universal skill runner.

#### Scenario: Skill returns a generated artifact

- **WHEN** a skill produces a canonical output-relative path and deterministic
  bytes or stream
- **THEN** only the trusted host publishes that artifact through the shared
  append-immutable output boundary and terminal receipt

### Requirement: Standalone helpers are input-confined deterministic processors

Any executable helper required by a public skill SHALL ship inside that skill's
installable package. It MUST accept only a declared input-root descriptor plus
canonical relative target paths, or validated in-memory/standard-input data. It
MUST emit deterministic structured results or artifact bytes. It MUST reject
absolute paths, traversal, symlink escapes, undeclared roles, unsupported
entries, malformed bytes, and inputs beyond its documented bounds. It MUST NOT
perform arbitrary command dispatch, direct output publication, or receipt
creation.

#### Scenario: Skill package is copied without repository root

- **WHEN** a helper runs from the isolated copied skill package
- **THEN** it performs its documented deterministic processing without an
  import, executable, graph, repository, or persistence dependency outside the
  package and declared input data

### Requirement: Folder migration preserves approved legal behavior

The migration SHALL preserve every approved legal-analysis, drafting,
source-classification, authority, human-decision, non-mutation, finding-schema,
and provenance requirement. It SHALL NOT convert a mechanical check into legal
judgment or change a legal-behavior fixture merely to satisfy the folder
boundary.

#### Scenario: Existing legal fixture is rerun after migration

- **WHEN** the fixture does not depend on an obsolete runtime seam
- **THEN** its passing and regression outcomes remain unchanged

### Requirement: Migration verification proves effective confinement

Deterministic tests SHALL cover all 22 exact contracts, isolated package
installation, byte-for-byte recursive input non-mutation, output confinement,
exclusive append-only publication, undeclared-path denial, target confinement,
and network traps for internet-disabled skills. Tests SHALL reject direct helper
writes, repository-root imports, arbitrary checker commands, alternate output
paths, and obsolete current runtime requirements. Historical archived OpenSpec
changes are excluded from terminology rewrites.

#### Scenario: Disabled skill attempts network or undeclared access

- **WHEN** a test double attempts network use or a path outside declared roles
- **THEN** execution fails closed, input bytes remain unchanged, and no output
  artifact or success receipt is published
