# Proposal: confine temporary work to the output folder

## Why

The original output writer correctly stages beneath the explicit output root,
but it stores transient files inside the durable `.skill-runs/` receipt
namespace and does not expose a canonical process-temporary configuration. Every
invocation must instead use `<output-folder>/temp/` for all transient work and
nowhere else.

## What changes

- Reserve `temp/` as a trusted-host-only output namespace.
- Move atomic publication staging to `temp/<run-id>/`.
- Expose a process configuration whose working directory and temporary
  environment variables all select `<output-folder>/temp/`.
- Update current specifications, tests, and guidance.

## Non-goals

- Changing durable artifact paths or the `.skill-runs/<run-id>/` receipt
  namespace.
- Implementing a semantic-work launcher in this story.
- Treating environment variables as filesystem isolation.
