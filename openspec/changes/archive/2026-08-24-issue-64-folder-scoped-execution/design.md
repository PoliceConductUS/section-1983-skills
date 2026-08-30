# Design

## Context

Skills in this repository are independently installable instruction packages.
Some also include focused Python scripts, but repository governance sends
general-purpose executable products to their owning repositories. Issue #64
therefore needs a contract and deterministic conformance seam without pretending
that a Python helper can sandbox an arbitrary agent.

## Goals / Non-Goals

**Goals:**

- Make folder access and internet authority explicit and fail closed.
- Give hosts one versioned invocation shape and deterministic path semantics.
- Make logical input fingerprints reproducible across machines.
- Preserve the boundary when any public skill is installed alone.

**Non-goals:**

- Implement operating-system sandboxing or network filtering.
- Write generated artifacts or define collision and atomic-write behavior.
- Define the concrete input roles for every existing legal workflow.
- Add CaseGraph compatibility.

## Decisions

### Versioned JSON envelope

`governance/folder-invocation.schema.json` defines version 1. Required fields
identify the skill, one or more named input folders, exactly one output folder,
runtime limits, internet policy, and host isolation. An optional target selects
one relative path within one input role.

Folder roots are absolute. Relative roots would silently depend on the ambient
working directory, which is outside the declared invocation. Role names and
skill names use lower-case kebab syntax so receipts and later package manifests
have stable logical identifiers.

The isolation object is an assertion supplied by a trusted launcher, not an
assertion supplied by an arbitrary skill caller. It has exact values:
`inputs: read-only`, `output: read-write`, and `undeclared: none`. The runtime's
internet value is `disabled` or `authorized`.

### Canonical paths and containment

`scripts/validate_folder_invocation.py` resolves every declared root strictly
before work. Inputs and output must exist as directories. The output may not be
inside an input, and an input may not be inside the output. Input roots may
overlap other input roots because the caller can intentionally assign two
logical roles to the same source tree.

Child paths are always relative and reject `..`. Existing symlinks are resolved
component by component and must remain within their declared root. Directory
symlinks in an input manifest are traversed only when they remain inside the
root; real-directory identities prevent cycles. File symlinks may resolve only
inside the same root.

### Logical manifest

The conformance validator walks roles in declaration order and files in sorted
relative-path order. Each entry records `path`, `size`, and lowercase SHA-256.
The manifest records no canonical root and no absolute source path. This makes
the same bytes at a different machine path produce the same logical manifest.

### Enforcement split

The validator proves envelope shape, path confinement, target selection, and
input fingerprints. It does not prove the host mounted inputs read-only or
blocked undeclared filesystem/network access. `FOLDER_SCOPED_EXECUTION.md` and
the compact install-local skill boundary require the host to establish those
capabilities and require the invocation to stop when it cannot.

### Compact independently installable contract

Every public `SKILL.md` contains the same compact boundary:

1. only caller-declared input folders are available and recursively read-only;
2. writes occur only beneath the caller-declared output folder;
3. internet is used only when that skill expressly authorizes it; and
4. execution stops before reading case material if the host cannot enforce the
   filesystem and network boundary.

The complete protocol remains in one root owner document and JSON schema.
Deterministic governance validation checks the compact semantic markers in all
public skills.

## Risks / Trade-offs

- **A host may falsely attest isolation.** The contract expressly assigns trust
  to the launcher and makes no prompt-only sandbox claim.
- **Embedding compact text touches every skill.** Governance validation prevents
  drift, while #71 later adds only each skill's concrete roles and internet
  policy.
- **Internal symlinks can duplicate a file in the manifest.** Each logical path
  remains explicit and hashed; escaping and cycles fail closed.

## Migration plan

1. Add the schema, conformance validator, canonical document, and tests.
2. Add the compact contract to every public skill and governance validation.
3. Archive the OpenSpec change and publish the durable specifications.
4. Let #71 migrate concrete implemented entrypoints without changing this
   foundation.

## Open questions

None.
