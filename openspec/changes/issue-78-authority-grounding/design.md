# Design: Proposition-level correctness and groundedness

## Audit unit

The unit of approval is one atomic material proposition, not a sentence,
paragraph, citation, or source list. A compound statement is split until each
proposition can receive its own correctness and groundedness result. Reusing one
authority is allowed only when the exact source supports every proposition in
the asserted context.

## Status model

Each proposition records correctness as `verified`, `incorrect`, or
`unresolved`. Only a verified proposition receives a substantive groundedness
classification: `grounded`, `misgrounded`, or `ungrounded`. Incorrect and
unresolved propositions use `not-applicable`. This keeps whether the proposition
is correct separate from whether the cited material grounds it.

Every material proposition maps to the exact cited authority artifact and
pinpoint, even when that mapping proves the citation irrelevant, contradictory,
partial, or absent at the asserted location. Source-support records preserve the
exact source text, qualifiers, jurisdiction, decision date, posture,
precedential force, source voice, selected domain-YAML paths, artifact hash, and
verification provenance.

## Outputs

The audit returns a JSON record conforming to an installed reference schema and
a human-readable report with one section per stable proposition ID. Both expose
all failed and unresolved propositions; no aggregate pass can hide them. The
trusted host remains responsible for append-immutable publication beneath the
exact output folder.

The schema validates required fields, identifiers, enumerations, and the
correctness/groundedness relationship. It does not decide whether a proposition
is correct, whether source text supports it, which voice is speaking, whether
authority applies, or whether a filing is ready.

## Regression corpus

Six isolated synthetic fixtures cover:

1. an inverted holding;
2. party argument described as the court's holding;
3. lower-court language attributed to the appellate court;
4. panel authority superseded en banc;
5. a real but irrelevant citation; and
6. two propositions supported by only one source.

Each fixture includes bounded synthetic source text, one passing audit, and one
permanent regression. The repository evaluation stays deterministic and
network-independent.

## Boundaries

The audit reads only `filing-source` and `verified-authority`, leaves both byte
identical, uses no internet during `audit`, writes only through the declared
output folder, and keeps transient work under `<output-folder>/temp/`. Human
litigation decisions and filing approval remain reserved.
