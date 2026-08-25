# repository-skill-governance Delta

## ADDED Requirements

### Requirement: Public package workflows use the shared immutable envelope

The repository MUST expose one common install-independent package contract.
Public skills that produce or consume profiles, overlays, or research corpora
MUST link to the common install-independent folder-package contract. They MUST
retain their domain-specific validation and MUST NOT convert participant data
into generated skills, static-role changes, ambient filesystem authority, or
mutable package access.

#### Scenario: An overlay skill is installed independently

- **WHEN** a current counsel or litigation-alignment skill is copied without the
  repository around it
- **THEN** its package retains the shared immutable-package boundary and its
  domain-specific validator
