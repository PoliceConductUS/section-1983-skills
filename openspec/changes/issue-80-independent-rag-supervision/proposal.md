# Proposal: Require independent legal-RAG supervision

## Why

A drafting or research stage cannot establish the fidelity of its own authority
work. Issue #80 requires a separate audit over immutable filing and authority
bytes, explicit stage provenance, fail-closed supervision outcomes, and a
permanent synthetic legal-RAG regression corpus.

## What changes

- Require a separate non-mutating `audit-authorities` invocation for filing-near
  legal propositions.
- Bind generation and audit stages to exact ordinary-file fingerprints and
  distinct output folders without introducing a package or workspace model.
- Record stage, invocation, model or provider when available, selected source
  identities, execution time, and bounded supervision outcomes.
- Make AI-only audit records incapable of representing human approval.
- Add a versioned, deterministic, network-independent YAML regression corpus
  covering the complete Issue #80 failure taxonomy.
- Add governance tests for self-review, changed inputs, missing audit stages,
  missing human-reserved boundaries, and incomplete corpus taxonomies.

## Capability

- `verified-authority-audit`

## Non-goals

- No automated litigation strategy, filing approval, live commercial-provider
  dependency, vendor-reliability claim, package, graph, CaseGraph, repository,
  Git, datastore, or ambient workspace.
