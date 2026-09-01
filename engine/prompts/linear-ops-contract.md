# External Tracking Contract

An external tracker may mirror repository execution but never owns canon or creative
content.

## Trackable Units

- engine revision
- deterministic preflight
- one creative transaction by generation ID
- mechanical validation verdict
- artistic acceptance verdict
- static build and publication status

Do not create separate claimant, arc, scene, artifact, critique, or rewrite tasks that
imply sequential creative authorship.

## Ordering

1. update repo truth
2. complete the relevant local action
3. record its generation ID, commit, hashes, and verdict in the tracker

If tracker state conflicts with the repo or accepted manifest, the repo and manifest
win. Never store unique fictional facts, generated prose, or repair instructions only
in tracker issues.

## Statuses

Use only statuses equivalent to:

- engine_revision
- preflight
- generating_once
- mechanical_validation
- artistic_acceptance
- accepted
- rejected
- built

`rejected` is terminal for a generation ID. A fresh attempt receives a new ID; it does
not reopen the failed work for creative repair.
