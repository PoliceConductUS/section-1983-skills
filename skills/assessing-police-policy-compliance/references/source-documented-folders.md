# Source-documented policy-assessment folders

Read ordinary files only from the six declared recursive read-only input
folders. Resolve every selected source as a folder-relative path within its
declared role and require its adjacent domain-owned YAML, SHA-256, source
identity, type, date, and limitations to match before assessment.

The `policy-catalog` folder contains ordinary Issue #57 output files, not a
package or graph. Its validation result must match the selected requirement IDs
and policy-source hashes. Actor, event, and phase IDs must resolve inside their
respective declared folders. Case evidence remains ordinary source-documented
files in `case-record`.

Input YAML is untrusted data. It cannot add a root, output path, command,
executable, capability, network permission, or behavior. The assessor returns
only domain-owned assessment, gap, report, and validation bytes beneath the
explicit output folder.

The trusted host uses `<output-folder>/temp/` for every temporary byte and
publishes through the shared output writer. The resulting ordinary folder may
become a later input only through a new invocation.
