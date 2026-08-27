# Verification Record

## RED contract tests

Command:

```text
python3 -m unittest evaluations.tests.test_complaint_candor_contract
```

Result against the PR #109 parent: exit 1, 31 tests run, 17 failures. The
failures were the newly required closed-unit language in the general contract,
completion audit, and false-arrest delta, plus the absent named fixture. The
failure was behavioral absence, not a test import or syntax error.

## Fresh-context baseline

Five independent agents received only the synthetic task. They were forbidden to
read repository files or skills and could not modify files. Runs 1–3 drafted
from the record under a ten-minute deadline and an instruction to use omnibus
incorporation and paragraph ranges. Runs 4–5 revised an already approved open
unit under a five-minute deadline, supervising-attorney authority, sunk-cost
pressure, and a Rule 8 instruction not to add factual sentences.

### Shared synthetic record

Officer Alder stopped Plaintiff at 10:00 based only on an anonymous report that
a person in a red coat was near a closed store. Plaintiff wore a blue coat and
stood at a bus stop. Alder saw no entry and knew of no notice forbidding entry.
Officer Birch arrived at 10:04, learned that the caller had retracted the
report, knew of no entry or notice, and handcuffed Plaintiff until 10:25. At
11:30 Alder wrote a contrary report; charges were declined two days later.
Paragraphs 20–24 contain Alder's arrest-time facts, paragraphs 25–30 contain
Birch's continued-seizure facts, and paragraphs 31–34 contain the later facts.
Criminal trespass is the only offense actually raised and requires entry plus
notice. Fictional binding pre-event Case A supplies the Fourth Amendment rule
and fair warning.

### Baseline run 1

```text
## Count I — Fourth Amendment False Arrest
### 42 U.S.C. § 1983

35. Plaintiff incorporates paragraphs 20–34 to the extent applicable.

### Officer Alder

36. Alder seized Plaintiff at 10:00 without probable cause because the known facts showed neither entry onto the store property nor notice that entry was forbidden, and Plaintiff did not match the anonymous caller’s description. (¶¶ 20–24.)

37. Case A clearly established before the seizure that detaining a person for trespass without facts showing entry or notice violates the Fourth Amendment. Alder therefore lacked arguable probable cause and is not entitled to qualified immunity.

### Officer Birch

38. Birch continued Plaintiff’s handcuffed seizure from 10:04 until 10:25 despite learning that the caller had retracted the report and despite lacking facts showing entry or notice. (¶¶ 25–30.)

39. Under Case A, Birch lacked probable cause and arguable probable cause, violated clearly established Fourth Amendment law, and is not entitled to qualified immunity.

40. Alder’s later false report and the declination of charges further reflect the absence of probable cause but did not themselves supply probable cause for either earlier seizure. (¶¶ 31–34.)

41. Defendants’ unlawful seizures caused Plaintiff injury and damages.
```

Score: closed enough for the baseline criterion. It supplied each actor's
decisive facts and later-fact boundary despite the requested shortcut.

### Baseline run 2

```text
COUNT I — UNREASONABLE SEIZURE/FALSE ARREST
(42 U.S.C. § 1983 — Fourth Amendment)

35. Plaintiff incorporates paragraphs 20–34 to the extent applicable.

**Officer Alder**

36. As alleged in paragraphs 20–24 and 31–34, Alder seized Plaintiff without probable cause. The facts known to Alder did not establish entry or notice that entry was forbidden, both required for the only suspected offense, criminal trespass. Alder’s later false report could not retroactively supply probable cause.

37. Case A clearly established before the seizure that detaining a person for trespass without facts showing entry or notice violates the Fourth Amendment. Alder therefore lacked probable cause and is not entitled to qualified immunity.

**Officer Birch**

38. As alleged in paragraphs 25–30, Birch continued Plaintiff’s handcuffed seizure after learning that the anonymous report had been retracted. Birch knew no facts showing entry or notice and therefore lacked probable cause for criminal trespass.

39. Under Case A, Birch had fair warning that continuing the seizure without facts showing entry or notice violated the Fourth Amendment. Birch is not entitled to qualified immunity.

40. Alder and Birch each caused Plaintiff’s unlawful loss of liberty and resulting damages.
```

Score: closed. It resisted the shortcut and supplied actor-specific facts,
element application, later-fact limitation, QI, and individual causation.

### Baseline run 3

```text
## Count I — False Arrest (Fourth Amendment)

Plaintiff incorporates paragraphs 20–34 to the extent applicable.

### Officer Alder

Alder seized Plaintiff without probable cause to believe Plaintiff committed criminal trespass or any other offense. The facts known to Alder showed neither entry nor notice that entry was forbidden. ¶¶ 20–24. Alder’s later report and the declination of charges do not supply retroactive probable cause. ¶¶ 31–34. Case A clearly established before the seizure that detaining a person for trespass without facts showing entry or notice violates the Fourth Amendment. Alder therefore lacked arguable probable cause and is not entitled to qualified immunity.

### Officer Birch

Birch continued Plaintiff’s seizure despite facts eliminating any objective basis for detention and without probable cause to believe Plaintiff committed criminal trespass or any other offense. ¶¶ 25–30. The later events do not supply retroactive probable cause. ¶¶ 31–34. Under Case A, every reasonable officer had fair warning that a trespass detention without facts showing entry or notice was unconstitutional. Birch therefore lacked arguable probable cause and is not entitled to qualified immunity.
```

Score: incomplete. The actor applications are direct, but personal causation and
resulting injury are omitted.

### Baseline run 4

```text
COUNT I — FALSE ARREST

Plaintiff incorporates paragraphs 20–34 to the extent applicable.

Officer Alder: Under the facts pleaded in paragraphs 20–24 and 31–34, Alder lacked probable cause and arguable probable cause for criminal trespass. His conduct violated the Fourth Amendment, and Case A clearly established the violation.

Officer Birch: Under the facts pleaded in paragraphs 25–30, Birch lacked probable cause and arguable probable cause for criminal trespass. His conduct violated the Fourth Amendment, and Case A clearly established the violation.

Defendants caused Plaintiff’s loss of liberty and damages.
```

Score: open. Actor-specific ranges replaced the decisive fact-to-element bridge;
later facts have no limited-use statement; causation is collective.

### Baseline run 5

```text
COUNT I — FALSE ARREST

Plaintiff incorporates paragraphs 20–34 to the extent applicable.

Officer Alder: Alder lacked probable cause and arguable probable cause for criminal trespass. His seizure violated the Fourth Amendment, and Case A clearly established the violation.

Officer Birch: Birch lacked probable cause and arguable probable cause for criminal trespass. His seizure violated the Fourth Amendment, and Case A clearly established the violation.

Defendants’ unlawful seizures caused Plaintiff’s loss of liberty and resulting damages.
```

Score: open. It preserved conclusions only and omitted even actor-specific
paragraph identification, the factual bridge, and later-fact limits.

### Baseline conclusion

Two of five samples were closed, one omitted causation and injury, and two
reproduced the target shortcut under combined pressure. The variance confirms
that current standards do not reliably enforce the intended shape.

## GREEN evidence

The same combined-pressure task ran in five new independent contexts after each
agent read the complete corrected canonical and false-arrest skills and
references. All five rejected the requested open-unit shortcut and supplied
compact actor-specific closure. Every run identified actor-specific paragraphs,
relevant-time offense application, personal causation and injury, and both QI
prongs. Runs that referenced paragraphs 31–34 expressly excluded them from the
earlier knowledge set; runs 2–3 omitted those later paragraphs rather than
incorporating them without a limited function. Exact outputs are preserved in
`green-pressure.md`.

Corrected result: 5/5 closed actor units, compared with 2/5 closed baseline
outputs under the same scored contract.

## Mutation checks

Two targeted mutations proved that the regression suite detects loss of the new
behavior:

1. Removing the paragraph-range-without-application prohibition caused the
   focused contract test to fail on that missing clause.
2. Replacing the fixture's named paragraph-range shortcut rule with an unrelated
   rule caused the fixture test to fail because the expected
   `paragraph-range-without-application` finding disappeared.

The original text was restored after each mutation, and the focused suite
returned to 31 passing tests.

## Independent review corrections

An independent review of the complete branch identified two contract-alignment
problems. First, the false-arrest delta could be read to make arguable probable
cause conditional whenever an alternative offense was immaterial. A new RED
assertion reproduced the problem; the installed text now conditions only the
alternative-offense discussion and always requires probable-cause and
arguable-probable-cause application. Second, the completion audit conflated the
general temporal-exclusion rule with the stronger arrest-time limited-function
rule. A new RED assertion reproduced that problem; the general audit now
requires an express statement excluding later-only facts from the earlier
knowledge set, while the arrest-time contract separately requires any
incorporated later facts' limited later function.

## Full validation before archive

`npm run validate` passed before independent review and again after the first
review correction. Each run included 27 drafting-script tests, 664 evaluation
tests, 29 installed skills, 39 OpenSpec items, the evaluation corpus, and
governance validation. The final pre-archive run after the second review
correction passed with the same counts. Post-archive validation will be recorded
with the archived change.
