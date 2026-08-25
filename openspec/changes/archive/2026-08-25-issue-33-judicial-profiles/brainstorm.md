# Brainstorm

## Problem

The repository still exposes a real-judge drafting skill. That embeds
participant data and drafting behavior in one public package, prevents profile
reuse by a generic static role, and conflicts with the folder-native package
boundary.

## Selected design

Create one generic `building-judicial-reasoning-profiles` skill. It compiles
fictional or real public-source data into the standard immutable
`judicial-profile` folder package without generating judge-named skills or role
instructions.

The skill supports two non-overlapping operations:

- acquisition may use expressly authorized internet access and returns only a
  provenance-bearing source package;
- compilation uses internet-disabled, already-approved source folders and
  returns a complete judicial-profile package.

Newly acquired bytes cannot influence compilation in the same invocation. They
become approved-source input only through a later invocation.

## Domain boundary

The profile schema and install-local validator preserve four source classes:
`revealed_reasoning`, `stated_philosophy`, `self_presentation`, and
`court_compliance`. Each record retains proposition, source, source date, issue,
posture, attribution status, and use limits. Adoption-only orders,
recommendations, and outcome-only records never become independent reasoning.

Cross-class comparisons retain both record identities, exact propositions,
source dates, issue, posture, similarities, differences, and one bounded state:
`aligned`, `tension`, `divergent`, or `indeterminate`. The schema has no score,
weight, average, personality, preference, prediction, or behavioral-control
field.

Neutral drafting transfers may cite only validated independently reasoned
`revealed_reasoning` records for the same issue and posture. Unsupported
transfer produces no judge-specific drafting change.

## Rejected approaches

- Keep or rename the real-judge skill: participant data would remain behavior.
- Generate one skill per judge or profile variation: profile bytes could become
  capabilities and instructions.
- Compile newly downloaded material immediately: acquisition would bypass the
  approved-source and read-only package gate.
- Add averaging or prediction: source classes have different evidentiary uses
  and do not support psychological or outcome inference.
