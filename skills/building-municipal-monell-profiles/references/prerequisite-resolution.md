# Municipal-profile prerequisite resolution

Use prerequisite resolution when the caller cannot yet supply every validated
folder required by the separate municipal-profile compilation operation. The
resolver is a pure trusted-host preflight over declared state. It does not open
an input folder, inspect a candidate output folder, run another skill, or
publish files itself.

The caller supplies one full absolute output folder for the resolution result.
The trusted host publishes only these returned artifacts beneath that folder:

- `municipal-profile-prerequisites.yaml`;
- `municipal-profile-prerequisites.md`; and
- the terminal run receipt.

All resolver temporary work, if any, stays beneath that output folder's `temp/`.
The resolver's output folder is not a collection, analysis, assessment, or
compilation output folder.

## Trusted-host state

Call `build_prerequisite_plan` from the installed
`scripts/municipal_profile_records.py` with these exact keyword arguments:

- `policy_source_state`;
- `policy_catalog`;
- `policy_assessment`;
- `available_roles`;
- `output_folders`; and
- `collection_authorization`.

Each upstream state record contains exactly:

```yaml
state: absent
terminal_receipt: false
expected_artifacts: false
validation_passed: false
fingerprints_match: false
```

`policy_source_state.state` is `absent`, `candidate`, `approved`, or `invalid`.
Catalog and assessment state is `absent`, `valid`, or `invalid`. A record may
also contain the boolean `substantive_gaps`. It never contains a path, command,
credential, source bytes, or asserted legal conclusion.

For `absent`, all four mechanical fields are false. For a candidate, approved,
or valid supplied output, a false mechanical field makes that output
`blocked-invalid`. `substantive_gaps: true` does not invalidate an otherwise
valid output.

`available_roles` contains exactly `collection`, `analysis`, `assessment`, and
`profile`. Each value lists the currently available roles from the owning
skill's contract. `output_folders` contains the same four keys with boolean
values stating whether the caller supplied a fresh full absolute output folder
for that later stage. These booleans do not grant folder access; the trusted
host validates every actual invocation separately.

`collection_authorization` contains exactly:

```yaml
internet: false
fees_required: false
fees_approved: false
```

Authorization applies only to the proposed collection invocation. It never
transfers to analysis, assessment, profile compilation, or a later resolver.

## Status routing

| Status                   | Meaning and required action                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------- |
| `input-required`         | Supply every listed role or one fresh full absolute output folder for the named next skill. |
| `authorization-required` | Supply bounded collection internet or fee authorization; do not begin collection.           |
| `review-required`        | Obtain independent `approved_for_analysis` review of candidate sources.                     |
| `ready-for-collection`   | Invoke `collecting-police-policy-sources` under its exact four-role authorized contract.    |
| `ready-for-analysis`     | Invoke `analyzing-police-policy-sources` under its exact four-role offline contract.        |
| `ready-for-assessment`   | Invoke `assessing-police-policy-compliance` under its exact six-role offline contract.      |
| `ready-for-profile`      | Start a new seven-role offline municipal-profile compilation invocation.                    |
| `blocked-invalid`        | Reject the named stale or invalid output and supply a fresh output folder for regeneration. |

The resolver selects one status. Missing roles precede output-folder readiness.
Collection authorization precedes collection output-folder readiness. It does
not invent or acquire a missing municipality, department, case record, verified
authority, actor, event, phase, jurisdiction, scope, or approval.

## Separate stage invocations

Every ready state names the owning installed skill, its exact roles, internet
mode, output-folder state, blocking reasons, and ordered postconditions. The
trusted host starts that skill as a new invocation. It exposes only the named
recursive read-only folders, supplies one fresh full absolute output folder, and
confines all temporary bytes to `<stage-output-folder>/temp/`.

After collection, stop for independent review. Candidate collection output
cannot mark itself approved and cannot become analysis input automatically.
After review, declare the approved ordinary source folder as the later analysis
invocation's read-only `policy-source` role.

Analysis must return:

- `policy-requirements.yaml`;
- `policy-analysis-gaps.yaml`;
- `policy-analysis.md`; and
- `policy-analysis-validation.json`.

Assessment must return:

- `policy-assessments.yaml`;
- `policy-assessment-gaps.yaml`;
- `policy-assessment.md`; and
- `policy-assessment-validation.json`.

Before continuation, require every named artifact, a successful terminal run
receipt, a passing domain validation, and matching input fingerprints. The
assessment must preserve actor, event, and phase separation and every unresolved
gap. A passing result with substantive gaps remains eligible; a missing,
changed, stale, or mechanically invalid result does not.

## Compilation remains unchanged

`ready-for-profile` does not compile inside the resolver. Start a new
`building-municipal-monell-profiles` invocation using the existing
`folder-contract.json`: exactly seven recursive read-only roles, disabled
internet, one fresh full absolute output folder, and output-local temporary
work. Return only the existing four municipal-profile artifacts and terminal
receipt.
