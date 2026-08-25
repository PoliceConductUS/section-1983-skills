# implemented-skill-folder-migration Delta

## MODIFIED Requirements

### Requirement: Every public skill carries an exact folder contract

Every public skill MUST link to a schema-valid install-local folder contract
with exactly its approved ordered role set, target policy and target roles,
internet policy, and `append-immutable` output mode:

| Skill                                             | Ordered input roles                                                         | Target policy and roles                       | Internet   |
| ------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------------------- | ---------- |
| `adversarial-filing-review`                       | `filing`, `approved-sources`                                                | required in `filing`                          | authorized |
| `audit-authorities`                               | `filing`, `authorities`                                                     | required in `filing`                          | authorized |
| `auditing-section-1983-discovery-responses`       | `served-discovery`, `responses`, `production`, `authorities`                | required in `served-discovery` or `responses` | disabled   |
| `auditing-section-1983-privilege-logs`            | `privilege-log`, `served-discovery`, `authorities`                          | required in `privilege-log`                   | disabled   |
| `building-defense-counsel-overlays`               | `research-snapshot`, `case-record`                                          | required in `research-snapshot`               | disabled   |
| `building-judicial-reasoning-profiles`            | `judge-identity`, `court-scope`, `approved-sources`, `verified-authorities` | none                                          | authorized |
| `building-litigation-alignment-overlays`          | `docket-snapshot`, `filing`                                                 | required in `docket-snapshot`                 | disabled   |
| `drafting-false-arrest-complaints`                | `record`, `authorities`, `filing`                                           | optional in `filing`                          | disabled   |
| `drafting-section-1983-complaints`                | `record`, `authorities`, `filing`                                           | optional in `filing`                          | disabled   |
| `drafting-section-1983-declarations-and-evidence` | `record`, `authorities`                                                     | optional in `record`                          | disabled   |
| `drafting-section-1983-deposition-outlines`       | `record`, `authorities`, `discovery`                                        | optional in `record`                          | disabled   |
| `drafting-section-1983-meet-and-confer`           | `discovery-audit`, `served-discovery`, `authorities`, `conference-record`   | required in `discovery-audit`                 | disabled   |
| `drafting-section-1983-rule-59e`                  | `record`, `authorities`, `filing`                                           | optional in `filing`                          | disabled   |
| `drafting-section-1983-written-discovery`         | `record`, `authorities`, `claim-map`                                        | optional in `claim-map`                       | disabled   |
| `filing-ci`                                       | `filing`, `authorities`                                                     | required in `filing`                          | disabled   |
| `horan-bad-words`                                 | `filing`                                                                    | required in `filing`                          | disabled   |
| `rrd`                                             | `motion`, `record`, `authorities`                                           | required in `motion`                          | disabled   |
| `rrd-rule12`                                      | `motion`, `record`, `authorities`                                           | required in `motion`                          | disabled   |
| `rrd-rule12-city`                                 | `motion`, `record`, `authorities`                                           | required in `motion`                          | disabled   |
| `rrd-rule12-officers`                             | `motion`, `record`, `authorities`                                           | required in `motion`                          | disabled   |
| `section-1983-drafting`                           | `record`, `authorities`, `strategy`, `filing`                               | optional in `filing`                          | authorized |
| `studying-rule-59e-decisions`                     | `decisions`, `authorities`                                                  | optional in `decisions`                       | authorized |

The contract object MUST contain no additional fields. Every role listed by the
contract MUST appear exactly once and in order in the invocation. A required
target MUST be present in an allowed target role; an optional target MAY be
omitted for non-targeted behavior but MUST use an allowed role when present; a
`none` target policy MUST reject a target. A composed workflow MUST validate
each skill independently and MUST NOT union role, target, internet, or output
authority across skills.

#### Scenario: A quality-control-only skill omits its primary target

- **WHEN** a discovery-response or privilege-log audit invocation omits its
  required primary target
- **THEN** installed-skill validation reports `contract-target` before reading
  case material or publishing a report
