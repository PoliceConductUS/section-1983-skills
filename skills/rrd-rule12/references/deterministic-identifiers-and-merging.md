# Deterministic Identifiers and Idempotent Merging

## Step 2 — Idempotence + Deterministic IDs (Required)

### Why this matters

If this skill is re-run after edits or after the movant files a reply, you need
the generator to **update** rather than create duplicates. That requires
**stable, deterministic IDs**.

### Deterministic ID Rules (MUST)

All generated objects that can repeat across runs MUST have a deterministic `id`
based on a **fingerprint hash**.

Objects that MUST have deterministic IDs:

- `response_units[]`
- `strategic_arguments_library.arguments[]`
- `argument_map[]` items (if you keep them as discrete objects)
- `video_dispute_map[]` items (when present)
- `risk_register[]` items (optional but recommended)
- `amendment_handoff[]`

### Fingerprint

A fingerprint is a _stable_ string derived from the essence of the thing, then
hashed.

**Normalization rules:**

- lowercase
- trim whitespace
- collapse internal whitespace to a single space
- remove punctuation that does not affect meaning (keep slashes, hyphens)
- do **not** include ordering/sequence numbers
- do **not** include timestamps like “generated_at”

**Hash rule:**

- `sha256(fingerprint)` → take the first 10 hex chars → uppercase
- Use that as an ID suffix.

### ID formats

- Response Units: `RU-<HASH10>`
- Strategic arguments: `SA-<HASH10>`
- Video dispute map items: `VDM-<HASH10>`
- Risks: `RISK-<HASH10>`
- Argument map entries: `AM-<HASH10>`
- Amendment handoffs: `AH-<HASH10>`

### Fingerprint recipes (canonical)

These are the default recipes; if the user supplies claim IDs from a `claims/`
folder, prefer those keys.

**Response Unit fingerprint:**

```
ru|<motion_key>|<claim_key>|<defendant_key>|<event_stage>|<challenged_conduct>|<movant_cluster_key>|<attacked_issue_key>
```

**Strategic argument fingerprint:**

```
sa|<motion_key>|<legal_theory_key>|<proposition_normalized>
```

**Video dispute map fingerprint:**

```
vdm|<motion_key>|<issue_key>|<timestamp>|<plaintiff_allegation_normalized>|<defense_claim_normalized>
```

**Risk fingerprint:**

```
risk|<motion_key>|<risk_key>|<risk_statement_normalized>
```

**Argument map fingerprint:**

```
am|<motion_key>|<movant_heading_normalized>|<targeted_claim_key>|<defense_type_key>
```

**Amendment handoff fingerprint:**

```
ah|<motion_key>|<motion_or_ruling_premise>|<claim_key>|<defendant_key>|<event_stage>|<exact_defect_normalized>
```

### Merge rules (idempotent updates)

When `rrd.yaml` already exists, the generator MUST:

1. Parse existing YAML.
2. Build an index by `id` for all deterministic objects.
3. For each newly generated object:
   - If `id` exists → **update** machine-managed fields; preserve user notes.
   - If `id` does not exist → **append**.
4. For objects present in the old file but not regenerated:
   - Keep them, but mark with `status: stale` (do not delete automatically).

Apply these same update-by-ID and stale-item rules to `amendment_handoff[]`; do
not duplicate a cure when its deterministic ID already exists.

**User-preserved fields** (never overwrite on a regenerated object if present):

- `user_notes`
- `status` (unless it is missing; default to `draft`)
- `worklog`
- `owner`
- any field under a `manual:` subtree (reserved)

The generated transition from an item no longer produced to `status: stale` is
the sole exception to status preservation. If the item is produced again,
restore its last non-stale user status when recorded; otherwise use the schema
default.

---
