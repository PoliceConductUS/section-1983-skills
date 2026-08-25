# case-workspace-start-guide Specification Delta

## ADDED Requirements

### Requirement: The guide uses the invocation-owned temp workspace

The canonical folder-operation guide MUST tell the caller to provide one
absolute output-folder path or ask for it before execution. It MUST state that
`<output-folder>/temp/` is the invocation's only transient workspace and that
the trusted host configures semantic-work `cwd`, `TMPDIR`, `TMP`, and `TEMP` to
that folder. It MUST distinguish transient `temp/` content from durable output
artifacts and MUST NOT authorize system temporary directories, repository
worktrees, input folders, ambient current directories, or undeclared paths.

#### Scenario: The output path is not supplied

- **WHEN** a folder-scoped operation has all semantic inputs but no explicit
  absolute output-folder path
- **THEN** the guide tells the skill to ask the caller for that path and stop
  until it is supplied

#### Scenario: The trusted host starts semantic work

- **WHEN** the guide's synthetic host-conformance operation starts
- **THEN** its working directory and process temporary variables select
  `<output-folder>/temp/` and its durable artifacts use other output-relative
  paths
