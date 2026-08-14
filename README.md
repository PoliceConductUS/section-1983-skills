# section-1983-skills

Agent skills for drafting and editing documents in Section 1983 pro se
plaintiff cases. Each skill lives under `skills/<name>/SKILL.md` in the open
Agent Skills format, so it works in Claude Code, Claude.ai, Cursor, Codex,
and any other agent that reads `SKILL.md`.

## Install

Install into your agent with the [skills CLI](https://github.com/vercel-labs/skills):

```bash
# Interactive: pick skills and target agents
npx skills add PoliceConductUS/section-1983-skills

# A specific skill, non-interactive, into Claude Code
npx skills add PoliceConductUS/section-1983-skills --skill section-1983-drafting -a claude-code -y

# List what this repository offers
npx skills add PoliceConductUS/section-1983-skills --list

# Update installed skills later
npx skills update
```

## Skills

| Skill                   | What it does                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `section-1983-drafting` | Drafts and edits any filing in a § 1983 case (complaints, motion-to-dismiss and summary judgment responses, extension and leave-to-amend motions, R&R objections and responses) in a unified plain-language writing system, with per-document federal skeletons, a district localization protocol, a citation-sourcing protocol, a consolidated banned-word list, and a deterministic linter. |

## Writing system

The complaint skill enforces one merged writing system: Simplified
Technical English mechanics combined with the editing discipline of legal
writing guides. Bans from all sources stack. Where the sources' advice
conflicts, the ASD-STE100 spec controls. See
`skills/section-1983-drafting/references/writing-system.md`.

## Contributing

See `CONTRIBUTING.md`. Every push to `main` is a release: installation
always pulls the latest commit, and users update with `npx skills update`.

## Disclaimer

These skills help structure and edit documents. They are not legal advice,
and no skill output substitutes for a lawyer's judgment about whether,
where, or what to file.
