## Design Summary

Issue #102 correctly added a defendant-specific limitations gate, but its single
knowable-date field can collapse source availability, possession, objective
ascertainability, and actual identification. Its trigger can also miss an
unresolved intended individual defendant unless someone has already raised
limitations. The approved correction separates those facts, expands the
defendant-specific record, and adds deterministic structural enforcement at the
existing complaint-checker seam while reserving legal judgment to the agent and
user.

## Alternatives Considered

### Alternative A: Guidance and synthetic fixtures only

- **Approach:** Expand the Markdown contract and the existing candidate-record
  evaluator without changing the installed checker.
- **Advantages:** Smallest change and no new handoff fields.
- **Disadvantages:** An actual complaint handoff can still omit the limitations
  record while deterministic checks pass.
- **Why not selected:** It repeats the enforcement weakness that prompted this
  corrective issue.

### Alternative B: Let Filing CI decide limitations sufficiency

- **Approach:** Teach Filing CI to decide relation back, tolling, mistake,
  notice, diligence, and authority fit.
- **Advantages:** One apparent filing-readiness verdict.
- **Disadvantages:** Converts disputed legal judgment into brittle automation,
  exceeds the checker boundary, and intrudes on reserved litigation decisions.
- **Why not selected:** The repository may enforce structure and unresolved
  status, but it must not automate litigation judgment.

### Alternative C: One schema-backed limitations gate in the complaint handoff

- **Approach:** Add a required `limitations_gate` object to the existing
  complaint mechanical handoff. Intended-individual entries provide observable
  trigger facts; one schema-backed record is required for each affected entry.
  The installed complaint checker and Filing CI validate the same shape and fail
  closed on missing, malformed, or unresolved material.
- **Advantages:** Enforces the artifact at the public seam, remains
  deterministic and folder-scoped, and preserves the legal-judgment boundary.
- **Disadvantages:** The installed checker contracts and fixtures must migrate
  together, and the two independently installable skills retain aligned copies
  of the contract.

## Agreed Approach

Use Alternative C. The handoff will carry intended-individual identity status,
amendment action, deadline status, and a risk-raised flag. The checker will
derive affected defendants without scanning prose or inventing a day-count
threshold. Each affected defendant must have a complete record with separate
identity events, diligence stages, record-control provenance, notice, service,
Rule 4(m), authority-route, attribution, fallback, and gap data.

The checker will validate only cardinality, field shape, supported vocabularies,
ISO dates, source-reference presence, and fail-closed status. It will not decide
whether relation back, tolling, mistake, notice, service, authority application,
or requested relief succeeds.

## Key Decisions

- The complaint handoff, not a new persistence layer, owns the limitations
  record presented to mechanical checking.
- The gate activates for an intended individual who is unnamed, role-only,
  misnamed, or not serviceable even when no one expressly raises limitations.
- An unidentified witness who is not an intended defendant does not activate the
  gate.
- Availability, possession, objective ascertainability, and actual
  identification are independent events and never imply one another.
- Diligence is divided into pre-limitations, post-filing/pre-identification, and
  post-identification/pre-service stages.
- Notice, service, and Rule 4(m) relief are separate record sections.
- Municipal, custodian, and individual attribution are recorded separately.
- A supported adverse fact may be structurally complete; deterministic checking
  does not turn it into a legal conclusion. Missing or unresolved material is a
  hard filing-critical finding.

## Open Questions

None.
