# Approved Monell planning handoff

The drafting intake must identify the planning-record version, source
fingerprint, path IDs, exact path types, and one typed approval record for each
path. The approval record contains `status: approved`, approver identity,
approval scope, approved narrowing, decision-record path, and decision-record
SHA-256. The approver must be the litigation principal. A recommendation is not
approval and does not authorize filed allegations.

For every approved path, carry forward:

- challenged policy, custom, decision, or omission;
- supporting facts, source identities, and pleading locations;
- every proposition record, including its stable ID, text, classification,
  planned placement, and class-specific basis;
- inference classification and municipal inference;
- attribution route and implementation or transmission mechanism;
- underlying violation, particular injury, and moving-force chain;
- typed temporal lanes and information-and-belief basis;
- path-specific fields;
- contrary material, missing connections, and approved narrowing; and
- CaseGraph status and every used authority-resolution receipt.

When a path was previously `preserve-internal`, also carry forward its complete
staged-development record, the newly obtained source support, comparison to the
recorded evidence threshold, current diligence record, applicable amendment
standard, and the principal's express approval to amend. Missing threshold,
support, amendment-gate, or approval fields stop drafting for that path.

If approval is missing or ambiguous, stop that path. Do not infer approval from
the user requesting a general revision, the planner's recommendation, a
deadline, or the existence of a prior complaint.

If the current source or pleading fingerprint differs from the approved planning
record, report the stale handoff and obtain a refreshed planning or approval
record before drafting that path.
