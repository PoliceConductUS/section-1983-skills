# Design: canonical temp guidance

The first-hour sequence keeps its existing six steps. Step 1 identifies the
caller-selected absolute output root and the stop-and-ask rule. Step 4 explains
the trusted-host configuration and operating-system isolation. Step 6 verifies
that transient work remains under `temp/` and that durable artifacts do not use
that namespace.

The deterministic documentation test executes the real `OutputRun`, inspects its
process configuration, and verifies the reserved namespace. This proves the
guide and executable contract remain aligned without introducing a universal
runner.
