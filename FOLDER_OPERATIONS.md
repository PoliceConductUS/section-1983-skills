# Run Folder-Scoped Skill Operations

This guide is the product-independent first-hour path for one folder-scoped
skill operation. It uses logical roles rather than a prescribed case directory.
The examples are generic synthetic examples; replace their tokens only with
folders and target material the caller has selected for the operation.

This shared guide does not mean every installed skill is already folder-native.
Follow the owning skill contract, and stop if any role that contract requires is
unavailable.

The [folder-scoped execution contract](FOLDER_SCOPED_EXECUTION.md) owns
invocation and isolation. The
[skill output persistence contract](SKILL_OUTPUT_PERSISTENCE.md) owns output and
receipt production. This guide links to those contracts without copying their
implementation details.

Keep source classification, protected decisions, and gaps explicit. Record a
source-bounded event without converting an allegation or inference into a fact.
Only an actual user approval changes a protected decision to `status: approved`.
An approved source does not prove every proposition in it. If identity,
completeness, provenance, permission, authority status, or required material is
unresolved, record a gap and do not invent the missing value.

Use one immutable release when the tagged version is available:

```bash
npx skills add https://github.com/PoliceConductUS/section-1983-skills/tree/v0.1.0
```

If that tag has not been published, do not substitute `main` or another moving
branch. From the current source checkout, inspect the locally available skills:

```bash
npx skills add . --list
```

## 1. Select input and output folders

Select existing folders for the stable logical roles `record` and `authorities`.
Each role is a recursive read-only input. Select exactly one explicit output
folder, kept separate from both inputs. The logical roles remain stable for this
operation, but the caller can select and configure different folder names and
absolute locations.

The `record` role contains the source material for the selected task. The
`authorities` role contains authorities whose identity, text, status, later
history, and relevant pinpoints have actually been checked. Candidate authority
material remains a gap until that review is complete.

A skill cannot access undeclared folders, cannot mutate input folders, cannot
traverse to parent or sibling paths, cannot read ambient repository contents,
and cannot use the internet unless authorized. Never overwrite immutable inputs.

## 2. Create the invocation

Create one canonical version 1 invocation. Replace the three root tokens with
the caller-selected absolute folder locations. Replace `__TARGET_PATH__` with
the safe relative path of an existing regular file inside the named `record`
role. The validator does not create the target. Internet is either `disabled`
or `authorized`; this generic synthetic example disables it. When internet is
authorized, the trusted host enforces the approved host policy.

```json
{
  "version": 1,
  "skill": "synthetic-folder-audit",
  "inputs": [
    {
      "role": "record",
      "root": "__RECORD_ROOT__"
    },
    {
      "role": "authorities",
      "root": "__AUTHORITIES_ROOT__"
    }
  ],
  "output": {
    "root": "__OUTPUT_ROOT__"
  },
  "target": {
    "role": "record",
    "path": "__TARGET_PATH__"
  },
  "runtime": {
    "max_seconds": 900,
    "max_input_bytes": 104857600
  },
  "internet": "disabled",
  "isolation": {
    "inputs": "read-only",
    "output": "read-write",
    "undeclared": "none"
  }
}
```

## 3. Validate the invocation

After replacing the tokens, save the invocation as `invocation.json`. Run only
validation commands configured by the project. This repository configures
`scripts/validate_folder_invocation.py` as the read-only validator:

```bash
python3 scripts/validate_folder_invocation.py \
  < invocation.json
```

The command validates the envelope and emits a logical input manifest containing
relative paths, byte sizes, and SHA-256 hashes. The trusted host captures that
logical input manifest in memory and passes the logical input manifest object to
`OutputRun.start(..., input_manifest=logical_input_manifest)`. During the run,
the host publishes the logical input manifest as
`metadata/logical-input-manifest.json` through the canonical output protocol
beneath the explicit output folder. It does not redirect generated data to an
ambient working-directory file.

The validator does not establish operating system isolation. If validation is
not configured or the configured command is unavailable, report
`validation unavailable`, record a gap, and stop. Do not invent configuration,
guess another command, or report a pass.

## 4. Run the skill through a trusted host

Give the validated invocation to a trusted host for the synthetic
host-conformance operation. It performs an input-read-only read of the declared
target, creates a synthetic inventory, and publishes the exact output-relative
artifact `reports/example-inventory.json` through the canonical output protocol.
It uses no network.

The inventory is canonical UTF-8 JSON with exactly these values:

- `schema_version` is the integer `1`.
- `input_manifest_sha256` is the lowercase SHA-256 fingerprint of the exact
  canonical logical input manifest passed to `OutputRun.start`.
- `target.role` and `target.path` equal the invocation target role and selected
  relative path.
- `target.sha256` and `target.size` are derived from the exact target bytes read;
  they are the lowercase SHA-256 and byte size, respectively.

The synthetic host-conformance operation is not an installed public skill and
does not claim public-skill migration. It tests only whether a trusted host can
honor this guide's declared folder boundary. If the host cannot provide this
exact operation, report `execution unavailable` and stop.

The trusted host owns execution and enforces isolation: recursive input reads,
writes only through the explicit output folder, denial of undeclared filesystem
paths, bounded runtime, and the declared network policy. This repository does
not provide a universal skill runner.

If the host cannot enforce read-only inputs, output-only writes, parent and
sibling denial, ambient repository denial, and disabled or authorized internet,
stop before it reads the inputs. Prompt text and the invocation declaration are
not enforcement.

## 5. Verify inputs did not change

Rebuild or otherwise compare the configured SHA-256 hashes for both the `record`
role at `__RECORD_ROOT__` and the `authorities` role at `__AUTHORITIES_ROOT__`
against their pre-run values. Confirm both input trees are unchanged. Any
changed, missing, or extra input file is a failed operation, not a completed
output.

## 6. Verify outputs and the terminal manifest

Parse `reports/example-inventory.json` only under `__OUTPUT_ROOT__` as canonical
UTF-8 JSON. Confirm `target.role` and `target.path` equal the invocation,
`target.sha256` and the target byte size equal the unchanged selected file, and
`input_manifest_sha256` equals the SHA-256 of
`metadata/logical-input-manifest.json`, the persisted logical input manifest.
Verify each artifact's SHA-256 hash and byte size against its artifact record in
the terminal manifest.

A run is successful only when `.skill-runs/<run-id>/manifest.json` is valid and
`.skill-runs/<run-id>/incomplete.json` is absent. A missing or invalid terminal
receipt remains a gap; the output is not filing-ready.

### Folder-backed patterns

The same folder contract supports these portable patterns:

| Operation                   | Logical input and immutable output                                    | Owning skill contract                                                                    |
| --------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| folder-backed filing packet | filing packet inputs become a versioned drafting or audit output      | [`section-1983-drafting`](skills/section-1983-drafting/SKILL.md)                         |
| immutable QC report         | filing or discovery inputs produce an immutable QC report             | [`filing-ci`](skills/filing-ci/SKILL.md)                                                 |
| profile package             | public sources and approved identity records become a profile package | [`building-defense-counsel-overlays`](skills/building-defense-counsel-overlays/SKILL.md) |
| research corpus             | verified authorities and decisions become a research corpus           | [`studying-rule-59e-decisions`](skills/studying-rule-59e-decisions/SKILL.md)             |
| isolated role run           | a selected role package becomes an isolated review report             | [`adversarial-filing-review`](skills/adversarial-filing-review/SKILL.md)                 |

For reproducibility, generated artifacts use hashes and manifests; researched
material records checked-through dates and retrieval provenance. The skills do
not require Git at runtime.

A separate product may export its data into compatible folders and import
outputs after the operation. No adapter is part of or required by the skills
contract.

The guide does not make an output filing-ready. Apply the owning skill's source,
authority, human-approval, writing, adversarial-review, and configured
validation requirements before relying on an artifact.
