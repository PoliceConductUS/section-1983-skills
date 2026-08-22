## ADDED Requirements

### Requirement: Filed complaint does not assess its own legal weakness

The canonical complaint contract MUST distinguish accurate factual/source
qualification from an adverse legal merits assessment. Filed text MUST NOT
volunteer that a pleaded claim, element, fair-warning path, or
qualified-immunity position is weak, likely to fail, likely barred, or otherwise
legally deficient. Legal risk assessment MUST be routed to versioned strategy or
internal audit work without concealing adverse evidence or authority.

#### Scenario: Source leaves an event fact unresolved

- **WHEN** the available source does not resolve a material event fact
- **THEN** the complaint may identify the source limitation and supported
  alternatives without characterizing the claim itself as weak

#### Scenario: Drafter doubts prong two

- **WHEN** the drafter believes the clearly-established-law path may fail
- **THEN** the assessment is recorded internally and the filed complaint either
  states a supportable fair-warning path or reports a filing-critical GAP for a
  reserved strategy decision

#### Scenario: Alternative pleading is authorized

- **WHEN** supported facts permit alternative or conditional pleading
- **THEN** the complaint may plead those alternatives without treating the
  procedural qualification as an adverse concession

### Requirement: Complaint-level fair-warning analysis remains bounded

Each distinct complaint-level fair-warning proposition MUST ordinarily use one
verified lead binding pre-event authority and the decisive factual comparison.
Any additional complaint-level authority MUST perform a separately identified
job. Full comparison matrices, competing case discussions, later history, and
string cites MUST remain in internal work product or a brief unless needed for a
separately identified complaint-level proposition.

#### Scenario: One case supplies the fair-warning proposition

- **WHEN** one verified binding pre-event case supplies the relevant rule and
  decisive factual comparison
- **THEN** the complaint uses that lead authority without reproducing the
  internal multi-case matrix

#### Scenario: A second case performs a distinct job

- **WHEN** another authority is necessary for a separate controlling proposition
  or precedential link
- **THEN** the complaint identifies that distinct job rather than adding an
  unexplained string cite

### Requirement: One canonical tuple checklist governs count completion

The complaint contract MUST define one canonical checklist for every
claim–defendant–challenged-act tuple. The universal fields MUST be the claim,
defendant, challenged act and event stage, governing element or standard,
decisive facts, facts known to the defendant at the legally relevant time,
resulting element-specific legal application, and result. For every
qualified-immunity-eligible individual-capacity tuple, the same checklist MUST
also require the event date; conduct-specific right or rule; verified binding
pre-event authority; authority-audit status; materially similar facts; material
differences; defendant-specific fair warning; rule-of-orderliness and later-
history review status; and separate prong-one and prong-two results.

The complaint contract MUST own these field names and the completion rule, but
MUST NOT duplicate the detailed authority-verification procedure owned by
`audit-authorities`. A missing or unverified universal field makes the tuple
incomplete. A missing or unverified qualified-immunity field creates an internal
filing-critical GAP, blocks filing-ready status, and routes the issue for a
reserved strategy decision without adding an adverse merits assessment to filed
text.

The install-local mechanical handoff MUST use the same tuple cardinality and
machine-readable field names. Capacity remains a required tuple field, but it
MUST NOT replace challenged act in the tuple cardinality. The handoff remains a
non-executable interface and MUST NOT claim to perform the authority audit.

#### Scenario: Universal application bridge is incomplete

- **WHEN** a count states decisive facts but omits the defendant's relevant-time
  knowledge or the resulting element-specific application
- **THEN** the tuple remains incomplete and the complaint cannot be marked
  filing-ready

#### Scenario: Fair-warning verification is incomplete

- **WHEN** a qualified-immunity-eligible tuple lacks verified authority status
  or completed rule-of-orderliness and later-history review
- **THEN** the internal record contains a filing-critical GAP, filing-ready
  status is blocked, and the filed complaint does not volunteer an adverse
  merits assessment

### Requirement: Uncertain factual paragraphs perform a pleaded function

The completion audit MUST inventory every factual paragraph the draft labels
unresolved, unknown, unrelated, or non-establishing. Each retained paragraph
MUST identify at least one function: an element, an actual defense premise, a
material chronology function, or a candor/preservation function. A paragraph
with no such function MUST be removed from filed text or moved to internal
chronology.

#### Scenario: Unresolved detail serves no pleaded job

- **WHEN** a paragraph says a detail is unresolved but maps to no element,
  defense premise, chronology need, or candor/preservation duty
- **THEN** the completion audit directs that paragraph out of filed text

#### Scenario: Unresolved detail preserves a material source limit

- **WHEN** an unresolved fact is material and the source limitation must be
  disclosed accurately
- **THEN** the audit records the candor/preservation function and retains only
  the bounded necessary statement

### Requirement: Material incorporated-record ambiguity completes the offense analysis

The false-arrest specialization SHALL, for each alternative offense actually
raised by the defense, a controlling ruling, or governing law, identify any
incorporated-record fact left unresolved that is material to an offense element.
Without admitting the fact occurred, the count MUST either state the supported
element-level reason the unresolved fact does not supply probable or arguable
probable cause or record a filing-critical GAP for reserved strategy decision.
The specialization MUST NOT inventory merely conceivable offenses.

#### Scenario: Recording leaves possible conduct unresolved

- **WHEN** a recording leaves possible conduct unresolved and the conduct is
  material to an element of an actually raised alternative offense
- **THEN** the count identifies the disputed fact and element and either
  completes the supported probable-cause analysis without an admission or logs a
  filing-critical GAP

#### Scenario: Offense is merely conceivable

- **WHEN** no defense, controlling ruling, or governing law has made an offense
  material
- **THEN** the skill does not add that offense to the pleading or matrix
