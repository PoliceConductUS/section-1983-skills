# Brainstorm

## Design summary

The current complaint contract is compositionally unsafe. The umbrella package
owns the whole-document skeleton, the general complaint package owns the
detailed count contract, and the false-arrest specialization repeats both. A
partial installation can therefore omit half the contract, while a complete
installation gives an agent competing general owners to reconcile.

The approved design makes `drafting-section-1983-complaints` the only canonical
owner of the complete general complaint contract. Its install-local references
will contain the whole-document skeleton, detailed count contract, and a
machine-readable mechanical handoff. The umbrella will route and fail closed;
the false-arrest package will require the canonical owner and carry only
false-arrest deltas.

The reusable filing checker is a separate CaseGraph story. This repository
defines the instruction and checker handoff but does not implement structural
filing validation.

## Alternatives considered

### Keep the split and improve cross-references

This preserves fewer file moves, but an independently installed general
complaint package still lacks its own complete contract and a missing package
still fails silently. Cross-references cannot turn two owners into one owner.

### Let the false-arrest package own the complete contract

This gives false-arrest work one complete source, but promotes a specialization
to the owner of every Section 1983 complaint. General complaints would depend on
an irrelevant corpus-derived package, and future specializations would be
tempted to repeat the same pattern.

### Canonical general owner with routing and deltas

This approach matches the public skill boundaries. One general package owns the
complete contract; the umbrella chooses it; specializations add only their
issue-specific requirements. A machine-readable contract exposes the
deterministic subset without pretending to decide legal sufficiency.

## Agreed approach

- Put the complete whole-document and count contract in an install-local
  reference owned by `drafting-section-1983-complaints`.
- Add one install-local JSON contract for the deterministic mechanical subset.
- Turn the umbrella complaint reference into a routing and fail-closed entry.
- Reduce the false-arrest complaint reference to false-arrest-only deltas and
  require the general complaint skill first.
- Preserve `filing-ci` as thin project-configured orchestration. CaseGraph owns
  the executable checker in PoliceConductUS/casegraph#18.
- Test package structure and machine-readable behavior deterministically, then
  repeat the same fresh-agent pressure scenarios before and after the change.

## Key decisions

- Preserve the existing umbrella skeleton order as the canonical order: caption,
  optional introduction, jurisdiction and venue, parties, facts, counts, prayer,
  jury demand, and signature block.
- Require one count mapping per claim-defendant-capacity tuple.
- Treat presence, order, numbering, identifiers, paragraph references,
  incorporation targets, and required field locations as deterministic.
- Exclude truth, legal sufficiency, authority fit, material analogy, strategy,
  and filing readiness from deterministic checking.
- Fail closed when the canonical general complaint package or either canonical
  contract reference is unavailable.

## RED pressure controls

Three isolated current-state installations exercise the umbrella alone, the
general complaint package alone, and the complete false-arrest stack. Each fresh
agent must produce a source-traceable complete skeleton and count checklist
without inventing missing requirements or silently reconciling competing owners.

All three agents failed the requested complete-contract seam for a different
reason:

- The umbrella-only agent found the ordered skeleton but refused to invent the
  absent detailed count contract. It concluded that the installation did not
  expose one canonical complete owner or a stable checker interface. Output
  SHA-256: `5e88e1bbab3e7212825ecf36333f780a8eebe6e95242917f224058f2cd174a90`.
- The general-only agent found the detailed count contract but no authoritative
  whole-complaint skeleton. It identified the missing routing package rather
  than inventing section order. Output SHA-256:
  `65c05fb919c8a260edf0031b3de145c4a68e4baf7937213c95b4542db6f91f1b`.
- The full-stack agent found three competing general sources. It identified
  direct conflicts in jurisdiction/party order, jury-demand placement,
  signature-block completeness, count granularity, fair-warning triggers,
  authority verification, and duplicate count and Monell ownership. It concluded
  that no stable checker interface could be derived without an extra precedence
  rule. Output SHA-256:
  `6699b810be8797963e865bf31dbabee97dcfe67fe9c2a47034b062351a4507a8`.

These are shape and ownership failures, not discipline failures: the agents
correctly refused to invent or silently harmonize. The GREEN contract must give
them one positive recipe and one owner rather than add more prohibitions.

## Open questions

None. The user approved the ownership split, CaseGraph boundary, and test seam.

## GREEN pressure controls

The same isolated compositions were rerun after implementation.

- The umbrella-only agent reported **complaint contract unavailable**, named the
  missing general owner and both canonical references, and did not invent the
  skeleton or count contract. Preserved output SHA-256:
  `8cdb677067f37f4d19a584d4b9f641fb6a60c3638394eadf30c57bc9ed82a6f5`.
- The first general-only run exposed a real Markdown/JSON drift: the Markdown
  called Element a seventeenth record field although the approved JSON treats
  Element as a count function performed through the governing standard. A RED
  test now binds the human field identifiers to the sixteen machine fields. The
  corrected fresh-context run found one owner, one complete human contract, and
  one stable bounded mechanical handoff with no general-scope gap. Preserved
  verdict SHA-256:
  `dac72c5094960707ff2cfdca21e1414269aac159908592d73913931c1a64e4c9`.
- The first full-stack run exposed two live stale summaries: the umbrella
  reference index still called its complaint route a skeleton, and the general
  skill retained an obsolete Element -> Facts -> Inference -> Result sequence.
  RED tests now reject both. The corrected fresh-context run found one general
  owner, routing without fallback, universal governance without competing
  ownership, a specialization-only false-arrest construction delta, and the
  approved bounded general mechanical interface. Preserved verdict SHA-256:
  `a082a4f98fb3bc8d2f316a230a3cdb0042e66ec65b13afab0bf82970b4b1319a`.

The pressure review also proposed encoding false-arrest doctrine, Monell
sufficiency, authority quality, fair-warning analogy, and other legal branches
in the JSON. That proposal was rejected as outside the approved deterministic
boundary. Those judgments remain expressly excluded rather than being
misrepresented as mechanical checks.
