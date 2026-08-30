## Why

The Issue #102 gate can collapse four different identity dates and can remain
inactive for an unresolved intended individual defendant unless someone has
already raised limitations. Its current evaluation proves instructions and
synthetic candidate handling, but an actual complaint handoff may still omit a
limitations record while deterministic checks pass. The correction must preserve
the factual timeline and enforce record structure without automating litigation
judgment.

## What Changes

**Trigger and identity timeline**

- From: A passed deadline or expressly raised risk triggers the gate, and one
  knowable-date field records identity timing.
- To: Any unresolved intended individual defendant triggers the gate, and
  availability, possession, objective ascertainability, and actual
  identification are separate sourced events.
- Reason: The current trigger and field can omit a live Doe risk or imply facts
  the record does not establish.
- Impact: New complaint handoffs must declare intended-individual trigger data.

**Defendant-specific completion record**

- From: Pre-limitations diligence, combined notice/service, and general
  concealment or tolling entries.
- To: Three diligence stages; record-control and withholding provenance;
  separate notice, service, and Rule 4(m) sections; actor-specific attribution;
  and authority-route records with jurisdiction, pinpoint, status, proposition,
  application, and unresolved state.
- Reason: The omitted distinctions perform different factual and procedural
  jobs.
- Impact: Affected defendant records become more explicit and auditable.

**Structural enforcement**

- From: Guidance and a synthetic candidate evaluator do not require an actual
  limitations record at the installed checker seam.
- To: A machine-readable schema and aligned native validators make missing,
  malformed, or unresolved limitations material a hard finding in the complaint
  checker and Filing CI.
- Reason: Filing readiness must fail closed when the required artifact is not
  present.
- Impact: Installed checker contracts, fixtures, and focused evaluations change
  together; legal sufficiency remains excluded.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drafting-section-1983-complaints`: Strengthen the gate, per-defendant record,
  behavioral verification, and mechanical handoff requirements.
- `deterministic-filing-integrity`: Require Filing CI to preserve the complaint
  checker's limitations-record hard findings without deciding legal sufficiency.

## Impact

The change affects the canonical complaint contract and completion audit, the
complaint mechanical handoff and installed checker, Filing CI's aligned contract
and checker implementation, focused fixtures, and OpenSpec verification. It adds
no dependency, graph, repository abstraction, ambient filesystem access, or
automated litigation decision.
