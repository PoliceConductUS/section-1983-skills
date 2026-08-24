# explicit-skill-output-persistence Delta Specification

## ADDED Requirements

### Requirement: Only the trusted host publishes helper results

Standalone skill helpers SHALL return deterministic output-relative artifact
paths, bytes or streams, and validated source metadata to the trusted host. They
MUST NOT open the output root, stage artifacts, create run-state files, or call
the output writer. The trusted host MUST validate every returned path and source
record and SHALL remain the sole caller of output-run start, write, complete,
and fail operations.

#### Scenario: Helper returns report bytes

- **WHEN** a packaged checker returns one report path and complete report bytes
- **THEN** the trusted host publishes them append-immutably and derives the
  terminal artifact and internet status from the accepted write
