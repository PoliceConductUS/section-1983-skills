# Retrospective

## What remained valid

The five consumers still preserve their existing filing, authority, discovery,
target, internet, and no-strategy boundaries. Municipal-profile use adds
evidence-bounded context without deciding liability, selecting litigation
strategy, or revising a target during independent review.

## What changed during review

The first implementation made `municipal-profile` mandatory for every
invocation. Full-suite failures proved that contradicted the story's non-profile
compatibility requirement. The folder contract now declares one explicit
optional role, while each skill makes the folder mandatory whenever the task
requests profile-aware work.

Whole-story review also found that internal identifiers and upstream hashes did
not by themselves prove the three profile artifact bytes were unchanged. The
producer now records artifact hashes and the consumer validates them before use.
The adversarial validator was moved into the installed skill so isolated
installation does not depend on a repository-root script.

## Downstream rule

Future consumers may read these ordinary profile files from a declared input
folder. They must not introduce a profile package, loader, graph, repository,
ambient workspace, or temporary path outside `<output-folder>/temp/`.
