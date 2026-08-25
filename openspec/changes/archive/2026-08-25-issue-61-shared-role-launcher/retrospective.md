# Retrospective

## What changed

The rejected package-shaped launcher design was replaced with one direct
folder-to-bytes boundary. The trusted host selects ordinary files, validates the
domain YAML required by the fixed role, snapshots the selected bytes, and
launches one protected role without exposing local paths.

## What the review caught

The first green implementation snapshot source YAML but did not invoke a
role-owned semantic validator. Whole-story review added that missing gate and
made both the YAML record and its referenced source content hash-stable across
binding and execution.

## Result

`adversarial-filing-review` now composes through the shared launcher while its
five-category, independence, no-remediation, read-only-target, and
plaintiff-decision rules remain owned by the fixed role. Every temporary path is
under the explicit output folder.
