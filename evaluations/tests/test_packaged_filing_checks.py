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
    }


def tree_hashes(root):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file()
    }


class PackagedFilingChecksTest(unittest.TestCase):
    def test_required_helpers_ship_inside_their_skill_packages(self):
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
        packaged = json.loads(
            (FILING_CI_SKILL / "references" / "packaged-complaint-checker.json").read_text()
        )
        self.assertEqual(packaged, canonical)

    def test_complaint_checker_is_deterministic_limited_and_non_mutating(self):
        checker = load_module("packaged_complaint_checker", COMPLAINT_SCRIPT)
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
            self.assertEqual(first["artifact"], "reports/complaint-mechanical-check.json")
            self.assertIsInstance(first["report_bytes"], bytes)
            self.assertTrue(first["report_bytes"].endswith(b"\n"))
            report = json.loads(first["report_bytes"])
            self.assertEqual(report["excluded_judgments"], contract["excluded_judgments"])
            self.assertEqual(report["checks"], contract["mechanical_checks"])
            self.assertEqual(report["findings"], [])

    def test_complaint_checker_reports_only_declared_mechanical_findings(self):
        checker = load_module("packaged_complaint_checker_findings", COMPLAINT_SCRIPT)
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
        self.assertEqual(finding_checks, set(contract["mechanical_checks"]))
        self.assertTrue(set(contract["excluded_judgments"]).isdisjoint(finding_checks))

    def test_complaint_checker_rejects_unconfined_targets(self):
        checker = load_module("packaged_complaint_checker_paths", COMPLAINT_SCRIPT)
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
        checker = load_module("packaged_complaint_checker_malformed", COMPLAINT_SCRIPT)
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
        filing_ci = load_module("packaged_filing_ci_nested_references", FILING_CI_SCRIPT)
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

    def test_filing_ci_dispatches_only_the_registered_packaged_checker(self):
        filing_ci = load_module("packaged_filing_ci", FILING_CI_SCRIPT)
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
            self.assertEqual(first["artifact"], "reports/filing-ci.json")
            self.assertIsInstance(first["report_bytes"], bytes)
            self.assertEqual(tree_hashes(filing_root), before["filing"])
            self.assertEqual(tree_hashes(authorities_root), before["authorities"])

    def test_filing_ci_returns_stable_unavailable_and_rejects_command_authority(self):
        filing_ci = load_module("packaged_filing_ci_unavailable", FILING_CI_SCRIPT)
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
        filing_ci = load_module("packaged_filing_ci_classes", FILING_CI_SCRIPT)
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
