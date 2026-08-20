import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


MODES = {"rules-independent", "runtime-sourced", "bundled-rules-dependent"}
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


def validate_repository(repository_root):
    errors = []
    errors.extend(validate_registry(repository_root))
    errors.extend(validate_policy(repository_root))
    errors.extend(validate_pull_request_template(repository_root))
    errors.extend(validate_contribution_contract(repository_root))
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
