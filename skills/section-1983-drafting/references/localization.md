# Localization protocol

The document skeletons in `documents/` state the federal baseline, which is
uniform. Districts and individual judges layer requirements on top, and those
cannot be authored in advance. This file encodes the shape of that variation as
a checklist. Run it once per district, cache the answers, and reuse them.

## Step 1: Identify the forum

The district, the division, the assigned district judge, and the assigned
magistrate judge. All four can carry their own rules.

## Step 2: Check available caches

First use a project-defined localization or local-rules cache. A bundled
`jurisdictions/<district-slug>.md` file may be used as a retrieval lead if it is
current, but an installed skill directory is not the user's case workspace. Do
not write to or commit changes inside an installed skill package.

## Step 3: Fetch the sources

- The district's local civil rules, from the district court's website.
- The assigned judges' practice standards or standing orders, from their pages
  on the same site.
- The district's pro se guide, if one exists.

## Step 4: Answer the checklist

For the district and, where they speak, the assigned judges:

1. Response deadlines: days to respond to dispositive and nondispositive
   motions, and how the district counts them.
2. Length limits: pages or words, per document type, and whether a certificate
   of compliance is required.
3. Motion mechanics: is a separate memorandum or brief required alongside the
   motion; is a proposed order required; is a meet-and-confer with a certificate
   required, and for which motions.
4. Summary judgment format: the exact required form of the fact statement and
   the response to it (numbered paragraphs, record citations, admit/deny
   format), since this is the most district-specific document in the case.
5. Amendment mechanics: whether a motion for leave must attach the proposed
   amended pleading, and whether a redline is required.
6. Filing mechanics for a pro se party: paper or electronic filing, whether ECF
   access is available on request, courtesy copies, and how service on the
   plaintiff runs (mail or ECF notice).
7. Anything the assigned judge's standing orders add or change.

## Step 5: Preserve the localization result

If the project defines a localization-cache path, write the answers there, one
section per checklist item, each with a citation to the local rule or standing
order and the date checked. Otherwise return the completed checklist as an
internal audit and ask before creating a durable project file. Do not invent a
repository path, edit the installed skill tree, commit, or push unless the user
separately authorizes that repository action.

## Step 6: Apply it

Every document drafted for that forum gets a final pass against the cache file.
Deadlines and length limits from the cache override the federal baseline in the
skeletons whenever they are stricter.
