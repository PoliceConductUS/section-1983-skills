# Proposal: correct Judicial Reasoning Profile persistence

## Why

The implemented builder correctly separated behavior from participant data but
published and consumed that data through the now-removed package layer. Issue
#33 must use the folder/YAML contract established by corrected Issue #68.

## What Changes

- Replace the install-local package reference with source-documented-folder
  guidance.
- Make acquisition return ordinary source bytes plus `SOURCE.yaml` records.
- Make compilation return `judicial-profile.json`,
  `judicial-profile-sources.yaml`, and `validation-receipt.json` through the
  shared output writer.
- Remove every package helper import and package-shaped test assertion.
- Correct active specifications, public docs, discovery metadata, and the
  archived wrong Issue #33 change.

## Preserved behavior

- source-class separation and attribution rules;
- no averaging, mind-reading, manipulation, voice imitation, or outcome
  prediction;
- neutral transfers only from independently reasoned revealed reasoning;
- profile data cannot alter protected behavior; and
- no real-participant skills.
