# Proposal: Monell Claim Contract Version 2

## Why

The complaint handoff can pass generic structural checks without recording the
defendant-specific individual-capacity, qualified-immunity, or path-specific
Monell analysis needed to test a Section 1983 claim.

## What changes

- Add separate public skills for Monell planning and approved-path drafting.
- Replace complaint contract version 1 with a strict typed version 2.
- Add a narrow install-local validator for the version-2 handoff.
- Permit optional read-only legal assessment from a valid CaseGraph stored on
  disk, without invoking a CaseGraph CLI.
- Require graph-used authority propositions to resolve to the verified opinion
  artifact, pinpoint, and exact matching passage rather than accepting a
  citation string alone.
- Give Filing CI distinct drafting and filing modes and explicit graph states.

## Capabilities

### New capabilities

- `planning-section-1983-monell-claims`
- `drafting-section-1983-monell-claims`

### Modified capabilities

- `drafting-section-1983-complaints`
- `filing-ci-orchestration`

## Impact

The change affects two new public skill packages, the canonical complaint
contract and validator, Filing CI instructions, governance provenance, package
routing, README guidance, and synthetic evaluation fixtures. It does not edit a
case filing, write to a CaseGraph, invoke a CaseGraph CLI, or decide litigation
strategy without the litigation principal.
