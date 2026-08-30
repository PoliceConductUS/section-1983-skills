# repository-skill-governance Specification

## Purpose

Define repository-wide controls for user-reserved legal judgment,
jurisdiction-specific propositions, rules provenance, protected contribution
gates, tool ownership, and non-mutating independent quality-control stages.

## Requirements

### Requirement: User-reserved litigation judgment

Public skills MUST reserve litigation strategy, positions, concessions,
requested relief, filing, and other material legal choices to the user. When a
skill can support multiple material paths, it SHALL state the supported choices
and consequences, select none, and identify the user decision required.

#### Scenario: Multiple supported litigation paths

- **WHEN** a skill encounters a material choice among supported litigation paths
- **THEN** it presents the supported choices and consequences, identifies the
  user decision required, and does not choose a path

#### Scenario: User has supplied a decision

- **WHEN** the user expressly selects a supported path
- **THEN** the skill may apply that decision without enlarging it or silently
  deciding a different material choice

### Requirement: Jurisdiction-specific proposition confinement

A current jurisdiction-specific legal proposition MUST appear only in a verified
reference that identifies its jurisdiction, authoritative source provenance, and
checked date. This includes a deadline, limit, local rule, standing-order
requirement, judge requirement, or judge-specific legal proposition. A public
SKILL file SHALL route to that reference and preserve source gates without
restating the proposition.

#### Scenario: Maintainer adds a local requirement

- **WHEN** a maintainer adds a current district or judge requirement
- **THEN** the proposition is placed in a jurisdiction reference with the
  jurisdiction, authoritative source, and checked date rather than in SKILL
  workflow prose

#### Scenario: Jurisdiction source is unavailable or stale

- **WHEN** the required jurisdiction reference is unavailable or its currency
  cannot be established
- **THEN** the skill reports the source gap and does not supply the proposition
  from memory or a generic substitute

### Requirement: Complete rules-freshness registry

The repository MUST maintain a public machine-readable registry containing
exactly one classification for every public skill. Each entry SHALL have a
nonempty rationale and ISO review date. A bundled-rules-dependent entry MUST
identify authoritative source records with HTTPS provenance URLs and concrete
checked dates. A runtime-sourced entry MUST define that the skill's returned
artifact exposes the actual approved source identity and checked date used.

#### Scenario: New public skill is unclassified

- **WHEN** a public `skills/*/SKILL.md` exists without a matching registry entry
- **THEN** repository validation fails before the change is accepted

#### Scenario: Rules-dependent entry lacks provenance

- **WHEN** a bundled-rules-dependent skill has no authoritative source ID, URL,
  or checked date
- **THEN** repository validation fails with the incomplete entry identified

#### Scenario: Runtime-sourced skill completes work

- **WHEN** a runtime-sourced skill applies an approved rule or order source
- **THEN** its returned artifact exposes the stable source identity and the date
  that source was checked

### Requirement: Protected legal-gate review

Contribution guidance MUST identify verification, factual and authority source,
permission, filing-readiness, judgment-routing, rules-provenance, and
tool-ownership gates as protected. A contribution that weakens or bypasses one
of those gates SHALL require explicit human review that names the affected gate
and rationale.

#### Scenario: Pull request changes a protected gate

- **WHEN** a contribution weakens, bypasses, removes, or changes a protected
  gate
- **THEN** the contribution identifies the affected gate and rationale and
  requests explicit review before acceptance

#### Scenario: Review prompt is removed

- **WHEN** repository contribution surfaces no longer require protected-gate
  review
- **THEN** repository validation fails

### Requirement: Thin skill-wrapper ownership boundary

The repository MUST retain only public skill instructions and
repository-specific validation or evaluation support. General-purpose executable
rule retrieval, citation verification, evidence processing, filing inspection,
or other reusable tooling SHALL belong in its owning repository, with only a
thin skill wrapper here when needed.

#### Scenario: Contribution proposes reusable executable tooling

- **WHEN** a contribution's executable behavior is general-purpose rather than
  specific to validating or evaluating this repository
- **THEN** maintainers route it to an owning repository and keep at most the
  public thin skill wrapper in this repository

### Requirement: Governance validation is repository-specific and fail-closed

Repository validation MUST deterministically compare public skill directories
with the rules registry and validate governance policy and contribution-review
surfaces. It SHALL use no network retrieval and MUST fail on malformed JSON,
duplicate or unknown skill entries, invalid modes or dates, unknown source IDs,
insecure or malformed provenance, or missing protected policy language.

#### Scenario: Valid governance state

- **WHEN** all public skills are classified and all required policy, provenance,
  and review data is valid
- **THEN** governance validation exits successfully without network access

#### Scenario: Invalid governance state

- **WHEN** any required governance invariant is absent or malformed
- **THEN** governance validation exits nonzero and identifies the violated
  invariant

### Requirement: Durable contributor workflow

The contribution guide MUST require one story per stacked branch, RED/GREEN TDD,
OpenSpec design/tasks/verification/retrospective artifacts, archive of the
completed change, refactoring only while tests remain green, and the complete
repository validation gate before release.

#### Scenario: Contributor begins a story

- **WHEN** a contributor starts one backlog story
- **THEN** the contributor uses one stacked branch, writes the failing test
  before implementation, completes the OpenSpec cycle, and runs the full gate

### Requirement: Human-controlled legal judgment

The contribution guide MUST preserve the existing protected-gates authority and
state that automation does not silently select plaintiff decisions, litigation
strategy, or legal conclusions.

#### Scenario: Automation encounters a protected choice

- **WHEN** a contribution could automate a material legal choice
- **THEN** it routes the choice through the existing governance authority and
  leaves the selection to the human

### Requirement: Measurement remains feedback

The contribution guide MUST state that measurement is feedback, never a verdict.
Score deltas and judgment-based evaluations SHALL reveal change or prompt review
and MUST NOT decide legal quality, filing readiness, or human judgment.

#### Scenario: Evaluation score changes

- **WHEN** a score or judgment-based evaluation changes
- **THEN** the contributor investigates the signal without treating it as a
  verdict

### Requirement: Self-documenting code and bounded comments

The contribution guide MUST require self-documenting code and refactoring before
adding a comment. A necessary comment SHALL be short and clear and SHOULD
reference an ADR or recorded decision when practical.

#### Scenario: Code appears to need an explanatory comment

- **WHEN** clearer names or structure can express the reason
- **THEN** the contributor refactors instead of adding the comment

### Requirement: Immutable release contribution

The contribution guide MUST link the existing release authority, state that a
push to `main` is not publication, and require immutable semantic-version tags
after complete validation.

#### Scenario: Contributor finishes a branch

- **WHEN** the contribution is complete and green
- **THEN** it remains unreleased until the existing tagged-release process
  validates and publishes the integrated commit

### Requirement: Confined owner links without policy duplication

The contribution guide MUST use confined relative links to the existing
governance and publishing owners. Both destinations SHALL resolve inside the
repository. The guide MUST NOT copy the protected-gates registry, release
workflow command, or owner section as a parallel policy.

#### Scenario: Contributor consults an owner policy

- **WHEN** the contribution guide routes a protected-gate or release question
- **THEN** its relative link resolves to the existing owner and the guide does
  not embed a parallel registry or release procedure

### Requirement: Deterministic contribution validation

Repository governance validation MUST fail when the contribution contract or its
owner links are missing or semantically inverted. The validator MUST check only
deterministic documentation and workflow boundaries and MUST NOT score
subjective prose, comment, test, or legal quality.

#### Scenario: Contribution contract omits a protected workflow rule

- **WHEN** a required deterministic rule is absent or inverted
- **THEN** repository governance validation fails with a stable contribution
  contract finding

### Requirement: Independent quality-control stages are non-mutating

Independent quality-control stages MUST be non-mutating. This includes every
independent audit, verification, review, evaluation, Filing CI run, or
behaviorally equivalent quality-control stage. The stage MAY read designated
artifacts and write its designated report or result. It MUST NOT edit,
overwrite, correct, regenerate, or otherwise modify an artifact under review.

#### Scenario: Combined audit-and-fix request

- **WHEN** a user asks an independent quality-control stage to audit and fix the
  same artifact
- **THEN** the stage preserves the artifact bytes, writes only its report or
  result, and does not treat the combined instruction as remediation authority

#### Scenario: Pressure conflicts with the quality-control boundary

- **WHEN** deadline pressure, sunk cost, claimed prior approval, or a contrary
  workflow instruction directs the independent stage to mutate the artifact
- **THEN** the quality-control boundary controls and the artifact remains
  unchanged

### Requirement: Quality-control recommendations are advisory

Quality-control output MUST remain advisory. Recommendations, proposed language,
corrections, and copy-ready replacements from an independent quality-control
stage MUST NOT authorize implementation.

#### Scenario: Report supplies copy-ready replacement text

- **WHEN** an independent report contains complete replacement language
- **THEN** the reviewed artifact remains unchanged until a separately authorized
  drafting or revision stage applies a selected correction

### Requirement: Remediation and re-verification are separate stages

Remediation MUST occur in a separately authorized drafting or revision stage and
MUST create a new version when repository or project versioning applies. A new
read-only quality-control stage MUST verify the remediated artifact.

#### Scenario: User authorizes remediation after review

- **WHEN** a user separately authorizes a supported correction
- **THEN** the drafting stage creates the applicable new version and a later
  independent quality-control stage assesses that version without modifying it

### Requirement: Authorized drafting self-checks remain distinct

Authorized drafting self-checks MUST remain distinct from independent quality
control. An internal self-check inside an explicitly authorized drafting or
revision stage MAY guide edits within that stage. It MUST NOT be represented as
an independent audit, verification, review, evaluation, or quality-control
result.

#### Scenario: Drafter checks its work while revising

- **WHEN** an authorized drafting stage performs an internal completion check
- **THEN** it may use the result to revise the working artifact but does not
  label that self-check as an independent quality-control stage

### Requirement: Independently installable quality-control contract

Each affected public skill MUST carry the compact contract within its own
installable package. An affected skill is one whose trigger permits an
independent quality-control stage. The compact contract covers non-mutation,
advisory output, separate remediation, versioning, and fresh verification.

#### Scenario: Quality-control skill is installed alone

- **WHEN** an agent loads the skill without repository-root governance files
- **THEN** the skill still prohibits same-stage artifact mutation and routes
  remediation and re-verification to separate stages

### Requirement: Deterministic quality-control contract validation

Repository governance validation MUST identify current public quality-control
entrypoints from their trigger language and fail with a stable skill-specific
finding when the compact contract is absent or inverted. Deterministic
validation MUST NOT claim to prove agent behavior or evaluate subjective prose
quality.

#### Scenario: Audit-capable skill permits same-stage correction

- **WHEN** an affected public skill omits the contract or permits an independent
  audit to edit the reviewed artifact
- **THEN** repository governance validation exits nonzero and identifies the
  affected skill through the stable quality-control contract finding

### Requirement: Quality-control reports are immutable

Each report MUST use a unique filename containing the stable check kind, UTC
timestamp, and run ID. Report creation MUST be exclusive. A quality-control run
MUST NOT edit, overwrite, replace, rename, or delete an existing report.

#### Scenario: Selected report path already exists

- **WHEN** a quality-control run resolves a report path that already exists
- **THEN** it fails closed and preserves the existing report bytes

### Requirement: Generated reports are excluded by default

Prior quality-control reports MUST NOT become implicit input. A report MAY be
reviewed only when that exact report is expressly present in a declared input
role and selected consistently with the reviewing skill's target policy. The
reviewing stage MUST propose a different new append-immutable report for trusted
host publication.

#### Scenario: An output folder contains earlier reports

- **WHEN** a later quality-control run begins
- **THEN** those outputs remain unavailable as input unless the caller declares
  them under an authorized input role in a separate invocation

### Requirement: Reports identify their evidence and result

Each report MUST identify the audited version, artifact paths and fingerprints,
quality-control kind, UTC run time, run ID, scope, approved source identities,
and result. It MUST separate failed findings from passing-but-suboptimal
observations.

#### Scenario: A filing passes with an improvement opportunity

- **WHEN** a reviewed artifact passes but a supported improvement exists
- **THEN** the report preserves the passing result and records the improvement
  separately as a non-authorizing observation

### Requirement: Report recommendations remain advisory

A report MUST treat any included remediation recommendations, proposed language,
and copy-ready replacements for failures or passing-but-suboptimal observations
as advisory. Those items MUST NOT authorize implementation. A separately
authorized drafting or revision stage applies any selected change, and a fresh
read-only stage verifies the new version.

#### Scenario: Report contains a copy-ready correction

- **WHEN** a quality-control report supplies complete replacement language
- **THEN** the reviewed version and all prior reports remain unchanged until a
  separately authorized remediation stage creates the applicable new version

### Requirement: Install-local report contract

Every public skill whose trigger permits independent quality control MUST carry
the compact non-mutation, target, append-immutable report, input exclusion,
content, receipt, and advisory-remediation contract in its independently
installable package. It MUST identify its exact
`references/folder-contract.json` without copying the full shared persistence
protocol.

#### Scenario: Quality-control skill is installed alone

- **WHEN** an agent loads one affected skill without root governance files
- **THEN** the package still selects only a declared target, returns one new
  output-relative report, preserves every input and prior output, and leaves
  publication to the trusted host

### Requirement: Deterministic report-contract validation

Repository governance validation MUST apply the behavioral quality-control
classifier and MUST fail with a stable root- or skill-specific finding when the
explicit-output immutable report contract is missing or inverted. It MUST reject
project-boundary, version-folder, implicit `audits/`, fallback output, direct
helper write, and overwrite permissions in current public contracts.

#### Scenario: Skill permits project-shaped or direct output

- **WHEN** an affected skill permits a report outside the trusted host's
  caller-declared output boundary or permits replacement of an existing report
- **THEN** governance validation exits nonzero and identifies the affected skill

### Requirement: Independently installable folder boundary

Every public `SKILL.md` MUST link to a schema-valid install-local
`references/folder-contract.json` that states the exact ordered input roles,
target policy and roles, allowed internet policy or policies, and declared
output mode. A multi-operation skill MAY map each operation name to its exact
internet policy, while each invocation MUST choose one known operation and its
matching policy. The skill MUST also carry the compact recursive
input-read-only, output-only, internet, and host-enforcement boundary. The full
protocol SHALL remain in the repository's canonical execution owner and MUST NOT
be copied into every skill.

#### Scenario: Skill is installed alone

- **WHEN** an agent loads one public skill without repository-root governance
  files
- **THEN** the package still exposes its complete exact invocation authority and
  preserves the compact enforcement boundary

### Requirement: Deterministic folder-contract validation

Repository governance validation MUST inspect every public skill package and
fail with a stable skill-specific finding when its folder contract is missing,
unreadable, malformed, noncanonical, mismatched to the public skill name, or
different from the approved role/target/internet/output matrix. Deterministic
validation MUST NOT claim to prove host isolation or subjective agent behavior.

#### Scenario: Public skill changes one role or policy

- **WHEN** a public contract adds, removes, duplicates, reorders, or renames a
  role or changes its target, internet, or output policy
- **THEN** repository validation exits nonzero and identifies that skill before
  any invocation uses the broadened authority

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

### Requirement: Quality-control reports use explicit output

An independent quality-control stage MUST select exactly one artifact through
its declared input roles and target policy and MUST propose exactly one unique
append-immutable output-relative report beneath the caller-declared output
folder. A missing, ambiguous, nonexistent, or out-of-role target MUST fail
closed without a fallback write. The report path MUST reject absolute paths,
traversal, symlink escapes, and existing destinations. Only the trusted host MAY
publish the report through the shared output boundary.

#### Scenario: Quality-control target is unresolved

- **WHEN** a quality-control run has no single valid target required by its
  install-local folder contract
- **THEN** it reports output unavailability and the trusted host publishes no
  completed report

#### Scenario: Proposed report escapes output

- **WHEN** a helper returns an absolute, traversing, escaping, or colliding
  output-relative report path
- **THEN** publication fails closed and every existing input and output byte is
  preserved

### Requirement: Standalone helper ownership is deterministic

Repository governance validation MUST identify every helper named by a public
folder contract and verify that the file exists inside that skill package. A
helper MUST NOT import repository-root validator/writer modules, accept an
output-root argument, perform arbitrary command dispatch, or directly create an
output artifact or receipt.

#### Scenario: Installed helper depends on repository root

- **WHEN** a helper imports or references a required executable outside its
  isolated skill package
- **THEN** governance validation fails with a stable skill-specific helper
  ownership finding

### Requirement: Every quality-control invocation has one primary target

Every public quality-control skill MUST require exactly one primary target
within its approved declared input roles. This applies when its trigger permits
an independent audit, validation, verification, review, evaluation, Filing CI
run, or behaviorally equivalent quality-control stage. Missing, ambiguous,
directory, or out-of-role targets MUST fail closed.

#### Scenario: A QC-capable drafting skill is invoked without a filing target

- **WHEN** an invocation selects the independent quality-control behavior but
  supplies no primary target
- **THEN** the quality-control stage publishes no report and does not choose a
  target from the input tree

#### Scenario: The host receives only a generic validated invocation

- **WHEN** a quality-control publisher receives an invocation that was not bound
  to the installed skill's target policy and approved target roles
- **THEN** it publishes no report and fails closed

### Requirement: Quality-control report metadata is complete and receipt-bound

Every independent quality-control report MUST record the skill and version,
quality-control kind, UTC run time, run ID, filtered logical input roles and
reviewed artifact hashes, primary target role/path/hash/size, scope, result,
failed findings, passing-but-suboptimal recommendations, and the terminal
run-manifest identity. Findings and recommendations remain advisory and MUST NOT
authorize same-stage remediation.

#### Scenario: A passing run has a supported improvement

- **WHEN** a quality-control run passes but identifies a suboptimal choice
- **THEN** its report preserves the passing result, records the recommendation
  separately, and leaves the target bytes unchanged

### Requirement: Generated QC reports are excluded from reviewed fingerprints

The trusted host MUST exclude files beneath the reserved
`quality-control-reports/` output prefix and files identified by the canonical
quality-control metadata envelope from a quality-control run's reviewed-input
manifest unless one exact report is itself the explicit primary target.
Selecting one report MUST NOT implicitly include sibling or older reports.

#### Scenario: A prior report folder is declared as an input role

- **WHEN** a later quality-control invocation targets an ordinary artifact
- **THEN** prior generated reports do not contribute to the reviewed-input
  manifest or its fingerprint

#### Scenario: The declared input role is the report directory itself

- **WHEN** generated report relative paths omit the reserved prefix because the
  declared role is rooted directly at `quality-control-reports/`
- **THEN** the canonical metadata envelope still identifies and excludes every
  non-target generated report

#### Scenario: One prior report is the primary target

- **WHEN** the caller expressly selects one report beneath the reserved prefix
- **THEN** that report alone remains in the reviewed-input manifest and other
  generated reports remain excluded

### Requirement: Installed QC packages carry the shared report contract

Every behaviorally detected QC skill MUST carry the compact target, metadata,
report-exclusion, immutable publication, receipt-success, and advisory-only
remediation contract in its independently installable package. Deterministic
governance validation MUST fail with a stable skill-specific finding when that
contract is missing or inverted.

#### Scenario: A QC skill omits run-manifest identity

- **WHEN** an independently installed QC skill no longer requires its report to
  identify the terminal run manifest
- **THEN** repository validation exits nonzero and identifies that skill

### Requirement: Public filing workflows use ordinary folders

Public filing-generation and quality-control skills MUST describe ordinary files
under declared recursive read-only folder authority. A one-file task MUST
identify the declared input role and folder-relative path. A whole-folder task
MUST expressly identify the ordinary files in scope and MUST NOT infer
membership from a folder-wide manifest, loader, registry, or shared folder
object. Skills MUST preserve input immutability, trusted-host publication,
explicit targets, exact output-folder writes, and exclusive temporary use of
`<output-folder>/temp/`.

#### Scenario: A public skill reviews one filing

- **WHEN** the caller selects one role-relative filing target
- **THEN** the skill reviews only that ordinary file and does not silently treat
  the result as coverage of sibling files

#### Scenario: A current public filing skill is installed independently

- **WHEN** any currently published skill that drafts or reviews a filing is
  copied without the repository around it
- **THEN** its entrypoint retains the ordinary filing-folder boundary without a
  repository-local persistence helper

### Requirement: Public data workflows use source-documented folders

The repository MUST document that profile, overlay, and research data consists
of ordinary files selected from declared recursive read-only input folders.
Public skills that produce or consume that data MUST link to install-local
source-documented-folder guidance, retain their domain-specific validation, and
MUST NOT convert participant data into generated skills, static-role changes,
ambient filesystem authority, or mutable input access. Domain-owned YAML source
records MUST preserve applicable folder-relative paths, hashes, provenance,
dates, classifications, validation state, assumptions, and gaps without a
generic root envelope.

#### Scenario: An overlay skill is installed independently

- **WHEN** a current counsel or litigation-alignment skill is copied without the
  repository around it
- **THEN** its installed skill retains the source-documented-folder boundary and
  its domain-specific validator

### Requirement: Participant profiles remain data rather than skills

The repository MUST keep judge-, attorney-, team-, court-, source-class-, and
assumption-specific information in ordinary files within declared read-only
input folders. It MUST NOT publish real-participant skills, generate
person-specific skills, or permit profile data to alter protected installed
behavior.

#### Scenario: Maintainer adds a new participant profile

- **WHEN** the profile is intended for an agent simulating that participant's
  litigation role
- **THEN** the maintainer adds or regenerates validated profile files and
  domain-owned YAML source records while reusable behavior remains unchanged
