# Design

## Context

`CONTRIBUTING.md` already describes audience, skill structure, validation, and
release ownership. `GOVERNANCE.md`, `PUBLISHING.md`, and the governance
validator already enforce adjacent concerns. Issue 20 fills only the missing
contributor norms.

## Decisions

### One contribution contract

Add concise sections for:

- one story per stacked branch;
- RED before GREEN and refactor only while tests remain green;
- OpenSpec design, tasks, verification, retrospective, and archive artifacts;
- human control over protected decisions and legal conclusions;
- measurement as feedback, never a verdict, including deltas and judgment-based
  evaluations;
- self-documenting code before comments, with short clear comments tied to an
  ADR or recorded decision when practical; and
- full validation plus immutable tagged release discipline.

### Link, do not duplicate

The guide links `GOVERNANCE.md` for protected gates and `PUBLISHING.md` for
release mechanics. It does not restate the protected-gates registry or create a
parallel release procedure.

### Deterministic validator

Add `validate_contribution_contract` to the existing governance validator. It
checks file presence, owner links, and normalized required phrases. It returns
one stable failure class. It does not evaluate prose quality, comment quality,
test quality, or legal reasoning.

### Tests

Focused tests exercise the live contract and temporary repositories. Mutations
remove or invert one enforceable rule and must produce the stable validator
failure. Existing reachability proves `npm run validate` invokes the governance
validator.

## Risks

- **Policy duplication:** link owner documents and test those links.
- **Keyword presence can accept inversion:** require bounded affirmative phrases
  and direct inverse mutations.
- **Validator becomes a style judge:** enforce only stable structural language
  and explicitly prohibit subjective scoring.
