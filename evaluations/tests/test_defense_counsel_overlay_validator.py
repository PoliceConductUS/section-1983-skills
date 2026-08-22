import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[2]
SKILL = REPOSITORY / "skills" / "building-defense-counsel-overlays"
VALIDATOR = SKILL / "scripts" / "validate_counsel_overlays.py"
FIXTURES = SKILL / "references" / "fixtures"


def canonical_sha256(value):
    payload = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def text_sha256(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def source(source_id, role, actor_ids, matter_id, content, source_date):
    return {
        "source_id": source_id,
        "source_role": role,
        "retrieved_on": "2026-02-10",
        "source_date": source_date,
        "actor_ids": actor_ids,
        "matter_id": matter_id,
        "content": content,
        "sha256": text_sha256(content),
    }


def complete_snapshot():
    sources = [
        source(
            "SRC-BAR-A",
            "bar-directory",
            ["ATTY-A"],
            None,
            "Attorney Alpha is active in the Example Bar and affiliated with Example Defense Firm.",
            "2026-02-01",
        ),
        source(
            "SRC-APPEARANCE-A",
            "official-court-record",
            ["ATTY-A", "ATTY-B"],
            "MATTER-CURRENT",
            "Attorneys Alpha and Beta appear for Officer Example.",
            "2026-01-02",
        ),
        source(
            "SRC-MOTION-CURRENT",
            "current-docket-filed-paper",
            ["ATTY-A", "ATTY-B"],
            "MATTER-CURRENT",
            "Signed by Attorney Alpha for the defense team. The motion raises qualified immunity and requests dismissal.",
            "2026-01-10",
        ),
        source(
            "SRC-BRIEF-ONE",
            "official-court-record",
            ["ATTY-A"],
            "MATTER-ONE",
            "Attorney Alpha signed a motion raising qualified immunity and requesting dismissal.",
            "2025-05-01",
        ),
        source(
            "SRC-ORDER-ONE",
            "official-court-record",
            ["COURT-ONE"],
            "MATTER-ONE",
            "The court rejected the qualified-immunity argument at the pleading stage.",
            "2025-06-01",
        ),
        source(
            "SRC-BRIEF-TWO",
            "courtlistener-recap",
            ["ATTY-A"],
            "MATTER-TWO",
            "Attorney Alpha signed a motion raising qualified immunity and requesting dismissal.",
            "2025-09-01",
        ),
        source(
            "SRC-ORDER-TWO",
            "official-court-record",
            ["COURT-TWO"],
            "MATTER-TWO",
            "The court adopted the qualified-immunity argument at the pleading stage.",
            "2025-10-01",
        ),
        source(
            "SRC-BRIEF-THREE",
            "approved-public-case-artifact",
            ["ATTY-A"],
            "MATTER-THREE",
            "Attorney Alpha signed a motion addressing personal participation instead of qualified immunity.",
            "2025-12-01",
        ),
    ]
    return {
        "schema_version": "1.0",
        "snapshot_id": "COUNSEL-SNAPSHOT-1",
        "version": "v1",
        "checked_through": "2026-02-10",
        "research_protocol": {
            "queries": [
                {
                    "query_id": "QUERY-1",
                    "query": "synthetic attorney qualified immunity motions",
                    "searched_on": "2026-02-10",
                    "systems": ["official-court", "courtlistener-recap"],
                    "scope": "Three identified pleading-stage matters plus the current case.",
                }
            ],
            "deduplication_method": "Docket and source fingerprint.",
            "coverage_status": "complete",
            "denominator_definition": "All three approved comparable pleading-stage matters identified by QUERY-1.",
            "candidate_record_count": 3,
            "retrieved_record_count": 3,
            "unresolved_record_count": 0,
            "unavailable_record_count": 0,
        },
        "attorneys": [
            {"attorney_id": "ATTY-A", "professional_name": "Attorney Alpha"},
            {"attorney_id": "ATTY-B", "professional_name": "Attorney Beta"},
        ],
        "matters": [
            {
                "matter_id": "MATTER-CURRENT",
                "court": "Example District Court",
                "docket": "1:26-cv-00001",
                "posture": "pleading-stage",
                "represented_party": "Officer Example",
                "alignment_group_ids": ["GROUP-OFFICER"],
            },
            *[
                {
                    "matter_id": f"MATTER-{word}",
                    "court": f"Example Court {word}",
                    "docket": f"1:25-cv-0000{index}",
                    "posture": "pleading-stage",
                    "represented_party": f"Synthetic Client {word}",
                    "alignment_group_ids": [f"HIST-GROUP-{word}"],
                }
                for index, word in enumerate(("ONE", "TWO", "THREE"), 1)
            ],
        ],
        "sources": sources,
        "gaps": [],
    }


def location(source_id, quote):
    return {
        "source_id": source_id,
        "page": "1",
        "heading": "Synthetic argument",
        "quote": quote,
    }


def identity_records():
    return [
        {
            "identity_id": "IDENTITY-A",
            "attorney_id": "ATTY-A",
            "professional_name": "Attorney Alpha",
            "bar_status": "active",
            "bar_status_checked_on": "2026-02-10",
            "firm_affiliations": [
                {
                    "firm_name": "Example Defense Firm",
                    "start_date": "2025-01-01",
                    "end_date": None,
                    "source_ids": ["SRC-BAR-A"],
                }
            ],
            "appearances": [
                {
                    "matter_id": "MATTER-CURRENT",
                    "represented_party": "Officer Example",
                    "start_date": "2026-01-02",
                    "end_date": None,
                    "roles": ["signer", "appearance-counsel"],
                    "source_ids": ["SRC-APPEARANCE-A", "SRC-MOTION-CURRENT"],
                }
            ],
            "source_ids": ["SRC-BAR-A", "SRC-APPEARANCE-A", "SRC-MOTION-CURRENT"],
        },
        {
            "identity_id": "IDENTITY-B",
            "attorney_id": "ATTY-B",
            "professional_name": "Attorney Beta",
            "bar_status": "unverified",
            "bar_status_checked_on": "2026-02-10",
            "firm_affiliations": [],
            "appearances": [
                {
                    "matter_id": "MATTER-CURRENT",
                    "represented_party": "Officer Example",
                    "start_date": "2026-01-02",
                    "end_date": None,
                    "roles": ["appearance-counsel", "listed-counsel"],
                    "source_ids": ["SRC-APPEARANCE-A"],
                }
            ],
            "source_ids": ["SRC-APPEARANCE-A"],
        },
    ]


def argument(argument_id, matter_id, team_id, source_id, quote, attorney_id):
    historical_label = matter_id.split("-")[-1]
    return {
        "argument_id": argument_id,
        "matter_id": matter_id,
        "team_id": team_id,
        "attorney_id": attorney_id,
        "attribution_role": "signer" if attorney_id else "counsel-team",
        "source_ids": [source_id],
        "source_location": location(source_id, quote),
        "date": "2026-01-10" if matter_id == "MATTER-CURRENT" else {
            "MATTER-ONE": "2025-05-01",
            "MATTER-TWO": "2025-09-01",
            "MATTER-THREE": "2025-12-01",
        }[matter_id],
        "posture": "pleading-stage",
        "represented_party": (
            "Officer Example"
            if matter_id == "MATTER-CURRENT"
            else f"Synthetic Client {historical_label}"
        ),
        "alignment_group_ids": (
            ["GROUP-OFFICER"] if matter_id == "MATTER-CURRENT" else [f"HIST-GROUP-{matter_id.split('-')[-1]}"]
        ),
        "claim_id": "CLAIM-SEARCH",
        "challenged_act_id": "ACT-SEARCH",
        "element_or_defense": (
            "personal participation" if matter_id == "MATTER-THREE" else "qualified immunity"
        ),
        "qualified_immunity_prong": (
            None if matter_id == "MATTER-THREE" else "prong-one"
        ),
        "requested_relief": "dismissal",
        "status": "asserted",
    }


def update_fingerprints(overlay):
    names = (
        "identity_records",
        "team_records",
        "historical_arguments",
        "judicial_treatments",
        "current_attack_links",
        "patterns",
        "forecasts",
        "overrides",
        "gaps",
        "review_slices",
    )
    overlay["ledger_fingerprints"] = {
        name: canonical_sha256(overlay[name]) for name in names
    }


def complete_overlay(snapshot=None):
    snapshot = snapshot or complete_snapshot()
    current_quote = "Signed by Attorney Alpha for the defense team. The motion raises qualified immunity and requests dismissal."
    one_quote = "Attorney Alpha signed a motion raising qualified immunity and requesting dismissal."
    two_quote = one_quote
    three_quote = "Attorney Alpha signed a motion addressing personal participation instead of qualified immunity."
    arguments = [
        argument("ARG-CURRENT", "MATTER-CURRENT", "TEAM-CURRENT", "SRC-MOTION-CURRENT", current_quote, None),
        argument("ARG-ONE", "MATTER-ONE", "TEAM-ONE", "SRC-BRIEF-ONE", one_quote, "ATTY-A"),
        argument("ARG-TWO", "MATTER-TWO", "TEAM-TWO", "SRC-BRIEF-TWO", two_quote, "ATTY-A"),
        argument("ARG-THREE", "MATTER-THREE", "TEAM-THREE", "SRC-BRIEF-THREE", three_quote, "ATTY-A"),
    ]
    overlay = {
        "schema_version": "1.0",
        "overlay_id": "COUNSEL-OVERLAY-1",
        "version": "v1",
        "generated_at": "2026-02-10T12:00:00Z",
        "source_snapshot": {
            "snapshot_id": snapshot["snapshot_id"],
            "version": snapshot["version"],
            "sha256": canonical_sha256(snapshot),
            "checked_through": snapshot["checked_through"],
        },
        "identity_records": identity_records(),
        "team_records": [
            {
                "team_id": "TEAM-CURRENT",
                "matter_id": "MATTER-CURRENT",
                "version": "v1",
                "effective_start": "2026-01-02",
                "effective_end": None,
                "member_attorney_ids": ["ATTY-A", "ATTY-B"],
                "represented_party": "Officer Example",
                "alignment_group_ids": ["GROUP-OFFICER"],
                "source_ids": ["SRC-APPEARANCE-A", "SRC-MOTION-CURRENT"],
            },
            *[
                {
                    "team_id": f"TEAM-{word}",
                    "matter_id": f"MATTER-{word}",
                    "version": "v1",
                    "effective_start": "2025-01-01",
                    "effective_end": "2025-12-31",
                    "member_attorney_ids": ["ATTY-A"],
                    "represented_party": f"Synthetic Client {word}",
                    "alignment_group_ids": [f"HIST-GROUP-{word}"],
                    "source_ids": [f"SRC-BRIEF-{word}"],
                }
                for word in ("ONE", "TWO", "THREE")
            ],
        ],
        "historical_arguments": arguments,
        "judicial_treatments": [
            {
                "treatment_id": "TREAT-ONE",
                "argument_id": "ARG-ONE",
                "court_actor": "Example Court One",
                "source_ids": ["SRC-ORDER-ONE"],
                "source_location": location(
                    "SRC-ORDER-ONE",
                    "The court rejected the qualified-immunity argument at the pleading stage.",
                ),
                "date": "2025-06-01",
                "treatment": "rejected",
            },
            {
                "treatment_id": "TREAT-TWO",
                "argument_id": "ARG-TWO",
                "court_actor": "Example Court Two",
                "source_ids": ["SRC-ORDER-TWO"],
                "source_location": location(
                    "SRC-ORDER-TWO",
                    "The court adopted the qualified-immunity argument at the pleading stage.",
                ),
                "date": "2025-10-01",
                "treatment": "adopted",
            },
        ],
        "current_attack_links": [
            {
                "link_id": "LINK-CURRENT",
                "attack_id": "ATK-CURRENT-QI",
                "team_id": "TEAM-CURRENT",
                "alignment_group_id": "GROUP-OFFICER",
                "claim_id": "CLAIM-SEARCH",
                "defendant_ids": ["DEF-OFFICER"],
                "challenged_act_ids": ["ACT-SEARCH"],
                "source_ids": ["SRC-MOTION-CURRENT"],
            }
        ],
        "patterns": [
            {
                "pattern_id": "PATTERN-QI",
                "pattern_type": "recurring-defense",
                "comparable_argument_ids": ["ARG-ONE", "ARG-TWO", "ARG-THREE"],
                "scope": "Approved pleading-stage comparable matters.",
                "selection_method": "All matters identified by QUERY-1.",
                "denominator": 3,
                "coded_record_count": 3,
                "missingness": {"unresolved": 0, "unavailable": 0},
                "posture": "pleading-stage",
                "supporting_argument_ids": ["ARG-ONE", "ARG-TWO"],
                "contrary_argument_ids": ["ARG-THREE"],
                "treatment_ids": ["TREAT-ONE", "TREAT-TWO"],
                "conclusion": "Qualified immunity appeared in two of three approved comparable matters.",
                "confidence": "moderate",
                "source_ids": ["SRC-BRIEF-ONE", "SRC-BRIEF-TWO", "SRC-BRIEF-THREE", "SRC-ORDER-ONE", "SRC-ORDER-TWO"],
                "checked_through": "2026-02-10",
                "limits": "The synthetic public set is limited to the declared matters.",
            }
        ],
        "forecasts": [
            {
                "forecast_id": "FORECAST-QI",
                "professional_move": "The team may preserve qualified immunity as an alternative pleading-stage defense.",
                "pattern_ids": ["PATTERN-QI"],
                "comparable_argument_ids": ["ARG-ONE", "ARG-TWO", "ARG-THREE"],
                "denominator": 3,
                "coded_record_count": 3,
                "missingness": {"unresolved": 0, "unavailable": 0},
                "posture": "pleading-stage",
                "supporting_argument_ids": ["ARG-ONE", "ARG-TWO"],
                "contrary_argument_ids": ["ARG-THREE"],
                "confidence": "moderate",
                "source_ids": ["SRC-BRIEF-ONE", "SRC-BRIEF-TWO", "SRC-BRIEF-THREE"],
                "checked_through": "2026-02-10",
                "limits": "This is a professional next-move forecast, not an actual attack or outcome prediction.",
            }
        ],
        "overrides": [],
        "gaps": [],
        "ledger_fingerprints": {},
        "review_slices": [
            {
                "slice_id": "SLICE-BLIND",
                "job_id": "JOB-BLIND",
                "review_kind": "blind-common-attack",
                "alignment_group_id": "GROUP-OFFICER",
                "target_artifact_id": "TARGET-AMENDED-COMPLAINT",
                "team_ids": [],
                "identity_ids": [],
                "historical_argument_ids": [],
                "treatment_ids": [],
                "current_attack_link_ids": [],
                "pattern_ids": [],
                "forecast_ids": [],
                "common_attack_ids": ["COMMON-QI", "COMMON-ALTERNATIVE-PC"],
            },
            {
                "slice_id": "SLICE-ACTUAL",
                "job_id": "JOB-ACTUAL",
                "review_kind": "actual-adversary",
                "alignment_group_id": "GROUP-OFFICER",
                "target_artifact_id": "TARGET-AMENDED-COMPLAINT",
                "team_ids": ["TEAM-CURRENT"],
                "identity_ids": ["IDENTITY-A", "IDENTITY-B"],
                "historical_argument_ids": ["ARG-CURRENT", "ARG-ONE", "ARG-TWO", "ARG-THREE"],
                "treatment_ids": ["TREAT-ONE", "TREAT-TWO"],
                "current_attack_link_ids": ["LINK-CURRENT"],
                "pattern_ids": ["PATTERN-QI"],
                "forecast_ids": ["FORECAST-QI"],
                "common_attack_ids": ["COMMON-QI", "COMMON-ALTERNATIVE-PC"],
            },
        ],
    }
    update_fingerprints(overlay)
    return overlay


def incomplete_snapshot():
    snapshot = complete_snapshot()
    snapshot["snapshot_id"] = "COUNSEL-SNAPSHOT-INCOMPLETE"
    protocol = snapshot["research_protocol"]
    protocol["coverage_status"] = "incomplete"
    protocol["candidate_record_count"] = 4
    protocol["unresolved_record_count"] = 0
    protocol["unavailable_record_count"] = 1
    snapshot["gaps"] = [
        {
            "gap_id": "GAP-PACER",
            "query_ids": ["QUERY-1"],
            "matter_ids": [],
            "reason": "fee-gated",
            "description": "One identified filing is not available from approved public sources; paid PACER retrieval was not authorized.",
        }
    ]
    return snapshot


def bounded_example_overlay(snapshot):
    overlay = complete_overlay(complete_snapshot())
    overlay["overlay_id"] = "COUNSEL-OVERLAY-INCOMPLETE"
    overlay["source_snapshot"] = {
        "snapshot_id": snapshot["snapshot_id"],
        "version": snapshot["version"],
        "sha256": canonical_sha256(snapshot),
        "checked_through": snapshot["checked_through"],
    }
    overlay["patterns"] = []
    overlay["forecasts"] = []
    overlay["gaps"] = [
        {
            "gap_id": "OVERLAY-GAP-PACER",
            "source_gap_ids": ["GAP-PACER"],
            "scope": "Recurring-pattern and forecast strength.",
            "consequence": "Only bounded examples are available.",
        }
    ]
    for review_slice in overlay["review_slices"]:
        review_slice["pattern_ids"] = []
        review_slice["forecast_ids"] = []
    update_fingerprints(overlay)
    return overlay


def load_validator():
    if not VALIDATOR.is_file():
        raise AssertionError(f"missing validator: {VALIDATOR.relative_to(REPOSITORY)}")
    specification = importlib.util.spec_from_file_location(
        f"counsel_overlay_validator_{uuid.uuid4().hex}", VALIDATOR
    )
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def finding_ids(findings):
    return {finding["id"] for finding in findings}


class DefenseCounselOverlayValidatorTest(unittest.TestCase):
    def test_schema_required_fields_match_validator_record_keys(self):
        validator = load_validator()
        snapshot_schema = json.loads(
            (SKILL / "references" / "counsel-research-snapshot.schema.json").read_text()
        )
        overlay_schema = json.loads(
            (SKILL / "references" / "defense-counsel-overlay.schema.json").read_text()
        )
        snapshot_pairs = {
            "query": validator.QUERY_KEYS,
            "attorney": validator.ATTORNEY_KEYS,
            "matter": validator.MATTER_KEYS,
            "source": validator.SOURCE_KEYS,
            "gap": validator.SNAPSHOT_GAP_KEYS,
        }
        overlay_pairs = {
            "identityRecord": validator.IDENTITY_KEYS,
            "teamRecord": validator.TEAM_KEYS,
            "historicalArgument": validator.ARGUMENT_KEYS,
            "judicialTreatment": validator.TREATMENT_KEYS,
            "currentAttackLink": validator.ATTACK_LINK_KEYS,
            "pattern": validator.PATTERN_KEYS,
            "forecast": validator.FORECAST_KEYS,
            "override": validator.OVERRIDE_KEYS,
            "overlayGap": validator.OVERLAY_GAP_KEYS,
            "reviewSlice": validator.SLICE_KEYS,
        }
        for name, keys in snapshot_pairs.items():
            with self.subTest(schema="snapshot", record=name):
                self.assertEqual(set(snapshot_schema["$defs"][name]["required"]), keys)
        for name, keys in overlay_pairs.items():
            with self.subTest(schema="overlay", record=name):
                self.assertEqual(set(overlay_schema["$defs"][name]["required"]), keys)

    def test_complete_and_incomplete_public_corpora_validate_at_declared_strength(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        self.assertEqual(validator.validate_snapshot(snapshot), [])
        self.assertEqual(validator.validate_overlay(overlay, snapshot), [])
        incomplete = incomplete_snapshot()
        bounded = bounded_example_overlay(incomplete)
        self.assertEqual(validator.validate_snapshot(incomplete), [])
        self.assertEqual(validator.validate_overlay(bounded, incomplete), [])

    def test_required_roots_nested_types_and_duplicate_ids_fail_closed(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        missing = copy.deepcopy(snapshot)
        missing.pop("research_protocol")
        self.assertIn("snapshot-structure-invalid", finding_ids(validator.validate_snapshot(missing)))
        wrong_type = copy.deepcopy(overlay)
        wrong_type["historical_arguments"][0]["team_id"] = []
        update_fingerprints(wrong_type)
        self.assertIn("argument-structure-invalid", finding_ids(validator.validate_overlay(wrong_type, snapshot)))
        duplicate = copy.deepcopy(overlay)
        duplicate["identity_records"].append(copy.deepcopy(duplicate["identity_records"][0]))
        update_fingerprints(duplicate)
        self.assertIn("overlay-duplicate-identifier", finding_ids(validator.validate_overlay(duplicate, snapshot)))

    def test_invalid_snapshot_stops_overlay_semantics_without_traceback(self):
        validator = load_validator()
        invalid = complete_snapshot()
        invalid["research_protocol"] = []
        self.assertIn(
            "snapshot-invalid-for-overlay",
            finding_ids(validator.validate_overlay(complete_overlay(), invalid)),
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            snapshot_path = root / "snapshot.json"
            overlay_path = root / "overlay.json"
            snapshot_path.write_text(json.dumps(invalid))
            overlay_path.write_text(json.dumps(complete_overlay()))
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(snapshot_path), str(overlay_path)],
                cwd=REPOSITORY,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertIn("snapshot-invalid-for-overlay", finding_ids(payload["findings"]))

    def test_unhashable_nested_values_fail_closed_across_record_types(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        mutations = (
            ("identity", ("identity_records", 0, "appearances", 0, "matter_id"), "identity-structure-invalid"),
            ("team", ("team_records", 0, "matter_id"), "team-structure-invalid"),
            ("argument-role", ("historical_arguments", 0, "attribution_role"), "argument-structure-invalid"),
            ("argument-source", ("historical_arguments", 1, "source_ids", 0), "overlay-structure-invalid"),
            ("treatment", ("judicial_treatments", 0, "treatment"), "treatment-structure-invalid"),
            ("pattern-type", ("patterns", 0, "pattern_type"), "pattern-structure-invalid"),
            ("pattern-source", ("patterns", 0, "source_ids", 0), "overlay-structure-invalid"),
            ("forecast-confidence", ("forecasts", 0, "confidence"), "forecast-evidence-incomplete"),
            ("forecast-source", ("forecasts", 0, "source_ids", 0), "overlay-structure-invalid"),
        )
        for name, path, expected in mutations:
            with self.subTest(field=name):
                overlay = complete_overlay(snapshot)
                target = overlay
                for part in path[:-1]:
                    target = target[part]
                target[path[-1]] = []
                update_fingerprints(overlay)
                self.assertIn(
                    expected,
                    finding_ids(validator.validate_overlay(overlay, snapshot)),
                )

    def test_source_hash_date_role_and_quote_integrity_are_enforced(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        changed = copy.deepcopy(snapshot)
        changed["sources"][0]["content"] += " changed"
        self.assertIn("snapshot-source-fingerprint-mismatch", finding_ids(validator.validate_snapshot(changed)))
        future = copy.deepcopy(snapshot)
        future["sources"][0]["retrieved_on"] = "2026-02-11"
        self.assertIn("snapshot-source-after-check-date", finding_ids(validator.validate_snapshot(future)))
        wrong_quote = complete_overlay(snapshot)
        wrong_quote["historical_arguments"][0]["source_location"]["quote"] = "Absent quotation."
        update_fingerprints(wrong_quote)
        self.assertIn("source-quote-mismatch", finding_ids(validator.validate_overlay(wrong_quote, snapshot)))
        biography_behavior = complete_overlay(snapshot)
        biography_behavior["historical_arguments"][1]["source_ids"] = ["SRC-BAR-A"]
        biography_behavior["historical_arguments"][1]["source_location"] = location("SRC-BAR-A", "Attorney Alpha is active in the Example Bar.")
        update_fingerprints(biography_behavior)
        self.assertIn("behavior-source-role-invalid", finding_ids(validator.validate_overlay(biography_behavior, snapshot)))

    def test_joint_filing_does_not_become_listed_attorney_behavior(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        current = overlay["historical_arguments"][0]
        current["attorney_id"] = "ATTY-B"
        current["attribution_role"] = "listed-counsel"
        update_fingerprints(overlay)
        self.assertIn("individual-attribution-unsupported", finding_ids(validator.validate_overlay(overlay, snapshot)))

    def test_direct_signer_attribution_and_team_membership_must_match_sources(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        overlay["historical_arguments"][1]["attorney_id"] = "ATTY-B"
        update_fingerprints(overlay)
        self.assertIn("individual-attribution-unsupported", finding_ids(validator.validate_overlay(overlay, snapshot)))
        wrong_team = complete_overlay(snapshot)
        wrong_team["team_records"][0]["member_attorney_ids"] = ["ATTY-A", "ATTY-MISSING"]
        update_fingerprints(wrong_team)
        self.assertIn("team-attorney-link-invalid", finding_ids(validator.validate_overlay(wrong_team, snapshot)))

    def test_identity_team_pattern_and_forecast_provenance_is_reconciled(self):
        validator = load_validator()
        snapshot = complete_snapshot()

        unknown_appearance = complete_overlay(snapshot)
        unknown_appearance["identity_records"][0]["appearances"][0]["source_ids"] = ["SRC-MISSING"]
        update_fingerprints(unknown_appearance)
        self.assertIn("identity-source-link-invalid", finding_ids(validator.validate_overlay(unknown_appearance, snapshot)))

        wrong_team_source = complete_overlay(snapshot)
        wrong_team_source["team_records"][0]["source_ids"] = ["SRC-BRIEF-ONE"]
        update_fingerprints(wrong_team_source)
        self.assertIn("team-source-link-invalid", finding_ids(validator.validate_overlay(wrong_team_source, snapshot)))

        expired_team = complete_overlay(snapshot)
        expired_team["team_records"][0]["effective_end"] = "2026-01-05"
        update_fingerprints(expired_team)
        self.assertIn("team-source-link-invalid", finding_ids(validator.validate_overlay(expired_team, snapshot)))

        wrong_attack_source = complete_overlay(snapshot)
        wrong_attack_source["current_attack_links"][0]["source_ids"] = ["SRC-BRIEF-ONE"]
        update_fingerprints(wrong_attack_source)
        self.assertIn("current-attack-source-link-invalid", finding_ids(validator.validate_overlay(wrong_attack_source, snapshot)))

        unrelated_treatment = complete_overlay(snapshot)
        unrelated_treatment["patterns"][0]["comparable_argument_ids"] = ["ARG-TWO", "ARG-THREE", "ARG-CURRENT"]
        unrelated_treatment["patterns"][0]["supporting_argument_ids"] = ["ARG-TWO", "ARG-CURRENT"]
        update_fingerprints(unrelated_treatment)
        self.assertIn("pattern-evidence-link-invalid", finding_ids(validator.validate_overlay(unrelated_treatment, snapshot)))

        split_sources = complete_overlay(snapshot)
        split_sources["forecasts"][0]["source_ids"] = ["SRC-BRIEF-ONE"]
        update_fingerprints(split_sources)
        self.assertIn("forecast-source-union-invalid", finding_ids(validator.validate_overlay(split_sources, snapshot)))

    def test_judicial_treatment_and_current_attacks_remain_linked_not_copied(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        overlay["judicial_treatments"][0]["argument_id"] = "ARG-MISSING"
        update_fingerprints(overlay)
        self.assertIn("treatment-argument-link-invalid", finding_ids(validator.validate_overlay(overlay, snapshot)))
        copied = complete_overlay(snapshot)
        copied["current_attack_links"][0]["attack_text"] = "copied attack"
        update_fingerprints(copied)
        self.assertIn("current-attack-structure-invalid", finding_ids(validator.validate_overlay(copied, snapshot)))

    def test_patterns_require_complete_reconciled_denominator_and_linked_evidence(self):
        validator = load_validator()
        incomplete = incomplete_snapshot()
        overlay = complete_overlay(complete_snapshot())
        overlay["source_snapshot"] = {
            "snapshot_id": incomplete["snapshot_id"],
            "version": incomplete["version"],
            "sha256": canonical_sha256(incomplete),
            "checked_through": incomplete["checked_through"],
        }
        update_fingerprints(overlay)
        self.assertIn("pattern-incomplete-corpus", finding_ids(validator.validate_overlay(overlay, incomplete)))
        mismatch = complete_overlay()
        mismatch["patterns"][0]["denominator"] = 4
        update_fingerprints(mismatch)
        self.assertIn("pattern-denominator-invalid", finding_ids(validator.validate_overlay(mismatch, complete_snapshot())))
        unknown = complete_overlay()
        unknown["patterns"][0]["supporting_argument_ids"] = ["ARG-MISSING"]
        update_fingerprints(unknown)
        self.assertIn("pattern-evidence-link-invalid", finding_ids(validator.validate_overlay(unknown, complete_snapshot())))

    def test_forecasts_require_calibration_contrary_evidence_and_no_certainty(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        certainty = complete_overlay(snapshot)
        certainty["forecasts"][0]["professional_move"] = "Counsel will always raise qualified immunity and win."
        update_fingerprints(certainty)
        ids = finding_ids(validator.validate_overlay(certainty, snapshot))
        self.assertIn("forecast-certainty-prohibited", ids)
        self.assertIn("forecast-outcome-prohibited", ids)
        no_contrary = complete_overlay(snapshot)
        no_contrary["forecasts"][0]["contrary_argument_ids"] = []
        update_fingerprints(no_contrary)
        self.assertIn("forecast-evidence-incomplete", finding_ids(validator.validate_overlay(no_contrary, snapshot)))
        wrong_posture = complete_overlay(snapshot)
        wrong_posture["forecasts"][0]["posture"] = "summary-judgment"
        update_fingerprints(wrong_posture)
        self.assertIn("forecast-posture-mismatch", finding_ids(validator.validate_overlay(wrong_posture, snapshot)))

    def test_cross_case_comparison_does_not_create_automatic_legal_effect(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        overlay["patterns"][0]["pattern_type"] = "cross-case-comparison"
        overlay["patterns"][0]["conclusion"] = "The difference automatically waives the current position and creates judicial estoppel."
        update_fingerprints(overlay)
        self.assertIn("automatic-legal-effect-prohibited", finding_ids(validator.validate_overlay(overlay, snapshot)))

    def test_personal_profile_fields_and_content_are_rejected(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        overlay["identity_records"][0]["politics"] = "irrelevant"
        update_fingerprints(overlay)
        self.assertIn("identity-structure-invalid", finding_ids(validator.validate_overlay(overlay, snapshot)))
        content = complete_overlay(snapshot)
        content["patterns"][0]["conclusion"] = "Attorney Alpha has an aggressive personality and family pressure."
        update_fingerprints(content)
        self.assertIn("personal-profile-prohibited", finding_ids(validator.validate_overlay(content, snapshot)))

    def test_blind_and_actual_review_slices_preserve_relevance_and_common_attacks(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        blind_leak = complete_overlay(snapshot)
        blind_leak["review_slices"][0]["team_ids"] = ["TEAM-CURRENT"]
        update_fingerprints(blind_leak)
        self.assertIn("blind-review-counsel-leak", finding_ids(validator.validate_overlay(blind_leak, snapshot)))
        wrong_team = complete_overlay(snapshot)
        wrong_team["review_slices"][1]["team_ids"] = ["TEAM-HIST"]
        update_fingerprints(wrong_team)
        self.assertIn("actual-review-scope-invalid", finding_ids(validator.validate_overlay(wrong_team, snapshot)))
        suppressed = complete_overlay(snapshot)
        suppressed["review_slices"][1]["common_attack_ids"] = []
        update_fingerprints(suppressed)
        self.assertIn("common-attack-pass-suppressed", finding_ids(validator.validate_overlay(suppressed, snapshot)))

    def test_overrides_preserve_history_and_ledger_fingerprints(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        overlay["overrides"] = [
            {
                "override_id": "OVERRIDE-1",
                "instruction_id": "USER-1",
                "action": "exclude",
                "scope": "forecast research",
                "affected_ids": ["ATTY-B"],
                "rationale": "User excluded Attorney Beta from forecast research.",
            }
        ]
        update_fingerprints(overlay)
        self.assertEqual(validator.validate_overlay(overlay, snapshot), [])
        rewrite = complete_overlay(snapshot)
        rewrite["overrides"] = [
            {
                "override_id": "OVERRIDE-2",
                "instruction_id": "USER-2",
                "action": "rewrite-attribution",
                "scope": "historical argument",
                "affected_ids": ["ARG-CURRENT"],
                "rationale": "Rewrite the source attribution.",
            }
        ]
        update_fingerprints(rewrite)
        self.assertIn("override-provenance-rewrite-prohibited", finding_ids(validator.validate_overlay(rewrite, snapshot)))
        drift = complete_overlay(snapshot)
        drift["historical_arguments"][0]["status"] = "withdrawn"
        self.assertIn("ledger-fingerprint-mismatch", finding_ids(validator.validate_overlay(drift, snapshot)))

    def test_filing_pins_are_separate_current_and_passing(self):
        validator = load_validator()
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        pins = [
            {
                "kind": kind,
                "overlay_id": overlay["overlay_id"],
                "version": overlay["version"],
                "sha256": canonical_sha256(overlay),
                "checked_through": snapshot["checked_through"],
                "validator_result": "passed",
                "source_snapshot_id": snapshot["snapshot_id"],
                "source_snapshot_version": snapshot["version"],
                "source_snapshot_sha256": canonical_sha256(snapshot),
            }
            for kind in ("counsel-identity", "counsel-team")
        ]
        self.assertEqual(validator.validate_filing_pins(pins, overlay, snapshot), [])
        stale = copy.deepcopy(pins)
        stale[1]["checked_through"] = "2026-02-09"
        self.assertIn("counsel-pin-stale", finding_ids(validator.validate_filing_pins(stale, overlay, snapshot)))
        failed = copy.deepcopy(pins)
        failed[0]["validator_result"] = "failed"
        self.assertIn("counsel-pin-validator-failed", finding_ids(validator.validate_filing_pins(failed, overlay, snapshot)))

    def test_public_cli_validates_committed_fixtures_and_reports_stable_json(self):
        complete = subprocess.run(
            [sys.executable, str(VALIDATOR), str(FIXTURES / "complete-research-snapshot.json"), str(FIXTURES / "complete-counsel-overlay.json")],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(complete.returncode, 0, complete.stderr)
        self.assertEqual(json.loads(complete.stdout), {"findings": [], "passed": True})
        bounded = subprocess.run(
            [sys.executable, str(VALIDATOR), str(FIXTURES / "incomplete-research-snapshot.json"), str(FIXTURES / "bounded-example-overlay.json")],
            cwd=REPOSITORY,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(bounded.returncode, 0, bounded.stderr)
        self.assertTrue(json.loads(bounded.stdout)["passed"])
        with tempfile.TemporaryDirectory() as directory:
            bad = Path(directory) / "bad.json"
            bad.write_bytes(b"\xff")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), str(bad), str(FIXTURES / "complete-counsel-overlay.json")],
                cwd=REPOSITORY,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["findings"][0]["id"], "input-file-malformed-json")

    def test_public_cli_validates_counsel_pins_in_filing_manifest(self):
        snapshot = complete_snapshot()
        overlay = complete_overlay(snapshot)
        pins = [
            {
                "kind": kind,
                "overlay_id": overlay["overlay_id"],
                "version": overlay["version"],
                "sha256": canonical_sha256(overlay),
                "checked_through": snapshot["checked_through"],
                "validator_result": "passed",
                "source_snapshot_id": snapshot["snapshot_id"],
                "source_snapshot_version": snapshot["version"],
                "source_snapshot_sha256": canonical_sha256(snapshot),
            }
            for kind in ("counsel-identity", "counsel-team")
        ]
        manifest = {
            "schema_version": "1.0",
            "filing_version_id": "FILING-V1",
            "artifact_id": "TARGET-V1",
            "artifact_sha256": "1" * 64,
            "source_snapshot": {
                "snapshot_id": "DOCKET-SNAPSHOT-1",
                "version": "v1",
                "sha256": "2" * 64,
                "checked_through": "2026-02-10",
            },
            "overlays": pins,
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            snapshot_path = root / "snapshot.json"
            overlay_path = root / "overlay.json"
            manifest_path = root / "manifest.json"
            snapshot_path.write_text(json.dumps(snapshot))
            overlay_path.write_text(json.dumps(overlay))
            manifest_path.write_text(json.dumps(manifest))
            command = [
                sys.executable,
                str(VALIDATOR),
                str(snapshot_path),
                str(overlay_path),
                "--filing-manifest",
                str(manifest_path),
            ]
            passing = subprocess.run(
                command,
                cwd=REPOSITORY,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(passing.returncode, 0, passing.stderr)
            manifest["overlays"][1]["checked_through"] = "2026-02-09"
            manifest_path.write_text(json.dumps(manifest))
            stale = subprocess.run(
                command,
                cwd=REPOSITORY,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("counsel-pin-stale", finding_ids(json.loads(stale.stdout)["findings"]))


if __name__ == "__main__":
    unittest.main()
