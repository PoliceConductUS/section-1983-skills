# explicit-skill-output-persistence Delta

## ADDED Requirements

### Requirement: Quality-control publication is one receipt-bound report

The trusted host MUST publish an independent quality-control result as exactly
one append-immutable report through the shared output writer. The report path
MUST contain the quality-control kind, UTC run time, and collision-resistant run
ID. Report bytes MUST identify the terminal run-manifest path that the same
output run will publish. The host MUST NOT report completion unless both the
report and terminal success manifest are durable and incomplete state is absent.

#### Scenario: Report write succeeds but terminal completion fails

- **WHEN** report bytes are published but the terminal success manifest cannot
  be completed durably
- **THEN** the quality-control run does not report completion and visible run
  state remains failed or incomplete

#### Scenario: A report name already exists

- **WHEN** a quality-control publication selects an existing report path
- **THEN** the writer preserves the existing bytes, rejects the collision, and
  the run cannot report successful completion
