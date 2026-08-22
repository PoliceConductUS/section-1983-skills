"""Deterministic linter for the mechanical subset of the drafting rules.

Score is violations per 100 words. Lint a draft, revise, and lint again; the
delta between the two scores is the signal. The linter checks form only. It
cannot judge whether a fact is well pleaded.
"""

import json
import re
import sys
from pathlib import Path

from banned_terms import BONUS_WORDS, MORE_WORDS, TOP_FIFTY_WORDS

EXEMPT_PHRASES = (
    "clearly established",
    "clearly erroneous",
    "deliberate indifference",
    "deliberately indifferent",
    "under color of state law",
    "excessive force",
    "false arrest",
    "false imprisonment",
    "objectively reasonable",
    "objectively unreasonable",
    "serious medical needs",
    "serious medical need",
    "genuine dispute",
    "genuine issue",
    "actual damages",
    "actual malice",
    "actual knowledge",
    "gross negligence",
    "grossly negligent",
    "void for vagueness",
    "final policymaker",
    "final judgment",
    "general jurisdiction",
    "punitive damages",
    "active resistance",
    "materially similar",
    "reasonably trustworthy",
)
FORMAL_WORDS = (
    "begin", "begins", "commence", "commences", "initiate", "initiates",
    "originate", "utilize", "utilizes", "utilizing", "utilization",
    "leverage", "leverages", "leveraging", "facilitate", "facilitates",
    "ensure", "ensures", "ensuring", "prior to", "subsequent to", "obtain",
    "obtains", "acquire", "acquires", "demonstrate", "demonstrates",
    "additionally", "furthermore", "moreover", "comprehensive",
    "comprehensively", "aforementioned", "henceforth", "therein", "whilst",
    "amongst", "numerous", "myriad", "plethora", "in order to",
    "a variety of", "in the event that", "due to the fact that", "regarding",
    "concerning",
)

MARKETING_ADJECTIVES = (
    "seamless", "seamlessly", "robust", "powerful", "cutting-edge",
    "effortless", "effortlessly", "world-class", "next-generation",
    "revolutionary", "blazing", "lightning-fast", "elegant", "delightful",
    "turnkey", "best-in-class", "state-of-the-art", "game-changing",
    "first-class", "battle-tested", "enterprise-grade", "supercharge",
    "unlock", "unleash", "empower", "empowers",
)

PHRASAL_VERBS = (
    "spin up", "spin down", "reach out", "dive into", "kick off", "roll out",
    "tear down", "ramp up", "circle back", "drill down",
)

HEDGES = (
    "it is important to note", "it should be noted", "it is worth noting",
    "please note that", "as mentioned", "as noted above",
)

EMPTY_OPENERS = (
    "it is", "there are", "there is", "the nature of", "the fact that",
)

BE_VERB_PATTERN = r"(?:am|is|are|was|were|be|been|being)"

IRREGULAR_PARTICIPLE_PATTERN = (
    r"(?:done|made|sent|read|built|kept|held|set|put|run|written|shown"
    r"|given|taken|found|seen|known|thrown|drawn|searched|struck|beaten)"
)


def remove_exempt_phrases(text):
    lowered = text.lower().replace("\u2019", "'")
    for phrase in EXEMPT_PHRASES:
        lowered = lowered.replace(phrase, " ")
    return lowered


def split_sentences(text):
    stripped_lines = (line.strip() for line in text.split("\n"))
    joined = " ".join(line for line in stripped_lines if line)
    pieces = re.split(r"(?<=[.!?])\s+", joined)
    return [piece for piece in pieces if piece]


def count_words(text):
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/]*", text))


def compile_phrase_pattern(phrases):
    ordered = sorted(phrases, key=len, reverse=True)
    alternation = "|".join(re.escape(phrase) for phrase in ordered)
    return re.compile(r"(?<![a-z])(?:" + alternation + r")(?![a-z])")


TOP_FIFTY_PATTERN = compile_phrase_pattern(TOP_FIFTY_WORDS)
MORE_WORDS_PATTERN = compile_phrase_pattern(MORE_WORDS)
BONUS_PATTERN = compile_phrase_pattern(BONUS_WORDS)


def count_phrases(text, pattern):
    return len(pattern.findall(text))


def count_top_fifty_words(text):
    return count_phrases(remove_exempt_phrases(text), TOP_FIFTY_PATTERN)


def count_more_words(text):
    return count_phrases(remove_exempt_phrases(text), MORE_WORDS_PATTERN)


def count_bonus_words(text):
    return count_phrases(remove_exempt_phrases(text), BONUS_PATTERN)


def count_formal_words(text):
    return count_phrases(remove_exempt_phrases(text), FORMAL_WORDS_PATTERN)


def count_marketing_adjectives(text):
    return count_phrases(text.lower(), MARKETING_ADJECTIVES_PATTERN)


def count_phrasal_verbs(text):
    return count_phrases(text.lower(), PHRASAL_VERBS_PATTERN)


def count_hedges(text):
    return count_phrases(text.lower(), HEDGES_PATTERN)


def count_empty_openers(text):
    sentences = split_sentences(text.lower())
    return sum(
        1
        for sentence in sentences
        if any(sentence.startswith(opener + " ") for opener in EMPTY_OPENERS)
    )


def count_semicolons(text):
    return text.count(";")


def count_em_dashes(text):
    return text.count("\u2014") + text.count("\u2013")


def count_contractions(text):
    return len(re.findall(r"\b\w+['\u2019](?:t|re|ve|ll|d|m)\b", text))


def count_passive_voice(text):
    pattern = (
        r"\b" + BE_VERB_PATTERN + r"\s+(?:\w+ed|"
        + IRREGULAR_PARTICIPLE_PATTERN + r")\b"
    )
    return len(re.findall(pattern, text, re.IGNORECASE))


def count_long_sentences(text):
    return sum(1 for sentence in split_sentences(text) if count_words(sentence) > 25)


FORMAL_WORDS_PATTERN = compile_phrase_pattern(FORMAL_WORDS)
MARKETING_ADJECTIVES_PATTERN = compile_phrase_pattern(MARKETING_ADJECTIVES)
PHRASAL_VERBS_PATTERN = compile_phrase_pattern(PHRASAL_VERBS)
HEDGES_PATTERN = compile_phrase_pattern(HEDGES)
EXEMPT_PATTERN = compile_phrase_pattern(EXEMPT_PHRASES)
CASE_CITATION_PATTERN = re.compile(
    r"\b\d+\s+(?:U\.S\.|S\.\s?Ct\.|F\.(?:2d|3d|4th)|"
    r"F\.\s?Supp\.\s?(?:2d|3d)?|S\.W\.(?:2d|3d))\s+\d+\b",
    re.IGNORECASE,
)
LONG_SENTENCE_DENSITY_THRESHOLD = 2
CASE_CITATION_DENSITY_THRESHOLD = 4


CHECKS = {
    "top_fifty_word": count_top_fifty_words,
    "more_word": count_more_words,
    "bonus_word": count_bonus_words,
    "formal_word": count_formal_words,
    "marketing_adjective": count_marketing_adjectives,
    "phrasal_verb": count_phrasal_verbs,
    "hedge": count_hedges,
    "empty_opener": count_empty_openers,
    "semicolon": count_semicolons,
    "em_dash": count_em_dashes,
    "contraction": count_contractions,
    "passive_voice": count_passive_voice,
    "long_sentence": count_long_sentences,
}


def paragraphs_with_locations(text):
    paragraphs = []
    lines = text.splitlines()
    current = []
    start_line = None

    for line_number, line in enumerate(lines, start=1):
        if line.strip():
            if start_line is None:
                start_line = line_number
            current.append(line)
            continue
        if current:
            paragraphs.append(("\n".join(current), start_line, line_number - 1))
            current = []
            start_line = None

    if current:
        paragraphs.append(("\n".join(current), start_line, len(lines)))

    return paragraphs


def bounded_excerpt(text, limit=240):
    compact = " ".join(text.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def location_fields(artifact, paragraph_number, start_line, end_line):
    return {
        "artifact": artifact,
        "paragraph": paragraph_number,
        "start_line": start_line,
        "end_line": end_line,
    }


def paragraph_findings(paragraphs, artifact):
    findings = []
    for paragraph_number, (text, start_line, end_line) in enumerate(
        paragraphs, start=1
    ):
        for check_name, check in CHECKS.items():
            count = check(text)
            if not count:
                continue
            finding = {
                "finding_id": f"paragraph-{paragraph_number}:{check_name}",
                "check": check_name,
                **location_fields(
                    artifact, paragraph_number, start_line, end_line
                ),
                "count": count,
                "excerpt": bounded_excerpt(text),
                "classification": "unexempted_violation",
            }
            findings.append(finding)
    return findings


def paragraph_exemptions(paragraphs, artifact):
    exemptions = []
    for paragraph_number, (text, start_line, end_line) in enumerate(
        paragraphs, start=1
    ):
        lowered = text.lower().replace("\u2019", "'")
        occurrences = {}
        for match in EXEMPT_PATTERN.finditer(lowered):
            phrase = match.group(0)
            occurrences[phrase] = occurrences.get(phrase, 0) + 1
            exemption = {
                "exemption_id": (
                    f"paragraph-{paragraph_number}:controlling-term:"
                    f"{phrase.replace(' ', '-')}:{occurrences[phrase]}"
                ),
                **location_fields(
                    artifact, paragraph_number, start_line, end_line
                ),
                "phrase": phrase,
                "classification": "controlling_term_of_art",
            }
            exemptions.append(exemption)
    return exemptions


def paragraph_warnings(paragraphs, artifact):
    warnings = []
    for paragraph_number, (text, start_line, end_line) in enumerate(
        paragraphs, start=1
    ):
        observed = (
            ("long_sentence_density", count_long_sentences(text), LONG_SENTENCE_DENSITY_THRESHOLD),
            (
                "case_citation_density",
                len(CASE_CITATION_PATTERN.findall(text)),
                CASE_CITATION_DENSITY_THRESHOLD,
            ),
        )
        for check_name, count, threshold in observed:
            if count < threshold:
                continue
            warning = {
                "warning_id": f"paragraph-{paragraph_number}:{check_name}",
                "check": check_name,
                **location_fields(
                    artifact, paragraph_number, start_line, end_line
                ),
                "observed": count,
                "threshold": threshold,
                "classification": "review_heuristic",
            }
            warnings.append(warning)
    return warnings


def lint(text, artifact="<memory>"):
    paragraphs = paragraphs_with_locations(text)
    findings = paragraph_findings(paragraphs, artifact)
    violations = {
        name: sum(
            finding["count"] for finding in findings if finding["check"] == name
        )
        for name in CHECKS
    }
    words = count_words(text) or 1
    total = sum(violations.values())

    return {
        "words": words,
        "violations": violations,
        "total": total,
        "total_per_hundred_words": round(total * 100.0 / words, 2),
        "findings": findings,
        "exemptions": paragraph_exemptions(paragraphs, artifact),
        "warnings": paragraph_warnings(paragraphs, artifact),
    }


def lint_paths(paths):
    return {path: lint(Path(path).read_text(), artifact=path) for path in paths}


def format_report(reports):
    return json.dumps(reports, indent=2)


def main(arguments):
    reports = (
        lint_paths(arguments)
        if arguments
        else lint(sys.stdin.read(), artifact="<stdin>")
    )
    print(format_report(reports))


if __name__ == "__main__":
    main(sys.argv[1:])
