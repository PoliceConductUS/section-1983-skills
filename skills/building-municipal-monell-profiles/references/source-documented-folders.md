# Source-documented municipal-profile folders

Prerequisite resolution opens no source-documented folder. It consumes only the
trusted host's exact state records described in `prerequisite-resolution.md` and
returns a plan for one later invocation.

Profile compilation reads ordinary files only from the seven declared recursive
read-only input folders. Each selected institutional source uses a
folder-relative path and adjacent domain-owned YAML with matching SHA-256,
source identity, type, date, and limitations.

Upstream policy-catalog, policy-assessment, and verified-authority folders
remain ordinary validated files. Their passing results and folder fingerprints
must match before use. Input YAML cannot add roots or capabilities.

Every resolver, collection, analysis, assessment, and compilation operation has
its own explicit output folder. The trusted host uses that operation's
`<output-folder>/temp/` for every temporary byte and publishes only beneath the
explicit output folder. One operation's resulting ordinary folder may become a
later input only through a new invocation that declares it as recursive
read-only input. Network or fee authority never transfers between operations.
