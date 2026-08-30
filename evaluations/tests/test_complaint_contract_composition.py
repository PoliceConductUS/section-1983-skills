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
COUNT_CARDINALITY = ("claim", "defendant", "capacity", "challenged_act")
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
    "qualified_immunity",
    "monell_paths",
)
QUALIFIED_IMMUNITY_FIELDS = (
    "event_date",
    "precise_right",
    "jurisdiction",
    "prong_one_result",
    "prong_two_result",
    "binding_pre_event_authority",
    "authority_audit_status",
    "materially_similar_facts",
    "material_differences",
    "fair_warning",
    "rule_of_orderliness_review_status",
    "later_history_review_status",
    "later_authority_treatment",
)
MECHANICAL_CHECKS = (
    "strict-contract-version",
    "section-presence",
    "section-order",
    "unique-count-id",
    "claim-defendant-capacity-challenged-act-cardinality",
    "paragraph-reference-target",
    "typed-individual-capacity-unit",
    "conditional-qualified-immunity-unit",
    "separated-monell-path",
    "path-specific-monell-fields",
    "assessment-document-fingerprint",
    "assessment-claim-coverage",
    "authority-artifact-hash",
    "authority-exact-passage",
)
EXCLUDED_JUDGMENTS = (
    "fact-truth",
    "legal-sufficiency",
    "authority-fit",
    "material-analogy",
    "strategy",
    "filing-readiness",
)
FINDING_FIELDS = ("code", "location", "message")
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
HUMAN_COUNT_REQUIREMENTS = (
    r"\belement\b",
    r"\bcount (?:id|identifier)\b",
    r"\bclaim\b",
    r"\bconstitutional source\b",
    r"\bdefendant\b",
    r"\bcapacity\b",
    r"\bchallenged act\b",
    r"\bevent stage\b",
    r"\b(?:governing )?standard\b",
    r"\b(?:standard )?(?:pinpoint|pincite)\b",
    r"\bdecisive[- ]fact paragraphs?\b",
    r"\bincorporated paragraphs?\b",
    r"\brelevant[- ]time knowledge\b",
    r"\bapplication\b",
    r"\binjury\b",
    r"\brelief\b",
    r"\bresult\b",
    r"\bevent date\b",
    r"\bprecise right\b",
    r"\bbinding pre[- ]event authority\b",
    r"\bmaterially similar facts\b",
    r"\bmaterial differences\b",
    r"\bfair warning\b",
    r"\bprong (?:one|1) result\b",
    r"\bprong (?:two|2) result\b",
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


def local_destination(destination):
    return destination.split("#", 1)[0].split("?", 1)[0]


def assert_install_local_links(test, package_directory):
    package_root = package_directory.resolve()
    for markdown_path in package_directory.rglob("*.md"):
        for destination in markdown_destinations(markdown_path.read_text(encoding="utf-8")):
            if is_external_destination(destination):
                continue
            target = local_destination(destination)
            test.assertFalse(Path(target).is_absolute(), "absolute local path")
            test.assertFalse(re.match(r"^[A-Za-z]:[\\/]", target), "drive path")
            test.assertNotIn("..", Path(target).parts, "traversal")
            resolved = (markdown_path if not target else markdown_path.parent / target).resolve()
            test.assertTrue(
                resolved.is_relative_to(package_root),
                "symlink or target escapes isolated package",
            )
            test.assertTrue(resolved.is_file(), "missing local target")


def local_markdown_routes(path):
    return tuple(
        local_destination(destination)
        for destination in markdown_destinations(path.read_text(encoding="utf-8"))
        if local_destination(destination).endswith(".md")
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


def assert_human_contract(test, path):
    test.assertTrue(path.is_file(), "canonical human complaint contract is unavailable")
    if not path.is_file():
        return
    text = normalized_text(path)
    position = 0
    for heading in SECTION_HEADINGS:
        match = re.search(re.escape(heading), text[position:])
        test.assertIsNotNone(match, f"missing ordered human section: {heading}")
        if match is None:
            return
        position += match.end()
    test.assertRegex(text, r"(?:introduction.{0,80}optional|optional.{0,80}introduction)")
    test.assertRegex(
        text,
        r"one (?:count )?mapping (?:for|per) (?:every|each) "
        r"claim[- ]defendant[- ]capacity tuple",
    )
    for requirement in HUMAN_COUNT_REQUIREMENTS:
        with test.subTest(requirement=requirement):
            test.assertRegex(text, requirement)


def assert_fail_closed(test, path):
    text = normalized_text(path)
    test.assertIn("complaint contract unavailable", text)
    test.assertRegex(
        text,
        r"(?:do not|must not|never)\s+draft,\s+revise,\s+or\s+audit",
    )
    test.assertRegex(
        text,
        r"(?:do not|must not|never)\s+invent(?:\s+or)?\s+reconstruct",
    )


def assert_machine_contract(test, path):
    test.assertTrue(path.is_file(), "canonical mechanical complaint contract is unavailable")
    if not path.is_file():
        return
    contract = json.loads(path.read_text(encoding="utf-8"))
    test.assertEqual(contract["version"], 2)
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
    test.assertIn("capacity", contract["required_count_fields"])
    test.assertIn("capacity", contract["count_cardinality"])
    test.assertEqual(
        tuple(contract["conditional_qualified_immunity_fields"]),
        QUALIFIED_IMMUNITY_FIELDS,
    )
    test.assertEqual(tuple(contract["mechanical_checks"]), MECHANICAL_CHECKS)
    test.assertEqual(tuple(contract["excluded_deterministic_judgments"]), EXCLUDED_JUDGMENTS)
    test.assertEqual(tuple(contract["finding_fields"]), FINDING_FIELDS)
    test.assertEqual(contract["hard_failure_exit_status"], "nonzero")


def assert_human_machine_qi_fields_align(test, human_path, machine_path):
    human = human_path.read_text(encoding="utf-8")
    block = re.search(
        r"When qualified immunity applies.*?conditional\s+fields:(.*?)"
        r"If a required universal field",
        human,
        re.DOTALL | re.I,
    )
    test.assertIsNotNone(block, "human conditional QI field block is unavailable")
    if block is None:
        return
    human_ids = tuple(
        re.findall(r"`([a-z][a-z0-9_]*)`", block.group(1))
    )
    machine = json.loads(machine_path.read_text(encoding="utf-8"))
    machine_ids = tuple(machine["conditional_qualified_immunity_fields"])
    test.assertEqual(human_ids, QUALIFIED_IMMUNITY_FIELDS)
    test.assertEqual(human_ids, machine_ids)


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


def assert_false_arrest_delta_has_no_general_machine_fields(test, delta):
    identifiers = set(REQUIRED_COUNT_FIELDS) | set(QUALIFIED_IMMUNITY_FIELDS)
    for identifier in re.findall(r"`([a-z][a-z0-9_]*)`", delta):
        test.assertNotIn(
            identifier,
            identifiers,
            f"false-arrest delta repeats canonical machine field `{identifier}`",
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
                (package / name).write_text("# Anchor\n", encoding="utf-8")
            markdown = """[inline](inline.md)
[fragment](inline.md#anchor)
[self](#local-anchor)
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

# Local anchor
"""
            self.assertEqual(
                markdown_destinations(markdown),
                [
                    "inline.md",
                    "inline.md#anchor",
                    "#local-anchor",
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
            self.assertEqual(
                local_markdown_routes(package / "navigation.md").count("inline.md"),
                2,
            )
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
            package = install / "skills" / GENERAL_PACKAGE
            assert_machine_contract(
                self,
                package / CANONICAL_MECHANICAL_REFERENCE,
            )
            assert_human_machine_qi_fields_align(
                self,
                package / CANONICAL_HUMAN_REFERENCE,
                package / CANONICAL_MECHANICAL_REFERENCE,
            )

    def test_human_count_field_ids_match_the_machine_handoff(self):
        human = (
            SKILLS / GENERAL_PACKAGE / CANONICAL_HUMAN_REFERENCE
        ).read_text(encoding="utf-8")
        field_block = re.search(
            r"Record the following fields in this order:(.*?)"
            r"When qualified immunity applies",
            human,
            re.DOTALL,
        )
        self.assertIsNotNone(field_block, "human count-field block is unavailable")
        if field_block is None:
            return
        self.assertEqual(
            tuple(re.findall(r"`([a-z][a-z0-9_]*)`", field_block.group(1))),
            REQUIRED_COUNT_FIELDS,
        )

    def test_general_package_routes_to_both_canonical_references_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            package = install / "skills" / GENERAL_PACKAGE
            skill = package / "SKILL.md"
            assert_human_contract(self, package / CANONICAL_HUMAN_REFERENCE)
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
            reference_index = re.sub(
                r"\s+", " ", workflow.read_text(encoding="utf-8").casefold()
            )
            self.assertNotRegex(
                reference_index,
                r"references/documents/.{0,160}(?:one|a) "
                r"(?:federal[- ]baseline )?skeleton.{0,160}complaint\.md",
            )

    def test_fail_closed_rejects_drafting_permission_despite_noninvention_rule(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            complaint = (
                install
                / "skills"
                / UMBRELLA_PACKAGE
                / "references"
                / "documents"
                / "complaint.md"
            )
            mutated, replacements = re.subn(
                r"do not draft, revise, or\s+audit the complaint\. Do not\s+"
                r"invent or reconstruct the missing requirements\.",
                "may draft, revise, or audit the complaint. Do not invent or "
                "reconstruct the missing requirements.",
                complaint.read_text(encoding="utf-8"),
                count=1,
                flags=re.I,
            )
            self.assertEqual(replacements, 1)
            complaint.write_text(mutated, encoding="utf-8")
            with self.assertRaises(AssertionError):
                assert_fail_closed(self, complaint)

    def test_general_skill_has_no_competing_count_function_sequence(self):
        skill = normalized_text(SKILLS / GENERAL_PACKAGE / "SKILL.md")
        self.assertIn(
            "element → decisive facts → relevant-time knowledge → application → result",
            skill,
        )
        self.assertNotRegex(
            skill,
            r"element (?:→|->) facts (?:→|->) inference (?:→|->) result",
        )

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
            assert_false_arrest_delta_has_no_general_machine_fields(self, delta_text)

    def test_false_arrest_delta_rejects_one_general_machine_field(self):
        with tempfile.TemporaryDirectory() as directory:
            install = copied_install(directory)
            delta = install / "skills" / FALSE_ARREST_PACKAGE / FALSE_ARREST_DELTA
            self.assertTrue(delta.is_file(), "false-arrest complaint delta is unavailable")
            if not delta.is_file():
                return
            delta.write_text(
                delta.read_text(encoding="utf-8") + "\nGeneral field: `count_id`.\n",
                encoding="utf-8",
            )
            with self.assertRaises(AssertionError):
                assert_false_arrest_delta_has_no_general_machine_fields(
                    self,
                    delta.read_text(encoding="utf-8"),
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
