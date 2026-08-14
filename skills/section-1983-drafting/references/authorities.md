# Authorities protocol

Citations decide these documents, and a wrong citation costs more than a
missing one: courts sanction parties for fabricated or mischaracterized
authority, and a pro se filing gets no benefit of the doubt. This protocol
governs where citations come from.

## Source hierarchy

Use the first available source, in this order:

1. A verified-authorities tool. If an MCP tool for searching a curated
   authorities collection is available (a tool that returns citations with
   verified propositions, binding scope, and verification dates), use it
   as the primary citation source. Scope every search to the forum:
   binding authority for that district and circuit first, then persuasive
   in-circuit district decisions, then persuasive out-of-circuit
   authority, labeled as such.
2. A local authorities repository. If the user provides a path to an
   authorities repository (files describing verified cases), read and use
   it the same way: binding for the forum first, then persuasive.
3. General legal knowledge, flagged. Without a verified source, a case
   may be cited only with a `[VERIFY]` marker after the citation, and the
   draft must end with a list of every marked citation and the
   instruction to confirm each one, including that it exists, says what
   the draft claims, and remains good law, before filing.

## Rules regardless of source

- Never invent a citation, a quotation, a pin cite, or a parenthetical.
  An argument without a citation is weaker; an argument with a false one
  is sanctionable and can sink the case.
- Binding before persuasive, always. Identify the circuit and district
  before searching, and say which court each cited case comes from when
  it is not binding.
- Quotations are transcribed from the source, never reconstructed. If the
  source text is unavailable, paraphrase and cite without quotation
  marks.
- Standards and elements are the law's voice: recite them in the
  controlling authority's words with a citation, per the writing system's
  precedence rule.
- One proposition, one best citation. String cites spend the reader's
  attention; pick the binding or most recent authority and stop.

## Interface expectations (for the future authorities repository)

This skill assumes, without requiring, an authorities source that can
answer: given a jurisdiction and an issue, which verified authorities
apply, which are binding there, and what proposition each supports with a
pin cite. When that source exists as an MCP server or a repository, no
change to this skill is needed beyond its availability.
