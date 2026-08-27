import copy
import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
COMPLAINT_SKILL = REPOSITORY / "skills" / "drafting-section-1983-complaints"
FILING_CI_SKILL = REPOSITORY / "skills" / "filing-ci"
COMPLAINT_SCRIPT = COMPLAINT_SKILL / "scripts" / "check_complaint.py"
FILING_CI_SCRIPT = FILING_CI_SKILL / "scripts" / "run_filing_ci.py"
CHECKER_ID = "section-1983-complaint-v1"
COMPLAINT_LIMITATIONS_SCHEMA = (
    COMPLAINT_SKILL / "references" / "limitations-record.schema.json"
)
FILING_CI_LIMITATIONS_SCHEMA = (
    FILING_CI_SKILL / "references" / "limitations-record.schema.json"
)


def empty_limitations_gate():
    return {
        "schema_version": 1,
        "status": "clear",
        "intended_individuals": [],
        "records": [],
        "filing_critical_gaps": [],
    }


def intended_individual(defendant_id="officer-doe", **overrides):
    value = {
        "defendant_id": defendant_id,
        "name_or_role": "Arresting Officer Doe",
        "identity_status": "role-only",
        "amendment_action": "unchanged",
        "deadline_status": "not-passed",
        "risk_raised": False,
    }
    value.update(overrides)
    return value


def complete_analysis(text="Completed from the declared sources."):
    return {
        "status": "complete",
        "analysis": text,
        "source_refs": ["record:identity-source-1"],
    }


def complete_limitations_record(defendant_id="officer-doe"):
    event = {
        "status": "complete",
        "date": "2025-11-03",
        "basis": "The visible badge and roster made the identity ascertainable.",
        "source_refs": ["record:identity-source-1"],
    }
    diligence_entry = {
        "date": "2025-10-01",
        "action": "Requested the arresting-officer identity record.",
        "result": "The request remained pending.",
        "source_refs": ["record:request-1"],
    }
    authority_route = {
        "status": "relied-on",
        "controlling_jurisdiction": "United States Court of Appeals for the Fifth Circuit",
        "governing_authority": "Synthetic controlling authority",
        "pinpoint": "at 12",
        "authority_status": "binding-current",
        "supported_proposition": "Synthetic proposition for structural testing.",
        "defendant_specific_application": "Applied separately to Officer Doe.",
        "source_refs": ["authority:synthetic-1"],
    }
    not_relied_on_route = {
        "status": "not-relied-on",
        "reason": "No supported reliance on this route.",
        "source_refs": ["authority:synthetic-1"],
    }
    return {
        "record_id": f"limitations-{defendant_id}",
        "defendant_id": defendant_id,
        "accrual": {
            "status": "complete",
            "date": "2024-01-15",
            "basis": "The challenged seizure occurred on this date.",
            "source_refs": ["record:arrest-1"],
        },
        "limitations_deadline": {
            "status": "complete",
            "date": "2026-01-15",
            "basis": "Calculated under the identified limitations rule.",
            "source_refs": ["authority:limitations-1"],
        },
        "original_doe_or_role_description": complete_analysis(
            "Arresting Officer Doe was the original role description."
        ),
        "same_transaction_analysis": complete_analysis(
            "The proposed identification concerns the same arrest."
        ),
        "mistake_versus_lack_of_knowledge": complete_analysis(
            "The supplied record supports lack of knowledge, not a mistake."
        ),
        "identity_timeline": {
            "source_first_available": {
                **event,
                "date": "2025-09-01",
                "basis": "The BWC was first available on this date.",
            },
            "source_first_possessed": {
                **event,
                "date": "2025-09-10",
                "basis": "The BWC was first possessed on this date.",
            },
            "objectively_ascertainable": dict(event),
            "actual_identification": {
                **event,
                "date": "2026-01-20",
                "basis": "The badge was matched to the roster after filing.",
                "identification_source": "BWC and personnel roster",
                "identification_method": "Visible-badge comparison",
            },
        },
        "diligence": {
            "pre_limitations": [dict(diligence_entry)],
            "post_filing_pre_identification": [
                {**diligence_entry, "date": "2025-12-05"}
            ],
            "post_identification_pre_service": [
                {**diligence_entry, "date": "2026-01-21"}
            ],
        },
        "record_control_provenance": [
            {
                "record": "Body-worn-camera video",
                "holder_or_controller": "City records custodian",
                "request_recipient": "City public-information office",
                "request_date": "2025-10-01",
                "response_date": "2025-10-10",
                "denial_date": None,
                "follow_up_dates": ["2025-10-20"],
                "stated_basis": "Production remained pending.",
                "source_refs": ["record:request-1"],
                "attribution": {
                    "municipality": complete_analysis("Municipal control is supported."),
                    "custodian": complete_analysis("Custodian possession is supported."),
                    "individual_defendant": complete_analysis(
                        "No individual-defendant withholding is supported."
                    ),
                },
            }
        ],
        "rule_15_c_1_c_notice": {
            "status": "complete",
            "recipient": "Officer Doe",
            "date": None,
            "factual_basis": "No supported notice date was found.",
            "prejudice_analysis": "The prejudice question was analyzed.",
            "knew_or_should_have_known_but_for_mistake_analysis": (
                "The knowledge and mistake question was analyzed separately."
            ),
            "source_refs": ["record:service-1"],
        },
        "service": {
            "status": "complete",
            "service_status": "not-attempted",
            "date": None,
            "method": "None",
            "attempts": "No attempt occurred before identification.",
            "proof": "No proof of service exists.",
            "source_refs": ["record:service-1"],
        },
        "rule_4_m": {
            "status": "complete",
            "deadline": "2026-03-04",
            "extension_request_status": "not-requested",
            "good_cause_facts": "The supported diligence facts were inventoried.",
            "discretionary_extension_facts": "The supported extension facts were inventoried.",
            "requested_relief": "No extension request has yet been authorized.",
            "source_refs": ["record:docket-1"],
        },
        "authority_routes": {
            "limitations": dict(authority_route),
            "rule_15_c_1_a": dict(authority_route),
            "rule_15_c_1_c": dict(authority_route),
            "rule_4_m": dict(authority_route),
            "tolling": dict(not_relied_on_route),
            "concealment": dict(not_relied_on_route),
        },
        "defendant_specific_concealment_or_tolling": complete_analysis(
            "No supported individual-defendant concealment was found."
        ),
        "fallback_claims_and_severable_relief": complete_analysis(
            "The supported fallback and severable relief were identified."
        ),
        "filing_critical_gaps": [],
        "status": "clear",
    }


def load_module(name, path):
    specification = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def complaint_document():
    required_fields = json.loads(
        (
            COMPLAINT_SKILL
            / "references"
            / "complaint-structure-contract.json"
        ).read_text()
    )["required_count_fields"]
    count = {field: f"value-{field}" for field in required_fields}
    count.update(
        {
            "number": 1,
            "count_id": "count-1",
            "claim": "Fourth Amendment false arrest",
            "defendant": "Officer One",
            "challenged_act": "arrest decision",
            "decisive_fact_paragraphs": [1, 2],
            "incorporated_paragraphs": [1, 2],
        }
    )
    return {
        "sections": [
            "caption",
            "introduction",
            "jurisdiction-and-venue",
            "parties",
            "statement-of-facts",
            "counts",
            "prayer-for-relief",
            "jury-demand",
            "signature-block",
        ],
        "paragraphs": [
            {"number": 1, "cross_references": []},
            {"number": 2, "cross_references": [1]},
        ],
        "counts": [count],
        "limitations_gate": empty_limitations_gate(),
    }


def tree_hashes(root):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file()
    }


class InstalledFilingChecksTest(unittest.TestCase):
    def test_required_helpers_ship_inside_their_skill_directories(self):
        self.assertTrue(COMPLAINT_SCRIPT.is_file())
        self.assertTrue(FILING_CI_SCRIPT.is_file())
        for script in (COMPLAINT_SCRIPT, FILING_CI_SCRIPT):
            source = script.read_text()
            self.assertNotIn("scripts.validate_folder_invocation", source)
            self.assertNotIn("scripts.skill_output_writer", source)
            self.assertNotIn("output_root", source)
            self.assertNotIn("subprocess", source)
            self.assertNotIn("urllib", source)
            self.assertNotIn("socket", source)
        canonical = json.loads(
            (
                COMPLAINT_SKILL
                / "references"
                / "complaint-structure-contract.json"
            ).read_text()
        )
        installed = json.loads(
            (FILING_CI_SKILL / "references" / "complaint-checker-contract.json").read_text()
        )
        self.assertEqual(installed, canonical)

    def test_limitations_schemas_ship_aligned_inside_installed_skills(self):
        self.assertTrue(COMPLAINT_LIMITATIONS_SCHEMA.is_file())
        self.assertTrue(FILING_CI_LIMITATIONS_SCHEMA.is_file())
        self.assertEqual(
            COMPLAINT_LIMITATIONS_SCHEMA.read_bytes(),
            FILING_CI_LIMITATIONS_SCHEMA.read_bytes(),
        )

    def test_complaint_checker_requires_limitations_gate(self):
        checker = load_module("installed_complaint_checker_gate", COMPLAINT_SCRIPT)
        document = complaint_document()
        document.pop("limitations_gate")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "complaint.json").write_text(json.dumps(document))
            result = checker.check_complaint(root, "complaint.json")

        self.assertEqual(result["status"], "failed")
        self.assertIn(
            "limitations-gate-presence",
            {finding["check_id"] for finding in result["findings"]},
        )

    def test_role_only_intended_defendant_requires_matching_record(self):
        checker = load_module("installed_complaint_checker_role_only", COMPLAINT_SCRIPT)
        document = complaint_document()
        document["limitations_gate"]["intended_individuals"] = [
            intended_individual()
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "complaint.json").write_text(json.dumps(document))
            result = checker.check_complaint(root, "complaint.json")

        self.assertEqual(result["status"], "failed")
        self.assertIn(
            "limitations-record-cardinality",
            {finding["check_id"] for finding in result["findings"]},
        )

    def test_limitations_identity_events_are_separate_and_fail_closed(self):
        checker = load_module("installed_complaint_checker_identity_events", COMPLAINT_SCRIPT)
        document = complaint_document()
        record = complete_limitations_record()
        record["identity_timeline"].pop("source_first_possessed")
        document["limitations_gate"] = {
            "schema_version": 1,
            "status": "clear",
            "intended_individuals": [intended_individual()],
            "records": [record],
            "filing_critical_gaps": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "complaint.json").write_text(json.dumps(document))
            result = checker.check_complaint(root, "complaint.json")

        checks = {finding["check_id"] for finding in result["findings"]}
        self.assertEqual(result["status"], "failed")
        self.assertIn("limitations-record-structure", checks)
        self.assertIn("limitations-filing-critical-status", checks)

    def test_complete_supported_adverse_record_does_not_create_legal_judgment(self):
        checker = load_module("installed_complaint_checker_complete_limitations", COMPLAINT_SCRIPT)
        document = complaint_document()
        document["limitations_gate"] = {
            "schema_version": 1,
            "status": "clear",
            "intended_individuals": [intended_individual()],
            "records": [complete_limitations_record()],
            "filing_critical_gaps": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "complaint.json").write_text(json.dumps(document))
            result = checker.check_complaint(root, "complaint.json")

        self.assertEqual(result["status"], "passed")
        report = json.loads(result["report_bytes"])
        self.assertTrue(
            {
                "relation-back",
                "tolling",
                "mistake",
                "notice-sufficiency",
                "service-sufficiency",
            }.issubset(set(report["excluded_judgments"]))
        )

    def test_filing_ci_preserves_limitations_record_findings(self):
        filing_ci = load_module("installed_filing_ci_limitations", FILING_CI_SCRIPT)
        document = complaint_document()
        document["limitations_gate"]["intended_individuals"] = [
            intended_individual()
        ]
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            filing_root = base / "filing"
            authorities_root = base / "authorities"
            filing_root.mkdir()
            authorities_root.mkdir()
            (filing_root / "complaint.json").write_text(json.dumps(document))
            result = filing_ci.run_filing_ci(
                filing_root,
                "complaint.json",
                authorities_root,
                CHECKER_ID,
            )

        self.assertEqual(result["status"], "failed")
        self.assertIn(
            "limitations-record-cardinality",
            {finding["check_id"] for finding in result["findings"]},
        )

    def test_complaint_checker_is_deterministic_limited_and_non_mutating(self):
        checker = load_module("installed_complaint_checker", COMPLAINT_SCRIPT)
        contract = json.loads(
            (
                COMPLAINT_SKILL
                / "references"
                / "complaint-structure-contract.json"
            ).read_text()
        )
        with tempfile.TemporaryDirectory() as directory:
            filing_root = Path(directory)
            target = filing_root / "complaint.json"
            target.write_text(json.dumps(complaint_document()))
            before = tree_hashes(filing_root)
            first = checker.check_complaint(filing_root, "complaint.json")
            second = checker.check_complaint(filing_root, "complaint.json")

            self.assertEqual(first, second)
            self.assertEqual(tree_hashes(filing_root), before)
            self.assertEqual(first["status"], "passed")
            self.assertEqual(first["exit_status"], 0)
            self.assertNotIn("artifact", first)
            self.assertIsInstance(first["report_bytes"], bytes)
            self.assertTrue(first["report_bytes"].endswith(b"\n"))
            report = json.loads(first["report_bytes"])
            self.assertEqual(report["excluded_judgments"], contract["excluded_judgments"])
            self.assertEqual(report["checks"], contract["mechanical_checks"])
            self.assertEqual(report["findings"], [])

    def test_complaint_checker_reports_only_declared_mechanical_findings(self):
        checker = load_module("installed_complaint_checker_findings", COMPLAINT_SCRIPT)
        contract = json.loads(
            (
                COMPLAINT_SKILL
                / "references"
                / "complaint-structure-contract.json"
            ).read_text()
        )
        document = complaint_document()
        document["sections"].remove("jury-demand")
        document["sections"][2], document["sections"][3] = (
            document["sections"][3],
            document["sections"][2],
        )
        document["paragraphs"][1]["number"] = 3
        document["paragraphs"][1]["cross_references"] = [99]
        duplicate_count = copy.deepcopy(document["counts"][0])
        document["counts"][0]["number"] = 2
        duplicate_count["number"] = 4
        duplicate_count["incorporated_paragraphs"] = [99]
        document["counts"].append(duplicate_count)
        document["counts"][0].pop("injury")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "complaint.json").write_text(json.dumps(document))
            result = checker.check_complaint(root, "complaint.json")

        self.assertEqual(result["status"], "failed")
        self.assertNotEqual(result["exit_status"], 0)
        finding_checks = {finding["check_id"] for finding in result["findings"]}
        self.assertEqual(
            finding_checks,
            set(contract["mechanical_checks"])
            - {
                "limitations-gate-presence",
                "limitations-trigger-structure",
                "limitations-record-cardinality",
                "limitations-record-structure",
                "limitations-filing-critical-status",
            },
        )
        self.assertTrue(set(contract["excluded_judgments"]).isdisjoint(finding_checks))

    def test_complaint_checker_rejects_unconfined_targets(self):
        checker = load_module("installed_complaint_checker_paths", COMPLAINT_SCRIPT)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            outside = root.parent / f"{root.name}-outside-complaint.json"
            outside.write_text(json.dumps(complaint_document()))
            try:
                for target in (str(outside), "../outside-complaint.json", "folder//file.json"):
                    with self.subTest(target=target):
                        with self.assertRaises(checker.ComplaintCheckError) as captured:
                            checker.check_complaint(root, target)
                        self.assertEqual(captured.exception.finding_id, "invalid-target")
            finally:
                outside.unlink()

    def test_complaint_checker_bounds_malformed_bytes_and_structures(self):
        checker = load_module("installed_complaint_checker_malformed", COMPLAINT_SCRIPT)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "malformed.json").write_text("not json\n")
            with self.assertRaises(checker.ComplaintCheckError) as captured:
                checker.check_complaint(root, "malformed.json")
            self.assertEqual(captured.exception.finding_id, "malformed-input")

            document = complaint_document()
            document["counts"][0]["claim"] = ["not", "scalar"]
            (root / "invalid-structure.json").write_text(json.dumps(document))
            result = checker.check_complaint(root, "invalid-structure.json")
            self.assertEqual(result["status"], "failed")
            self.assertIn(
                "claim-defendant-challenged-act-cardinality",
                {finding["check_id"] for finding in result["findings"]},
            )

            document = complaint_document()
            document["paragraphs"][1]["cross_references"] = [[]]
            document["counts"][0]["incorporated_paragraphs"] = [{}]
            (root / "nested-references.json").write_text(json.dumps(document))
            result = checker.check_complaint(root, "nested-references.json")
            self.assertEqual(result["status"], "failed")
            self.assertTrue(
                {
                    "cross-reference-target",
                    "incorporation-target",
                }.issubset({finding["check_id"] for finding in result["findings"]})
            )

            outside = root.parent / f"{root.name}-symlink-target.json"
            outside.write_text(json.dumps(complaint_document()))
            try:
                (root / "linked.json").symlink_to(outside)
                with self.assertRaises(checker.ComplaintCheckError) as captured:
                    checker.check_complaint(root, "linked.json")
                self.assertEqual(captured.exception.finding_id, "invalid-target")
            finally:
                outside.unlink()

    def test_filing_ci_bounds_nested_reference_values(self):
        filing_ci = load_module("installed_filing_ci_nested_references", FILING_CI_SCRIPT)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            filing_root = base / "filing"
            authorities_root = base / "authorities"
            filing_root.mkdir()
            authorities_root.mkdir()
            document = complaint_document()
            document["paragraphs"][1]["cross_references"] = [[]]
            document["counts"][0]["incorporated_paragraphs"] = [{}]
            (filing_root / "complaint.json").write_text(json.dumps(document))

            result = filing_ci.run_filing_ci(
                filing_root,
                "complaint.json",
                authorities_root,
                CHECKER_ID,
            )

        self.assertEqual(result["status"], "failed")
        self.assertTrue(
            {
                "cross-reference-target",
                "incorporation-target",
            }.issubset({finding["check_id"] for finding in result["findings"]})
        )

    def test_filing_ci_dispatches_only_the_registered_installed_checker(self):
        filing_ci = load_module("installed_filing_ci", FILING_CI_SCRIPT)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            filing_root = base / "filing"
            authorities_root = base / "authorities"
            filing_root.mkdir()
            authorities_root.mkdir()
            (filing_root / "complaint.json").write_text(json.dumps(complaint_document()))
            (authorities_root / "README.md").write_text("Synthetic verified authority root.\n")
            before = {"filing": tree_hashes(filing_root), "authorities": tree_hashes(authorities_root)}
            first = filing_ci.run_filing_ci(
                filing_root,
                "complaint.json",
                authorities_root,
                CHECKER_ID,
            )
            second = filing_ci.run_filing_ci(
                filing_root,
                "complaint.json",
                authorities_root,
                CHECKER_ID,
            )

            self.assertEqual(first, second)
            self.assertEqual(first["status"], "passed")
            self.assertEqual(first["checker_id"], CHECKER_ID)
            self.assertNotIn("artifact", first)
            self.assertIsInstance(first["report_bytes"], bytes)
            self.assertEqual(tree_hashes(filing_root), before["filing"])
            self.assertEqual(tree_hashes(authorities_root), before["authorities"])

    def test_filing_ci_returns_stable_unavailable_and_rejects_command_authority(self):
        filing_ci = load_module("installed_filing_ci_unavailable", FILING_CI_SCRIPT)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            filing_root = base / "filing"
            authorities_root = base / "authorities"
            filing_root.mkdir()
            authorities_root.mkdir()
            (filing_root / "complaint.json").write_text(json.dumps(complaint_document()))
            first = filing_ci.run_filing_ci(
                filing_root,
                "complaint.json",
                authorities_root,
                "unknown-checker",
            )
            second = filing_ci.run_filing_ci(
                filing_root,
                "complaint.json",
                authorities_root,
                "unknown-checker",
            )

            self.assertEqual(first, second)
            self.assertEqual(first["status"], "unavailable")
            self.assertEqual(first["reason"], "checker-unavailable")
            self.assertEqual(first["checker_id"], "unknown-checker")
            self.assertIsInstance(first["report_bytes"], bytes)
            for forbidden in (
                {"command": ["checker"]},
                {"executable": "/tmp/checker"},
                {"output_root": base / "output"},
            ):
                with self.subTest(forbidden=forbidden):
                    with self.assertRaises(TypeError):
                        filing_ci.run_filing_ci(
                            filing_root,
                            "complaint.json",
                            authorities_root,
                            CHECKER_ID,
                            **forbidden,
                        )

    def test_filing_ci_distinguishes_fail_closed_unavailable_classes(self):
        filing_ci = load_module("installed_filing_ci_classes", FILING_CI_SCRIPT)
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            filing_root = base / "filing"
            authorities_root = base / "authorities"
            filing_root.mkdir()
            authorities_root.mkdir()
            (filing_root / "complaint.json").write_text("not json\n")
            (filing_root / "complaint.md").write_text("{}\n")

            cases = (
                ("../outside.json", authorities_root, "invalid-target"),
                ("complaint.md", authorities_root, "checker-incompatible"),
                ("complaint.json", authorities_root, "malformed-input"),
                ("complaint.json", base / "missing-authorities", "unresolved-input"),
            )
            for target, authority_root, reason in cases:
                with self.subTest(reason=reason):
                    result = filing_ci.run_filing_ci(
                        filing_root,
                        target,
                        authority_root,
                        CHECKER_ID,
                    )
                    self.assertEqual(result["status"], "unavailable")
                    self.assertEqual(result["reason"], reason)

    def test_helpers_execute_from_isolated_skill_copies(self):
        with tempfile.TemporaryDirectory() as directory:
            install = Path(directory)
            complaint_copy = install / "complaint-skill"
            filing_ci_copy = install / "filing-ci-skill"
            shutil.copytree(COMPLAINT_SKILL, complaint_copy)
            shutil.copytree(FILING_CI_SKILL, filing_ci_copy)
            complaint = load_module(
                "isolated_complaint_checker", complaint_copy / "scripts" / "check_complaint.py"
            )
            filing_ci = load_module(
                "isolated_filing_ci", filing_ci_copy / "scripts" / "run_filing_ci.py"
            )
            filing_root = install / "filing"
            authorities_root = install / "authorities"
            filing_root.mkdir()
            authorities_root.mkdir()
            (filing_root / "complaint.json").write_text(json.dumps(complaint_document()))

            self.assertEqual(
                complaint.check_complaint(filing_root, "complaint.json")["status"],
                "passed",
            )
            self.assertEqual(
                filing_ci.run_filing_ci(
                    filing_root,
                    "complaint.json",
                    authorities_root,
                    CHECKER_ID,
                )["status"],
                "passed",
            )


if __name__ == "__main__":
    unittest.main()
