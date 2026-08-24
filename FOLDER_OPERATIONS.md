# Start a Case Workspace

This guide establishes the artifact roles that the skills expect during a new
user's first hour. It is documentation only. It does not create a workspace
template, companion repository, or scaffolding command, and completing it does
not make any document filing-ready.

Use one immutable release when the tagged version is available:

```bash
npx skills add https://github.com/PoliceConductUS/section-1983-skills/tree/v0.1.0
```

If that tag has not been published, do not substitute `main` or another moving
branch. From the current source checkout, inspect the locally available skills
instead:

```bash
npx skills add . --list
```

The paths below are example paths, not mandatory paths. Rename them or use a
different name when the project's configuration or role mapping identifies the
equivalent role.

| Example path      | Role                                                         |
| ----------------- | ------------------------------------------------------------ |
| `case-workspace/` | Workspace root for one matter                                |
| `inputs/`         | Immutable inputs exactly as received                         |
| `sources.md`      | Approved source IDs, locations, roles, and review status     |
| `chronology.md`   | Source-bounded events, dates, actors, and uncertainty        |
| `strategy.md`     | Current user-approved objectives and reserved choices        |
| `decisions.md`    | Protected decisions with approval status and date            |
| `authorities/`    | Verified authorities with identity, status, and pinpoints    |
| `gaps.md`         | Missing facts, evidence, authority, configuration, and tools |
| `working/`        | Replaceable analysis and drafts                              |
| `generated/`      | Versioned generated artifacts and their source relationships |

Use one document for several roles if its fields keep those roles distinct. Do
not invent a file merely to match the example layout.

## 1. Choose a workspace root

Choose an existing project root or create one location approved by the user.
Record its purpose and the matter it belongs to. Do not infer a private path,
default case, or current matter from conversation history.

Keep immutable input material separate from working analysis and generated
artifacts. If the project already has those roles, use them instead of creating
duplicates.

## 2. Record approved sources

Create or update the project's approved source registry. A generic synthetic
example is:

```yaml
id: SRC-001
role: example operative document
path: inputs/example-document.pdf
status: approved
approved_by: user
```

An approved source ID identifies material the workflow may use. It does not
prove every proposition in the source. Record a gap when identity, location,
completeness, provenance, or permission is unresolved. Do not invent a source
ID, path, hash, quotation, or approval.

Create a verified authorities role only from sources whose identity, text,
pinpoint, status, and later history have actually been checked. A candidate
authority is not a verified authority.

## 3. Add a chronology entry

Add one source-bounded entry without converting an allegation or inference into
a fact:

```yaml
event_id: EVT-001
date: 2026-01-15
statement: The example document bears this date.
classification: source fact
source_ids: [SRC-001]
```

Use separate entries when actors, stages, times, sources, or classifications
differ. Label supported inference, allegation, disputed interpretation, and
discovery lead explicitly. If the source does not establish the date or event,
record a gap instead.

## 4. Record a protected decision

Keep strategy, positions, concessions, requested relief, and other user-
reserved choices separate from source facts. A generic synthetic workspace
decision looks like this:

```yaml
decision_id: DEC-001
decision: Keep the original input immutable and create a new generated version.
status: approved
approved_by: user
approved_on: 2026-01-16
```

Record pending options and consequences without selecting one. Only an actual
user approval changes a protected decision to `status: approved`.

## 5. Separate inputs from generated artifacts

Never overwrite immutable inputs. Put drafts, extracted text, reports, and other
generated artifacts in their configured role. When the project uses versions,
hashes, manifests, or source relationships, update them after each material
generation step. When it does not, do not fabricate those controls.

Working material is replaceable analysis. A generated artifact is an output that
should identify the inputs and process that produced it. Neither becomes an
approved source merely because a tool created it.

## 6. Run available validation

Run only validation commands configured by the project. Record the exact
command, input version, result, and time. If no command is configured, report
`validation unavailable` and record a gap; do not invent configuration, run a
guessed command, or report a pass.

Resolve every available deterministic failure before relying on the artifact.
Missing evidence, authority, approval, or an optional tool remains visible. This
first-hour workspace is not filing-ready and does not replace authority review,
adversarial review, writing review, or Filing CI.
