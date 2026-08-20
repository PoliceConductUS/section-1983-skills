# section-1983-skills

Agent skills for drafting and editing documents in Section 1983 pro se plaintiff
cases. Each skill lives under `skills/<name>/SKILL.md` in the open Agent Skills
format, so it works in Claude Code, Claude.ai, Cursor, Codex, and any other
agent that reads `SKILL.md`.

## Install

Install into your agent with the
[skills CLI](https://github.com/vercel-labs/skills):

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

| Skill                                             | Role                                                                                                                                                                       |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `adversarial-filing-review`                       | Independent clean-room adversarial review of a canonical Section 1983 filing, with read-only categorized findings and plaintiff-reserved strategy decisions.               |
| `section-1983-drafting`                           | Entry point for document routing, deadlines, localization, authority sourcing, and the shared writing system.                                                              |
| `drafting-section-1983-declarations-and-evidence` | Source-bounded factual declarations, statement classification, exhibit-foundation prompts, and human approval status for summary judgment.                                 |
| `drafting-section-1983-rule-59e`                  | Rule 59(e) filing contract for postjudgment amendment, relief-first structure, manifest error, and claim-specific nonfutility.                                             |
| `drafting-section-1983-complaints`                | General complaint and amended-complaint pleading contract, including defendant-specific facts, qualified immunity, and Monell.                                             |
| `drafting-false-arrest-complaints`                | False-arrest specialization derived from a manually reviewed complaint corpus: seizure timing, offense elements, actor roles, incorporated-material risk, and compression. |
| `drafting-section-1983-written-discovery`         | Mapped and bounded requests for production, interrogatories, and requests for admission without assumed evidence or selected service strategy.                             |
| `auditing-section-1983-discovery-responses`       | Request-by-request audit of discovery responses, objections, production, withholding, deficiencies, and supported cures.                                                   |
| `drafting-section-1983-meet-and-confer`           | Neutral meet-and-confer correspondence from a completed discovery-response audit, with a separate factual conference record.                                               |
| `auditing-section-1983-privilege-logs`            | Source-bounded privilege-log requirements and entry audit without invented metadata, privilege adjudication, or automatic waiver.                                          |
| `drafting-section-1983-deposition-outlines`       | Chronology- and element-gap-driven deposition outlines that ask grounded questions without scripting testimony.                                                            |
| `drafting-for-judge-scholer`                      | Judge-specific overlay for matters assigned to Judge Karen Gren Scholer.                                                                                                   |
| `studying-rule-59e-decisions`                     | Evidence-coded research contract for governing Rule 59 law, judge-specific decision corpora, denominator limits, and transfer cards.                                       |
| `rrd`                                             | Generic Response Requirements Document planner; routes Section 1983 Rule 12 matters to the specialized RRD skills.                                                         |
| `rrd-rule12`                                      | Base Rule 12 response-planning contract.                                                                                                                                   |
| `rrd-rule12-officers`                             | Officer-motion specialization with claim-by-claim and officer-by-officer qualified-immunity analysis.                                                                      |
| `rrd-rule12-city`                                 | Municipal-motion specialization with theory-specific Monell analysis.                                                                                                      |
| `audit-authorities`                               | Final authority, pinpoint, posture, later-history, and clearly-established-law audit.                                                                                      |
| `horan-bad-words`                                 | Final judge-facing plain-language and rhetoric review.                                                                                                                     |
| `filing-ci`                                       | Orchestrates a project-configured deterministic filing-integrity checker and its fail-closed filing gate.                                                                  |

## How the skills compose

Load each applicable skill once. The more specific skill adds requirements; it
does not replace source, authority, or court rules.

1. Start with `section-1983-drafting` for routing, localization, and writing
   rules.
2. For factual declarations and exhibit-foundation preparation supporting
   summary judgment, add `drafting-section-1983-declarations-and-evidence`.
3. For a Section 1983 Rule 59(e) filing, add `drafting-section-1983-rule-59e`.
4. For complaints, add `drafting-section-1983-complaints`.
5. For false-arrest, probable-cause, alternative-offense, arrest-timing, or
   incorporated-video issues, add `drafting-false-arrest-complaints`.
6. Add `drafting-for-judge-scholer` when Judge Scholer is assigned.
7. For a Rule 12 response plan, use `rrd-rule12` and then the officers or city
   specialization. Those planners hand amendment work back to the applicable
   complaint skills.
8. For discovery, use `drafting-section-1983-written-discovery`,
   `auditing-section-1983-discovery-responses`,
   `drafting-section-1983-meet-and-confer`,
   `auditing-section-1983-privilege-logs`, or
   `drafting-section-1983-deposition-outlines` for its named task. The existing
   drafting entrypoint supplies routing and the shared coordination contract;
   each peer remains independently usable.
9. Before treating legal work as filing-ready, run `audit-authorities`, followed
   by the applicable writing-system pass and the required `horan-bad-words` edit
   pass. Every drafting skill requires that final pass; rerun it after a
   material authority-driven revision.
10. Run `adversarial-filing-review` in a fresh clean-room context after
    substantive, authority, and writing review. Any approved correction returns
    to a separate drafting workflow and requires a new independent review.
11. Run `filing-ci` after the applicable prose and authority audits, after each
    material change, and immediately before a filing-readiness statement. A
    current Filing CI pass does not replace authority or writing review; those
    remain independent gates.

The ownership boundaries are deliberate: the umbrella routes; complaint skills
establish pleading sufficiency; false-arrest and judge skills add issue-specific
constraints; RRD skills organize motion responses; discovery peers draft or
audit only their named artifacts; the authority and writing skills are final
gates, and Filing CI adds a separate configured integrity gate.

## Project inputs and portability

The skills describe artifact roles, not a required case-management product.
Projects may use different filenames or keep the same information in one
document. When a skill calls for a strategy, chronology or fact lock, claim
ledger, gap register, authority library, or coded corpus:

- use the project's existing equivalent;
- do not invent a file or imply that a missing artifact was reviewed;
- ask before drafting without a strategy; and
- create a minimal internal working table for other missing roles when the
  document can still be prepared from verified sources.

Localization results belong in a project-defined cache or returned internal
audit, not inside an installed skill package. Numbered packet folders,
manifests, hashes, and source records apply only when the user's project already
uses them.

Judge-specific observations are optional. If the reviewed corpus does not
support an issue-specific conclusion, the judge overlay contributes no
judge-specific proposition for that issue.

## Writing system

The core drafting skill enforces one merged writing system: Simplified Technical
English mechanics combined with the editing discipline of legal writing guides.
Bans from all sources stack. Where the sources' advice conflicts, the ASD-STE100
spec controls. See `skills/section-1983-drafting/references/writing-system.md`.

## Formatting

Markdown is formatted with [Prettier](https://prettier.io) using the settings in
`.prettierrc.yaml` (`proseWrap: always`, with Prettier's default 80-character
width):

```bash
# Format everything in the repository
npx prettier --write .

# Check formatting without writing changes
npx prettier --check .
```

## Contributing

See `CONTRIBUTING.md`. `main` is the stable release branch. Develop changes on
feature branches, merge only after the required validation passes, and tag each
release. Installation pulls the current stable branch, and users update with
`npx skills update`.

## Disclaimer

These skills help structure and edit documents. They are not legal advice, and
no skill output substitutes for a lawyer's judgment about whether, where, or
what to file.
