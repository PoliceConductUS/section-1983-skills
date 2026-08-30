import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


MODES = {"rules-independent", "runtime-sourced", "bundled-rules-dependent"}
FOLDER_CONTRACT_FIELDS = {
    "version",
    "skill",
    "input_roles",
    "target",
    "internet",
    "output",
}
SAFE_ROLE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SOURCE_DOCUMENTED_SKILLS = (
    "building-defense-counsel-overlays",
    "building-judicial-reasoning-profiles",
    "building-litigation-alignment-overlays",
    "collecting-police-policy-sources",
)


def folder_contract(skill, input_roles, target_policy, target_roles, internet):
    return {
        "version": 1,
        "skill": skill,
        "input_roles": input_roles,
        "target": {"policy": target_policy, "roles": target_roles},
        "internet": internet,
        "output": {"mode": "append-immutable"},
    }


APPROVED_FOLDER_CONTRACTS = {
    "adversarial-filing-review": folder_contract(
        "adversarial-filing-review",
        ["filing", "approved-sources"],
        "required",
        ["filing"],
        "authorized",
    ),
    "audit-authorities": folder_contract(
        "audit-authorities",
        ["filing-source", "verified-authority"],
        "required",
        ["filing-source"],
        {"audit": "disabled", "freshness-research": "authorized"},
    ),
    "auditing-section-1983-discovery-responses": folder_contract(
        "auditing-section-1983-discovery-responses",
        ["served-discovery", "responses", "production", "authorities"],
        "required",
        ["served-discovery", "responses"],
        "disabled",
    ),
    "auditing-section-1983-privilege-logs": folder_contract(
        "auditing-section-1983-privilege-logs",
        ["privilege-log", "served-discovery", "authorities"],
        "required",
        ["privilege-log"],
        "disabled",
    ),
    "building-defense-counsel-overlays": folder_contract(
        "building-defense-counsel-overlays",
        ["research-snapshot", "case-record"],
        "required",
        ["research-snapshot"],
        "disabled",
    ),
    "building-litigation-alignment-overlays": folder_contract(
        "building-litigation-alignment-overlays",
        ["docket-snapshot", "filing"],
        "required",
        ["docket-snapshot"],
        "disabled",
    ),
    "building-judicial-reasoning-profiles": folder_contract(
        "building-judicial-reasoning-profiles",
        [
            "judge-identity",
            "court-scope",
            "approved-sources",
            "verified-authorities",
        ],
        "none",
        [],
        {"acquisition": "authorized", "compilation": "disabled"},
    ),
    "collecting-police-policy-sources": folder_contract(
        "collecting-police-policy-sources",
        [
            "department-identity",
            "jurisdiction",
            "approved-source-system",
            "research-scope",
        ],
        "none",
        [],
        "authorized",
    ),
    "judicial-reviewer": folder_contract(
        "judicial-reviewer",
        ["profile", "filing", "approved-sources"],
        "required",
        ["filing"],
        "disabled",
    ),
    "opposing-counsel": folder_contract(
        "opposing-counsel",
        ["profile", "filing", "approved-sources"],
        "required",
        ["filing"],
        "disabled",
    ),
    "drafting-false-arrest-complaints": folder_contract(
        "drafting-false-arrest-complaints",
        ["record", "authorities", "filing"],
        "optional",
        ["filing"],
        "disabled",
    ),
    "drafting-section-1983-complaints": folder_contract(
        "drafting-section-1983-complaints",
        ["record", "authorities", "filing"],
        "optional",
        ["filing"],
        "disabled",
    ),
    "drafting-section-1983-declarations-and-evidence": folder_contract(
        "drafting-section-1983-declarations-and-evidence",
        ["record", "authorities"],
        "optional",
        ["record"],
        "disabled",
    ),
    "drafting-section-1983-deposition-outlines": folder_contract(
        "drafting-section-1983-deposition-outlines",
        ["record", "authorities", "discovery"],
        "optional",
        ["record"],
        "disabled",
    ),
    "drafting-section-1983-meet-and-confer": folder_contract(
        "drafting-section-1983-meet-and-confer",
        ["discovery-audit", "served-discovery", "authorities", "conference-record"],
        "required",
        ["discovery-audit"],
        "disabled",
    ),
    "drafting-section-1983-rule-59e": folder_contract(
        "drafting-section-1983-rule-59e",
        ["record", "authorities", "filing"],
        "optional",
        ["filing"],
        "disabled",
    ),
    "drafting-section-1983-written-discovery": folder_contract(
        "drafting-section-1983-written-discovery",
        ["record", "authorities", "claim-map"],
        "optional",
        ["claim-map"],
        "disabled",
    ),
    "filing-ci": folder_contract(
        "filing-ci",
        [
            "filing-source",
            "filing-index",
            "record-reference",
            "exhibit",
            "docket-to-appendix",
            "verified-authority",
        ],
        "required",
        ["filing-source"],
        "disabled",
    ),
    "horan-bad-words": folder_contract(
        "horan-bad-words", ["filing"], "required", ["filing"], "disabled"
    ),
    "rrd": folder_contract(
        "rrd", ["motion", "record", "authorities"], "required", ["motion"], "disabled"
    ),
    "rrd-rule12": folder_contract(
        "rrd-rule12",
        ["motion", "record", "authorities"],
        "required",
        ["motion"],
        "disabled",
    ),
    "rrd-rule12-city": folder_contract(
        "rrd-rule12-city",
        ["motion", "record", "authorities"],
        "required",
        ["motion"],
        "disabled",
    ),
    "rrd-rule12-officers": folder_contract(
        "rrd-rule12-officers",
        ["motion", "record", "authorities"],
        "required",
        ["motion"],
        "disabled",
    ),
    "section-1983-drafting": folder_contract(
        "section-1983-drafting",
        ["record", "authorities", "strategy", "filing"],
        "optional",
        ["filing"],
        "authorized",
    ),
    "studying-rule-59e-decisions": folder_contract(
        "studying-rule-59e-decisions",
        ["decisions", "authorities"],
        "optional",
        ["decisions"],
        "authorized",
    ),
}
CONTRIBUTION_RULES = (
    (
        "Use one story per stacked branch.",
        "Do not use one story per stacked branch.",
    ),
    (
        "Write the RED failing test before GREEN implementation.",
        "Write GREEN implementation before the RED failing test.",
    ),
    (
        "Refactor only while the tests remain green.",
        "Refactor while the tests are failing.",
    ),
    (
        "Complete OpenSpec design, tasks, verification, retrospective, and archive artifacts.",
        "Do not complete OpenSpec design, tasks, verification, retrospective, and archive artifacts.",
    ),
    (
        "Automation must not silently select plaintiff decisions, litigation strategy, or legal conclusions.",
        "Automation may silently select plaintiff decisions, litigation strategy, or legal conclusions.",
    ),
    ("Measurement is feedback, never a verdict.", "Measurement is a verdict."),
    (
        "Score deltas and judgment-based evaluations prompt review and do not decide legal quality, filing readiness, or human judgment.",
        "Score deltas and judgment-based evaluations decide legal quality, filing readiness, and human judgment.",
    ),
    ("Prefer self-documenting code.", "Do not prefer self-documenting code."),
    (
        "Refactor before adding a comment.",
        "Do not refactor before adding a comment.",
    ),
    (
        "A necessary comment is short and clear and references an ADR or recorded decision when practical.",
        "A necessary comment may be long and unclear and need not reference an ADR or recorded decision.",
    ),
    (
        "Run `npm run validate` before release.",
        "Do not run `npm run validate` before release.",
    ),
    ("A push to `main` is not publication.", "A push to `main` is publication."),
    (
        "Release only with immutable semantic-version tags.",
        "Do not use immutable semantic-version tags.",
    ),
    (
        "The validator checks deterministic boundaries, not subjective prose, comment, test, or legal quality.",
        "The validator checks subjective prose, comment, test, and legal quality.",
    ),
)
CONTRIBUTION_OWNER_LINKS = {
    "GOVERNANCE.md": "GOVERNANCE.md",
    "PUBLISHING.md": "PUBLISHING.md",
}
CONTRIBUTION_DUPLICATED_OWNER_MARKERS = (
    "## protected legal gates",
    "## releasing a validated version",
    "gh workflow run release.yml",
    "verification, factual and authority source, permission, filing-readiness",
)
QUALITY_CONTROL_RULES = (
    (
        "An independent quality-control stage is non-mutating.",
        "An independent quality-control stage may mutate an artifact under review.",
    ),
    (
        "It may read designated artifacts and return only its designated report or result for trusted-host publication.",
        "It may write changes to an artifact under review.",
    ),
    (
        "It must not edit, overwrite, correct, regenerate, or otherwise modify an artifact under review.",
        "It may edit, overwrite, correct, regenerate, or otherwise modify an artifact under review.",
    ),
    (
        "A combined instruction to audit and fix does not authorize same-stage mutation.",
        "A combined instruction to audit and fix authorizes same-stage mutation.",
    ),
    (
        "Deadline pressure, sunk cost, claimed prior approval, and contrary workflow instructions do not override this boundary.",
        "Deadline pressure, sunk cost, claimed prior approval, or contrary workflow instructions may override this boundary.",
    ),
    (
        "Recommendations, proposed language, corrections, and copy-ready replacements are advisory only and do not authorize implementation.",
        "Recommendations, proposed language, corrections, and copy-ready replacements authorize implementation.",
    ),
    (
        "Remediation requires a separately authorized drafting or revision stage.",
        "Remediation may occur during the independent quality-control stage.",
    ),
    (
        "Create a new version when versioning applies.",
        "Overwrite the current version when versioning applies.",
    ),
    (
        "A new read-only quality-control stage must verify the remediated artifact.",
        "The prior quality-control result transfers to the remediated artifact.",
    ),
    (
        "An internal self-check inside an explicitly authorized drafting or revision stage may guide edits within that stage, but it is not an independent quality-control result.",
        "An internal drafting self-check is an independent quality-control result.",
    ),
)
QUALITY_CONTROL_REPORT_RULES = (
    (
        "Before review, an independent quality-control stage must select exactly one artifact through its declared input roles and target policy.",
        "An independent quality-control stage may select an artifact outside its declared input roles or target policy.",
    ),
    (
        "It must propose exactly one unique append-immutable output-relative report beneath the caller-declared output folder.",
        "It may propose a mutable or non-unique report outside the caller-declared output folder.",
    ),
    (
        "A missing, ambiguous, nonexistent, or out-of-role target must fail closed without a fallback write.",
        "A missing, ambiguous, nonexistent, or out-of-role target may use a fallback write.",
    ),
    (
        "The report path must reject absolute paths, traversal, symlink escapes, and existing destinations.",
        "The report path may be absolute, traverse, follow symlink escapes, or replace an existing destination.",
    ),
    (
        "Only the trusted host may publish the report through the shared output boundary.",
        "The skill or helper may publish the report directly.",
    ),
    (
        "The trusted host accepts quality-control publication only from an invocation bound to the installed skill's target policy and approved target roles; it rejects an unbound invocation or a target outside those approved roles.",
        "The trusted host may publish from an unbound invocation or a target outside the installed skill's approved roles.",
    ),
    (
        "Prior quality-control reports must not become implicit input.",
        "Prior quality-control reports may become implicit input.",
    ),
    (
        "A report may be reviewed only when that exact report is expressly present in a declared input role and selected consistently with the reviewing skill's target policy.",
        "A report may be reviewed from ambient output without a declared input role or target.",
    ),
    (
        "The reviewing stage must propose a different new append-immutable report for trusted-host publication.",
        "The reviewing stage may update or replace the report under review.",
    ),
    (
        "Existing reports are immutable and must not be edited, overwritten, replaced, renamed, or deleted.",
        "Existing reports may be edited, overwritten, replaced, renamed, or deleted.",
    ),
    (
        "The trusted host prefixes the report with the canonical quality-control metadata envelope containing the skill and version, filtered logical input roles and reviewed artifact hashes, selected target role, relative path, SHA-256 fingerprint, and byte size, quality-control kind, UTC run time, run ID, scope, approved source identities, result, failed findings, passing-but-suboptimal recommendations, and terminal run-manifest identity.",
        "The report may omit its skill version, reviewed artifact hashes, target fingerprint, findings, recommendations, or run-manifest identity.",
    ),
    (
        "The trusted host derives the report path as `quality-control-reports/<check-kind>-<utc-run-time>-<run-id>.md` and publishes exactly one report through the shared output writer.",
        "The skill may choose any report path or publish more than one report.",
    ),
    (
        "Generated reports beneath `quality-control-reports/` are excluded from the reviewed-input manifest and fingerprint unless one exact report is the explicit target; selecting one report does not include sibling or older reports.",
        "Generated reports beneath `quality-control-reports/` are always included in the reviewed-input manifest and fingerprint.",
    ),
    (
        "The canonical quality-control metadata envelope identifies a generated report even when the report directory itself is a declared input root.",
        "A report is not generated when its declared input root omits the `quality-control-reports/` path segment.",
    ),
    (
        "A quality-control run ID must be a canonical lowercase UUIDv4; weak, malformed, or reused identities fail closed before publication.",
        "A quality-control run may use a weak, malformed, or reused identity.",
    ),
    (
        "The quality-control run is complete only after both report bytes and the terminal success manifest are durable and incomplete state is absent.",
        "The quality-control run may report completion before its report or terminal success manifest is durable.",
    ),
    (
        "The skill returns report content and structured findings; it does not build the canonical metadata envelope or publish output.",
        "The skill builds the canonical metadata envelope and publishes output directly.",
    ),
    (
        "Separate failed findings from passing-but-suboptimal observations.",
        "Combine failed findings and passing-but-suboptimal observations without distinction.",
    ),
    (
        "Recommendations, proposed language, and copy-ready replacements for failures or passing-but-suboptimal observations are advisory and do not authorize implementation.",
        "Report recommendations and copy-ready replacements authorize implementation.",
    ),
)
FOLDER_SCOPE_RULES = (
    (
        "Only caller-declared input folders are available and recursively read-only.",
        "Any input folder is available and writable.",
    ),
    (
        "Writes occur only beneath the caller-declared output folder.",
        "Writes may occur outside the caller-declared output folder.",
    ),
    (
        "Internet is used only when that skill expressly authorizes it.",
        "Internet may be used without that skill expressly authorizing it.",
    ),
    (
        "Execution stops before reading case material if the host cannot enforce the filesystem and network boundary.",
        "Execution may read case material when the host cannot enforce the filesystem and network boundary.",
    ),
)
QUALITY_CONTROL_TRIGGER = re.compile(
    r"(?:\buse when\b.{0,120}\b(?:independently\s+)?(?:auditing|reviewing|"
    r"verifying|evaluating|checking|assessing|performing quality control|"
    r"performing an? assessment|conducting (?:an? )?(?:independent )?assessment)\b|"
    r"\bneeds (?:an )?independent.{0,60}\breview\b|"
    r"\bneeds to (?:independently )?(?:audit|review|verify|evaluate|check)\b|"
    r"\bneeds to determine.{0,80}\bor audit\b|\bdrafts and audits\b|"
    r"\bdrafting, revising, or auditing\b|\bchecker must run\b|"
    r"\buse for (?:an? )?independent (?:audit(?:ing)?|review(?:ing)?|verification|"
    r"evaluat(?:ing|ion)|check(?:ing)?|assessment)\b|"
    r"\bthis skill (?:independently (?:audits|reviews|verifies|evaluates|checks|assesses)|"
    r"performs (?:an? )?independent (?:audit|review|verification|evaluation|check|assessment))\b)",
    re.IGNORECASE,
)
PROHIBITED_QUALITY_CONTROL_PERMISSION = re.compile(
    r"\bindependent (?:quality-control stage|audit|review|verification|evaluation|assessment)"
    r".{0,100}\b(?:may|can|is authorized to|is permitted to) "
    r"(?:edit|modify|overwrite|correct|regenerate|revise|rewrite|fix|change|mutate)\b"
    r".{0,80}\b(?:artifact|draft|document)\b",
    re.IGNORECASE,
)
PROHIBITED_QUALITY_CONTROL_REPORT_PERMISSIONS = (
    re.compile(
        r"\bindependent audit.{0,80}\bmay save its report\b.{0,80}\bshared project folder\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\blatest audit report\b.{0,80}\bmay replace\b.{0,80}\bprevious report\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bprior audit reports\b.{0,80}\bincluded\b.{0,80}\bevery re-audit\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bresolve exactly one existing version-specific folder\b.{0,80}"
        r"\bdesignated project boundary\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bwrite exactly one new report\b.{0,100}"
        r"`?<version-folder>/audits/`?",
        re.IGNORECASE,
    ),
    re.compile(
        r"\bexclude `?audits/`? from review input\b",
        re.IGNORECASE,
    ),
)


def is_date(value):
    if not isinstance(value, str):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def is_https_url(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value)
        hostname = parsed.hostname
        parsed.port
    except ValueError:
        return False
    return (
        parsed.scheme == "https"
        and bool(hostname)
        and not any(character.isspace() for character in hostname)
    )


def is_nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def inside_root(root, value):
    if not is_nonblank(value):
        return False
    try:
        (root / value).resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def normalized(text):
    return " ".join(text.lower().split())


def markdown_links(text):
    prose = re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1\s*", "", text)
    return re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", prose)


def frontmatter_description(text):
    parts = text.split("---", 2)
    if len(parts) != 3:
        return ""
    description = []
    collecting = False
    for line in parts[1].splitlines():
        if line.startswith("description:"):
            collecting = True
            value = line.partition(":")[2].strip()
            if value not in {"", ">", ">-", "|", "|-"}:
                description.append(value.strip("\"'"))
            continue
        if collecting and line.startswith((" ", "\t")):
            description.append(line.strip().strip("\"'"))
            continue
        if collecting:
            break
    return " ".join(description)


def validate_registry(repository_root):
    errors = []
    registry_path = repository_root / "governance" / "rules-provenance.json"
    try:
        registry = json.loads(registry_path.read_text())
    except (OSError, json.JSONDecodeError):
        return ["invalid-registry"]
    if not isinstance(registry, dict):
        return ["invalid-registry"]
    sources = registry.get("sources")
    skills = registry.get("skills")
    if not isinstance(sources, list) or not isinstance(skills, list):
        return ["invalid-registry"]
    source_ids = set()
    for source in sources:
        if not isinstance(source, dict) or not is_nonblank(source.get("id")):
            errors.append("invalid-source")
            continue
        if source["id"] in source_ids:
            errors.append("duplicate-source-id")
        source_ids.add(source["id"])
        if not is_https_url(source.get("url")):
            errors.append("insecure-source-url")
        if not is_date(source.get("checked_on")):
            errors.append("invalid-date")
    discovered_names = sorted(path.parent.name for path in (repository_root / "skills").glob("*/SKILL.md"))
    names = []
    for skill in skills:
        if not isinstance(skill, dict):
            errors.append("skill-entry-mismatch")
            continue
        name = skill.get("name")
        names.append(name)
        mode = skill.get("rules_mode")
        if not isinstance(mode, str) or mode not in MODES:
            errors.append("invalid-rules-mode")
        if not is_date(skill.get("reviewed_on")):
            errors.append("invalid-date")
        if not is_nonblank(skill.get("rationale")):
            errors.append("rationale-required")
        if mode == "bundled-rules-dependent":
            ids = skill.get("source_ids")
            if not isinstance(ids, list) or not ids or not all(is_nonblank(item) for item in ids):
                errors.append(f"bundled-source-required: {name}")
            elif any(item not in source_ids for item in ids):
                errors.append(f"unknown-source-id: {name}")
            reference = skill.get("jurisdiction_reference")
            if not inside_root(repository_root, reference) or not (repository_root / reference).is_file():
                errors.append(f"jurisdiction-reference-required: {name}")
        if mode == "runtime-sourced":
            provenance = skill.get("output_provenance")
            if not isinstance(provenance, dict) or not is_nonblank(provenance.get("source_identity")):
                errors.append("runtime-source-identity-required")
            if not isinstance(provenance, dict) or not is_nonblank(provenance.get("checked_date")):
                errors.append("runtime-source-date-required")
    if sorted(name for name in names if isinstance(name, str)) != discovered_names or len(names) != len(discovered_names):
        errors.append("skill-entry-mismatch")
    return errors


def validate_policy(repository_root):
    try:
        policy = (repository_root / "GOVERNANCE.md").read_text().lower()
    except OSError:
        return ["governance-policy-missing"]
    required = (
        "strategy",
        "positions",
        "concessions",
        "requested\nrelief",
        "filing",
        "supported\nchoices",
        "consequence",
        "select none",
        "jurisdiction-specific propositions",
        "verified reference",
        "authoritative source provenance",
        "checked\ndate",
        "verification",
        "factual and authority source",
        "permission",
        "filing-readiness",
        "judgment-routing",
        "rules-provenance",
        "tool-ownership",
        "folder scope",
        "recursive input non-mutation",
        "output confinement",
        "declared internet policy",
        "explicit human review",
        "thin skill wrapper",
        "owning repository",
    )
    normalized = " ".join(policy.split())
    return [] if all(item.replace("\n", " ") in normalized for item in required) else ["governance-policy-language-missing"]


def validate_pull_request_template(repository_root):
    try:
        template = (repository_root / ".github" / "pull_request_template.md").read_text().lower()
    except OSError:
        return ["protected-review-language-missing"]
    normalized = " ".join(template.split())
    required = ("affected protected gate", "rationale", "explicit human review")
    return [] if all(item in normalized for item in required) else ["protected-review-language-missing"]


def validate_contribution_contract(repository_root):
    try:
        guide = (repository_root / "CONTRIBUTING.md").read_text()
    except OSError:
        return ["contribution-contract-language-missing"]
    contract = normalized(guide)
    if any(
        normalized(affirmative) not in contract or normalized(inversion) in contract
        for affirmative, inversion in CONTRIBUTION_RULES
    ):
        return ["contribution-contract-language-missing"]
    if any(marker in contract for marker in CONTRIBUTION_DUPLICATED_OWNER_MARKERS):
        return ["contribution-contract-language-missing"]
    links = markdown_links(guide)
    for label, destination in CONTRIBUTION_OWNER_LINKS.items():
        targets = [target for link_label, target in links if link_label == label]
        if not targets:
            return ["contribution-contract-language-missing"]
        for target in targets:
            if target != destination or not inside_root(repository_root, target):
                return ["contribution-contract-language-missing"]
            if not (repository_root / target).is_file():
                return ["contribution-contract-language-missing"]
    return []


def quality_control_contract_missing(text):
    contract = normalized(text)
    return PROHIBITED_QUALITY_CONTROL_PERMISSION.search(contract) is not None or any(
        normalized(affirmative) not in contract or normalized(inversion) in contract
        for affirmative, inversion in QUALITY_CONTROL_RULES
    )


def quality_control_report_contract_missing(text):
    contract = normalized(text)
    return any(
        pattern.search(contract) is not None
        for pattern in PROHIBITED_QUALITY_CONTROL_REPORT_PERMISSIONS
    ) or any(
        normalized(affirmative) not in contract or normalized(inversion) in contract
        for affirmative, inversion in QUALITY_CONTROL_REPORT_RULES
    )


def validate_quality_control_contracts(repository_root):
    errors = []
    try:
        policy = (repository_root / "GOVERNANCE.md").read_text()
    except OSError:
        return ["quality-control-contract-language-missing: GOVERNANCE.md"]
    if quality_control_contract_missing(policy):
        errors.append("quality-control-contract-language-missing: GOVERNANCE.md")
    if quality_control_report_contract_missing(policy):
        errors.append(
            "quality-control-report-contract-language-missing: GOVERNANCE.md"
        )
    for path in sorted((repository_root / "skills").glob("*/SKILL.md")):
        try:
            text = path.read_text()
        except OSError:
            errors.append(f"quality-control-contract-unreadable: {path.parent.name}")
            continue
        if QUALITY_CONTROL_TRIGGER.search(frontmatter_description(text)):
            if quality_control_contract_missing(text):
                errors.append(
                    f"quality-control-contract-language-missing: {path.parent.name}"
                )
            if quality_control_report_contract_missing(text):
                errors.append(
                    "quality-control-report-contract-language-missing: "
                    f"{path.parent.name}"
                )
    return errors


def folder_scope_contract_missing(text):
    contract = normalized(text)
    return any(
        normalized(affirmative) not in contract or normalized(inversion) in contract
        for affirmative, inversion in FOLDER_SCOPE_RULES
    )


def validate_folder_scope_contracts(repository_root):
    errors = []
    for path in sorted((repository_root / "skills").glob("*/SKILL.md")):
        try:
            text = path.read_text()
        except OSError:
            errors.append(
                f"folder-scope-contract-language-missing: {path.parent.name}"
            )
            continue
        if folder_scope_contract_missing(text):
            errors.append(
                f"folder-scope-contract-language-missing: {path.parent.name}"
            )
    return errors


def validate_folder_contract_document(document, expected_skill):
    if not isinstance(document, dict) or set(document) != FOLDER_CONTRACT_FIELDS:
        return ["invalid-folder-contract-shape"]

    errors = []
    if type(document.get("version")) is not int or document.get("version") != 1:
        errors.append("invalid-folder-contract-version")
    if document.get("skill") != expected_skill:
        errors.append("skill-folder-contract-mismatch")

    roles = document.get("input_roles")
    if (
        not isinstance(roles, list)
        or not roles
        or any(not isinstance(role, str) or not SAFE_ROLE.fullmatch(role) for role in roles)
        or len(roles) != len(set(roles))
    ):
        errors.append("invalid-folder-contract-input-roles")

    target = document.get("target")
    target_valid = isinstance(target, dict) and set(target) == {"policy", "roles"}
    if target_valid:
        policy = target["policy"]
        target_roles = target["roles"]
        target_valid = (
            policy in {"required", "optional", "none"}
            and isinstance(target_roles, list)
            and all(
                isinstance(role, str) and SAFE_ROLE.fullmatch(role)
                for role in target_roles
            )
            and len(target_roles) == len(set(target_roles))
            and isinstance(roles, list)
            and all(role in roles for role in target_roles)
            and ((policy == "none" and not target_roles) or (policy != "none" and target_roles))
        )
    if not target_valid:
        errors.append("invalid-folder-contract-target")

    internet = document.get("internet")
    if isinstance(internet, str):
        internet_valid = internet in {"disabled", "authorized"}
    else:
        internet_valid = (
            isinstance(internet, dict)
            and bool(internet)
            and all(
                isinstance(operation, str) and SAFE_ROLE.fullmatch(operation)
                for operation in internet
            )
            and all(
                policy in {"disabled", "authorized"}
                for policy in internet.values()
            )
        )
    if not internet_valid:
        errors.append("invalid-folder-contract-internet")
    if document.get("output") != {"mode": "append-immutable"}:
        errors.append("invalid-folder-contract-output")

    expected = APPROVED_FOLDER_CONTRACTS.get(expected_skill)
    if expected is not None and document != expected:
        errors.append("skill-folder-contract-mismatch")
    return list(dict.fromkeys(errors))


def validate_skill_folder_contracts(repository_root):
    errors = []
    entrypoints = sorted((repository_root / "skills").glob("*/SKILL.md"))
    discovered = {entrypoint.parent.name for entrypoint in entrypoints}
    approved = set(APPROVED_FOLDER_CONTRACTS)
    errors.extend(
        f"approved-skill-folder-contract-missing: {skill}"
        for skill in sorted(approved - discovered)
    )
    errors.extend(
        f"unapproved-skill-folder-contract: {skill}"
        for skill in sorted(discovered - approved)
    )
    for entrypoint in entrypoints:
        skill = entrypoint.parent.name
        contract_path = entrypoint.parent / "references" / "folder-contract.json"
        if not contract_path.is_file():
            errors.append(f"skill-folder-contract-missing: {skill}")
            continue
        try:
            document = json.loads(contract_path.read_text())
        except (OSError, json.JSONDecodeError):
            errors.append(f"skill-folder-contract-unreadable: {skill}")
            continue
        errors.extend(
            f"{finding}: {skill}"
            for finding in validate_folder_contract_document(document, skill)
        )
        try:
            entrypoint_text = entrypoint.read_text().lower()
        except OSError:
            entrypoint_text = ""
        if "[folder contract](references/folder-contract.json)" not in entrypoint_text:
            errors.append(f"skill-folder-contract-link-missing: {skill}")
    return errors


def validate_source_documented_folder_guidance(repository_root):
    errors = []
    guide = repository_root / "SOURCE_DOCUMENTED_FOLDERS.md"
    try:
        guide_text = normalized(guide.read_text())
    except OSError:
        return ["source-documented-folder-guide-missing"]
    required = (
        "declared input folders",
        "recursive read-only",
        "explicit output folder",
        "domain-owned yaml",
        "source.yaml",
        "folder-relative path",
        "sha-256",
        "protected behavior",
    )
    if any(item not in guide_text for item in required):
        errors.append("source-documented-folder-guide-incomplete")
    for skill in SOURCE_DOCUMENTED_SKILLS:
        skill_root = repository_root / "skills" / skill
        reference = skill_root / "references" / "source-documented-folders.md"
        try:
            entrypoint = (skill_root / "SKILL.md").read_text().lower()
            reference_text = normalized(reference.read_text())
            if (
                reference.is_symlink()
                or reference.resolve().parent != reference.parent.resolve()
            ):
                errors.append(f"source-documented-folder-reference-invalid: {skill}")
                continue
        except (OSError, RuntimeError):
            errors.append(f"source-documented-folder-reference-missing: {skill}")
            continue
        if (
            "[source-documented folders](references/source-documented-folders.md)"
            not in entrypoint
        ):
            errors.append(f"source-documented-folder-link-missing: {skill}")
        if any(
            item not in reference_text
            for item in (
                "recursive read-only input folders",
                "folder-relative path",
                "sha-256",
                "domain-owned yaml",
                "<output-folder>/temp/",
            )
        ):
            errors.append(f"source-documented-folder-reference-incomplete: {skill}")
    return errors


def validate_repository(repository_root):
    errors = []
    errors.extend(validate_registry(repository_root))
    errors.extend(validate_policy(repository_root))
    errors.extend(validate_pull_request_template(repository_root))
    errors.extend(validate_contribution_contract(repository_root))
    errors.extend(validate_quality_control_contracts(repository_root))
    errors.extend(validate_folder_scope_contracts(repository_root))
    errors.extend(validate_skill_folder_contracts(repository_root))
    errors.extend(validate_source_documented_folder_guidance(repository_root))
    return errors


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate_repository(root)
    if errors:
        print("\n".join(errors))
        return 1
    print("governance validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
