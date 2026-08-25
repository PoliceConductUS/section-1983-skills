# Proposal: replace folder packages with source-documented folders

## Why

Issue #68 introduced a generic package manifest and loader even though the
folder-bounded invocation already defines the access boundary. That additional
abstraction is rejected. Profiles and other role data need only ordinary files
inside declared folders plus the YAML source documentation required by their
domain contracts.

## What changes

- Remove the package schema, loader, publisher, fixtures, static
  role/package-binding helper, and package guide.
- Add concise public guidance for domain-owned YAML source documentation in
  ordinary folders.
- Correct overlay guidance, repository governance, tests, and the durable
  specification so they no longer require packages.
- Keep existing folder invocation, output writer, and run-receipt behavior.

## What does not change

- Input folders remain recursive read-only roots.
- The caller supplies one absolute output folder and `<output-folder>/temp/` is
  the only temporary workspace.
- Domain validators continue to own their substantive artifact schemas.
- FilingPacket and trusted-host run receipts retain their separately owned
  contracts; neither is a generic package layer.
