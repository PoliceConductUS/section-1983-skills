import copy
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
import uuid
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL = REPOSITORY / "skills" / "building-litigation-alignment-overlays"
VALIDATOR = SKILL / "scripts" / "validate_overlays.py"
FIXTURES = SKILL / "references" / "fixtures"


def canonical_sha256(value):
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def text_sha256(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source(source_id, docket_entry, family, actors, content, filed_date):
    return {
        "source_id": source_id,
        "docket_entry": docket_entry,
        "filed_date": filed_date,
        "document_family": family,
        "filed_by_actor_ids": actors,
        "content": content,
        "sha256": text_sha256(content),
    }


def complete_snapshot():
    sources = [
        source(
            "SRC-COMPLAINT",
            "1",
            "complaint",
            ["ACT-PLAINTIFF"],
            "Synthetic complaint against Officer Alpha, Officer Beta, and Example City.",
            "2026-01-02",
        ),
        source(
            "SRC-MOTION",
            "8",
            "motion-to-dismiss",
            ["ACT-ALPHA", "ACT-BETA", "ACT-CITY"],
            "Alpha raises qualified immunity. Beta disputes personal participation. Example City attacks policy causation.",
            "2026-01-10",
        ),
        source(
            "SRC-LEAVE",
            "12",
            "leave-to-amend-motion",
            ["ACT-PLAINTIFF"],
            "Plaintiff requests leave to amend the synthetic complaint.",
            "2026-01-14",
        ),
        source(
            "SRC-FAC",
            "12-1",
            "proposed-amended-complaint",
            ["ACT-PLAINTIFF"],
            "The proposed amended complaint separately alleges each synthetic challenged act.",
            "2026-01-14",
        ),
        source(
            "SRC-RECOMMENDATION",
            "18",
            "magistrate-recommendation",
            ["ACT-MAGISTRATE"],
            "The magistrate judge recommends granting Alpha's first attack.",
            "2026-01-18",
        ),
        source(
            "SRC-ORDER",
            "20",
            "district-order",
            ["ACT-DISTRICT"],
            "The district judge adopts the recommendation without additional reasoning.",
            "2026-01-20",
        ),
    ]
    return {
        "schema_version": "1.0",
        "snapshot_id": "SNAP-COMPLETE",
        "version": "v1",
        "checked_through": "2026-01-20",
        "actors": [
            {
                "actor_id": "ACT-PLAINTIFF",
                "actor_type": "plaintiff",
                "display_label": "Plaintiff Example",
            },
            {
                "actor_id": "ACT-ALPHA",
                "actor_type": "individual-defendant",
                "display_label": "Officer Alpha",
            },
            {
                "actor_id": "ACT-BETA",
                "actor_type": "individual-defendant",
                "display_label": "Officer Beta",
            },
            {
                "actor_id": "ACT-CITY",
                "actor_type": "municipality-defendant",
                "display_label": "Example City",
            },
            {
                "actor_id": "ACT-MAGISTRATE",
                "actor_type": "magistrate-judge",
                "display_label": "Magistrate Judge Example",
            },
            {
                "actor_id": "ACT-DISTRICT",
                "actor_type": "district-judge",
                "display_label": "District Judge Example",
            },
        ],
        "sources": sources,
    }


def initial_snapshot():
    snapshot = complete_snapshot()
    snapshot["snapshot_id"] = "SNAP-INITIAL"
    snapshot["checked_through"] = "2026-01-02"
    snapshot["sources"] = [snapshot["sources"][0]]
    return snapshot


def dimension(
    issue_id,
    claim_id,
    capacity,
    challenged_act,
    knowledge,
    qi_position,
    relief,
    defense,
):
    return {
        "issue_id": issue_id,
        "claim_id": claim_id,
        "capacity": capacity,
        "challenged_act_id": challenged_act,
        "relevant_time_knowledge_position": knowledge,
        "qualified_immunity_position": qi_position,
        "requested_relief": relief,
        "other_material_defense": defense,
    }


def defendant(defendant_id, defendant_type, label, source_ids, dimensions):
    return {
        "defendant_id": defendant_id,
        "defendant_type": defendant_type,
        "display_label": label,
        "source_ids": source_ids,
        "dimensions": dimensions,
    }


def group(group_id, defendant_id, source_ids, mixed=False):
    return {
        "group_id": group_id,
        "issue_id": "ISSUE-1",
        "member_defendant_ids": [defendant_id],
        "mixed_municipal_alignment_established": mixed,
        "source_ids": source_ids,
        "basis": "The approved synthetic docket states this issue-specific position.",
        "uncertainty": None,
    }


def location(source_id, docket_entry, quote):
    return {
        "source_id": source_id,
        "docket_entry": docket_entry,
        "page": "1",
        "heading": "Synthetic ground",
        "quote": quote,
    }


def attack(attack_id, group_id, defendant_id, claim_id, act_id, defense, quote):
    return {
        "attack_id": attack_id,
        "source_ids": ["SRC-MOTION"],
        "source_location": location("SRC-MOTION", "8", quote),
        "date": "2026-01-10",
        "group_id": group_id,
        "claim_id": claim_id,
        "defendant_ids": [defendant_id],
        "challenged_act_id": act_id,
        "element_or_defense": defense,
        "qualified_immunity_prong": (
            "prong-one"
            if defendant_id == "DEF-ALPHA"
            else "prong-two" if defendant_id == "DEF-BETA" else None
        ),
        "requested_disposition": "dismiss the claim",
        "status": "adversary-asserted",
    }


def response():
    return {
        "response_id": "RESP-ALPHA",
        "attack_id": "ATK-ALPHA",
        "source_ids": ["SRC-LEAVE", "SRC-FAC"],
        "source_location": location(
            "SRC-LEAVE",
            "12",
            "Plaintiff requests leave to amend the synthetic complaint.",
        ),
        "date": "2026-01-14",
        "coverage": "plaintiff-answered",
        "coverage_explanation": "The motion and proposed amendment address the attack.",
    }


def treatments():
    return [
        {
            "treatment_id": "TREAT-MAG",
            "attack_id": "ATK-ALPHA",
            "response_ids": ["RESP-ALPHA"],
            "judicial_actor_id": "ACT-MAGISTRATE",
            "judicial_actor_role": "magistrate-judge",
            "source_ids": ["SRC-RECOMMENDATION"],
            "source_location": location(
                "SRC-RECOMMENDATION",
                "18",
                "The magistrate judge recommends granting Alpha's first attack.",
            ),
            "date": "2026-01-18",
            "treatment": "magistrate-judge-recommended-grant",
            "reasoning_type": "recommendation",
            "related_treatment_ids": [],
            "status": "current",
        },
        {
            "treatment_id": "TREAT-DISTRICT",
            "attack_id": "ATK-ALPHA",
            "response_ids": ["RESP-ALPHA"],
            "judicial_actor_id": "ACT-DISTRICT",
            "judicial_actor_role": "district-judge",
            "source_ids": ["SRC-ORDER"],
            "source_location": location(
                "SRC-ORDER",
                "20",
                "The district judge adopts the recommendation without additional reasoning.",
            ),
            "date": "2026-01-20",
            "treatment": "district-judge-adopted",
            "reasoning_type": "adoption-without-independent-reasoning",
            "related_treatment_ids": ["TREAT-MAG"],
            "status": "current",
        },
    ]


def review_jobs(groups, attacks, target, available=True):
    jobs = []
    counter = 1
    for group_value in groups:
        group_id = group_value["group_id"]
        matching = [item for item in attacks if item["group_id"] == group_id]
        kinds = (
            ("blind-common-attack", []),
            ("actual-adversary", [item["attack_id"] for item in matching]),
        )
        if not available:
            kinds = (("blind-common-attack", []), ("blind-common-attack", []))
        for kind, attack_ids in kinds:
            source_ids = [target["source_id"]]
            if kind == "actual-adversary":
                source_ids.extend(
                    sorted(
                        {
                            source_id
                            for item in matching
                            for source_id in item["source_ids"]
                        }
                    )
                )
            jobs.append(
                {
                    "job_id": f"JOB-{counter}",
                    "run_id": f"00000000-0000-4000-8000-{counter:012d}",
                    "target_artifact_id": target["artifact_id"],
                    "target_sha256": target["sha256"],
                    "group_id": group_id,
                    "review_kind": kind,
                    "attack_ids": attack_ids,
                    "source_ids": source_ids,
                    "prior_review_ids": [],
                }
            )
            counter += 1
    return jobs


def update_ledger_fingerprints(overlay):
    overlay["ledger_fingerprints"] = {
        name: canonical_sha256(value) for name, value in overlay["ledgers"].items()
    }


def complete_overlay(snapshot=None):
    snapshot = snapshot or complete_snapshot()
    defendants = [
        defendant(
            "DEF-ALPHA",
            "individual",
            "Officer Alpha",
            ["SRC-COMPLAINT", "SRC-MOTION"],
            [
                dimension(
                    "ISSUE-1",
                    "CLAIM-1",
                    "individual",
                    "ACT-ALPHA-1",
                    "knowledge-disputed",
                    "qualified-immunity-prong-one",
                    "dismissal",
                    "none",
                )
            ],
        ),
        defendant(
            "DEF-BETA",
            "individual",
            "Officer Beta",
            ["SRC-COMPLAINT", "SRC-MOTION"],
            [
                dimension(
                    "ISSUE-1",
                    "CLAIM-1",
                    "individual",
                    "ACT-BETA-1",
                    "personal-participation-disputed",
                    "qualified-immunity-prong-two",
                    "dismissal",
                    "personal-participation",
                )
            ],
        ),
        defendant(
            "DEF-CITY",
            "municipality",
            "Example City",
            ["SRC-COMPLAINT", "SRC-MOTION"],
            [
                dimension(
                    "ISSUE-1",
                    "CLAIM-MONELL",
                    "official",
                    "ACT-POLICY-1",
                    "notice-disputed",
                    "not-applicable",
                    "dismissal",
                    "moving-force",
                )
            ],
        ),
    ]
    groups = [
        group("GROUP-ALPHA", "DEF-ALPHA", ["SRC-MOTION"]),
        group("GROUP-BETA", "DEF-BETA", ["SRC-MOTION"]),
        group("GROUP-CITY", "DEF-CITY", ["SRC-MOTION"]),
    ]
    attacks = [
        attack(
            "ATK-ALPHA",
            "GROUP-ALPHA",
            "DEF-ALPHA",
            "CLAIM-1",
            "ACT-ALPHA-1",
            "qualified immunity",
            "Alpha raises qualified immunity.",
        ),
        attack(
            "ATK-BETA",
            "GROUP-BETA",
            "DEF-BETA",
            "CLAIM-1",
            "ACT-BETA-1",
            "personal participation",
            "Beta disputes personal participation.",
        ),
        attack(
            "ATK-CITY",
            "GROUP-CITY",
            "DEF-CITY",
            "CLAIM-MONELL",
            "ACT-POLICY-1",
            "moving force",
            "Example City attacks policy causation.",
        ),
    ]
    response_records = [response()]
    treatment_records = treatments()
    ledgers = {
        "adversary_attacks": {
            "ledger_id": "LEDGER-ATTACKS",
            "version": "v1",
            "records": attacks,
        },
        "plaintiff_responses": {
            "ledger_id": "LEDGER-RESPONSES",
            "version": "v1",
            "records": response_records,
        },
        "judicial_treatments": {
            "ledger_id": "LEDGER-TREATMENTS",
            "version": "v1",
            "records": treatment_records,
        },
    }
    matrices = [
        {
            "row_id": "ROW-ALPHA",
            "attack_id": "ATK-ALPHA",
            "response_ids": ["RESP-ALPHA"],
            "treatment_ids": ["TREAT-MAG", "TREAT-DISTRICT"],
            "response_state": "plaintiff-answered",
            "judicial_state": "district-judge-adopted",
            "current_procedural_status": "district disposition entered",
            "current_status_source_ids": ["SRC-ORDER"],
            "source_ids": [
                "SRC-FAC",
                "SRC-LEAVE",
                "SRC-MOTION",
                "SRC-ORDER",
                "SRC-RECOMMENDATION",
            ],
        },
        {
            "row_id": "ROW-BETA",
            "attack_id": "ATK-BETA",
            "response_ids": [],
            "treatment_ids": [],
            "response_state": "plaintiff-response-unavailable",
            "judicial_state": "judicial-treatment-unavailable",
            "current_procedural_status": "attack pending on supplied record",
            "current_status_source_ids": ["SRC-MOTION"],
            "source_ids": ["SRC-MOTION"],
        },
        {
            "row_id": "ROW-CITY",
            "attack_id": "ATK-CITY",
            "response_ids": [],
            "treatment_ids": [],
            "response_state": "plaintiff-response-unavailable",
            "judicial_state": "judicial-treatment-unavailable",
            "current_procedural_status": "attack pending on supplied record",
            "current_status_source_ids": ["SRC-MOTION"],
            "source_ids": ["SRC-MOTION"],
        },
    ]
    fac_source = next(
        item for item in snapshot["sources"] if item["source_id"] == "SRC-FAC"
    )
    target = {
        "artifact_id": "TARGET-FAC",
        "source_id": "SRC-FAC",
        "sha256": fac_source["sha256"],
        "document_family": "proposed-amended-complaint",
    }
    overlay = {
        "schema_version": "1.0",
        "overlay_id": "OVERLAY-COMPLETE",
        "version": "v1",
        "generated_at": "2026-01-20T12:00:00Z",
        "source_snapshot": {
            "snapshot_id": snapshot["snapshot_id"],
            "version": snapshot["version"],
            "sha256": canonical_sha256(snapshot),
            "checked_through": snapshot["checked_through"],
        },
        "previous_version_id": None,
        "invalidation_events": [],
        "defendants": defendants,
        "generated_groups": copy.deepcopy(groups),
        "overrides": [],
        "effective_groups": copy.deepcopy(groups),
        "ledgers": ledgers,
        "ledger_fingerprints": {},
        "issue_matrix": matrices,
        "review_plan": {
            "actual_profile_status": "available",
            "targets": [target],
            "jobs": review_jobs(groups, attacks, target),
        },
    }
    update_ledger_fingerprints(overlay)
    return overlay


def no_responsive_overlay(snapshot=None):
    snapshot = snapshot or initial_snapshot()
    overlay = complete_overlay(complete_snapshot())
    overlay["overlay_id"] = "OVERLAY-INITIAL"
    overlay["source_snapshot"] = {
        "snapshot_id": snapshot["snapshot_id"],
        "version": snapshot["version"],
        "sha256": canonical_sha256(snapshot),
        "checked_through": snapshot["checked_through"],
    }
    for defendant_value in overlay["defendants"]:
        defendant_value["source_ids"] = ["SRC-COMPLAINT"]
    for group_value in overlay["generated_groups"] + overlay["effective_groups"]:
        group_value["source_ids"] = ["SRC-COMPLAINT"]
    overlay["ledgers"]["adversary_attacks"]["records"] = []
    overlay["ledgers"]["plaintiff_responses"]["records"] = []
    overlay["ledgers"]["judicial_treatments"]["records"] = []
    overlay["issue_matrix"] = []
    complaint = snapshot["sources"][0]
    target = {
        "artifact_id": "TARGET-COMPLAINT",
        "source_id": complaint["source_id"],
        "sha256": complaint["sha256"],
        "document_family": "complaint",
    }
    overlay["review_plan"] = {
        "actual_profile_status": "actual-adversary-unavailable",
        "targets": [target],
        "jobs": review_jobs(
            overlay["effective_groups"],
            [],
            target,
            available=False,
        ),
    }
    update_ledger_fingerprints(overlay)
    return overlay


def complete_manifest(snapshot=None, overlay=None):
    snapshot = snapshot or complete_snapshot()
    overlay = overlay or complete_overlay(snapshot)
    fac = next(item for item in snapshot["sources"] if item["source_id"] == "SRC-FAC")
    return {
        "schema_version": "1.0",
        "filing_version_id": "FILING-V1",
        "artifact_id": "TARGET-FAC",
        "artifact_sha256": fac["sha256"],
        "source_snapshot": copy.deepcopy(overlay["source_snapshot"]),
        "overlays": [
            {
                "kind": "litigation-alignment",
                "overlay_id": overlay["overlay_id"],
                "version": overlay["version"],
                "sha256": canonical_sha256(overlay),
                "checked_through": overlay["source_snapshot"]["checked_through"],
                "validator_result": "passed",
                "source_snapshot_id": snapshot["snapshot_id"],
                "source_snapshot_version": snapshot["version"],
                "source_snapshot_sha256": canonical_sha256(snapshot),
            }
        ],
    }


def add_appellate_stage(snapshot, overlay):
    snapshot["actors"].append(
        {
            "actor_id": "ACT-APPELLATE",
            "actor_type": "appellate-court",
            "display_label": "Example Court of Appeals",
        }
    )
    appellate_source = source(
        "SRC-APPELLATE",
        "24",
        "appellate-disposition",
        ["ACT-APPELLATE"],
        "The appellate court affirms the district disposition.",
        "2026-02-01",
    )
    snapshot["sources"].append(appellate_source)
    snapshot["checked_through"] = "2026-02-01"
    overlay["source_snapshot"] = {
        "snapshot_id": snapshot["snapshot_id"],
        "version": snapshot["version"],
        "sha256": canonical_sha256(snapshot),
        "checked_through": snapshot["checked_through"],
    }
    overlay["ledgers"]["judicial_treatments"]["records"].append(
        {
            "treatment_id": "TREAT-APPELLATE",
            "attack_id": "ATK-ALPHA",
            "response_ids": ["RESP-ALPHA"],
            "judicial_actor_id": "ACT-APPELLATE",
            "judicial_actor_role": "appellate-court",
            "source_ids": ["SRC-APPELLATE"],
            "source_location": location(
                "SRC-APPELLATE",
                "24",
                "The appellate court affirms the district disposition.",
            ),
            "date": "2026-02-01",
            "treatment": "appellate-court-affirmed",
            "reasoning_type": "appellate-disposition",
            "related_treatment_ids": ["TREAT-DISTRICT"],
            "status": "current",
        }
    )
    row = overlay["issue_matrix"][0]
    row["treatment_ids"].append("TREAT-APPELLATE")
    row["judicial_state"] = "appellate-court-affirmed"
    row["current_procedural_status"] = "appellate disposition entered"
    row["current_status_source_ids"] = ["SRC-APPELLATE"]
    row["source_ids"].append("SRC-APPELLATE")
    row["source_ids"].sort()
    update_ledger_fingerprints(overlay)


def load_validator():
    if not VALIDATOR.is_file():
        raise AssertionError(
            f"missing validator: {VALIDATOR.relative_to(REPOSITORY)}"
        )
    specification = importlib.util.spec_from_file_location(
        f"overlay_validator_{uuid.uuid4().hex}", VALIDATOR
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def finding_ids(findings):
    return {finding["id"] for finding in findings}


class LitigationAlignmentOverlayValidatorTest(unittest.TestCase):
    def test_complete_and_no_responsive_lifecycles_validate(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        manifest = complete_manifest(snapshot, overlay)
        self.assertEqual(validator.validate_snapshot(snapshot), [])
        self.assertEqual(validator.validate_overlay(overlay, snapshot), [])
        self.assertEqual(
            validator.validate_filing_manifest(manifest, overlay, snapshot), []
        )
        initial = initial_snapshot()
        self.assertEqual(validator.validate_snapshot(initial), [])
        self.assertEqual(
            validator.validate_overlay(no_responsive_overlay(initial), initial), []
        )

    def test_required_root_and_record_structures_are_enforced(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        manifest = complete_manifest(snapshot, overlay)

        missing_snapshot = copy.deepcopy(snapshot)
        missing_snapshot.pop("actors")
        self.assertIn(
            "snapshot-structure-invalid",
            finding_ids(validator.validate_snapshot(missing_snapshot)),
        )

        missing_overlay = copy.deepcopy(overlay)
        missing_overlay.pop("defendants")
        self.assertIn(
            "overlay-structure-invalid",
            finding_ids(validator.validate_overlay(missing_overlay, snapshot)),
        )

        missing_attack_field = copy.deepcopy(overlay)
        missing_attack_field["ledgers"]["adversary_attacks"]["records"][0].pop(
            "date"
        )
        update_ledger_fingerprints(missing_attack_field)
        self.assertIn(
            "attack-structure-invalid",
            finding_ids(validator.validate_overlay(missing_attack_field, snapshot)),
        )

        missing_manifest = copy.deepcopy(manifest)
        missing_manifest.pop("overlays")
        self.assertIn(
            "manifest-structure-invalid",
            finding_ids(
                validator.validate_filing_manifest(
                    missing_manifest, overlay, snapshot
                )
            ),
        )

    def test_nested_wrong_json_types_fail_closed_with_stable_findings(self):
        validator = load_validator()

        invalid_actor = complete_snapshot()
        invalid_actor["actors"][0]["actor_type"] = []
        self.assertIn(
            "snapshot-structure-invalid",
            finding_ids(validator.validate_snapshot(invalid_actor)),
        )

        snapshot = complete_snapshot()
        invalid_attack = complete_overlay(snapshot)
        invalid_attack["ledgers"]["adversary_attacks"]["records"][0][
            "group_id"
        ] = []
        update_ledger_fingerprints(invalid_attack)
        self.assertIn(
            "attack-structure-invalid",
            finding_ids(validator.validate_overlay(invalid_attack, snapshot)),
        )

        invalid_response = complete_overlay(snapshot)
        invalid_response["ledgers"]["plaintiff_responses"]["records"][0][
            "attack_id"
        ] = []
        update_ledger_fingerprints(invalid_response)
        self.assertIn(
            "response-structure-invalid",
            finding_ids(validator.validate_overlay(invalid_response, snapshot)),
        )

        invalid_treatment = complete_overlay(snapshot)
        invalid_treatment["ledgers"]["judicial_treatments"]["records"][0][
            "source_location"
        ] = []
        update_ledger_fingerprints(invalid_treatment)
        self.assertIn(
            "source-location-invalid",
            finding_ids(validator.validate_overlay(invalid_treatment, snapshot)),
        )

        invalid_related = complete_overlay(snapshot)
        invalid_related["ledgers"]["judicial_treatments"]["records"][1][
            "related_treatment_ids"
        ] = [[]]
        update_ledger_fingerprints(invalid_related)
        self.assertIn(
            "treatment-structure-invalid",
            finding_ids(validator.validate_overlay(invalid_related, snapshot)),
        )

        invalid_job = complete_overlay(snapshot)
        invalid_job["review_plan"]["jobs"][0]["group_id"] = []
        self.assertIn(
            "review-plan-structure-invalid",
            finding_ids(validator.validate_overlay(invalid_job, snapshot)),
        )

        invalid_manifest = complete_manifest(snapshot, complete_overlay(snapshot))
        invalid_manifest["overlays"][0]["kind"] = []
        self.assertIn(
            "manifest-structure-invalid",
            finding_ids(
                validator.validate_filing_manifest(
                    invalid_manifest,
                    complete_overlay(snapshot),
                    snapshot,
                )
            ),
        )

    def test_identifiers_dates_sources_and_exact_quotes_are_validated(self):
        validator = load_validator()
        snapshot = complete_snapshot()

        duplicate = copy.deepcopy(snapshot)
        duplicate["sources"].append(copy.deepcopy(duplicate["sources"][0]))
        self.assertIn(
            "snapshot-duplicate-identifier",
            finding_ids(validator.validate_snapshot(duplicate)),
        )

        invalid_date = copy.deepcopy(snapshot)
        invalid_date["checked_through"] = "2026-99-99"
        self.assertIn(
            "snapshot-structure-invalid",
            finding_ids(validator.validate_snapshot(invalid_date)),
        )

        unknown_source = complete_overlay(snapshot)
        unknown_source["ledgers"]["adversary_attacks"]["records"][0][
            "source_ids"
        ] = ["SRC-UNKNOWN"]
        update_ledger_fingerprints(unknown_source)
        self.assertIn(
            "overlay-unknown-source",
            finding_ids(validator.validate_overlay(unknown_source, snapshot)),
        )

        wrong_quote = complete_overlay(snapshot)
        wrong_quote["ledgers"]["adversary_attacks"]["records"][0][
            "source_location"
        ]["quote"] = "This quotation does not appear."
        update_ledger_fingerprints(wrong_quote)
        self.assertIn(
            "source-quote-mismatch",
            finding_ids(validator.validate_overlay(wrong_quote, snapshot)),
        )

    def test_records_bind_location_date_issue_and_judicial_authorship(self):
        validator = load_validator()
        snapshot = complete_snapshot()

        split_provenance = complete_overlay(snapshot)
        split_provenance["ledgers"]["adversary_attacks"]["records"][0][
            "source_ids"
        ] = ["SRC-FAC"]
        update_ledger_fingerprints(split_provenance)
        self.assertIn(
            "record-source-link-invalid",
            finding_ids(validator.validate_overlay(split_provenance, snapshot)),
        )

        wrong_date = complete_overlay(snapshot)
        wrong_date["ledgers"]["adversary_attacks"]["records"][0]["date"] = (
            "2026-01-11"
        )
        update_ledger_fingerprints(wrong_date)
        self.assertIn(
            "record-date-mismatch",
            finding_ids(validator.validate_overlay(wrong_date, snapshot)),
        )

        wrong_dimension = complete_overlay(snapshot)
        wrong_dimension["ledgers"]["adversary_attacks"]["records"][0][
            "claim_id"
        ] = "CLAIM-UNRELATED"
        update_ledger_fingerprints(wrong_dimension)
        self.assertIn(
            "attack-dimension-link-invalid",
            finding_ids(validator.validate_overlay(wrong_dimension, snapshot)),
        )

        wrong_judicial_author = complete_snapshot()
        order = next(
            source
            for source in wrong_judicial_author["sources"]
            if source["source_id"] == "SRC-ORDER"
        )
        order["filed_by_actor_ids"] = ["ACT-MAGISTRATE"]
        overlay = complete_overlay(wrong_judicial_author)
        self.assertIn(
            "judicial-source-attribution-invalid",
            finding_ids(
                validator.validate_overlay(overlay, wrong_judicial_author)
            ),
        )

        future_source = complete_snapshot()
        future_source["sources"][-1]["filed_date"] = "2026-01-21"
        self.assertIn(
            "snapshot-source-after-check-date",
            finding_ids(validator.validate_snapshot(future_source)),
        )

    def test_matrix_and_review_targets_preserve_exact_source_scope(self):
        validator = load_validator()
        snapshot = complete_snapshot()

        wrong_family = complete_overlay(snapshot)
        wrong_family["review_plan"]["targets"][0]["document_family"] = (
            "complaint"
        )
        self.assertIn(
            "review-target-source-mismatch",
            finding_ids(validator.validate_overlay(wrong_family, snapshot)),
        )

        unknown_status_source = complete_overlay(snapshot)
        row = unknown_status_source["issue_matrix"][1]
        row["current_status_source_ids"] = ["SRC-UNKNOWN"]
        row["source_ids"] = ["SRC-MOTION", "SRC-UNKNOWN"]
        self.assertIn(
            "overlay-unknown-source",
            finding_ids(
                validator.validate_overlay(unknown_status_source, snapshot)
            ),
        )

        cross_attack_response = complete_overlay(snapshot)
        row = cross_attack_response["issue_matrix"][1]
        row["response_ids"] = ["RESP-ALPHA"]
        row["response_state"] = "plaintiff-answered"
        row["source_ids"] = ["SRC-FAC", "SRC-LEAVE", "SRC-MOTION"]
        self.assertIn(
            "matrix-link-invalid",
            finding_ids(
                validator.validate_overlay(cross_attack_response, snapshot)
            ),
        )

    def test_snapshot_and_ledger_fingerprints_fail_closed(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        snapshot["sources"][0]["content"] += " changed"
        self.assertIn(
            "snapshot-source-fingerprint-mismatch",
            finding_ids(validator.validate_snapshot(snapshot)),
        )

        good_snapshot = complete_snapshot()
        overlay = complete_overlay(good_snapshot)
        overlay["source_snapshot"]["sha256"] = "0" * 64
        self.assertIn(
            "overlay-snapshot-fingerprint-mismatch",
            finding_ids(validator.validate_overlay(overlay, good_snapshot)),
        )

        overlay = complete_overlay(good_snapshot)
        overlay["ledgers"]["adversary_attacks"]["records"][0]["status"] = (
            "adversary-renewed"
        )
        self.assertIn(
            "ledger-fingerprint-mismatch",
            finding_ids(validator.validate_overlay(overlay, good_snapshot)),
        )

    def test_material_divergence_municipality_and_assignment_are_enforced(self):
        validator = load_validator()
        snapshot = complete_snapshot()

        diverged = complete_overlay(snapshot)
        diverged["effective_groups"][0]["member_defendant_ids"].append("DEF-BETA")
        diverged["effective_groups"].pop(1)
        self.assertIn(
            "alignment-dimensions-diverge",
            finding_ids(validator.validate_overlay(diverged, snapshot)),
        )

        mixed = complete_overlay(snapshot)
        mixed["effective_groups"][0]["member_defendant_ids"].append("DEF-CITY")
        mixed["effective_groups"].pop(2)
        self.assertIn(
            "municipality-alignment-unproved",
            finding_ids(validator.validate_overlay(mixed, snapshot)),
        )

        missing = complete_overlay(snapshot)
        missing["effective_groups"].pop(1)
        self.assertIn(
            "defendant-group-assignment-invalid",
            finding_ids(validator.validate_overlay(missing, snapshot)),
        )

    def test_explicit_regroup_override_preserves_generated_profile(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        overlay["overrides"] = [
            {
                "override_id": "OVERRIDE-1",
                "instruction_id": "USER-INSTRUCTION-1",
                "action": "regroup",
                "affected_defendant_ids": ["DEF-BETA"],
                "generated_group_ids": ["GROUP-BETA"],
                "effective_group_ids": ["GROUP-BETA-USER"],
                "rationale": "The user requested a separate issue-scoped label.",
            }
        ]
        overlay["effective_groups"][1]["group_id"] = "GROUP-BETA-USER"
        beta_attack = overlay["ledgers"]["adversary_attacks"]["records"][1]
        beta_attack["group_id"] = "GROUP-BETA-USER"
        for job in overlay["review_plan"]["jobs"]:
            if job["group_id"] == "GROUP-BETA":
                job["group_id"] = "GROUP-BETA-USER"
        update_ledger_fingerprints(overlay)
        self.assertEqual(validator.validate_overlay(overlay, snapshot), [])

        missing_override = copy.deepcopy(overlay)
        missing_override["overrides"] = []
        self.assertIn(
            "override-provenance-invalid",
            finding_ids(validator.validate_overlay(missing_override, snapshot)),
        )

    def test_attack_response_and_judicial_roles_cannot_conflate(self):
        validator = load_validator()
        snapshot = complete_snapshot()

        attack_contamination = complete_overlay(snapshot)
        attack_contamination["ledgers"]["adversary_attacks"]["records"][0][
            "plaintiff-answered"
        ] = True
        update_ledger_fingerprints(attack_contamination)
        self.assertIn(
            "attack-role-contamination",
            finding_ids(validator.validate_overlay(attack_contamination, snapshot)),
        )

        conflated = complete_overlay(snapshot)
        district = conflated["ledgers"]["judicial_treatments"]["records"][1]
        district["reasoning_type"] = "independent-reasoning"
        district["related_treatment_ids"] = []
        update_ledger_fingerprints(conflated)
        self.assertIn(
            "judicial-stage-conflation",
            finding_ids(validator.validate_overlay(conflated, snapshot)),
        )

        wrong_actor = complete_overlay(snapshot)
        wrong_actor["ledgers"]["judicial_treatments"]["records"][0][
            "judicial_actor_id"
        ] = "ACT-DISTRICT"
        update_ledger_fingerprints(wrong_actor)
        self.assertIn(
            "judicial-stage-conflation",
            finding_ids(validator.validate_overlay(wrong_actor, snapshot)),
        )

        invalid_attack_status = complete_overlay(snapshot)
        invalid_attack_status["ledgers"]["adversary_attacks"]["records"][0][
            "status"
        ] = "plaintiff-answered"
        update_ledger_fingerprints(invalid_attack_status)
        self.assertIn(
            "attack-status-invalid",
            finding_ids(validator.validate_overlay(invalid_attack_status, snapshot)),
        )

        invalid_response_status = complete_overlay(snapshot)
        invalid_response_status["ledgers"]["plaintiff_responses"]["records"][0][
            "coverage"
        ] = "adversary-asserted"
        update_ledger_fingerprints(invalid_response_status)
        self.assertIn(
            "response-status-invalid",
            finding_ids(
                validator.validate_overlay(invalid_response_status, snapshot)
            ),
        )

    def test_appellate_stage_is_valid_and_cannot_be_attributed_to_district_actor(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        add_appellate_stage(snapshot, overlay)
        self.assertEqual(validator.validate_snapshot(snapshot), [])
        self.assertEqual(validator.validate_overlay(overlay, snapshot), [])

        conflated = copy.deepcopy(overlay)
        appellate = conflated["ledgers"]["judicial_treatments"]["records"][-1]
        appellate["judicial_actor_id"] = "ACT-DISTRICT"
        update_ledger_fingerprints(conflated)
        self.assertIn(
            "judicial-stage-conflation",
            finding_ids(validator.validate_overlay(conflated, snapshot)),
        )

    def test_matrix_preserves_sources_and_does_not_infer_from_silence(self):
        validator = load_validator()
        snapshot = complete_snapshot()

        missing_source = complete_overlay(snapshot)
        missing_source["issue_matrix"][0]["source_ids"].remove("SRC-ORDER")
        self.assertIn(
            "matrix-source-union-mismatch",
            finding_ids(validator.validate_overlay(missing_source, snapshot)),
        )

        inferred = complete_overlay(snapshot)
        inferred["issue_matrix"][1]["response_state"] = "plaintiff-not-answered"
        inferred["issue_matrix"][1]["judicial_state"] = "district-judge-rejected"
        self.assertIn(
            "matrix-silence-inferred",
            finding_ids(validator.validate_overlay(inferred, snapshot)),
        )

        copied = complete_overlay(snapshot)
        copied["issue_matrix"][0]["adversary_position"] = "copied position"
        self.assertIn(
            "matrix-role-contamination",
            finding_ids(validator.validate_overlay(copied, snapshot)),
        )

    def test_review_plan_is_blind_or_exactly_group_scoped(self):
        validator = load_validator()
        snapshot = complete_snapshot()

        blind_leak = complete_overlay(snapshot)
        blind = next(
            job
            for job in blind_leak["review_plan"]["jobs"]
            if job["review_kind"] == "blind-common-attack"
        )
        blind["attack_ids"] = ["ATK-ALPHA"]
        self.assertIn(
            "blind-review-overlay-leak",
            finding_ids(validator.validate_overlay(blind_leak, snapshot)),
        )

        blind_source_leak = complete_overlay(snapshot)
        blind = next(
            job
            for job in blind_source_leak["review_plan"]["jobs"]
            if job["review_kind"] == "blind-common-attack"
        )
        blind["source_ids"].append("SRC-MOTION")
        self.assertIn(
            "blind-review-overlay-leak",
            finding_ids(validator.validate_overlay(blind_source_leak, snapshot)),
        )

        cross_group = complete_overlay(snapshot)
        actual = next(
            job
            for job in cross_group["review_plan"]["jobs"]
            if job["group_id"] == "GROUP-ALPHA"
            and job["review_kind"] == "actual-adversary"
        )
        actual["attack_ids"].append("ATK-BETA")
        self.assertIn(
            "actual-review-scope-leak",
            finding_ids(validator.validate_overlay(cross_group, snapshot)),
        )

        cross_source = complete_overlay(snapshot)
        actual = next(
            job
            for job in cross_source["review_plan"]["jobs"]
            if job["group_id"] == "GROUP-ALPHA"
            and job["review_kind"] == "actual-adversary"
        )
        actual["source_ids"].append("SRC-ORDER")
        self.assertIn(
            "actual-review-scope-leak",
            finding_ids(validator.validate_overlay(cross_source, snapshot)),
        )

    def test_review_jobs_are_fresh_and_do_not_consume_prior_reviews(self):
        validator = load_validator()
        snapshot = complete_snapshot()

        duplicate_run = complete_overlay(snapshot)
        duplicate_run["review_plan"]["jobs"][1]["run_id"] = duplicate_run[
            "review_plan"
        ]["jobs"][0]["run_id"]
        self.assertIn(
            "review-run-not-fresh",
            finding_ids(validator.validate_overlay(duplicate_run, snapshot)),
        )

        inherited = complete_overlay(snapshot)
        inherited["review_plan"]["jobs"][0]["prior_review_ids"] = ["PRIOR-1"]
        self.assertIn(
            "review-run-not-fresh",
            finding_ids(validator.validate_overlay(inherited, snapshot)),
        )

    def test_leave_package_has_four_jobs_per_group(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        attacks = overlay["ledgers"]["adversary_attacks"]["records"]
        leave = next(
            item for item in snapshot["sources"] if item["source_id"] == "SRC-LEAVE"
        )
        target = {
            "artifact_id": "TARGET-LEAVE",
            "source_id": "SRC-LEAVE",
            "sha256": leave["sha256"],
            "document_family": "leave-to-amend-motion",
        }
        offset = len(overlay["review_plan"]["jobs"])
        added = review_jobs(overlay["effective_groups"], attacks, target)
        for index, job in enumerate(added, start=offset + 1):
            job["job_id"] = f"JOB-{index}"
            job["run_id"] = f"00000000-0000-4000-8000-{index:012d}"
        overlay["review_plan"]["targets"].append(target)
        overlay["review_plan"]["jobs"].extend(added)
        self.assertEqual(validator.validate_overlay(overlay, snapshot), [])

        overlay["review_plan"]["jobs"].pop()
        self.assertIn(
            "review-plan-cardinality-invalid",
            finding_ids(validator.validate_overlay(overlay, snapshot)),
        )

    def test_no_responsive_filing_runs_two_blind_jobs_and_no_actual_job(self):
        validator = load_validator()
        snapshot = initial_snapshot()
        overlay = no_responsive_overlay(snapshot)
        self.assertEqual(validator.validate_overlay(overlay, snapshot), [])
        for group_value in overlay["effective_groups"]:
            jobs = [
                job
                for job in overlay["review_plan"]["jobs"]
                if job["group_id"] == group_value["group_id"]
            ]
            self.assertEqual(len(jobs), 2)
            self.assertEqual(
                {job["review_kind"] for job in jobs}, {"blind-common-attack"}
            )
            self.assertEqual(len({job["run_id"] for job in jobs}), 2)

        invented = copy.deepcopy(overlay)
        invented["review_plan"]["jobs"][0]["review_kind"] = "actual-adversary"
        self.assertIn(
            "actual-profile-unavailable-invented",
            finding_ids(validator.validate_overlay(invented, snapshot)),
        )

    def test_filing_manifest_rejects_stale_failed_or_mismatched_overlay(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)

        mismatched = complete_manifest(snapshot, overlay)
        mismatched["overlays"][0]["sha256"] = "0" * 64
        self.assertIn(
            "manifest-overlay-fingerprint-mismatch",
            finding_ids(
                validator.validate_filing_manifest(mismatched, overlay, snapshot)
            ),
        )

        stale = complete_manifest(snapshot, overlay)
        stale["overlays"][0]["checked_through"] = "2026-01-19"
        self.assertIn(
            "manifest-overlay-stale",
            finding_ids(validator.validate_filing_manifest(stale, overlay, snapshot)),
        )

        failed = complete_manifest(snapshot, overlay)
        failed["overlays"][0]["validator_result"] = "failed"
        self.assertIn(
            "manifest-validator-failed",
            finding_ids(
                validator.validate_filing_manifest(failed, overlay, snapshot)
            ),
        )

    def test_committed_fixtures_pass_public_cli(self):
        self.assertTrue(VALIDATOR.is_file())
        complete = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--docket-snapshot-root",
                str(FIXTURES),
                "--docket-snapshot-target",
                "complete-snapshot.json",
                "--filing-root",
                str(FIXTURES),
                "--filing-manifest-target",
                "complete-filing-manifest.json",
            ],
            cwd=REPOSITORY,
            input=(FIXTURES / "complete-overlay.json").read_bytes(),
            capture_output=True,
            check=False,
        )
        self.assertEqual(complete.returncode, 0, complete.stderr.decode())
        self.assertTrue(json.loads(complete.stdout)["passed"])

        initial = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--docket-snapshot-root",
                str(FIXTURES),
                "--docket-snapshot-target",
                "initial-snapshot.json",
            ],
            cwd=REPOSITORY,
            input=(FIXTURES / "no-responsive-overlay.json").read_bytes(),
            capture_output=True,
            check=False,
        )
        self.assertEqual(initial.returncode, 0, initial.stderr.decode())
        self.assertTrue(json.loads(initial.stdout)["passed"])

    def test_cli_reports_stable_findings_and_nonzero(self):
        validator = load_validator()
        stdout = io.StringIO()
        with (
            tempfile.TemporaryDirectory() as directory,
            patch("sys.stdin", io.StringIO("{}")),
            redirect_stdout(stdout),
        ):
            exit_code = validator.main([
                "--docket-snapshot-root",
                directory,
                "--docket-snapshot-target",
                "missing-snapshot.json",
            ])
        result = json.loads(stdout.getvalue())
        self.assertNotEqual(exit_code, 0)
        self.assertIs(result["passed"], False)
        self.assertEqual(result["findings"][0]["id"], "input-file-unavailable")
        self.assertEqual(set(result["findings"][0]), {"id", "path", "message"})

    def test_folder_targets_reject_noncanonical_and_escaping_paths(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "directory").mkdir()
            outside = root.parent / f"outside-{uuid.uuid4().hex}.json"
            outside.write_text("{}", encoding="utf-8")
            (root / "escape.json").symlink_to(outside)
            try:
                for target, expected in (
                    ("/absolute.json", "input-path-invalid"),
                    ("C:/absolute.json", "input-path-invalid"),
                    ("folder\\snapshot.json", "input-path-invalid"),
                    ("../outside.json", "input-path-invalid"),
                    ("./snapshot.json", "input-path-invalid"),
                    ("escape.json", "input-path-invalid"),
                    ("directory", "input-path-invalid"),
                    ("missing.json", "input-file-unavailable"),
                    ("bad\x00name", "input-path-invalid"),
                ):
                    with self.subTest(target=target):
                        result = validator.validate_folder_overlay(
                            docket_snapshot_root=root,
                            docket_snapshot_target=target,
                            overlay={},
                        )
                        self.assertFalse(result["passed"])
                        self.assertEqual(
                            result["findings"][0]["id"], expected
                        )
                result = validator.validate_folder_overlay(
                    docket_snapshot_root="relative",
                    docket_snapshot_target="snapshot.json",
                    overlay={},
                )
                self.assertEqual(result["findings"][0]["id"], "input-path-invalid")
            finally:
                outside.unlink()

    def test_folder_target_reader_is_bounded_and_preserves_input_bytes(self):
        validator = load_validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            snapshot = root / "snapshot.json"
            snapshot.write_text(json.dumps(complete_snapshot()), encoding="utf-8")
            before = hashlib.sha256(snapshot.read_bytes()).hexdigest()
            result = validator.validate_folder_overlay(
                docket_snapshot_root=root,
                docket_snapshot_target="snapshot.json",
                overlay=complete_overlay(complete_snapshot()),
                max_input_bytes=1,
            )
            after = hashlib.sha256(snapshot.read_bytes()).hexdigest()
        self.assertFalse(result["passed"])
        self.assertEqual(result["findings"][0]["id"], "input-file-too-large")
        self.assertEqual(after, before)

    def test_generated_overlay_stdin_is_bounded_and_strict_json(self):
        command = [
            sys.executable,
            str(VALIDATOR),
            "--docket-snapshot-root",
            str(FIXTURES),
            "--docket-snapshot-target",
            "complete-snapshot.json",
        ]
        for payload, expected in (
            (b"\xff", "input-file-malformed-json"),
            (b" " * 1_000_001, "input-file-too-large"),
        ):
            with self.subTest(expected=expected):
                completed = subprocess.run(
                    command,
                    cwd=REPOSITORY,
                    input=payload,
                    capture_output=True,
                    check=False,
                )
                result = json.loads(completed.stdout)
                self.assertNotEqual(completed.returncode, 0)
                self.assertEqual(result["findings"][0]["id"], expected)


if __name__ == "__main__":
    unittest.main()
