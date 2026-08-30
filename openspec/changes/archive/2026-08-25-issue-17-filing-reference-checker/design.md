# Design: Installed filing reference checker completion

## Existing milestone

The installed `filing-ci` skill already owns `scripts/run_filing_ci.py` and its
fixed complaint-checker contract. The trusted host validates selected ordinary
files and domain YAML from `filing-source`, `filing-index`, `record-reference`,
`exhibit`, `docket-to-appendix`, and `verified-authority`, constructs bounded
in-memory context, calls the installed checker, and publishes deterministic
JSON, Markdown, and receipt files beneath the explicit output folder.

Issue #17 does not duplicate that implementation. It records this first
milestone under its own story and closes one strictness gap found during
whole-story review.

## Date strictness

Python accepts some compact ISO-compatible date spellings. Domain YAML requires
the canonical `YYYY-MM-DD` spelling because the exact date text participates in
deterministic source documentation. The validator parses the date and compares
`parsed.isoformat()` with the supplied value. A mismatch is `invalid`, creates
no output, and does not invoke the semantic checker.

The current comparison is accidentally indented after an earlier function's
unconditional return, so it never runs. The implementation moves it back into
the date validator. A RED test uses `20260825`, which is parseable on the
supported interpreter but noncanonical.

## Filesystem and judgment boundary

The change adds no input role and no filesystem authority. Inputs remain
recursive read-only folders. Durable reports stay beneath the exact output
folder; every temporary path stays beneath `<output-folder>/temp/`. Internet is
disabled. The checker remains mechanical and does not decide truth, legal
sufficiency, authority quality, strategy, filing readiness, or correction.
