# Authorities protocol

Citations decide these documents, and a wrong citation costs more than a missing
one: courts sanction parties for fabricated or mischaracterized authority, and a
pro se filing gets no benefit of the doubt. This protocol governs where
citations come from.

## Source hierarchy

Use the first available source, in this order:

1. Approved authority material inside the declared `authorities` input role.
   Scope every search to the forum: binding authority for that district and
   circuit first, then persuasive in-circuit district decisions, then persuasive
   out-of-circuit authority, labeled as such.
2. Primary sources retrieved through the invocation's authorized internet
   connection. Verify identity, proposition, binding scope, pinpoint, date, and
   later history before treating a citation as verified.
3. General legal knowledge, flagged. Without a verified source, a case may be
   cited only with a `[VERIFY]` marker after the citation, and the draft must
   end with a list of every marked citation and the instruction to confirm each
   one, including that it exists, says what the draft claims, and remains good
   law, before filing.

## Rules regardless of source

- Treat legal-AI, RAG, semantic-search, citator, snippet, and generated research
  as a retrieval lead until an independent audit verifies the exact source. A
  real citation, working link, source list, or positive treatment symbol does
  not establish proposition support or current applicability.
- Split every material generated or filing-near statement into atomic
  propositions before authority approval. Verify each atomic proposition against
  the exact source, pinpoint, context, qualifiers, jurisdiction, date, posture,
  precedential force, and source voice. One citation may support several
  propositions only when it independently supports every one.
- Distinguish majority holding, court dicta, party argument, lower-court ruling
  under review, factual or procedural background, concurrence, dissent, and
  quoted secondary authority. Do not attribute one voice to another.
- Never invent a citation, a quotation, a pin cite, or a parenthetical. An
  argument without a citation is weaker; an argument with a false one is
  sanctionable and can sink the case.
- Binding before persuasive, always. Identify the circuit and district before
  searching, and say which court each cited case comes from when it is not
  binding.
- Quotations are transcribed from the source, never reconstructed. If the source
  text is unavailable, paraphrase and cite without quotation marks.
- Standards and elements are the law's voice: recite them in the controlling
  authority's words with a citation, per the writing system's precedence rule.
- One proposition, one best citation. String cites spend the reader's attention;
  pick the binding or most recent authority and stop.

## Authorities input expectations

Material supplied in `authorities` should identify the jurisdiction, verified
authorities, binding scope, supported proposition, pinpoint, and verification
date. Missing metadata is a gap; do not search undeclared folders for a
fallback.
