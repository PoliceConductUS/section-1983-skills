# Issue #65 — explicit output persistence

This OpenSpec change implements PoliceConductUS/section-1983-skills Issue #65 on
top of Issue #64's folder-scoped invocation contract. It owns atomic,
create-exclusive artifact publication and reproducible run receipts inside the
caller-declared output folder. It does not add repository, graph, or external
persistence dependencies.
