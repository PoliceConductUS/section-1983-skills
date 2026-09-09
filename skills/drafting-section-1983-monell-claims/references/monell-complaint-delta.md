# Monell complaint delta

## Typed delta

Return one object for every approved path with its `path_id`, one `path_type`,
target count, target factual and count paragraphs, proposed paragraph text,
source locations, the complete carried-forward `propositions` collection, and
all version-2 common and path-specific fields. Preserve each proposition's
stable ID and classification. Set its placement to `complaint` or
`discovery_plan` under the rule below.

The filed prose must state:

1. the challenged policy, custom, decision, or omission;
2. concrete facts and their source-bounded classification;
3. the reasonable municipal inference;
4. the legally required attribution route;
5. any implementation or transmission mechanism;
6. the underlying constitutional violation;
7. the particular injury; and
8. why the policy or mechanism was the moving force causing that particular
   injury.

Do not plead a mechanism as a freestanding path; contract version 2 has no FTO,
review, handoff, or implementation path type. Authority suggesting a new path
requires replanning and an approved contract change. Multiple employees making
the same policy statement may support a reasonable practice inference; it does
not by itself establish final-policymaker identity or authority.

Do not plead boilerplate, the underlying incident alone, or an expected-
discovery proposition as a speculative placeholder merely to preserve a Monell
path. Plead only the narrowest factually plausible formulation approved on the
current record. A previously preserved internal path may enter the typed delta
only after its path-specific evidence threshold is met, current source support
is recorded, the applicable amendment gate is satisfied, and the litigation
principal approves amendment.

## Proposition placement

Every Monell paragraph must distinguish source-documented facts, supported
inferences drawn from identified pleaded facts, and expected-discovery
propositions. The complaint may allege source-documented facts and supported
inferences, with attribution, temporal limits, and the inference's factual
basis. Expected-discovery propositions are not present facts or evidence and
belong in the discovery plan. A supporting brief may explain why the pleaded
facts support a reasonable inference, but it may not supply a missing complaint-
level factual basis.

Treat a complete information-and-belief allegation as a supported inference, not
as expected discovery, only when the known facts and every required basis field
below support it. The fact that a municipality controls identified records does
not establish the expected contents of those records.

For an approved `formal_policy` path based on repeated statements and repeated
implementation, preserve that approved type. Plead the repeated words, actors,
duration, and implementation first, then the narrow inference that they were
applying a municipal rule. Put unknown policy text, operative status, source, or
adopting authority into the typed information-and-belief basis, preserve each as
an unresolved connection, and do not invent a written policy or policymaker. Do
not silently retype the approved path as `custom_or_practice`.

## Information and belief

Use an `information_and_belief_basis` object with `used`, `known_facts`,
`expected_information`, `controller`, `inference`, and `affected_fields`. When
`used` is true, every other field is required. The known facts and controlled
information must be concrete; the phrase cannot replace a missing basis.

## Time

Use a `temporal_lanes` collection and map every supporting fact to one or more
of `pre_event_notice`, `event_implementation`, `post_event_ratification`,
`recurrence`, `later_injury`, or `corroboration`. Post-event notice,
ratification, recurrence, later injury, or corroboration cannot supply pre-event
causation or pre-event notice. A later event may corroborate an already-existing
training, FTO, review, or handoff mechanism only when the supporting facts and
inference are pleaded without treating the later event as retroactive notice.

## Authority receipt

Every CaseGraph-used authority must have status `resolved`. Any `missing`,
`hash_mismatch`, `pinpoint_unresolved`, `text_mismatch`, or `ambiguous_match`
status makes the dependent drafted component incomplete and unusable. A derived
text representation requires verified provenance to the hashed canonical
opinion. Fuzzy or semantic matching cannot replace an exact passage at the cited
pinpoint.

## Integration receipt

Identify every added or revised paragraph and the typed v2 path object it
implements. Map every complaint proposition to its integrated paragraph and
every expected-discovery proposition to its discovery-plan location. List
unresolved planning conditions and do not draft them as facts. After the
canonical complaint owner integrates the delta, update the document fingerprint
and rerun the version-2 validator.
