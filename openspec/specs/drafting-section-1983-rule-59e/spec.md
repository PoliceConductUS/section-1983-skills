# drafting-section-1983-rule-59e Specification

## Purpose

TBD - created by archiving change issue-114-post-draft-assertion-validation.
Update Purpose after archive.

## Requirements

### Requirement: Rule 59 packet validation preserves one-target invocations

The Rule 59(e) workflow MUST invoke `validating-court-facing-assertions`
separately for each generated court-facing motion, brief, proposed amended
pleading, proposed order, and appendix. It MUST then reconcile the complete
packet across the resulting current receipts and MUST NOT combine multiple
filing targets into one validation invocation.

#### Scenario: Packet contains several court-facing documents

- **WHEN** a Rule 59(e) packet contains more than one generated court-facing
  document
- **THEN** each document receives its own current validation receipt before the
  workflow performs packet-level consistency reconciliation
