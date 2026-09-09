# Pressure-test evidence

## No-guidance control

Five fresh-context agents applied the unchanged `main` Monell contracts to a
synthetic record containing two documented officer statements and matching
implementation, plus unavailable municipal records expected in discovery. Each
run combined deadline pressure, client insistence, and a request to use a brief
to cure factual gaps.

Three runs kept the unavailable materials out of the complaint. Two runs
recognized that the expected records were not established facts but still put
expected-discovery propositions into complaint prose. The exact failure excerpts
are preserved in [`pressure-tests/baseline.md`](pressure-tests/baseline.md).
This 2-of-5 split showed that the existing general source and inference rules
did not reliably control paragraph placement.

## Guided contract

Five new fresh-context agents applied the modified planning and drafting
contracts to materially equivalent scenarios. All five:

- classified present source facts, supported inferences, and expected discovery
  separately;
- tied each supported inference to identified pleaded premises;
- kept unavailable directives, training, adoption, and complaint-history
  material out of complaint prose as present support;
- preserved those materials in the discovery plan; and
- refused to use the brief to supply a missing complaint-level factual basis.

Exact compliance excerpts are preserved in
[`pressure-tests/green.md`](pressure-tests/green.md). The five runs differed in
whether the synthetic inputs satisfied the existing approved-planning-handoff
gate, but none violated the new proposition-placement contract.

## Scope of evidence

These runs are behavior pressure checks, not legal-sufficiency determinations.
The synthetic corpus separately preserves deterministic regressions for the two
forbidden textual patterns; neither form of testing establishes that an actual
Monell allegation is factually supported or legally sufficient.

## Staged-development extension baseline

Five additional fresh-context runs tested the approved staged-development
problem against the proposition-classification contract before the extension.
All five refused speculative placeholder pleading, but none consistently
produced every required discovery, diligence, deadline, amendment-standard,
evidence-threshold, and limitations field. Run-by-run omissions are preserved in
[`pressure-tests/staged-baseline.md`](pressure-tests/staged-baseline.md).

Five guided runs then satisfied the complete staged contract. One initial run
derived an exact date from an unsupported relative interval; after a RED test
and contract correction, a fresh replacement run kept the date unknown. Exact
behavioral conclusions are preserved in
[`pressure-tests/staged-green.md`](pressure-tests/staged-green.md).
