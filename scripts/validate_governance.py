import json
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


MODES = {"rules-independent", "runtime-sourced", "bundled-rules-dependent"}


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


def validate_repository(repository_root):
    errors = []
    errors.extend(validate_registry(repository_root))
    errors.extend(validate_policy(repository_root))
    errors.extend(validate_pull_request_template(repository_root))
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
