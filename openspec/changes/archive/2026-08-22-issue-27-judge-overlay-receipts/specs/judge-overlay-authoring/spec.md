## MODIFIED Requirements

### Requirement: Neutral downstream consumption

A drafting skill SHALL load an applicable assigned-judge overlay after the
governing document and claim skills. It SHALL consume only validated neutral
transfer cards, preserve their source identity, evidence strength, permitted
use, prohibited inference, denominator, and missingness, and keep governing law
separate. The transfer MUST NOT expose private strategy or select a litigation
path.

Every composition run SHALL write an immutable version-local execution receipt.
A prohibited inference or no qualifying support produces no judge-specific
drafting change and records the bounded reason. Missing, stale, invalid, or
unavailable required inputs fail closed and are not represented as passing. The
absence of judge-specific prose does not establish that the overlay ran.

#### Scenario: Transfer card supports no drafting change

- **WHEN** the card prohibits the proposed inference or reports no qualifying
  support
- **THEN** the drafting skill makes no judge-specific change, preserves the
  card's limitation, and writes a receipt stating
  `no judge-specific drafting change`

#### Scenario: Applicable overlay never runs

- **WHEN** composition produces no execution receipt
- **THEN** review treats overlay execution as unproven rather than inferring a
  successful no-change result from the filing text
