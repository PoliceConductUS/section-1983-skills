## 1. RED alignment contract

- [ ] 1.1 Add a focused test that inventories every schema required-field and
      enum node and maps each node to one validator constant.
- [ ] 1.2 Prove mismatches report the contract and one-sided values.
- [ ] 1.3 Run the test and confirm it fails because inline validator enums do
      not yet expose the required comparison constants.
- [ ] 1.4 Commit the RED test and sync the child branch.

## 2. GREEN validator seam

- [ ] 2.1 Extract named constants for every currently inline schema-controlled
      enum and the study date-range required fields without changing any value.
- [ ] 2.2 Reuse those constants at the existing controlled-value call sites.
- [ ] 2.3 Run the focused alignment and Rule 59 corpus suites.
- [ ] 2.4 Commit the GREEN refactor and sync the child branch.

## 3. Verification and archive

- [ ] 3.1 Run all evaluation tests and the full repository validation chain.
- [ ] 3.2 Run OpenSpec, compile, formatting, diff, forbidden-folder, and comment
      checks.
- [ ] 3.3 Record verification and retrospective artifacts.
- [ ] 3.4 Archive the OpenSpec change, commit, and sync the child branch.
