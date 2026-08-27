import copy
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from evaluations.deterministic import grade_candidate
from evaluations.fixtures import load_fixture


REPOSITORY = Path(__file__).resolve().parents[2]
SKILLS = REPOSITORY / "skills"
FIXTURES = REPOSITORY / "evaluations" / "fixtures"
GENERAL_PACKAGE = "drafting-section-1983-complaints"
FALSE_ARREST_PACKAGE = "drafting-false-arrest-complaints"
COMPLAINT_CONTRACT = "references/complaint-contract.md"
COMPLETION_AUDIT = "references/completion-audit.md"
FALSE_ARREST_DELTA = "references/false-arrest-complaint-delta.md"
EXPECTED_FIXTURES = {
    "complaint-adverse-merits-self-assessment": {
        "target_skill": GENERAL_PACKAGE,
        "location": "filed-adverse-merits-assessment",
        "assets": {
            "approved-facts-and-authority.md",
            "approved-filing-boundary.md",
            "fixture.json",
            "passing.md",
            "prompt.md",
            "regression-filed-assessment.md",
            "sources.json",
        },
    },
    "complaint-fair-warning-brief-creep": {
        "target_skill": GENERAL_PACKAGE,
        "location": "unexplained-string-cite",
        "assets": {
            "approved-authority-record.md",
            "approved-fair-warning-boundary.md",
            "fixture.json",
            "passing.md",
            "prompt.md",
            "regression-string-cite.md",
            "sources.json",
        },
    },
    "complaint-nonfunctional-uncertainty": {
        "target_skill": GENERAL_PACKAGE,
        "location": "retained-uncertainty-without-job",
        "assets": {
            "approved-pruning-boundary.md",
            "approved-uncertain-paragraphs.md",
            "fixture.json",
            "passing.md",
            "prompt.md",
            "regression-retained-uncertainty.md",
            "sources.json",
        },
    },
    "complaint-ambiguous-alternative-offense": {
        "target_skill": FALSE_ARREST_PACKAGE,
        "location": "ambiguous-fact-admitted-or-unresolved-effect",
        "assets": {
            "approved-offense-and-record.md",
            "approved-offense-boundary.md",
            "fixture.json",
            "passing.md",
            "prompt.md",
            "regression-unresolved-effect.md",
            "sources.json",
        },
    },
    "complaint-open-actor-unit": {
        "target_skill": FALSE_ARREST_PACKAGE,
        "location": "paragraph-range-without-application",
        "assets": {
            "approved-authority.md",
            "approved-facts.md",
            "fixture.json",
            "passing.md",
            "prompt.md",
            "regression-open-actor-unit.md",
            "sources.json",
        },
    },
}

CONFORMING_ADVERSE_MERITS = """
Filed text may accurately qualify what a source proves and state a factual
source limitation as unresolved. Supported alternative or conditional pleading
is permitted. Filed text must not describe its own claim, element, fair-warning
path, or qualified-immunity position as weak, likely to fail, likely barred, or
legally deficient. Legal merits and strength assessment must be routed to
versioned strategy or an internal audit. That route does not permit concealment
of contrary evidence or authority.
"""

CONFORMING_FAIR_WARNING = """
Each distinct complaint-level fair-warning proposition must ordinarily use one
verified lead binding pre-event authority and the decisive factual comparison.
Any additional complaint-level authority must perform a separately identified
job. Full comparison matrices, competing case discussions, later history, and
string cites must remain in internal work product or a brief. The limit is
functional, not a universal numeric maximum.
"""

CONFORMING_UNCERTAINTY_AUDIT = """
The completion audit must inventory every factual paragraph that the draft
labels unresolved, unknown, unrelated, or non-establishing. Each retained
paragraph must identify at least one function: an element, an actual defense
premise, a material chronology function, or a candor/preservation function. A
paragraph with no such function must be removed from filed text or moved to
internal chronology.
"""

CONFORMING_ACTUAL_OFFENSE = """
For each alternative offense actually raised by the defense, a controlling
ruling, or governing law, identify any incorporated-record fact left unresolved
that is material to an offense element. Without admitting the fact occurred,
map the unresolved fact to the offense element and either state the supported
element-level reason it does not supply probable cause or arguable probable
cause or record a filing-critical GAP. The specialization must not inventory
merely conceivable offenses.
"""

CONFORMING_CANONICAL_CHECKLIST = """
### Canonical claim-defendant-challenged-act checklist

Use one checklist for each claim, defendant, and challenged act. Record these
universal fields: claim; defendant; challenged act and event stage; governing
element and standard; decisive facts; relevant-time knowledge; element-specific
legal application; and result.

When qualified immunity applies, also record these conditional fields: event
date; conduct-specific right or rule; verified binding pre-event authority;
authority-audit status; materially similar facts; material differences;
defendant-specific fair warning; rule-of-orderliness and later-history review
status; prong one result; and prong two result.

If a required universal field is missing or unverified, the mapping is
incomplete. If a conditional qualified-immunity field is missing or unverified,
record an internal filing-critical GAP, do not mark the complaint filing-ready,
and route the GAP to a reserved strategy decision without placing an adverse
merits assessment in filed text. This checklist does not duplicate detailed
authority verification owned by `audit-authorities`.
"""


def normalized_value(text):
    return re.sub(r"\s+", " ", text).strip().casefold()


def normalized_prose(path):
    text = path.read_text(encoding="utf-8")
    visible = []
    fence = None
    for line in text.splitlines(keepends=True):
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            if opening and opening.group(1)[0] == fence[0] and len(opening.group(1)) >= len(fence):
                fence = None
            continue
        if opening:
            fence = opening.group(1)
            continue
        visible.append(line)
    return normalized_value("".join(visible))


def clauses(text):
    return tuple(
        clause.strip()
        for clause in re.split(r"(?<=[.!?])\s+", text)
        if clause.strip()
    )


def assert_clause_contains(test, text, *patterns):
    for clause in clauses(text):
        if all(re.search(pattern, clause) for pattern in patterns):
            return
    test.fail(f"no operative clause contains: {patterns}")


def assert_no_clause_contains(test, text, *patterns):
    for clause in clauses(text):
        if all(re.search(pattern, clause) for pattern in patterns):
            test.fail(f"contradictory operative clause: {clause}")


def copied_package(directory, package_name):
    package = Path(directory) / "skills" / package_name
    shutil.copytree(SKILLS / package_name, package, symlinks=True)
    return package


def finding_pairs(result):
    return {
        (finding["id"], finding.get("location"))
        for finding in result["findings"]
    }


def insert_before_heading(candidate, heading, insertion):
    marker = f"\n# {heading}\n"
    replacement = f"\n{insertion}\n\n# {heading}\n"
    replaced = candidate.replace(marker, replacement, 1)
    if replaced == candidate:
        raise AssertionError(f"heading unavailable: {heading}")
    return replaced


def replace_once(candidate, old, new):
    replaced = candidate.replace(old, new, 1)
    if replaced == candidate:
        raise AssertionError(f"candidate text unavailable: {old}")
    return replaced


def markdown_sections(markdown, heading_pattern):
    lines = markdown.splitlines()
    sections = []
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if not match or not re.search(heading_pattern, match.group(2), re.I):
            continue
        level = len(match.group(1))
        end = len(lines)
        for candidate_index in range(index + 1, len(lines)):
            candidate = re.match(r"^(#{1,6})\s+", lines[candidate_index])
            if candidate and len(candidate.group(1)) <= level:
                end = candidate_index
                break
        sections.append("\n".join(lines[index:end]))
    return tuple(sections)


def assert_authority_verification_ownership(test, text):
    assert_clause_contains(
        test,
        normalized_value(text),
        r"(?:does not|must not|do not)",
        r"duplicate",
        r"detailed authority verification",
        r"(?:owned by|belongs to|performed by).{0,40}`?audit-authorities`?",
    )


def assert_canonical_claim_checklist(test, markdown):
    sections = markdown_sections(
        markdown,
        r"canonical claim[-–— ]defendant[-–— ]challenged[- ]act checklist",
    )
    test.assertEqual(len(sections), 1, "one canonical claim checklist is required")
    if len(sections) != 1:
        return
    text = normalized_value(sections[0])
    qualified_immunity_checklists = []
    for checklist in markdown_sections(markdown, r"\bchecklist\b"):
        heading = normalized_value(checklist.splitlines()[0])
        checklist_text = normalized_value(checklist)
        heading_claims_qualified_immunity = re.search(
            r"qualified[- ]immunity.*checklist|checklist.*qualified[- ]immunity",
            heading,
        )
        body_claims_conditional_interface = (
            re.search(
                r"conditional qualified[- ]immunity field|when qualified immunity applies",
                checklist_text,
            )
            and re.search(r"prong one result|separate prong results", checklist_text)
        )
        if heading_claims_qualified_immunity or body_claims_conditional_interface:
            qualified_immunity_checklists.append(checklist)
    test.assertEqual(
        len(qualified_immunity_checklists),
        1,
        "one checklist must own qualified-immunity completion",
    )
    if len(qualified_immunity_checklists) == 1:
        test.assertEqual(
            normalized_value(qualified_immunity_checklists[0]),
            text,
            "the canonical claim checklist must own qualified-immunity completion",
        )
    universal_fields = (
        r"\bclaim\b",
        r"\bdefendant\b",
        r"challenged act",
        r"event stage",
        r"governing (?:element|standard)",
        r"decisive facts",
        r"relevant[- ]time knowledge",
        r"element[- ]specific legal application",
        r"\bresult\b",
    )
    conditional_fields = (
        r"event date",
        r"conduct[- ]specific (?:right|rule)",
        r"verified binding pre[- ]event authority",
        r"authority[- ]audit status",
        r"materially similar facts",
        r"material differences",
        r"defendant[- ]specific fair warning",
        r"rule[- ]of[- ]orderliness",
        r"later[- ]history review status",
        r"prong one result",
        r"prong two result",
    )
    for field in universal_fields + conditional_fields:
        with test.subTest(field=field):
            test.assertRegex(text, field)
    test.assertRegex(text, r"(?:conditional|when).{0,80}qualified immunity")
    assert_clause_contains(
        test,
        text,
        r"required universal field",
        r"missing or unverified",
        r"mapping is incomplete",
    )
    assert_no_clause_contains(
        test,
        text,
        r"required universal field",
        r"missing or unverified",
        r"mapping is incomplete",
        r"unless",
        r"reserved strategy",
        r"treats? it (?:as )?complete",
    )
    assert_clause_contains(
        test,
        text,
        r"conditional qualified[- ]immunity field",
        r"missing or unverified",
        r"internal filing[- ]critical gap",
        r"(?:do not|must not).{0,80}(?:mark|treat).{0,80}filing[- ]ready",
        r"reserved strategy decision",
        r"(?:without|no).{0,100}adverse merits assessment.{0,80}filed text",
    )
    assert_no_clause_contains(
        test,
        text,
        r"conditional qualified[- ]immunity field",
        r"missing or unverified",
        r"internal filing[- ]critical gap",
        r"unless",
        r"strategy waives",
    )
    assert_no_clause_contains(
        test,
        text,
        r"adverse merits assessment",
        r"filed text",
        r"unless",
        r"strategy approves",
    )
    assert_authority_verification_ownership(test, sections[0])


def assert_no_adverse_merits_self_assessment(test, text):
    assert_clause_contains(
        test,
        text,
        r"filed (?:complaint|text)",
        r"(?:must not|shall not|do not)",
        r"claim",
        r"element",
        r"fair[- ]warning",
        r"qualified[- ]immunity",
        r"(?:weak|likely to fail|likely barred|legally deficient)",
    )
    assert_clause_contains(
        test,
        text,
        r"\baccurat(?:e|ely)\b",
        r"(?:source|record|evidence)",
        r"(?:limitation|unresolved|uncertain)",
    )
    assert_clause_contains(
        test,
        text,
        r"\bsupported\b",
        r"(?:alternative|conditional) pleading",
        r"(?:permitted|allowed|may|preserve)",
    )
    assert_clause_contains(
        test,
        text,
        r"(?:risk|merits|strength) assessment",
        r"(?:versioned strategy|internal audit)",
    )
    assert_clause_contains(
        test,
        text,
        r"(?:does not|must not|may not).*(?:conceal|hide)",
        r"(?:adverse|contrary)",
        r"evidence",
        r"authority",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:may|allowed|permitted)",
        r"(?:assess|characterize|describe|label)",
        r"(?:claim|element|fair[- ]warning|qualified[- ]immunity)",
        r"(?:weak|likely to fail|likely barred|legally deficient)",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:may|allowed|permitted)",
        r"(?:call|assess|characterize|describe|label)",
        r"(?:claim|element|fair[- ]warning|qualified[- ]immunity|immunity)",
        r"\b(?:contested|doubtful)\b",
    )


def assert_bounded_fair_warning_authority(test, text):
    assert_clause_contains(
        test,
        text,
        r"(?:each|per) distinct (?:complaint[- ]level )?fair[- ]warning proposition",
        r"(?:ordinarily|default)",
        r"one verified lead binding pre[- ]event authority",
    )
    assert_clause_contains(
        test,
        text,
        r"(?:additional|another|second) complaint[- ]level authority",
        r"(?:separately identified|distinct) job",
    )
    assert_clause_contains(
        test,
        text,
        r"(?:comparison|matrix)",
        r"(?:string cite|competing case)",
        r"(?:remain|stay|route|keep)",
        r"(?:internal|brief)",
    )
    assert_clause_contains(
        test,
        text,
        r"functional",
        r"not",
        r"(?:universal|absolute|numeric)",
        r"(?:maximum|cap|limit)",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:never|must not|do not)",
        r"(?:cite|use)",
        r"more than one authority per count",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:may|can|allowed|permitted)",
        r"(?:include|use|add)",
        r"unexplained",
        r"(?:multi[- ]case|string cite)",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:may|can|allowed|permitted)",
        r"(?:additional|another|second) complaint[- ]level authority",
        r"(?:repeat|duplicate)",
        r"(?:without|no).*(?:separate|distinct) job",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:additional|another|second) complaint[- ]level authority",
        r"(?:separately identified|distinct) job",
        r"\bunless\b",
        r"repeat.*lead authority",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:complaint|count)",
        r"(?:limited|capped|maximum|no more than)",
        r"one authority",
        r"per count",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:may|can|allowed|permitted)",
        r"(?:comparison|matrix|string cite)",
        r"filed (?:complaint|text)",
    )


def assert_uncertainty_purpose_audit(test, text):
    assert_clause_contains(
        test,
        text,
        r"(?:inventory|identify)",
        r"(?:every|each)",
        r"(?:factual )?paragraph",
        r"unresolved",
        r"unknown",
        r"unrelated",
        r"non[- ]establishing",
    )
    assert_clause_contains(
        test,
        text,
        r"(?:each|every) retained paragraph",
        r"(?:must|required)",
        r"(?:at least one|one or more)",
        r"element",
        r"(?:actual|actually raised) defense",
        r"\bmaterial chronology\b",
        r"(?:candor|preservation)",
    )
    assert_clause_contains(
        test,
        text,
        r"(?:no|without).*(?:job|function)",
        r"(?:must|direct|require)",
        r"(?:remove|removed|prune)",
        r"(?:move|moved)",
        r"(?:internal chronology|internal work product)",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:paragraph|uncertainty)",
        r"(?:no|without).*(?:job|function)",
        r"(?:may|can|allowed|permitted).*(?:remain|retain|keep|kept)",
        r"filed (?:complaint|text)",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:paragraph|uncertainty)",
        r"(?:no|without).*(?:job|function)",
        r"(?:may|can|allowed|permitted).*(?:remain|retain|keep|kept)",
        r"narrative flow",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:paragraph|uncertainty)",
        r"(?:no|without).*(?:job|function)",
        r"(?:remove|removed|move|moved)",
        r"\bunless\b",
        r"narrative flow.*retention",
    )


def assert_ambiguous_actual_offense_analysis(test, text):
    assert_clause_contains(
        test,
        text,
        r"(?:alternative )?offense",
        r"actually raised by (?:the )?defense",
        r"controlling ruling",
        r"governing law",
    )
    assert_clause_contains(
        test,
        text,
        r"incorporated[- ](?:record|recording|material)",
        r"(?:unresolved|ambiguous)",
        r"(?:fact|conduct)",
        r"\bmaterial to (?:an |the )?offense element\b",
    )
    assert_clause_contains(
        test,
        text,
        r"(?:identify|map)",
        r"(?:unresolved|ambiguous|disputed) fact",
        r"offense element",
    )
    assert_clause_contains(
        test,
        text,
        r"(?:without|do not|must not).*(?:admit|admitting|admission)",
        r"(?:fact|conduct)",
    )
    assert_clause_contains(
        test,
        text,
        r"\bsupported\b",
        r"\bdoes not supply\b",
        r"\bprobable cause\b",
        r"\barguable probable cause\b",
        r"filing[- ]critical gap",
    )
    assert_clause_contains(
        test,
        text,
        r"(?:do not|must not)",
        r"(?:add|inventory|address)",
        r"(?:every|merely) conceivable offense",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:may|can|allowed|permitted|should)",
        r"(?:admit|admitted|admission)",
        r"(?:unresolved|ambiguous|ambiguity).*(?:fact|conduct)|"
        r"(?:fact|conduct).*(?:unresolved|ambiguous|ambiguity)",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:may|can|allowed|permitted)",
        r"(?:leave|omit|skip)",
        r"(?:offense|probable cause)",
        r"(?:effect|analysis|unresolved)",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:may|can|allowed|permitted)",
        r"(?:add|inventory|address)",
        r"merely conceivable offenses?",
    )
    assert_no_clause_contains(
        test,
        text,
        r"(?:may|can|allowed|permitted)",
        r"(?:treat|regard|accept)",
        r"(?:unresolved|ambiguous).*(?:fact|conduct)|"
        r"(?:fact|conduct).*(?:unresolved|ambiguous)",
        r"(?:as true|as established)",
    )


def assert_closed_actor_unit_contract(test, text):
    assert_clause_contains(
        test,
        text,
        r"(?:each|every) claim.{0,30}defendant.{0,30}challenged[- ]act",
        r"(?:own|actor[- ]specific) incorporated (?:factual )?paragraphs",
    )
    assert_clause_contains(
        test,
        text,
        r"omnibus incorporation",
        r"to the extent applicable",
        r"(?:insufficient|does not satisfy)",
        r"(?:different|differ)",
        r"(?:acts|stages|knowledge)",
    )
    assert_clause_contains(
        test,
        text,
        r"paragraph range",
        r"(?:does not|cannot)",
        r"(?:perform|supply)",
        r"application",
    )
    required_fields = (
        r"challenged act",
        r"event time",
        r"decisive facts",
        r"known to (?:that|the) defendant",
        r"disputed (?:claim or offense )?element",
        r"(?:establish|fail to establish).{0,40}element",
        r"later.{0,30}(?:cannot|must not).{0,40}(?:knowledge set|relevant[- ]time knowledge)",
        r"personal causal role",
        r"resulting injury",
        r"qualified[- ]immunity prongs? one and two|both qualified[- ]immunity prongs",
    )
    for field in required_fields:
        with test.subTest(closed_actor_field=field):
            test.assertRegex(text, field)
    assert_clause_contains(
        test,
        text,
        r"functional closure",
        r"(?:does not|must not)",
        r"fixed paragraph count",
        r"needless repetition",
    )
    assert_clause_contains(
        test,
        text,
        r"supporting brief",
        r"may expand",
        r"(?:cannot|must not|may not) supply",
        r"missing complaint[- ]level",
        r"application|factual bridge",
    )


def assert_completion_audit_rejects_open_actor_units(test, text):
    required_failures = (
        r"court must (?:search|gather).{0,80}(?:construct|supply).{0,80}(?:fact[- ]to[- ]element|element analysis|application)",
        r"(?:officers|actors|defendants).{0,60}(?:different acts|different stages|different knowledge|acts, stages, or knowledge).{0,80}(?:broad|omnibus) incorporation",
        r"qualified[- ]immunity.{0,60}paragraph range.{0,60}conclusion",
        r"later[- ]only facts.{0,80}(?:knowledge set|relevant[- ]time knowledge).{0,80}(?:express|limited[- ]use)",
        r"brief.{0,80}(?:cure|supply).{0,80}missing complaint[- ]level",
    )
    for failure in required_failures:
        with test.subTest(open_actor_failure=failure):
            test.assertRegex(text, failure)
    assert_clause_contains(
        test,
        text,
        r"unresolved",
        r"required (?:component|part|field)",
        r"filing[- ]critical",
    )


def assert_false_arrest_closed_actor_unit(test, text):
    required_fields = (
        r"(?:each|every) (?:challenged )?officer",
        r"seizure or continued[- ]seizure point|seizure point",
        r"suspected offense",
        r"alternative offense.{0,80}actually raised",
        r"facts known to that officer",
        r"missing or disputed element",
        r"post[- ]seizure identification",
        r"resistance",
        r"reports?",
        r"probable[- ]cause and arguable[- ]probable[- ]cause application",
        r"personal participation",
        r"causal stage",
        r"resulting injury",
        r"conduct[- ]specific fair[- ]warning",
        r"qualified[- ]immunity prongs? one and two|both qualified[- ]immunity prongs",
    )
    for field in required_fields:
        with test.subTest(false_arrest_actor_field=field):
            test.assertRegex(text, field)
    assert_clause_contains(
        test,
        text,
        r"post[- ]seizure|later",
        r"(?:limited later function|exclude|not part)",
        r"(?:contemporaneous|relevant[- ]time|earlier) knowledge",
    )


class ComplaintCandorContractTest(unittest.TestCase):
    def test_conforming_canonical_checklist_satisfies_the_contract(self):
        assert_canonical_claim_checklist(self, CONFORMING_CANONICAL_CHECKLIST)
        with self.assertRaises(AssertionError):
            assert_canonical_claim_checklist(
                self,
                CONFORMING_CANONICAL_CHECKLIST + CONFORMING_CANONICAL_CHECKLIST,
            )

    def test_collapsed_universal_and_qi_gap_rule_is_rejected(self):
        collapsed = replace_once(
            CONFORMING_CANONICAL_CHECKLIST,
            "If a required universal field is missing or unverified, the mapping is\n"
            "incomplete. If a conditional qualified-immunity field is missing or "
            "unverified,\nrecord an internal filing-critical GAP",
            "If any required universal or conditional qualified-immunity field is "
            "missing or\nunverified, record an internal filing-critical GAP",
        )
        with self.assertRaises(AssertionError):
            assert_canonical_claim_checklist(self, collapsed)

    def test_universal_completion_unless_exception_is_rejected(self):
        mutation = replace_once(
            CONFORMING_CANONICAL_CHECKLIST,
            "the mapping is\nincomplete",
            "the mapping is incomplete unless reserved strategy treats it as complete",
        )
        with self.assertRaises(AssertionError):
            assert_canonical_claim_checklist(self, mutation)

    def test_conditional_qi_gap_unless_exception_is_rejected(self):
        mutation = replace_once(
            CONFORMING_CANONICAL_CHECKLIST,
            "record an internal filing-critical GAP",
            "record an internal filing-critical GAP unless strategy waives it",
        )
        with self.assertRaises(AssertionError):
            assert_canonical_claim_checklist(self, mutation)

    def test_adverse_filed_assessment_unless_exception_is_rejected(self):
        mutation = replace_once(
            CONFORMING_CANONICAL_CHECKLIST,
            "without placing an adverse\nmerits assessment in filed text",
            "without placing an adverse merits assessment in filed text unless "
            "strategy approves",
        )
        with self.assertRaises(AssertionError):
            assert_canonical_claim_checklist(self, mutation)

    def test_second_qi_completion_checklist_is_rejected(self):
        mutation = CONFORMING_CANONICAL_CHECKLIST + """

### Separate qualified-immunity completion checklist

When qualified immunity applies, record event date, authority-audit status,
fair warning, and separate prong results.
"""
        with self.assertRaises(AssertionError):
            assert_canonical_claim_checklist(self, mutation)

    def test_general_contract_has_one_canonical_claim_checklist(self):
        with tempfile.TemporaryDirectory() as directory:
            package = copied_package(directory, GENERAL_PACKAGE)
            contract = (package / COMPLAINT_CONTRACT).read_text(encoding="utf-8")
            assert_canonical_claim_checklist(self, contract)

    def test_general_contract_defers_detailed_authority_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            package = copied_package(directory, GENERAL_PACKAGE)
            contract = (package / COMPLAINT_CONTRACT).read_text(encoding="utf-8")
            assert_authority_verification_ownership(self, contract)

    def test_authoritative_conforming_samples_satisfy_each_contract(self):
        conforming = (
            (
                assert_no_adverse_merits_self_assessment,
                CONFORMING_ADVERSE_MERITS,
            ),
            (assert_bounded_fair_warning_authority, CONFORMING_FAIR_WARNING),
            (assert_uncertainty_purpose_audit, CONFORMING_UNCERTAINTY_AUDIT),
            (assert_ambiguous_actual_offense_analysis, CONFORMING_ACTUAL_OFFENSE),
        )
        for assertion, sample in conforming:
            with self.subTest(assertion=assertion.__name__):
                assertion(self, normalized_value(sample))

    def test_independent_general_package_prohibits_adverse_merits_assessment(self):
        with tempfile.TemporaryDirectory() as directory:
            package = copied_package(directory, GENERAL_PACKAGE)
            assert_no_adverse_merits_self_assessment(
                self,
                normalized_prose(package / COMPLAINT_CONTRACT),
            )

    def test_independent_general_package_bounds_fair_warning_authority_by_job(self):
        with tempfile.TemporaryDirectory() as directory:
            package = copied_package(directory, GENERAL_PACKAGE)
            assert_bounded_fair_warning_authority(
                self,
                normalized_prose(package / COMPLAINT_CONTRACT),
            )

    def test_independent_general_package_prunes_uncertainty_without_a_pleaded_job(self):
        with tempfile.TemporaryDirectory() as directory:
            package = copied_package(directory, GENERAL_PACKAGE)
            assert_uncertainty_purpose_audit(
                self,
                normalized_prose(package / COMPLETION_AUDIT),
            )

    def test_independent_false_arrest_package_completes_actual_offense_analysis(self):
        with tempfile.TemporaryDirectory() as directory:
            package = copied_package(directory, FALSE_ARREST_PACKAGE)
            assert_ambiguous_actual_offense_analysis(
                self,
                normalized_prose(package / FALSE_ARREST_DELTA),
            )

    def test_independent_general_package_requires_closed_actor_units(self):
        with tempfile.TemporaryDirectory() as directory:
            package = copied_package(directory, GENERAL_PACKAGE)
            assert_closed_actor_unit_contract(
                self,
                normalized_prose(package / COMPLAINT_CONTRACT),
            )

    def test_independent_general_completion_audit_rejects_open_actor_units(self):
        with tempfile.TemporaryDirectory() as directory:
            package = copied_package(directory, GENERAL_PACKAGE)
            assert_completion_audit_rejects_open_actor_units(
                self,
                normalized_prose(package / COMPLETION_AUDIT),
            )

    def test_independent_false_arrest_package_requires_closed_actor_units(self):
        with tempfile.TemporaryDirectory() as directory:
            package = copied_package(directory, FALSE_ARREST_PACKAGE)
            assert_false_arrest_closed_actor_unit(
                self,
                normalized_prose(package / FALSE_ARREST_DELTA),
            )

    def test_adverse_merits_permission_mutation_is_rejected(self):
        text = normalized_value(CONFORMING_ADVERSE_MERITS)
        assert_no_adverse_merits_self_assessment(self, text)
        mutation = text.replace(
            "must not describe its own claim",
            "may describe its own claim",
            1,
        )
        self.assertNotEqual(mutation, text)
        with self.assertRaises(AssertionError):
            assert_no_adverse_merits_self_assessment(self, mutation)

    def test_unexplained_string_cite_and_absolute_cap_mutations_are_rejected(self):
        text = normalized_value(CONFORMING_FAIR_WARNING)
        assert_bounded_fair_warning_authority(self, text)
        mutations = (
            text + " A complaint may include unexplained multi-case string cites.",
            text + " Never cite more than one authority per count.",
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation[len(text) :].strip()):
                with self.assertRaises(AssertionError):
                    assert_bounded_fair_warning_authority(
                        self,
                        normalized_value(mutation),
                    )

    def test_no_job_retention_mutation_is_rejected(self):
        text = normalized_value(CONFORMING_UNCERTAINTY_AUDIT)
        assert_uncertainty_purpose_audit(self, text)
        mutation = text.replace(
            "must be removed from filed text or moved to internal chronology",
            "may be kept in the filed complaint",
            1,
        )
        self.assertNotEqual(mutation, text)
        with self.assertRaises(AssertionError):
            assert_uncertainty_purpose_audit(self, mutation)

    def test_actual_offense_semantic_inversions_are_rejected(self):
        text = normalized_value(CONFORMING_ACTUAL_OFFENSE)
        assert_ambiguous_actual_offense_analysis(self, text)
        admission = text.replace(
            "without admitting the fact occurred",
            "by admitting the unresolved fact occurred",
            1,
        )
        unresolved_effect = text.replace(
            "either state the supported element-level reason it does not supply "
            "probable cause or arguable probable cause or record a filing-critical gap",
            "leave the unresolved fact's offense effect unanalyzed",
            1,
        )
        conceivable_expansion = (
            text + " The specialization may add merely conceivable offenses."
        )
        self.assertNotEqual(admission, text)
        self.assertNotEqual(unresolved_effect, text)
        for mutation in (admission, unresolved_effect, conceivable_expansion):
            with self.subTest(mutation=mutation):
                with self.assertRaises(AssertionError):
                    assert_ambiguous_actual_offense_analysis(self, mutation)

    def test_adjacent_no_concession_mutations_are_rejected(self):
        text = normalized_value(CONFORMING_ADVERSE_MERITS)
        mutations = (
            text.replace("accurately qualify", "inaccurately qualify", 1),
            text.replace("supported alternative", "unsupported alternative", 1),
            text
            + " Filed text may call its fair-warning path contested and doubtful.",
        )
        for mutation in mutations:
            self.assertNotEqual(mutation, text)
            with self.subTest(mutation=mutation):
                with self.assertRaises(AssertionError):
                    assert_no_adverse_merits_self_assessment(self, mutation)

    def test_adjacent_fair_warning_mutations_are_rejected(self):
        text = normalized_value(CONFORMING_FAIR_WARNING)
        surplus_in_filed_text = text.replace(
            "must remain in internal work product or a brief",
            "may remain in filed complaint text or a brief",
            1,
        )
        mutations = (
            text
            + " An additional complaint-level authority may repeat the lead "
            "authority without a separate job.",
            text + " The complaint is limited to one authority per count.",
            surplus_in_filed_text,
        )
        for mutation in mutations:
            self.assertNotEqual(mutation, text)
            with self.subTest(mutation=mutation):
                with self.assertRaises(AssertionError):
                    assert_bounded_fair_warning_authority(self, mutation)

    def test_inline_repeated_authority_unless_exception_is_rejected(self):
        text = normalized_value(CONFORMING_FAIR_WARNING)
        mutation = text.replace(
            "must perform a separately identified job",
            "must perform a separately identified job unless it repeats the "
            "lead authority",
            1,
        )
        self.assertNotEqual(mutation, text)
        with self.assertRaises(AssertionError):
            assert_bounded_fair_warning_authority(self, mutation)

    def test_adjacent_uncertainty_mutations_are_rejected(self):
        text = normalized_value(CONFORMING_UNCERTAINTY_AUDIT)
        mutations = (
            text.replace("material chronology", "immaterial chronology", 1),
            text
            + " A paragraph without a permitted function may remain in filed "
            "text when narrative flow favors retention.",
        )
        for mutation in mutations:
            self.assertNotEqual(mutation, text)
            with self.subTest(mutation=mutation):
                with self.assertRaises(AssertionError):
                    assert_uncertainty_purpose_audit(self, mutation)

    def test_inline_narrative_flow_unless_exception_is_rejected(self):
        text = normalized_value(CONFORMING_UNCERTAINTY_AUDIT)
        mutation = text.replace(
            "must be removed from filed text or moved to internal chronology",
            "must be removed from filed text or moved to internal chronology "
            "unless narrative flow favors retention",
            1,
        )
        self.assertNotEqual(mutation, text)
        with self.assertRaises(AssertionError):
            assert_uncertainty_purpose_audit(self, mutation)

    def test_adjacent_actual_offense_mutations_are_rejected(self):
        text = normalized_value(CONFORMING_ACTUAL_OFFENSE)
        mutations = (
            text.replace(
                "material to an offense element",
                "immaterial to an offense element",
                1,
            ),
            text.replace(
                "supported element-level reason",
                "unsupported element-level reason",
                1,
            ),
            text.replace("does not supply probable cause", "does supply probable cause", 1),
            text
            + " When the recording is ambiguous, the unresolved fact may be "
            "treated as true.",
        )
        for mutation in mutations:
            self.assertNotEqual(mutation, text)
            with self.subTest(mutation=mutation):
                with self.assertRaises(AssertionError):
                    assert_ambiguous_actual_offense_analysis(self, mutation)

    def test_fixture_adjacent_violations_emit_the_target_finding(self):
        adverse = load_fixture(
            FIXTURES / "complaint-adverse-merits-self-assessment"
        )
        fair_warning = load_fixture(
            FIXTURES / "complaint-fair-warning-brief-creep"
        )
        pruning = load_fixture(FIXTURES / "complaint-nonfunctional-uncertainty")
        offense = load_fixture(
            FIXTURES / "complaint-ambiguous-alternative-offense"
        )
        adverse_probes = (
            "The fair-warning precedent is doubtful and too uncertain to "
            "overcome immunity.",
            "The claim is contested and likely barred.",
        )
        fair_warning_probes = (
            "CASE-2 repeats the lead proposition.",
            "CASE-3, with different punctuation, repeats the lead proposition.",
        )
        pruning_probes = (
            "P2 remains in the filed facts for completeness.",
            "P4 remains in the filed facts for completeness.",
            "P6 remains in the filed facts for completeness.",
            "The unknown vehicle color remains for completeness.",
            "The unrelated building detail remains for completeness.",
            "The unknown background detail remains for completeness.",
        )
        effect_sentence = (
            "The\nunresolved possibility of Conduct C therefore does not supply "
            "probable or\narguable probable cause for Offense Z because the "
            "required Z2 basis remains\nabsent from the approved arrest-time record."
        )
        offense_probes = (
            replace_once(
                offense["passing_candidate"],
                effect_sentence,
                "No conclusion is offered about Conduct C's effect on the "
                "required offense elements.",
            ),
            replace_once(
                offense["passing_candidate"],
                effect_sentence,
                "The effect of Conduct C is deferred until later briefing.",
            ),
            replace_once(
                offense["passing_candidate"],
                "The\nrecording does not resolve whether Conduct C occurred, and "
                "Plaintiff does not\nadmit that it did.",
                "Conduct C is treated as established.",
            ),
            replace_once(offense["passing_candidate"], effect_sentence, ""),
        )
        probes = tuple(
            (
                adverse,
                insert_before_heading(
                    adverse["passing_candidate"],
                    "Internal Strategy Note",
                    probe,
                ),
                "filed-adverse-merits-assessment",
            )
            for probe in adverse_probes
        )
        probes += tuple(
            (
                fair_warning,
                insert_before_heading(
                    fair_warning["passing_candidate"],
                    "Internal Authority Matrix",
                    probe,
                ),
                "unexplained-string-cite",
            )
            for probe in fair_warning_probes
        )
        probes += tuple(
            (
                pruning,
                insert_before_heading(
                    pruning["passing_candidate"],
                    "Internal Chronology",
                    probe,
                ),
                "retained-uncertainty-without-job",
            )
            for probe in pruning_probes
        )
        probes += tuple(
            (
                offense,
                candidate,
                "ambiguous-fact-admitted-or-unresolved-effect",
            )
            for candidate in offense_probes
        )
        for fixture, candidate, location in probes:
            with self.subTest(fixture=fixture["id"]):
                self.assertEqual(
                    finding_pairs(grade_candidate(fixture, candidate)),
                    {("banned-pattern", location)},
                )

    def test_fixture_adjacent_safe_candidates_grade_cleanly(self):
        adverse = load_fixture(
            FIXTURES / "complaint-adverse-merits-self-assessment"
        )
        fair_warning = load_fixture(
            FIXTURES / "complaint-fair-warning-brief-creep"
        )
        pruning = load_fixture(FIXTURES / "complaint-nonfunctional-uncertainty")
        offense = load_fixture(
            FIXTURES / "complaint-ambiguous-alternative-offense"
        )
        effect_sentence = (
            "The\nunresolved possibility of Conduct C therefore does not supply "
            "probable or\narguable probable cause for Offense Z because the "
            "required Z2 basis remains\nabsent from the approved arrest-time record."
        )
        gap_candidate = replace_once(
            offense["passing_candidate"],
            effect_sentence,
            "The approved record does not permit a supported conclusion about "
            "the unresolved fact's effect on Z2.",
        )
        gap_candidate = replace_once(
            gap_candidate,
            "None for this bounded issue. The approved offense rule and record "
            "permit the\nelement-level conclusion above without resolving "
            "Conduct C against Plaintiff.",
            "Z2 arrest-time support is missing, so the filing-critical GAP is "
            "reserved for a strategy decision.",
        )
        safe_candidates = (
            (
                adverse,
                insert_before_heading(
                    adverse["passing_candidate"],
                    "Internal Strategy Note",
                    "The claim does not depend on weak signal evidence from SRC-1.",
                ),
            ),
            (fair_warning, fair_warning["passing_candidate"]),
            (pruning, pruning["passing_candidate"]),
            (offense, offense["passing_candidate"]),
            (offense, gap_candidate),
        )
        for fixture, candidate in safe_candidates:
            with self.subTest(fixture=fixture["id"]):
                result = grade_candidate(fixture, candidate)
                self.assertTrue(result["passed"])
                self.assertEqual(result["findings"], [])

    def test_causal_first_actual_offense_candidate_grades_cleanly(self):
        fixture = load_fixture(
            FIXTURES / "complaint-ambiguous-alternative-offense"
        )
        effect_sentence = (
            "The\nunresolved possibility of Conduct C therefore does not supply "
            "probable or\narguable probable cause for Offense Z because the "
            "required Z2 basis remains\nabsent from the approved arrest-time record."
        )
        causal_first = replace_once(
            fixture["passing_candidate"],
            effect_sentence,
            "Because Z2 is absent from the approved arrest-time record, the "
            "unresolved possibility of Conduct C does not supply probable or "
            "arguable probable cause for Offense Z.",
        )
        result = grade_candidate(fixture, causal_first)
        self.assertTrue(result["passed"])
        self.assertEqual(result["findings"], [])

    def test_present_named_fixtures_have_exact_assets_and_behavior_findings(self):
        observed_directories = {
            path.name
            for path in FIXTURES.glob("complaint-*")
            if path.is_dir()
        }
        self.assertTrue(set(EXPECTED_FIXTURES).issubset(observed_directories))
        for fixture_id, expected in EXPECTED_FIXTURES.items():
            fixture_directory = FIXTURES / fixture_id
            with self.subTest(fixture=fixture_id):
                self.assertTrue(fixture_directory.is_dir())
                self.assertEqual(
                    {path.name for path in fixture_directory.iterdir()},
                    expected["assets"],
                )
                fixture = load_fixture(fixture_directory)
                self.assertEqual(fixture["id"], fixture_id)
                self.assertEqual(fixture["target_skill"], expected["target_skill"])
                self.assertEqual(len(fixture["regressions"]), 1)
                regression = fixture["regressions"][0]
                self.assertEqual(regression["expected_findings"], ["banned-pattern"])
                self.assertEqual(
                    finding_pairs(grade_candidate(fixture, regression["candidate"])),
                    {("banned-pattern", expected["location"])},
                )
                passing_result = grade_candidate(fixture, fixture["passing_candidate"])
                self.assertTrue(passing_result["passed"])
                self.assertEqual(passing_result["findings"], [])

    def test_present_named_fixtures_discriminate_an_unrelated_rule(self):
        for fixture_id, expected in EXPECTED_FIXTURES.items():
            fixture_directory = FIXTURES / fixture_id
            with self.subTest(fixture=fixture_id):
                self.assertTrue((fixture_directory / "fixture.json").is_file())
                fixture = load_fixture(fixture_directory)
                mutated = copy.deepcopy(fixture)
                mutated["deterministic"]["banned_patterns"].append(
                    {
                        "id": "unrelated-rule",
                        "pattern": "UNRELATED COMPLAINT FIXTURE RULE",
                    }
                )
                candidate = (
                    f"{fixture['passing_candidate']}\n"
                    "UNRELATED COMPLAINT FIXTURE RULE\n"
                )
                observed = finding_pairs(grade_candidate(mutated, candidate))
                self.assertEqual(observed, {("banned-pattern", "unrelated-rule")})
                self.assertNotIn(("banned-pattern", expected["location"]), observed)


if __name__ == "__main__":
    unittest.main()
