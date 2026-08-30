# Proposal: Harden proposition-level authority audits

## Why

An authentic authority and a correct citation do not prove that the cited source
supports every proposition attributed to it. Issue #78 requires the authority
audit to expose inverted holdings, source-voice mistakes, obsolete authority,
irrelevant citations, and partially supported compound statements instead of
allowing a citation-level pass to conceal them.

## What changes

- Require atomic decomposition of every material generated or filing-near
  statement before authority approval.
- Record correctness, groundedness, exact source support, source voice, scope,
  legal applicability, and verification provenance for each proposition.
- Define machine-readable and human-readable proposition-audit outputs without
  assigning legal judgment to deterministic software.
- Apply the same authority rule to the shared Section 1983 drafting protocol.
- Add six synthetic passing/regression fixtures for the named legal-RAG failure
  modes.

## Capability

- `verified-authority-audit`

## Non-goals

- No retrieval workflow, commercial-provider requirement, automated legal
  judgment, filing approval, source mutation, or litigation-strategy choice.
