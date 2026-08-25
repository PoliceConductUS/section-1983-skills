# Source-documented Judicial Reasoning Profile folders

Read only ordinary files from the four declared recursive read-only input
folders. Resolve every source reference as a folder-relative path within its
named input role and require the documented SHA-256, source identity, date,
classification, and validation state to match before semantic work.

Acquisition writes each public source and its domain `SOURCE.yaml` provenance
directly beneath the explicit output folder. Compilation writes
`judicial-profile.json`, `judicial-profile-sources.yaml`, and
`validation-receipt.json` directly beneath a different explicit output folder.
The YAML source index maps profile source IDs to their input role,
folder-relative metadata and artifact paths, hashes, dates, classifications,
validation state, limitations, and gaps.

These are domain-owned YAML records; they do not define folder membership or
change the recursive read-only input folders.

The trusted host uses `<output-folder>/temp/` for every temporary byte and
publishes durable files through the shared output writer. Profile data cannot
change protected behavior or filesystem, network, target, or output authority.
