import json
import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL = REPOSITORY / "skills" / "building-litigation-alignment-overlays"
README = REPOSITORY / "README.md"
ROUTER = REPOSITORY / "skills" / "section-1983-drafting" / "SKILL.md"
GUIDE = REPOSITORY / "OVERLAYS.md"
JUDGE_GUIDE = REPOSITORY / "JUDGE_OVERLAYS.md"
JUDGE_SPEC = REPOSITORY / "openspec" / "specs" / "judge-overlay-authoring" / "spec.md"
SCHEMAS = (
    "docket-snapshot.schema.json",
    "litigation-alignment-overlay.schema.json",
    "filing-overlay-manifest.schema.json",
)
FIXTURES = (
    "complete-snapshot.json",
    "complete-overlay.json",
    "complete-filing-manifest.json",
    "initial-snapshot.json",
    "no-responsive-overlay.json",
)


def text(path):
    if not path.is_file():
        raise AssertionError(f"missing public artifact: {path.relative_to(REPOSITORY)}")
    return path.read_text()


class LitigationAlignmentOverlayStructureTest(unittest.TestCase):
    def test_public_skill_has_exact_install_local_surface(self):
        expected = {
            "SKILL.md",
            "agents/openai.yaml",
            "scripts/validate_overlays.py",
            *(f"references/{name}" for name in SCHEMAS),
            *(f"references/fixtures/{name}" for name in FIXTURES),
        }
        self.assertTrue(SKILL.is_dir())
        actual = {
            path.relative_to(SKILL).as_posix()
            for path in SKILL.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        self.assertEqual(actual, expected)
        skill = text(SKILL / "SKILL.md")
        metadata = text(SKILL / "agents" / "openai.yaml")
        self.assertRegex(
            skill,
            r"(?m)^name:\s*building-litigation-alignment-overlays\s*$",
        )
        self.assertIn("$building-litigation-alignment-overlays", metadata)

    def test_schemas_are_draft_2020_12_and_require_canonical_roots(self):
        required = {
            "docket-snapshot.schema.json": {
                "schema_version",
                "snapshot_id",
                "version",
                "checked_through",
                "actors",
                "sources",
            },
            "litigation-alignment-overlay.schema.json": {
                "schema_version",
                "overlay_id",
                "version",
                "generated_at",
                "source_snapshot",
                "defendants",
                "generated_groups",
                "overrides",
                "effective_groups",
                "ledgers",
                "ledger_fingerprints",
                "issue_matrix",
                "review_plan",
            },
            "filing-overlay-manifest.schema.json": {
                "schema_version",
                "filing_version_id",
                "artifact_id",
                "artifact_sha256",
                "source_snapshot",
                "overlays",
            },
        }
        for filename, fields in required.items():
            with self.subTest(schema=filename):
                schema = json.loads(text(SKILL / "references" / filename))
                self.assertEqual(
                    schema.get("$schema"),
                    "https://json-schema.org/draft/2020-12/schema",
                )
                self.assertIs(schema.get("additionalProperties"), False)
                self.assertEqual(set(schema.get("required", [])), fields)

    def test_readme_and_router_reach_the_skill_and_general_guide(self):
        readme = text(README)
        router = text(ROUTER)
        self.assertIn("`building-litigation-alignment-overlays`", readme)
        self.assertIn("[Manage case overlays](OVERLAYS.md)", readme)
        self.assertIn("building-litigation-alignment-overlays", router)
        self.assertRegex(
            router,
            r"(?is)(?:amended complaint|leave to amend).{0,500}(?:docket|overlay)",
        )

    def test_general_guide_owns_the_complete_lifecycle(self):
        guide = text(GUIDE)
        for heading in (
            "Overlay inventory",
            "Creation prerequisites",
            "Create, reuse, refresh, rebuild, or supersede",
            "Event-driven invalidation",
            "User overrides and precedence",
            "Review routing",
            "Filing-version manifest",
            "Synthetic end-to-end lifecycle",
        ):
            with self.subTest(heading=heading):
                self.assertRegex(guide, rf"(?m)^##\s+{re.escape(heading)}\s*$")
        for phrase in (
            "litigation-alignment groups",
            "adversary attack",
            "plaintiff response",
            "judicial treatment",
            "checked-through",
            "validator result",
            "source snapshot",
            "immutable",
            "supersede",
            "no specialized drafting change",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), guide.casefold())

    def test_general_guide_has_complete_synthetic_lifecycle_and_role_separation(self):
        guide = text(GUIDE)
        lifecycle = re.search(
            r"(?ms)^## Synthetic end-to-end lifecycle\s*$([\s\S]*?)(?=^## |\Z)",
            guide,
        )
        self.assertIsNotNone(lifecycle)
        section = lifecycle.group(1).casefold()
        for stage in (
            "initial complaint",
            "responsive motion",
            "amended complaint",
            "magistrate",
            "district",
        ):
            self.assertIn(stage, section)
        self.assertRegex(
            guide,
            r"(?is)adversary.{0,120}(?:only|separate).{0,220}plaintiff.{0,220}judicial",
        )
        self.assertRegex(
            guide,
            r"(?is)silence.{0,120}(?:must not|never).{0,160}(?:agreement|withdrawal|adoption|rejection)",
        )

    def test_judge_guide_links_to_general_lifecycle_and_owns_judge_triggers(self):
        judge = text(JUDGE_GUIDE)
        self.assertRegex(judge, r"(?m)^#\s+Judicial Reasoning Profile\s*$")
        self.assertRegex(
            judge,
            r"(?is)judicial reasoning profile.{0,500}"
            r"(?:issue|procedural posture).{0,300}(?:authorship|evidence strength)",
        )
        normalized_judge = " ".join(judge.casefold().split())
        self.assertIn("court-specific filing rules", normalized_judge)
        self.assertIn("separate compliance component", normalized_judge)
        self.assertIn("[Manage case overlays](OVERLAYS.md)", judge)
        for phrase in (
            "assignment",
            "reassignment",
            "official procedure",
            "standing order",
            "validated corpus",
            "checked date",
            "new immutable version",
        ):
            self.assertIn(phrase.casefold(), judge.casefold())
        self.assertRegex(
            judge.casefold(),
            r"do not manipulate(?: or predict)? judicial assignment",
        )

    def test_judge_overlay_is_a_judicial_reasoning_profile(self):
        judge = text(JUDGE_GUIDE)
        self.assertRegex(judge, r"(?m)^##\s+Judicial reasoning dimensions\s*$")
        for phrase in (
            "substantive doctrine",
            "procedural doctrine",
            "reasoning patterns",
            "authority hierarchy",
            "factual methodology",
            "error sensitivities",
            "analytical presentation patterns",
            "published opinions",
            "prior orders",
            "articles",
            "speeches",
            "books",
            "standing orders",
            "courtroom procedures",
            "apply the judge's own verified reasoning consistently",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), judge.casefold())
        self.assertRegex(
            judge,
            r"(?is)(?:articles|speeches|books).{0,300}"
            r"(?:not governing authority|(?:do|does) not become governing authority)",
        )
        self.assertRegex(
            judge,
            r"(?is)(?:writing|presentation).{0,250}"
            r"(?:without|do not|must not|never).{0,100}(?:imitate|mimic)",
        )

    def test_durable_judge_spec_has_concrete_lifecycle_purpose(self):
        specification = text(JUDGE_SPEC)
        purpose = re.search(
            r"(?ms)^## Purpose\s*$([\s\S]*?)(?=^## |\Z)", specification
        )
        self.assertIsNotNone(purpose)
        self.assertNotIn("TBD", purpose.group(1))
        self.assertIn("judge overlay", purpose.group(1).casefold())
        self.assertRegex(
            purpose.group(1), r"(?is)judicial\s+reasoning\s+profile"
        )
        self.assertIn("lifecycle", specification.casefold())

    def test_public_skill_keeps_counsel_research_and_filing_edits_out_of_scope(self):
        skill = text(SKILL / "SKILL.md")
        self.assertRegex(
            skill,
            r"(?is)(?:must|does|do)\s+not.{0,120}(?:research|profile).{0,80}(?:attorney|counsel)",
        )
        self.assertRegex(
            skill,
            r"(?is)(?:must|does|do)\s+not.{0,100}(?:edit|revise|modify).{0,80}(?:filing|artifact)",
        )


if __name__ == "__main__":
    unittest.main()
