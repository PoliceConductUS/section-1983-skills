# Design: trusted-host quality-control report publication

## Invocation and target

Every skill discovered by the repository's behavioral quality-control classifier
has `target.policy: required` in its install-local folder contract. The target
role remains restricted to that skill's approved target-role set. The trusted
host rejects a missing, directory, escaping, or out-of-role target before report
publication.

## Reviewed-input manifest

The host starts from the deterministic logical input manifest produced by
`build_input_manifest()`. For a QC run it filters every path beneath the
reserved `quality-control-reports/` prefix from the reviewed set. If and only if
the explicit target is itself beneath that prefix, the exact target file remains
in the filtered manifest; sibling and older reports remain excluded. Role order,
file order, sizes, and SHA-256 values remain canonical.

The report metadata contains the complete filtered logical manifest, so the
logical input roles and every reviewed artifact hash are inspectable. The
existing `OutputRun` fingerprints the same filtered manifest in its terminal
receipt.

## Canonical report path

The host derives exactly one path:

`quality-control-reports/<check-kind>-<YYYYMMDDTHHMMSS[ffffff]Z>-<run-id>.md`

`check-kind` and `run-id` are lower-kebab identifiers. The UTC instant is
supplied explicitly and must be timezone-aware UTC. The microsecond component is
included only when nonzero. `OutputRun` remains the final authority for
canonical path validation, collision refusal, output confinement, and durable
create-exclusive publication.

## Report metadata and bytes

The report begins with one fenced `quality-control-report+json` block. Its
canonical compact JSON object has exactly:

- `schema_version` (1);
- `skill` and `skill_version`;
- `quality_control_kind`, `run_at`, and `run_id`;
- `input_manifest`, containing ordered logical roles and reviewed file hashes;
- `target`, containing role, relative path, SHA-256, and byte size;
- `scope` and `result`;
- `failed_findings` and `passing_but_suboptimal_recommendations`;
- `run_manifest`, containing the same run ID and the canonical output-relative
  identity `.skill-runs/<run-id>/manifest.json`.

The processor-supplied Markdown body follows the metadata block. Finding and
recommendation arrays are JSON values supplied by the skill and must be
canonically serializable; their substantive schema remains owned by the skill.
Recommendations remain advisory and never authorize mutation.

The manifest path is an identity known before terminal publication, not a claim
that the manifest already exists. A run is complete only after `OutputRun`
durably publishes the report and its success manifest and removes incomplete
state.

## Trusted-host API

`scripts/quality_control_report.py` exposes one report-plan builder and one
publication operation. The builder validates scalar metadata, derives the
filtered manifest and target identity, and returns detached path/content/input
manifest values without writing. The publisher starts `OutputRun` in
`append-immutable` mode, writes exactly the planned report, and completes the
run. Internet source records, when supplied, remain validated and recorded by
`OutputRun`.

Any validation, write, sync, collision, or receipt failure propagates as a
bounded failure. The publisher never returns a success receipt unless both
report bytes and the terminal manifest are durable. Retry requires a different
run ID and therefore a different report path.

## Public-skill contract

Governance and every independently installable QC skill state that the stage:

1. declares all exact input roles and one primary target;
2. returns report content and structured findings only;
3. uses the trusted-host QC publisher for one new report;
4. treats prior reports as excluded unless one is the explicit target; and
5. leaves all remediation to a separately authorized stage followed by fresh
   verification.

Public skill processors do not import the publisher or output writer and do not
receive output-root paths.
