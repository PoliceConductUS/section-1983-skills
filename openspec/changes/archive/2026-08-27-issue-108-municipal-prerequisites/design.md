## Context

The installed municipal-profile skill currently has one offline compilation
path. It correctly fails when its validated `policy-catalog` or
`policy-assessment` inputs are absent, but the failure does not tell a public
agent how to produce those inputs through the already installed policy skills.
Users must discover and sequence collection, review, analysis, and assessment
manually.

Those stages intentionally have different roles and network policies. Policy
collection may use bounded authorized internet; source review is independent;
analysis and assessment are offline; profile compilation has its own seven-role
contract. A public solution must make the sequence usable without collapsing
these least-privilege boundaries.

## Goals / Non-Goals

**Goals:**

- Make the municipal-profile skill the public entry point for resolving missing
  policy catalog and assessment prerequisites.
- Return a deterministic machine-readable state and actionable next stage.
- Route through existing installed skills under their unchanged folder,
  internet, output, and semantic boundaries.
- Resume only after trusted-host publication, terminal completion, validation,
  fingerprint binding, and any required independent review.
- Distinguish a structurally valid output containing substantive gaps from an
  invalid or stale output.

**Non-Goals:**

- Do not create a general workflow engine or make one invocation receive the
  union of every stage's folders.
- Do not self-approve collected policy sources or infer adoption, actor, event,
  phase, scope, evidence, authority, compliance, or liability.
- Do not change the semantic work or output artifacts of collection, analysis,
  assessment, or profile compilation.
- Do not resolve unrelated missing municipality, department, case-record, or
  verified-authority inputs beyond reporting them.

## Decisions

### Add a prerequisite-resolution operation to the existing skill

The skill will choose exactly one operation: prerequisite resolution or profile
compilation. Compilation retains its existing exact seven roles. Resolution uses
caller-supplied state about available validated folders, stage roles,
authorizations, approvals, and output-folder readiness; it never opens those
folders itself.

This keeps the public entry point discoverable without introducing a new skill
or broad filesystem contract.

### Add a deterministic domain planner

`municipal_profile_records.py` will expose a small planner that validates exact
state values and returns deterministic bytes for:

- `municipal-profile-prerequisites.yaml`; and
- `municipal-profile-prerequisites.md`.

The YAML record will contain the workflow version, current status, next
installed skill, exact required and missing roles, internet mode, output-folder
status, blocking reasons, and ordered postconditions. Status is one of:

- `input-required`;
- `authorization-required`;
- `review-required`;
- `ready-for-collection`;
- `ready-for-analysis`;
- `ready-for-assessment`;
- `ready-for-profile`; or
- `blocked-invalid`.

The planner proposes no command and opens no folder. The trusted host remains
responsible for validating and launching every invocation.

### Use a fixed precedence for next actions

1. Invalid or stale supplied catalog or assessment returns `blocked-invalid` and
   requires a fresh output folder for regeneration.
2. A valid catalog advances to assessment planning.
3. An absent catalog with approved sources advances to analysis planning.
4. Candidate but unapproved sources return `review-required`.
5. Absent sources require collection roles, bounded internet authority, and a
   collection output folder before returning `ready-for-collection`.
6. A valid catalog and valid assessment return `ready-for-profile` only if all
   existing compilation roles and a separate profile output folder are ready.

For each stage, missing roles take precedence over output-folder readiness;
missing internet or cost authorization takes precedence over collection
readiness. This produces one stable next action without hiding all missing
conditions from the plan.

### Preserve review and postcondition gates

Collection output is always candidate material and always pauses for an
independent `approved_for_analysis` review. A later analysis invocation requires
the reviewed adopted-policy source state already documented by its existing
contract.

Analysis and assessment output may contain gaps while remaining valid. The
planner requires the expected four ordinary artifacts, a terminal successful
receipt, `valid: true`, and matching input fingerprints. It does not require a
zero-gap result. Assessment preserves uncertain or indeterminate findings rather
than filling them.

Every transition to a later stage requires a new invocation that explicitly
declares the prior output folder as recursive read-only input and supplies a new
full absolute output folder. Network authority never transfers between stages.

### Keep implementation at the public skill seam

The change updates the installed skill, a focused prerequisite reference, README
routing, the deterministic domain helper, public-seam tests, and the durable
OpenSpec requirement. It adds no dependency, network client, credential
handling, repository operation, or persistence abstraction.

## Risks / Trade-offs

- **Risk: Users interpret orchestration as one privileged invocation** → State
  repeatedly that each stage is a new host-validated invocation under the owning
  skill's exact folder and network contract.
- **Risk: Candidate collection self-promotes into policy** → Make
  `review-required` mandatory after every collection output.
- **Risk: Gaps are confused with invalidity** → Separate validator/postcondition
  failure from a valid artifact that preserves substantive gaps.
- **Risk: Planner state drifts from skill guidance** → Test the helper, skill,
  reference, and README at the installed public seam.
- **Trade-off: Workflow may pause several times** → The pauses are the cost of
  explicit authorization, source review, and least-privilege folders; the plan
  makes each pause actionable.

## Migration Plan

1. Add RED tests for deterministic next-stage planning and installed guidance.
2. Add the planner and prerequisite reference without changing compilation.
3. Update the skill and README route.
4. Strictly validate, archive the OpenSpec delta, and run full repository
   validation.

Rollback removes the resolver helper/guidance and restores the prior compile-
only skill; existing profile compilation artifacts and contracts are unchanged.

## Open Questions

None.
