# Retrospective

The nested `filing-packets/<packet-id>/` path was a leftover collection model,
not part of the clarified one-invocation, one-output-folder contract. Removing
the prefix also made the output easier to consume: a later invocation selects
the generated folder directly as its `filing` input.

Moving to a direct root required complete-membership validation to distinguish
packet artifacts from trusted-host receipt and temp namespaces. That distinction
now matches the profile-folder correction in the next stacked story.
