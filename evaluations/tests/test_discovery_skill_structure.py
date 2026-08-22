import re
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPOSITORY = Path(__file__).resolve().parents[2]
README = REPOSITORY / "README.md"
ROUTER_DIRECTORY = REPOSITORY / "skills" / "section-1983-drafting"
ROUTER = ROUTER_DIRECTORY / "SKILL.md"
COORDINATION_REFERENCE = (
    ROUTER_DIRECTORY / "references" / "discovery-coordination-contract.md"
)

SKILL_NAMES = (
    "drafting-section-1983-written-discovery",
    "auditing-section-1983-discovery-responses",
    "drafting-section-1983-meet-and-confer",
    "auditing-section-1983-privilege-logs",
    "drafting-section-1983-deposition-outlines",
)

TARGET_FIELDS = (
    "target_id",
    "claim",
    "defendant",
    "element",
    "factual_gap",
    "likely_custodian",
    "expected_native_source",
)

INLINE_MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
REFERENCE_MARKDOWN_LINK = re.compile(r"!?\[([^\]]+)\]\[([^\]]*)\]")
REFERENCE_MARKDOWN_DEFINITION = re.compile(
    r"(?m)^\s{0,3}\[([^\]]+)\]:\s*(<[^>]+>|\S+)"
)


def skill_directory(name):
    return REPOSITORY / "skills" / name


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


def assert_positive_requirement(test, text, label, term):
    with test.subTest(requirement=label):
        test.assertRegex(
            text,
            rf"(?is)(?:"
            rf"(?:must|shall)\s+(?!not\b)(?:include|record|identify|audit|state|mark|flag|address).{{0,500}}(?:{term})"
            rf"|(?:outline|output)\s+(?:marks?|flags?|identifies?|includes?|addresses?).{{0,120}}(?:{term})"
            rf")",
        )


def markdown_targets(markdown):
    for match in INLINE_MARKDOWN_LINK.finditer(markdown):
        raw_target = match.group(1).strip()
        yield markdown_destination(raw_target)

    definitions = {}
    for match in REFERENCE_MARKDOWN_DEFINITION.finditer(markdown):
        label = match.group(1).strip().casefold()
        target = markdown_destination(match.group(2).strip())
        definitions[label] = target
        yield target

    for match in REFERENCE_MARKDOWN_LINK.finditer(markdown):
        link_text = match.group(1).strip()
        label = (match.group(2).strip() or link_text).casefold()
        if label not in definitions:
            raise AssertionError(f"reference-style Markdown link is undefined: {label}")


def markdown_destination(raw_target):
    if raw_target.startswith("<") and ">" in raw_target:
        return raw_target[1 : raw_target.index(">")]
    return raw_target.split(maxsplit=1)[0]


class DiscoverySkillStructureTest(unittest.TestCase):

    def test_named_public_skill_packages_have_metadata(self):
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                directory = skill_directory(name)
                skill = required_text(directory / "SKILL.md")
                metadata = required_text(directory / "agents" / "openai.yaml")

                self.assertRegex(skill, rf"(?m)^name:\s*{re.escape(name)}\s*$")
                self.assertRegex(skill, r"(?m)^description:\s*(?:>|>-|\S)")
                assert_phrases(
                    self,
                    metadata,
                    (
                        "interface:",
                        "display_name:",
                        "short_description:",
                        "default_prompt:",
                        f"${name}",
                    ),
                )

    def test_readme_and_existing_router_route_every_peer(self):
        readme = required_text(README)
        router = required_text(ROUTER)

        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                self.assertIn(f"`{name}`", readme)
                self.assertIn(f"`{name}`", router)
        self.assertIn("references/discovery-coordination-contract.md", router)

    def test_shared_coordination_reference_exposes_complete_contract(self):
        reference = required_text(COORDINATION_REFERENCE)

        assert_phrases(
            self,
            reference,
            TARGET_FIELDS
            + (
                "proportionality",
                "PLAINTIFF DECISION REQUIRED",
            ),
        )
        self.assert_approved_source_identifiers(reference)
        self.assert_common_contract_semantics(reference)

    def test_every_peer_repeats_the_portable_coordination_contract(self):
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                skill = required_text(skill_directory(name) / "SKILL.md")
                assert_phrases(
                    self,
                    skill,
                    TARGET_FIELDS
                    + (
                        "proportionality",
                        "PLAINTIFF DECISION REQUIRED",
                    ),
                )
                self.assert_approved_source_identifiers(skill)
                self.assert_common_contract_semantics(skill)

    def test_written_discovery_owns_distinct_bounded_request_forms(self):
        skill = required_text(
            skill_directory("drafting-section-1983-written-discovery") / "SKILL.md"
        )

        assert_phrases(
            self,
            skill,
            (
                "requests for production",
                "interrogatories",
                "requests for admission",
            ),
        )
        assert_semantics(
            self,
            skill,
            (
                (
                    "separate numbering",
                    (r"separately\s+number", r"number.{0,50}separate"),
                ),
                (
                    "request target links",
                    (
                        r"request.{0,80}target(?:_id|\s+ID)",
                        r"target(?:_id|\s+ID).{0,80}request",
                    ),
                ),
                ("native form", (r"native\s+form",)),
                (
                    "bounded categories",
                    (r"bounded.{0,80}(?:document|ESI|categor)",),
                ),
                (
                    "discrete admission",
                    (
                        r"(?:admission|RFA).{0,80}(?:one|single|discrete)\s+(?:fact|proposition)",
                        r"(?:one|single|discrete)\s+(?:fact|proposition).{0,80}(?:admission|RFA)",
                    ),
                ),
                (
                    "approved numerical limits",
                    (
                        r"approved.{0,60}numerical\s+limit",
                        r"numerical\s+limit.{0,60}approved",
                    ),
                ),
                ("importance", (r"importance",)),
                ("burden", (r"burden",)),
                (
                    "narrower alternatives",
                    (
                        r"narrower.{0,30}alternative",
                        r"alternative.{0,30}narrower",
                    ),
                ),
            ),
        )

    def test_response_audit_owns_request_by_request_status_and_cure(self):
        skill = required_text(
            skill_directory("auditing-section-1983-discovery-responses")
            / "SKILL.md"
        )

        assert_phrases(
            self,
            skill,
            (
                "not produced",
                "claimed nonexistent",
                "withheld",
                "unclear",
            ),
        )
        assert_semantics(
            self,
            skill,
            (
                (
                    "exact request and response",
                    (
                        r"exact.{0,60}request.{0,120}response",
                        r"response.{0,120}exact.{0,60}request",
                    ),
                ),
                (
                    "objection and production",
                    (
                        r"objection.{0,100}production",
                        r"production.{0,100}objection",
                    ),
                ),
                (
                    "deficiency and cure",
                    (r"deficienc.{0,80}cure", r"cure.{0,80}deficienc"),
                ),
                (
                    "silence is not nonexistence",
                    (
                        r"silence.{0,100}(?:not|does\s+not).{0,80}(?:nonexist|exist)",
                        r"(?:do\s+not|must\s+not|does\s+not).{0,50}(?:infer|treat|convert).{0,50}(?:nonexist|existence).{0,80}silence",
                    ),
                ),
                (
                    "silence is not withholding",
                    (
                        r"silence.{0,100}(?:not|does\s+not).{0,80}withheld",
                        r"(?:do\s+not|must\s+not|does\s+not).{0,50}(?:infer|treat|convert).{0,50}(?:withheld|withholding).{0,80}silence",
                    ),
                ),
                (
                    "no waiver conclusion",
                    (
                        r"(?:must|does|shall)\s+not.{0,80}(?:declare|decide|find).{0,30}waiver",
                        r"waiver.{0,80}(?:undecided|plaintiff.{0,30}(?:choice|decision))",
                    ),
                ),
                (
                    "no correspondence drafting",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}draft.{0,60}(?:meet|confer|correspondence)",
                        r"(?:meet|confer|correspondence).{0,100}(?:separate|outside).{0,60}(?:audit|skill|workflow)",
                    ),
                ),
            ),
        )

    def test_meet_and_confer_owns_audit_driven_draft_and_factual_record(self):
        skill = required_text(
            skill_directory("drafting-section-1983-meet-and-confer") / "SKILL.md"
        )

        assert_semantics(
            self,
            skill,
            (
                (
                    "completed audit input",
                    (r"completed.{0,60}audit", r"audit.{0,60}(?:completed|complete)"),
                ),
                (
                    "request-specific deficiency",
                    (
                        r"request.{0,80}(?:exact\s+)?deficienc",
                        r"deficienc.{0,80}request",
                    ),
                ),
                (
                    "approved source and cure",
                    (
                        r"approved.{0,50}(?:rule|order|source).{0,120}cure",
                        r"cure.{0,120}approved.{0,50}(?:rule|order|source)",
                    ),
                ),
                (
                    "date requires user approval",
                    (
                        r"date.{0,100}(?:user.{0,40}(?:suppl|approv)|PLAINTIFF DECISION REQUIRED)",
                        r"user.{0,40}(?:suppl|approv).{0,100}date",
                    ),
                ),
                (
                    "separate factual conference record",
                    (
                        r"separate.{0,80}(?:conference|certification).{0,40}record",
                        r"(?:conference|certification).{0,40}record.{0,80}separate",
                    ),
                ),
                (
                    "silence is not consent",
                    (
                        r"silence.{0,80}(?:not|does\s+not).{0,50}(?:consent|agreement)",
                        r"(?:do\s+not|must\s+not|does\s+not).{0,50}(?:infer|claim|state).{0,50}(?:consent|agreement).{0,80}silence",
                    ),
                ),
                (
                    "no silent narrowing",
                    (
                        r"(?:must|does|shall)\s+not.{0,80}(?:silently\s+)?narrow",
                        r"narrowing.{0,80}(?:plaintiff|user).{0,40}(?:choice|decision)",
                    ),
                ),
                (
                    "no automatic escalation",
                    (
                        r"(?:must|does|shall)\s+not.{0,120}(?:move\s+to\s+compel|fees|sanctions|automatic\s+relief)",
                        r"(?:move\s+to\s+compel|fees|sanctions|automatic\s+relief).{0,120}(?:plaintiff|user).{0,40}(?:choice|decision)",
                    ),
                ),
            ),
        )

    def test_privilege_log_audit_owns_source_bounded_requirements_and_entry_review(self):
        skill = required_text(
            skill_directory("auditing-section-1983-privilege-logs") / "SKILL.md"
        )

        for label, term in (
            ("identifier", r"identifier"),
            ("date", r"date"),
            ("author", r"author"),
            ("recipients", r"recipients?"),
            ("document type", r"document\s+type"),
            ("nonprivileged subject", r"nonprivileged\s+subject"),
            ("asserted privilege or protection", r"asserted.{0,20}(?:privilege|protection)"),
            ("stated basis", r"stated\s+basis"),
            ("custodian", r"custodian"),
            ("family or attachment relationship", r"(?:family|attachment).{0,30}relationship"),
            ("timing", r"timing"),
            ("request relationship", r"request.{0,30}relationship"),
        ):
            assert_positive_requirement(self, skill, label, term)
        assert_semantics(
            self,
            skill,
            (
                (
                    "approved governing sources",
                    (
                        r"approved.{0,80}(?:rule|order|agreement|source)",
                        r"(?:rule|order|agreement|source).{0,80}approved",
                    ),
                ),
                (
                    "requirements before log",
                    (
                        r"(?:before|without|no).{0,80}(?:log).{0,100}requirements?\s+checklist",
                        r"requirements?\s+checklist.{0,100}(?:before|without|no).{0,80}log",
                    ),
                ),
                (
                    "entry-by-entry audit",
                    (r"(?:each|every|line.by.line).{0,60}(?:log\s+)?entr",),
                ),
                ("missing metadata", (r"missing.{0,50}(?:field|metadata)",)),
                (
                    "no generic rule substitution",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}(?:generic|unsupplied).{0,40}(?:court\s+)?rule",
                    ),
                ),
                (
                    "no invented metadata",
                    (
                        r"(?:must|does|shall)\s+not.{0,80}invent.{0,50}(?:fact|field|metadata|entry)",
                        r"(?:use|include|audit).{0,80}only.{0,50}(?:supplied|approved).{0,50}(?:fact|field|metadata|entry)",
                    ),
                ),
                (
                    "no privileged-substance disclosure",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}(?:reveal|expose).{0,50}privileged\s+substance",
                    ),
                ),
                (
                    "no privilege adjudication",
                    (
                        r"(?:must|does|shall)\s+not.{0,80}(?:adjudicate|decide).{0,40}privilege",
                        r"privilege.{0,80}(?:undecided|not.{0,30}adjudicat)",
                    ),
                ),
                (
                    "no waiver declaration",
                    (
                        r"(?:must|does|shall)\s+not.{0,80}(?:declare|decide).{0,30}waiver",
                        r"waiver.{0,80}(?:undecided|plaintiff.{0,30}(?:choice|decision))",
                    ),
                ),
            ),
        )

    def test_deposition_outline_owns_chronology_and_element_gap_questions(self):
        skill = required_text(
            skill_directory("drafting-section-1983-deposition-outlines") / "SKILL.md"
        )

        assert_semantics(
            self,
            skill,
            (
                (
                    "marks foundation needs",
                    (
                        r"(?:must|shall)\s+(?!not\b)(?:mark|flag|identify|include|address).{0,80}foundation",
                        r"(?:outline|output)\s+(?:marks?|flags?|identifies?|includes?|addresses?).{0,80}foundation",
                    ),
                ),
                (
                    "marks authentication needs",
                    (
                        r"(?:must|shall)\s+(?!not\b)(?:mark|flag|identify|include|address).{0,80}authentication",
                        r"(?:outline|output)\s+(?:marks?|flags?|identifies?|includes?|addresses?).{0,80}authentication",
                    ),
                ),
                (
                    "chronology anchors gaps",
                    (
                        r"chronolog.{0,120}(?:anchor|element|gap)",
                        r"(?:element|gap).{0,120}chronolog",
                    ),
                ),
                (
                    "topic identifies element",
                    (r"topic.{0,100}element", r"element.{0,100}topic"),
                ),
                (
                    "topic identifies source",
                    (
                        r"topic.{0,100}(?:source|exhibit|record)",
                        r"(?:source|exhibit|record).{0,100}topic",
                    ),
                ),
                (
                    "topic identifies gap",
                    (r"topic.{0,100}gap", r"gap.{0,100}topic"),
                ),
                (
                    "questions not testimony",
                    (
                        r"question.{0,100}(?:not|distinguish).{0,100}(?:testimony|answer)",
                        r"(?:testimony|answer).{0,100}(?:not|distinguish).{0,100}question",
                    ),
                ),
                (
                    "no scripted answers",
                    (
                        r"(?:must|does|shall)\s+not.{0,80}(?:script|invent|state).{0,50}(?:answer|testimony)",
                    ),
                ),
                (
                    "outstanding document dependency",
                    (
                        r"(?:document|record).{0,80}(?:outstanding|not.{0,20}produced).{0,80}(?:depend|foundation|flag)",
                        r"(?:flag|foundation|depend).{0,100}(?:outstanding|not.{0,20}produced).{0,40}(?:document|record)",
                    ),
                ),
                (
                    "deponent selection reserved",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}(?:choose|decide|select).{0,60}(?:deponent|witness|whom)",
                        r"(?:deponent|witness|whom).{0,100}(?:plaintiff|user).{0,40}(?:choice|decision)",
                    ),
                ),
                (
                    "deposition order reserved",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}(?:order|which.{0,20}first)",
                        r"(?:deposition|witness).{0,40}order.{0,100}(?:plaintiff|user).{0,40}(?:choice|decision)",
                    ),
                ),
                (
                    "whether to depose is reserved",
                    (
                        r"(?:must|does|shall)\s+not.{0,100}(?:whether|decide).{0,60}(?:take|notice|conduct).{0,30}deposition",
                        r"whether.{0,80}(?:take|notice|conduct).{0,30}deposition.{0,100}(?:plaintiff|user).{0,40}choice",
                    ),
                ),
                (
                    "ungrounded topic is reported",
                    (
                        r"(?:missing|no).{0,80}(?:source|exhibit|record|gap).{0,100}(?:report|not.{0,30}(?:draft|ground|support))",
                        r"(?:report|not.{0,30}(?:draft|ground|support)).{0,100}(?:missing|no).{0,80}(?:source|exhibit|record|gap)",
                    ),
                ),
            ),
        )

    def test_peer_markdown_links_are_install_local(self):
        for name in SKILL_NAMES:
            with self.subTest(skill=name):
                directory = skill_directory(name).resolve()
                skill_path = directory / "SKILL.md"
                skill = required_text(skill_path)
                for target in markdown_targets(skill):
                    with self.subTest(skill=name, target=target):
                        parsed = urlsplit(target)
                        self.assertNotEqual(
                            parsed.scheme.casefold(),
                            "file",
                            f"peer link uses a local file URI: {target}",
                        )
                        if parsed.scheme or parsed.netloc or target.startswith("//"):
                            continue
                        local_path = unquote(parsed.path) or skill_path.name
                        relative = Path(local_path)
                        self.assertFalse(relative.is_absolute())
                        resolved = (skill_path.parent / relative).resolve()
                        try:
                            resolved.relative_to(directory)
                        except ValueError as error:
                            self.fail(
                                f"relative peer link leaves installed skill: {target} ({error})"
                            )
                        self.assertTrue(
                            resolved.is_file(),
                            f"relative peer link is missing: {target}",
                        )

    def assert_common_contract_semantics(self, text):
        assert_semantics(
            self,
            text,
            (
                (
                    "stable target identifier",
                    (
                        r"stable.{0,40}target(?:_id|\s+ID)",
                        r"target(?:_id|\s+ID).{0,40}stable",
                    ),
                ),
                (
                    "meaningful nonblank values",
                    (
                        r"(?:meaningful.{0,30})?non[ -]?(?:blank|empty)",
                        r"(?:must|does|shall)\s+not.{0,80}(?:blank|null|empty|placeholder)",
                    ),
                ),
                (
                    "bounded proportionality",
                    (
                        r"bounded.{0,100}proportional",
                        r"proportional.{0,100}bounded",
                    ),
                ),
                (
                    "one row per legal tuple",
                    (
                        r"one.{0,30}(?:map\s+)?row.{0,120}(?:legal\s+)?tuple",
                        r"(?:legal\s+)?tuple.{0,120}one.{0,30}(?:map\s+)?row",
                    ),
                ),
                (
                    "bounded time scope",
                    (
                        r"bounded.{0,100}(?:time|date)",
                        r"(?:time|date).{0,100}bounded",
                    ),
                ),
                (
                    "bounded actor or entity scope",
                    (
                        r"bounded.{0,100}(?:actor|entit)",
                        r"(?:actor|entit).{0,100}bounded",
                    ),
                ),
                (
                    "bounded system or category scope",
                    (
                        r"bounded.{0,100}(?:system|categor)",
                        r"(?:system|categor).{0,100}bounded",
                    ),
                ),
                (
                    "likely custodian is not established",
                    (
                        r"likely(?:_custodian|\s+custodian).{0,120}(?:expect|not.{0,30}establish|unverified)",
                        r"(?:expect|not.{0,30}establish|unverified).{0,120}likely(?:_custodian|\s+custodian)",
                    ),
                ),
                (
                    "expected native source is not established",
                    (
                        r"expected(?:_native_source|\s+native\s+source).{0,120}(?:expect|not.{0,30}establish|unverified)",
                        r"(?:expect|not.{0,30}establish|unverified).{0,120}expected(?:_native_source|\s+native\s+source)",
                    ),
                ),
                (
                    "existence before content",
                    (
                        r"exist(?:s|ence).{0,140}(?:content|identif|conditional)",
                        r"content.{0,140}(?:exist(?:s|ence)|conditional)",
                    ),
                ),
                (
                    "choices and consequences",
                    (
                        r"choices?.{0,80}consequences?",
                        r"consequences?.{0,80}choices?",
                    ),
                ),
                (
                    "selects no strategy",
                    (
                        r"(?:select|choose).{0,50}(?:none|no\s+(?:choice|option|strategy))",
                        r"(?:must|does|shall)\s+not.{0,80}(?:select|choose).{0,80}(?:strategy|option|choice)",
                    ),
                ),
            ),
        )

    def assert_approved_source_identifiers(self, text):
        assert_semantics(
            self,
            text,
            (
                (
                    "approved source identifiers",
                    (
                        r"approved.{0,40}source.{0,20}(?:IDs?|identifiers?)",
                        r"source.{0,20}(?:IDs?|identifiers?).{0,40}approved",
                    ),
                ),
            ),
        )


if __name__ == "__main__":
    unittest.main()
