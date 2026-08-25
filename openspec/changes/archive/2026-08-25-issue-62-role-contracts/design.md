# Design: Protected profile-conditioned findings roles

## Shared boundary

Both roles execute through the archived `static-role-launcher` contract. The
caller declares ordered absolute `profile`, `filing`, and `approved-sources`
input folders and one absolute output folder. The trusted host selects ordinary
relative files from those roots. The child receives path-free snapshots only.
Its process working directory and all temporary paths remain under
`<output-folder>/temp/<run-id>/`.

## Profile validation

The opposing-counsel role accepts one defense-counsel overlay and its matching
research snapshot under their existing domain schemas. The judicial-reviewer
accepts one `judicial-profile.json` plus its `judicial-profile-sources.yaml`.
Role-owned validators run before dispatch and verify the selected profile files,
source-documentation selection, profile kind, and hashes. Instruction-shaped
profile data fails domain validation or remains inert data; it never changes the
static role.

## Static behavior

`opposing-counsel` identifies source-backed professional attacks available from
the supplied record. It does not claim access to confidential information,
impersonate a real attorney, select plaintiff strategy, concede, remediate, or
emit a disposition.

`judicial-reviewer` identifies findings about comprehension, procedural framing,
authority presentation, record traceability, and gaps. It does not imitate
judicial voice, predict the assigned judge's outcome, choose a disposition,
remediate, or declare filing readiness.

Both roles are findings-only and internet-disabled. Output validation rejects
unknown fields, unsupported categories, source IDs outside the validated
allowlist, disposition or outcome language, target edits, and automatic
remediation.

## Output

Each child returns one structured role result. The trusted validator converts it
to one proposed output-relative JSON findings artifact. The shared launcher does
not publish it. Only the trusted host may publish beneath the explicit output
folder and record the terminal receipt.
