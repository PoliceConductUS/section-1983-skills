## ADDED Requirements

### Requirement: Authority audit contributes specialist assertion findings

The authority-audit skill MUST provide `validating-court-facing-assertions` with
proposition-specific findings for actual holding, pinpoint, controlling status,
posture, relevant later treatment, factual fit, and application. It MUST
distinguish pre-event clearly established law, defendant knowledge, municipal
notice, and Rule 15(c) lawsuit notice and MUST NOT claim complete whole-document
assertion or omission coverage.

#### Scenario: Authority is relevant but does not support the draft

- **WHEN** a valid authority concerns the general doctrine but its holding does
  not support the exact drafted proposition
- **THEN** the authority audit returns a failed proposition finding for the
  shared report rather than a relevance-based pass
