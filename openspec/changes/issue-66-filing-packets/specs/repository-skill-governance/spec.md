# repository-skill-governance Delta

## ADDED Requirements

### Requirement: Public filing workflows preserve packet boundaries

Public filing-generation and quality-control skills MUST describe a FilingPacket
as a manifest-listed set of ordinary files under declared folder authority. They
MUST preserve kind/role separation, source packet immutability, trusted-host
publication, packet/member target semantics, and complete packet-level gate
coverage without adding CaseGraph or ambient filesystem authority.

#### Scenario: A public skill reviews one packet member

- **WHEN** the caller selects a manifest-listed member rather than the whole
  packet
- **THEN** the skill identifies the member by stable document ID and does not
  silently treat the result as whole-packet coverage
