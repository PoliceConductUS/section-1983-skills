# Design: direct output-folder publication

`publish_folder_package()` continues to use the Issue #65 `OutputRun` in
`fresh-regenerable` mode. Each member path and `package-manifest.json` are
written relative to the output root without a prefix. The returned terminal
receipt therefore names the same three direct artifacts for a two-member profile
folder.

The output root also contains writer-owned control namespaces:

- `.skill-runs/<run-id>/` contains durable execution receipts;
- `temp/<run-id>/` contains transient staging and scratch space.

These namespaces are not package artifacts and cannot be proposed as member
paths. Artifact membership remains complete for every other regular file below
the output root. Hand-authored fictional fixtures may omit host control
namespaces and remain valid.
