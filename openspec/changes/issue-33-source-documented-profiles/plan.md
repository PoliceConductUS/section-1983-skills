# Plan: correct Issue #33

1. Add failing tests that reject package surfaces and require direct profile
   files plus YAML source records.
2. Correct the skill, metadata, public docs, and durable specifications.
3. Replace the package-based operation test with a direct `OutputRun` workflow.
4. Remove the obsolete archived Issue #33 package design.
5. Run focused tests, full validation, archive this correction, push every
   commit, and verify the exact GitHub head before returning PR #82 to ready.
