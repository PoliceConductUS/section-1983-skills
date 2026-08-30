# Source-documented legal-authority collection folders

Read ordinary files only from the six declared recursive read-only input
folders. Legal questions, jurisdictions, hierarchies, dates, seeds, and approved
source systems remain domain-owned YAML and ordinary files. Each ordinary file
uses a folder-relative path. Inputs cannot add roots or capabilities.

Every retrieved ordinary file is proposed beneath the explicit output folder
with adjacent domain-owned YAML and matching SHA-256. The trusted host uses
`<output-folder>/temp/` for every temporary byte, performs only authorized
network access, and publishes through the shared output writer.

The resulting source-documented folder is not verified authority. It may become
a later input only through a new `audit-authorities` invocation with its own
declared folder contract.
