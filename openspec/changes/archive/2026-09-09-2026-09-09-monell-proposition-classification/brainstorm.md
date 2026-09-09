## Design Summary

This is a bounded change to existing Monell planning, drafting, and validation
contracts. Planning owns three proposition classes and the staged-development
record for supported but incomplete paths. Drafting enforces proposition
placement and bars preservation by placeholder. The existing assertion-
validation skill remains the semantic reviewer for the integrated complaint and
checks that expected discovery has not become an existing fact.

## Alternatives Considered

### Alternative A: Add only a drafting reminder

- **Approach:** Put the approved paragraph in the Monell drafting reference.
- **Benefit:** Smallest textual change.
- **Cost:** Leaves planning records without a stable classification that the
  drafter can consume.
- **Why not selected:** The distinction should be made before drafting, not
  reconstructed during drafting.

### Alternative B: Planning owns classification and drafting owns placement

- **Approach:** Add the three classes to the planning record and enforce their
  complaint, brief, and discovery-plan placement in the drafting contract.
- **Benefit:** Gives each existing skill one bounded responsibility and reuses
  the shared assertion validator after integration.
- **Cost:** Requires coordinated edits and regressions in two skill packages.
- **Why selected:** It matches the repository's existing ownership boundaries
  without creating another skill or workflow.

### Alternative C: Add the broader staged-litigation strategy

- **Approach:** Also prescribe discovery sequencing and later amendment under
  Rules 15 and 16.
- **Benefit:** Could guide longer-term case strategy.
- **Cost:** Exceeds the approved paragraph rule and introduces case-dependent
  procedural judgments.
- **Why selected after extension:** The user subsequently approved the bounded
  staged-development strategy, including conditional discovery, diligence,
  deadline, and amendment gates while reserving claim and amendment decisions to
  the litigation principal.

## Agreed Approach

Use Alternatives B and C in sequence. Preserve the approved proposition rule,
then add only the staged-development records and gates the user approved.

## Key Decisions

- Planning owns proposition classification.
- Drafting owns complaint, brief, and discovery-plan placement.
- Expected-discovery propositions are not present facts or evidence.
- A supporting brief may explain an inference but may not cure a missing
  complaint-level factual basis.
- Presently supportable paths are pleaded narrowly; supported but incomplete
  paths remain internal with a complete staged-development record.
- Discovery is request-specific and conditional; it is not guaranteed by the
  survival of an individual claim.
- After a scheduling-order deadline, Rule 16 good cause is analyzed before Rule
  15, and the litigation principal decides whether to amend.

## Open Questions

None.
