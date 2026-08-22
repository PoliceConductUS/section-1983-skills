import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL_NAME = "drafting-section-1983-declarations-and-evidence"
SKILL_DIRECTORY = REPOSITORY / "skills" / SKILL_NAME
SKILL = SKILL_DIRECTORY / "SKILL.md"
METADATA = SKILL_DIRECTORY / "agents" / "openai.yaml"
README = REPOSITORY / "README.md"
ROUTER = REPOSITORY / "skills" / "section-1983-drafting" / "SKILL.md"
SUMMARY_JUDGMENT = (
    REPOSITORY
    / "skills"
    / "section-1983-drafting"
    / "references"
    / "documents"
    / "msj-response.md"
)

DOMESTIC_FORM = (
    "I declare under penalty of perjury that the foregoing is true and correct. "
    "Executed on (date)."
)
FOREIGN_FORM = (
    "I declare under penalty of perjury under the laws of the United States of "
    "America that the foregoing is true and correct. Executed on (date)."
)

CLASSIFICATIONS = (
    "firsthand fact",
    "attributed record fact",
    "derived analysis",
    "inference",
    "legal conclusion",
    "discovery expectation",
)

OUTPUTS = (
    "statement classification ledger",
    "unsigned draft declaration",
    "exhibit foundation map",
    "excluded or separate material",
    "approval and execution status",
)


def required_text(path):
    if not path.is_file():
        raise AssertionError(
            f"required public file is missing: {path.relative_to(REPOSITORY)}"
        )
    return path.read_text()


def assert_phrases(test, text, phrases):
    folded = text.casefold()
    for phrase in phrases:
        with test.subTest(phrase=phrase):
            test.assertIn(phrase.casefold(), folded)


def assert_semantics(test, text, concepts):
    for label, patterns in concepts:
        with test.subTest(concept=label):
            alternatives = "|".join(f"(?:{pattern})" for pattern in patterns)
            test.assertRegex(text, rf"(?is){alternatives}")


def collapsed_whitespace(text):
    return " ".join(text.split())


class DeclarationEvidenceSkillStructureTest(unittest.TestCase):

    def test_public_skill_package_has_valid_entrypoint(self):
        skill = required_text(SKILL)

        self.assertRegex(skill, rf"(?m)^name:\s*{re.escape(SKILL_NAME)}\s*$")
        self.assertRegex(skill, r"(?m)^description:\s*(?:>|>-|\S)")
        assert_phrases(self, skill, ("declaration", "evidence", "summary judgment"))

    def test_public_skill_has_openai_discovery_metadata(self):
        metadata = required_text(METADATA)

        assert_phrases(
            self,
            metadata,
            (
                "interface:",
                "display_name:",
                "short_description:",
                "default_prompt:",
                f"${SKILL_NAME}",
            ),
        )

    def test_readme_umbrella_and_summary_judgment_reference_route_the_skill(self):
        routes = {
            "README": required_text(README),
            "section-1983-drafting": required_text(ROUTER),
            "summary-judgment response": required_text(SUMMARY_JUDGMENT),
        }

        for label, text in routes.items():
            with self.subTest(route=label):
                self.assertIn(f"`{SKILL_NAME}`", text)

    def test_skill_requires_the_complete_applicable_section_1746_form(self):
        skill = required_text(SKILL)
        collapsed = collapsed_whitespace(skill)

        self.assertIn(DOMESTIC_FORM, collapsed)
        self.assertIn(FOREIGN_FORM, collapsed)
        assert_semantics(
            self,
            skill,
            (
                (
                    "actual execution location selects the form",
                    (
                        r"actual.{0,30}(?:place|location).{0,100}execution.{0,100}(?:select|form)",
                        r"(?:select|form).{0,100}actual.{0,30}(?:place|location).{0,100}execution",
                    ),
                ),
                (
                    "residence venue and incarceration do not select the form",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}(?:infer|select).{0,100}residence.{0,80}venue.{0,80}(?:incarceration|custody)",
                    ),
                ),
                (
                    "missing location blocks form selection",
                    (
                        r"(?:missing|unknown|no).{0,60}(?:execution\s+)?(?:place|location).{0,160}(?:block.{0,50}(?:form\s+)?selection|(?:do|does|must|shall)\s+not.{0,80}(?:select|choose).{0,50}(?:form|language))",
                        r"(?:block.{0,50}(?:form\s+)?selection|(?:do|does|must|shall)\s+not.{0,80}(?:select|choose).{0,50}(?:form|language)).{0,160}(?:missing|unknown|no).{0,60}(?:execution\s+)?(?:place|location)",
                    ),
                ),
                (
                    "missing location prohibits combining the forms",
                    (
                        r"(?:missing|unknown|no).{0,60}(?:execution\s+)?(?:place|location).{0,180}(?:do|does|must|shall)\s+not.{0,80}(?:combine|merge|mix).{0,50}(?:form|language)",
                        r"(?:do|does|must|shall)\s+not.{0,80}(?:combine|merge|mix).{0,50}(?:form|language).{0,180}(?:missing|unknown|no).{0,60}(?:execution\s+)?(?:place|location)",
                    ),
                ),
                (
                    "human date and signature remain blank",
                    (
                        r"(?:date.{0,40}signature|signature.{0,40}date).{0,100}(?:blank|human\s+declarant)",
                        r"(?:blank|human\s+declarant).{0,100}(?:date.{0,40}signature|signature.{0,40}date)",
                    ),
                ),
            ),
        )

    def test_skill_requires_identity_and_statement_specific_knowledge_and_competency(self):
        skill = required_text(SKILL)

        assert_semantics(
            self,
            skill,
            (
                (
                    "declarant identity",
                    (
                        r"(?:require|record|identify|state).{0,80}declarant.{0,30}(?:identity|name)",
                        r"declarant.{0,30}(?:identity|name).{0,80}(?:require|record|identify|state)",
                    ),
                ),
                (
                    "one material proposition per numbered paragraph",
                    (
                        r"one\s+material\s+proposition.{0,80}(?:numbered\s+)?paragraph",
                        r"(?:numbered\s+)?paragraph.{0,80}one\s+material\s+proposition",
                    ),
                ),
                (
                    "statement-specific personal-knowledge basis",
                    (
                        r"statement.specific.{0,100}(?:personal\s+knowledge|perception|perceived)",
                        r"(?:personal\s+knowledge|perception|perceived).{0,100}statement.specific",
                    ),
                ),
                (
                    "statement-specific competency basis",
                    (
                        r"statement.specific.{0,100}competen",
                        r"competen.{0,100}statement.specific",
                    ),
                ),
                (
                    "generic recital cannot replace the bases",
                    (
                        r"generic.{0,40}recital.{0,120}(?:must\s+not|does\s+not|cannot).{0,100}(?:basis|knowledge|competen)",
                        r"(?:must\s+not|does\s+not|cannot).{0,100}generic.{0,40}recital",
                    ),
                ),
            ),
        )

    def test_skill_classifies_every_statement_and_excludes_laundered_material(self):
        skill = required_text(SKILL)

        assert_phrases(
            self,
            skill,
            CLASSIFICATIONS
            + (
                "stable statement ID",
                "exact proposed text",
                "declarant knowledge basis",
                "competency basis",
                "approved source IDs",
                "exhibit IDs",
                "disposition",
                "gap",
                "human declarant approval status",
                "Excluded or Separate Material",
            ),
        )
        assert_semantics(
            self,
            skill,
            (
                (
                    "record review does not become firsthand knowledge",
                    (
                        r"(?:read|review).{0,50}record.{0,140}(?:must\s+not|does\s+not|cannot).{0,100}(?:firsthand|personal\s+knowledge)",
                        r"(?:firsthand|personal\s+knowledge).{0,100}(?:must\s+not|does\s+not|cannot).{0,140}(?:read|review).{0,50}record",
                    ),
                ),
                (
                    "attributed record content remains attributed",
                    (
                        r"attributed\s+record.{0,120}(?:remain|stay).{0,40}attribut",
                        r"(?:remain|stay).{0,40}attribut.{0,120}attributed\s+record",
                    ),
                ),
            ),
        )
        for label, term in (
            ("derived analysis", r"derived\s+analysis"),
            ("inference", r"inferences?"),
            ("legal conclusion", r"legal\s+conclusions?"),
            ("discovery expectation", r"discovery\s+expectations?"),
        ):
            assert_semantics(
                self,
                skill,
                (
                    (
                        f"{label} goes to excluded or separate material",
                        (
                            rf"{term}.{{0,180}}Excluded or Separate Material",
                            rf"Excluded or Separate Material.{{0,180}}{term}",
                        ),
                    ),
                    (
                        f"{label} is never a retained declaration paragraph",
                        (
                            rf"{term}.{{0,180}}(?:must\s+not|does\s+not|do\s+not|never).{{0,100}}(?:retained\s+)?declaration\s+paragraph",
                            rf"(?:retained\s+)?declaration\s+paragraph.{{0,100}}(?:must\s+not|does\s+not|do\s+not|never).{{0,180}}{term}",
                        ),
                    ),
                ),
            )

    def test_skill_reports_discovery_expectations_as_gaps_not_personal_knowledge(self):
        skill = required_text(SKILL)

        assert_semantics(
            self,
            skill,
            (
                (
                    "expected requested missing or unproduced discovery is a gap",
                    (
                        r"expected.{0,50}requested.{0,50}missing.{0,50}unproduced.{0,120}(?:gap|unknown)",
                        r"(?:gap|unknown).{0,120}expected.{0,50}requested.{0,50}missing.{0,50}unproduced",
                    ),
                ),
                (
                    "expected source content is not predicted",
                    (
                        r"(?:must\s+not|does\s+not|cannot).{0,120}(?:recording|witness|record|source).{0,100}(?:show|prove|confirm)",
                        r"(?:show|prove|confirm).{0,100}(?:must\s+not|does\s+not|cannot).{0,120}(?:expected|discovery)",
                    ),
                ),
            ),
        )

    def test_skill_prompts_for_source_bounded_exhibit_foundation(self):
        skill = required_text(SKILL)

        assert_phrases(
            self,
            skill,
            (
                "exhibit ID",
                "description",
                "statement ID",
                "recognizes",
                "creation",
                "receipt",
                "observation",
                "custody",
                "maintenance",
                "accuracy",
                "completeness",
                "missing foundation",
            ),
        )
        assert_semantics(
            self,
            skill,
            (
                (
                    "missing foundation produces focused prompts",
                    (
                        r"missing\s+foundation.{0,120}(?:focused\s+)?(?:prompt|question)",
                        r"(?:focused\s+)?(?:prompt|question).{0,120}missing\s+foundation",
                    ),
                ),
                (
                    "foundation facts are not invented",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}invent.{0,100}(?:custodian|relationship|creation|chain|accuracy|authentication)",
                    ),
                ),
                (
                    "no exhibit authentication or admissibility declaration",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}(?:declare|certify|call).{0,80}(?:authenticated|authentic|admissible)",
                    ),
                ),
            ),
        )

    def test_skill_requires_exact_human_approval_before_execution(self):
        skill = required_text(SKILL)

        assert_phrases(self, skill, ("approve", "revise", "omit", "pending"))
        self.assertNotRegex(
            skill,
            r"(?is)human\s+declarant\s+approval\s+status.{0,100}\brevised\b",
        )
        assert_semantics(
            self,
            skill,
            (
                (
                    "the human declarant is the approver",
                    (
                        r"human\s+declarant.{0,100}(?:approve|revise|omit)",
                        r"(?:approve|revise|omit).{0,100}human\s+declarant",
                    ),
                ),
                (
                    "retained exact text begins pending",
                    (
                        r"(?:every|each).{0,40}retained.{0,50}(?:statement|paragraph).{0,100}(?:begin|start).{0,30}pending",
                        r"pending.{0,100}(?:every|each).{0,40}retained.{0,50}(?:statement|paragraph)",
                    ),
                ),
                (
                    "silence is not approval",
                    (r"silence.{0,50}(?:not|does\s+not|must\s+not).{0,40}approval",),
                ),
                (
                    "changed text returns to pending",
                    (
                        r"(?:changed|revised|edited).{0,60}(?:statement|paragraph|text).{0,100}(?:return|reset).{0,30}pending",
                        r"(?:return|reset).{0,30}pending.{0,100}(?:changed|revised|edited).{0,60}(?:statement|paragraph|text)",
                    ),
                ),
                (
                    "execution blocked until every retained statement is approved",
                    (
                        r"(?:execution|ready).{0,80}block.{0,120}(?:every|each).{0,60}retained.{0,60}(?:explicit|approv)",
                        r"(?:every|each).{0,60}retained.{0,60}(?:explicit|approv).{0,120}(?:execution|ready).{0,80}block",
                    ),
                ),
                (
                    "agent cannot sign date execute or file",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}sign.{0,50}date.{0,50}execute.{0,50}file",
                    ),
                ),
            ),
        )

    def test_skill_returns_bounded_outputs_without_certification(self):
        skill = required_text(SKILL)

        assert_phrases(self, skill, OUTPUTS)
        assert_semantics(
            self,
            skill,
            (
                (
                    "no truth authentication or admissibility certification",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}certif.{0,80}truth.{0,80}authentication.{0,80}admissibility",
                        r"(?:must|does|shall)\s+not.{0,100}(?:truth|authentication|admissibility).{0,100}certif",
                    ),
                ),
                (
                    "no execution filing or readiness certification",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}(?:certif|claim).{0,80}execution.{0,80}filing.{0,80}(?:filing\s+readiness|filing-ready)",
                        r"(?:must|does|shall)\s+not.{0,100}(?:execution|filing|filing\s+readiness|filing-ready).{0,100}(?:certif|claim)",
                    ),
                ),
            ),
        )


if __name__ == "__main__":
    unittest.main()
