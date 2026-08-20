# Proposal: Section 1983 Discovery Skill Suite

## Why

The repository identifies pleading and filing gaps but has no coordinated,
traceable workflow for drafting discovery, auditing responses, conferring over
deficiencies, determining privilege-log requirements, auditing supplied logs, or
preparing depositions. Issue #8 requires those responsibilities to be decomposed
before implementation so every public skill can be independently tested and
cannot silently assume evidence or make litigation choices for the user.

## What changes

- Add five separately discoverable and tested public discovery skills.
- Add a consolidated Discovery Target Map reference under the existing drafting
  entrypoint and route each peer skill from that entrypoint and README.
- Require claim-, defendant-, element-, gap-, custodian-, and native-source
  traceability with approved source IDs and bounded proportional scope.
- Distinguish requests about existence or identification from assertions about
  unverified content.
- Reserve service, narrowing, escalation, waiver, sanctions, deposition, and
  other material strategy choices to the plaintiff.
- Add one synthetic behavioral regression per skill, structural mapping tests,
  and fresh bounded behavior checks.

## Capabilities

### New capabilities

- `drafting-section-1983-written-discovery`: Draft mapped and bounded requests
  for production, interrogatories, and requests for admission.
- `auditing-section-1983-discovery-responses`: Audit discovery responses,
  objections, production, withholding, and concrete cure by request.
- `drafting-section-1983-meet-and-confer`: Draft neutral request-specific
  deficiency and cure correspondence from a completed audit.
- `auditing-section-1983-privilege-logs`: Determine approved privilege-log
  requirements and audit supplied logs without exposing substance or
  adjudicating privilege.
- `drafting-section-1983-deposition-outlines`: Build chronology- and element-
  gap-driven deposition outlines with traceable sources and no scripted
  testimony.

### Modified capabilities

None.

## Impact

The change adds five skill directories with OpenAI metadata, one coordination
reference under the existing drafting skill, README and routing text, focused
standard-library tests, and five generic synthetic fixtures. It adds no external
dependency, private case fact, provider integration, automatic service, filing,
correspondence, motion, or strategy decision.
