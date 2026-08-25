# section-1983-skills

Agent skills for drafting and editing documents in Section 1983 pro se plaintiff
cases. Each skill lives under `skills/<name>/SKILL.md` in the open Agent Skills
format, so it works in Claude Code, Claude.ai, Cursor, Codex, and any other
agent that reads `SKILL.md`.

## Install

Install into your agent with the
[skills CLI](https://github.com/vercel-labs/skills):

The commands below pin release `v0.1.0`. A pinned install never follows the
moving `main` branch.

```bash
# Interactive: pick skills and target agents
npx skills add https://github.com/PoliceConductUS/section-1983-skills/tree/v0.1.0

# A specific skill, non-interactive, into Claude Code
npx skills add https://github.com/PoliceConductUS/section-1983-skills/tree/v0.1.0 --skill section-1983-drafting -a claude-code -y

# List what this repository offers
npx skills add https://github.com/PoliceConductUS/section-1983-skills/tree/v0.1.0 --list
```

To upgrade deliberately, choose a newer published tag from
[Releases](https://github.com/PoliceConductUS/section-1983-skills/releases),
replace `v0.1.0` in the install command, and run it again. Do not substitute a
branch name: tags are the immutable release identity.

## Folder-scoped invocation

Every invocation receives fixed recursive read-only input folders and one
caller-selected absolute output folder. If the output path is missing, ask the
caller for it before beginning work. Durable artifacts and run receipts are
written only beneath that output folder.

The trusted host reserves `<output-folder>/temp/` as the invocation's only
temporary workspace. It uses that folder for staging, intermediate files,
scratch files, the semantic-work current directory, and `TMPDIR`, `TMP`, and
`TEMP`. It does not use a system temporary directory, repository worktree, input
folder, ambient current directory, or undeclared path for invocation temporary
work. `temp/` is not a durable artifact destination.

## Skills

| Skill                                             | Role                                                                                                                                                                       |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `adversarial-filing-review`                       | Independent clean-room adversarial review of a canonical Section 1983 filing, with read-only categorized findings and plaintiff-reserved strategy decisions.               |
| `building-litigation-alignment-overlays`          | Immutable docket-derived defendant alignment, adversary attack, plaintiff-response, judicial-treatment, review-plan, and filing-manifest overlays.                         |
| `building-defense-counsel-overlays`               | Immutable professional defense-attorney identity, counsel-team behavior, court-treatment, and calibrated next-move overlays from approved public sources.                  |
| `section-1983-drafting`                           | Entry point for document routing, deadlines, localization, authority sourcing, and the shared writing system.                                                              |
| `drafting-section-1983-declarations-and-evidence` | Source-bounded factual declarations, statement classification, exhibit-foundation prompts, and human approval status for summary judgment.                                 |
| `drafting-section-1983-rule-59e`                  | Rule 59(e) filing contract for postjudgment amendment, relief-first structure, manifest error, and claim-specific nonfutility.                                             |
| `drafting-section-1983-complaints`                | Canonical owner of the complete general complaint skeleton, detailed count contract, and packaged install-local mechanical check.                                          |
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
| `filing-ci`                                       | Runs registered packaged deterministic filing checks and preserves a fail-closed filing gate.                                                                              |

## How the skills compose

Load each applicable skill once. The more specific skill adds requirements; it
does not replace source, authority, or court rules.

Composition is sequential: the trusted host validates and invokes each skill
separately against that installed skill's exact folder contract. It never unions
roles across the stack or enlarges one skill's filesystem or internet authority.
Output from one skill is available to another only through a new invocation that
expressly supplies it in the receiving skill's declared input role.

Multi-document filing workflows use
[folder-backed FilingPackets](FILING_PACKETS.md): ordinary files plus one strict
manifest that fixes member identity, order, kind, packet role, path, hash, and
revision provenance. Source packets remain read-only; the trusted host publishes
a complete new packet beneath the explicit output folder.

Profile, overlay, and research-corpus workflows use
[immutable folder packages](FOLDER_PACKAGES.md): ordinary folders with one
complete hashed manifest, frozen member bytes, explicit freshness, and a
protected static-role boundary. These packages are folder-native and do not
depend on CaseGraph or Git.

1. Start with `section-1983-drafting` for routing, localization, and writing
   rules.
2. For factual declarations and exhibit-foundation preparation supporting
   summary judgment, add `drafting-section-1983-declarations-and-evidence`.
3. For a Section 1983 Rule 59(e) filing, add `drafting-section-1983-rule-59e`.
4. For complaints, add `drafting-section-1983-complaints`.
5. For false-arrest, probable-cause, alternative-offense, arrest-timing, or
   incorporated-video issues, add `drafting-false-arrest-complaints`.
6. Add `drafting-for-judge-scholer` when Judge Scholer is assigned.
7. Add `building-litigation-alignment-overlays` before an amended complaint,
   leave package, or other filing that should consume the current docket's
   actual adversary positions and judicial treatment.
8. Add `building-defense-counsel-overlays` when an actual-adversary review
   should consume validated professional history for the effective defense team.
   Keep that material out of the blind common-attack review.
9. For a Rule 12 response plan, use `rrd-rule12` and then the officers or city
   specialization. Those planners hand amendment work back to the applicable
   complaint skills.
10. For discovery, use `drafting-section-1983-written-discovery`,
    `auditing-section-1983-discovery-responses`,
    `drafting-section-1983-meet-and-confer`,
    `auditing-section-1983-privilege-logs`, or
    `drafting-section-1983-deposition-outlines` for its named task. The existing
    drafting entrypoint supplies routing and the shared coordination contract;
    each peer remains independently usable.
11. Before treating legal work as filing-ready, run `audit-authorities`,
    followed by the applicable writing-system pass and the required
    `horan-bad-words` edit pass. Every drafting skill requires that final pass;
    rerun it after a material authority-driven revision.
12. Run `adversarial-filing-review` in a fresh clean-room context after
    substantive, authority, and writing review. Any approved correction returns
    to a separate drafting workflow and requires a new independent review.
13. Run `filing-ci` after the applicable prose and authority audits, after each
    material change, and immediately before a filing-readiness statement. A
    current Filing CI pass does not replace authority or writing review; those
    remain independent gates.

For every complaint, `drafting-section-1983-complaints` must read its
install-local `references/complaint-contract.md` and
`references/complaint-structure-contract.json` before drafting, revision, or
audit. If the package or either reference is unavailable, the result is
**complaint contract unavailable** and complaint work stops; no routing or
specialization skill supplies a fallback.

For a false-arrest complaint, the required order is `section-1983-drafting`,
then `drafting-section-1983-complaints` with both canonical references, and then
`drafting-false-arrest-complaints` with its install-local false-arrest delta.

The ownership boundaries are deliberate: the umbrella routes; complaint skills
establish pleading sufficiency; false-arrest and judge skills add issue-specific
constraints; RRD skills organize motion responses; discovery peers draft or
audit only their named artifacts; the authority and writing skills are final
gates, and Filing CI adds a separate packaged integrity gate.

### Trusted adversarial-review runtime

Independent adversarial review uses the built-in stateless OpenAI runtime. The
declared `filing` role root supplies the filing bytes, and the declared
`approved-sources` role root supplies every approved packet source. A required
filing target selects one canonical relative file inside `filing`. Internet is
authorized for this provider dispatch. Set `OPENAI_API_KEY`, choose an explicit
model, build the bounded packet required by the skill, and run the install-local
processor:

```bash
python3 skills/adversarial-filing-review/scripts/launch_review.py \
  --trusted-openai \
  --model "$OPENAI_REVIEW_MODEL" \
  --filing-root "$FILING_ROOT" \
  --approved-sources-root "$APPROVED_SOURCES_ROOT" \
  --filing-target "$FILING_TARGET" \
  --internet-policy authorized \
  < "$REVIEW_PACKET"
```

The processor returns report bytes, a canonical output-relative artifact path,
and validated internet-source records. It accepts no arbitrary command or output
folder and writes nothing directly. Only the trusted host publishes the bytes
with `OutputRun` and records the append-immutable terminal receipt. A missing
credential, unavailable provider, or invalid response returns a bounded
unavailable report and a nonzero exit; it is not a completed independent review.

## Complaint checker boundary

The canonical JSON complaint contract drives the install-local
`scripts/check_complaint.py` mechanical checker. It does not decide fact truth,
legal sufficiency, authority fit, material analogy, strategy, or filing
readiness. Filing CI dispatches only checker IDs registered inside its installed
package; an absent, unknown, unavailable, or incompatible checker returns an
honest unavailable result. Neither helper accepts a command, executable, or
output folder, and only the trusted host publishes returned report bytes.

## Invocation inputs and portability

The skills consume named artifact roles, not a case-management product or
repository layout. Callers may use different filenames or keep related
information in one document, but each invocation exposes only the exact
recursive read-only folders declared for that skill. Missing strategy,
chronology, fact-lock, claim-ledger, gap-register, authority, or corpus material
is reported as a gap; the skill does not search another folder or imply that an
absent artifact was reviewed.

New users can follow [Run folder-scoped skill operations](FOLDER_OPERATIONS.md)
to map roles to input folders, select one output folder, and verify a synthetic
operation before using the drafting skills. Only the trusted host publishes
returned artifacts. Logical input hashes and run manifests are required for
every folder-scoped operation and bind the declared inputs to the terminal
output run. Caller-specific additional packet controls remain optional and
separate from the shared folder contract.

Judge-specific observations are optional. If the reviewed corpus does not
support an issue-specific conclusion, the judge overlay contributes no
judge-specific proposition for that issue.

[Create a judge overlay](JUDGE_OVERLAYS.md) explains the reusable corpus,
transfer, court-conduct, degradation, and anti-gaming method.

[Manage case overlays](OVERLAYS.md) explains when to create, reuse, refresh,
rebuild, supersede, validate, and pin judge, litigation-alignment, and later
counsel overlays.

[Build defense-counsel overlays](COUNSEL_OVERLAYS.md) explains professional
source hierarchy, attribution, time-bounded counsel teams, evidence strength,
calibrated forecasts, and counsel-specific lifecycle triggers.

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

See `CONTRIBUTING.md`. `main` is the integration branch, not a published
version. Develop changes on feature branches and merge only after the required
validation passes. The release workflow validates the exact `main` commit before
creating its immutable semantic-version tag.

## Disclaimer

These skills help structure and edit documents. They are not legal advice, and
no skill output substitutes for a lawyer's judgment about whether, where, or
what to file.
