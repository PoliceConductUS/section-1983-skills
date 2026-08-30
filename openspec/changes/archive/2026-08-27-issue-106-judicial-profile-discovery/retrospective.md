# Retrospective: issue-106-judicial-profile-discovery

> Written: 2026-08-26 (after verification passed with one review warning)  
> Commit range:
> `c9191aeb657f41c044d6efce483e88eca8f2c19f..224a7c4c469b98d546c62ccf8d4a610e7a9e27e5`  
> Worktree:
> `/Users/dalelotts/dev/PoliceConductUS/section-1983-skills/.worktrees/issue-106-judicial-profile-discovery`

## 0. Evidence

- **Commit range**: four pre-retrospective feature commits
- **Diff size**: 488 inserted lines across 12 files before verification and
  retrospective artifacts
- **Tasks done**: 7/9 at write time; the remaining two are archive and external
  readiness lifecycle steps
- **Active hours**: less than one
- **Subagent dispatches**: 0
- **New external dependencies**: none
- **Bugs encountered post-merge**: none; the branch remains unmerged
- **OpenSpec validate state at archive**: pre-archive pass, 39/39 items
- **Test coverage signal**: 27 unit tests and 652 evaluation tests passed; 29
  skills were install-local discoverable

Commit chain:

```text
473ccc2 docs: design judicial profile case discovery
23fa184 test: require judicial profile case discovery contract
eb2deb1 feat: add judicial profile case discovery guidance
224a7c4 chore: format judicial discovery change
```

## 1. Wins

- The RED commit `23fa184` proved that the installed skill lacked the approved
  discovery and authorization contracts before implementation.
- `eb2deb1` kept the change at the public skill seam: no network client,
  credential store, persistence layer, graph, or new dependency was added.
- The builder, source documentation, and public guide now agree on judge-first
  discovery, relationship distinctions, primary-document verification, candidate
  dispositions, and runtime-only secrets.
- Fresh `npm run validate` passed every repository gate recorded in `verify.md`.

## 2. Misses

- 🟡 **Painful**: no fresh agent-behavior pressure review ran. The deterministic
  instruction contract is tested, but this cycle cannot claim evidence about a
  fresh agent following it under pressure.
- 📌 **Nit**: the first full validation exposed the guide's intentional
  repository-relative link allowlist when the new external documentation link
  was added. The guide now names the API without adding an external Markdown
  link; the skill retains the official documentation link.
- 📌 **Nit**: the first full validation also required formatting seven changed
  Markdown files before the green repository run.

## 3. Plan deviations

| Plan task                   | What changed                                                                   | Why                                                                                                  |
| --------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| Fresh skill pressure review | Replaced by deterministic install-local contract tests and an explicit warning | New subagent dispatches were not authorized in this task.                                            |
| Public guide API citation   | Kept as text rather than a live external Markdown link                         | The guide's tested navigation surface intentionally permits only confined repository-relative links. |

## 4. Skill and workflow compliance

| Skill                                        | Used |
| -------------------------------------------- | ---- |
| `superpowers:brainstorming`                  | ✓    |
| `superpowers:writing-plans`                  | ✗    |
| `superpowers:using-git-worktrees`            | ✓    |
| `superpowers:subagent-driven-development`    | ✗    |
| `superpowers:test-driven-development`        | ✓    |
| `superpowers:requesting-code-review`         | ✗    |
| `superpowers:finishing-a-development-branch` | ✓    |

### Deliberately skipped skills

- **`superpowers:writing-plans`**
  - **What was skipped**: the standalone skill invocation before implementation;
    the approved design was still converted into `plan.md` and `tasks.md`.
  - **Why this cycle**: implementation resumed from an already approved bounded
    design and OpenSpec artifact sequence, and the standalone invocation was
    omitted before commit `23fa184`.
  - **How to prevent recurrence**: `CLAUDE.md trigger` — require the writing-
    plans skill explicitly before creating `plan.md`, even for a bounded change.
- **`superpowers:subagent-driven-development`**
  - **What was skipped**: fresh implementer and per-task reviewer subagents.
  - **Why this cycle**: the active controller prohibited spawning new agents
    without explicit user authorization, and this issue approval did not grant
    that authority.
  - **How to prevent recurrence**: `scope-judgment rule` — when a selected
    OpenSpec schema requires subagents but the controller requires explicit
    authorization, request that authorization before apply or select a
    non-subagent schema before creating the change.
- **`superpowers:requesting-code-review`**
  - **What was skipped**: the required independent reviewer subagent; the
    primary agent performed the spec-to-diff review instead.
  - **Why this cycle**: the same no-new-subagent controller boundary applied at
    final review.
  - **How to prevent recurrence**: `scope-judgment rule` — obtain explicit
    reviewer-agent authorization before apply when this schema is selected.

## 5. Surprises

- The public judge-overlay guide has a stricter link surface than ordinary
  repository Markdown: its test requires an exact set of confined relative
  destinations.
- OpenSpec's generated lifecycle asks task completion verification to occur
  before the retrospective and archive tasks can truthfully be completed. The
  verification report therefore identifies those two lifecycle tasks explicitly
  instead of representing them as already done.

## 6. Promote candidates to long-term learning

- [ ] 🟡 **Resolve controller authorization before selecting a subagent-required
      schema** → **Promote to schema**

  > **Why**: This cycle produced deterministic coverage but could not run the
  > schema's independent pressure and review agents. **How to apply**: At
  > OpenSpec change creation, fail early or choose a compatible schema when
  > agent dispatch is not expressly authorized.

- [ ] 📌 **Keep strict public-guide navigation links distinct from source
      citations** → **Promote to project instructions**
  > **Why**: `test_judge_overlay_guide` rejected a new official external link
  > because the guide intentionally exposes an exact relative-link set. **How to
  > apply**: Before adding an external Markdown link to a top-level guide,
  > inspect its navigation/link-guard tests and place the citation in the
  > installable skill when appropriate.
