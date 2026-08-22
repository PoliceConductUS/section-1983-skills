# The writing system

One system, merged from ASD-STE100 Simplified Technical English (via the
ste-writing skill) and the legal editing guides (Horan, _Bad Words_; McAlpin,
_Beyond the First Draft_). Source tags: [STE], [Horan], [McAlpin].

## Precedence rule

Bans stack: if any source bans a word, phrase, or construction, it is banned.
Advice conflicts do not stack: where one source recommends what another forbids,
ASD-STE100 controls. Known applications of the rule:

- Voice and euphony. Legal style prizes language "pleasing to the ear." STE
  strips voice on purpose. STE controls: plain, dry, and repetitive beats varied
  and musical. Repeating "Officer Doe" eleven times is correct; elegant
  variation is a defect, not a style.
- Vocabulary: the own-voice/law's-voice split. STE's short-common-word
  substitutions control everything written in the writer's own voice, which
  means the factual narrative, most of a complaint ("show," not "demonstrate";
  "before," not "prior to"). Legal standards and elements are the law's voice:
  state them in the controlling authority's words, quoted or closely tracked
  with a citation, and quoted matter is exempt. The split is the whole rule. A
  formal word in the facts section is a violation. A paraphrased standard in a
  Count is a missed citation.
- Sentence caps. STE's numeric caps (20 words for an instruction, 25 for a
  descriptive sentence; a complaint's allegations are descriptive) control over
  the guides' softer "write shorter" advice.
- Terms of art. STE permits technical names outside its dictionary. Legal terms
  of art ("clearly established," "deliberate indifference," "under color of
  state law") are technical names, so keeping their required wording is
  STE-compliant, not an exception to it.

## WORDS

- One name for one thing; one meaning for one word. [STE]
- Use the short common word. Substitution table in `banned-words.md`. [STE]
- Delete adjectives and adverbs unless the sentence loses a fact without them.
  An intensifier signals overstatement; if you must say something is clear, it
  usually is not. Replace the modifier with the fact that tempted you to use it.
  [Horan]
- No legalese, no five-cent words, no SAT words that send a judge to a
  dictionary. [Horan]
- No marketing adjectives. [STE]
- Choose words that are accurate and consistent across the document; do not
  switch synonyms mid-stream. [McAlpin] [STE]
- American spelling. [STE]

## VERBS

- Active voice with a named actor. In a complaint, passive voice hides the
  defendant. [STE] [McAlpin]
- Use a verb for the action; undo nominalizations ("searched," not "performed a
  search"). [STE] [McAlpin]
- Concrete subjects: no empty abstract nouns or "It is / There are" openers.
  [McAlpin]
- No vague verbs where a concrete verb exists. [McAlpin]
- No stacked auxiliaries; no "-ing" main verb where a simple tense works. [STE]
- No phrasal verbs from the banned list. [STE]

## SENTENCES

- One point per sentence; in a complaint, one factual allegation per sentence
  and per numbered paragraph (Rule 10(b) harmony). [STE]
- Caps: 25 words for allegations and other descriptive prose; 20 words for any
  instruction-form sentence. [STE]
- Keep subject and verb close together; fix misplaced, dangling, and squinting
  modifiers. [McAlpin]
- No contractions; use articles (a, an, the, this, these). [STE]
- Pronouns: every pronoun needs an unambiguous, nearby antecedent that agrees in
  number. When in doubt, repeat the noun. [McAlpin]

## PUNCTUATION

- No semicolons: write two sentences, or use lettered subparagraphs. [STE]
- No exclamation marks. [Horan]
- No em dashes or en dashes. [project rule, per the source repo's note]
- Standard commas, colons, quotation marks, and apostrophes per the McAlpin
  polish checklist; when a comma rule is debatable, recast the sentence so the
  question disappears. [McAlpin]

## STRUCTURE

- One topic per paragraph, six sentences maximum. [STE]
- Every section and every argument opens with an introduction; every paragraph
  opens with a topic sentence. [McAlpin]
- Transitions between paragraphs are substantive (repeat the idea being carried
  forward), not decorative ("moreover" is banned anyway). [McAlpin]
- For steps or lists, use a numbered vertical list, one item per entry, a
  condition before its command. In a complaint this becomes: numbered
  paragraphs, lettered subparagraphs in the prayer for relief. [STE]

## REGISTER

- No rhetorical questions: state the point as a declarative sentence and answer
  it with a fact. [Horan]
- No weasel assurances ("believe me," "the truth is," "speaks for itself"): an
  assertion that needs vouching needs a record cite instead. [Horan]
- No footnotes unless there is a strong reason for one. [Horan]
- Show, do not tell. Plead the dispassionate chronology and let the court write
  the conclusion in its own order. [Horan]
- Understate. The dry version of the sentence is the forceful one. [Horan]
- Civility is a hard constraint: write nothing you would not say to opposing
  counsel's face in open court. Hyperbole is inversely proportional to
  substance, and judges know it. [Horan]
- Write only the requested text: no preamble, no summary, no closing remarks
  around a drafting task. [STE]

## PARTY POSITIONS AND CONCESSIONS

- No concession by default. Do not agree with an adverse fact, characterization,
  element, inference, or legal conclusion without express user approval of the
  exact proposition.
- Attribute an adverse characterization to its speaker or filing. Do not repeat
  that characterization in the drafter's own voice as a fact.
- State the user's position affirmatively. Use the supported facts and source
  limits that advance that position.
- Do not speculate against the client. Do not add a caveat such as "may bear
  on," "could support," or "does not prove that no" merely to sound balanced.
- Do not convert an unclear, incomplete, or occluded record into an adverse
  inference. State what the source shows and what it does not show.
- Omit a point that does not require a response without conceding it. Silence
  does not authorize agreement.
- Treat a hypothetical adverse premise as a potential concession. Use it only
  after the user approves the exact premise and the reason for using it.
- If the sources conflict, identify the conflict for the user. Do not resolve
  the conflict against the user's position.
- If candor or accuracy may require an adverse admission, stop drafting that
  passage and ask for the user's express approval.

## Self-edit pass (run in order, before the linter)

1. Any affirmative or implied concession? Delete it unless the user approved the
   exact proposition.
2. Any adverse characterization in the drafter's own voice? Attribute it to its
   source and state the user's position.
3. Any caveat or speculation that favors another party? Delete it.
4. Any sentence over its cap? Split it.
5. Any adjective or adverb? Delete it unless a fact disappears with it.
6. Any word on the banned list? Substitute the plain word.
7. Any passive voice with a known actor? Name the actor.
8. Any nominalization, vague verb, or empty opener? Recast with a concrete
   subject and a concrete verb.
9. Same thing named two ways? Pick one name everywhere.
10. Any semicolon, em dash, or contraction? Remove it.
11. Any paragraph with more than one set of circumstances? Split it.
12. Run `scripts/draft_lint.py`, revise, and rerun it. The score delta is
    editing feedback only, never a merits verdict, legal-sufficiency decision,
    or filing-readiness decision. Target zero unexempted violations. Reconcile
    every residual hit exactly once as an unexempted violation, an accurate
    quotation verified against its approved source, or a controlling term of art
    supported by the linter exemption record. Repair every unexempted violation.
    Review warnings separately as review heuristics; they do not change the
    score or establish filing readiness.

The full _Bad Words_ inventory (Top 50, additional words and phrases, and the
bonus lists) is merged into `banned-words.md` and enforced by the linter. The
recurring rationales behind those entries — wordiness, obscurity, overstatement,
ambiguity, weasel words, incivility — are the rules above.
