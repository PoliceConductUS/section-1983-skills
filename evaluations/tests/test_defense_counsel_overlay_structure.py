import json
import re
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL = REPOSITORY / "skills" / "building-defense-counsel-overlays"
README = REPOSITORY / "README.md"
ROUTER = REPOSITORY / "skills" / "section-1983-drafting" / "SKILL.md"
GENERAL_GUIDE = REPOSITORY / "OVERLAYS.md"
COUNSEL_GUIDE = REPOSITORY / "COUNSEL_OVERLAYS.md"
GOVERNANCE = REPOSITORY / "governance" / "rules-provenance.json"
ALIGNMENT_SCHEMA = (
    REPOSITORY
    / "skills"
    / "building-litigation-alignment-overlays"
    / "references"
    / "filing-overlay-manifest.schema.json"
)
SCHEMAS = (
    "counsel-research-snapshot.schema.json",
    "defense-counsel-overlay.schema.json",
)
FIXTURES = (
    "complete-research-snapshot.json",
    "complete-counsel-overlay.json",
    "incomplete-research-snapshot.json",
    "bounded-example-overlay.json",
)


def text(path):
    if not path.is_file():
        raise AssertionError(f"missing public artifact: {path.relative_to(REPOSITORY)}")
    return path.read_text()


class DefenseCounselOverlayStructureTest(unittest.TestCase):
    def test_public_skill_has_exact_install_local_surface(self):
        expected = {
            "SKILL.md",
            "agents/openai.yaml",
            "scripts/validate_counsel_overlays.py",
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
        self.assertRegex(skill, r"(?m)^name:\s*building-defense-counsel-overlays\s*$")
        self.assertIn("$building-defense-counsel-overlays", metadata)

    def test_schemas_are_draft_2020_12_and_require_canonical_roots(self):
        required = {
            "counsel-research-snapshot.schema.json": {
                "schema_version",
                "snapshot_id",
                "version",
                "checked_through",
                "research_protocol",
                "attorneys",
                "matters",
                "sources",
                "gaps",
            },
            "defense-counsel-overlay.schema.json": {
                "schema_version",
                "overlay_id",
                "version",
                "generated_at",
                "source_snapshot",
                "identity_records",
                "team_records",
                "historical_arguments",
                "judicial_treatments",
                "current_attack_links",
                "patterns",
                "forecasts",
                "overrides",
                "gaps",
                "ledger_fingerprints",
                "review_slices",
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

    def test_overlay_schema_publishes_every_nested_record_contract(self):
        schema = json.loads(
            text(SKILL / "references" / "defense-counsel-overlay.schema.json")
        )
        expected = {
            "identity_records": "identityRecord",
            "team_records": "teamRecord",
            "historical_arguments": "historicalArgument",
            "judicial_treatments": "judicialTreatment",
            "current_attack_links": "currentAttackLink",
            "patterns": "pattern",
            "forecasts": "forecast",
            "overrides": "override",
            "gaps": "overlayGap",
            "review_slices": "reviewSlice",
        }
        for property_name, definition_name in expected.items():
            with self.subTest(property=property_name):
                self.assertEqual(
                    schema["properties"][property_name]["items"],
                    {"$ref": f"#/$defs/{definition_name}"},
                )
                definition = schema["$defs"][definition_name]
                self.assertIs(definition.get("additionalProperties"), False)
                self.assertEqual(
                    set(definition.get("required", [])),
                    set(definition.get("properties", {})),
                )

    def test_readme_router_governance_and_general_guide_route_the_skill(self):
        readme = text(README)
        router = text(ROUTER)
        general = text(GENERAL_GUIDE)
        registry = json.loads(text(GOVERNANCE))
        self.assertIn("`building-defense-counsel-overlays`", readme)
        self.assertIn("[Build defense-counsel overlays](COUNSEL_OVERLAYS.md)", readme)
        self.assertIn("building-defense-counsel-overlays", router)
        self.assertIn("[Defense-counsel overlay guide](COUNSEL_OVERLAYS.md)", general)
        governed = {entry["name"]: entry for entry in registry["skills"]}
        entry = governed["building-defense-counsel-overlays"]
        self.assertEqual(entry["rules_mode"], "runtime-sourced")
        self.assertEqual(
            set(entry["output_provenance"]), {"source_identity", "checked_date"}
        )

    def test_counsel_guide_owns_sources_attribution_lifecycle_and_calibration(self):
        guide = text(COUNSEL_GUIDE)
        normalized = " ".join(guide.casefold().split())
        for heading in (
            "Professional scope",
            "Source hierarchy and research record",
            "Identity, attribution, and counsel teams",
            "Historical arguments and judicial treatment",
            "Patterns and calibrated forecasts",
            "Review and filing composition",
            "Create, reuse, refresh, rebuild, and supersede",
            "Synthetic substitution and realignment lifecycle",
        ):
            with self.subTest(heading=heading):
                self.assertRegex(guide, rf"(?m)^##\s+{re.escape(heading)}\s*$")
        for phrase in (
            "signer",
            "named author",
            "oral advocate",
            "appearance counsel",
            "listed counsel",
            "jointly filed",
            "counsel team",
            "litigation-alignment group",
            "denominator",
            "missingness",
            "supporting examples",
            "contrary examples",
            "checked-through",
            "calibrated confidence",
            "paid PACER",
            "separate explicit authorization",
            "new immutable version",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.casefold(), normalized)

    def test_counsel_guide_keeps_four_layers_and_three_profiles_separate(self):
        guide = text(COUNSEL_GUIDE)
        normalized = " ".join(guide.split())
        for phrase in (
            "historical counsel arguments",
            "judicial treatment",
            "current-case attacks",
            "forecasted next moves",
            "Judicial Reasoning Profile",
            "controlling law",
            "defense-counsel profile",
        ):
            self.assertIn(phrase.casefold(), normalized.casefold())
        self.assertRegex(
            normalized,
            r"(?is)joint(?:ly)? filed.{0,260}(?:team|individual).{0,260}"
            r"(?:direct|supported|source)",
        )
        self.assertRegex(
            normalized,
            r"(?is)court.{0,180}(?:treatment|rejection|adoption).{0,220}"
            r"(?:not|never|separate).{0,100}counsel",
        )

    def test_professional_boundary_rejects_personal_and_certain_predictions(self):
        guide = text(COUNSEL_GUIDE)
        for phrase in (
            "family",
            "politics",
            "private life",
            "protected traits",
            "personality",
            "irrelevant social media",
            "case-outcome prediction",
            "judicial behavior prediction",
        ):
            self.assertIn(phrase.casefold(), guide.casefold())
        self.assertRegex(
            guide,
            r"(?is)(?:must not|never|does not).{0,120}(?:will|certainty|certain)",
        )
        self.assertRegex(
            guide,
            r"(?is)(?:waiver|estoppel|concession).{0,220}"
            r"(?:separate|verified).{0,100}legal analysis",
        )

    def test_manifest_supports_distinct_identity_and_team_pins(self):
        schema = json.loads(text(ALIGNMENT_SCHEMA))
        kinds = set(schema["$defs"]["overlayPin"]["properties"]["kind"]["enum"])
        self.assertEqual(
            kinds,
            {"litigation-alignment", "judge", "counsel-identity", "counsel-team"},
        )

    def test_skill_preserves_blind_review_and_non_mutation_boundaries(self):
        skill = text(SKILL / "SKILL.md")
        self.assertRegex(
            skill,
            r"(?is)blind.{0,160}(?:no|must not|never).{0,120}counsel",
        )
        self.assertRegex(
            skill,
            r"(?is)forecast.{0,200}(?:must not|never|does not).{0,120}"
            r"(?:suppress|replace|remove|displace).{0,100}common",
        )
        self.assertRegex(
            skill,
            r"(?is)(?:must|does|do)\s+not.{0,100}"
            r"(?:edit|revise|modify).{0,80}(?:filing|artifact)",
        )


if __name__ == "__main__":
    unittest.main()
