# Legal Filing Tooling Backlog Design

## Goal

Work through PoliceConductUS organization Project 1 in project order. Add only
the items that logically belong in this public Section 1983 skills repository,
and leave a GitHub issue comment recommending an owning repository for each
skipped general-purpose tool.

## Delivery structure

Use an ordered Git Town stack rooted at `main`:

1. `codex/project-1-bootstrap`
2. `codex/issue-1-filing-ci`
3. `codex/issue-6-drafting-evaluations`
4. `codex/issue-7-adversarial-review`
5. `codex/issue-8-discovery-suite`
6. `codex/issue-9-declaration-evidence`
7. `codex/issue-14-governance`
8. `codex/issue-15-rule-59-corpus`

Keep one linked worktree for every branch under `.worktrees/<branch-slug>`.
Each issue branch must contain only that backlog item's OpenSpec artifacts,
implementation, tests, and documentation on top of its parent branch.

Do not merge, close issues, or change GitHub Project status. Commit completed
work locally. Add external comments only to issues skipped under the routing
boundary below.

## Workflow

The bootstrap branch installs the repository-local OpenSpec configuration and
the `superpowers-bridge` schema used by the PoliceConductUS template repositories.
It also records repository instructions and validation commands needed by later
branches.

For every eligible issue:

1. Create the issue branch and worktree from the preceding eligible branch.
2. Create the OpenSpec change before implementation.
3. Work in vertical red-green TDD slices at the approved public seams.
4. Validate the skill or command through its public interface.
5. Complete the bridge verification and retrospective artifacts.
6. Commit the complete issue change before starting the next project item.

## Public test seams

### Skills

The public seam is an installed skill invoked by a fresh-context agent against
synthetic litigation materials. Pressure scenarios must exercise the decisions
and safety boundaries in the issue acceptance criteria. Tests must inspect the
agent's resulting work product, not wording or internal reasoning.

### Deterministic scripts and evaluation tools

The public seam is the command-line interface. Standard-library `unittest`
tests must verify exit status, machine-readable output, and observable files.
Mock only external agent runners or checker executables. Do not mock repository
modules that the command controls.

### Repository governance

The public seam is the documented contributor workflow plus commands executed
by continuous integration. A proposed weakening of a protected verification,
source, permission, or filing-readiness gate must be visible to an explicit
reviewer rather than passing as an ordinary unreviewed edit.

## Ordered backlog disposition

### Issue 1: implement here

Create a thin Filing CI orchestration skill. It invokes a project-configured
filing-integrity executable and treats missing configuration, unavailable
execution, or unresolved hard findings as an open filing gate. Tests use a fake
checker executable at the external process boundary and confirm that the skill
does not edit the filing or invent a path.

### Issues 2 through 5: route out

These issues define a reusable filing checker, verified-authority store,
structured-source compiler, and court-formatting compiler. Recommend a new
`PoliceConductUS/filing-toolchain` repository. This skills repository should
retain only thin orchestration skills once those tools expose stable public
interfaces.

### Issue 6: implement here

Create repository-owned drafting-skill regression evaluations. Deterministic
graders operate on synthetic fixtures. Judgment graders use a configurable
fresh-context runner and repeat samples so the report exposes variance. Private
case data must not enter fixtures.

### Issue 7: implement here

Create the independent adversarial filing-review skill. Its fresh reviewer sees
only the canonical draft and approved sources. Its output classifies defects and
arguments and supplies attacked text plus a copy-ready replacement without
silently editing the canonical filing or deciding reserved strategy questions.

### Issue 8: implement here

Decompose the discovery epic inside its OpenSpec change before implementation.
Deliver separately invocable and separately tested skills for written discovery,
response and objection audit, meet-and-confer correspondence, privilege logs,
and deposition outlines. Every generated request maps to the required claim,
defendant, element, gap, custodian, and expected native source.

### Issue 9: implement here

Create the declaration-and-evidence skill contract. It separates firsthand
facts, attributed records, derived analysis, inference, and legal conclusion;
checks personal knowledge and foundation; and requires human approval of every
statement before execution.

### Issues 10 and 11: route out

These are reusable declaration and evidence-timeline compilers. Recommend a new
`PoliceConductUS/legal-evidence-tooling` repository with thin invocation skills
added here after stable interfaces exist.

### Issues 12 and 13: route out

The deadline engine and versioned jurisdiction rule packs are shared legal
infrastructure. Recommend a new `PoliceConductUS/court-rules` repository that
owns the calculator, source provenance, versioned packs, and calendar export.

### Issue 14: implement here

Add repository-wide judgment-routing and rules-freshness governance. The change
must reserve strategy to the user, require sourced and freshness-dated
jurisdiction propositions, identify thin-wrapper ownership boundaries, and make
gate weakening subject to explicit review.

### Issue 15: implement here

Publish the Rule 59 decision-corpus schema and coding contract used by the
existing study skill. Include neutral synthetic fixtures, deterministic
validation, missing-document and denominator limits, and a neutral transfer-card
format without private case material.

## Failure handling

Fail an issue branch visibly when its OpenSpec change, public-seam tests, skill
validation, formatting, or repository validation does not pass. Do not call the
branch complete or start its dependent child branch until the failure is fixed.
An unavailable external checker or agent runner remains an explicit open gate;
it is never converted into a passing result.

## Scope boundaries

Do not implement the skipped general-purpose packages in this repository. Do
not add compatibility paths, fallback behavior, provider-specific agent code,
private case material, automatic filing, automatic signing, or automatic
calendar mutation. Do not silently choose legal strategy for the user.
