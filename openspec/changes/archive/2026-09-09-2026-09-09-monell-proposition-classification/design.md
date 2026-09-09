## Context

The planning contract records supporting facts, an inference classification, the
municipal inference, information-and-belief support, and discovery leads. The
drafting contract requires facts before inference and bars unresolved
connections from becoming facts. A fresh-context baseline still placed expected
policy, adopting-authority, and complaint-history discovery propositions inside
the complaint. The missing rule is where each proposition class belongs.

## Goals / Non-Goals

**Goals:**

- Establish three explicit Monell proposition classes during planning.
- Require supported inferences to identify their pleaded factual premises.
- Keep expected-discovery propositions out of the complaint as present facts or
  evidence.
- Prevent a brief from supplying a missing complaint-level factual basis.
- Preserve expected-discovery propositions in the discovery plan.
- Define a staged-development record for supported but incomplete Monell paths.
- Require request-specific discovery relevance, diligence, deadline, amendment-
  standard, evidence-threshold, and limitations or relation-back analysis.

**Non-Goals:**

- Selecting, narrowing, abandoning, or approving a Monell path.
- Changing general assertion-validation ownership.
- Adding executable legal-sufficiency judgment.
- Promising that discovery will be available or that amendment will be allowed.

## Decisions

### Planning owns classification

Each path record classifies every proposed Monell proposition as
`source_documented_fact`, `supported_inference`, or `expected_discovery`. A
supported inference identifies the pleaded facts from which it is drawn, its
reasoning, attribution, and temporal limits. An expected-discovery record
identifies the expected information and its planned discovery treatment without
converting it into present support. The complete proposition collection is part
of each path record and survives the approved planning handoff.

### Drafting owns placement

The complaint may state source-documented facts and supported inferences with
attribution, temporal limits, and the inference's factual basis. Expected-
discovery propositions belong in the discovery plan, not in complaint prose as
present facts or evidence. A supporting brief may explain why the pleaded facts
support an inference but cannot add the missing factual premise.

The typed drafting delta preserves proposition IDs and classifications and maps
each record to its integrated complaint paragraph or discovery-plan location.
The install-local complaint-handoff validator checks that each Monell path
contains the collection, each class contains its required basis, inference
premises resolve to source-documented facts, and placement matches the class.

### Planning owns staged development

Planning must recommend that each presently supportable path be pleaded at the
narrowest factually plausible level. It must not recommend a speculative or
incident-only placeholder merely to preserve a claim. A supported but incomplete
path may receive `preserve-internal` only with a staged-development record that
identifies the missing connection, expected records or testimony, information
controller, and request-specific independent relevance to a named live claim or
defense.

The record also captures anticipated restrictions or stays, request and
production dates, the first-reasonably-knowable date, a diligence chronology,
the pleading-amendment deadline, the evidence threshold for recommending
amendment, and limitations or relation-back risk. It schedules reassessment when
responsive material arrives and before the amendment deadline. Unknown or
inapplicable dates remain explicit rather than invented.

The staged plan does not assume discovery merely because another claim survives.
Each request needs its own relevance theory and must account for applicable
discovery restrictions. Before a scheduling-order deadline, the plan records the
applicable amendment standard. After that deadline, it requires the applicable
Rule 16 good-cause analysis, including diligence and the explanation for delay,
before applying Rule 15. Any recommendation to amend remains subject to the
litigation principal's approval and what the record then establishes.

### Drafting bars preservation by placeholder

Drafting consumes only principal-approved paths supported at the required
pleading level. It may not draft boilerplate, the underlying incident alone, or
an expected-discovery proposition as a placeholder to keep a Monell theory in
the complaint. A formerly preserved path enters drafting only after the staged
plan's evidence threshold is met, current support is recorded, and the principal
approves amendment.

### Existing validation owner remains unchanged

After integration, `validating-court-facing-assertions` reviews whether the
filed text preserves fact and inference boundaries. The Monell skills do not
copy that skill's full report or correction-loop contract.

That shared validator expressly checks that a Monell expected-discovery
proposition has not been stated as an existing fact or used by a brief to repair
a missing complaint-level factual basis. This is a semantic review, not a claim
that deterministic checks decide evidentiary support or legal sufficiency.

### Behavioral evidence

Add one synthetic fixture with paired regressions: a complaint that states an
expected directive as fact, and a brief that supplies the absent factual basis.
The passing candidate classifies each proposition and places the expectation in
the discovery plan. Additional paraphrased regressions cover an unsupported
directive, an information-and-belief expectation in complaint prose, and a
missing proposition inventory.

Add staged-development regressions for a thin preservation placeholder, generic
discovery relevance labels, an after-deadline Rule 15 assumption without Rule 16
good cause, and expected discovery stated as present fact. A passing plan keeps
the incomplete path internal and supplies the complete staged record.

## Risks / Trade-offs

- **Risk: Classification becomes labeling without substance.** → Require every
  supported inference to identify its pleaded factual premises.
- **Risk: Information-and-belief allegations are mistaken for discovery-plan
  expectations.** → Preserve the existing complete information-and-belief
  foundation while forbidding an expectation alone from serving as support.
- **Risk: The brief is used to repair the complaint.** → Require the complaint
  itself to contain the factual basis for each pleaded inference.
- **Risk: Internal preservation becomes indefinite speculation.** → Require a
  missing connection, concrete discovery target, evidence threshold,
  reassessment trigger, and deadline.
- **Risk: Discovery relevance is asserted categorically.** → Require an
  independent, request-specific connection to a named live claim or defense and
  record anticipated restrictions or stays.
- **Risk: A post-deadline amendment is treated as routine.** → Require the
  applicable Rule 16 good-cause analysis before Rule 15 and preserve the
  diligence record.
