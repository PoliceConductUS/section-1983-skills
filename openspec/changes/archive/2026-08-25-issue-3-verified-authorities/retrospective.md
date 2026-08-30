# Retrospective

## What changed

Issue #3 now provides an offline verified-authority audit over one selected
filing and one recursively available authority folder. Strict corpus, authority,
and source YAML bind exact ordinary opinion bytes, while a pinned eyecite
integration supplies citation candidates and antecedent resolution only.

## What the review caught

The first green implementation checked quotation and pinpoint presence
independently. Review added page-delimited pinpoint segments so a quotation on a
different page cannot pass. It also added explicit persistent-markup resolution
to authority YAML, source YAML, and opinion paths, and removed ordinary-audit
language that could imply web research.

## Result

Authority auditing is independent of packages and graphs. Caller folders define
scope, YAML documents selected sources, eyecite supplies only extraction, and
the explicit output folder owns every durable and transient write.
