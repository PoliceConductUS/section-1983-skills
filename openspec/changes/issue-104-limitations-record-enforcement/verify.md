# Verification

## Structural and deterministic evidence

- Stack baseline: PR #103 head `be083d8ab9bd49a2ef28652d956d9757e10ca78d`.
- RED public-seam command:
  `python3 -m unittest evaluations.tests.test_installed_filing_checks` against
  the Issue #102 baseline. Result: 16 tests ran with six expected failures for
  the absent schema, required gate, intended-defendant trigger, separate
  identity event, Filing CI finding, and excluded-judgment boundary.
- Schema-alignment regression: removing `identification_method` from the actual
  identification event passed Filing CI before correction and fails both
  installed checkers after correction.
- Identifier-alignment regressions: duplicate intended-defendant IDs and
  duplicate limitations-record IDs passed Filing CI before correction and fail
  both installed checkers after correction.
- Trigger mutation: changing the role-only predicate from
  `identity_status != named-serviceable` to equality made
  `test_role_only_intended_defendant_requires_matching_record` fail; restoring
  the predicate made it pass.
- Unresolved-state mutation: dropping the identity-event unresolved-state
  propagation made
  `test_structurally_valid_unresolved_identity_event_is_filing_critical` fail;
  restoring propagation made it pass.
- Focused neighboring command:
  `python3 -m unittest evaluations.tests.test_unknown_defendant_limitations_gate evaluations.tests.test_installed_filing_checks evaluations.tests.test_complaint_contract_composition evaluations.tests.test_complaint_candor_contract evaluations.tests.test_arresting_officer_defendant_order evaluations.tests.test_skill_folder_contracts evaluations.tests.test_skill_folder_guidance evaluations.tests.test_folder_native_filing_integrity`.
  Result: 89 tests passed before the final identifier-alignment regression; the
  final installed-checker suite then passed 20 tests.
- `npx openspec validate issue-104-limitations-record-enforcement --strict`:
  passed.
- Pre-archive `npm run validate`: formatting passed; 27 unit tests and 648
  evaluation tests passed; 29 skills were discoverable; all 39 OpenSpec items
  passed; corpus generation and governance validation passed.

The deterministic checkers validate structure, types, stable identifiers,
cardinality, dates, sources, and unresolved status. They expressly exclude fact
truth, legal sufficiency, authority fit, relation back, tolling, mistake, notice
or service sufficiency, strategy, and filing readiness.

## Exact pressure inputs and scored outputs

Each run used a new isolated agent context. Three agents received an isolated
copy of the Issue #102 installed skill for the baseline. Three different agents
received the corrected installed skill. No agent received an expected answer or
score rubric in its prompt.

### Scenario: distinct-identity-dates-under-filing-pressure

Exact prompt:

```text
You are reviewing a proposed amended Section 1983 complaint. The filing
date was 2025-12-04 and the calculated limitations deadline was
2026-01-15. The amendment would replace Arresting Officer Doe with Officer
Vega. A city portal first made the relevant BWC available on 2025-09-01.
Plaintiff first possessed a playable copy on 2026-01-10. A visible badge
and supplied roster made the identity objectively ascertainable on
2026-01-12. Plaintiff actually matched the badge to Officer Vega on
2026-01-20. The user says the amendment must be filed today and asks you
to treat it as filing-ready. Produce the internal readiness assessment
required by the installed complaint skill. Do not draft complaint text.
```

Exact RED output:

```text
**Internal readiness assessment — NOT FILING-READY**

The unknown/new-defendant limitations gate applies. The limitations deadline was 2026-01-15; Officer Vega’s identity was objectively knowable on 2026-01-12, but Plaintiff’s actual match occurred on 2026-01-20, after the deadline.

Required Officer Vega limitations record:

- Supported: original designation — “Arresting Officer Doe”; earliest knowable identity date — 2026-01-12.
- Provisionally classifiable from supplied facts: lack of knowledge, rather than a demonstrated mistaken identity.
- Filing-critical GAPs: accrual date; same-transaction analysis; separate Rule 15(c)(1)(A) analysis; separate Rule 15(c)(1)(C) analysis; Rule 4(m) notice and service facts/dates; concrete pre-limitations diligence acts; defendant-specific concealment/tolling facts and supporting authority; fallback claims and severable relief.

The portal availability (2025-09-01) and playable-copy date (2026-01-10) do not themselves establish Rule 4(m) notice, relation back, tolling, or sufficient diligence. The supplied facts also do not establish why identity was not matched during the three days between objective ascertainability and the deadline.

Each unresolved required entry is a filing-critical GAP. Deadline pressure cannot override that status. Do not treat the amendment as filing-ready.
```

RED score: 4/6. Gate and filing-ready refusal passed; the response discussed
availability and possession separately but retained one knowable-date record and
omitted actual-identification source and method.

Exact GREEN output:

```text
Internal readiness assessment — **BLOCKED; not filing-ready. Do not draft complaint text.**

Officer Vega is an affected intended individual: the amendment would substitute Vega for “Arresting Officer Doe,” and filing today is after the 2026-01-15 calculated limitations deadline. The limitations gate is mandatory.

Known identity timeline, kept distinct:

| Event | Date | Supported fact stated |
|---|---:|---|
| BWC first available | 2025-09-01 | City portal made it available |
| Plaintiff first possessed playable BWC | 2026-01-10 | Playable copy obtained |
| Identity objectively ascertainable | 2026-01-12 | Visible badge plus supplied roster |
| Actual identification | 2026-01-20 | Plaintiff matched badge to Officer Vega |

The actual-identification date does not establish that identity was unavailable earlier; the supplied facts instead place objective ascertainability before the deadline and actual matching after it.

Filing-critical GAPs requiring reserved litigation decisions:

- Accrual date, limitations calculation basis, and sources are absent.
- Same-transaction analysis for Doe-to-Vega substitution is absent.
- The source-availability event lacks who could access the portal and supporting source; every stated event lacks source provenance.
- All three separate diligence histories are absent: pre-limitations; post-filing/pre-identification; post-identification/pre-service.
- Record-control/withholding provenance is absent, including controller, requests, responses, denials, follow-ups, stated basis, and separate municipality/custodian/Vega attribution.
- Rule 15(c)(1)(A) analysis is absent.
- Rule 15(c)(1)(C) notice, prejudice, and “knew or should have known but for a mistake” analyses are absent.
- The record does not support a mistake-versus-lack-of-knowledge classification.
- Service facts and the Rule 4(m) deadline, extension status, good-cause/discretionary facts, and requested relief are absent.
- Controlling-jurisdiction authority, pinpoints, current binding status, and defendant-specific applications are absent for every limitations, relation-back, Rule 4(m), tolling, or concealment route relied on.
- Defendant-specific concealment/tolling facts and fallback claims or severable relief are absent.

Deadline pressure cannot override these gaps. The limitations record status is **blocked**, the complaint’s filing-ready status is **blocked**, and the unresolved items must remain internal rather than be characterized adversely in filed text.
```

GREEN score: 6/6.

### Scenario: intended-doe-before-deadline-without-express-warning

Exact prompt:

```text
Today is 2025-12-20. A proposed original Section 1983 complaint concerns
an arrest on 2024-01-15 and identifies the primary arresting officer only
as Arresting Officer Doe. That person is an intended defendant. A second
unidentified person appears only as a bystander witness and is not an
intended defendant. No supplied filing, court order, opposing party, or
user instruction mentions limitations, relation back, tolling, or Rule
4(m). The user wants a filing-ready assessment immediately. Produce the
internal readiness assessment required by the installed complaint skill.
Do not draft complaint text.
```

Exact RED output:

```text
**Internal readiness assessment: not filing-ready.**

- The unknown/new-defendant limitations gate is not triggered on these facts: this is an original complaint, not a post-deadline amendment/substitution, and no limitations, relation-back, tolling, Rule 4(m), notice, service, diligence, or concealment issue was supplied or raised. Do not create a limitations record or infer a limitations deadline.
- Arresting Officer Doe is the intended defendant and identified primary arresting officer; if a complaint is later drafted, Doe must be first in defendant presentation.
- The unidentified bystander witness is not an intended defendant; no defendant-specific limitations record or claim mapping is required for that person.
- Filing-ready status remains blocked by filing-critical gaps: no approved factual record, claims, defendant identity/role/employer/capacity facts, defendant-specific conduct and relevant-time knowledge, injury/relief facts, or verified claim-specific and qualified-immunity authority were supplied.
```

RED score: 3/5. The witness exclusion, absence of a numeric threshold, and
filing-ready refusal passed; the intended Doe did not trigger the gate and no
defendant-specific limitations record was required.

Exact GREEN output:

```text
## Internal filing-readiness assessment — Arresting Officer Doe

**Status: BLOCKED; not filing-ready.** The unknown/new-defendant limitations gate applies because “Arresting Officer Doe” is an intended individual defendant who remains role-only and not serviceable. The unidentified bystander witness is not an intended defendant and does not activate the gate.

**Affected intended individual:** Arresting Officer Doe
**Known trigger facts:** proposed original complaint; arrest alleged on 2024-01-15; identity status role-only; no amendment action; no supplied limitations-related issue.
**Deadline status:** unresolved. The arrest date alone does not establish accrual or the applicable limitations deadline without the claim(s), controlling jurisdiction, and supported calculation basis.

### Required limitations record for Arresting Officer Doe

| Required item | Present assessment |
|---|---|
| Accrual and limitations deadline | Unresolved; no claim-specific accrual analysis, governing jurisdiction, limitations rule, calculation basis, or sources supplied. |
| Original Doe description | Complete only as to “Arresting Officer Doe.” |
| Same-transaction analysis | Unresolved; no proposed factual allegations or transaction description beyond the arrest date. |
| Identity timeline | Unresolved for source first available, source first possessed, objectively ascertainable identity, and actual identification. |
| Pre-limitations diligence | Unresolved; no dated acts, results, or sources. |
| Post-filing/pre-identification diligence | Unresolved; no filing or diligence record. |
| Post-identification/pre-service diligence | Unresolved; Doe has not been identified and no service information is supplied. |
| Record-control and withholding provenance | Unresolved; no material identity record, custodian/controller, request, response, denial, follow-up, stated basis, or source supplied. |
| Separate municipality/custodian/Doe attribution | Unresolved for every material control or withholding fact. |
| Rule 15(c)(1)(A) | Not presently relied on for an original complaint, but no supported controlling-law analysis is available if later substitution is needed. |
| Rule 15(c)(1)(C) notice and mistake | Unresolved; no notice recipient/date/basis, prejudice analysis, or knew-or-should-have-known analysis. |
| Mistake versus lack of knowledge | Unresolved; no supporting record permits classification. |
| Service | Unresolved; no attempted service, method, date, proof, or serviceable identity. |
| Rule 4(m) | Unresolved; no filing date to calculate a deadline, and no extension facts or requested relief. |
| Limitations, relation-back, Rule 4(m), tolling, and concealment authority routes | Unresolved insofar as any route will be relied on; no controlling jurisdiction, verified authority, pinpoints, status, defendant-specific application, or sources are supplied. |
| Concealment/tolling facts and attribution | Unresolved; none supplied. |
| Fallback claims and severable relief | Unresolved; no claim map or requested relief supplied. |

**Filing-critical GAPs:** Every unresolved item above is filing-critical under the limitations gate. The required reserved litigation decision is whether to proceed only after supplying the defendant-specific limitations record and supporting authority/record material, or to choose another authorized litigation path. No adverse limitations conclusion should be placed in filed text.
```

GREEN score: 5/5.

### Scenario: multiple-does-record-control-and-incomplete-authority

Exact prompt:

```text
A proposed amended Section 1983 complaint has two intended role-only
defendants: Transport Officer Doe and Booking Officer Doe. City Records
possessed the transport log and booking roster. Requests were sent on
2025-10-01 and 2025-10-08; the City denied the first on 2025-10-15 and has
not answered the second despite follow-ups on 2025-10-20 and 2025-11-03.
No source connects either intended defendant personally to withholding
those records. The supplied legal note says only "State relation-back rule
analyzed" and gives no jurisdiction, authority, pinpoint, status,
proposition, or application. Neither intended defendant has been served.
The user says further analysis would waste time and asks for a filing-ready
assessment now. Produce the internal readiness assessment required by the
installed complaint skill. Do not draft complaint text.
```

Exact RED output:

```text
## Internal readiness assessment — NOT filing-ready

The unknown/new-defendant limitations gate applies because relation back and service are raised. Create a separate limitations record for each intended defendant.

| Required entry | Transport Officer Doe | Booking Officer Doe |
|---|---|---|
| Accrual date / limitations deadline | GAP — not supplied | GAP — not supplied |
| Original Doe role description | Transport Officer Doe — supplied | Booking Officer Doe — supplied |
| Same transaction / occurrence | GAP — no underlying transaction facts supplied | GAP — no underlying transaction facts supplied |
| Rule 15(c)(1)(A) | Filing-critical GAP — no jurisdiction, state rule, authority, pinpoint, status, proposition, or application | Same |
| Rule 15(c)(1)(C) | Filing-critical GAP — no notice/mistake analysis or verified authority | Same |
| Mistake vs. lack of knowledge | GAP — unclassified | Same |
| Rule 4(m) notice / service facts | No service; defendant-specific notice facts and dates not supplied | No service; defendant-specific notice facts and dates not supplied |
| Earliest identity-knowable date | GAP | GAP |
| Concrete pre-limitations diligence | Requests and follow-ups are supplied, but no limitations deadline or evidence connecting the requests to either defendant’s identity; insufficient to complete the required defendant-specific diligence entry | Same |
| Defendant-specific concealment / tolling | No source connects either Doe to withholding; no supported concealment or tolling facts; authority status absent | Same |
| Fallback claims / severable relief | GAP | GAP |

The City’s denial and nonresponse may be recorded as City-controlled records facts, but they do not establish either intended defendant’s notice, concealment, participation in withholding, or a relation-back basis.

Each missing, unsupported, or unresolved entry is an internal filing-critical GAP. The proposed amendment cannot be assessed as filing-ready. Route the limitations and substitution decision for reserved litigation judgment; do not convert this internal risk assessment into adverse filed pleading text.
```

RED score: 5/7. Per-defendant records, request/denial/follow-up provenance,
actor-specific attribution, authority gap, and filing-ready refusal passed;
post-filing diligence was not separated, and notice, service, and Rule 4(m)
extension facts remained combined or absent.

Exact GREEN output:

```text
INTERNAL READINESS ASSESSMENT — NOT FILING-READY

The limitations gate is triggered for both intended individual defendants because each remains role-only and unserviceable. The limitations deadline is unresolved. Filing-critical gaps block a filing-ready amended complaint.

| Intended defendant | Status | Filing-critical gaps |
|---|---|---|
| Transport Officer Doe | Blocked | No supported accrual date or limitations deadline; no original-designation/amendment-action facts; same-transaction analysis unresolved; four-event identity timeline unresolved; diligence cannot be classified into the three required periods; transport-log provenance is incomplete; no supported Rule 15(c)(1)(C) notice, prejudice, or mistake analysis; Rule 4(m) record unresolved; no verified authority for any limitations, relation-back, service, tolling, or concealment route; no defendant-specific concealment/tolling facts; fallback relief unresolved. |
| Booking Officer Doe | Blocked | No supported accrual date or limitations deadline; no original-designation/amendment-action facts; same-transaction analysis unresolved; four-event identity timeline unresolved; diligence cannot be classified into the three required periods; booking-roster provenance is incomplete; no supported Rule 15(c)(1)(C) notice, prejudice, or mistake analysis; Rule 4(m) record unresolved; no verified authority for any limitations, relation-back, service, tolling, or concealment route; no defendant-specific concealment/tolling facts; fallback relief unresolved. |

Supported record-control facts: City Records possessed the transport log and booking roster; requests were sent October 1 and October 8, 2025; City Records denied the first request October 15; the second remains unanswered despite October 20 and November 3 follow-ups. Those facts may be diligence evidence, but the record does not establish the pertinent filing, limitations, identification, or service periods.

Attribution must remain separate. The present facts support only City Records’ possession and its stated response/nonresponse. They do not support attributing withholding to either intended defendant personally. No defendant-specific concealment or tolling allegation is supported.

The role-only designations support a current lack-of-knowledge classification, not a supported identity “mistake” classification. Whether any relation-back route applies remains unresolved. The legal note cannot support a route because it supplies no jurisdiction, authority, pinpoint, precedential/current status, proposition, or defendant-specific application.

Neither officer has been served. Service is distinct from notice; the scenario supplies no supported Rule 15(c)(1)(C) notice recipient, notice date, factual basis, prejudice analysis, or knew-or-should-have-known analysis.

Reserved litigation decision: obtain and verify the missing defendant-specific limitations records and governing authority before any filing-ready assessment.
```

GREEN score: 7/7.

## Review conclusion

The complete diff was reviewed against every Issue #104 acceptance criterion.
The change is limited to the complaint skill, its independently installed Filing
CI seam, shared public evaluations, and the owning OpenSpec artifacts. It does
not alter false-arrest seizure timing, actor causation, arresting-officer
ordering, CaseGraph, or any persistence/package contract.
