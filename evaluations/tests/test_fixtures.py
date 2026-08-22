import json
import tempfile
import unittest
from pathlib import Path

from evaluations.fixtures import FixtureValidationError, load_corpus, load_fixture


def write_fixture(directory, manifest_changes=None, source_changes=None):
    directory.mkdir(parents=True)
    (directory / "prompt.md").write_text("Draft a synthetic filing report.\n")
    (directory / "source.md").write_text("Synthetic source text.\n")
    (directory / "passing.md").write_text("# Result\n\n[cite:SRC-1]\n")
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

    def test_rejects_malformed_deterministic_contract_values(self):
        cases = (
            ("required-fields-not-list", "required_fields", "analysis.result"),
            ("required-field-not-string", "required_fields", [7]),
            ("required-field-empty", "required_fields", [""]),
            ("headings-not-list", "ordered_headings", "Result"),
            ("heading-not-string", "ordered_headings", [7]),
            ("heading-empty", "ordered_headings", [""]),
            ("citations-not-list", "required_citations", "SRC-1"),
            ("citation-not-string", "required_citations", [7]),
            ("citation-empty", "required_citations", [""]),
            ("terms-not-list", "banned_terms", {}),
            ("patterns-not-list", "banned_patterns", {}),
        )

        for label, field, value in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as root:
                def change_contract(manifest):
                    manifest["deterministic"][field] = value

                fixture_directory = write_fixture(
                    Path(root) / "fixture", manifest_changes=change_contract
                )

                with self.assertRaises(FixtureValidationError):
                    load_fixture(fixture_directory)

    def test_rejects_malformed_banned_rules_and_invalid_regular_expression(self):
        cases = (
            ("term-missing-id", "banned_terms", [{"term": "merely"}]),
            ("term-empty-id", "banned_terms", [{"id": "", "term": "merely"}]),
            ("term-missing-value", "banned_terms", [{"id": "merely"}]),
            ("term-non-string", "banned_terms", [{"id": "merely", "term": 7}]),
            ("term-empty", "banned_terms", [{"id": "merely", "term": ""}]),
            ("pattern-missing-id", "banned_patterns", [{"pattern": "merely"}]),
            (
                "pattern-empty-id",
                "banned_patterns",
                [{"id": "", "pattern": "merely"}],
            ),
            ("pattern-missing-value", "banned_patterns", [{"id": "merely"}]),
            (
                "pattern-non-string",
                "banned_patterns",
                [{"id": "merely", "pattern": 7}],
            ),
            (
                "pattern-empty",
                "banned_patterns",
                [{"id": "merely", "pattern": ""}],
            ),
            (
                "pattern-invalid-regex",
                "banned_patterns",
                [{"id": "invalid", "pattern": "["}],
            ),
        )

        for label, field, rules in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as root:
                def change_rules(manifest):
                    manifest["deterministic"][field] = rules

                fixture_directory = write_fixture(
                    Path(root) / "fixture", manifest_changes=change_rules
                )

                with self.assertRaises(FixtureValidationError):
                    load_fixture(fixture_directory)

    def test_rejects_malformed_rubric_criteria(self):
        cases = (
            [{"description": "Uses bounded sources."}],
            [{"id": "", "description": "Uses bounded sources."}],
            [{"id": 7, "description": "Uses bounded sources."}],
            [{"id": "source-boundary"}],
            [{"id": "source-boundary", "description": ""}],
            [{"id": "source-boundary", "description": 7}],
        )

        for rubric in cases:
            with self.subTest(rubric=rubric), tempfile.TemporaryDirectory() as root:
                def change_rubric(manifest):
                    manifest["rubric"] = rubric

                fixture_directory = write_fixture(
                    Path(root) / "fixture", manifest_changes=change_rubric
                )

                with self.assertRaises(FixtureValidationError):
                    load_fixture(fixture_directory)

    def test_rejects_empty_or_non_string_fixture_and_target_skill_identifiers(self):
        cases = (
            ("id", ""),
            ("id", 7),
            ("target_skill", ""),
            ("target_skill", 7),
        )

        for field, value in cases:
            with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as root:
                def change_identifier(manifest):
                    manifest[field] = value

                fixture_directory = write_fixture(
                    Path(root) / "fixture", manifest_changes=change_identifier
                )

                with self.assertRaises(FixtureValidationError):
                    load_fixture(fixture_directory)

    def test_rejects_empty_source_regression_expected_findings_and_rubric(self):
        def empty_source(sources):
            sources[0]["id"] = ""
            return sources

        def empty_regression_id(manifest):
            manifest["regressions"][0]["id"] = ""

        def empty_expected_findings(manifest):
            manifest["regressions"][0]["expected_findings"] = []

        def empty_rubric(manifest):
            manifest["rubric"] = []

        cases = (
            ("source-id", None, empty_source),
            ("regression-id", empty_regression_id, None),
            ("expected-findings", empty_expected_findings, None),
            ("rubric", empty_rubric, None),
        )

        for label, manifest_changes, source_changes in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory() as root:
                fixture_directory = write_fixture(
                    Path(root) / "fixture",
                    manifest_changes=manifest_changes,
                    source_changes=source_changes,
                )

                with self.assertRaises(FixtureValidationError):
                    load_fixture(fixture_directory)

    def test_rejects_duplicate_contract_and_expected_finding_entries(self):
        def duplicate_required_fields(manifest):
            manifest["deterministic"]["required_fields"] = [
                "analysis.result",
                "analysis.result",
            ]

        def duplicate_headings(manifest):
            manifest["deterministic"]["ordered_headings"] = ["Result", "Result"]

        def duplicate_citations(manifest):
            manifest["deterministic"]["required_citations"] = ["SRC-1", "SRC-1"]

        def duplicate_expected_findings(manifest):
            manifest["regressions"][0]["expected_findings"] = [
                "citation-missing",
                "citation-missing",
            ]

        cases = (
            duplicate_required_fields,
            duplicate_headings,
            duplicate_citations,
            duplicate_expected_findings,
        )

        for manifest_changes in cases:
            with self.subTest(change=manifest_changes.__name__), tempfile.TemporaryDirectory() as root:
                fixture_directory = write_fixture(
                    Path(root) / "fixture", manifest_changes=manifest_changes
                )

                with self.assertRaisesRegex(FixtureValidationError, "duplicate"):
                    load_fixture(fixture_directory)

    def test_rejects_empty_corpus(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaisesRegex(FixtureValidationError, "fixture"):
                load_corpus(Path(root))

    def test_rejects_immediate_corpus_child_without_fixture_manifest(self):
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / "missing-manifest").mkdir()

            with self.assertRaisesRegex(FixtureValidationError, "fixture.json"):
                load_corpus(Path(root))


if __name__ == "__main__":
    unittest.main()
