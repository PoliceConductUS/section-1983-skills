# immutable-folder-packages Specification Delta

## MODIFIED Requirements

### Requirement: Regeneration publishes the explicit output folder

Only the trusted host MAY publish folder output. It MUST require an
installed-contract-bound invocation whose caller supplied one absolute output
root, or stop and ask for that root before execution. It MUST write every
proposed member and `package-manifest.json` directly beneath that exact fresh
output root through one complete output run. It MUST NOT create an intermediate
`packages/<package-id>/` namespace, mutate a consumed folder or context input,
or relocate output through CaseGraph, Git, a registry, or an ambient path.

Writer-owned `.skill-runs/` receipt files and `temp/` transient files are not
package artifacts. Every other regular file beneath the output root MUST appear
exactly once in `package-manifest.json`.

#### Scenario: A profile folder is regenerated

- **WHEN** a builder creates a new complete profile from declared read-only
  inputs and one caller-selected fresh output folder
- **THEN** `package-manifest.json` and all members appear directly beneath that
  output folder, the folder has its own fingerprint and preserved source
  identities, and every input remains byte-for-byte unchanged
