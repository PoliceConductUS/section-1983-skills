# Proposal: document the invocation-owned temp folder

## Why

Issue #65 now reserves `<output-folder>/temp/` as every invocation's only
temporary workspace. The canonical first-hour guide predates that correction and
must teach the exact same boundary.

## What changes

- Tell callers to supply one absolute output-folder path or answer a prompt for
  it before work begins.
- Document `temp/` as the exclusive staging, scratch, intermediate,
  working-directory, and process-temporary namespace.
- Verify the synthetic flow uses the corrected writer and process configuration.

## Non-goals

- Adding a runner, adapter, CaseGraph integration, or case-directory template.
- Duplicating the output writer implementation in the guide.
