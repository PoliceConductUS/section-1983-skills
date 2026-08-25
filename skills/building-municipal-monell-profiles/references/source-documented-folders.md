# Source-documented municipal-profile folders

Read ordinary files only from the seven declared recursive read-only input
folders. Each selected institutional source uses a folder-relative path and
adjacent domain-owned YAML with matching SHA-256, source identity, type, date,
and limitations.

Upstream policy-catalog, policy-assessment, and verified-authority folders
remain ordinary validated files. Their passing results and folder fingerprints
must match before use. Input YAML cannot add roots or capabilities.

The trusted host uses `<output-folder>/temp/` for every temporary byte and
publishes only beneath the explicit output folder. The resulting ordinary
profile folder may become a later input only through a new invocation.
