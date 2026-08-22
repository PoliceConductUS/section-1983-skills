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
        r"(?:may|must|accurat)",
        r"(?:source|record|evidence)",
        r"(?:limitation|unresolved|uncertain)",
    )
    assert_clause_contains(
        test,
        text,
        r"supported",
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
        r"(?:material )?chronology",
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
        r"material to (?:an |the )?offense element",
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
        r"supported",
        r"probable cause",
        r"arguable probable cause",
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


class ComplaintCandorContractTest(unittest.TestCase):
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

    def test_present_named_fixtures_have_exact_assets_and_behavior_findings(self):
        observed_directories = {
            path.name
            for path in FIXTURES.glob("complaint-*")
            if path.is_dir()
        }
        self.assertEqual(observed_directories, set(EXPECTED_FIXTURES))
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
