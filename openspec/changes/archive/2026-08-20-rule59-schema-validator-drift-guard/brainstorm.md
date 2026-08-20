# Rule 59 Schema-Validator Drift Guard Brainstorm

## Approved direction

Add an automatic structural alignment test for the Rule 59 corpus schemas and
validator. Compare the public schema's required fields and controlled enums to
explicit validator constants. Keep the existing CLI and fixture tests as the
authority for semantic and cross-field behavior.

## Boundaries

- Do not implement or add a general JSON Schema engine.
- Do not infer coverage by scanning Python source text.
- Do not replace the existing behavioral validator tests.
- Do not change the public schemas or accepted corpus behavior.
- Do not add a dependency, runtime command, or separate CI workflow.

## Rejected alternatives

- Source-text field-reference scanning is brittle and cannot distinguish a
  validation rule from an incidental field access.
- Duplicating schema literals in a test would only create a third contract that
  can drift.
- Using a general schema package would not establish alignment with the custom
  semantic validator and would expand the dependency surface.
