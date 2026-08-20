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

| Skill                              | Role                                                                                                                                                                       |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `section-1983-drafting`            | Entry point for document routing, deadlines, localization, authority sourcing, and the shared writing system.                                                              |
| `drafting-section-1983-rule-59e`   | Rule 59(e) filing contract for postjudgment amendment, relief-first structure, manifest error, and claim-specific nonfutility.                                             |
| `drafting-section-1983-complaints` | General complaint and amended-complaint pleading contract, including defendant-specific facts, qualified immunity, and Monell.                                             |
| `drafting-false-arrest-complaints` | False-arrest specialization derived from a manually reviewed complaint corpus: seizure timing, offense elements, actor roles, incorporated-material risk, and compression. |
| `drafting-for-judge-scholer`       | Judge-specific overlay for matters assigned to Judge Karen Gren Scholer.                                                                                                   |
| `rrd`                              | Generic Response Requirements Document planner; routes Section 1983 Rule 12 matters to the specialized RRD skills.                                                         |
| `rrd-rule12`                       | Base Rule 12 response-planning contract.                                                                                                                                   |
| `rrd-rule12-officers`              | Officer-motion specialization with claim-by-claim and officer-by-officer qualified-immunity analysis.                                                                      |
| `rrd-rule12-city`                  | Municipal-motion specialization with theory-specific Monell analysis.                                                                                                      |
| `audit-authorities`                | Final authority, pinpoint, posture, later-history, and clearly-established-law audit.                                                                                      |
| `horan-bad-words`                  | Final judge-facing plain-language and rhetoric review.                                                                                                                     |

The repository also contains `prd`, a standalone software-product planning utility. It does not participate in the legal-drafting workflow.

## How the skills compose

Load each applicable skill once. The more specific skill adds requirements; it does not replace source, authority, or court rules.

1. Start with `section-1983-drafting` for routing, localization, and writing rules.
2. For a Section 1983 Rule 59(e) filing, add `drafting-section-1983-rule-59e`.
3. For complaints, add `drafting-section-1983-complaints`.
4. For false-arrest, probable-cause, alternative-offense, arrest-timing, or incorporated-video issues, add `drafting-false-arrest-complaints`.
5. Add `drafting-for-judge-scholer` when Judge Scholer is assigned.
6. For a Rule 12 response plan, use `rrd-rule12` and then the officers or city specialization. Those planners hand amendment work back to the applicable complaint skills.
7. Before treating legal work as filing-ready, run `audit-authorities`, followed by the applicable writing-system pass and the required `horan-bad-words` edit pass. Every drafting skill requires that final pass; rerun it after a material authority-driven revision.

The ownership boundaries are deliberate: the umbrella routes; complaint skills establish pleading sufficiency; false-arrest and judge skills add issue-specific constraints; RRD skills organize motion responses; the authority and writing skills are final gates.

## Writing system

The core drafting skill enforces one merged writing system: Simplified
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
