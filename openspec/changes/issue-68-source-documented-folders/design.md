# Design: ordinary folders with domain YAML provenance

## Boundary

The generic runtime boundary is the validated invocation from #64. It contains
ordered named input roots and one output root. No second folder identity or
membership format is introduced.

## Source documentation

Each domain skill names the YAML records it requires. A `SOURCE.yaml` may
document one source unit; a profile builder may define a profile-specific YAML
record. When applicable, those records carry folder-relative artifact paths,
content hashes, provenance or retrieval identities, checked-through or retrieval
dates, classifications, validation results, assumptions, and gaps. There is
intentionally no generic root schema or required filename for every folder.

References are resolved only through the existing declared-input path boundary.
A missing domain record, invalid YAML, escaping relative path, mismatched hash,
or stale required date fails before semantic work.

## Behavior/data separation

Protected behavior stays in installed skill or static-role instructions.
Participant and court material stays in ordinary input files. The trusted host
selects immutable bytes from declared roots; data never rewrites the protected
instructions or grants filesystem, output, or network authority.

## Removal

Delete every Issue #68 artifact whose only purpose is package identity,
membership, loading, publication, or role/package compatibility. Replace public
package language in the two existing overlay skills with direct-output and
domain-YAML language.
