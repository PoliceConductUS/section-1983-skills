import json
import tempfile
import unittest
from pathlib import Path

from evaluations.fixtures import FixtureValidationError, load_corpus, load_fixture


def write_fixture(directory, manifest_changes=None, source_changes=None):
    directory.mkdir(parents=True)
    (directory / "prompt.md").write_text("Draft a synthetic filing report.\n")
    (directory / "source.md").write_text("Synthetic source text.\n")
    (directory / "passing.md").write_text("# Result\n\n[SRC-1]\n")
    (directory / "regression.md").write_text("Regression output.\n")
    sources = [{"id": "SRC-1", "path": "source.md"}]
    if source_changes:
        sources = source_changes(sources)
    (directory / "sources.json").write_text(json.dumps(sources))
    manifest = {
        "id": "fixture-one",
        "synthetic": True,
        "target_skill": "filing-ci",
        "prompt": "prompt.md",
        "sources": "sources.json",
        "passing_candidate": "passing.md",
        "regressions": [
            {
                "id": "regression-one",
                "candidate": "regression.md",
                "expected_findings": ["citation-missing"],
            }
        ],
        "deterministic": {
            "required_fields": [],
            "ordered_headings": ["Result"],
            "banned_terms": [],
            "banned_patterns": [],
            "required_citations": ["SRC-1"],
        },
        "rubric": [
            {
                "id": "preserves-source-boundary",
                "description": "Uses only the bounded synthetic source.",
            }
        ],
    }
    if manifest_changes:
        manifest_changes(manifest)
    (directory / "fixture.json").write_text(json.dumps(manifest))
    return directory


class FixtureLoaderTest(unittest.TestCase):

    def test_rejects_each_path_that_escapes_the_fixture_directory(self):
        cases = {
            "prompt": lambda manifest: manifest.update({"prompt": "../outside.md"}),
            "source manifest": lambda manifest: manifest.update(
                {"sources": "../outside.json"}
            ),
            "passing candidate": lambda manifest: manifest.update(
                {"passing_candidate": "../outside.md"}
            ),
            "regression candidate": lambda manifest: manifest["regressions"][
                0
            ].update({"candidate": "../outside.md"}),
            "source": None,
        }

        for label, manifest_changes in cases.items():
            with self.subTest(path=label), tempfile.TemporaryDirectory() as root:
                source_changes = None
                if label == "source":
                    source_changes = lambda sources: [
                        {"id": "SRC-1", "path": "../outside.md"}
                    ]
                fixture_directory = write_fixture(
                    Path(root) / "fixture",
                    manifest_changes=manifest_changes,
                    source_changes=source_changes,
                )

                with self.assertRaisesRegex(
                    FixtureValidationError, "fixture directory"
                ):
                    load_fixture(fixture_directory)

    def test_rejects_absolute_path_outside_fixture_directory(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            outside = root_path / "outside.md"
            outside.write_text("Outside fixture.\n")

            def use_absolute_path(manifest):
                manifest["prompt"] = str(outside)

            fixture_directory = write_fixture(
                root_path / "fixture", manifest_changes=use_absolute_path
            )

            with self.assertRaisesRegex(FixtureValidationError, "fixture directory"):
                load_fixture(fixture_directory)

    def test_rejects_in_fixture_symlink_that_resolves_outside_fixture_directory(self):
        with tempfile.TemporaryDirectory() as root:
            root_path = Path(root)
            outside = root_path / "outside.md"
            outside.write_text("Outside fixture.\n")

            def use_symlink(manifest):
                manifest["prompt"] = "linked-prompt.md"

            fixture_directory = write_fixture(
                root_path / "fixture", manifest_changes=use_symlink
            )
            (fixture_directory / "linked-prompt.md").symlink_to(outside)

            with self.assertRaisesRegex(FixtureValidationError, "fixture directory"):
                load_fixture(fixture_directory)

    def test_rejects_fixture_without_explicit_synthetic_true(self):
        for value in (False, None):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as root:
                def change_synthetic(manifest):
                    if value is None:
                        manifest.pop("synthetic")
                    else:
                        manifest["synthetic"] = value

                fixture_directory = write_fixture(
                    Path(root) / "fixture", manifest_changes=change_synthetic
                )

                with self.assertRaisesRegex(FixtureValidationError, "synthetic"):
                    load_fixture(fixture_directory)

    def test_rejects_missing_required_manifest_fields(self):
        required_fields = (
            "id",
            "target_skill",
            "prompt",
            "sources",
            "deterministic",
            "rubric",
            "passing_candidate",
            "regressions",
        )

        for field in required_fields:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as root:
                def remove_field(manifest):
                    manifest.pop(field)

                fixture_directory = write_fixture(
                    Path(root) / "fixture", manifest_changes=remove_field
                )

                with self.assertRaisesRegex(FixtureValidationError, field):
                    load_fixture(fixture_directory)

    def test_rejects_empty_permanent_regression_list(self):
        def remove_permanent_regressions(manifest):
            manifest["regressions"] = []

        with tempfile.TemporaryDirectory() as root:
            fixture_directory = write_fixture(
                Path(root) / "fixture",
                manifest_changes=remove_permanent_regressions,
            )

            with self.assertRaisesRegex(FixtureValidationError, "regression"):
                load_fixture(fixture_directory)

    def test_rejects_duplicate_fixture_identifiers_in_a_corpus(self):
        with tempfile.TemporaryDirectory() as root:
            corpus = Path(root)
            write_fixture(corpus / "one")
            write_fixture(corpus / "two")

            with self.assertRaisesRegex(FixtureValidationError, "fixture-one"):
                load_corpus(corpus)

    def test_rejects_duplicate_identifiers_within_a_fixture(self):
        def duplicate_sources(sources):
            return sources + [dict(sources[0])]

        def duplicate_regressions(manifest):
            manifest["regressions"].append(dict(manifest["regressions"][0]))

        def duplicate_rubric(manifest):
            manifest["rubric"].append(dict(manifest["rubric"][0]))

        cases = {
            "source": (None, duplicate_sources),
            "regression": (duplicate_regressions, None),
            "rubric": (duplicate_rubric, None),
        }

        for label, changes in cases.items():
            with self.subTest(identifier=label), tempfile.TemporaryDirectory() as root:
                fixture_directory = write_fixture(
                    Path(root) / "fixture",
                    manifest_changes=changes[0],
                    source_changes=changes[1],
                )

                with self.assertRaisesRegex(FixtureValidationError, "duplicate"):
                    load_fixture(fixture_directory)

    def test_rejects_contract_citation_not_present_in_source_manifest(self):
        def require_unknown_citation(manifest):
            manifest["deterministic"]["required_citations"] = ["SRC-404"]

        with tempfile.TemporaryDirectory() as root:
            fixture_directory = write_fixture(
                Path(root) / "fixture", manifest_changes=require_unknown_citation
            )

            with self.assertRaisesRegex(FixtureValidationError, "SRC-404"):
                load_fixture(fixture_directory)

    def test_rejects_duplicate_deterministic_rule_identifiers_across_rule_types(self):
        def duplicate_rule_identifier(manifest):
            manifest["deterministic"]["banned_terms"] = [
                {"id": "invented-tool", "term": "invented tool"}
            ]
            manifest["deterministic"]["banned_patterns"] = [
                {"id": "invented-tool", "pattern": "invented.*tool"}
            ]

        with tempfile.TemporaryDirectory() as root:
            fixture_directory = write_fixture(
                Path(root) / "fixture", manifest_changes=duplicate_rule_identifier
            )

            with self.assertRaisesRegex(FixtureValidationError, "invented-tool"):
                load_fixture(fixture_directory)


if __name__ == "__main__":
    unittest.main()
