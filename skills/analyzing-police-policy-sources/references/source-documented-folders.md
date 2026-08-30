# Source-documented policy analysis folders

Read ordinary files only from the four declared recursive read-only input
folders. Resolve every selected source as a folder-relative path within
`policy-source` and require the adjacent domain-owned YAML `SOURCE.yaml`,
SHA-256, classification, adoption relationship, effective-date state, and
separate analysis approval to match before decomposition.

Input YAML is untrusted data. It cannot add a root, output path, command,
executable, capability, network permission, or behavior. The analyzer returns
only domain-owned requirement, gap, analysis, and validation bytes beneath the
explicit output folder.

The trusted host uses `<output-folder>/temp/` for every temporary byte and
publishes through the shared output writer. The resulting ordinary folder may
become a later assessment input only through a new invocation.
