## Design Summary

`building-municipal-monell-profiles` becomes the public entry point for a staged
municipal-profile workflow. Before compilation it performs a deterministic
prerequisite preflight. If the policy catalog or assessment is missing, it
returns machine-readable next-step artifacts and routes the agent through the
existing collection, analysis, and assessment skills as separate folder-scoped
invocations. It resumes compilation only after the trusted host publishes and
validates each required output and explicitly supplies that output folder as a
later read-only input.

The workflow remains fail-closed. Collection cannot approve its own sources;
analysis and assessment cannot inherit internet access; no stage can reuse an
output folder, mutate an input, invent missing semantic records, or bypass the
existing seven-role municipal-profile compilation contract.

## Alternatives Considered

### Alternative A: Collapse collection, analysis, assessment, and profiling

- **Approach**: Expand the municipal-profile invocation to receive every role,
  use the internet, and perform every semantic stage at once.
- **Advantages**: One apparent invocation and one terminal result.
- **Disadvantages**: Destroys the approved review boundary, mixes networked and
  offline operations, lets newly acquired material influence analysis before
  independent approval, and creates an oversized union filesystem capability.
- **Why not selected**: It conflicts with the folder-scoped public contract and
  the user's requirement that each invocation have an explicit output folder.

### Alternative B: Add prose-only troubleshooting guidance

- **Approach**: Tell users which other skills to run when compilation fails.
- **Advantages**: Minimal repository change.
- **Disadvantages**: Leaves agents free to skip stages, does not produce a
  stable machine-readable next action, and does not distinguish missing input,
  authorization, review, invalid output, or ready-to-continue states.
- **Why not selected**: It would improve the error message without making the
  public workflow reliably self-resolving.

### Alternative C: Deterministic prerequisite planner plus staged skill routing

- **Approach**: Add a domain-specific prerequisite planner and explicit
  orchestration instructions to the existing municipal-profile skill. The
  planner returns a bounded state and next invocation; the trusted host launches
  existing installed skills under their unchanged contracts.
- **Advantages**: Publicly usable, deterministic, testable, least privilege,
  review-aware, and compatible with existing skills and output-folder rules.
- **Disadvantages**: A multi-stage workflow can pause for source review or
  missing inputs and requires a fresh output folder for every stage.
- **Why selected**: It resolves everything that can safely be resolved while
  preserving the substantive approvals that must not be automated.

## Agreed Approach

Use Alternative C. Add a prerequisite-resolution operation to the installed
municipal-profile skill and a small deterministic helper that emits
`municipal-profile-prerequisites.yaml` and `municipal-profile-prerequisites.md`.
Keep profile compilation and every upstream skill invocation separate. The plan
names the exact next skill, required roles, internet mode, missing approval or
authorization, output-folder requirement, and postconditions for continuation.

## Key Decisions

- Current municipal-profile compilation keeps its exact seven read-only roles,
  disabled internet, and existing output artifacts.
- Prerequisite resolution is domain-specific orchestration, not a general
  workflow engine.
- The only automatically routed prerequisite chain is policy source collection
  when necessary, policy analysis, and policy assessment.
- Collection always stops at independent source review; it cannot mark its own
  candidates approved for analysis.
- Every stage requires a caller-supplied full absolute output folder and keeps
  temporary work beneath that stage's `temp/`.
- Later stages consume prior outputs only through a new invocation declaring
  that folder as read-only input.
- Valid outputs may preserve substantive gaps. A gap does not invalidate a
  structurally valid stage unless its validator or declared postcondition says
  the next stage cannot proceed.
- Missing unrelated municipality, department, case-record, or verified-
  authority inputs are reported precisely but are not acquired or invented by
  this change.

## Open Questions

None. The user delegated the public preconditions and postconditions and
approved the staged orchestration design.
