import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL_DIRECTORY = REPOSITORY / "skills" / "adversarial-filing-review"
SKILL = SKILL_DIRECTORY / "SKILL.md"
METADATA = SKILL_DIRECTORY / "agents" / "openai.yaml"
CHECKLIST = SKILL_DIRECTORY / "references" / "document-attack-checklists.md"
README = REPOSITORY / "README.md"

FAMILIES = (
    "complaint or amended complaint",
    "motion-to-dismiss response",
    "summary-judgment response",
    "leave to amend",
    "extension motion",
    "R&R objection",
    "R&R response",
)

CATEGORIES = (
    "Fatal Defects",
    "Credible Opposition Arguments",
    "Factual Disputes",
    "Discovery Issues",
    "Style Complaints",
)


def required_text(path):
    if not path.is_file():
        raise AssertionError(f"required public file is missing: {path.relative_to(REPOSITORY)}")
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


class AdversarialReviewStructureTest(unittest.TestCase):

    def test_public_skill_metadata_and_readme_route_exist(self):
        skill = required_text(SKILL)
        metadata = required_text(METADATA)
        readme = required_text(README)

        self.assertRegex(skill, r"(?m)^name:\s*adversarial-filing-review\s*$")
        self.assertRegex(skill, r"(?m)^description:\s*(?:>|>-|\S)")
        assert_phrases(
            self,
            metadata,
            (
                "interface:",
                "display_name:",
                "short_description:",
                "default_prompt:",
                "$adversarial-filing-review",
            ),
        )
        self.assertIn("`adversarial-filing-review`", readme)
        self.assertRegex(
            readme,
            r"(?is)adversarial-filing-review.{0,500}(independent|fresh|clean-room)",
        )

    def test_one_public_checklist_reference_has_universal_and_exact_families(self):
        skill = required_text(SKILL)
        checklist = required_text(CHECKLIST)

        self.assertIn("references/document-attack-checklists.md", skill)
        self.assertRegex(checklist.casefold(), r"universal.{0,40}(attack|checklist)")
        assert_phrases(self, checklist, FAMILIES)

    def test_skill_states_clean_room_inputs_and_exclusions(self):
        skill = required_text(SKILL)

        assert_semantics(
            self,
            skill,
            (
                ("bounded draft", (r"(?:canonical|immutable|controlling)\s+draft",)),
                ("draft version", (r"draft.{0,40}version", r"version.{0,40}draft")),
                ("fingerprints", (r"fingerprint", r"sha-?256", r"content\s+hash")),
                ("approved sources", (r"approved\s+source", r"source\s+allowlist",)),
                ("stable source identifiers", (r"stable.{0,30}identif", r"source\s+id",)),
                ("embedded content", (r"(?:immutable|embedded|source)\s+content",)),
                ("drafting history", (r"drafting\s+histor",)),
                ("redlines", (r"redline",)),
                ("strategy or control conclusions", (r"(?:strategy|control).{0,40}(?:conclusion|memo|decision)",)),
                ("prior reviews", (r"prior\s+review",)),
                ("checker output", (r"checker\s+(?:output|result)",)),
                ("conversation state", (r"conversation",)),
                ("session state", (r"session",)),
                ("empty capabilities", (r"(?:empty|no)\s+(?:reviewer\s+)?capabilit",)),
                ("filesystem access", (r"file\s*system", r"filesystem")),
                ("repository access", (r"repository",)),
                ("browser access", (r"browser",)),
                ("fail closed", (r"independent review unavailable",)),
            ),
        )

    def test_skill_prohibits_paths_and_urls_in_the_reviewer_packet(self):
        skill = required_text(SKILL)

        self.assertRegex(
            skill,
            r"(?is)(?:paths?.{0,30}urls?|urls?.{0,30}paths?).{0,80}must\s+not\s+appear.{0,80}(?:reviewer\s+)?packet",
        )

    def test_skill_does_not_allow_provenance_only_paths_or_urls(self):
        skill = required_text(SKILL)

        self.assertNotRegex(
            skill,
            r"(?is)(?:provenance[- ]only|only\s+as\s+provenance|provenance\s+metadata\s+only)",
        )

    def test_skill_requires_five_categories_corrections_and_plaintiff_gate(self):
        skill = required_text(SKILL)

        assert_phrases(self, skill, CATEGORIES)
        assert_phrases(
            self,
            skill,
            (
                "None found",
                "Replace:",
                "With:",
                "PLAINTIFF DECISION REQUIRED",
            ),
        )
        assert_semantics(
            self,
            skill,
            (
                ("reserved choices", (r"retain.{0,120}narrow.{0,120}omit",)),
                ("choice consequences", (r"choice.{0,100}consequence", r"consequence.{0,100}choice")),
            ),
        )

    def test_skill_preserves_read_only_workflow_boundaries(self):
        skill = required_text(SKILL)

        assert_phrases(
            self,
            skill,
            (
                "read-only",
            ),
        )
        assert_semantics(
            self,
            skill,
            (
                ("authority certification boundary", (r"(?:must|does|shall)\s+not.{0,140}(?:certif|verify).{0,140}(?:authority|binding|quotation)",)),
                ("readiness or outcome boundary", (r"(?:must|does|shall)\s+not.{0,140}(?:filing readiness|filing-ready|outcome)",)),
                ("RRD boundary", (r"(?:must|does|shall)\s+not.{0,100}(?:create|run|produce).{0,40}RRD",)),
                ("Filing CI boundary", (r"(?:must|does|shall)\s+not.{0,100}(?:run|interpret|replace).{0,40}Filing CI",)),
                ("editing boundary", (r"(?:must|does|shall)\s+not.{0,100}(?:edit|revise|change).{0,40}(?:filing|draft)",)),
                ("separate drafting", (r"separate.{0,60}drafting\s+workflow", r"drafting\s+workflow.{0,60}separate",)),
                ("gates rerun", (r"(?:rerun|run again).{0,100}(?:review|Filing CI|gate)",)),
            ),
        )

    def test_public_route_uses_the_folder_processor_and_host_publication(self):
        skill = required_text(SKILL)
        readme = required_text(README)

        for artifact in (skill, readme):
            with self.subTest(artifact=artifact[:20]):
                assert_semantics(
                    self,
                    artifact,
                    (
                        ("filing role", (r"declared.{0,80}filing.{0,40}(?:role|root)",)),
                        (
                            "approved sources role",
                            (r"declared.{0,80}approved-sources.{0,40}(?:role|root)",),
                        ),
                        ("required target", (r"required.{0,80}filing target",)),
                        ("authorized internet", (r"internet.{0,40}authorized",)),
                        (
                            "host publication",
                            (r"(?:trusted host|outputrun).{0,120}(?:publish|write)",),
                        ),
                        (
                            "returned bytes",
                            (r"(?:return|emit).{0,100}(?:report bytes|artifact bytes)",),
                        ),
                    ),
                )
                self.assertNotRegex(
                    artifact,
                    r"(?is)(?:--project-boundary|--version-folder|--artifact\b|"
                    r"--reviewer-command-json|<version-folder>/audits/)",
                )


if __name__ == "__main__":
    unittest.main()
