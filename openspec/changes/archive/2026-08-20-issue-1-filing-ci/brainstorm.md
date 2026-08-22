## Design Summary

Add one public `filing-ci` skill that orchestrates a project's configured
filing-integrity checker. The skill runs after material drafting changes and
again before any filing-readiness statement. It delegates all deterministic
validation to the configured checker, returns checker findings to the drafting
loop, and keeps the filing gate open when configuration, execution, required
inputs, or hard findings remain unresolved.

The skill is an orchestration contract, not a Python checker. It resolves the
controlling draft, checker invocation, verified-authority root, and output
location from project instructions, configuration, or explicit user input. It
does not assume command flags, invent paths, edit the filing, or recreate
deterministic checks in prose.

Behavior will be tested at the installed-skill seam with fresh-context agents
and synthetic projects. A fake checker at the external process boundary will
exercise success, unavailable-checker, hard-finding, missing-authority-root, and
no-silent-edit scenarios.

## Alternatives Considered

### Option A: Thin configured orchestration skill

- **Approach**: Add a skill that resolves and runs the exact project-configured
  checker invocation, explains its result classes, and controls the
  filing-readiness gate.
- **Advantages**: Matches this repository's ownership boundary, remains
  portable, and lets the deterministic tool evolve behind its own interface.
- **Disadvantages**: A project without a configured checker remains blocked.
- **Why chosen**: This is the issue's stated outcome and the smallest complete
  behavior that belongs in this repository.

### Option B: Reimplement checks in the skill

- **Approach**: Describe citation, paragraph, docket, appendix, and gate checks
  as agent instructions.
- **Advantages**: Appears usable before the external checker exists.
- **Disadvantages**: Produces nondeterministic duplicate logic, drifts from the
  checker, and could falsely describe a filing as validated.
- **Why not chosen**: It violates the thin-wrapper boundary and the acceptance
  criterion requiring execution of the configured tool.

### Option C: Defer the skill until the checker repository exists

- **Approach**: Add no skill until Issues 2 and 3 expose stable tooling.
- **Advantages**: Avoids defining orchestration before the executable ships.
- **Disadvantages**: Leaves no explicit filing gate or portable integration
  contract for projects that already have an internal checker.
- **Why not chosen**: The wrapper can fail closed today without inventing the
  external tool's command-line interface.

## Agreed Approach

Use Option A. Create only `skills/filing-ci/SKILL.md` plus the README routing
entry. The skill will treat the project's configured invocation as opaque and
authoritative. It may interpret documented exit status and checker findings, but
it will not infer unconfigured flags or substitute agent judgment for a checker
result.

## Key Decisions

- `filing-ci` is the skill name.
- A material drafting change invalidates the prior Filing CI result.
- The skill runs after each material drafting change and immediately before a
  filing-readiness statement.
- Configuration is resolved from repository instructions, project configuration,
  or an explicit user-supplied invocation, in that order.
- If the project configures a verified-authority root, the checker invocation
  must use that root. If the checker configuration cannot express it, the gate
  remains open.
- Missing checker configuration, an unavailable executable, an unreadable draft,
  an unresolved required input, malformed checker output when a format is
  promised, or any unresolved hard finding blocks filing readiness.
- Warnings remain visible and return to the drafting loop according to the
  checker's own severity contract; the skill does not silently downgrade them.
- The skill never edits the controlling draft or creates project paths.
- The first implementation will not add a checker, authority store, formatter,
  or compatibility adapter to this repository.

## Open Questions

None. The external executable's flags and output schema remain owned by project
configuration and the future filing-toolchain repository.
