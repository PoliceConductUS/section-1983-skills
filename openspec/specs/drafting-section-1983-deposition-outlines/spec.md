# drafting-section-1983-deposition-outlines Specification

## Purpose

Define chronology- and element-gap-driven Section 1983 deposition outlines that
link grounded questions to approved sources without scripting testimony or
selecting deposition strategy.

## Requirements

### Requirement: Gap-driven, chronology-anchored outline

A deposition outline SHALL be organized by the still-open element gaps and
anchored to the locked chronology and the produced record. Each topic MUST tie
to the element it tests, the exhibit or record cite that grounds it with an
approved source identifier, and the gap it aims to close. A topic with no
element, cite, or gap MUST be reported rather than drafted as grounded.

#### Scenario: Topic ties to element, cite, and gap

- **WHEN** an outline is built from the gap register and the locked chronology
- **THEN** each topic identifies the element it tests, the exhibit or record
  cite that grounds it, and the open gap it aims to close

#### Scenario: Ungrounded topic

- **WHEN** a proposed topic has no supporting exhibit, record cite, or
  identified gap
- **THEN** the skill reports the missing ground and does not present the topic
  as record-supported

### Requirement: No scripted testimony

The outline SHALL plan questions and MUST NOT script a witness's answers, assert
what the witness will say, or supply testimony the record does not contain. It
MUST mark foundation and authentication needs and flag topics that depend on
documents still outstanding.

#### Scenario: Draft asserts expected testimony

- **WHEN** a proposed outline states what the witness will admit or concede
- **THEN** the skill rewrites the topic as a question that tests the point and
  removes the asserted answer

#### Scenario: Topic depends on an outstanding document

- **WHEN** a topic requires a document that has not yet been produced
- **THEN** the outline flags the dependency and marks the foundation the topic
  will need

### Requirement: Reserved strategy

The skill MUST NOT decide whom to depose, in what order, or whether to take a
deposition at all. It SHALL present those as plaintiff choices with their
consequences.

#### Scenario: User asks the skill to choose the deponent

- **WHEN** a request asks the skill to decide which witness to depose first
- **THEN** the skill presents the candidates, the gaps each could close, and the
  consequences without selecting one
