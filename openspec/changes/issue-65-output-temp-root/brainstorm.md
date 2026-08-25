# Brainstorm: invocation-owned temporary workspace

## Clarified boundary

Every invocation already receives one explicit absolute output folder. The user
clarified that `<output-folder>/temp/` must also be the invocation's only
temporary workspace.

## Decision

Keep durable artifacts and run receipts under the explicit output root. Move
writer staging from `.skill-runs/<run-id>/staging/` to `temp/<run-id>/`. Reserve
`temp/` against public artifact writes. Expose the trusted-host process
configuration that uses `<output-folder>/temp/` as both the working directory
and the `TMPDIR`, `TMP`, and `TEMP` value.

The operating-system isolation boundary from Issue #64 remains responsible for
making undeclared paths inaccessible. Environment variables and prompt text do
not substitute for that isolation.
