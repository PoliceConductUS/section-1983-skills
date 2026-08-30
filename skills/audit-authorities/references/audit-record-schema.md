# Authority-audit record contract

The normative machine-readable record is
[proposition-audit.schema.json](proposition-audit.schema.json). It records one
entry for every atomic proposition rather than one aggregate entry for a
citation or sentence.

## Independent legal-RAG supervision

A generation stage or material-revision stage cannot certify its own authority
work. Run a separate non-mutating `audit-authorities` invocation against the
exact immutable draft bytes and exact selected authority-source bytes. Declare
the draft folder as `filing-source`, authority folders as `verified-authority`,
and a new output folder distinct from the generation stage's output folder.
Changed input invalidates the prior result.

The record preserves both stage and invocation identities, optional model or
provider identity, exact role/path/SHA-256 input fingerprints, selected source
identities, UTC execution time, and distinct output-folder fingerprints. It
distinguishes successful independent execution, unavailable execution, malformed
output, unresolved source gaps, incorrect propositions, misgrounded
propositions, ungrounded propositions, and completed grounded propositions.
Generator self-review, a missing independent stage, reused output, changed
input, unavailable execution, malformed output, and unresolved or failed
propositions never pass.

`human_approval` is always `not-provided`. An AI-only audit is not human
approval and cannot make a filing decision. Credentials, tokens, provider
continuation state, conversation IDs, and session IDs are prohibited.

## Required proposition results

- `correctness`: `verified`, `incorrect`, or `unresolved`.
- `groundedness`: `grounded`, `misgrounded`, or `ungrounded` only when
  correctness is `verified`; otherwise `not-applicable`.
- `source_support`: every asserted source mapped to the exact selected artifact,
  SHA-256, authority and source YAML, pinpoint, source text, scope and
  qualifiers, jurisdiction, decision date, posture, precedential force, source
  voice, and support status.
- `verification_provenance`: the audit stage, exact input fingerprints, selected
  source identities, execution time, and model or provider when available.

Source voice is `majority-holding`, `court-dicta`, `party-argument`,
`lower-court-ruling-under-review`, `factual-or-procedural-background`,
`concurrence`, `dissent`, or `quoted-secondary-authority`. In the human report,
render those values as majority holding, court dicta, party argument,
lower-court ruling under review, factual or procedural background, concurrence,
dissent, and quoted secondary authority.

## Human-readable report

Render these headings in order:

1. `# Proposition authority audit`
2. `## Scope and provenance`
3. one `## <proposition_id>` section for every proposition in filing order
4. `## Unresolved and failed propositions`
5. `## Overall result`

Each proposition section states the exact proposition and filing location,
correctness, groundedness, exact source mapping, source voice, support status,
scope and qualifiers, legal applicability fields, verification provenance, and
any advisory remediation. No aggregate pass may conceal a proposition-level
failure. A real citation, working link, source list, snippet, or positive
treatment symbol is not source support.

JSON-schema conformance validates shape and vocabulary only. It does not decide
correctness, groundedness, source voice, applicability, litigation strategy, or
filing readiness.

Historical benchmark results must identify the provider, product, version,
dates, query distribution, sample size, complete query provenance, and
limitations. Never represent a prior result as a current vendor reliability
rate. Optional live-provider work remains separate from the deterministic
synthetic corpus.
