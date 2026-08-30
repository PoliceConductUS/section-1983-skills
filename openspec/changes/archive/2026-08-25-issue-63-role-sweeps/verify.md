# Verification

## Focused

Command:

```text
python3 -m unittest evaluations.tests.test_role_profile_sweeps evaluations.tests.test_static_role_launcher evaluations.tests.test_skill_output_writer evaluations.tests.test_profile_conditioned_roles
```

Result: 83 tests passed.

## Full repository

Command:

```text
npm run validate
```

Result:

- Prettier check passed.
- 27 drafting tests passed.
- 555 evaluation tests passed.
- 24 installable skills were discovered.
- 29 OpenSpec items passed.
- evaluation corpus generation passed.
- governance validation passed.

## Boundary audit

- `run_role_attack` accepts one already validated fixed-role binding and
  publishes only its validated ordinary findings file and `run-receipt.yaml`.
- A sweep requires identical target bytes, hashes, task instructions, fixed role
  policy, and trusted adapter class across every profile selection.
- Every variant receives one fresh launcher process, a distinct explicit output
  folder, and only output-local `temp/` work.
- Comparison bytes are independent of input order. A failed or unavailable run
  makes the comparison incomplete and suppresses stable, subset, and flipped
  conclusions.
- A sequence binder runs only after the prior ordinary output file is durably
  published. The next binding must select that exact prior-output root, relative
  path, size, and hash as a declared read-only input.
- No package, package loader, graph, CaseGraph object, repository, ambient
  workspace, hidden conversation, or in-memory child result enters the runtime.
