import json
import importlib.util
import re
import unittest
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
README_PATH = REPOSITORY_ROOT / "README.md"
GUIDE_PATH = REPOSITORY_ROOT / "JUDGE_OVERLAYS.md"
REQUIRED_GUIDE_TARGETS = {
    "skills/drafting-for-judge-scholer/SKILL.md",
    "skills/studying-rule-59e-decisions/references/decision-corpus.schema.json",
    "skills/studying-rule-59e-decisions/references/transfer-card.schema.json",
    "skills/studying-rule-59e-decisions/scripts/validate_corpus.py",
}
METHOD_HEADINGS = (
    "define the research scope",
    "build and validate the corpus",
    "classify conclusion strength",
    "build the court-conduct checklist",
    "export neutral transfer cards",
    "consume the overlay in drafting",
    "apply the degradation clause",
)
ANTI_GAMING_RULES = (
    "do not manipulate or predict judicial assignment",
    "do not exploit perceived personal preferences",
    "do not tailor facts or law to a supposed desired outcome",
    "do not conceal adverse authority",
    "do not distort the record",
    "do not personalize attacks on the court",
    "do not copy or rename another judge's conclusions",
)
CONDUCT_CATEGORIES = (
    "official rules",
    "individual procedures",
    "standing orders",
    "candor duties",
    "civility requirements",
    "ex parte limits",
    "filing limits",
    "other conduct the court expressly prohibits or discourages",
)
INVERSE_PERMISSIONS = re.compile(
    r"\b(?:may|can|should|is allowed to) "
    r"(?:manipulate|predict|exploit|tailor|conceal|distort|personalize|copy|rename)\b"
)
def normalize(markdown):
    return " ".join(markdown.lower().split())


STRUCTURAL_CONTRACT = normalize(
    "The existing "
    "[Scholer overlay](skills/drafting-for-judge-scholer/SKILL.md) is a "
    "structural example only. It separates judicial authorship stages, "
    "preserves evidence strength, and adds no judge-specific proposition when "
    "qualifying support is absent. Do not copy its substantive conclusions."
)


def prose_markdown(markdown):
    prose = []
    fence = None
    for line in markdown.splitlines():
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            run = marker.group(1)
            if fence is None:
                fence = (run[0], len(run))
            elif run[0] == fence[0] and len(run) >= fence[1]:
                fence = None
            continue
        if fence is not None or line.startswith(("    ", "\t")):
            continue
        prose.append(line)
    return "\n".join(prose)


def live_links(markdown):
    prose = prose_markdown(markdown)
    definitions = {
        key.lower(): destination.strip("<>")
        for key, destination in re.findall(
            r"(?m)^ {0,3}\[([^\]]+)\]:\s*(\S+)", prose
        )
    }
    links = []
    for image, label, destination in re.findall(
        r"(!?)\[([^\]]+)\]\(([^)]+)\)", prose
    ):
        links.append(("image" if image else "markdown", label, destination))
    for image, label, key in re.findall(
        r"(!?)\[([^\]]+)\]\[([^\]]*)\]", prose
    ):
        resolved_key = key or label
        if resolved_key.lower() in definitions:
            kind = "image" if image else "reference"
            links.append((kind, label, definitions[resolved_key.lower()]))
    for label in re.findall(r"(?<!!)\[([^\]]+)\](?![\[(:])", prose):
        if label.lower() in definitions:
            links.append(("reference", label, definitions[label.lower()]))
    for destination in re.findall(
        r"<([A-Za-z][A-Za-z0-9+.-]*:[^ <>]+|[^ <>@]+@[^ <>@]+)>", prose
    ):
        if ":" not in destination:
            destination = f"mailto:{destination}"
        links.append(("autolink", destination, destination))
    for attributes, label in re.findall(
        r"(?is)<a\s+([^>]*)>(.*?)</a>", prose
    ):
        destination = html_attribute(attributes, "href")
        if destination:
            links.append(("html", re.sub(r"<[^>]+>", "", label), destination))
    for tag, attributes in re.findall(
        r"(?is)<(area|link|img)\s+([^>]*)>", prose
    ):
        destination = html_attribute(attributes, "src" if tag.lower() == "img" else "href")
        if destination:
            label = html_attribute(attributes, "alt") or tag
            links.append(("image" if tag.lower() == "img" else "html", label, destination))
    return links


def html_attribute(attributes, name):
    match = re.search(
        rf"(?is)\b{re.escape(name)}\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))",
        attributes,
    )
    if not match:
        return None
    return next(value for value in match.groups() if value is not None)


def second_level_headings(markdown):
    return [
        normalize(heading)
        for heading in re.findall(
            r"(?m)^##\s+(?:\d+\.\s+)?(.+?)\s*$", prose_markdown(markdown)
        )
    ]


def section(markdown, heading):
    match = re.search(
        rf"(?ms)^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)", markdown
    )
    return match.group(1) if match else ""


def yaml_record(markdown, heading):
    body = section(markdown, heading)
    match = re.search(r"(?ms)^```ya?ml\s*$\n(.*?)^```\s*$", body)
    if not match:
        return {}
    record = {}
    for line in match.group(1).splitlines():
        key, separator, value = line.partition(":")
        if separator:
            record[key.strip()] = value.strip()
    return record


def json_record(markdown, heading):
    body = section(markdown, heading)
    match = re.search(r"(?ms)^```json\s*$\n(.*?)^```\s*$", body)
    return json.loads(match.group(1)) if match else {}


class JudgeOverlayGuideTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.readme = README_PATH.read_text(encoding="utf-8")
        cls.guide = GUIDE_PATH.read_text(encoding="utf-8") if GUIDE_PATH.is_file() else ""
        cls.prose = normalize(prose_markdown(cls.guide))

    def assert_readme_route(self, readme):
        routes = [
            link for link in live_links(readme) if "judge overlay" in link[1].lower()
        ]
        self.assertEqual(
            routes, [("markdown", "Create a judge overlay", "JUDGE_OVERLAYS.md")]
        )

    def assert_guide_links(self, guide):
        links = live_links(guide)
        destinations = {destination for _, _, destination in links}
        self.assertEqual(destinations, REQUIRED_GUIDE_TARGETS)
        navigable = {
            destination
            for kind, _, destination in links
            if kind in {"markdown", "reference"}
        }
        self.assertEqual(navigable, REQUIRED_GUIDE_TARGETS)
        for destination in destinations:
            parsed = urlparse(destination)
            self.assertFalse(parsed.scheme or parsed.netloc)
            self.assertFalse(Path(destination).is_absolute())
            resolved = (REPOSITORY_ROOT / destination).resolve()
            resolved.relative_to(REPOSITORY_ROOT.resolve())
            self.assertTrue(resolved.is_file())

    def assert_anti_gaming(self, guide):
        prose = normalize(prose_markdown(guide))
        for rule in ANTI_GAMING_RULES:
            self.assertIn(rule, prose)
        self.assertNotRegex(prose, INVERSE_PERMISSIONS)
        self.assertIn("never predicts an outcome or judicial behavior", prose)
        self.assertIn("does not infer judge psychology", prose)
        self.assertIn("does not publish unsupported tendencies", prose)
        self.assertIn("does not use unverified citations", prose)

    def assert_conduct_record(self, guide):
        record = yaml_record(guide, "Generic synthetic conduct record")
        self.assertEqual(
            set(record),
            {
                "source_id",
                "official_source",
                "issuing_body",
                "jurisdiction_or_judge",
                "checked_on",
                "warning",
                "status",
            },
        )
        self.assertRegex(record["source_id"], r"^COURT-SRC-[0-9]{3}$")
        source = urlparse(record["official_source"])
        self.assertEqual(source.scheme, "https")
        self.assertTrue(source.netloc.endswith(".example.invalid"))
        self.assertNotEqual(record["issuing_body"], "")
        self.assertNotEqual(record["jurisdiction_or_judge"], "")
        date.fromisoformat(record["checked_on"])
        self.assertGreaterEqual(len(record["warning"]), 12)
        self.assertEqual(record["status"], "verified")

    def assert_conduct_contract(self, guide):
        prose = normalize(prose_markdown(guide))
        for category in CONDUCT_CATEGORIES:
            self.assertIn(category, prose)
        self.assert_conduct_record(guide)
        self.assertRegex(
            prose,
            r"unverified or stale warning remains a gap.*"
            r"(?:is not|must not be stated as) a court requirement",
        )
        self.assertNotRegex(
            prose,
            r"(?:an )?unverified (?:or stale )?warnings? "
            r"(?:is|are|counts? as|(?:may|can|must) (?:be|count as)) "
            r"(?:a )?court requirements?",
        )

    def assert_degradation_contract(self, guide):
        prose = normalize(prose_markdown(guide))
        self.assertRegex(
            prose,
            r"(?:thin|incomplete)[^.]*corpus[^.]*adds no judge-specific proposition",
        )
        self.assertNotRegex(
            prose,
            r"(?:thin|incomplete)[^.]*corpus[^.]*"
            r"(?:may|can|should) add a judge-specific proposition",
        )

    def assert_transfer_contract(self, guide):
        prose = normalize(prose_markdown(guide))
        self.assertIn(
            "consume only neutral transfer cards that passed the canonical corpus validator",
            prose,
        )
        self.assertIn(
            "preserve each card's source identity and checked date, evidence level, denominator and missingness, permitted use, and prohibited inference",
            prose,
        )
        self.assertIn(
            "a prohibited inference or no qualifying support produces no judge-specific drafting change",
            prose,
        )
        self.assertNotRegex(
            prose,
            r"(?:discard|ignore|need not preserve).*"
            r"(?:source identity|evidence level|denominator|prohibited inference)",
        )
        self.assertNotRegex(
            prose,
            r"(?:a prohibited inference|no qualifying support) "
            r"(?:may|can|should) produce "
            r"a judge-specific drafting change",
        )

    def assert_schema_valid_card(self, card):
        schema_path = (
            REPOSITORY_ROOT
            / "skills/studying-rule-59e-decisions/references/transfer-card.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(set(card), set(schema["required"]))
        self.assertFalse(schema["additionalProperties"])
        type_checks = {
            "string": lambda value: isinstance(value, str),
            "integer": lambda value: isinstance(value, int) and not isinstance(value, bool),
            "array": lambda value: isinstance(value, list),
        }
        for field, value in card.items():
            rules = schema["properties"][field]
            self.assertTrue(type_checks[rules["type"]](value), field)
            if "minLength" in rules:
                self.assertGreaterEqual(len(value), rules["minLength"], field)
            if "minimum" in rules:
                self.assertGreaterEqual(value, rules["minimum"], field)
            if "minItems" in rules:
                self.assertGreaterEqual(len(value), rules["minItems"], field)
            if rules.get("uniqueItems"):
                self.assertEqual(len(value), len(set(value)), field)
            if "enum" in rules:
                self.assertIn(value, rules["enum"], field)
            if "pattern" in rules:
                self.assertRegex(value, rules["pattern"], field)
            if rules["type"] == "array":
                for item in value:
                    self.assertIsInstance(item, str, field)
                    self.assertGreaterEqual(len(item), rules["items"]["minLength"], field)
        validator_path = (
            REPOSITORY_ROOT
            / "skills/studying-rule-59e-decisions/scripts/validate_corpus.py"
        )
        spec = importlib.util.spec_from_file_location(
            "judge_overlay_corpus_validator", validator_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        findings = []
        module.validate_transfer_cards([card], findings)
        self.assertEqual(findings, [])

    def assert_no_private_or_real_conclusion(self, guide):
        structural = section(guide, "Structural example only")
        self.assertIn("Scholer", structural)
        structural_prose = normalize(structural)
        self.assertEqual(structural_prose, STRUCTURAL_CONTRACT)
        guide_without_urls = re.sub(r"https?://[^\s)>]+", "", guide)
        self.assertNotRegex(
            guide_without_urls,
            r"(?<![A-Za-z0-9])/(?!/)[A-Za-z0-9._-]",
        )
        self.assertNotRegex(guide, r"(?i)(?:^|\s)[A-Z]:\\")
        self.assertNotRegex(
            guide,
            r"(?i)(?:^|\s)(?:\d+:\d{2}-cv-|PD-\d{4}-\d+)",
        )
        without_structural = re.sub(
            r"(?ms)^##\s+Structural example only\s*$\n.*?(?=^##\s+|\Z)",
            "",
            guide,
        )
        self.assertNotIn("scholer", normalize(without_structural))
        judge_names = set(re.findall(r"\bJudge [A-Z][A-Za-z'-]+\b", without_structural))
        self.assertLessEqual(judge_names, {"Judge Example"})
        self.assertNotRegex(
            without_structural,
            r"\b[A-Z][a-z]+ [A-Z][a-z]+[^.\n]{0,80}"
            r"\b(?:always|usually|prefers|dislikes|grants|denies)\b",
        )

    def test_readme_routes_to_root_guide(self):
        self.assertTrue(GUIDE_PATH.is_file())
        self.assert_readme_route(self.readme)

    def test_link_guards_handle_images_html_references_and_fences(self):
        self.assert_guide_links(self.guide)
        image_route = self.readme.replace(
            "[Create a judge overlay](JUDGE_OVERLAYS.md)",
            "![Create a judge overlay](JUDGE_OVERLAYS.md)",
        )
        with self.assertRaises(AssertionError):
            self.assert_readme_route(image_route)
        unsafe = self.guide + '\n<a href="../outside.md">outside</a>\n'
        unsafe += (
            "\n~~~markdown\n"
            "[decoy](skills/drafting-for-judge-scholer/SKILL.md)\n"
            "~~~\n"
        )
        with self.assertRaises(AssertionError):
            self.assert_guide_links(unsafe)
        for hidden in (
            "\n[outside]: https://example.com\n[outside]\n",
            "\n<a href=https://example.com>outside</a>\n",
            "\n<mailto:person@example.com>\n",
        ):
            with self.subTest(hidden=hidden), self.assertRaises(AssertionError):
                self.assert_guide_links(self.guide + hidden)
        image_only = self.guide.replace("[", "![")
        with self.assertRaises(AssertionError):
            self.assert_guide_links(image_only)

    def test_method_stages_are_actual_ordered_headings(self):
        headings = second_level_headings(self.guide)
        positions = []
        for required in METHOD_HEADINGS:
            matches = [
                index for index, heading in enumerate(headings) if required in heading
            ]
            self.assertEqual(len(matches), 1)
            positions.append(matches[0])
        self.assertEqual(positions, sorted(positions))

    def test_corpus_contract_and_strength_limits_are_explicit(self):
        for phrase in (
            "official primary materials",
            "docket documents",
            "retrieval leads",
            "assigned judge, reasoning author, recommendation author, and adopting judge",
            "denominator",
            "missingness",
            "adverse and disconfirming evidence",
            "one verified disposition is an example",
            "an incomplete or non-systematic group is a documented cluster",
            "a tendency requires a disclosed complete denominator",
        ):
            self.assertIn(phrase, self.prose)
        self.assertRegex(
            self.prose,
            r"canonical corpus.*must pass.*validate_corpus\.py.*before "
            r"(?:publication or transfer|publication and transfer)",
        )

    def test_degradation_clause_rejects_reversed_semantics(self):
        self.assert_degradation_contract(self.guide)
        mutated = self.guide.replace(
            "adds no judge-specific proposition", "may add a judge-specific proposition"
        )
        with self.assertRaises(AssertionError):
            self.assert_degradation_contract(mutated)

    def test_anti_gaming_boundary_rejects_inverse_permission(self):
        self.assert_anti_gaming(self.guide)
        for rule in ANTI_GAMING_RULES:
            mutated = self.guide.replace(rule, rule.replace("do not ", "may ", 1))
            with self.subTest(rule=rule), self.assertRaises(AssertionError):
                self.assert_anti_gaming(mutated)
        with self.assertRaises(AssertionError):
            self.assert_anti_gaming(self.guide + "\nThe overlay may manipulate assignment.\n")

    def test_court_conduct_is_source_bounded_and_fail_closed(self):
        self.assert_conduct_contract(self.guide)
        for original, replacement in (
            ("checked_on: 2026-08-20", "checked_on:"),
            (
                "official_source: https://court.example.invalid/rules",
                "official_source: notes.md",
            ),
            ("status: verified", "status: unverified"),
        ):
            with self.subTest(replacement=replacement), self.assertRaises(
                (AssertionError, ValueError)
            ):
                self.assert_conduct_contract(self.guide.replace(original, replacement))
        for inverse in (
            "An unverified warning is a court requirement.",
            "Unverified warnings are court requirements.",
            "An unverified warning may be a court requirement.",
            "An unverified warning may count as a court requirement.",
            "Unverified warnings can count as court requirements.",
        ):
            with self.subTest(inverse=inverse), self.assertRaises(AssertionError):
                self.assert_conduct_contract(self.guide + f"\n{inverse}\n")

    def test_transfer_cards_preserve_limits_and_fail_closed(self):
        self.assert_transfer_contract(self.guide)
        self.assertIn("governing law remains separate", self.prose)
        self.assertIn("does not expose private strategy", self.prose)
        self.assertIn("does not select a litigation path", self.prose)
        mutated = self.guide.replace("preserve each card's", "discard each card's")
        with self.assertRaises(AssertionError):
            self.assert_transfer_contract(mutated)
        contradiction = (
            self.guide
            + "\nA prohibited inference may produce a judge-specific drafting change.\n"
        )
        with self.assertRaises(AssertionError):
            self.assert_transfer_contract(contradiction)
        unsupported = (
            self.guide
            + "\nNo qualifying support may produce a judge-specific drafting change.\n"
        )
        with self.assertRaises(AssertionError):
            self.assert_transfer_contract(unsupported)

    def test_paired_examples_are_parsed_fictional_and_bounded(self):
        valid_metadata = yaml_record(self.guide, "Generic synthetic valid overlay")
        valid = json_record(self.guide, "Generic synthetic valid overlay")
        thin = yaml_record(self.guide, "Generic synthetic thin-corpus result")
        self.assertEqual(
            set(valid_metadata), {"fictional", "court_id", "judge_id", "artifact"}
        )
        self.assertEqual(valid_metadata.get("fictional"), "true")
        self.assertEqual(thin.get("fictional"), "true")
        self.assertEqual(
            set(thin),
            {
                "fictional",
                "court_id",
                "judge_id",
                "corpus_status",
                "overlay_result",
                "gap",
            },
        )
        for record in (valid_metadata, thin):
            self.assertRegex(record.get("court_id", ""), r"^Example District$")
            self.assertRegex(record.get("judge_id", ""), r"^Judge Example$")
        self.assertEqual(valid_metadata.get("artifact"), "validated neutral transfer card")
        self.assert_schema_valid_card(valid)
        invalid_count = dict(valid, numerator=valid["denominator"] + 1)
        with self.assertRaises(AssertionError):
            self.assert_schema_valid_card(invalid_count)
        invalid_date = dict(valid, source_checked_date="2026-99-99")
        with self.assertRaises(AssertionError):
            self.assert_schema_valid_card(invalid_date)
        self.assertEqual(thin.get("corpus_status"), "incomplete")
        self.assertEqual(thin.get("overlay_result"), "no judge-specific proposition")
        self.assertNotEqual(thin.get("gap", ""), "")
        serialized_examples = normalize(json.dumps([valid_metadata, valid, thin]))
        self.assertNotRegex(
            serialized_examples,
            r"judge (?!example\b)[a-z][a-z'-]+[^.]{0,80}"
            r"\b(?:always|usually|prefers|dislikes|grants|denies)\b",
        )

    def test_examples_and_structural_reference_exclude_private_conclusions(self):
        self.assertIn("structural example only", self.prose)
        self.assertIn("do not copy its substantive conclusions", self.prose)
        self.assert_no_private_or_real_conclusion(self.guide)
        for unsafe in (
            "/private/tmp/client-record",
            "`/private/tmp/client-record`",
            "Jane Doe usually denies Rule 59 motions.",
            "Judge Other prefers short motions.",
        ):
            with self.subTest(unsafe=unsafe), self.assertRaises(AssertionError):
                self.assert_no_private_or_real_conclusion(self.guide + f"\n{unsafe}\n")
        structural_mutation = self.guide.replace(
            "structural example only",
            "structural example only. Judge Scholer usually denies Rule 59 motions. "
            "Source: /private/tmp/client-record",
        )
        with self.assertRaises(AssertionError):
            self.assert_no_private_or_real_conclusion(structural_mutation)
        for conclusion in (
            "Judge Scholer has a tendency to deny Rule 59 motions.",
            "Judge Scholer has a preference for denying Rule 59 motions.",
            "Judge Scholer outcomes favor denial of Rule 59 motions.",
        ):
            mutated = self.guide.replace(
                "Do not copy its substantive conclusions.", conclusion
            )
            with self.subTest(conclusion=conclusion), self.assertRaises(AssertionError):
                self.assert_no_private_or_real_conclusion(mutated)
        for hidden in (
            "\n```text\nJudge Scholer has a tendency to deny Rule 59 motions.\n```",
            "\n    Judge Scholer has a preference for denying Rule 59 motions.",
        ):
            mutated = self.guide.replace(
                "Do not copy its substantive conclusions.",
                f"Do not copy its substantive conclusions.{hidden}",
            )
            with self.subTest(hidden=hidden), self.assertRaises(AssertionError):
                self.assert_no_private_or_real_conclusion(mutated)


if __name__ == "__main__":
    unittest.main()
