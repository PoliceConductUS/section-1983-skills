# Reproducible baseline pressure test

## Exact prompt

```text
Validate every assertion and required-content omission in evaluations/fixtures/post-draft-assertion-validation/target-draft.md against the other files in that fixture folder. Do not edit the draft. Return the report you believe is appropriate.

Do not read or use skills/validating-court-facing-assertions or the Issue #114 OpenSpec files. Read only the target and fixture source/control/prior-report files. Return your complete report verbatim, followed by a clearly separated short self-assessment of what report schema, status taxonomy, freshness/dependency, issue-register, and stopping rules you had to invent or could not infer. Do not edit files.
```

## Verbatim output

```text
# Assertion Validation Report

## Scope and source basis

Target reviewed: `target-draft.md`.

Sources reviewed:

- `recording-observation.md`
- `transcript.md`
- `authority.md`
- `control.md`
- `prior-report.md`

This review is limited to those files. The transcript is derivative and expressly does not represent native-audio review. No native-audio verification is claimed here.

## Assertion register

### A-001 — “Plaintiff submitted to Officer Alder’s authority.”

**Finding: Unsupported.**

The recording observation establishes Alder’s command but expressly states that the recording does not establish Plaintiff’s agreement, voluntary yielding, or submission before Alder took hold of his arm. The transcript supplies only the command. Neither source supports presenting submission as an established fact.

### A-002 — “Alder knew Plaintiff had not committed an offense.”

**Finding: Unsupported.**

No supplied source establishes either that Plaintiff had not committed an offense or that Alder knew this. The asserted mental state cannot be derived from the supplied chronology alone.

### A-003 — “Smith controls because it concerns a traffic stop.”

**Finding: Partially supported but materially overbroad.**

The authority review assumes Smith is controlling authority in the synthetic jurisdiction, but Smith’s holding is limited to investigative-stop duration. Merely involving a traffic stop does not make Smith controlling for every proposition arising from the encounter. Smith does not decide whether an arrest command establishes voluntary submission and cannot support that proposition.

### A-004 — “Officer Roe remains identified as Doe under the approved treatment.”

**Finding: Supported.**

The current control expressly authorizes Roe’s identity to remain unknown and requires the approved Doe treatment. Unknown status alone is not a defect.

### A-005 — “Plaintiff remembers Alder saying, ‘You are under arrest,’ immediately before the seizure.”

**Finding: Unsupported and unresolved against the supplied record.**

No supplied source supports Plaintiff’s asserted recollection, the quoted words, or their timing. The recording observation and derived transcript instead document Alder saying, “Turn around and place your hands behind your back,” immediately before physical contact. The supplied materials do not establish whether an additional statement occurred. The asserted quotation therefore cannot be validated, and the discrepancy requires resolution from an appropriate original source.

## Requirement coverage

### R-001 — Approved Count II

**Finding: Required-content omission.**

The current control requires Count II to appear in the candidate. It does not appear in the target draft. Existing issue `ISS-001` remains unresolved.

### R-002 — Supported detention duration

**Finding: Required-content omission.**

The current control requires the principal correction to state the supported detention duration. The target draft states no detention duration.

### R-003 — Approved Doe treatment for Officer Roe

**Finding: Satisfied.**

The target draft retains Officer Roe as Doe under the approved treatment, consistent with the current control.

## Issue register

- `ISS-001` — Open: approved Count II remains omitted.
- `ISS-002` — Open: Plaintiff’s submission is presented as fact without source support.
- `ISS-003` — Open: Alder’s asserted knowledge and the underlying no-offense proposition lack source support.
- `ISS-004` — Open: Smith’s controlling effect is stated beyond the reviewed holding and factual fit.
- `ISS-005` — Open: Plaintiff’s recollection, quoted arrest statement, and timing are unsupported and unresolved against the supplied recording account.
- `ISS-006` — Open: the required supported detention duration is omitted.

## Freshness and prior-review effect

The prior report does not validate the current submission assertion. It reviewed “Alder ordered Plaintiff to turn around,” while the current draft says “Plaintiff submitted to Alder’s authority.” That material change requires a fresh assertion-level review, which this report performs.

This report is current only relative to the supplied file contents. No hashes, versions, or review timestamps were provided to establish a stronger freshness claim.

## Overall status

**Fail — the target draft is not assertion-validated.**

The draft contains multiple unsupported or materially overbroad court-facing assertions and omits two requirements imposed by the current control.

## Stopping decision

Stop at reporting. Do not treat the draft as validated unless the unsupported assertions and required-content omissions are resolved and the resulting candidate is reviewed again. No draft edits were made.

---

## Baseline self-assessment

- **Report schema:** I invented the section structure, `A-###` and `R-###` records, and per-item finding/basis format. The prompt specifies no report schema.
- **Status taxonomy:** I invented `Supported`, `Unsupported`, `Partially supported but materially overbroad`, `Satisfied`, `Required-content omission`, `Open`, and overall `Fail`. No permitted values or roll-up rules were supplied.
- **Freshness/dependency rules:** The prior report expressly excludes the changed submission sentence, so non-transfer of that review is strongly inferable. I could not infer formal invalidation triggers, dependency fields, version/hash requirements, or the name of a stale-review status.
- **Issue register:** Only `ISS-001` and its unresolved state came from a source. I invented `ISS-002` through `ISS-006`, including issue granularity and `Open` status. No deduplication, ownership, severity, closure, or supersession rules were supplied.
- **Stopping rules:** I inferred that material unsupported court-facing assertions and mandatory omissions prevent validation and require another review after correction. The prompt does not define when to fail, block, conditionally pass, or stop. The conclusion that Roe’s authorized unknown status is not a stopper comes directly from the current control.
```

## Result

The baseline caught several obvious defects, but it invented the report schema,
status taxonomy, issue-register behavior, and stopping rule. It also omitted the
newly supplied `plaintiff-memory.md` and `plaintiff-drafted-motion.md` sources,
causing it to reject the attributed-memory proposition instead of applying the
approved independent-source distinction. This demonstrates the missing reusable
behavior rather than claiming the baseline failed to notice every bad phrase.
