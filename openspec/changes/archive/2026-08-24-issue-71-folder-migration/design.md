# Design: exact install-local contracts with host-owned persistence

## Contract shape

Every `skills/<name>/references/folder-contract.json` has exactly this version-1
shape:

```json
{
  "version": 1,
  "skill": "section-1983-drafting",
  "input_roles": ["record", "authorities", "strategy", "filing"],
  "target": {
    "policy": "optional",
    "roles": ["filing"]
  },
  "internet": "authorized",
  "output": {
    "mode": "append-immutable"
  }
}
```

The object has no additional properties. `input_roles` is a nonempty ordered
array of unique safe role names. Every listed role is required in the invocation
and maps to one existing recursive read-only folder; unavailable material inside
a role remains a reported gap. `target.policy` is `required`, `optional`, or
`none`. Required and optional targets may use only the listed target roles;
`none` requires an empty role array. `internet` is exactly `disabled` or
`authorized`. Output mode is always `append-immutable`.

## Approved per-skill matrix

| Skill                                             | Exact input roles, in order                                               | Target policy and allowed roles           | Internet   |
| ------------------------------------------------- | ------------------------------------------------------------------------- | ----------------------------------------- | ---------- |
| `adversarial-filing-review`                       | `filing`, `approved-sources`                                              | required: `filing`                        | authorized |
| `audit-authorities`                               | `filing`, `authorities`                                                   | required: `filing`                        | authorized |
| `auditing-section-1983-discovery-responses`       | `served-discovery`, `responses`, `production`, `authorities`              | optional: `served-discovery`, `responses` | disabled   |
| `auditing-section-1983-privilege-logs`            | `privilege-log`, `served-discovery`, `authorities`                        | optional: `privilege-log`                 | disabled   |
| `building-defense-counsel-overlays`               | `research-snapshot`, `case-record`                                        | required: `research-snapshot`             | disabled   |
| `building-litigation-alignment-overlays`          | `docket-snapshot`, `filing`                                               | required: `docket-snapshot`               | disabled   |
| `drafting-false-arrest-complaints`                | `record`, `authorities`, `filing`                                         | optional: `filing`                        | disabled   |
| `drafting-for-judge-scholer`                      | `filing`, `judge-corpus`, `court-conduct`                                 | required: `filing`                        | disabled   |
| `drafting-section-1983-complaints`                | `record`, `authorities`, `filing`                                         | optional: `filing`                        | disabled   |
| `drafting-section-1983-declarations-and-evidence` | `record`, `authorities`                                                   | optional: `record`                        | disabled   |
| `drafting-section-1983-deposition-outlines`       | `record`, `authorities`, `discovery`                                      | optional: `record`                        | disabled   |
| `drafting-section-1983-meet-and-confer`           | `discovery-audit`, `served-discovery`, `authorities`, `conference-record` | required: `discovery-audit`               | disabled   |
| `drafting-section-1983-rule-59e`                  | `record`, `authorities`, `filing`                                         | optional: `filing`                        | disabled   |
| `drafting-section-1983-written-discovery`         | `record`, `authorities`, `claim-map`                                      | optional: `claim-map`                     | disabled   |
| `filing-ci`                                       | `filing`, `authorities`                                                   | required: `filing`                        | disabled   |
| `horan-bad-words`                                 | `filing`                                                                  | required: `filing`                        | disabled   |
| `rrd`                                             | `motion`, `record`, `authorities`                                         | required: `motion`                        | disabled   |
| `rrd-rule12`                                      | `motion`, `record`, `authorities`                                         | required: `motion`                        | disabled   |
| `rrd-rule12-city`                                 | `motion`, `record`, `authorities`                                         | required: `motion`                        | disabled   |
| `rrd-rule12-officers`                             | `motion`, `record`, `authorities`                                         | required: `motion`                        | disabled   |
| `section-1983-drafting`                           | `record`, `authorities`, `strategy`, `filing`                             | optional: `filing`                        | authorized |
| `studying-rule-59e-decisions`                     | `decisions`, `authorities`                                                | optional: `decisions`                     | authorized |

The variants reflect substantive seams rather than storage products. Motion
planners select the motion; filing reviewers select a filing; snapshot builders
select the immutable snapshot; new drafting can omit a filing target. Internet
is authorized only for the stateless provider, authority retrieval,
localization/source work, and Rule 59 research. Snapshot-based builders and all
other operations consume declared local material with internet disabled.

## Trusted-host flow

1. The host loads the installed skill's folder contract.
2. It rejects an invocation whose skill, ordered role set, target, internet, or
   output mode differs from that contract.
3. The canonical root validator resolves absolute roots and emits the logical
   input manifest.
4. The host enforces recursive input-read-only access, output-only writes,
   undeclared-path denial, runtime bounds, and the exact internet policy.
5. The skill or packaged helper consumes declared input bytes and returns an
   artifact plan containing canonical output-relative paths, bytes or streams,
   and validated internet provenance when applicable.
6. The host alone calls `OutputRun.start`, `write`, `complete`, or `fail`.

The skills never receive an output-root path. They cannot instantiate a second
persistence manager, create receipts, or select an alternate output location.

## Standalone helper interface

Packaged helpers must work when their skill folder is copied alone. They may
accept:

- one declared input-root descriptor plus canonical slash-separated relative
  target paths; or
- validated in-memory objects or JSON/bytes from standard input.

They return deterministic structured results or artifact bytes on standard
output/in memory. They reject absolute paths, traversal, symlink escapes,
undeclared roles, unsupported entries, malformed bytes, and unbounded input.
They do not import `scripts/validate_folder_invocation.py` or
`scripts/skill_output_writer.py`, open output roots, create reports, or perform
general command dispatch.

## Filing CI and complaint checks

`filing-ci` ships a narrow wrapper with an explicit registry of packaged checker
IDs. The wrapper accepts the declared `filing` root, required filing target, and
the `authorities` root. It dispatches only a checker packaged in the installed
skill distribution. An unknown, absent, or incompatible checker produces a
stable unavailable result before artifact publication.

`drafting-section-1983-complaints` packages the mechanical checks already
declared by `complaint-structure-contract.json`: section order, numbering,
identifiers, tuple/cardinality, cross-references, incorporation, and required
field presence. It excludes fact truth, legal sufficiency, authority fit,
material analogy, strategy, and filing readiness. The helper emits one
deterministic mechanical handoff report for host publication.

## Quality control and immutable outputs

Quality-control stages remain non-mutating and advisory. They no longer resolve
a project boundary, version folder, or implicit `audits/` directory. Each stage
reads its declared roles and selected target and proposes a unique
output-relative report path. The host publishes that report append-only and
records logical input hashes, artifact hashes, internet provenance, run ID,
time, scope, sources, and outcome in the shared terminal receipt. Review of a
prior report requires that report to be expressly present in a declared input
role; the new report remains a different append-only output artifact.

## Compatibility and scope

Legal requirements, source classifications, human approvals, claim structures,
anti-gaming checks, finding schemas, overlay schemas, corpus schemas, and
substantive validators remain unchanged. Current public docs and durable specs
drop product-shaped runtime instructions, while archived changes remain
historical. Repository release/evaluation Git and command use remains outside
the public-skill runtime contract.

## Deterministic verification

Tests copy each skill package without repository-root files, load and validate
its exact contract, build only its declared role folders, hash every input tree,
and exercise required/optional/none targets. Mutation tests add missing, extra,
duplicate, reordered, unsafe, and wrong-skill roles; invalid target policies;
wrong internet; non-append output; traversal; symlink escapes; undeclared paths;
direct output writes; and root imports. Internet-disabled operations run with a
network trap. Every completed or unavailable artifact is published only by a
host test double through the shared output writer, and all input hashes remain
unchanged.
