# Canonical Section 1983 complaint contract

This reference is the complete general contract for a federal Section 1983
complaint, amended complaint, or amendment proffer. A verified governing-court
requirement controls any necessary variation in form.

## Ordered document skeleton

Use each applicable section once and in this order:

1. Caption
2. Introduction (optional)
3. Jurisdiction and venue
4. Parties
5. Statement of Facts
6. Counts
7. Prayer for relief
8. Jury demand
9. Signature block

The caption identifies the court, parties, case number or placeholder, and
document title. Keep any introduction short, outcome-first, and factual. Use
lettered subparagraphs in the prayer for relief. The signature block must
satisfy Rule 11.

## Jurisdiction, venue, parties, and capacities

Plead federal-question and civil-rights jurisdiction under 28 U.S.C. § 1331 and
§ 1343(a)(3). When the complaint includes state-law claims, plead supplemental
jurisdiction under 28 U.S.C. § 1367(a). Plead venue under 28 U.S.C. § 1391(b) in
the district where a substantial part of the events occurred or where a
defendant resides.

For each defendant, identify the defendant's name, role, employer, capacity sued
in, and action under color of state law. Every Section 1983 claim requires facts
showing:

1. a person, whether an individual or a municipality through Monell;
2. action under color of state law;
3. deprivation of a right secured by the Constitution or federal law; and
4. proximate causation of the injury.

Identify the specific constitutional source in each count. For an
individual-capacity claim, plead each defendant's personal involvement. Do not
rely on respondeat superior. Plead what each named defendant did, saw, ordered,
or failed to do. For a supervisor, plead personal participation, a policy the
supervisor created, or deliberate indifference to known misconduct.

For an official-capacity or municipal claim, plead an official policy, a
widespread custom, a final-policymaker decision, or a failure to train amounting
to deliberate indifference. Plead supporting facts such as prior incidents,
complaint histories, training records, and the policymaker's identity when
applicable.

## Rule 8, Rule 10, Rule 11, facts, and incorporation

Rule 8(a) requires a short and plain statement. Rule 10(b) requires numbered
paragraphs limited to a single set of circumstances. Rule 11(b) requires
evidentiary support, or a specifically identified likelihood of evidentiary
support after discovery, for every factual contention.

Present the Statement of Facts in numbered paragraphs and chronological order.
When implicated, separate pre-seizure observations, the investigative encounter,
the arrest decision, the seizure, alleged resistance, force, continued custody,
and later reports or prosecution into distinct subsections or paragraph groups.
For each stage, identify the actor, what that actor knew then, and what that
actor did. Do not use later conduct or later-acquired information to justify an
earlier decision unless supported facts show the decisionmaker knew it then.
Limit each paragraph to one material event or one closely connected set of
circumstances within a stage.

Courts disregard legal conclusions and credit well-pleaded facts under _Ashcroft
v. Iqbal_ and _Bell Atlantic Corp. v. Twombly_. A legal conclusion may appear in
a count only after the facts support it. Track a controlling authority's wording
when reciting an element and cite the authority; do not substitute a looser
paraphrase.

Each count must incorporate only the numbered factual paragraphs relevant to
that count. Identify every incorporated paragraph by a valid paragraph number or
range. Do not incorporate all preceding allegations indiscriminately, and do not
make the reader assemble an element from unrelated sections.

## One mapping for every count tuple

Create one count mapping for every claim-defendant-capacity tuple, then complete
it separately for each challenged act. Two defendants or two challenged acts on
the same claim require separately complete mappings. The mapping is the
count-level drafting and audit record; the filed count may express its functions
in concise paragraphs rather than labels or a table.

### Canonical claim–defendant–challenged-act checklist

Record the following fields in this order:

1. Count ID or identifier (`count_id`)
2. Claim (`claim`)
3. Constitutional source (`constitutional_source`)
4. Defendant (`defendant`)
5. Capacity (`capacity`)
6. Challenged act (`challenged_act`)
7. Event stage (`event_stage`)
8. Governing element and standard (`standard`)
9. Standard pinpoint or pincite (`standard_pincite`)
10. Decisive facts (`decisive_fact_paragraphs`)
11. Incorporated paragraphs (`incorporated_paragraphs`)
12. Relevant-time knowledge (`relevant_time_knowledge`)
13. Element-specific legal application (`application`)
14. Injury (`injury`)
15. Relief (`relief`)
16. Result (`result`)
17. Qualified-immunity applicability and analysis unit (`qualified_immunity`)
18. Separated municipal-liability path collection (`monell_paths`)

When qualified immunity applies to the mapping, also record these conditional
fields:

1. Event date (`event_date`)
2. Conduct-specific right or rule (`precise_right`)
3. Governing jurisdiction (`jurisdiction`)
4. Prong one result (`prong_one_result`)
5. Prong two result (`prong_two_result`)
6. Verified binding pre-event authority (`binding_pre_event_authority`)
7. Authority-audit status (`authority_audit_status`)
8. Materially similar facts (`materially_similar_facts`)
9. Material differences (`material_differences`)
10. Defendant-specific fair warning (`fair_warning`)
11. Rule-of-orderliness review status (`rule_of_orderliness_review_status`)
12. Later-history review status (`later_history_review_status`)
13. Later-authority treatment (`later_authority_treatment`)

If a required universal field is missing or unverified, the mapping is
incomplete. Any missing or unverified conditional qualified-immunity field
creates an internal filing-critical GAP: do not mark the complaint filing-ready
and route the GAP to a reserved strategy decision without placing an adverse
merits assessment in filed text. This checklist does not duplicate the detailed
authority verification owned by `audit-authorities`.

Every count must perform the five functions **Element → Decisive Facts →
Relevant-Time Knowledge → Application → Result** in that order. This is a
functional requirement, not mandatory wording or a fixed number of paragraphs.
Identify the count, claim, constitutional source, defendant, capacity,
challenged act, and event stage before applying the standard. Identify the
injury caused by that defendant's challenged act and the relief requested from
the count.

### Standard

State the governing test precisely and attach verified authority with a pinpoint
to the statement of the test, not only to the count as a whole:

> To state a claim for [claim], a plaintiff must allege [elements]. _[Case]_,
> [vol] [rptr] [first], [pincite] ([court] [year]).

State the test in the controlling authority's own formulation. Do not paraphrase
it into a looser or broader proposition, and do not state a black-letter rule as
a bare, uncited sentence. Match the level of generality the disputed element
requires.

When the claim uses a named multi-factor or multi-prong framework, state and
cite that framework before applying facts. This includes the _Graham v. Connor_
objective-reasonableness factors, the _Nieves v. Bartlett_ probable-cause rule
and narrow exception for retaliatory arrest, the _Bell v. Wolfish_ and _Kingsley
v. Hendrickson_ punishment standard, and the elements of Section 1983
conspiracy, failure to intervene, and Monell when applicable. Verify the current
status and controlling circuit's formulation.

Identify the constitutional right, not only Section 1983. When a claim turns on
a state-law offense, state the offense elements from the statute and cite the
controlling state-court construction that fixes those elements. Do not state the
offense from memory or as a bare statutory paraphrase.

Every legal proposition stating a test, element, factor, or offense element must
carry its own verified standard pincite. A citation appearing only in the
fair-warning or application discussion does not cure an uncited Standard.

### Defendant-specific decisive facts and relevant-time knowledge

Connect each defendant's pleaded facts to each element. Cite the decisive-fact
paragraphs that state the defendant's concrete conduct, words, knowledge,
sequence, and omissions. A collective allegation does not establish every
defendant's liability. Do not substitute labels such as "retaliated,"
"conspired," or "ratified" for supporting facts.

Use only the facts known to that defendant at the legally relevant time. State
the defendant's act, knowledge, timing, opportunity, and causal role.
Later-acquired information cannot justify an earlier act.

### Element-specific application and conditional inference

State the application supported by the decisive facts and the defendant's
relevant-time knowledge. Name the defendant and the element established or
negated. For example:

> Before ordering the arrest, Officer Doe observed [decisive facts]. Those
> then-known facts did not support [the disputed offense element]. No reasonable
> officer with the same information could have believed probable cause existed.

Use a direct application when it fully states the bridge. Expressly identify a
reasonable inference when the application depends on an unobserved state of
mind, agreement, causal mechanism, municipal attribution, or another non-obvious
inferential step. State the supporting facts first. Do not add a stock inference
phrase when the application already performs that work.

When supported facts permit alternatives, plead them expressly. For example, if
responsible city personnel reviewed a recording and took no corrective action,
the facts may support deliberate acceptance; if the review system failed to
surface the recording, the facts may instead support inadequate supervision,
training, or review. Preserve supported alternatives when discovery-controlled
facts prevent choosing between them.

### Filed-text candor and no-concession boundary

Filed complaint text may accurately qualify what a source, record, or evidence
proves and identify a source limitation, unresolved fact, or uncertainty.
Supported alternative or conditional pleading is permitted. Filed complaint text
must not describe its own claim, element, fair-warning path, or
qualified-immunity position as weak, likely to fail, likely barred, or legally
deficient. Route legal risk, merits, or strength assessment to versioned
strategy or an internal audit. That route does not permit concealment of
contrary evidence or authority.

### Qualified immunity for eligible individual counts

For every qualified-immunity-eligible individual mapping, complete the
conditional qualified-immunity fields in the canonical checklist.

Address each individual defendant and each qualified-immunity prong separately.
For prong one, state which facts, taken as true, show that defendant violated
the precise right. For prong two, identify the binding authority decided before
the event date that clearly established the right in the specific factual
context. Do not lump defendants or rely on a broad constitutional proposition
when fact-specific authority is required.

Before treating the count as complete, compare the defendant and challenged
conduct, binding case and authority status, materially similar facts, material
differences, and why the case gave fair warning on the event date. Use the level
of specificity at which the defendant acted. As applicable, identify the
suspected offense, threat, resistance, flight, compliance, force type, duration,
warning interval, injury, protected activity, probable-cause posture, and event
sequence. Explain material differences rather than hiding them.

Do not use a district-court decision, an unpublished nonprecedential decision,
or a later-decided case as the source of clearly established law. Such authority
may be persuasive on method or application only when its status and limited use
are stated accurately.

The filed complaint itself must contain a concise, defendant-specific
fair-warning unit for every individual-capacity count against a defendant who
can assert qualified immunity. This filed fair-warning rule is mandatory and
non-waivable. A separate brief, internal matrix, strategy or control memo, or
promise to provide the analysis later cannot substitute for it. A brief may add
authority discussion but cannot replace the complaint's fair-warning unit.

For each eligible claim and defendant, the filed complaint must state:

1. the right at the factual specificity of that defendant's conduct;
2. the defendant's act, knowledge, and event stage;
3. verified binding authority decided before the event date;
4. the materially similar facts and material differences;
5. why that authority gave the defendant fair warning; and
6. a conclusion addressing the prong one result and prong two result.

Each distinct complaint-level fair-warning proposition ordinarily uses one
verified lead binding pre-event authority and the decisive factual comparison.
Any additional complaint-level authority must perform a separately identified
job. Full comparison matrices, competing case discussions, later history, and
unexplained string cites remain in internal work product or a brief. This
boundary is functional, not a universal numeric maximum.

A case-specific strategy, routing, packet, or instruction to put clearly
established law only in a brief does not relax this rule. Flag the conflict,
keep the complaint-level unit, and route only surplus analysis to the brief. The
full five-role case stack, later-history research, competing-authority
discussion, and extended futility analysis may remain in the brief and internal
audits; the complaint-level unit may not.

Rule 8 does not lower this floor. _Johnson v. City of Shelby_, 574 U.S. 10
(2014), confirms that a complaint need not contain a brief or perfectly state
every legal theory, while _Degenhardt v. Bintliff_, 117 F.4th 747, 753–54, 758
(5th Cir. 2024), and _Kelson v. Clark_, 1 F.4th 411, 416 (5th Cir. 2021),
require corresponding specificity when pleading liability and defeating
qualified immunity. A prior qualified-immunity ruling or futility inquiry
raises, rather than lowers, the required specificity. The unit is concise, not
an authority brief.

The only exception is a count against a defendant or capacity that cannot assert
qualified immunity, such as a municipality or other entity on a Monell count.
The qualified-immunity fields and filed fair-warning unit are inapplicable to
that count. Every other required count field remains mandatory.

### Result

Conclude the count:

> Accepting these facts as true and drawing reasonable inferences in Plaintiff's
> favor, Plaintiff has stated a [claim] against [defendant].

The Result must follow from the element map. It cannot repair a missing
allegation. Confirm that the count identifies the injury and relief before the
Result.

## Version-2 complaint handoff and validation

The install-local
[complaint-structure-contract.json](complaint-structure-contract.json) provides
the strict version-2 mechanical interface. Version 1 is unsupported. Run the
install-local `../scripts/validate_complaint_handoff.py` against every handoff.
Keep its `structural_validation`, `casegraph_assessment`, and `filing_gate`
results separate. A structural pass does not make or replace a legal judgment.

Every individual-capacity count must include a typed `individual_capacity` unit
identifying the personal act or causal role, event stage, relevant time, facts
then known, underlying violation, application, injury, and causation. The typed
`qualified_immunity` unit must state whether QI applies and, when it does, must
include every field in the JSON contract.

Every municipal count must contain one or more separately typed `monell_paths`.
Do not combine formal policy, custom or practice, final-policymaker decision,
ratification, failure to train, or failure to supervise or discipline in one
path object. Each path must include the common causal and attribution fields and
the fields specific to its one path type. An FTO method, jail handoff, complaint
review, or similar process belongs in the implementation or transmission
mechanism field unless verified authority supports treating it as a distinct
path.

An optional CaseGraph assessment is read-only and consumes an explicit on-disk
graph path without invoking a CLI. Every authority proposition used in an
assessment must resolve through the authority node and verified source metadata
to the canonical opinion bytes and hash, the cited pinpoint, and an exact
passage in a provenance-linked text representation. Record the exact passage,
stable locator, hashes, and deterministic normalization. Citation labels,
pinpoint strings, and semantic or fuzzy matches are insufficient.

Deterministic checking is limited to the listed mechanical checks. It excludes
fact truth, legal sufficiency, authority fit, material analogy, strategy, and
filing readiness. A reasoned graph assessment may separately express a
procedural-lens opinion, but it must expose its sources, contrary paths, missing
connections, and exact authority-resolution status. Drafting mode may continue
with an explicit unassessed graph state. Filing mode fails closed unless every
included claim unit has a current completed assessment and no unresolved receipt
finding.
