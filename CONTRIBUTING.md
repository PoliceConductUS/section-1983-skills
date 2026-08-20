# Contributing

Contributions of new skills and improvements to existing skills are welcome.
Every skill in this repository serves one audience: pro se plaintiffs in Section
1983 cases. Keep that reader in mind. They are smart, unrepresented, and judged
on their filings.

## Change workflow

Use one story per stacked branch. Write the RED failing test before GREEN
implementation. Refactor only while the tests remain green. Complete OpenSpec
design, tasks, verification, retrospective, and archive artifacts.

Automation must not silently select plaintiff decisions, litigation strategy, or
legal conclusions. Follow [GOVERNANCE.md](GOVERNANCE.md).

Measurement is feedback, never a verdict. Score deltas and judgment-based
evaluations prompt review and do not decide legal quality, filing readiness, or
human judgment.

Prefer self-documenting code. Refactor before adding a comment. A necessary
comment is short and clear and references an ADR or recorded decision when
practical.

Run `npm run validate` before release. A push to `main` is not publication.
Release only with immutable semantic-version tags. Follow
[PUBLISHING.md](PUBLISHING.md).

The validator checks deterministic boundaries, not subjective prose, comment,
test, or legal quality.

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md` with `name` and `description` in the
   YAML frontmatter. The description is the trigger: state what the skill does
   and the situations in which an agent should reach for it.
2. Keep `SKILL.md` under 500 lines. Put long material in `references/` and
   deterministic steps in `scripts/`.
3. Follow the writing system. Prose in every skill obeys
   `skills/section-1983-drafting/references/writing-system.md`, including the
   precedence rule: bans stack, and where advice conflicts, ASD-STE100 controls.
4. Add the skill to the table in `README.md`.
5. Read [GOVERNANCE.md](GOVERNANCE.md) and add exactly one matching entry to
   `governance/rules-provenance.json`. Keep its review date and rationale
   current; bundled-rule entries need approved source IDs and a checked
   jurisdiction reference, while runtime-sourced entries describe the actual
   source identity and checked date exposed in their output.

## Improving a skill

Open an issue first for changes to the writing system or the banned-word
inventory, since those are shared policy. Fixes to structure references,
scripts, and tests can go straight to a pull request.

Changes to a protected gate named in [GOVERNANCE.md](GOVERNANCE.md) must name
the affected gate and rationale in the pull-request template and request
explicit human review before acceptance.

## Scripts

Scripts use the Python standard library only, so an installed skill runs with no
package installation. Write tests first. Existing conventions: no abbreviations
in names, no data types in names, pure functions, and dictionary dispatch
instead of if statements.

Run the tests before every push:

```bash
python3 -m unittest discover skills/section-1983-drafting/scripts
npx skills add . --list
```

Also run the `skill-creator` runtime's `quick_validate.py` against every
`skills/*/` directory that contains `SKILL.md`. Every skill must pass before
review.

New document types are new skeletons under
`skills/section-1983-drafting/references/documents/`, following the existing
pattern: deadline first, standard of review in the law's voice, skeleton,
discipline rules. District-specific knowledge goes in
`references/jurisdictions/` via the localization protocol, never into the
federal skeletons.

## What does not belong here

- Explanatory text from copyrighted books. Word lists carry the bans; the
  explanations in this repository must be original.
- Legal advice. Skills structure and edit documents. They do not decide whether,
  where, or what to file.
- Skills unrelated to Section 1983 practice. Start a separate repository in the
  organization instead.
