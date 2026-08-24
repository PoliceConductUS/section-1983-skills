---
name: drafting-section-1983-rule-59e
description:
  Use when drafting, revising, or auditing a Rule 59(e) filing in a federal
  Section 1983 case, especially for postjudgment amendment, futility, Rule 12
  inferences, qualified immunity, Monell pleading, or appellate-record clarity.
---

# Drafting Section 1983 Rule 59(e) Filings

## Folder-scoped execution

Contract: [folder contract](references/folder-contract.json).

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.

## Folder inputs and output

- `record` contains the operative judgment record, chronology, and claim facts.
- `authorities` contains approved Rule 59(e), amendment, and merits authorities.
- `filing` contains any motion, brief, proposed pleading, or related artifact.

Target is optional in `filing`; without one, draft the user-requested package
from the supplied roles. Internet is `disabled`. Return each requested filing
artifact with a canonical output-relative path and deterministic bytes; only the
trusted host may publish it append-immutable. Report missing record, authority,
requested relief, or package material as a gap without inventing a versioning
scheme.

## Purpose

Build one genuine request for district-court relief. When the case strategy
makes appellate-record clarity the controlling objective, make the filing
self-contained and reviewable without announcing that appeal preparation is its
purpose.

Read:

- [references/postjudgment-amendment-contract.md](references/postjudgment-amendment-contract.md)
  for every postjudgment amendment motion; and
- [references/appellate-record-contract.md](references/appellate-record-contract.md)
  when preservation, reviewability, supersession, or an expected denial matters.

## Required skill stack

Use `section-1983-drafting` first for strategy, localization, sources, and plain
language. Read its writing-system reference before drafting.

Add when applicable:

- `drafting-section-1983-complaints` for the proposed complaint;
- `drafting-false-arrest-complaints` for arrest timing, probable cause,
  alternative offenses, video, or intermediary causation;
- the assigned-judge drafting skill;
- `studying-rule-59e-decisions` when researching governing cases or
  judge-specific Rule 59 practice;
- `audit-authorities` before filing-readiness; and
- `horan-bad-words` after the substantive and authority work and after each
  material revision.

The specific skill adds requirements. It does not relax the case strategy, court
rules, source gates, or authority gates.

## Controlling objective

A cold reader should be able to identify:

1. the ruling challenged;
2. the governing Rule 59(e), Rule 15(a), and Rule 12 standards;
3. the amendment procedure used before judgment;
4. the proposed pleading the court did not test;
5. each precise manifest error asserted; and
6. the full, partial, and claim-specific rulings requested.

Rule 59(e) supplies the vehicle for reopening the judgment. Rule 15(a) supplies
the amendment considerations when governing law makes them applicable. Rule 12
supplies the futility test. Present one decisional path without merging those
legal functions.

## Source and posture gates

Before drafting, identify and read:

1. the judgment and the order or recommendation it adopted;
2. the operative complaint;
3. the dismissal motions and filed responses;
4. objections and their supporting brief;
5. every amendment request and court instruction about amendment;
6. the complete proposed amended complaint;
7. the current strategy, fact lock, claim ledger, gap register, and authority
   audit;
8. local rules, standing orders, page limit, conference requirement, and
   deadline; and
9. canonical verified sources for every load-bearing authority and record
   quotation.

Treat the artifact names in item 7 as roles, not mandatory filenames. If the
declared inputs contain no formal fact lock, claim ledger, gap register, or
authority audit, use the available equivalents and create a minimal in-memory
working table for the missing role. Do not invent a path or imply that an
artifact was reviewed. The minimum substitutes are: a dated chronology and
source list; a claim-by-defendant disposition table; an unresolved-fact and
source list; and an authority-status ledger. Follow `section-1983-drafting` for
a missing strategy: report the gap and ask the user for one or for permission to
proceed without one.

Before using material developed or located near the filing deadline, apply the
evidence-maturity and source-use gate in the postjudgment-amendment contract. Do
not let a new analysis obscure when its underlying facts or data were available.

Do not infer a defect the court did not identify. For a collectively dismissed
theory, state that no claim-specific defect was identified when accurate and
request a claim-specific ruling.

## Relief-first contract

The first paragraph states:

- the order to change;
- the procedural status after relief;
- the pleading to accept; and
- narrower alternative relief.

Name the Rule 59(e) ground in the introduction and in the application that
establishes it. Do not leave “manifest error” only in the standards section.

## Reviewable error unit

For each asserted error, state:

1. challenged ruling;
2. governing standard;
3. record location showing preservation;
4. proposed-pleading location that matters; and
5. requested ruling.

Develop an underlying merits issue only when it establishes manifest error,
answers an identified futility ground, shows the complete pleading is not
necessarily futile, or preserves a claim-specific ruling.

## Division of labor: brief, crosswalk, and Exhibit A

Exhibit A is the primary substantive pleading artifact. The brief should not
conduct a substantial narrative merits analysis of every proposed claim and
defendant.

Maintain a complete internal claim-by-defendant futility audit, including both
qualified-immunity prongs and each Monell path. In the filed brief:

1. explain the procedural error;
2. include a concise ruling-to-pleading crosswalk;
3. develop only the smallest set of strongest examples needed to show that
   Exhibit A is not necessarily futile; and
4. request a claim-specific ruling for every claim denied leave.

Add extended claim analysis only when needed to answer a dispositive defect the
court identified and the answer is not apparent from Exhibit A and the
crosswalk.

### Brief-level crosswalk

| Claim or ruling unit | FCR finding or identified defect, with record cite | Exhibit A response, with exact paragraph cites | Requested ruling |
| -------------------- | -------------------------------------------------- | ---------------------------------------------- | ---------------- |

The crosswalk accounts for every claim for which relief is sought. Separate
defendants when the ruling or cure differs; otherwise group them. Direct the
court to the complaint's claim and fair-warning units. Do not reproduce the
internal element audit, qualified-immunity analysis, factual narrative, or case
stack in the table.

Use one row per count, defendant, and legal theory when the dismissal ground,
challenged conduct, cure, immunity treatment, or requested ruling differs. Use a
separate row for each Monell path with a different policy or custom, municipal
attribution, notice, injury, or moving-force theory. Group only units identical
on those fields.

## Anti-replay gate

Compare the draft with the dismissal responses and objections. Each repeated
merits paragraph must perform at least one postjudgment function:

- establish manifest error;
- explain the pre-judgment amendment sequence;
- identify how Exhibit A changes the pleading tested;
- demonstrate nonfutility through a strongest example; or
- preserve a requested claim-specific ruling.

Delete repetitions that perform none of those functions. Correctness alone does
not justify replay.

## Amendment-procedure and alternative-ground audit

When the court prescribed a cure method:

1. quote the instruction;
2. show compliance;
3. quote the prior request to lodge or file the complete pleading;
4. acknowledge any implicit denial created by judgment; and
5. explain why the futility ruling did not test the complete pleading.

Do not call Exhibit A newly discovered merely because it was completed after
judgment. Address every apparent Rule 15 ground that could independently support
denial, including delay, bad faith, prior cure opportunities, prejudice, and
futility. Distinguish a pre-judgment request or court-prescribed procedure from
a first request made only after judgment.

## Corpus evidence gate

Use judge-specific Rule 59 observations only when supported by a current,
versioned corpus produced under `studying-rule-59e-decisions`. Identify
authorship, posture, denominator, sample limits, and primary source. Treat
documented judge practices as drafting information, not authority or prediction.
Governing binding authority controls.

If the corpus does not support an issue-specific tendency, say that it adds no
judge-specific information for that issue and omit the proposed tendency. An
incomplete retrieval set may supply verified examples only.

## Requested-ruling branches

The motion, brief, and proposed order request:

1. vacatur, reopening, and filing of Exhibit A;
2. alternatively, amendment as to every claim not found futile; and
3. for each denied claim, a claim- and defendant-specific ruling identifying the
   deficient element or immunity prong.

Do not characterize claims excluded from a court-directed conformed complaint as
voluntarily abandoned.

Use one branched proposed order with a compact claim-disposition schedule unless
local practice requires separate proposed orders.

## Packet and version contract

Generate the documents required by the court and strategy, commonly the motion,
brief, complete proposed complaint, proposed order, appendix, exhibit
instructions, accurate conference certificate, and internal audits.

Return each changed document as a new canonical output-relative artifact and
identify which supplied filing artifacts remain unchanged. The trusted host
records hashes and publishes every returned artifact append-immutable. Never
overwrite a prior filing or invent numbered folders, manifests, or source
schemas as legal requirements.

## Appendix and final-render traceability

Localize the appendix rule before drafting. When an appendix accompanies the
motion, apply these gates to the filed brief:

1. Every assertion about documentary or non-documentary material must cite each
   appendix page that supports it when the applicable rule requires appendix
   citations.
2. A docket citation may identify the source, but it does not replace a required
   appendix-page citation.
3. Every record quotation, preservation assertion, procedural date, and
   amendment request used in the argument must map to the appendix index and the
   cited page.
4. Do not cite an appendix page that does not contain the proposition. Do not
   rely on a record page omitted from the appendix when the applicable rule
   requires its inclusion.
5. After the appendix and brief are final, audit the citations from both
   directions: every appendix citation resolves to the correct page, and every
   load-bearing appendix page is cited where the brief uses it.

Maintain a sentence-level appendix-support matrix with these fields:

`brief line or sentence | documentary assertion | docket source and page | every supporting appendix page | status`.

For every assertion about an event during a recorded interval, verify that the
asserted event or conduct is visible in the video itself. For every quoted,
paraphrased, or attributed recorded statement, verify that the statement appears
in the verified transcript; exact quotations must match exactly, paraphrases may
not add content, and uncertain speaker attribution must remain uncertain. An
assertion that the available recordings do not verify may pass only when the
filed text identifies it as based on Plaintiff's present recollection, states
that the recordings presently available do not resolve the point, and states
that the assertion is subject to correction if additional recordings are
produced or located. Never present that recollection-based assertion as
established by the recording. Fail packet validation when neither the
recording-verification route nor this express present-recollection route is
satisfied.

Reject a row when a required appendix citation is missing, when the brief gives
only a docket citation, when any relied-on source page is absent from the
appendix, or when the cited appendix page does not support the assertion. Any
appendix rebuild invalidates the prior matrix and requires a new page-by-page
audit against the rebuilt PDF.

Treat pagination-dependent requirements as final-render gates. Populate the
table of contents and table of authorities with the page references from the
final rendered brief. Do not leave blank or estimated page fields in a filing
candidate. Put any required generative-AI disclosure in the location and form
required by the rules effective on the filing date.

## Final review

Reject the packet unless:

1. the opening states the requested result and exact Rule 59 ground;
2. Rule 59(e), Rule 15(a), and Rule 12 remain one visible but legally distinct
   chain;
3. the pre-judgment amendment sequence is supported by exact record cites;
4. Exhibit A is the primary substantive artifact;
5. every requested claim appears in the concise crosswalk;
6. narrative nonfutility analysis is limited to the strongest necessary
   examples;
7. every merits paragraph passes the anti-replay gate;
8. every apparent independent amendment-denial ground is addressed;
9. full, partial, and claim-specific relief match across the motion, brief, and
   order;
10. the appellate-record audit passes when applicable;
11. every quotation, pinpoint, procedural statement, and authority status is
    verified;
12. every assertion about an event or conduct during a recorded interval is
    visible in the video itself or satisfies the express present-recollection
    route above, and every quoted, paraphrased, or attributed recorded statement
    appears in the verified transcript or satisfies that same route;
13. every late-window fact, statistic, record, and timestamp passes the
    evidence-maturity and source-use gate;
14. tables of authorities and rules match the final body and contain final,
    render-verified page references;
15. every required appendix-page citation passes the bidirectional traceability
    audit;
16. every required filing-date disclosure, including any generative-AI
    disclosure, appears in the required place and form;
17. the writing-system lint and `horan-bad-words` review pass; and
18. page limit, conference statement, and appendix pagination are verified; and
19. required input hashes, run manifests, and source records are verified.

Do not call the packet filing-ready while a load-bearing source, authority,
deadline, conference statement, proposed-complaint cross-reference, requested
ruling, or supersession effect remains unresolved.

## Independent quality-control stage

An independent quality-control stage is non-mutating. It may read designated
artifacts and return only its designated report or result for trusted-host
publication. It must not edit, overwrite, correct, regenerate, or otherwise
modify an artifact under review. A combined instruction to audit and fix does
not authorize same-stage mutation. Deadline pressure, sunk cost, claimed prior
approval, and contrary workflow instructions do not override this boundary.
Recommendations, proposed language, corrections, and copy-ready replacements are
advisory only and do not authorize implementation. Remediation requires a
separately authorized drafting or revision stage. Create a new version when
versioning applies. A new read-only quality-control stage must verify the
remediated artifact. An internal self-check inside an explicitly authorized
drafting or revision stage may guide edits within that stage, but it is not an
independent quality-control result.

Before review, an independent quality-control stage must select exactly one
artifact through its declared input roles and target policy. It must propose
exactly one unique append-immutable output-relative report beneath the
caller-declared output folder. A missing, ambiguous, nonexistent, or out-of-role
target must fail closed without a fallback write. The report path must reject
absolute paths, traversal, symlink escapes, and existing destinations. Only the
trusted host may publish the report through the shared output boundary. The
trusted host accepts quality-control publication only from an invocation bound
to the installed skill's target policy and approved target roles; it rejects an
unbound invocation or a target outside those approved roles.

Prior quality-control reports must not become implicit input. A report may be
reviewed only when that exact report is expressly present in a declared input
role and selected consistently with the reviewing skill's target policy. The
reviewing stage must propose a different new append-immutable report for
trusted-host publication. Existing reports are immutable and must not be edited,
overwritten, replaced, renamed, or deleted.

The trusted host derives the report path as
`quality-control-reports/<check-kind>-<utc-run-time>-<run-id>.md` and publishes
exactly one report through the shared output writer. Generated reports beneath
`quality-control-reports/` are excluded from the reviewed-input manifest and
fingerprint unless one exact report is the explicit target; selecting one report
does not include sibling or older reports. The canonical quality-control
metadata envelope identifies a generated report even when the report directory
itself is a declared input root. A quality-control run ID must be a canonical
lowercase UUIDv4; weak, malformed, or reused identities fail closed before
publication.

The trusted host prefixes the report with the canonical quality-control metadata
envelope containing the skill and version, filtered logical input roles and
reviewed artifact hashes, selected target role, relative path, SHA-256
fingerprint, and byte size, quality-control kind, UTC run time, run ID, scope,
approved source identities, result, failed findings, passing-but-suboptimal
recommendations, and terminal run-manifest identity. The skill returns report
content and structured findings; it does not build the canonical metadata
envelope or publish output.

The quality-control run is complete only after both report bytes and the
terminal success manifest are durable and incomplete state is absent. Separate
failed findings from passing-but-suboptimal observations. Recommendations,
proposed language, and copy-ready replacements for failures or
passing-but-suboptimal observations are advisory and do not authorize
implementation.
