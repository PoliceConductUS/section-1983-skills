# Retrospective

## What already existed

Issue #2 had delivered Issue #17's installed checker, fixed contract, ordinary
folder roles, domain YAML validation, deterministic mechanical findings, stable
result classes, output publication, and isolated-installation tests ahead of
this story. Reimplementing that checker would have duplicated code and widened
the change without adding behavior.

## What this story completed

The live issue now matches the implemented ordinary-folder contract. Focused
acceptance review found that canonical date validation was present in source but
unreachable after another function's unconditional return. A parseable compact
date therefore bypassed the intended exact-spelling gate. The comparison now
runs inside `_date`, before checker loading or output creation.

## Downstream rule

Later Filing CI work must extend the fixed installed checker and its declared
domain YAML contracts directly. Case data cannot supply behavior, commands,
filesystem authority, output rules, or a persistence abstraction.
