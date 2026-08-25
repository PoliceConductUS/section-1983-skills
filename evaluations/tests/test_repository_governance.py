import json
import re
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.validate_governance import (
    APPROVED_FOLDER_CONTRACTS,
    SOURCE_DOCUMENTED_SKILLS,
    validate_source_documented_folder_guidance,
)


REPOSITORY = Path(__file__).resolve().parents[2]
VALIDATOR = REPOSITORY / "scripts" / "validate_governance.py"
VALID_DATE = "2026-08-20"
CONTRIBUTION_RULES = (
    (
        "stacked story",
        "Use one story per stacked branch.",
        "Do not use one story per stacked branch.",
    ),
    (
        "RED before GREEN",
        "Write the RED failing test before GREEN implementation.",
        "Write GREEN implementation before the RED failing test.",
    ),
    (
        "green refactor",
        "Refactor only while the tests remain green.",
        "Refactor while the tests are failing.",
    ),
    (
        "OpenSpec lifecycle",
        "Complete OpenSpec design, tasks, verification, retrospective, and archive artifacts.",
        "Do not complete OpenSpec design, tasks, verification, retrospective, and archive artifacts.",
    ),
    (
        "human legal judgment",
        "Automation must not silently select plaintiff decisions, litigation strategy, or legal conclusions.",
        "Automation may silently select plaintiff decisions, litigation strategy, or legal conclusions.",
    ),
    (
        "measurement feedback",
        "Measurement is feedback, never a verdict.",
        "Measurement is a verdict.",
    ),
    (
        "measurement limits",
        "Score deltas and judgment-based evaluations prompt review and do not decide legal quality, filing readiness, or human judgment.",
        "Score deltas and judgment-based evaluations decide legal quality, filing readiness, and human judgment.",
    ),
    (
        "self-documenting code",
        "Prefer self-documenting code.",
        "Do not prefer self-documenting code.",
    ),
    (
        "refactor before comment",
        "Refactor before adding a comment.",
        "Do not refactor before adding a comment.",
    ),
    (
        "bounded comment",
        "A necessary comment is short and clear and references an ADR or recorded decision when practical.",
        "A necessary comment may be long and unclear and need not reference an ADR or recorded decision.",
    ),
    (
        "full validation",
        "Run `npm run validate` before release.",
        "Do not run `npm run validate` before release.",
    ),
    (
        "main is not publication",
        "A push to `main` is not publication.",
        "A push to `main` is publication.",
    ),
    (
        "immutable release",
        "Release only with immutable semantic-version tags.",
        "Do not use immutable semantic-version tags.",
    ),
    (
        "deterministic enforcement",
        "The validator checks deterministic boundaries, not subjective prose, comment, test, or legal quality.",
        "The validator checks subjective prose, comment, test, and legal quality.",
    ),
)
OWNER_LINKS = {
    "GOVERNANCE.md": "GOVERNANCE.md",
    "PUBLISHING.md": "PUBLISHING.md",
}
DUPLICATED_OWNER_MARKERS = (
    "## protected legal gates",
    "## releasing a validated version",
    "gh workflow run release.yml",
    "verification, factual and authority source, permission, filing-readiness",
)
QUALITY_CONTROL_RULES = (
    (
        "non-mutating stage",
        "An independent quality-control stage is non-mutating.",
        "An independent quality-control stage may mutate an artifact under review.",
    ),
    (
        "report-only output",
        "It may read designated artifacts and return only its designated report or result for trusted-host publication.",
        "It may write changes to an artifact under review.",
    ),
    (
        "reviewed artifact prohibition",
        "It must not edit, overwrite, correct, regenerate, or otherwise modify an artifact under review.",
        "It may edit, overwrite, correct, regenerate, or otherwise modify an artifact under review.",
    ),
    (
        "combined instruction boundary",
        "A combined instruction to audit and fix does not authorize same-stage mutation.",
        "A combined instruction to audit and fix authorizes same-stage mutation.",
    ),
    (
        "pressure and workflow precedence",
        "Deadline pressure, sunk cost, claimed prior approval, and contrary workflow instructions do not override this boundary.",
        "Deadline pressure, sunk cost, claimed prior approval, or contrary workflow instructions may override this boundary.",
    ),
    (
        "advisory output",
        "Recommendations, proposed language, corrections, and copy-ready replacements are advisory only and do not authorize implementation.",
        "Recommendations, proposed language, corrections, and copy-ready replacements authorize implementation.",
    ),
    (
        "separate remediation",
        "Remediation requires a separately authorized drafting or revision stage.",
        "Remediation may occur during the independent quality-control stage.",
    ),
    (
        "versioning",
        "Create a new version when versioning applies.",
        "Overwrite the current version when versioning applies.",
    ),
    (
        "fresh verification",
        "A new read-only quality-control stage must verify the remediated artifact.",
        "The prior quality-control result transfers to the remediated artifact.",
    ),
    (
        "drafting self-check distinction",
        "An internal self-check inside an explicitly authorized drafting or revision stage may guide edits within that stage, but it is not an independent quality-control result.",
        "An internal drafting self-check is an independent quality-control result.",
    ),
)
QUALITY_CONTROL_REPORT_RULES = (
    (
        "declared target",
        "Before review, an independent quality-control stage must select exactly one artifact through its declared input roles and target policy.",
        "An independent quality-control stage may select an artifact outside its declared input roles or target policy.",
    ),
    (
        "explicit append-immutable output",
        "It must propose exactly one unique append-immutable output-relative report beneath the caller-declared output folder.",
        "It may propose a mutable or non-unique report outside the caller-declared output folder.",
    ),
    (
        "no fallback",
        "A missing, ambiguous, nonexistent, or out-of-role target must fail closed without a fallback write.",
        "A missing, ambiguous, nonexistent, or out-of-role target may use a fallback write.",
    ),
    (
        "path confinement",
        "The report path must reject absolute paths, traversal, symlink escapes, and existing destinations.",
        "The report path may be absolute, traverse, follow symlink escapes, or replace an existing destination.",
    ),
    (
        "host-only publication",
        "Only the trusted host may publish the report through the shared output boundary.",
        "The skill or helper may publish the report directly.",
    ),
    (
        "installed-contract binding",
        "The trusted host accepts quality-control publication only from an invocation bound to the installed skill's target policy and approved target roles; it rejects an unbound invocation or a target outside those approved roles.",
        "The trusted host may publish from an unbound invocation or a target outside the installed skill's approved roles.",
    ),
    (
        "prior report exclusion",
        "Prior quality-control reports must not become implicit input.",
        "Prior quality-control reports may become implicit input.",
    ),
    (
        "declared prior report",
        "A report may be reviewed only when that exact report is expressly present in a declared input role and selected consistently with the reviewing skill's target policy.",
        "A report may be reviewed from ambient output without a declared input role or target.",
    ),
    (
        "new review report",
        "The reviewing stage must propose a different new append-immutable report for trusted-host publication.",
        "The reviewing stage may update or replace the report under review.",
    ),
    (
        "immutable reports",
        "Existing reports are immutable and must not be edited, overwritten, replaced, renamed, or deleted.",
        "Existing reports may be edited, overwritten, replaced, renamed, or deleted.",
    ),
    (
        "report identity",
        "The trusted host prefixes the report with the canonical quality-control metadata envelope containing the skill and version, filtered logical input roles and reviewed artifact hashes, selected target role, relative path, SHA-256 fingerprint, and byte size, quality-control kind, UTC run time, run ID, scope, approved source identities, result, failed findings, passing-but-suboptimal recommendations, and terminal run-manifest identity.",
        "The report may omit its skill version, reviewed artifact hashes, target fingerprint, findings, recommendations, or run-manifest identity.",
    ),
    (
        "canonical report path",
        "The trusted host derives the report path as `quality-control-reports/<check-kind>-<utc-run-time>-<run-id>.md` and publishes exactly one report through the shared output writer.",
        "The skill may choose any report path or publish more than one report.",
    ),
    (
        "generated report fingerprint exclusion",
        "Generated reports beneath `quality-control-reports/` are excluded from the reviewed-input manifest and fingerprint unless one exact report is the explicit target; selecting one report does not include sibling or older reports.",
        "Generated reports beneath `quality-control-reports/` are always included in the reviewed-input manifest and fingerprint.",
    ),
    (
        "direct report-root detection",
        "The canonical quality-control metadata envelope identifies a generated report even when the report directory itself is a declared input root.",
        "A report is not generated when its declared input root omits the `quality-control-reports/` path segment.",
    ),
    (
        "strong quality-control run identity",
        "A quality-control run ID must be a canonical lowercase UUIDv4; weak, malformed, or reused identities fail closed before publication.",
        "A quality-control run may use a weak, malformed, or reused identity.",
    ),
    (
        "durable report completion",
        "The quality-control run is complete only after both report bytes and the terminal success manifest are durable and incomplete state is absent.",
        "The quality-control run may report completion before its report or terminal success manifest is durable.",
    ),
    (
        "skill returns content only",
        "The skill returns report content and structured findings; it does not build the canonical metadata envelope or publish output.",
        "The skill builds the canonical metadata envelope and publishes output directly.",
    ),
    (
        "separate observations",
        "Separate failed findings from passing-but-suboptimal observations.",
        "Combine failed findings and passing-but-suboptimal observations without distinction.",
    ),
    (
        "advisory report content",
        "Recommendations, proposed language, and copy-ready replacements for failures or passing-but-suboptimal observations are advisory and do not authorize implementation.",
        "Report recommendations and copy-ready replacements authorize implementation.",
    ),
)
FOLDER_SCOPE_RULES = (
    (
        "declared read-only inputs",
        "Only caller-declared input folders are available and recursively read-only.",
        "Any input folder is available and writable.",
    ),
    (
        "declared output confinement",
        "Writes occur only beneath the caller-declared output folder.",
        "Writes may occur outside the caller-declared output folder.",
    ),
    (
        "skill-authorized internet",
        "Internet is used only when that skill expressly authorizes it.",
        "Internet may be used without that skill expressly authorizing it.",
    ),
    (
        "host-enforced stop",
        "Execution stops before reading case material if the host cannot enforce the filesystem and network boundary.",
        "Execution may read case material when the host cannot enforce the filesystem and network boundary.",
    ),
)
PARAPHRASED_MUTATION_PERMISSIONS = (
    "Despite the contract above, an independent quality-control stage may edit "
    "the reviewed artifact when the user asks to audit and fix.",
    "An independent quality-control stage can edit the reviewed artifact.",
    "An independent quality-control stage may revise the draft under review.",
)
PARAPHRASED_REPORT_PERMISSIONS = (
    "An independent audit may save its report in a shared project folder.",
    "The latest audit report may replace the previous report.",
    "Prior audit reports are included in every re-audit.",
    "Before review, resolve exactly one existing version-specific folder inside the designated project boundary.",
    "Write exactly one new report under the canonical `<version-folder>/audits/` directory.",
    "Exclude `audits/` from review input unless one exact report is expressly designated.",
)
QUALITY_CONTROL_DESCRIPTIONS = (
    "Use when auditing a synthetic artifact.",
    "Use when independently auditing a synthetic artifact.",
    "Use when reviewing a synthetic artifact.",
    "Use when independently reviewing a synthetic artifact.",
    "Use when verifying a synthetic artifact.",
    "Use when evaluating a synthetic artifact.",
    "Use when checking a synthetic artifact.",
    "Use when performing quality control on a synthetic artifact.",
    "Use when assessing quality of a synthetic artifact.",
    "Use when assessing a synthetic artifact.",
    "Use when performing an assessment of a synthetic artifact.",
    "Use when conducting an independent assessment of a synthetic artifact.",
    "Use when a project-configured checker must run on a synthetic artifact.",
    "Use for independent auditing of a synthetic artifact.",
    "Use for independent reviewing of a synthetic artifact.",
    "Use for independent verification of a synthetic artifact.",
    "Use for independent evaluating of a synthetic artifact.",
    "Use for independent checking of a synthetic artifact.",
    "Use for independent assessment of a synthetic artifact.",
    "Use for independent review of a synthetic artifact.",
    "Use for an independent audit of a synthetic artifact.",
    "This skill independently audits a synthetic artifact.",
    "This skill independently reviews a synthetic artifact.",
    "This skill independently verifies a synthetic artifact.",
    "This skill independently evaluates a synthetic artifact.",
    "This skill independently checks a synthetic artifact.",
    "This skill independently assesses a synthetic artifact.",
    "This skill performs an independent review of a synthetic artifact.",
)
LIVE_QUALITY_CONTROL_SKILLS = {
    "adversarial-filing-review",
    "audit-authorities",
    "auditing-section-1983-discovery-responses",
    "auditing-section-1983-privilege-logs",
    "drafting-false-arrest-complaints",
    "drafting-section-1983-complaints",
    "drafting-section-1983-rule-59e",
    "filing-ci",
}


def read_public_file(path):
    if not path.is_file():
        raise AssertionError(f"required public file is missing: {path.relative_to(REPOSITORY)}")
    return path.read_text()


def assert_semantics(test, text, concepts):
    for label, patterns in concepts:
        with test.subTest(concept=label):
            alternatives = "|".join(f"(?:{pattern})" for pattern in patterns)
            test.assertRegex(text, rf"(?is){alternatives}")


def normalized(text):
    return " ".join(text.lower().split())


def replace_phrase(text, phrase, replacement):
    pattern = re.compile(r"\s+".join(re.escape(word) for word in phrase.split()))
    mutated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise AssertionError(f"fixture phrase not found exactly once: {phrase}")
    return mutated


def markdown_links(text):
    prose = re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1\s*", "", text)
    return re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", prose)


def assert_contribution_contract(test, text, root):
    contract = normalized(text)
    for label, affirmative, inversion in CONTRIBUTION_RULES:
        with test.subTest(rule=label):
            test.assertIn(normalized(affirmative), contract)
            test.assertNotIn(normalized(inversion), contract)
    links = markdown_links(text)
    for label, destination in OWNER_LINKS.items():
        with test.subTest(owner=label):
            destinations = [target for link_label, target in links if link_label == label]
            test.assertTrue(destinations)
            for target in destinations:
                test.assertEqual(target, destination)
                resolved = (root / target).resolve()
                resolved.relative_to(root.resolve())
                test.assertTrue(resolved.is_file())
    for marker in DUPLICATED_OWNER_MARKERS:
        with test.subTest(duplicated_owner=marker):
            test.assertNotIn(marker, contract)


def assert_quality_control_contract(test, text):
    contract = normalized(text)
    for label, affirmative, inversion in QUALITY_CONTROL_RULES:
        with test.subTest(quality_control_rule=label):
            test.assertIn(normalized(affirmative), contract)
            test.assertNotIn(normalized(inversion), contract)


def assert_quality_control_report_contract(test, text):
    contract = normalized(text)
    for label, affirmative, inversion in QUALITY_CONTROL_REPORT_RULES:
        with test.subTest(quality_control_report_rule=label):
            test.assertIn(normalized(affirmative), contract)
            test.assertNotIn(normalized(inversion), contract)


def assert_folder_scope_contract(test, text):
    contract = normalized(text)
    for label, affirmative, inversion in FOLDER_SCOPE_RULES:
        with test.subTest(folder_scope_rule=label):
            test.assertIn(normalized(affirmative), contract)
            test.assertNotIn(normalized(inversion), contract)


def referenced_scripts(command):
    return set(re.findall(r"\bnpm\s+run\s+([A-Za-z0-9:_-]+)", command))


def reachable_scripts(scripts, start):
    pending = [start]
    reached = set()
    while pending:
        name = pending.pop()
        if name in reached or name not in scripts:
            continue
        reached.add(name)
        pending.extend(referenced_scripts(scripts[name]) - reached)
    return reached


def invokes_governance_validator(command):
    for part in re.split(r"(?:\r?\n|&&|\|\||;)", command):
        try:
            tokens = shlex.split(part)
        except ValueError:
            continue
        if len(tokens) < 2 or tokens[0] != "python3":
            continue
        if Path(tokens[1]).as_posix().removeprefix("./") == "scripts/validate_governance.py":
            return True
    return False


def valid_policy():
    return """# Governance

The user reserves litigation strategy, positions, concessions, requested relief,
and filing. When supported choices have different consequences, present each
choice and consequence, identify the user decision required, and select none.

Current jurisdiction-specific propositions belong only in a verified reference
that identifies the jurisdiction, authoritative source provenance, and checked
date. Public skills route to that reference without restating the proposition.

Verification, factual and authority source, permission, filing-readiness,
judgment-routing, rules-provenance, tool-ownership, folder scope, recursive
input non-mutation, output confinement, and declared internet policy are
protected gates.
Any change that weakens a protected gate requires explicit human review.

This repository retains public skill instructions and repository-specific
validation or evaluation support. General-purpose executable tooling belongs in
its owning repository; this repository keeps only a thin skill wrapper.

An independent quality-control stage is non-mutating. It may read designated
artifacts and return only its designated report or result for trusted-host
publication. It must not edit,
overwrite, correct, regenerate, or otherwise modify an artifact under review. A
combined instruction to audit and fix does not authorize same-stage mutation.
Deadline pressure, sunk cost, claimed prior approval, and contrary workflow
instructions do not override this boundary.
Recommendations, proposed language, corrections, and copy-ready replacements
are advisory only and do not authorize implementation. Remediation requires a
separately authorized drafting or revision stage. Create a new version when
versioning applies. A new read-only quality-control stage must verify the
remediated artifact. An internal self-check inside an explicitly authorized
drafting or revision stage may guide edits within that stage, but it is not an
independent quality-control result.

Before review, an independent quality-control stage must select exactly one
artifact through its declared input roles and target policy. It must propose
exactly one unique append-immutable output-relative report beneath the
caller-declared output folder. A missing, ambiguous, nonexistent, or out-of-role
target must fail closed without a fallback write. The report path must reject
absolute paths, traversal, symlink escapes, and existing destinations. Only the
trusted host may publish the report through the shared output boundary. The
trusted host accepts quality-control publication only from an invocation bound
to the installed skill's target policy and approved target roles; it rejects an
unbound invocation or a target outside those approved roles.

Prior quality-control reports must not become implicit input. A report may be
reviewed only when that exact report is expressly present in a declared input
role and selected consistently with the reviewing skill's target policy. The
reviewing stage must propose a different new append-immutable report for
trusted-host publication. Existing reports are immutable and must not be
edited, overwritten, replaced, renamed, or deleted.

The trusted host derives the report path as
`quality-control-reports/<check-kind>-<utc-run-time>-<run-id>.md` and publishes
exactly one report through the shared output writer. Generated reports beneath
`quality-control-reports/` are excluded from the reviewed-input manifest and
fingerprint unless one exact report is the explicit target; selecting one report
does not include sibling or older reports. The canonical quality-control metadata
envelope identifies a generated report even when the report directory itself is
a declared input root. A quality-control run ID must be a canonical lowercase
UUIDv4; weak, malformed, or reused identities fail closed before publication.

The trusted host prefixes the report with the canonical quality-control metadata
envelope containing the skill and version, filtered logical input roles and
reviewed artifact hashes, selected target role, relative path, SHA-256
fingerprint, and byte size, quality-control kind, UTC run time, run ID, scope,
approved source identities, result, failed findings, passing-but-suboptimal
recommendations, and terminal run-manifest identity. The skill returns report
content and structured findings; it does not build the canonical metadata
envelope or publish output.

The quality-control run is complete only after both report bytes and the
terminal success manifest are durable and incomplete state is absent. Separate
failed findings from passing-but-suboptimal observations. Recommendations,
proposed language, and copy-ready replacements for failures or
passing-but-suboptimal observations are advisory and do not authorize
implementation.
"""


def valid_pull_request_template():
    return """## Protected legal gates

- Affected protected gate:
- Rationale:
- [ ] I request explicit human review of this protected-gate change.
"""


def valid_contributing_contract():
    return """# Contributing

Use one story per stacked branch. Write the RED failing test before GREEN
implementation. Refactor only while the tests remain green. Complete OpenSpec
design, tasks, verification, retrospective, and archive artifacts.

Automation must not silently select plaintiff decisions, litigation strategy,
or legal conclusions. Follow [GOVERNANCE.md](GOVERNANCE.md).

Measurement is feedback, never a verdict. Score deltas and judgment-based
evaluations prompt review and do not decide legal quality, filing readiness, or
human judgment.

Prefer self-documenting code. Refactor before adding a comment. A necessary
comment is short and clear and references an ADR or recorded decision when
practical.

Run `npm run validate` before release. A push to `main` is not publication.
Release only with immutable semantic-version tags. Follow
[PUBLISHING.md](PUBLISHING.md).

The validator checks deterministic boundaries, not subjective prose, comment,
test, or legal quality.
"""


def valid_quality_control_skill(
    description="Use when independently auditing a synthetic artifact.",
):
    return f"""---
name: filing-ci
description: {description}
---

# Example skill

An independent quality-control stage is non-mutating. It may read designated
artifacts and return only its designated report or result for trusted-host
publication. It must not edit,
overwrite, correct, regenerate, or otherwise modify an artifact under review. A
combined instruction to audit and fix does not authorize same-stage mutation.
Deadline pressure, sunk cost, claimed prior approval, and contrary workflow
instructions do not override this boundary.
Recommendations, proposed language, corrections, and copy-ready replacements
are advisory only and do not authorize implementation. Remediation requires a
separately authorized drafting or revision stage. Create a new version when
versioning applies. A new read-only quality-control stage must verify the
remediated artifact. An internal self-check inside an explicitly authorized
drafting or revision stage may guide edits within that stage, but it is not an
independent quality-control result.

Before review, an independent quality-control stage must select exactly one
artifact through its declared input roles and target policy. It must propose
exactly one unique append-immutable output-relative report beneath the
caller-declared output folder. A missing, ambiguous, nonexistent, or out-of-role
target must fail closed without a fallback write. The report path must reject
absolute paths, traversal, symlink escapes, and existing destinations. Only the
trusted host may publish the report through the shared output boundary. The
trusted host accepts quality-control publication only from an invocation bound
to the installed skill's target policy and approved target roles; it rejects an
unbound invocation or a target outside those approved roles.

Prior quality-control reports must not become implicit input. A report may be
reviewed only when that exact report is expressly present in a declared input
role and selected consistently with the reviewing skill's target policy. The
reviewing stage must propose a different new append-immutable report for
trusted-host publication. Existing reports are immutable and must not be
edited, overwritten, replaced, renamed, or deleted.

The trusted host derives the report path as
`quality-control-reports/<check-kind>-<utc-run-time>-<run-id>.md` and publishes
exactly one report through the shared output writer. Generated reports beneath
`quality-control-reports/` are excluded from the reviewed-input manifest and
fingerprint unless one exact report is the explicit target; selecting one report
does not include sibling or older reports. The canonical quality-control metadata
envelope identifies a generated report even when the report directory itself is
a declared input root. A quality-control run ID must be a canonical lowercase
UUIDv4; weak, malformed, or reused identities fail closed before publication.

The trusted host prefixes the report with the canonical quality-control metadata
envelope containing the skill and version, filtered logical input roles and
reviewed artifact hashes, selected target role, relative path, SHA-256
fingerprint, and byte size, quality-control kind, UTC run time, run ID, scope,
approved source identities, result, failed findings, passing-but-suboptimal
recommendations, and terminal run-manifest identity. The skill returns report
content and structured findings; it does not build the canonical metadata
envelope or publish output.

The quality-control run is complete only after both report bytes and the
terminal success manifest are durable and incomplete state is absent. Separate
failed findings from passing-but-suboptimal observations. Recommendations,
proposed language, and copy-ready replacements for failures or
passing-but-suboptimal observations are advisory and do not authorize
implementation.
"""


def valid_folder_scope_skill(name="filing-ci"):
    source_guidance = (
        "\n[Source-documented folders](references/source-documented-folders.md)\n"
        if name in SOURCE_DOCUMENTED_SKILLS
        else ""
    )
    return f"""---
name: {name}
description: Use when preparing a synthetic artifact.
---

# Example skill

[Folder contract](references/folder-contract.json)

Only caller-declared input folders are available and recursively read-only.
Writes occur only beneath the caller-declared output folder. Internet is used
only when that skill expressly authorizes it. Execution stops before reading
case material if the host cannot enforce the filesystem and network boundary.
{source_guidance}
"""


def valid_registry():
    fixture_skill = "filing-ci"
    return {
        "version": 1,
        "sources": [
            {
                "id": "federal-rules",
                "url": "https://www.uscourts.gov/rules-policies/current-rules-practice-procedure",
                "checked_on": VALID_DATE,
            }
        ],
        "skills": [
            {
                "name": fixture_skill,
                "rules_mode": "bundled-rules-dependent",
                "reviewed_on": VALID_DATE,
                "rationale": "Contains current federal procedural rule content.",
                "source_ids": ["federal-rules"],
                "jurisdiction_reference": f"skills/{fixture_skill}/references/jurisdiction.md",
            },
            *(
                {
                    "name": name,
                    "rules_mode": "rules-independent",
                    "reviewed_on": VALID_DATE,
                    "rationale": "Contains no current procedural rule content.",
                }
                for name in sorted(APPROVED_FOLDER_CONTRACTS)
                if name != fixture_skill
            ),
        ],
    }


def runtime_sourced_registry():
    registry = valid_registry()
    skill = registry["skills"][0]
    skill.update(
        {
            "rules_mode": "runtime-sourced",
            "rationale": "Uses an approved source supplied at runtime.",
            "output_provenance": {
                "source_identity": "actual approved source identity used",
                "checked_date": "actual checked date used",
            },
        }
    )
    skill.pop("source_ids")
    skill.pop("jurisdiction_reference")
    return registry


def write_temporary_repository(
    root,
    registry=None,
    policy=None,
    template=None,
    contributing=None,
    skill_text=None,
):
    (root / "governance").mkdir()
    (root / ".github").mkdir()
    for name, contract in APPROVED_FOLDER_CONTRACTS.items():
        package = root / "skills" / name
        (package / "references").mkdir(parents=True)
        (package / "SKILL.md").write_text(valid_folder_scope_skill(name))
        (package / "references" / "folder-contract.json").write_text(
            json.dumps(contract)
        )
        if name in SOURCE_DOCUMENTED_SKILLS:
            (package / "references" / "source-documented-folders.md").write_text(
                "Declared recursive read-only input folders.\n"
                "Each source uses a folder-relative path and SHA-256.\n"
                "Write domain-owned YAML under the explicit output.\n"
                "Use <output-folder>/temp/ for temporary work.\n"
            )
    (root / "SOURCE_DOCUMENTED_FOLDERS.md").write_text(
        "Declared input folders are recursive read-only.\n"
        "Use one explicit output folder.\n"
        "Domain-owned YAML includes SOURCE.yaml and a folder-relative path.\n"
        "Record SHA-256 and keep protected behavior installed.\n"
    )
    fixture_package = root / "skills" / "filing-ci"
    (fixture_package / "SKILL.md").write_text(
        skill_text or valid_folder_scope_skill("filing-ci")
    )
    (fixture_package / "references" / "jurisdiction.md").write_text(
        "Jurisdiction: Example District\n"
        "Authoritative source: https://www.uscourts.gov\n"
        f"Checked date: {VALID_DATE}\n"
    )
    (root / "GOVERNANCE.md").write_text(policy or valid_policy())
    (root / "PUBLISHING.md").write_text(
        "# Publishing\n\nUse immutable semantic-version tags after validation.\n"
    )
    (root / "CONTRIBUTING.md").write_text(
        contributing if contributing is not None else valid_contributing_contract()
    )
    (root / ".github" / "pull_request_template.md").write_text(
        template or valid_pull_request_template()
    )
    (root / "governance" / "rules-provenance.json").write_text(
        json.dumps(registry or valid_registry())
    )


def run_validator(repository_root):
    return subprocess.run(
        ["python3", "scripts/validate_governance.py", str(repository_root)],
        text=True,
        capture_output=True,
        check=False,
        cwd=REPOSITORY,
    )


class RepositoryGovernanceTest(unittest.TestCase):

    def assert_temporary_repository_error(self, mutate_registry, error_id):
        registry = valid_registry()
        mutate_registry(registry)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(error_id, result.stdout + result.stderr)

    def test_public_governance_reserves_user_judgment_and_protects_boundaries(self):
        policy = read_public_file(REPOSITORY / "GOVERNANCE.md")

        assert_semantics(
            self,
            policy,
            (
                ("strategy", (r"litigation.{0,40}strategy", r"strategy")),
                ("positions", (r"legal.{0,40}positions?", r"positions?")),
                ("concessions", (r"concessions?",)),
                ("requested relief", (r"requested.{0,40}relief", r"relief")),
                ("filing", (r"filing",)),
                (
                    "supported choices and consequences without selection",
                    (
                        r"supported.{0,80}choices?.{0,120}consequences?.{0,160}(?:select.{0,30}none|no.{0,30}selection)",
                        r"choices?.{0,120}consequences?.{0,160}(?:select.{0,30}none|no.{0,30}selection)",
                    ),
                ),
                (
                    "jurisdiction reference confinement",
                    (
                        r"jurisdiction.{0,80}proposition.{0,120}(?:only|must).{0,120}reference",
                    ),
                ),
                (
                    "sourced dated jurisdiction reference",
                    (
                        r"jurisdiction.{0,180}(?:authoritative|source).{0,180}(?:checked|date)",
                    ),
                ),
                ("verification gate", (r"verification",)),
                ("source gate", (r"(?:factual|authority).{0,30}source|source",)),
                ("permission gate", (r"permission",)),
                ("filing-readiness gate", (r"filing[- ]readiness",)),
                ("judgment-routing gate", (r"judgment[- ]routing",)),
                ("rules-provenance gate", (r"rules[- ]provenance",)),
                ("tool-ownership gate", (r"tool[- ]ownership",)),
                (
                    "thin wrapper ownership boundary",
                    (
                        r"thin.{0,30}(?:skill.{0,30})?wrapper.{0,180}owning.{0,60}repository",
                    ),
                ),
            ),
        )
        assert_quality_control_contract(self, policy)
        assert_quality_control_report_contract(self, policy)
        assert_semantics(
            self,
            policy,
            (
                ("folder scope gate", (r"folder.{0,40}scope",)),
                (
                    "recursive input non-mutation gate",
                    (r"recursive.{0,40}input.{0,40}non[- ]mutation",),
                ),
                ("output confinement gate", (r"output.{0,40}confinement",)),
                (
                    "declared internet policy gate",
                    (r"declared.{0,40}internet.{0,40}policy",),
                ),
            ),
        )

    def test_pull_request_template_requires_protected_gate_review(self):
        template = read_public_file(REPOSITORY / ".github" / "pull_request_template.md")

        assert_semantics(
            self,
            template,
            (
                ("affected protected gate", (r"affected.{0,50}protected.{0,50}gate",)),
                ("rationale", (r"rationale",)),
                ("explicit human review", (r"explicit.{0,50}(?:human.{0,30})?review",)),
            ),
        )

    def test_public_contribution_contract_preserves_repository_norms(self):
        contract = read_public_file(REPOSITORY / "CONTRIBUTING.md")
        assert_contribution_contract(self, contract, REPOSITORY)

    def test_governance_validator_rejects_missing_or_inverted_contract(self):
        valid = valid_contributing_contract()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, contributing=valid)
            assert_contribution_contract(self, valid, root)

        mutations = [("missing contract", "# Contributing\n")]
        mutations.extend(
            (
                label,
                replace_phrase(valid, affirmative, inversion),
            )
            for label, affirmative, inversion in CONTRIBUTION_RULES
        )
        for label, destination in OWNER_LINKS.items():
            source = f"[{label}]({destination})"
            mutations.extend(
                (
                    (f"missing {label}", valid.replace(source, label)),
                    (
                        f"external {label}",
                        valid.replace(source, f"[{label}](https://example.com/{label})"),
                    ),
                    (
                        f"traversal {label}",
                        valid.replace(source, f"[{label}](../{label})"),
                    ),
                )
            )
        mutations.extend(
            (f"duplicated owner {marker}", f"{valid}\n{marker}\n")
            for marker in DUPLICATED_OWNER_MARKERS
        )
        for label, contract in mutations:
            with self.subTest(mutation=label):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, contributing=contract)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "contribution-contract-language-missing",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_rejects_missing_or_inverted_folder_scope_contract(self):
        valid = valid_folder_scope_skill()
        mutations = [("missing contract", "# Example skill\n")]
        mutations.extend(
            (
                label,
                replace_phrase(valid, affirmative, inversion),
            )
            for label, affirmative, inversion in FOLDER_SCOPE_RULES
        )
        for label, skill_text in mutations:
            with self.subTest(mutation=label):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill_text)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "folder-scope-contract-language-missing: filing-ci",
                    result.stdout + result.stderr,
                )

    def test_every_live_public_skill_preserves_folder_scope_contract(self):
        for path in sorted((REPOSITORY / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=path.parent.name):
                assert_folder_scope_contract(self, read_public_file(path))

    def test_governance_validator_rejects_missing_or_inverted_quality_control_contract(self):
        valid = valid_quality_control_skill()
        mutations = [("missing contract", """---
name: filing-ci
description: Use when independently auditing a synthetic artifact.
---

# Example skill
""")]
        mutations.extend(
            (
                label,
                replace_phrase(valid, affirmative, inversion),
            )
            for label, affirmative, inversion in QUALITY_CONTROL_RULES
        )
        for label, skill_text in mutations:
            with self.subTest(mutation=label):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill_text)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-contract-language-missing: filing-ci",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_classifies_quality_control_by_behavior(self):
        for description in QUALITY_CONTROL_DESCRIPTIONS:
            with self.subTest(description=description):
                skill = valid_quality_control_skill(description).partition(
                    "\nAn independent quality-control stage"
                )[0]
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-contract-language-missing: filing-ci",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_rejects_missing_or_inverted_quality_control_report_contract(self):
        valid = valid_quality_control_skill()
        without_report = valid.partition(
            "\nBefore review, an independent quality-control stage"
        )[0]
        mutations = [("missing report contract", without_report)]
        mutations.extend(
            (
                label,
                replace_phrase(valid, affirmative, inversion),
            )
            for label, affirmative, inversion in QUALITY_CONTROL_REPORT_RULES
        )
        for label, skill_text in mutations:
            with self.subTest(mutation=label):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill_text)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-report-contract-language-missing: filing-ci",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_applies_report_contract_to_every_quality_control_behavior(self):
        for description in QUALITY_CONTROL_DESCRIPTIONS:
            with self.subTest(description=description):
                skill = valid_quality_control_skill(description).partition(
                    "\nBefore review, an independent quality-control stage"
                )[0]
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-report-contract-language-missing: filing-ci",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_applies_report_contract_to_live_quality_control_descriptions(self):
        for skill_name in LIVE_QUALITY_CONTROL_SKILLS:
            with self.subTest(skill=skill_name):
                skill_text = read_public_file(
                    REPOSITORY / "skills" / skill_name / "SKILL.md"
                )
                skill_text = replace_phrase(
                    skill_text, QUALITY_CONTROL_REPORT_RULES[0][1], ""
                )
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill_text)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-report-contract-language-missing: filing-ci",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_rejects_paraphrased_report_boundary_permissions(self):
        for permission in PARAPHRASED_REPORT_PERMISSIONS:
            cases = (
                (
                    "skill",
                    {"skill_text": valid_quality_control_skill() + permission},
                    "quality-control-report-contract-language-missing: filing-ci",
                ),
                (
                    "governance",
                    {"policy": valid_policy() + permission},
                    "quality-control-report-contract-language-missing: GOVERNANCE.md",
                ),
            )
            for label, changes, finding in cases:
                with self.subTest(case=label, permission=permission):
                    with tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        write_temporary_repository(root, **changes)
                        result = run_validator(root)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(finding, result.stdout + result.stderr)

    def test_governance_validator_rejects_paraphrased_same_stage_mutation_permission(self):
        for permission in PARAPHRASED_MUTATION_PERMISSIONS:
            cases = (
                (
                    "skill",
                    {"skill_text": valid_quality_control_skill() + permission},
                    "quality-control-contract-language-missing: filing-ci",
                ),
                (
                    "governance",
                    {"policy": valid_policy() + permission},
                    "quality-control-contract-language-missing: GOVERNANCE.md",
                ),
            )
            for label, changes, finding in cases:
                with self.subTest(case=label, permission=permission):
                    with tempfile.TemporaryDirectory() as directory:
                        root = Path(directory)
                        write_temporary_repository(root, **changes)
                        result = run_validator(root)

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(finding, result.stdout + result.stderr)

    def test_governance_validator_fails_closed_on_unreadable_quality_control_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, skill_text=valid_quality_control_skill())
            skill_path = root / "skills" / "filing-ci" / "SKILL.md"
            skill_path.unlink()
            skill_path.mkdir()
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(
            "quality-control-contract-unreadable: filing-ci",
            result.stdout + result.stderr,
        )

    def test_governance_validator_rejects_missing_or_inverted_quality_control_policy(self):
        valid = valid_policy()
        mutations = [
            (
                "missing contract",
                valid.partition("\nAn independent quality-control stage")[0],
            )
        ]
        mutations.extend(
            (
                label,
                replace_phrase(valid, affirmative, inversion),
            )
            for label, affirmative, inversion in QUALITY_CONTROL_RULES
        )
        for label, policy in mutations:
            with self.subTest(mutation=label):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, policy=policy)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-contract-language-missing: GOVERNANCE.md",
                    result.stdout + result.stderr,
                )

    def test_governance_validator_rejects_missing_or_inverted_quality_control_report_policy(self):
        valid = valid_policy()
        without_report = valid.partition(
            "\nBefore review, an independent quality-control stage"
        )[0]
        mutations = [("missing report contract", without_report)]
        mutations.extend(
            (
                label,
                replace_phrase(valid, affirmative, inversion),
            )
            for label, affirmative, inversion in QUALITY_CONTROL_REPORT_RULES
        )
        for label, policy in mutations:
            with self.subTest(mutation=label):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, policy=policy)
                    result = run_validator(root)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    "quality-control-report-contract-language-missing: GOVERNANCE.md",
                    result.stdout + result.stderr,
                )

    def test_non_quality_control_trigger_does_not_require_the_contract(self):
        descriptions = (
            "Use when drafting correspondence from a completed audit report.",
            "Use when revising a draft with an internal self-check.",
            "Use when drafting from a report stored under audits/.",
            "Use when preparing copy-ready prose from SHA-256 identified source artifacts.",
            "Use when revising a versioned filing after validation is complete.",
        )
        for description in descriptions:
            with self.subTest(description=description):
                skill = valid_folder_scope_skill().replace(
                    "description: Use when preparing a synthetic artifact.",
                    f"description: {description}",
                )
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, skill_text=skill)
                    result = run_validator(root)

                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validate_reaches_governance_validator(self):
        scripts = json.loads((REPOSITORY / "package.json").read_text())["scripts"]
        reached = reachable_scripts(scripts, "validate")

        self.assertTrue(
            any(invokes_governance_validator(scripts[name]) for name in reached),
            "validate must reach python3 scripts/validate_governance.py",
        )

    def test_live_repository_governance_validator_succeeds(self):
        result = run_validator(REPOSITORY)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_live_registry_classifies_exactly_the_public_skill_names(self):
        registry_path = REPOSITORY / "governance" / "rules-provenance.json"
        registry = json.loads(read_public_file(registry_path))
        discovered_names = [
            path.parent.name for path in (REPOSITORY / "skills").glob("*/SKILL.md")
        ]
        classified_names = [entry["name"] for entry in registry["skills"]]

        self.assertCountEqual(classified_names, discovered_names)

    def test_complete_temporary_repository_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root)
            result = run_validator(root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_runtime_sourced_entry_with_output_provenance_is_valid(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=runtime_sourced_registry())
            result = run_validator(root)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_runtime_sourced_entry_requires_actual_source_identity(self):
        registry = runtime_sourced_registry()
        registry["skills"][0]["output_provenance"].pop("source_identity")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("runtime-source-identity-required", result.stdout + result.stderr)

    def test_runtime_sourced_entry_requires_actual_checked_date(self):
        registry = runtime_sourced_registry()
        registry["skills"][0]["output_provenance"].pop("checked_date")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("runtime-source-date-required", result.stdout + result.stderr)

    def test_every_live_runtime_sourced_skill_requires_output_provenance(self):
        registry = json.loads(
            read_public_file(REPOSITORY / "governance" / "rules-provenance.json")
        )
        runtime_skills = [
            entry["name"]
            for entry in registry["skills"]
            if entry["rules_mode"] == "runtime-sourced"
        ]

        for name in runtime_skills:
            with self.subTest(skill=name):
                skill = read_public_file(REPOSITORY / "skills" / name / "SKILL.md")
                self.assertRegex(
                    skill,
                    r"(?is)returned.{0,80}artifact.{0,200}actual.{0,100}approved.{0,100}source.{0,30}identity.{0,180}checked.{0,30}date.{0,100}used",
                )

    def test_skill_entry_mismatch_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"].append(
                {
                    "name": "orphan-skill",
                    "rules_mode": "rules-independent",
                    "reviewed_on": VALID_DATE,
                    "rationale": "No current procedural rules are supplied.",
                }
            ),
            "skill-entry-mismatch",
        )

    def test_duplicate_skill_classification_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"].append(dict(registry["skills"][0])),
            "skill-entry-mismatch",
        )

    def test_invalid_rules_mode_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"][0].update({"rules_mode": "invented-mode"}),
            "invalid-rules-mode",
        )

    def test_non_string_rules_modes_are_rejected_without_traceback(self):
        for value in ([], {}, 7):
            with self.subTest(rules_mode=value):
                registry = valid_registry()
                registry["skills"][0]["rules_mode"] = value
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, registry=registry)
                    result = run_validator(root)

                output = result.stdout + result.stderr
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("invalid-rules-mode", output)
                self.assertNotIn("Traceback", output)

    def test_invalid_date_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"][0].update({"reviewed_on": "20-08-2026"}),
            "invalid-date",
        )

    def test_bundled_rules_source_is_required(self):
        registry = valid_registry()
        registry["skills"][0]["source_ids"] = []
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("bundled-source-required: filing-ci", result.stdout + result.stderr)

    def test_unknown_source_id_is_rejected(self):
        registry = valid_registry()
        registry["skills"][0]["source_ids"] = ["unknown-source"]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, registry=registry)
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown-source-id: filing-ci", result.stdout + result.stderr)

    def test_insecure_source_url_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["sources"][0].update({"url": "http://www.uscourts.gov"}),
            "insecure-source-url",
        )

    def test_malformed_source_urls_are_rejected_without_traceback(self):
        for url in ("https://[", "https://white space.example"):
            with self.subTest(url=url):
                registry = valid_registry()
                registry["sources"][0]["url"] = url
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    write_temporary_repository(root, registry=registry)
                    result = run_validator(root)

                output = result.stdout + result.stderr
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("insecure-source-url", output)
                self.assertNotIn("Traceback", output)

    def test_duplicate_source_id_is_rejected(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["sources"].append(dict(registry["sources"][0])),
            "duplicate-source-id",
        )

    def test_jurisdiction_reference_is_required(self):
        self.assert_temporary_repository_error(
            lambda registry: registry["skills"][0].pop("jurisdiction_reference"),
            "jurisdiction-reference-required",
        )

    def test_protected_review_language_is_required(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_temporary_repository(root, template="# Pull request\n")
            result = run_validator(root)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("protected-review-language-missing", result.stdout + result.stderr)

    def test_source_documented_folder_guidance_is_public_and_install_local(self):
        self.assertEqual(
            SOURCE_DOCUMENTED_SKILLS,
            (
                "analyzing-police-policy-sources",
                "building-defense-counsel-overlays",
                "building-judicial-reasoning-profiles",
                "building-litigation-alignment-overlays",
                "collecting-police-policy-sources",
            ),
        )
        self.assertEqual(validate_source_documented_folder_guidance(REPOSITORY), [])
        for path in (REPOSITORY / "README.md", REPOSITORY / "GOVERNANCE.md"):
            self.assertIn("SOURCE_DOCUMENTED_FOLDERS.md", path.read_text())
        for skill in SOURCE_DOCUMENTED_SKILLS:
            root = REPOSITORY / "skills" / skill
            entrypoint = (root / "SKILL.md").read_text()
            reference = root / "references" / "source-documented-folders.md"
            self.assertIn(
                "[source-documented folders](references/source-documented-folders.md)",
                entrypoint.lower(),
            )
            text = reference.read_text()
            self.assertIn("domain-owned YAML", text)
            self.assertIn("folder-relative path", text)
            self.assertIn("SHA-256", text)


if __name__ == "__main__":
    unittest.main()
