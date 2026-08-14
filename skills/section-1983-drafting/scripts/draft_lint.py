"""Deterministic linter for the mechanical subset of the drafting rules.

Score is violations per 100 words. Lint a draft, revise, and lint again; the
delta between the two scores is the signal. The linter checks form only. It
cannot judge whether a fact is well pleaded.
"""

import json
import re
import sys

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


def lint(text):
    violations = {name: check(text) for name, check in CHECKS.items()}
    words = count_words(text) or 1
    total = sum(violations.values())

    return {
        "words": words,
        "violations": violations,
        "total": total,
        "total_per_hundred_words": round(total * 100.0 / words, 2),
    }


def lint_paths(paths):
    return {path: lint(open(path).read()) for path in paths}


def format_report(reports):
    return json.dumps(reports, indent=2)


def main(arguments):
    reports = lint_paths(arguments) if arguments else lint(sys.stdin.read())
    print(format_report(reports))


if __name__ == "__main__":
    main(sys.argv[1:])
