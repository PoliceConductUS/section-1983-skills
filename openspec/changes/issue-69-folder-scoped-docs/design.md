# Design: one folder-native public entry point

## Canonical document ownership

`FOLDER_OPERATIONS.md` becomes the first-hour guide and README links to it with
one repository-relative link. `FOLDER_SCOPED_EXECUTION.md` continues to own the
invocation/isolation protocol, and `SKILL_OUTPUT_PERSISTENCE.md` continues to
own output publication and receipt semantics. The guide links to those owners
instead of copying their full implementation contracts.

## Invocation example

The guide uses one parseable version-1 JSON envelope with two synthetic logical
roles, `record` and `authorities`, exactly one output root, one target in the
`record` role, disabled internet, bounded runtime, and the required isolation
declaration. Shell variables substitute caller-selected absolute folders before
validation; the repository does not prescribe their names or parent directory.

The ordered flow:

1. selects existing input and output folders;
2. writes the synthetic invocation envelope;
3. validates it with `scripts/validate_folder_invocation.py`;
4. supplies the validated envelope and selected skill contract to a trusted host
   for one input-read-only operation;
5. verifies input hashes are unchanged; and
6. verifies output artifacts plus `.skill-runs/<run-id>/manifest.json` and the
   absence of `incomplete.json`.

The guide does not invent a universal skill runner. It states that the trusted
host owns sandbox enforcement and invocation of the selected agent/skill.

## Portable artifact patterns

The guide describes each pattern only as logical roles and immutable outputs:

- filing packet inputs to a versioned drafting or audit output;
- filing or discovery inputs to an immutable QC report;
- public sources and approved identity records to a profile package;
- verified authorities/decisions to a research corpus; and
- one selected role package to an isolated review report.

Each operation links to its owning `skills/<name>/SKILL.md`. A separate product
may export compatible folders and import outputs, but no adapter is required or
implemented here.

## Deterministic tests

Replace the old workspace-guide test with a folder-operations documentation test
that parses the JSON fixture after substituting synthetic absolute roots, checks
link confinement/existence, asserts the ordered end-to-end headings, requires
stable role/output reuse, bans product-specific current-doc terms and private
markers, and verifies that every documented operation has an owning skill link.
