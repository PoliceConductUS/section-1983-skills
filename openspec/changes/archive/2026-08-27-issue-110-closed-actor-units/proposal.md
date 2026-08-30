## Why

Current complaint records can contain every named field while filed prose still
forces the court to gather facts from several sections and construct the
actor-specific element and qualified-immunity analysis. Multi-officer false-
arrest pleadings are especially vulnerable when one omnibus incorporation or
paragraph range masks different acts, times, and knowledge sets.

## What Changes

**Closed actor application**

- From: One complete mapping per claim–Defendant–challenged-act tuple with
  incorporation, knowledge, application, causation, injury, and QI fields.
- To: The same tuple must function as a closed complaint-level unit that names
  its own incorporated paragraphs and directly supplies the decisive bridge from
  the actor's relevant-time facts to the disputed element, causation, injury,
  and both QI prongs when applicable.
- Reason: Field presence and a paragraph range do not ensure the pleaded prose
  performs the application.
- Impact: The canonical contract and completion audit reject omnibus and
  paragraph-range shortcuts when actor acts or knowledge differ.

**False-arrest specialization**

- From: Actor, seizure, offense, relevant-time knowledge, probable-cause,
  causation, and fair-warning requirements may be satisfied across several
  sections.
- To: Every challenged officer receives one closed application covering the
  seizure stage, actually material offenses and elements, contemporaneous
  knowledge, later-fact exclusion, probable and arguable probable cause, causal
  role, injury, and conduct-specific QI analysis.
- Reason: Arrest-time analysis must not silently absorb post-seizure facts or
  collective allegations.
- Impact: The false-arrest delta states the complete actor-specific recipe.

**Regression evaluation**

- From: Existing mechanical fields and complaint fixtures do not reproduce the
  actor-heading plus paragraph-range shortcut.
- To: A paired synthetic fixture preserves the shortcut as a failing candidate
  and a closed per-officer application as the passing candidate.
- Reason: The defect is semantic behavior, not merely missing fields.
- Impact: Independent judgment uses explicit actor-closure criteria;
  deterministic grading remains narrow and does not claim legal sufficiency.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `drafting-section-1983-complaints`: Require functionally closed general and
  false-arrest actor units and fail the completion audit on known shortcuts.
- `drafting-skill-evaluations`: Preserve a paired semantic regression fixture
  without expanding deterministic grading into legal judgment.

## Impact

The change affects three installed Markdown references, the canonical durable
complaint contract, one synthetic fixture, focused evaluation tests, and the
durable evaluation specification. It adds no package, dependency, checker,
persistence layer, case-specific allegation, or filing strategy.
