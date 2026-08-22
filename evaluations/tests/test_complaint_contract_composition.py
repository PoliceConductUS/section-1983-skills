import html
import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILLS = REPOSITORY / "skills"
GENERAL_PACKAGE = "drafting-section-1983-complaints"
UMBRELLA_PACKAGE = "section-1983-drafting"
FALSE_ARREST_PACKAGE = "drafting-false-arrest-complaints"
PACKAGES = (GENERAL_PACKAGE, UMBRELLA_PACKAGE, FALSE_ARREST_PACKAGE)
CANONICAL_HUMAN_REFERENCE = (
    "references/complaint-contract.md"
)
CANONICAL_MECHANICAL_REFERENCE = (
    "references/complaint-structure-contract.json"
)
FALSE_ARREST_DELTA = "references/false-arrest-complaint-delta.md"
SECTION_IDS = (
    "caption",
    "introduction",
    "jurisdiction-and-venue",
    "parties",
    "statement-of-facts",
    "counts",
    "prayer-for-relief",
    "jury-demand",
    "signature-block",
)
COUNT_CARDINALITY = ("claim", "defendant", "capacity")
REQUIRED_COUNT_FIELDS = (
    "count_id",
    "claim",
    "constitutional_source",
    "defendant",
    "capacity",
    "challenged_act",
    "event_stage",
    "standard",
    "standard_pincite",
    "decisive_fact_paragraphs",
    "incorporated_paragraphs",
    "relevant_time_knowledge",
    "application",
    "injury",
    "relief",
    "result",
)
QUALIFIED_IMMUNITY_FIELDS = (
    "event_date",
    "precise_right",
    "binding_pre_event_authority",
    "materially_similar_facts",
    "material_differences",
    "fair_warning",
    "prong_one_result",
    "prong_two_result",
)
MECHANICAL_CHECKS = (
    "section-presence",
    "section-order",
    "paragraph-numbering-continuity",
    "count-numbering-continuity",
    "unique-count-id",
    "claim-defendant-capacity-cardinality",
    "cross-reference-target",
    "incorporation-target",
    "required-count-field-location",
)
EXCLUDED_JUDGMENTS = (
    "fact-truth",
    "legal-sufficiency",
    "authority-fit",
    "material-analogy",
    "strategy",
    "filing-readiness",
)
FINDING_FIELDS = (
    "finding_id",
    "check_id",
    "severity",
    "artifact",
    "location",
    "message",
)
SECTION_HEADINGS = (
    "caption",
    "introduction",
    "jurisdiction and venue",
    "parties",
    "statement of facts",
    "counts",
    "prayer for relief",
    "jury demand",
    "signature block",
)


def normalized_label(value):
    return re.sub(r"\s+", " ", value.strip().casefold())


def without_code_examples(markdown):
    kept = []
    fence = None
    for line in markdown.splitlines(keepends=True):
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is not None:
            kept.append("\n" if line.endswith("\n") else "")
            if opening and opening.group(1)[0] == fence[0] and len(opening.group(1)) >= len(fence):
                fence = None
            continue
        if opening:
            fence = opening.group(1)
            kept.append("\n" if line.endswith("\n") else "")
            continue
        if line.startswith(("    ", "\t")):
            kept.append("\n" if line.endswith("\n") else "")
            continue
        kept.append(line)
    visible = "".join(kept)
    visible = re.sub(r"(`+)(?:.|\n)*?\1", "", visible)
    return re.sub(r"(~{3,})(?:.|\n)*?\1", "", visible)


def markdown_destinations(markdown):
    visible = without_code_examples(markdown)
    references = {}
    for match in re.finditer(
        r"(?m)^ {0,3}\[([^\]]+)\]:\s*(?:<([^>]+)>|(\S+))", visible
    ):
        references[normalized_label(match.group(1))] = match.group(2) or match.group(3)

    visible_without_definitions = re.sub(
        r"(?m)^ {0,3}\[[^\]]+\]:\s*(?:<[^>]+>|\S+).*$(?:\n|$)",
        "",
        visible,
    )

    destinations = []
    inline = re.compile(
        r"(?<!!)\[[^\]]*\]\(\s*(?:<([^>]+)>|\"([^\"]+)\"|'([^']+)'|([^\s)]+))"
    )
    for match in inline.finditer(visible_without_definitions):
        destinations.append(next(value for value in match.groups() if value is not None))

    reference = re.compile(r"(?<!!)\[([^\]]+)\]\[([^\]]*)\]")
    for match in reference.finditer(visible_without_definitions):
        label = normalized_label(match.group(2) or match.group(1))
        if label in references:
            destinations.append(references[label])

    shortcut = re.compile(r"(?<![!\]])\[([^\]]+)\](?![\[(])")
    for match in shortcut.finditer(visible_without_definitions):
        label = normalized_label(match.group(1))
        if label in references:
            destinations.append(references[label])

    for match in re.finditer(r"(?is)<a\b[^>]*?\bhref\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))", visible_without_definitions):
        destinations.append(next(value for value in match.groups() if value is not None))

    for match in re.finditer(r"<([^ <>]+)>", visible_without_definitions):
        target = match.group(1)
        if re.match(r"(?:[a-z][a-z0-9+.-]*:|[^@ <>]+@[^@ <>]+$)", target, re.I):
            destinations.append(target)
    return [html.unescape(destination) for destination in destinations]


def copied_install(directory, package_names=PACKAGES):
    install = Path(directory) / "install"
    destination_skills = install / "skills"
    for package_name in package_names:
        shutil.copytree(
            SKILLS / package_name,
            destination_skills / package_name,
            symlinks=True,
        )
    return install


def is_external_destination(destination):
    return bool(
        re.match(r"(?:[a-z][a-z0-9+.-]*:|//|[^/]+@[^/]+$)", destination, re.I)
    )


def assert_install_local_links(test, package_directory):
    package_root = package_directory.resolve()
    for markdown_path in package_directory.rglob("*.md"):
        for destination in markdown_destinations(markdown_path.read_text(encoding="utf-8")):
            target = destination.split("#", 1)[0].split("?", 1)[0]
            if is_external_destination(target):
                continue
            test.assertFalse(Path(target).is_absolute(), "absolute local path")
            test.assertFalse(re.match(r"^[A-Za-z]:[\\/]", target), "drive path")
            test.assertNotIn("..", Path(target).parts, "traversal")
            resolved = (markdown_path.parent / target).resolve()
            test.assertTrue(
                resolved.is_relative_to(package_root),
                "symlink or target escapes isolated package",
            )
            test.assertTrue(resolved.is_file(), "missing local target")


def local_markdown_routes(path):
    return tuple(
        destination.split("#", 1)[0].split("?", 1)[0]
        for destination in markdown_destinations(path.read_text(encoding="utf-8"))
        if destination.endswith(".md")
    )


def normalized_text(path):
    return re.sub(r"\s+", " ", without_code_examples(path.read_text(encoding="utf-8"))).casefold()


def contains_whole_complaint_skeleton(markdown):
    numbered_items = re.findall(r"(?m)^\s*\d+\.\s+(.+)$", without_code_examples(markdown))
    normalized_items = " ".join(normalized_label(item) for item in numbered_items)
    return all(heading in normalized_items for heading in SECTION_HEADINGS)


def has_complete_count_field_list(markdown):
    normalized = normalized_text_value(markdown)
    return all(field in normalized for field in REQUIRED_COUNT_FIELDS)


def normalized_text_value(value):
    return re.sub(r"\s+", " ", without_code_examples(value)).casefold()


def assert_fail_closed(test, path):
    text = normalized_text(path)
    test.assertIn("complaint contract unavailable", text)
    test.assertRegex(
        text,
        r"(?:do not|must not|never) (?:draft|revise|audit|invent|reconstruct|proceed)",
    )


def assert_machine_contract(test, path):
    test.assertTrue(path.is_file(), "canonical mechanical complaint contract is unavailable")
    if not path.is_file():
        return
    contract = json.loads(path.read_text(encoding="utf-8"))
    test.assertEqual(contract["version"], 1)
    test.assertEqual(contract["owner"], GENERAL_PACKAGE)
    test.assertEqual(
        tuple(section["id"] for section in contract["sections"]),
        SECTION_IDS,
    )
    test.assertEqual(
        tuple(section["id"] for section in contract["sections"] if section.get("optional")),
        ("introduction",),
    )
    test.assertTrue(
        all(
            section.get("optional") is False
            for section in contract["sections"]
            if section["id"] != "introduction"
        )
    )
    test.assertEqual(tuple(contract["count_cardinality"]), COUNT_CARDINALITY)
    test.assertEqual(tuple(contract["required_count_fields"]), REQUIRED_COUNT_FIELDS)
    test.assertEqual(
        tuple(contract["conditional_qualified_immunity_fields"]),
        QUALIFIED_IMMUNITY_FIELDS,
    )
    test.assertEqual(tuple(contract["mechanical_checks"]), MECHANICAL_CHECKS)
    test.assertEqual(tuple(contract["excluded_judgments"]), EXCLUDED_JUDGMENTS)
    test.assertEqual(tuple(contract["finding_fields"]), FINDING_FIELDS)
    test.assertEqual(contract["hard_failure_exit_status"], "nonzero")


def assert_only_canonical_machine_contract(test, skills_directory):
    contracts = tuple(
        sorted(
            path.relative_to(skills_directory)
            for path in skills_directory.rglob("complaint-structure-contract.json")
        )
    )
    test.assertEqual(
        contracts,
        (Path(GENERAL_PACKAGE) / CANONICAL_MECHANICAL_REFERENCE,),
    )


class ComplaintContractCompositionTest(unittest.TestCase):
    def test_live_links_are_confined_to_each_isolated_package(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            for package_name in PACKAGES:
                with self.subTest(package=package_name):
                    assert_install_local_links(self, install / "skills" / package_name)

    def test_markdown_link_parser_covers_live_navigation_forms_and_rejects_escapes(self):
        with tempfile.TemporaryDirectory() as directory:
            package = Path(directory) / "package"
            package.mkdir()
            for name in ("inline.md", "reference.md", "shortcut.md", "html.md"):
                (package / name).write_text("ok\n", encoding="utf-8")
            markdown = """[inline](inline.md)
[external](https://example.com)
[reference][ref]
[shortcut]
[collapsed][]
[ref]: reference.md
[shortcut]: shortcut.md
[collapsed]: html.md
<a href=html.md>html</a>
<a href='html.md'>html</a>
<a href=\"html.md\">html</a>
<https://example.com>
<agent@example.com>
![image](missing.md)
`[ignored](missing.md)`
~~~markdown
[ignored](missing.md)
~~~
    [ignored](missing.md)
"""
            self.assertEqual(
                markdown_destinations(markdown),
                [
                    "inline.md",
                    "https://example.com",
                    "reference.md",
                    "html.md",
                    "shortcut.md",
                    "html.md",
                    "html.md",
                    "html.md",
                    "https://example.com",
                    "agent@example.com",
                ],
            )
            (package / "navigation.md").write_text(markdown, encoding="utf-8")
            assert_install_local_links(self, package)
            for destination in (
                "/tmp/file.md",
                "../escape.md",
                "missing.md",
            ):
                (package / "bad.md").write_text(
                    f"[bad]({destination})\n", encoding="utf-8"
                )
                with self.subTest(destination=destination):
                    with self.assertRaises(AssertionError):
                        assert_install_local_links(self, package)
            for autolink in ("<https://example.com>", "<agent@example.com>"):
                (package / "bad.md").write_text(autolink, encoding="utf-8")
                with self.subTest(autolink=autolink):
                    assert_install_local_links(self, package)
            (package / "bad.md").unlink()
            outside = Path(directory) / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            (package / "escape.md").symlink_to(outside)
            (package / "bad.md").write_text("[bad](escape.md)\n", encoding="utf-8")
            with self.assertRaises(AssertionError):
                assert_install_local_links(self, package)

    def test_canonical_machine_contract_has_the_literal_public_interface(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            assert_machine_contract(
                self,
                install / "skills" / GENERAL_PACKAGE / CANONICAL_MECHANICAL_REFERENCE,
            )

    def test_general_package_routes_to_both_canonical_references_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            package = install / "skills" / GENERAL_PACKAGE
            skill = package / "SKILL.md"
            self.assertTrue(
                (package / CANONICAL_HUMAN_REFERENCE).is_file(),
                "canonical human complaint contract is unavailable",
            )
            self.assertIn(CANONICAL_HUMAN_REFERENCE, local_markdown_routes(skill))
            self.assertIn(CANONICAL_MECHANICAL_REFERENCE, markdown_destinations(skill.read_text(encoding="utf-8")))
            assert_fail_closed(self, skill)

    def test_umbrella_routes_complaints_to_owner_without_a_local_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            package = install / "skills" / UMBRELLA_PACKAGE
            complaint = package / "references" / "documents" / "complaint.md"
            workflow = package / "SKILL.md"
            complaint_text = complaint.read_text(encoding="utf-8")
            self.assertIn(GENERAL_PACKAGE, normalized_text(complaint))
            self.assertIn(GENERAL_PACKAGE, normalized_text(workflow))
            self.assertIn("references/documents/complaint.md", local_markdown_routes(workflow))
            assert_fail_closed(self, complaint)
            assert_fail_closed(self, workflow)
            self.assertFalse(contains_whole_complaint_skeleton(complaint_text))
            self.assertFalse(has_complete_count_field_list(complaint_text))

    def test_false_arrest_loads_general_owner_then_adds_only_a_local_delta(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            package = install / "skills" / FALSE_ARREST_PACKAGE
            skill = package / "SKILL.md"
            delta = package / FALSE_ARREST_DELTA
            skill_text = normalized_text(skill)
            self.assertTrue(delta.is_file(), "false-arrest complaint delta is unavailable")
            self.assertRegex(
                skill_text,
                r"(?:required skill order|load order).{0,280}"
                r"drafting-section-1983-complaints.{0,280}"
                r"(?:then this skill|before applying this skill)",
            )
            complaint_routes = tuple(
                route for route in local_markdown_routes(skill) if "complaint" in route
            )
            self.assertEqual(complaint_routes, (FALSE_ARREST_DELTA,))
            assert_fail_closed(self, skill)
            delta_text = delta.read_text(encoding="utf-8")
            for requirement in (
                "seizure",
                "offense",
                "actor",
                "chronolog",
                "incorporat",
                "warrant",
                "compress",
            ):
                with self.subTest(requirement=requirement):
                    self.assertIn(requirement, normalized_text_value(delta_text))
            self.assertFalse(contains_whole_complaint_skeleton(delta_text))
            self.assertFalse(has_complete_count_field_list(delta_text))
            self.assertNotRegex(
                delta_text,
                r"(?im)^#{1,3}\s+(?:count contract|clearly-established-law matrix|monell rule)\b",
            )

    def test_only_the_general_package_may_publish_the_machine_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            assert_only_canonical_machine_contract(self, install / "skills")

    def test_duplicate_machine_contract_in_a_routing_package_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            canonical = install / "skills" / GENERAL_PACKAGE / CANONICAL_MECHANICAL_REFERENCE
            self.assertTrue(canonical.is_file(), "canonical contract is unavailable")
            if not canonical.is_file():
                return
            for package_name in (UMBRELLA_PACKAGE, FALSE_ARREST_PACKAGE):
                duplicate = install / "skills" / package_name / CANONICAL_MECHANICAL_REFERENCE
                duplicate.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(canonical, duplicate)
                with self.subTest(package=package_name):
                    with self.assertRaises(AssertionError):
                        assert_only_canonical_machine_contract(self, install / "skills")
                duplicate.unlink()


if __name__ == "__main__":
    unittest.main()
