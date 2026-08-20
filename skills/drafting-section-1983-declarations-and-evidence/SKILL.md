---
name: drafting-section-1983-declarations-and-evidence
description: >-
  Use when a Section 1983 plaintiff needs to prepare a factual human declaration
  or source-bounded exhibit foundation for summary judgment.
---

# Drafting Section 1983 Declarations and Evidence

Prepare an unsigned factual declaration from the human declarant's supplied
personal knowledge and approved sources. Keep record attribution, analysis,
inference, legal conclusions, and expected discovery visible instead of turning
them into firsthand testimony.

## Required inputs

Require and record:

- the human declarant's identity or name;
- every proposed proposition and its approved source ID;
- the statement-specific personal-knowledge basis describing how the declarant
  saw, heard, did, received, created, or maintained the matter;
- the statement-specific competency basis describing why the declarant can
  testify about that matter;
- each proposed exhibit, its approved exhibit ID, and the declarant's supplied
  relationship to it; and
- the actual place of execution, if known.

Report missing information as a gap. Do not fill a gap from an assumption.

## Classify before drafting

Assign every proposed proposition a stable statement ID and exactly one of these
classifications:

- `firsthand fact`: the declarant personally perceived or did the stated matter;
- `attributed record fact`: an identified record states or shows the matter;
- `derived analysis`: a calculation, aggregation, coding result, or cross-record
  comparison;
- `inference`: a conclusion drawn from other supplied facts;
- `legal conclusion`: a legal characterization or result; or
- `discovery expectation`: expected content or existence of requested, missing,
  or unproduced discovery.

For every statement, return a statement classification ledger with these fields:

| Required field                  | Content                                                        |
| ------------------------------- | -------------------------------------------------------------- |
| Stable statement ID             | One identifier preserved through revision                      |
| Exact proposed text             | The complete proposition under review                          |
| Classification                  | Exactly one of the six labels above                            |
| Declarant knowledge basis       | The supplied statement-specific perception or act              |
| Competency basis                | The supplied statement-specific basis for competency           |
| Approved source IDs             | Only approved sources supporting the proposition               |
| Exhibit IDs                     | Each linked approved exhibit ID, or none                       |
| Disposition                     | Retain, revise, omit, exclude, or separate                     |
| Gap                             | Each missing knowledge, competency, source, or foundation fact |
| Human declarant approval status | Pending, approved, or omitted                                  |

An `attributed record fact` must remain attributed to the identified record.
Reading or reviewing a record does not convert the record's description of an
underlying event into the declarant's firsthand fact or personal knowledge. The
declarant may state only the supplied facts about personally receiving,
creating, maintaining, reviewing, or recognizing the record and what the
identified record states or shows.

Apply these strict disposition rules:

- `derived analysis` goes to `Excluded or Separate Material` and must not appear
  in any retained declaration paragraph.
- `inference` goes to `Excluded or Separate Material` and must not appear in any
  retained declaration paragraph.
- `legal conclusion` goes to `Excluded or Separate Material` and must not appear
  in any retained declaration paragraph.
- `discovery expectation` goes to `Excluded or Separate Material` and must not
  appear in any retained declaration paragraph.

Expected, requested, missing, or unproduced discovery is a gap or unknown. The
skill must not state that a recording, witness, record, or other source will
show, prove, or confirm a fact when the source's existence or content is
unverified.

## Gate each declaration paragraph

Use one material proposition per numbered paragraph. Retain a proposed factual
paragraph only when its ledger row contains both a supplied statement-specific
personal-knowledge basis and a supplied statement-specific competency basis. A
generic personal-knowledge recital cannot replace either missing basis.

If the declarant did not perceive the matter or lacks a supplied competency
basis, report the gap and do not place the proposition in the declaration as
personal knowledge.

## Map exhibit foundation

For every proposed exhibit, return an exhibit foundation map that records:

- exhibit ID and description;
- every linked statement ID;
- how the declarant recognizes it;
- every supplied creation, receipt, observation, custody, or maintenance basis;
- every applicable supplied accuracy or completeness basis;
- each missing foundation fact; and
- focused prompts for each missing foundation fact.

Ask only questions that could supply the identified gap, such as who created or
received the item, how the declarant recognizes it, what the declarant observed,
how it was kept, and what supports any claimed accuracy or completeness. The
skill must not invent a custodian, relationship, creation method, chain,
accuracy basis, or authentication conclusion. Do not declare, certify, or call
an exhibit authenticated, authentic, or admissible.

## Require exact human approval

Each retained statement or paragraph must begin `pending` and must be shown to
the human declarant as exact text. The human declarant may `approve`, `revise`,
or `omit` each statement. Silence is not approval.

Approval attaches only to the exact retained text. A changed, revised, or edited
statement or paragraph must reset to `pending`. Execution remains blocked until
every retained statement has the human declarant's explicit approval. If any
statement remains pending, preserve the unsigned draft and report the blocking
statement IDs.

The skill must not sign, date, execute, or file a declaration for the human
declarant.

## Select the Section 1746 form

The supplied actual place of execution selects the statutory form. The skill
must not infer or select the form from residence, venue, incarceration, or
custody.

For execution within the United States, its territories, possessions, or
commonwealths, use only this domestic form:

`I declare under penalty of perjury that the foregoing is true and correct. Executed on (date).`

For execution without the United States, use only this foreign form:

`I declare under penalty of perjury under the laws of the United States of America that the foregoing is true and correct. Executed on (date).`

Leave the date and signature blank for the human declarant. If there is a
missing or unknown actual execution location, block form selection. The skill
must not select a form and must not combine or mix the statutory forms. Keep
execution blocked.

## Return outputs in order

Return these five outputs in this order:

1. `Statement Classification Ledger`
2. `Unsigned Draft Declaration`
3. `Exhibit Foundation Map`
4. `Excluded or Separate Material`
5. `Approval and Execution Status`

The unsigned draft includes the declarant's identity, numbered retained
paragraphs, and only the applicable unexecuted Section 1746 block when the
actual execution location is supplied. Keep the human date and signature blank.

The approval and execution status reports each retained statement ID and its
approval state, every blocking gap, the supplied actual execution location, and
whether form selection is blocked. It does not label the declaration or filing
ready.

## Boundaries

This skill prepares source-bounded materials. It does not certify the truth,
authentication, or admissibility of any statement or exhibit. It does not
certify or claim execution, filing, or filing readiness. It does not decide
whether to use an exhibit, make a legal argument, sign, date, execute, or file
anything.
